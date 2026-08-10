from pydantic import BaseModel
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
    script_id: uuid.UUID
    project_id: uuid.UUID
    order_index: int
    title: str
    description: Optional[str] = None
    dialogue: Optional[str] = None
    narration: Optional[str] = None
    camera_direction: Optional[str] = None
    shot_type: Optional[str] = None
    lighting: Optional[str] = None
    visual_prompt: Optional[str] = None
    audio_prompt: Optional[str] = None
    transition: Optional[str] = None
    duration_seconds: Optional[int] = None
    status: SceneStatus
    is_locked: bool
    created_at: datetime
    updated_at: datetime

class SceneReorder(BaseModel):
    scene_ids: List[uuid.UUID]

class SceneRegenerateRequest(BaseModel):
    scene_id: uuid.UUID
    instructions: Optional[str] = None
