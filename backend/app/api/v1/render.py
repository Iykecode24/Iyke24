import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from app.database import get_db
from app.models.render_job import RenderJob, RenderStatus, JobType
from app.models.user import User
from app.schemas.render import RenderJobCreate, RenderJobResponse, CostEstimateRequest, CostEstimate
from app.api.v1.auth import get_current_user
from app.workers.render_tasks import start_render_task

router = APIRouter(prefix="/render", tags=["render"])

@router.post("/estimate-cost", response_model=CostEstimate)
async def estimate_cost(
    request: CostEstimateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Mock cost estimation
    return CostEstimate(
        total_estimated_usd=1.50,
        breakdown={"gpu_time": 1.00, "api_calls": 0.50}
    )

@router.post("/start", response_model=RenderJobResponse)
async def start_render(
    request: RenderJobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger the final export job, which queues a task for video stitching and audio mixing.
    """
    # Create render job
    job = RenderJob(
        project_id=request.project_id,
        user_id=current_user.id,
        job_type=request.job_type,
        model_name=request.model_name,
        status=RenderStatus.queued,
        progress_percent=0.0
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # Queue Celery task
    start_render_task.delay(str(job.id))

    return job

@router.get("/jobs", response_model=List[RenderJobResponse])
async def list_jobs(
    project_id: uuid.UUID = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List render jobs for the current user."""
    stmt = select(RenderJob).where(RenderJob.user_id == current_user.id)
    if project_id:
        stmt = stmt.where(RenderJob.project_id == project_id)
    
    result = await db.execute(stmt)
    jobs = result.scalars().all()
    return jobs

@router.get("/jobs/{id}", response_model=RenderJobResponse)
async def get_job(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get status of a specific render job."""
    stmt = select(RenderJob).where(RenderJob.id == id, RenderJob.user_id == current_user.id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Render job not found")
        
    return job

@router.post("/jobs/{id}/cancel", response_model=RenderJobResponse)
async def cancel_job(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(RenderJob).where(RenderJob.id == id, RenderJob.user_id == current_user.id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Render job not found")
        
    if job.status in [RenderStatus.completed, RenderStatus.failed, RenderStatus.cancelled]:
        raise HTTPException(status_code=400, detail="Cannot cancel a job in its current state")
        
    job.status = RenderStatus.cancelled
    job.completed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(job)
    return job

@router.post("/jobs/{id}/retry", response_model=RenderJobResponse)
async def retry_job(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(RenderJob).where(RenderJob.id == id, RenderJob.user_id == current_user.id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Render job not found")
        
    job.status = RenderStatus.queued
    job.progress_percent = 0.0
    job.error_message = None
    job.retry_count += 1
    await db.commit()
    await db.refresh(job)
    
    # Re-queue
    start_render_task.delay(str(job.id))
    
    return job

@router.get("/queue")
async def get_queue():
    """Get overall queue statistics (admin or general overview)."""
    return {"message": "Queue status"}
