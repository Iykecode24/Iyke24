import uuid
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Text, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class ScriptStatus(str, enum.Enum):
    draft = "draft"
    generating = "generating"
    review = "review"
    approved = "approved"
    locked = "locked"

class Script(Base):
    __tablename__ = "scripts"
    
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    version: Mapped[int] = mapped_column(default=1)
    title: Mapped[str] = mapped_column(String)
    logline: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    synopsis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    full_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    structure_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    editing_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    social_media_package: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[ScriptStatus] = mapped_column(Enum(ScriptStatus), default=ScriptStatus.draft)
    
    project: Mapped["Project"] = relationship("Project", back_populates="script")
    scenes: Mapped[List["Scene"]] = relationship("Scene", back_populates="script")
