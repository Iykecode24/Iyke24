import uuid
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Text, Float, Boolean, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Character(Base):
    __tablename__ = "characters"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    appearance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    wardrobe: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    accessories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    personality: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    skin_tone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hair_description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    body_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    voice_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("voices.id"), nullable=True)
    accent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lora_reference: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ip_adapter_reference: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    model_seed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    prompt_template: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    negative_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    consistency_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_library: Mapped[bool] = mapped_column(Boolean, default=False)
    is_adult_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    history_log: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="characters")
    project: Mapped["Project"] = relationship("Project", back_populates="characters")
    references: Mapped[List["CharacterReference"]] = relationship("CharacterReference", back_populates="character")
    voice: Mapped[Optional["Voice"]] = relationship("Voice", back_populates="characters")
