import uuid
import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.project import Project, ProjectStatus
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectListResponse, ProjectUpdate
from app.security.auth import get_current_user
from app.services.script_engine import ScriptEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["projects"])

async def generate_script_background(project_id: uuid.UUID):
    # This background task uses its own session scope
    # Note: In a real app with BackgroundTasks, it's safer to spawn a new DB session.
    # For now, we will create a new session just to be safe.
    from app.database import async_session_maker
    async with async_session_maker() as session:
        engine = ScriptEngine(db=session)
        try:
            await engine.generate_script(project_id)
        except Exception as e:
            logger.error(f"Background script generation failed: {e}")

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new project and trigger script generation in the background.
    """
    project = Project(
        user_id=current_user.id,
        title=project_in.title,
        content_type=project_in.content_type,
        genre=project_in.genre,
        target_audience=project_in.target_audience,
        language=project_in.language,
        duration_seconds=project_in.duration_seconds,
        resolution=project_in.resolution,
        orientation=project_in.orientation,
        status=ProjectStatus.planning
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    # Trigger script generation
    background_tasks.add_task(generate_script_background, project.id)
    
    return project

@router.get("/{id}", response_model=ProjectResponse)
async def get_project(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    stmt = select(Project).where(Project.id == id, Project.user_id == current_user.id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    stmt = select(Project).where(Project.user_id == current_user.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    projects = result.scalars().all()
    
    # Simple total count approach (inefficient for large tables, but okay for MVP)
    # Ideally use a separate count query
    count_stmt = select(Project).where(Project.user_id == current_user.id)
    count_res = await db.execute(count_stmt)
    total = len(count_res.scalars().all())

    return ProjectListResponse(
        items=projects,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        size=limit
    )

@router.put("/{id}", response_model=ProjectResponse)
async def update_project(
    id: uuid.UUID,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    stmt = select(Project).where(Project.id == id, Project.user_id == current_user.id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
        
    await db.commit()
    await db.refresh(project)
    return project

@router.delete("/{id}")
async def delete_project(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    stmt = select(Project).where(Project.id == id, Project.user_id == current_user.id)
    result = await db.execute(stmt)
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    await db.delete(project)
    await db.commit()
    return {"message": "Project deleted successfully"}
