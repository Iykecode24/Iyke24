import os

BASE_DIR = r"c:\Users\user\Downloads\iyke-content-studio\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "app/schemas/__init__.py": "",

    "app/schemas/common.py": """from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

class ErrorResponse(BaseModel):
    detail: str

class SuccessResponse(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime""",

    "app/schemas/auth.py": """from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole
import uuid

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class MFASetupResponse(BaseModel):
    secret: str
    qr_code_url: str

class MFAVerifyRequest(BaseModel):
    code: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str
    role: UserRole
    mfa_enabled: bool
    email_verified: bool
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None""",

    "app/schemas/project.py": """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.project import ContentType, Orientation, ProjectStatus
import uuid

class ProjectCreate(BaseModel):
    title: str
    content_type: ContentType
    genre: Optional[str] = None
    target_audience: Optional[str] = None
    language: Optional[str] = None
    duration_seconds: Optional[int] = None
    resolution: Optional[str] = None
    orientation: Orientation

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    visual_style: Optional[str] = None
    time_period: Optional[str] = None
    country: Optional[str] = None
    voice_preference: Optional[str] = None
    music_preference: Optional[str] = None

class ProjectStatusUpdate(BaseModel):
    status: ProjectStatus
    progress_percent: Optional[float] = None

class ProjectResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    content_type: ContentType
    status: ProjectStatus
    progress_percent: float
    created_at: datetime
    updated_at: datetime

class ProjectListResponse(BaseModel):
    items: List[ProjectResponse]
    total: int
    page: int
    size: int""",

    "app/schemas/script.py": """from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from app.models.script import ScriptStatus
import uuid

class ScriptCreate(BaseModel):
    project_id: uuid.UUID
    title: str
    logline: Optional[str] = None

class ScriptUpdate(BaseModel):
    title: Optional[str] = None
    logline: Optional[str] = None
    synopsis: Optional[str] = None
    full_text: Optional[str] = None
    status: Optional[ScriptStatus] = None

class ScriptResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    status: ScriptStatus
    created_at: datetime
    updated_at: datetime

class ScriptGenerateRequest(BaseModel):
    project_id: uuid.UUID
    instructions: Optional[str] = None""",

    "app/schemas/scene.py": """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.scene import SceneStatus
import uuid

class SceneCreate(BaseModel):
    script_id: uuid.UUID
    project_id: uuid.UUID
    order_index: int
    title: str

class SceneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    dialogue: Optional[str] = None
    visual_prompt: Optional[str] = None
    status: Optional[SceneStatus] = None

class SceneResponse(BaseModel):
    id: uuid.UUID
    order_index: int
    title: str
    status: SceneStatus
    created_at: datetime
    updated_at: datetime

class SceneReorder(BaseModel):
    scene_ids: List[uuid.UUID]

class SceneRegenerateRequest(BaseModel):
    scene_id: uuid.UUID
    instructions: Optional[str] = None""",

    "app/schemas/character.py": """from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class CharacterCreate(BaseModel):
    name: str
    project_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CharacterResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_library: bool
    created_at: datetime
    updated_at: datetime

class CharacterReferenceCreate(BaseModel):
    character_id: uuid.UUID
    image_url: str
    image_type: str""",

    "app/schemas/render.py": """from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.render_job import JobType, RenderStatus
import uuid

class RenderJobCreate(BaseModel):
    project_id: uuid.UUID
    job_type: JobType
    model_name: Optional[str] = None

class RenderJobResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    job_type: JobType
    status: RenderStatus
    progress_percent: float
    created_at: datetime
    updated_at: datetime

class RenderJobStatusUpdate(BaseModel):
    status: RenderStatus
    progress_percent: Optional[float] = None
    error_message: Optional[str] = None

class CostEstimateRequest(BaseModel):
    project_id: uuid.UUID

class CostEstimate(BaseModel):
    total_estimated_usd: float
    breakdown: dict""",

    "app/schemas/admin.py": """from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
import uuid

class ApiIntegrationCreate(BaseModel):
    provider: str
    display_name: str
    api_key: str
    endpoint_url: Optional[str] = None

class ApiIntegrationUpdate(BaseModel):
    api_key: Optional[str] = None
    is_active: Optional[bool] = None

class ApiIntegrationResponse(BaseModel):
    id: uuid.UUID
    provider: str
    display_name: str
    is_active: bool
    is_configured: bool
    created_at: datetime

class ModelRegistryCreate(BaseModel):
    name: str
    display_name: str
    type: str
    provider: str
    version: str

class ModelRegistryResponse(BaseModel):
    id: uuid.UUID
    name: str
    display_name: str
    type: str
    enabled: bool

class GpuInstanceResponse(BaseModel):
    id: uuid.UUID
    provider_instance_id: str
    status: str
    cost_per_hour: float

class SystemStatsResponse(BaseModel):
    total_users: int
    active_projects: int
    running_gpus: int
    monthly_cost_usd: float"""
}

for path, content in files.items():
    write_file(path, content)
