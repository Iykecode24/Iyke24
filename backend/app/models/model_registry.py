import uuid
from typing import Optional
from sqlalchemy import String, Enum, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum

class ModelType(str, enum.Enum):
    llm = "llm"
    image = "image"
    video = "video"
    voice = "voice"
    lipsync = "lipsync"
    upscale = "upscale"
    enhance = "enhance"

class ModelRegistry(Base):
    __tablename__ = "model_registry"
    
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String)
    type: Mapped[ModelType] = mapped_column(Enum(ModelType))
    provider: Mapped[str] = mapped_column(String)
    version: Mapped[str] = mapped_column(String)
    endpoint_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gpu_memory_gb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    supported_tasks: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    storage_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    size_gb: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_installed: Mapped[bool] = mapped_column(Boolean, default=False)
    install_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
