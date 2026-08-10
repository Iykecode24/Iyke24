import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Enum, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum

class ResourceType(str, enum.Enum):
    gpu = "gpu"
    api_call = "api_call"
    storage = "storage"
    voice = "voice"
    image = "image"
    video = "video"

class CostCategory(str, enum.Enum):
    gpu = "gpu"
    voice = "voice"
    image = "image"
    video = "video"
    storage = "storage"
    api = "api"
    total = "total"

class LimitType(str, enum.Enum):
    per_project = "per_project"
    daily = "daily"
    monthly = "monthly"
    per_user = "per_user"

class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    resource_type: Mapped[ResourceType] = mapped_column(Enum(ResourceType))
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    unit_cost: Mapped[float] = mapped_column(Float)
    total_cost: Mapped[float] = mapped_column(Float)
    provider: Mapped[str] = mapped_column(String)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class CostRecord(Base):
    __tablename__ = "cost_records"
    
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    render_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("render_jobs.id"), nullable=True)
    category: Mapped[CostCategory] = mapped_column(Enum(CostCategory))
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class CostLimit(Base):
    __tablename__ = "cost_limits"
    
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    limit_type: Mapped[LimitType] = mapped_column(Enum(LimitType))
    max_amount: Mapped[float] = mapped_column(Float)
    current_usage: Mapped[float] = mapped_column(Float, default=0.0)
    period_start: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    period_end: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
