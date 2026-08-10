import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class JobType(str, enum.Enum):
    script = "script"
    image = "image"
    video = "video"
    voice = "voice"
    lipsync = "lipsync"
    stitch = "stitch"
    upscale = "upscale"
    enhance = "enhance"
    export = "export"

class RenderStatus(str, enum.Enum):
    queued = "queued"
    preparing = "preparing"
    starting_gpu = "starting_gpu"
    loading_model = "loading_model"
    rendering = "rendering"
    processing_audio = "processing_audio"
    lip_syncing = "lip_syncing"
    stitching = "stitching"
    upscaling = "upscaling"
    uploading = "uploading"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class RenderJob(Base):
    __tablename__ = "render_jobs"
    
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    job_type: Mapped[JobType] = mapped_column(Enum(JobType))
    model_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gpu_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gpu_instance_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("gpu_instances.id"), nullable=True)
    status: Mapped[RenderStatus] = mapped_column(Enum(RenderStatus), default=RenderStatus.queued)
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    output_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    logs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    project: Mapped["Project"] = relationship("Project", back_populates="render_jobs")
