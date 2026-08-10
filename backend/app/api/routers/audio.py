from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response

from app.database import get_db
from app.security.auth import get_current_user
from app.models.user import User
from app.providers.elevenlabs.services import ElevenLabsService
from app.providers.elevenlabs.client import ElevenLabsClient
from app.schemas.audio import AudioGenerateRequest, AudioPreviewRequest

router = APIRouter(prefix="/api/audio", tags=["audio"])

@router.post("/generate")
async def generate_audio(
    req: AudioGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ElevenLabsService(db)
    try:
        audio_file = await service.generate_and_save_audio(
            project_id=req.project_id,
            user_id=current_user.id,
            text=req.text,
            voice_id=req.voice_id,
            db_voice_id=req.db_voice_id,
            model_id=req.model_id,
            scene_id=req.scene_id
        )
        return {"status": "success", "audio_url": audio_file.url, "id": str(audio_file.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preview")
async def preview_audio(
    req: AudioPreviewRequest,
    current_user: User = Depends(get_current_user)
):
    client = ElevenLabsClient()
    try:
        audio_bytes = await client.generate_audio(
            voice_id=req.voice_id,
            text=req.text,
            model_id=req.model_id
        )
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
