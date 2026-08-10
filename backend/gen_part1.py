import os

BASE_DIR = r"c:\Users\user\Downloads\iyke-content-studio\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "requirements.txt": """fastapi[standard]==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy[asyncio]==2.0.35
asyncpg==0.30.0
psycopg2-binary==2.9.9
alembic==1.13.0
pydantic==2.9.0
pydantic-settings==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.12
cryptography==43.0.0
boto3==1.35.0
httpx==0.27.0
celery[redis]==5.4.0
redis==5.1.0
pyotp==2.9.0
qrcode==7.4.2
pillow==10.4.0
python-magic==0.4.27
aiofiles==24.1.0
sse-starlette==2.1.0""",

    "Dockerfile": """FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg libmagic1 gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]""",

    "app/__init__.py": "",

    "app/config.py": """from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    \"\"\"Application configuration settings.\"\"\"
    APP_NAME: str = "Iyke Content Studio"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str
    
    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()""",

    "app/database.py": """import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    echo=settings.APP_DEBUG
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    \"\"\"Base class for SQLAlchemy models.\"\"\"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

async def get_db():
    \"\"\"Dependency for getting async DB session.\"\"\"
    async with async_session_maker() as session:
        yield session""",

    "app/models/__init__.py": """from app.database import Base
from app.models.user import User
from app.models.session import Session
from app.models.project import Project
from app.models.script import Script
from app.models.scene import Scene
from app.models.character import Character
from app.models.character_reference import CharacterReference
from app.models.voice import Voice
from app.models.media import AudioFile, Image, VideoClip, FinalVideo
from app.models.render_job import RenderJob
from app.models.gpu_instance import GpuInstance
from app.models.model_registry import ModelRegistry
from app.models.api_integration import ApiIntegration
from app.models.social import SocialAccount, SocialPost
from app.models.billing import UsageRecord, CostRecord, CostLimit
from app.models.system import AuditLog, ModerationRecord, Notification""",

    "app/models/user.py": """import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    creator = "creator"
    editor = "editor"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.creator)
    mfa_secret: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="user")
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="user")
    social_accounts: Mapped[List["SocialAccount"]] = relationship("SocialAccount", back_populates="user")
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="user")""",

    "app/models/session.py": """import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String)
    ip_address: Mapped[str] = mapped_column(String)
    user_agent: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    user: Mapped["User"] = relationship("User", back_populates="sessions")""",

    "app/models/project.py": """import uuid
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Float, Enum
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
    final_videos: Mapped[List["FinalVideo"]] = relationship("FinalVideo", back_populates="project")""",

    "app/models/script.py": """import uuid
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
    scenes: Mapped[List["Scene"]] = relationship("Scene", back_populates="script")""",

    "app/models/scene.py": """import uuid
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
    audio_files: Mapped[List["AudioFile"]] = relationship("AudioFile", back_populates="scene")""",

    "app/models/character.py": """import uuid
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Text, Float, Boolean, Integer
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
    
    user: Mapped["User"] = relationship("User", back_populates="characters")
    project: Mapped["Project"] = relationship("Project", back_populates="characters")
    references: Mapped[List["CharacterReference"]] = relationship("CharacterReference", back_populates="character")
    voice: Mapped[Optional["Voice"]] = relationship("Voice", back_populates="characters")""",

    "app/models/character_reference.py": """import uuid
from sqlalchemy import ForeignKey, String, Boolean, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class ImageType(str, enum.Enum):
    front = "front"
    side = "side"
    full_body = "full_body"
    additional = "additional"

class CharacterReference(Base):
    __tablename__ = "character_references"
    
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id"))
    image_url: Mapped[str] = mapped_column(String)
    image_type: Mapped[ImageType] = mapped_column(Enum(ImageType))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    character: Mapped["Character"] = relationship("Character", back_populates="references")""",

    "app/models/voice.py": """import uuid
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
    
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="voice")""",

    "app/models/media.py": """import uuid
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
    
    project: Mapped["Project"] = relationship("Project", back_populates="final_videos")"""
}

for path, content in files.items():
    write_file(path, content)
