from pydantic import BaseModel
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
    logline: Optional[str] = None
    synopsis: Optional[str] = None
    full_text: Optional[str] = None
    genre: Optional[str] = None
    status: ScriptStatus
    created_at: datetime
    updated_at: datetime

class ScriptGenerateRequest(BaseModel):
    project_id: uuid.UUID
    instructions: Optional[str] = None
