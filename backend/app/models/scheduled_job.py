import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Enum, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class JobStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    
    job_type: Mapped[str] = mapped_column(String)  # e.g., 'ai_model_studio_production'
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.pending)
    
    scheduled_for: Mapped[datetime] = mapped_column(DateTime)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    error_log: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    user: Mapped["User"] = relationship("User")
    project: Mapped["Project"] = relationship("Project")
