import uuid
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.script import Script
from app.models.scene import Scene
from app.models.user import User
from app.schemas.script import ScriptResponse
from app.schemas.scene import SceneResponse
from app.security.auth import get_current_user

router = APIRouter(prefix="/scripts", tags=["scripts"])

@router.get("/project/{project_id}", response_model=ScriptResponse)
async def get_script_by_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get the script for a given project.
    """
    # Assuming user authorization for the project could be checked here.
    # For now, just query the script directly.
    stmt = select(Script).where(Script.project_id == project_id)
    result = await db.execute(stmt)
    script = result.scalar_one_or_none()
    
    if not script:
        raise HTTPException(status_code=404, detail="Script not found for this project")
        
    return script

@router.get("/{script_id}/scenes", response_model=List[SceneResponse])
async def get_scenes_for_script(
    script_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get all scenes for a specific script.
    """
    stmt = select(Scene).where(Scene.script_id == script_id).order_by(Scene.order_index)
    result = await db.execute(stmt)
    scenes = result.scalars().all()
    
    if not scenes:
        # Check if script exists
        script_stmt = select(Script).where(Script.id == script_id)
        script_result = await db.execute(script_stmt)
        if not script_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Script not found")
        return []
        
    return list(scenes)
