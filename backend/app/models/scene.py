import uuid
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Text, Enum, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class SceneStatus(str, enum.Enum):
    draft = "draft"
    generating = "generating"
    generated = "generated"
    approved = "approved"
    locked = "locked"
    failed = "failed"

class Scene(Base):
    __tablename__ = "scenes"
    
    script_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scripts.id"))
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    order_index: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    dialogue: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    narration: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    camera_direction: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    shot_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lighting: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    visual_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transition: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)
    status: Mapped[SceneStatus] = mapped_column(Enum(SceneStatus), default=SceneStatus.draft)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    project: Mapped["Project"] = relationship("Project", back_populates="scenes")
    script: Mapped["Script"] = relationship("Script", back_populates="scenes")
    images: Mapped[List["Image"]] = relationship("Image", back_populates="scene")
    video_clips: Mapped[List["VideoClip"]] = relationship("VideoClip", back_populates="scene")
    audio_files: Mapped[List["AudioFile"]] = relationship("AudioFile", back_populates="scene")
