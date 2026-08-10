import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Enum, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum

class Provider(str, enum.Enum):
    openai = "openai"
    elevenlabs = "elevenlabs"
    runpod = "runpod"
    storage = "storage"
    youtube = "youtube"
    facebook = "facebook"
    instagram = "instagram"
    tiktok = "tiktok"
    linkedin = "linkedin"
    x_twitter = "x_twitter"

class ApiIntegration(Base):
    __tablename__ = "api_integrations"
    
    provider: Mapped[Provider] = mapped_column(Enum(Provider), unique=True)
    display_name: Mapped[str] = mapped_column(String)
    encrypted_api_key: Mapped[str] = mapped_column(String)
    endpoint_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_configured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_tested_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_test_success: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    usage_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
