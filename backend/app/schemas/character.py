from pydantic import BaseModel
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
    image_type: str
