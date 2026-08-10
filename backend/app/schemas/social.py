from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from app.models.social import SocialPlatform, PostStatus

class SocialAccountBase(BaseModel):
    platform: SocialPlatform

class SocialAccountCreate(SocialAccountBase):
    auth_code: str # The OAuth code received from frontend
    
class SocialAccountOut(SocialAccountBase):
    id: UUID
    platform_username: Optional[str] = None
    avatar_url: Optional[str] = None
    subscriber_count: Optional[int] = None
    channel_data: Optional[Dict[str, Any]] = None
    is_active: bool
    connected_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class SocialPostBase(BaseModel):
    project_id: UUID
    social_account_id: UUID
    platform: SocialPlatform
    title: Optional[str] = None
    description: Optional[str] = None
    hashtags: Optional[Dict[str, Any]] = None
    privacy_setting: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class SocialPostCreate(SocialPostBase):
    pass

class SocialPostOut(SocialPostBase):
    id: UUID
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    published_at: Optional[datetime] = None
    status: PostStatus
    error_message: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
