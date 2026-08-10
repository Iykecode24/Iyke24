"""
ElevenLabs API Client for Iyke Content Studio.

Handles text-to-speech generation, voice listing, voice cloning,
and usage tracking through the ElevenLabs REST API.
"""

import logging
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Optional

import httpx

logger = logging.getLogger(__name__)

ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"


@dataclass
class ElevenLabsVoice:
    """Represents an ElevenLabs voice."""
    voice_id: str
    name: str
    category: str = ""
    description: str = ""
    labels: dict[str, str] | None = None
    preview_url: str = ""


@dataclass
class VoiceSettings:
    """Settings for voice generation."""
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True


class ElevenLabsClient:
    """
    Client for interacting with the ElevenLabs API.

    Supports:
    - Text-to-speech generation (standard and streaming)
    - Voice listing and discovery
    - Voice settings configuration
    - Usage and subscription tracking
    - Connection testing
    """

    def __init__(self, api_key: str, timeout: float = 60.0):
        """Initialize the ElevenLabs client.

        Args:
            api_key: ElevenLabs API key.
            timeout: Default request timeout in seconds.
        """
        self.api_key = api_key
        self.timeout = timeout
        self._headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        }

    def _client(self) -> httpx.AsyncClient:
        """Create a new async HTTP client."""
        return httpx.AsyncClient(
            headers=self._headers,
            timeout=self.timeout,
        )

    async def list_voices(self) -> list[ElevenLabsVoice]:
        """List all available voices."""
        async with self._client() as client:
            response = await client.get(f"{ELEVENLABS_API_BASE}/voices")
            response.raise_for_status()
            data = response.json()

        voices = []
        for voice_data in data.get("voices", []):
            voices.append(ElevenLabsVoice(
                voice_id=voice_data.get("voice_id", ""),
                name=voice_data.get("name", ""),
                category=voice_data.get("category", ""),
                description=voice_data.get("description", ""),
                labels=voice_data.get("labels"),
                preview_url=voice_data.get("preview_url", ""),
            ))
        return voices

    async def generate_speech(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_multilingual_v2",
        settings: Optional[VoiceSettings] = None,
    ) -> bytes:
        """Generate speech audio from text.

        Args:
            text: Text to convert to speech.
            voice_id: ElevenLabs voice ID.
            model_id: Model to use for generation.
            settings: Voice settings (stability, similarity, etc.).

        Returns:
            Audio data as bytes (MPEG format).
        """
        if settings is None:
            settings = VoiceSettings()

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": settings.stability,
                "similarity_boost": settings.similarity_boost,
                "style": settings.style,
                "use_speaker_boost": settings.use_speaker_boost,
            },
        }

        async with self._client() as client:
            response = await client.post(
                f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}",
                json=payload,
            )
            response.raise_for_status()

        logger.info(f"Generated speech for voice {voice_id} ({len(response.content)} bytes)")
        return response.content

    async def generate_speech_stream(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_flash_v2_5",
        settings: Optional[VoiceSettings] = None,
    ) -> AsyncGenerator[bytes, None]:
        """Stream speech audio from text.

        Args:
            text: Text to convert to speech.
            voice_id: ElevenLabs voice ID.
            model_id: Model to use (flash for lower latency).
            settings: Voice settings.

        Yields:
            Audio chunks as bytes.
        """
        if settings is None:
            settings = VoiceSettings()

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": settings.stability,
                "similarity_boost": settings.similarity_boost,
                "style": settings.style,
                "use_speaker_boost": settings.use_speaker_boost,
            },
        }

        async with self._client() as client:
            async with client.stream(
                "POST",
                f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}/stream",
                json=payload,
            ) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=4096):
                    yield chunk

    async def get_voice(self, voice_id: str) -> ElevenLabsVoice:
        """Get details of a specific voice."""
        async with self._client() as client:
            response = await client.get(f"{ELEVENLABS_API_BASE}/voices/{voice_id}")
            response.raise_for_status()
            data = response.json()

        return ElevenLabsVoice(
            voice_id=data.get("voice_id", ""),
            name=data.get("name", ""),
            category=data.get("category", ""),
            description=data.get("description", ""),
            labels=data.get("labels"),
            preview_url=data.get("preview_url", ""),
        )

    async def get_usage(self) -> dict[str, Any]:
        """Get subscription usage information."""
        async with self._client() as client:
            response = await client.get(f"{ELEVENLABS_API_BASE}/user/subscription")
            response.raise_for_status()
            data = response.json()

        return {
            "character_count": data.get("character_count", 0),
            "character_limit": data.get("character_limit", 0),
            "remaining_characters": data.get("character_limit", 0) - data.get("character_count", 0),
            "tier": data.get("tier", "free"),
            "next_reset": data.get("next_character_count_reset_unix"),
        }

    async def check_connection(self) -> bool:
        """Verify the API key is valid."""
        try:
            async with self._client() as client:
                response = await client.get(f"{ELEVENLABS_API_BASE}/user")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"ElevenLabs connection check failed: {e}")
            return False
