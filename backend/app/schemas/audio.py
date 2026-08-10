from pydantic import BaseModel
from typing import Optional
import uuid

class AudioGenerateRequest(BaseModel):
    project_id: uuid.UUID
    text: str
    voice_id: str
    db_voice_id: Optional[uuid.UUID] = None
    model_id: str = "eleven_monolingual_v1"
    scene_id: Optional[uuid.UUID] = None
    
class AudioPreviewRequest(BaseModel):
    text: str
    voice_id: str
    model_id: str = "eleven_monolingual_v1"
