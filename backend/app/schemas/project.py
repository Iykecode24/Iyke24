from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.project import ContentType, Orientation, ProjectStatus
import uuid

class ProjectCreate(BaseModel):
    title: str
    content_type: ContentType
    genre: Optional[str] = None
    target_audience: Optional[str] = None
    language: Optional[str] = None
    duration_seconds: Optional[int] = None
    resolution: Optional[str] = None
    orientation: Orientation

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    visual_style: Optional[str] = None
    time_period: Optional[str] = None
    country: Optional[str] = None
    voice_preference: Optional[str] = None
    music_preference: Optional[str] = None

class ProjectStatusUpdate(BaseModel):
    status: ProjectStatus
    progress_percent: Optional[float] = None

class ProjectResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content_type: ContentType
    status: ProjectStatus
    progress_percent: float
    created_at: datetime
    updated_at: datetime

class ProjectListResponse(BaseModel):
    items: List[ProjectResponse]
    total: int
    page: int
    size: int
