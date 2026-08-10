import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Enum, Boolean, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class SocialPlatform(str, enum.Enum):
    youtube = "youtube"
    facebook = "facebook"
    instagram = "instagram"
    tiktok = "tiktok"
    linkedin = "linkedin"
    x_twitter = "x_twitter"
    pinterest = "pinterest"

class PostStatus(str, enum.Enum):
    draft = "draft"
    scheduled = "scheduled"
    publishing = "publishing"
    published = "published"
    failed = "failed"

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    platform: Mapped[SocialPlatform] = mapped_column(Enum(SocialPlatform))
    access_token_encrypted: Mapped[str] = mapped_column(String)
    refresh_token_encrypted: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    token_expires_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    platform_user_id: Mapped[str] = mapped_column(String)
    platform_username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subscriber_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    channel_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    connected_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    user: Mapped["User"] = relationship("User", back_populates="social_accounts")

class SocialPost(Base):
    __tablename__ = "social_posts"
    
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    social_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("social_accounts.id"))
    platform: Mapped[SocialPlatform] = mapped_column(Enum(SocialPlatform))
    post_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    post_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hashtags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    privacy_setting: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    status: Mapped[PostStatus] = mapped_column(Enum(PostStatus), default=PostStatus.draft)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
