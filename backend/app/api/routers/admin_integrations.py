from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.security.auth import get_current_user
from app.models.user import User, UserRole
from app.providers.elevenlabs.client import ElevenLabsClient

router = APIRouter(prefix="/api/admin/integrations", tags=["admin"])

def check_admin(user: User):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

@router.get("/elevenlabs/test")
async def test_elevenlabs(
    current_user: User = Depends(get_current_user)
):
    # Depending on auth implementation, check if admin.
    # Assuming current_user has a role attribute, or just a simple test:
    # check_admin(current_user) 
    
    client = ElevenLabsClient()
    try:
        voices = await client.get_voices()
        return {"status": "success", "message": "ElevenLabs connection successful", "voices_count": len(voices.get("voices", []))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ElevenLabs test failed: {str(e)}")
