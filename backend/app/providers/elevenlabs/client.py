import httpx
from app.config import settings

class ElevenLabsClient:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

    async def generate_audio(self, voice_id: str, text: str, model_id: str = "eleven_monolingual_v1", voice_settings: dict = None) -> bytes:
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        data = {
            "text": text,
            "model_id": model_id,
        }
        
        if voice_settings:
            data["voice_settings"] = voice_settings

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=self.headers, timeout=60.0)
            response.raise_for_status()
            return response.content

    async def get_voices(self) -> dict:
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
