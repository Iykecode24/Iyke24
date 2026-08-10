import uuid
import secrets
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status
import logging

from app.models.social import SocialAccount, SocialPost, SocialPlatform, PostStatus
from app.schemas.social import SocialAccountCreate, SocialPostCreate
from app.security.encryption import encrypt_value, decrypt_value
from app.integrations.social.factory import SocialIntegrationFactory
from app.config import settings

logger = logging.getLogger(__name__)

class SocialService:
    """Service handling real social media OAuth connections, token management, and post scheduling."""

    @staticmethod
    def _get_platform_credentials(platform: SocialPlatform) -> dict:
        # In a real system, these would be in settings
        creds = {
            SocialPlatform.youtube: {"client_id": settings.YOUTUBE_CLIENT_ID if hasattr(settings, "YOUTUBE_CLIENT_ID") else "dummy", "client_secret": settings.YOUTUBE_CLIENT_SECRET if hasattr(settings, "YOUTUBE_CLIENT_SECRET") else "dummy", "redirect_uri": f"{settings.API_V1_STR}/social/youtube/callback" if hasattr(settings, "API_V1_STR") else "http://localhost:8000/api/v1/social/youtube/callback"},
            SocialPlatform.tiktok: {"client_id": "dummy", "client_secret": "dummy", "redirect_uri": "http://localhost:8000/api/v1/social/tiktok/callback"},
            SocialPlatform.facebook: {"client_id": "dummy", "client_secret": "dummy", "redirect_uri": "http://localhost:8000/api/v1/social/facebook/callback"},
            SocialPlatform.instagram: {"client_id": "dummy", "client_secret": "dummy", "redirect_uri": "http://localhost:8000/api/v1/social/instagram/callback"},
            SocialPlatform.linkedin: {"client_id": "dummy", "client_secret": "dummy", "redirect_uri": "http://localhost:8000/api/v1/social/linkedin/callback"},
            SocialPlatform.x_twitter: {"client_id": "dummy", "client_secret": "dummy", "redirect_uri": "http://localhost:8000/api/v1/social/x_twitter/callback"},
            SocialPlatform.pinterest: {"client_id": "dummy", "client_secret": "dummy", "redirect_uri": "http://localhost:8000/api/v1/social/pinterest/callback"},
        }
        return creds.get(platform, {"client_id": "dummy", "client_secret": "dummy", "redirect_uri": "http://localhost:8000/api/v1/social/callback"})

    @staticmethod
    async def generate_oauth_url(platform: SocialPlatform, state: Optional[str] = None) -> str:
        """Generate the OAuth URL for the user to authorize the platform with a CSRF state token."""
        creds = SocialService._get_platform_credentials(platform)
        integration = SocialIntegrationFactory.get_integration(
            platform=platform,
            client_id=creds["client_id"],
            client_secret=creds["client_secret"],
            redirect_uri=creds["redirect_uri"]
        )
        if not state:
            state = secrets.token_urlsafe(32)
        url = integration.get_auth_url(state=state)
        return url

    @staticmethod
    async def connect_account(db: AsyncSession, user_id: uuid.UUID, data: SocialAccountCreate) -> SocialAccount:
        """
        Connect a new social account by exchanging the OAuth code for tokens, 
        discovering channel info, and securely storing credentials.
        """
        creds = SocialService._get_platform_credentials(data.platform)
        integration = SocialIntegrationFactory.get_integration(
            platform=data.platform,
            client_id=creds["client_id"],
            client_secret=creds["client_secret"],
            redirect_uri=creds["redirect_uri"]
        )
        
        try:
            # 1. Exchange code for token
            token_data = await integration.exchange_code(data.auth_code)
            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 3600)
            
            if not access_token:
                raise ValueError("Failed to obtain access token from provider.")

            # 2. Channel Discovery Engine: fetch profile info
            channel_info = await integration.get_channel_info(access_token)
            
            # 3. Encrypt tokens for secure storage
            access_token_enc = encrypt_value(access_token)
            refresh_token_enc = encrypt_value(refresh_token) if refresh_token else None
            expiry_time = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in)) if expires_in else None

            # 4. Save/Update Account
            stmt = select(SocialAccount).where(
                SocialAccount.user_id == user_id, 
                SocialAccount.platform == data.platform,
                SocialAccount.platform_user_id == channel_info["platform_user_id"]
            )
            result = await db.execute(stmt)
            existing_account = result.scalars().first()

            if existing_account:
                existing_account.access_token_encrypted = access_token_enc
                existing_account.refresh_token_encrypted = refresh_token_enc or existing_account.refresh_token_encrypted
                existing_account.token_expires_at = expiry_time
                existing_account.platform_username = channel_info["platform_username"]
                existing_account.avatar_url = channel_info["avatar_url"]
                existing_account.subscriber_count = channel_info["subscriber_count"]
                existing_account.channel_data = channel_info["channel_data"]
                existing_account.is_active = True
                account = existing_account
            else:
                account = SocialAccount(
                    user_id=user_id,
                    platform=data.platform,
                    access_token_encrypted=access_token_enc,
                    refresh_token_encrypted=refresh_token_enc,
                    token_expires_at=expiry_time,
                    platform_user_id=channel_info["platform_user_id"],
                    platform_username=channel_info["platform_username"],
                    avatar_url=channel_info["avatar_url"],
                    subscriber_count=channel_info["subscriber_count"],
                    channel_data=channel_info["channel_data"],
                    is_active=True
                )
                db.add(account)
                
            await db.commit()
            await db.refresh(account)
            return account
        
        except Exception as e:
            logger.error(f"Error connecting {data.platform} account: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        finally:
            await integration.close()

    @staticmethod
    async def refresh_account_token(db: AsyncSession, account: SocialAccount) -> str:
        """Automatically refresh access token if it has expired."""
        if not account.refresh_token_encrypted:
            raise ValueError("No refresh token available.")

        creds = SocialService._get_platform_credentials(account.platform)
        integration = SocialIntegrationFactory.get_integration(
            platform=account.platform,
            client_id=creds["client_id"],
            client_secret=creds["client_secret"],
            redirect_uri=creds["redirect_uri"]
        )

        try:
            refresh_token = decrypt_value(account.refresh_token_encrypted)
            token_data = await integration.refresh_token(refresh_token)
            
            new_access_token = token_data.get("access_token")
            new_refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 3600)

            if new_access_token:
                account.access_token_encrypted = encrypt_value(new_access_token)
            if new_refresh_token:
                account.refresh_token_encrypted = encrypt_value(new_refresh_token)
            if expires_in:
                account.token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=int(expires_in))
                
            await db.commit()
            return decrypt_value(account.access_token_encrypted)
        except Exception as e:
            logger.error(f"Failed to refresh token for {account.platform}: {str(e)}")
            account.is_active = False
            await db.commit()
            raise ValueError("Authentication expired. Please reconnect your account.")
        finally:
            await integration.close()

    @staticmethod
    async def get_valid_access_token(db: AsyncSession, account: SocialAccount) -> str:
        """Get a valid access token, refreshing if necessary."""
        # Add 5 minutes buffer
        if account.token_expires_at and account.token_expires_at < datetime.now(timezone.utc) + timedelta(minutes=5):
            return await SocialService.refresh_account_token(db, account)
        return decrypt_value(account.access_token_encrypted)

    @staticmethod
    async def get_user_accounts(db: AsyncSession, user_id: uuid.UUID) -> List[SocialAccount]:
        """Retrieve all connected social accounts for a user."""
        stmt = select(SocialAccount).where(SocialAccount.user_id == user_id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def schedule_post(db: AsyncSession, user_id: uuid.UUID, data: SocialPostCreate) -> SocialPost:
        """
        Schedule a post for a specific project on a specific social account.
        Dispatches to background worker.
        """
        stmt = select(SocialAccount).where(
            SocialAccount.id == data.social_account_id,
            SocialAccount.user_id == user_id,
            SocialAccount.is_active == True
        )
        result = await db.execute(stmt)
        account = result.scalars().first()
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Social account not found or not active"
            )
            
        if account.platform != data.platform:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Platform mismatch between account and requested post"
            )
        
        post_status = PostStatus.scheduled if data.scheduled_at else PostStatus.draft
        
        post = SocialPost(
            project_id=data.project_id,
            social_account_id=data.social_account_id,
            platform=data.platform,
            title=data.title,
            description=data.description,
            hashtags=data.hashtags,
            privacy_setting=data.privacy_setting,
            scheduled_at=data.scheduled_at,
            status=post_status
        )
        
        db.add(post)
        await db.commit()
        await db.refresh(post)
        
        # Enqueue job to Celery worker if it's scheduled immediately or in the future
        if post_status == PostStatus.scheduled:
            from app.workers.social_tasks import publish_social_post
            # Schedule task using Celery's eta or countdown based on scheduled_at
            eta = post.scheduled_at if post.scheduled_at else None
            publish_social_post.apply_async(args=[str(post.id)], eta=eta)
            
        return post

    @staticmethod
    async def get_project_posts(db: AsyncSession, project_id: uuid.UUID) -> List[SocialPost]:
        """Retrieve all posts for a specific project."""
        stmt = select(SocialPost).where(SocialPost.project_id == project_id)
        result = await db.execute(stmt)
        return list(result.scalars().all())
