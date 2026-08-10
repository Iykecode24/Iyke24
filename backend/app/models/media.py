import uuid
from typing import Optional
from sqlalchemy import ForeignKey, String, Enum, Integer, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class AudioType(str, enum.Enum):
    dialogue = "dialogue"
    narration = "narration"
    music = "music"
    sfx = "sfx"
    full_mix = "full_mix"

class AudioFile(Base):
    __tablename__ = "audio_files"
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    scene_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("scenes.id"), nullable=True)
    type: Mapped[AudioType] = mapped_column(Enum(AudioType))
    url: Mapped[str] = mapped_column(String)
    duration_seconds: Mapped[float] = mapped_column(Float)
    provider: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    voice_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("voices.id"), nullable=True)
    transcript: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    project: Mapped["Project"] = relationship("Project", back_populates="audio_files")
    scene: Mapped[Optional["Scene"]] = relationship("Scene", back_populates="audio_files")

class ImageType(str, enum.Enum):
    scene = "scene"
    character = "character"
    thumbnail = "thumbnail"
    storyboard = "storyboard"
    product = "product"
    background = "background"

class Image(Base):
    __tablename__ = "images"
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    scene_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("scenes.id"), nullable=True)
    type: Mapped[ImageType] = mapped_column(Enum(ImageType))
    url: Mapped[str] = mapped_column(String)
    prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    negative_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    seed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    
    project: Mapped["Project"] = relationship("Project", back_populates="images")
    scene: Mapped[Optional["Scene"]] = relationship("Scene", back_populates="images")

class VideoClip(Base):
    __tablename__ = "video_clips"
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    scene_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("scenes.id"), nullable=True)
    url: Mapped[str] = mapped_column(String)
    duration_seconds: Mapped[float] = mapped_column(Float)
    resolution: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fps: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="completed")
    
    project: Mapped["Project"] = relationship("Project", back_populates="video_clips")
    scene: Mapped[Optional["Scene"]] = relationship("Scene", back_populates="video_clips")

class FinalVideo(Base):
    __tablename__ = "final_videos"
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    url: Mapped[str] = mapped_column(String)
    resolution: Mapped[str] = mapped_column(String)
    duration_seconds: Mapped[float] = mapped_column(Float)
    format: Mapped[str] = mapped_column(String)
    size_bytes: Mapped[int] = mapped_column(Integer)
    aspect_ratio: Mapped[str] = mapped_column(String)
    quality_preset: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    project: Mapped["Project"] = relationship("Project", back_populates="final_videos")
