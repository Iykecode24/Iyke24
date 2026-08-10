import base64
import hashlib
import hmac
import json
import uuid
from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings

router = APIRouter(tags=["privacy"])

def validate_meta_signed_request(signed_request: str, app_secret: str) -> dict:
    try:
        encoded_sig, payload = signed_request.split('.', 1)
        sig = base64.urlsafe_b64decode(encoded_sig + '=' * (-len(encoded_sig) % 4))
        data = json.loads(base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)).decode('utf-8'))
        
        # Verify signature
        expected_sig = hmac.new(app_secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expected_sig):
            raise ValueError("Invalid signature")
            
        return data
    except Exception as e:
        raise ValueError(f"Invalid signed_request: {str(e)}")

@router.post("/meta/data-deletion")
async def meta_data_deletion(
    signed_request: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        # In a real setup, we would need the META_APP_SECRET from settings
        # For now, we will fallback to a dummy if not found for testing
        app_secret = getattr(settings, "META_APP_SECRET", "dummy_secret_for_now")
        data = validate_meta_signed_request(signed_request, app_secret)
        
        user_id = data.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Missing user_id")
            
        # Mock token invalidation and queuing data deletion
        # In a complete implementation, this would involve Celery/background tasks
        
        confirmation_code = str(uuid.uuid4())
        
        # As per Meta documentation, return JSON with url and confirmation_code
        return {
            "url": f"https://iyke-content-studio.com/data-deletion/status?id={confirmation_code}",
            "confirmation_code": confirmation_code
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
