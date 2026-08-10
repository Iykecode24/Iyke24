import asyncio
import uuid
import logging
from datetime import datetime, timezone
from sqlalchemy import select
from app.workers.celery_app import celery_app
from app.database import async_session_maker
from app.models.social import SocialPost, PostStatus, SocialAccount
from app.services.social_service import SocialService
from app.integrations.social.factory import SocialIntegrationFactory

logger = logging.getLogger(__name__)

async def _publish_post_async(post_id_str: str):
    post_id = uuid.UUID(post_id_str)
    async with async_session_maker() as session:
        stmt = select(SocialPost).where(SocialPost.id == post_id)
        result = await session.execute(stmt)
        post = result.scalar_one_or_none()
        
        if not post:
            logger.error(f"SocialPost {post_id} not found")
            return
            
        if post.status not in [PostStatus.draft, PostStatus.scheduled, PostStatus.failed]:
            logger.info(f"Post {post_id} already processing or published.")
            return

        stmt = select(SocialAccount).where(SocialAccount.id == post.social_account_id)
        result = await session.execute(stmt)
        account = result.scalar_one_or_none()

        if not account or not account.is_active:
            post.status = PostStatus.failed
            post.error_message = "Account not found or inactive."
            await session.commit()
            return
            
        post.status = PostStatus.publishing
        await session.commit()
        
        try:
            # 1. Get valid access token
            access_token = await SocialService.get_valid_access_token(session, account)
            
            # 2. Get integration
            creds = SocialService._get_platform_credentials(account.platform)
            integration = SocialIntegrationFactory.get_integration(
                platform=account.platform,
                client_id=creds["client_id"],
                client_secret=creds["client_secret"],
                redirect_uri=creds["redirect_uri"]
            )
            
            # 3. Formulate post data for large video uploads / publishing
            post_data = {
                "title": post.title,
                "description": post.description,
                "tags": post.hashtags,
                "privacy_setting": post.privacy_setting or "private",
                "video_path": "path/to/rendered/video.mp4" # In real app, resolved from Media model
            }
            
            # 4. Publish
            result_data = await integration.publish_post(access_token, post_data)
            
            # 5. Update post status
            post.post_id = result_data.get("post_id")
            post.post_url = result_data.get("post_url")
            post.status = PostStatus.published
            post.published_at = datetime.now(timezone.utc)
            await session.commit()
            
        except Exception as e:
            logger.error(f"Error publishing post {post_id}: {str(e)}")
            post.status = PostStatus.failed
            post.error_message = str(e)
            post.retry_count += 1
            await session.commit()
            raise  # Reraise for Celery retry

async def _sync_daily_analytics_async():
    logger.info("Starting daily analytics sync")
    async with async_session_maker() as session:
        # Get all published posts
        stmt = select(SocialPost).where(SocialPost.status == PostStatus.published)
        result = await session.execute(stmt)
        posts = result.scalars().all()
        
        # Here we would group by account and fetch stats
        # For boilerplate, just log
        for post in posts:
            logger.info(f"Syncing stats for post {post.id} on {post.platform}")
        
        await session.commit()
        logger.info("Finished daily analytics sync")

@celery_app.task(bind=True, max_retries=3)
def publish_social_post(self, post_id_str: str):
    """Celery task to publish a social post with retry mechanism."""
    try:
        asyncio.run(_publish_post_async(post_id_str))
    except Exception as exc:
        logger.error(f"Task publish_social_post failed: {exc}")
        self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

@celery_app.task
def sync_daily_analytics():
    """Celery periodic task to sync daily analytics for all published posts."""
    asyncio.run(_sync_daily_analytics_async())
