from typing import Dict, Any
from app.integrations.social.base import SocialIntegrationBase
import urllib.parse
from fastapi import HTTPException

class TikTokIntegration(SocialIntegrationBase):
    def get_auth_url(self, state: str) -> str:
        base_url = "https://www.tiktok.com/v2/auth/authorize/"
        params = {
            "client_key": self.client_id,
            "response_type": "code",
            "scope": "user.info.basic,video.upload,video.publish",
            "redirect_uri": self.redirect_uri,
            "state": state
        }
        return f"{base_url}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str) -> Dict[str, Any]:
        url = "https://open.tiktokapis.com/v2/oauth/token/"
        data = {
            "client_key": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        response = await self.client.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"TikTok OAuth error: {response.text}")
        
        resp_data = response.json()
        return {
            "access_token": resp_data.get("access_token"),
            "refresh_token": resp_data.get("refresh_token"),
            "expires_in": resp_data.get("expires_in")
        }

    async def get_channel_info(self, access_token: str) -> Dict[str, Any]:
        url = "https://open.tiktokapis.com/v2/user/info/"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"fields": "open_id,union_id,avatar_url,display_name,follower_count"}
        response = await self.client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"TikTok Channel Fetch error: {response.text}")
        
        data = response.json().get("data", {}).get("user", {})
        
        return {
            "platform_user_id": data.get("open_id"),
            "platform_username": data.get("display_name"),
            "avatar_url": data.get("avatar_url"),
            "subscriber_count": data.get("follower_count", 0),
            "channel_data": {"union_id": data.get("union_id")}
        }

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        url = "https://open.tiktokapis.com/v2/oauth/token/"
        data = {
            "client_key": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        response = await self.client.post(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"TikTok Token Refresh error: {response.text}")
        
        resp_data = response.json()
        return {
            "access_token": resp_data.get("access_token"),
            "refresh_token": resp_data.get("refresh_token", refresh_token),
            "expires_in": resp_data.get("expires_in")
        }

    async def publish_post(self, access_token: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        # Boilerplate for TikTok video publish
        return {
            "post_id": "tk_placeholder_id",
            "post_url": "https://tiktok.com/@user/video/tk_placeholder_id"
        }
