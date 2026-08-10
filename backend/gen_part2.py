import os

BASE_DIR = r"c:\Users\user\Downloads\iyke-content-studio\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "app/models/render_job.py": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Enum, Float, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class JobType(str, enum.Enum):
    script = "script"
    image = "image"
    video = "video"
    voice = "voice"
    lipsync = "lipsync"
    stitch = "stitch"
    upscale = "upscale"
    enhance = "enhance"
    export = "export"

class RenderStatus(str, enum.Enum):
    queued = "queued"
    preparing = "preparing"
    starting_gpu = "starting_gpu"
    loading_model = "loading_model"
    rendering = "rendering"
    processing_audio = "processing_audio"
    lip_syncing = "lip_syncing"
    stitching = "stitching"
    upscaling = "upscaling"
    uploading = "uploading"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class RenderJob(Base):
    __tablename__ = "render_jobs"
    
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    job_type: Mapped[JobType] = mapped_column(Enum(JobType))
    model_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gpu_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    gpu_instance_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("gpu_instances.id"), nullable=True)
    status: Mapped[RenderStatus] = mapped_column(Enum(RenderStatus), default=RenderStatus.queued)
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    output_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    logs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    project: Mapped["Project"] = relationship("Project", back_populates="render_jobs")""",

    "app/models/gpu_instance.py": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Enum, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class GpuStatus(str, enum.Enum):
    creating = "creating"
    running = "running"
    stopping = "stopping"
    stopped = "stopped"
    terminated = "terminated"
    error = "error"

class GpuInstance(Base):
    __tablename__ = "gpu_instances"
    
    provider: Mapped[str] = mapped_column(String, default="runpod")
    provider_instance_id: Mapped[str] = mapped_column(String)
    gpu_type: Mapped[str] = mapped_column(String)
    gpu_count: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[GpuStatus] = mapped_column(Enum(GpuStatus))
    pod_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cost_per_hour: Mapped[float] = mapped_column(Float, default=0.0)
    total_cost: Mapped[float] = mapped_column(Float, default=0.0)
    network_volume_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    stopped_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    terminated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_health_check: Mapped[Optional[datetime]] = mapped_column(nullable=True)""",

    "app/models/model_registry.py": """import uuid
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
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)""",

    "app/models/api_integration.py": """import uuid
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
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)""",

    "app/models/social.py": """import uuid
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
    retry_count: Mapped[int] = mapped_column(Integer, default=0)""",

    "app/models/billing.py": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Enum, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum

class ResourceType(str, enum.Enum):
    gpu = "gpu"
    api_call = "api_call"
    storage = "storage"
    voice = "voice"
    image = "image"
    video = "video"

class CostCategory(str, enum.Enum):
    gpu = "gpu"
    voice = "voice"
    image = "image"
    video = "video"
    storage = "storage"
    api = "api"
    total = "total"

class LimitType(str, enum.Enum):
    per_project = "per_project"
    daily = "daily"
    monthly = "monthly"
    per_user = "per_user"

class UsageRecord(Base):
    __tablename__ = "usage_records"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    resource_type: Mapped[ResourceType] = mapped_column(Enum(ResourceType))
    quantity: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    unit_cost: Mapped[float] = mapped_column(Float)
    total_cost: Mapped[float] = mapped_column(Float)
    provider: Mapped[str] = mapped_column(String)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class CostRecord(Base):
    __tablename__ = "cost_records"
    
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    render_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("render_jobs.id"), nullable=True)
    category: Mapped[CostCategory] = mapped_column(Enum(CostCategory))
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class CostLimit(Base):
    __tablename__ = "cost_limits"
    
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    limit_type: Mapped[LimitType] = mapped_column(Enum(LimitType))
    max_amount: Mapped[float] = mapped_column(Float)
    current_usage: Mapped[float] = mapped_column(Float, default=0.0)
    period_start: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    period_end: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)""",

    "app/models/system.py": """import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey, String, Enum, Boolean, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum

class Severity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class NotificationType(str, enum.Enum):
    info = "info"
    success = "success"
    warning = "warning"
    error = "error"
    render_complete = "render_complete"
    render_failed = "render_failed"
    cost_alert = "cost_alert"
    system = "system"

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String)
    resource_type: Mapped[str] = mapped_column(String)
    resource_id: Mapped[str] = mapped_column(String)
    details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class ModerationRecord(Base):
    __tablename__ = "moderation_records"
    
    project_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    content_type: Mapped[str] = mapped_column(String)
    flagged_content: Mapped[str] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(String)
    severity: Mapped[Severity] = mapped_column(Enum(Severity))
    action_taken: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reviewed_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

class Notification(Base):
    __tablename__ = "notifications"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType))
    title: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(Text)
    link: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)"""
}

for path, content in files.items():
    write_file(path, content)
