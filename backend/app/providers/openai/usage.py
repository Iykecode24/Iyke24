import logging
from sqlalchemy.orm import Session
from app.models.ai_orchestration import AIUsage

logger = logging.getLogger(__name__)

async def track_usage(
    db: Session,
    project_id: str,
    agent_id: str,
    model_id: str,
    prompt_tokens: int,
    completion_tokens: int,
    cost: float = 0.0
) -> AIUsage:
    """
    Records AI usage to the database.
    """
    total_tokens = prompt_tokens + completion_tokens
    
    usage_record = AIUsage(
        project_id=project_id,
        agent_id=agent_id,
        model_id=model_id,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost=cost
    )
    
    try:
        db.add(usage_record)
        db.commit()
        db.refresh(usage_record)
        return usage_record
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to track AI usage: {str(e)}")
        raise
