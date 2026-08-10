import uuid
from typing import Optional, List
from sqlalchemy import String, Boolean, JSON, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class VoiceProvider(str, enum.Enum):
    elevenlabs = "elevenlabs"
    local = "local"
    custom = "custom"

class Voice(Base):
    __tablename__ = "voices"
    
    name: Mapped[str] = mapped_column(String)
    provider: Mapped[VoiceProvider] = mapped_column(Enum(VoiceProvider))
    provider_voice_id: Mapped[str] = mapped_column(String)
    language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    accent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    style: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    stability: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    similarity_boost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    speed: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    settings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="voice")
