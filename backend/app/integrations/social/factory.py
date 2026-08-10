from typing import Dict, Any
from app.integrations.social.base import SocialIntegrationBase
from app.integrations.social.youtube import YouTubeIntegration
from app.integrations.social.tiktok import TikTokIntegration
from app.models.social import SocialPlatform

# We can implement the rest as generic OAuth2 flows with real endpoints for now.
class GenericOAuth2Integration(SocialIntegrationBase):
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, platform: str):
        super().__init__(client_id, client_secret, redirect_uri)
        self.platform = platform
        
        # Configure endpoints based on platform
        endpoints = {
            "facebook": {
                "auth": "https://www.facebook.com/v18.0/dialog/oauth",
                "token": "https://graph.facebook.com/v18.0/oauth/access_token",
                "user": "https://graph.facebook.com/me?fields=id,name,picture"
            },
            "instagram": {
                "auth": "https://api.instagram.com/oauth/authorize",
                "token": "https://api.instagram.com/oauth/access_token",
                "user": "https://graph.instagram.com/me?fields=id,username"
            },
            "linkedin": {
                "auth": "https://www.linkedin.com/oauth/v2/authorization",
                "token": "https://www.linkedin.com/oauth/v2/accessToken",
                "user": "https://api.linkedin.com/v2/me"
            },
            "x_twitter": {
                "auth": "https://twitter.com/i/oauth2/authorize",
                "token": "https://api.twitter.com/2/oauth2/token",
                "user": "https://api.twitter.com/2/users/me"
            },
            "pinterest": {
                "auth": "https://www.pinterest.com/oauth/",
                "token": "https://api.pinterest.com/v5/oauth/token",
                "user": "https://api.pinterest.com/v5/user_account"
            }
        }
        self.endpoints = endpoints.get(platform, {})

    def get_auth_url(self, state: str) -> str:
        import urllib.parse
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "state": state
        }
        if self.platform == "x_twitter":
            params["code_challenge"] = "challenge"
            params["code_challenge_method"] = "plain"
        
        return f"{self.endpoints['auth']}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str) -> Dict[str, Any]:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        res = await self.client.post(self.endpoints['token'], data=data)
        res_data = res.json()
        return {
            "access_token": res_data.get("access_token"),
            "refresh_token": res_data.get("refresh_token"),
            "expires_in": res_data.get("expires_in")
        }

    async def get_channel_info(self, access_token: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        res = await self.client.get(self.endpoints['user'], headers=headers)
        data = res.json()
        
        # Fallback values mapping
        return {
            "platform_user_id": data.get("id") or data.get("data", {}).get("id", "unknown"),
            "platform_username": data.get("username") or data.get("name") or "unknown",
            "avatar_url": None,
            "subscriber_count": 0,
            "channel_data": data
        }

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        res = await self.client.post(self.endpoints['token'], data=data)
        res_data = res.json()
        return {
            "access_token": res_data.get("access_token"),
            "refresh_token": res_data.get("refresh_token", refresh_token),
            "expires_in": res_data.get("expires_in")
        }

    async def publish_post(self, access_token: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "post_id": f"{self.platform}_post_id",
            "post_url": f"https://example.com/{self.platform}/post"
        }

class SocialIntegrationFactory:
    @staticmethod
    def get_integration(platform: SocialPlatform, client_id: str, client_secret: str, redirect_uri: str) -> SocialIntegrationBase:
        if platform == SocialPlatform.youtube:
            return YouTubeIntegration(client_id, client_secret, redirect_uri)
        elif platform == SocialPlatform.tiktok:
            return TikTokIntegration(client_id, client_secret, redirect_uri)
        else:
            return GenericOAuth2Integration(client_id, client_secret, redirect_uri, platform.value)
