from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
from datetime import datetime, timezone

class SocialIntegrationBase(ABC):
    """Base class for all social media integrations."""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.client = httpx.AsyncClient(timeout=30.0)

    @abstractmethod
    def get_auth_url(self, state: str) -> str:
        """Return the OAuth URL to redirect the user to."""
        pass

    @abstractmethod
    async def exchange_code(self, code: str) -> Dict[str, Any]:
        """
        Exchange an OAuth code for access/refresh tokens.
        Expected return format:
        {
            "access_token": "str",
            "refresh_token": "Optional[str]",
            "expires_in": int (seconds)
        }
        """
        pass

    @abstractmethod
    async def get_channel_info(self, access_token: str) -> Dict[str, Any]:
        """
        Fetch information about the authenticated channel/user.
        Expected return format:
        {
            "platform_user_id": "str",
            "platform_username": "str",
            "avatar_url": "Optional[str]",
            "subscriber_count": "Optional[int]",
            "channel_data": "Optional[dict]"  # Contains sub-channels, pages, etc.
        }
        """
        pass

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh the access token.
        Expected return format same as exchange_code.
        """
        pass

    @abstractmethod
    async def publish_post(self, access_token: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish a post or video to the platform.
        Expected return format:
        {
            "post_id": "str",
            "post_url": "str"
        }
        """
        pass

    async def close(self):
        await self.client.aclose()
