import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import ForeignKey, String, Float, Enum, Boolean, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class ContentType(str, enum.Enum):
    movie = "movie"
    cartoon = "cartoon"
    explainer = "explainer"
    news = "news"
    image_to_video = "image_to_video"
    advertisement = "advertisement"
    ai_model_studio = "ai_model_studio"

class AutomationMode(str, enum.Enum):
    manual = "manual"
    scheduled = "scheduled"
    autonomous = "autonomous"

class Orientation(str, enum.Enum):
    landscape = "landscape"
    portrait = "portrait"
    square = "square"

class ProjectStatus(str, enum.Enum):
    planning = "planning"
    scriptwriting = "scriptwriting"
    character_creation = "character_creation"
    storyboarding = "storyboarding"
    voice_generation = "voice_generation"
    scene_generation = "scene_generation"
    lip_sync = "lip_sync"
    editing = "editing"
    upscaling = "upscaling"
    rendering = "rendering"
    uploading = "uploading"
    published = "published"
    failed = "failed"
    draft = "draft"

class Project(Base):
    __tablename__ = "projects"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    content_type: Mapped[ContentType] = mapped_column(Enum(ContentType))
    genre: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    target_audience: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    orientation: Mapped[Orientation] = mapped_column(Enum(Orientation))
    visual_style: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    time_period: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    voice_preference: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    music_preference: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    publishing_destination: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.draft)
    automation_mode: Mapped[AutomationMode] = mapped_column(Enum(AutomationMode), default=AutomationMode.manual)
    approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    scheduled_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    quality_threshold: Mapped[int] = mapped_column(Integer, default=90)
    automation_rules: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_cost: Mapped[float] = mapped_column(Float, default=0.0)
    actual_cost: Mapped[float] = mapped_column(Float, default=0.0)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="projects")
    script: Mapped["Script"] = relationship("Script", back_populates="project", uselist=False)
    scenes: Mapped[List["Scene"]] = relationship("Scene", back_populates="project")
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="project")
    render_jobs: Mapped[List["RenderJob"]] = relationship("RenderJob", back_populates="project")
    audio_files: Mapped[List["AudioFile"]] = relationship("AudioFile", back_populates="project")
    images: Mapped[List["Image"]] = relationship("Image", back_populates="project")
    video_clips: Mapped[List["VideoClip"]] = relationship("VideoClip", back_populates="project")
    final_videos: Mapped[List["FinalVideo"]] = relationship("FinalVideo", back_populates="project")
