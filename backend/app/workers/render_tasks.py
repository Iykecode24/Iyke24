import asyncio
import uuid
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update, or_
from app.workers.celery_app import celery_app
from app.database import async_session_maker
from app.models.render_job import RenderJob, RenderStatus, JobType
from app.models.gpu_instance import GpuInstance, GpuStatus
from app.models.media import FinalVideo, VideoClip, AudioFile
from app.services.runpod_service import RunPodService
from app.integrations.runpod_client import RunPodClient
from app.services.editing_service import EditingService
from app.services.audio_pipeline import AudioPipeline
from app.config import settings
import tempfile
import os
import shutil

logger = logging.getLogger(__name__)

async def _ephemeral_render_pipeline(job_id_str: str):
    """
    Serverless Ephemeral Rendering:
    (a) Creates a Pod
    (b) Mounts the volume
    (c) Executes rendering
    (d) Uploads to Cloudflare R2
    (e) Instantly destroys the pod to save costs
    """
    job_id = uuid.UUID(job_id_str)
    
    client = RunPodClient(api_key=settings.RUNPOD_API_KEY)
    service = RunPodService(client)
    
    async with async_session_maker() as session:
        stmt = select(RenderJob).where(RenderJob.id == job_id)
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()
        
        if not job:
            logger.error(f"RenderJob {job_id} not found")
            return
            
        instance = None
        try:
            job.status = RenderStatus.starting_gpu
            await session.commit()
            
            # (a) Creates a Pod and (b) Mounts the volume
            volume_id = await service.ensure_network_volume()
            
            gpu_type = job.gpu_type or "NVIDIA GeForce RTX 4090"
            instance = await service.provision_gpu(
                session=session,
                name=f"ephemeral-render-{job_id}",
                image="runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel",
                gpu_type=gpu_type,
                volume_id=volume_id
            )
            
            job.gpu_instance_id = instance.id
            job.status = RenderStatus.rendering
            await session.commit()
            
            # Wait for pod to be fully running
            await asyncio.sleep(10)
            
            # Fetch AudioFiles for the job's project to ingest into Lip-Sync
            audio_stmt = select(AudioFile).where(AudioFile.project_id == job.project_id)
            audio_result = await session.execute(audio_stmt)
            audio_files = audio_result.scalars().all()
            
            audio_urls = " ".join([af.url for af in audio_files if af.url])
            audio_args = f"--audio-urls {audio_urls}" if audio_urls else ""
            
            # (c) Executes rendering (mocked script)
            logger.info(f"Executing rendering on pod {instance.provider_instance_id} with audio {audio_urls}")
            render_script = (
                f"echo 'Starting render for job {job_id}...' && "
                f"mkdir -p /workspace/output/{job_id} && "
                f"python render.py --job {job_id} {audio_args} && "
                f"touch /workspace/output/{job_id}/final.mp4"
            )
            await client.run_command_in_pod(instance.provider_instance_id, render_script)
            
            job.status = RenderStatus.uploading
            await session.commit()
            
            # (d) Uploads to Cloudflare R2 (mocked upload script)
            logger.info(f"Uploading to Cloudflare R2 from pod {instance.provider_instance_id}")
            upload_script = (
                f"echo 'Uploading /workspace/output/{job_id}/final.mp4 to R2...' && "
                f"sleep 2"
            )
            await client.run_command_in_pod(instance.provider_instance_id, upload_script)
            
            # Update job state
            final_url = f"https://r2.example.com/projects/{job.project_id}/final.mp4"
            job.output_url = final_url
            job.status = RenderStatus.completed
            job.progress_percent = 100.0
            job.completed_at = datetime.now(timezone.utc)
            await session.commit()
            logger.info(f"Ephemeral render job {job_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Ephemeral render failed for job {job_id}: {e}")
            job.status = RenderStatus.failed
            job.error_message = str(e)
            job.completed_at = datetime.now(timezone.utc)
            await session.commit()
        finally:
            # (e) Instantly destroys the pod to save costs
            if instance:
                logger.info(f"Instantly terminating pod {instance.provider_instance_id} to save costs")
                try:
                    await service.terminate_gpu(session, instance.id)
                except Exception as e:
                    logger.error(f"Failed to terminate pod {instance.provider_instance_id}: {e}")

@celery_app.task
def start_render_task(job_id: str):
    asyncio.run(_ephemeral_render_pipeline(job_id))

@celery_app.task
def check_render_progress_task(job_id: str):
    pass

async def _gpu_lifecycle_logic(job_id_str: str):
    job_id = uuid.UUID(job_id_str)
    client = RunPodClient(api_key=settings.RUNPOD_API_KEY)
    service = RunPodService(client)

    async with async_session_maker() as session:
        # Get the job
        stmt = select(RenderJob).where(RenderJob.id == job_id)
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()
        
        if not job:
            logger.error(f"RenderJob {job_id} not found")
            return

        try:
            job.status = RenderStatus.starting_gpu
            await session.commit()

            # Need to provision or find a GPU
            gpu_type = job.gpu_type or "NVIDIA GeForce RTX 4090"
            
            # Check for existing stopped or running instance we can reuse
            stmt = select(GpuInstance).where(
                GpuInstance.gpu_type == gpu_type,
                GpuInstance.status.in_([GpuStatus.stopped, GpuStatus.running])
            )
            result = await session.execute(stmt)
            instance = result.scalars().first()

            if instance:
                if instance.status == GpuStatus.stopped:
                    instance = await service.start_gpu(session, instance.id)
            else:
                instance = await service.provision_gpu(
                    session=session,
                    name=f"render-gpu-{job_id}",
                    image="runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel",
                    gpu_type=gpu_type
                )
            
            job.gpu_instance_id = instance.id
            job.status = RenderStatus.loading_model
            await session.commit()
            logger.info(f"Successfully provisioned/started GPU for job {job_id}")

        except Exception as e:
            logger.error(f"Failed to provision GPU for job {job_id}: {e}")
            job.status = RenderStatus.failed
            job.error_message = str(e)
            await session.commit()

@celery_app.task
def gpu_lifecycle_task(job_id: str):
    """
    Handles provisioning a GPU via RunPodService based on a render job.
    """
    asyncio.run(_gpu_lifecycle_logic(job_id))

async def _emergency_shutdown_logic():
    client = RunPodClient(api_key=settings.RUNPOD_API_KEY)
    service = RunPodService(client)

    async with async_session_maker() as session:
        # Find GPUs running for more than 2 hours or some criteria
        # Let's say: running but no active jobs associated
        
        # We find running instances
        stmt = select(GpuInstance).where(GpuInstance.status == GpuStatus.running)
        result = await session.execute(stmt)
        running_instances = result.scalars().all()
        
        for instance in running_instances:
            # Check if there are active jobs for this instance
            active_jobs_stmt = select(RenderJob).where(
                RenderJob.gpu_instance_id == instance.id,
                RenderJob.status.in_([
                    RenderStatus.queued, RenderStatus.preparing, 
                    RenderStatus.starting_gpu, RenderStatus.loading_model, 
                    RenderStatus.rendering, RenderStatus.processing_audio, 
                    RenderStatus.lip_syncing, RenderStatus.stitching, 
                    RenderStatus.upscaling, RenderStatus.uploading
                ])
            )
            result = await session.execute(active_jobs_stmt)
            active_jobs = result.scalars().all()
            
            # If no active jobs and it has been running for more than 15 minutes, stop it
            if not active_jobs and instance.started_at:
                running_time = datetime.now(timezone.utc) - instance.started_at
                if running_time > timedelta(minutes=15):
                    logger.warning(f"Emergency shutdown: stopping idle GPU {instance.id}")
                    try:
                        await service.stop_gpu(session, instance.id)
                    except Exception as e:
                        logger.error(f"Failed to shutdown GPU {instance.id}: {e}")

@celery_app.task
def emergency_shutdown_task():
    """
    Stops GPUs that have been running too long without active jobs.
    """
    asyncio.run(_emergency_shutdown_logic())
