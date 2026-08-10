from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.render_job import JobType, RenderStatus
import uuid

class RenderJobCreate(BaseModel):
    project_id: uuid.UUID
    job_type: JobType
    model_name: Optional[str] = None

class RenderJobResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    job_type: JobType
    status: RenderStatus
    progress_percent: float
    created_at: datetime
    updated_at: datetime

class RenderJobStatusUpdate(BaseModel):
    status: RenderStatus
    progress_percent: Optional[float] = None
    error_message: Optional[str] = None

class CostEstimateRequest(BaseModel):
    project_id: uuid.UUID

class CostEstimate(BaseModel):
    total_estimated_usd: float
    breakdown: dict
