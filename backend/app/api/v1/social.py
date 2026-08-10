import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.security.auth import get_current_user
from app.schemas.social import SocialAccountCreate, SocialAccountOut, SocialPostCreate, SocialPostOut
from app.models.social import SocialPlatform
from app.services.social_service import SocialService

router = APIRouter(prefix="/social", tags=["Social Publishing"])

@router.post("/accounts", response_model=SocialAccountOut, status_code=status.HTTP_201_CREATED)
async def connect_social_account(
    data: SocialAccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Connect a new social media account for the user."""
    return await SocialService.connect_account(db, current_user.id, data)

@router.get("/auth-url")
async def get_oauth_url(
    platform: SocialPlatform,
    state: str = None,
    current_user: User = Depends(get_current_user)
):
    """Get the OAuth URL to authorize a social platform."""
    url = await SocialService.generate_oauth_url(platform, state)
    return {"auth_url": url}

@router.get("/accounts", response_model=List[SocialAccountOut])
async def get_social_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all connected social media accounts for the current user."""
    return await SocialService.get_user_accounts(db, current_user.id)

@router.post("/posts", response_model=SocialPostOut, status_code=status.HTTP_201_CREATED)
async def schedule_social_post(
    data: SocialPostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Schedule a new post for a connected social media account."""
    return await SocialService.schedule_post(db, current_user.id, data)

@router.get("/projects/{project_id}/posts", response_model=List[SocialPostOut])
async def get_project_social_posts(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all social posts for a specific project."""
    # In a full implementation, check if the project belongs to the user
    return await SocialService.get_project_posts(db, project_id)
