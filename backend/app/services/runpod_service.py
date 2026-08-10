import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.gpu_instance import GpuInstance, GpuStatus
from app.integrations.runpod_client import RunPodClient, Pod, PodStatus

logger = logging.getLogger(__name__)

class RunPodService:
    """
    Service for managing RunPod GPU instances dynamically.
    """
    def __init__(self, client: RunPodClient):
        self.client = client
        self.network_volume_name = "IykeStudio-NetworkVolume"
        self.network_volume_size = 500

    async def ensure_network_volume(self) -> str:
        """
        Auto-detects or creates a 500GB network volume named "IykeStudio-NetworkVolume".
        Returns the volume ID.
        """
        logger.info(f"Ensuring network volume '{self.network_volume_name}' exists...")
        volumes = await self.client.list_network_volumes()
        
        for vol in volumes:
            if vol.name == self.network_volume_name:
                logger.info(f"Found existing volume: {vol.id}")
                return vol.id
                
        logger.info(f"Creating new volume: {self.network_volume_name} ({self.network_volume_size}GB)")
        new_vol = await self.client.create_network_volume(
            name=self.network_volume_name,
            size_gb=self.network_volume_size
        )
        return new_vol.id

    async def initialize_volume(self, pod_id: str) -> None:
        """
        Builds the required directory tree on the volume.
        Assumes the volume is mounted at /workspace
        """
        logger.info(f"Initializing directory tree on volume for pod {pod_id}...")
        init_script = (
            "mkdir -p /workspace/models/checkpoints && "
            "mkdir -p /workspace/models/loras && "
            "mkdir -p /workspace/models/controlnet && "
            "mkdir -p /workspace/comfyui/custom_nodes && "
            "mkdir -p /workspace/output && "
            "echo 'Volume initialized'"
        )
        await self.client.run_command_in_pod(pod_id, init_script)

    async def provision_gpu(
        self,
        session: AsyncSession,
        name: str,
        image: str,
        gpu_type: str,
        volume_id: Optional[str] = None
    ) -> GpuInstance:
        """
        Provisions a new GPU pod on RunPod and records it in the database.
        """
        logger.info(f"Provisioning RunPod GPU: {name} ({gpu_type})")
        try:
            pod = await self.client.create_pod(
                name=name,
                image=image,
                gpu_type=gpu_type,
                volume_id=volume_id
            )
            
            instance = GpuInstance(
                id=uuid.uuid4(),
                provider="runpod",
                provider_instance_id=pod.id,
                gpu_type=pod.gpu_type,
                gpu_count=pod.gpu_count,
                status=GpuStatus.creating,
                pod_name=pod.name,
                cost_per_hour=pod.cost_per_hour,
                network_volume_id=pod.volume_id,
                started_at=datetime.now(timezone.utc)
            )
            
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            
            return instance
        except Exception as e:
            logger.error(f"Failed to provision GPU: {e}")
            raise

    async def start_gpu(self, session: AsyncSession, instance_id: uuid.UUID) -> GpuInstance:
        """
        Starts an existing stopped GPU pod.
        """
        stmt = select(GpuInstance).where(GpuInstance.id == instance_id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        
        if not instance:
            raise ValueError(f"GPU Instance {instance_id} not found")
            
        logger.info(f"Starting RunPod GPU: {instance.provider_instance_id}")
        await self.client.start_pod(instance.provider_instance_id)
        
        instance.status = GpuStatus.running
        instance.started_at = datetime.now(timezone.utc)
        instance.stopped_at = None
        
        await session.commit()
        await session.refresh(instance)
        
        return instance

    async def stop_gpu(self, session: AsyncSession, instance_id: uuid.UUID) -> GpuInstance:
        """
        Stops a running GPU pod.
        """
        stmt = select(GpuInstance).where(GpuInstance.id == instance_id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        
        if not instance:
            raise ValueError(f"GPU Instance {instance_id} not found")
            
        logger.info(f"Stopping RunPod GPU: {instance.provider_instance_id}")
        await self.client.stop_pod(instance.provider_instance_id)
        
        instance.status = GpuStatus.stopped
        instance.stopped_at = datetime.now(timezone.utc)
        
        await session.commit()
        await session.refresh(instance)
        
        return instance

    async def terminate_gpu(self, session: AsyncSession, instance_id: uuid.UUID) -> GpuInstance:
        """
        Terminates a GPU pod and calculates total costs.
        """
        stmt = select(GpuInstance).where(GpuInstance.id == instance_id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        
        if not instance:
            raise ValueError(f"GPU Instance {instance_id} not found")
            
        logger.info(f"Terminating RunPod GPU: {instance.provider_instance_id}")
        await self.client.terminate_pod(instance.provider_instance_id)
        
        instance.status = GpuStatus.terminated
        instance.terminated_at = datetime.now(timezone.utc)
        
        # Calculate naive total cost if it has run
        if instance.started_at:
            duration = instance.terminated_at - instance.started_at
            hours = duration.total_seconds() / 3600.0
            instance.total_cost = hours * instance.cost_per_hour
            
        await session.commit()
        await session.refresh(instance)
        
        return instance

    async def sync_status(self, session: AsyncSession, instance_id: uuid.UUID) -> GpuInstance:
        """
        Syncs the status of the GPU pod with RunPod API.
        """
        stmt = select(GpuInstance).where(GpuInstance.id == instance_id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        
        if not instance:
            raise ValueError(f"GPU Instance {instance_id} not found")
            
        try:
            status = await self.client.get_pod_status(instance.provider_instance_id)
            
            if status.status == "RUNNING":
                instance.status = GpuStatus.running
            elif status.status == "EXITED":
                instance.status = GpuStatus.stopped
            
            instance.last_health_check = datetime.now(timezone.utc)
            
            await session.commit()
            await session.refresh(instance)
            
        except Exception as e:
            logger.error(f"Error syncing status for {instance.provider_instance_id}: {e}")
            
        return instance

class ModelRouter:
    """
    Routes generative tasks to the most efficient GPU model based on requirement.
    """
    
    GPU_PREFERENCES = {
        "text_to_video": "NVIDIA A100 80GB PCIe",
        "image_to_video": "NVIDIA A100 80GB PCIe",
        "upscaling": "NVIDIA GeForce RTX 4090",
        "frame_interpolation": "NVIDIA GeForce RTX 4090",
        "lip_sync": "NVIDIA RTX A6000",
        "image_generation": "NVIDIA GeForce RTX 4090"
    }

    @classmethod
    def get_preferred_gpu(cls, task_type: str) -> str:
        """Returns the most efficient GPU for the given task."""
        return cls.GPU_PREFERENCES.get(task_type, "NVIDIA GeForce RTX 4090")
    
    @classmethod
    def route_task(cls, task_type: str, runpod_service: RunPodService) -> str:
        """
        Determines routing logic for a task. In production, this would 
        check for warm/running instances of the preferred GPU type, 
        and optionally provision a new one if all are busy.
        """
        preferred_gpu = cls.get_preferred_gpu(task_type)
        logger.info(f"Routing task '{task_type}' to preferred GPU: {preferred_gpu}")
        
        # Placeholder for dynamic routing logic that queries the DB for 
        # active GpuInstances matching preferred_gpu, or queues a provision task.
        return preferred_gpu
