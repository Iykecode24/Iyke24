from typing import Dict, Any
from app.integrations.social.base import SocialIntegrationBase
import urllib.parse
from fastapi import HTTPException
import httpx

class YouTubeIntegration(SocialIntegrationBase):
    def get_auth_url(self, state: str) -> str:
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly",
            "access_type": "offline",
            "prompt": "consent",
            "state": state
        }
        return f"{base_url}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        response = await self.client.post(url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"YouTube OAuth error: {response.text}")
        
        resp_data = response.json()
        return {
            "access_token": resp_data.get("access_token"),
            "refresh_token": resp_data.get("refresh_token"),
            "expires_in": resp_data.get("expires_in")
        }

    async def get_channel_info(self, access_token: str) -> Dict[str, Any]:
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "snippet,statistics",
            "mine": "true"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await self.client.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"YouTube Channel Fetch error: {response.text}")
        
        data = response.json()
        if not data.get("items"):
            raise HTTPException(status_code=404, detail="No YouTube channel found for user.")
            
        channel = data["items"][0]
        snippet = channel.get("snippet", {})
        stats = channel.get("statistics", {})
        
        return {
            "platform_user_id": channel.get("id"),
            "platform_username": snippet.get("title"),
            "avatar_url": snippet.get("thumbnails", {}).get("default", {}).get("url"),
            "subscriber_count": int(stats.get("subscriberCount", 0)),
            "channel_data": {"customUrl": snippet.get("customUrl")}
        }

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        response = await self.client.post(url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"YouTube Token Refresh error: {response.text}")
        
        resp_data = response.json()
        return {
            "access_token": resp_data.get("access_token"),
            "refresh_token": resp_data.get("refresh_token", refresh_token),
            "expires_in": resp_data.get("expires_in")
        }

    async def publish_post(self, access_token: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        # Typically requires resumable upload, simplified here for boilerplate
        url = "https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # In a real implementation we would stream the file from post_data['video_path']
        metadata = {
            "snippet": {
                "title": post_data.get("title", ""),
                "description": post_data.get("description", ""),
                "tags": post_data.get("tags", []),
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": post_data.get("privacy_setting", "private")
            }
        }
        
        # Since this involves multipart upload, it is more complex.
        # Providing boilerplate structure.
        return {
            "post_id": "yt_placeholder_id",
            "post_url": f"https://youtube.com/watch?v=yt_placeholder_id"
        }
