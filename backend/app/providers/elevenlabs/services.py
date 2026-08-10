import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.providers.elevenlabs.client import ElevenLabsClient
from app.services.storage import StorageService
from app.models.media import AudioFile, AudioType
from app.models.billing import UsageRecord, ResourceType

class ElevenLabsService:
    def __init__(self, db_session: AsyncSession):
        self.client = ElevenLabsClient()
        self.storage = StorageService()
        self.db = db_session

    async def generate_and_save_audio(
        self, 
        project_id: uuid.UUID,
        user_id: uuid.UUID,
        text: str, 
        voice_id: str, 
        db_voice_id: uuid.UUID = None,
        model_id: str = "eleven_monolingual_v1",
        scene_id: uuid.UUID = None,
        audio_type: AudioType = AudioType.dialogue,
        emotional_context: str = "neutral"
    ) -> AudioFile:
        # Map emotional context to voice settings to prevent rushed/robotic delivery
        voice_settings = {"stability": 0.5, "similarity_boost": 0.75}
        if emotional_context in ["angry", "excited", "panicked"]:
            voice_settings = {"stability": 0.3, "similarity_boost": 0.6}
        elif emotional_context in ["sad", "serious", "whispering"]:
            voice_settings = {"stability": 0.7, "similarity_boost": 0.8}

        # 1. Generate audio bytes from ElevenLabs
        audio_bytes = await self.client.generate_audio(
            voice_id=voice_id, 
            text=text, 
            model_id=model_id,
            voice_settings=voice_settings
        )
        
        # 2. Save byte stream to Cloudflare R2
        audio_url = self.storage.upload_audio(audio_bytes)
        
        # We don't have accurate duration from bytes unless we inspect it, default to a rough estimate or 0
        duration_estimate = len(audio_bytes) / 32000.0  # rough estimate for mp3
        
        # 3. Create AudioFile (AudioAsset) record
        audio_file = AudioFile(
            project_id=project_id,
            scene_id=scene_id,
            type=audio_type,
            url=audio_url,
            duration_seconds=duration_estimate,
            provider="elevenlabs",
            voice_id=db_voice_id,
            transcript=text
        )
        self.db.add(audio_file)
        
        # 4. Create ProviderUsage (UsageRecord) record
        usage = UsageRecord(
            user_id=user_id,
            project_id=project_id,
            resource_type=ResourceType.voice,
            quantity=len(text), # ElevenLabs charges by character
            unit="characters",
            unit_cost=0.00015, # example cost
            total_cost=len(text) * 0.00015,
            provider="elevenlabs"
        )
        self.db.add(usage)
        
        await self.db.commit()
        await self.db.refresh(audio_file)
        
        return audio_file
