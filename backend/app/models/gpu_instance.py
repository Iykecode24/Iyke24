import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Enum, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class GpuStatus(str, enum.Enum):
    creating = "creating"
    running = "running"
    stopping = "stopping"
    stopped = "stopped"
    terminated = "terminated"
    error = "error"

class GpuInstance(Base):
    __tablename__ = "gpu_instances"
    
    provider: Mapped[str] = mapped_column(String, default="runpod")
    provider_instance_id: Mapped[str] = mapped_column(String)
    gpu_type: Mapped[str] = mapped_column(String)
    gpu_count: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[GpuStatus] = mapped_column(Enum(GpuStatus))
    pod_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cost_per_hour: Mapped[float] = mapped_column(Float, default=0.0)
    total_cost: Mapped[float] = mapped_column(Float, default=0.0)
    network_volume_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    stopped_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    terminated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_health_check: Mapped[Optional[datetime]] = mapped_column(nullable=True)
