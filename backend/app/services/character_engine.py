import uuid
import json
import logging
from typing import Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.character import Character
from app.integrations.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class CharacterEngine:
    """
    Engine for generating and managing character profiles using AI.
    """
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def generate_character_from_script(
        self, 
        session: AsyncSession, 
        user_id: uuid.UUID,
        project_id: Optional[uuid.UUID],
        script_content: str, 
        character_name: str
    ) -> Character:
        """
        Auto-generates a character profile based on a script's content using OpenAI.
        Saves the resulting profile to the database.
        """
        prompt = f"Analyze the following script and extract a detailed character profile for '{character_name}'.\n\nScript:\n{script_content}"
        system_prompt = "You are an expert character designer and script analyzer. Extract character details into valid JSON matching the exact schema provided."
        
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "character_profile",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "age": {"type": "integer"},
                        "gender": {"type": "string"},
                        "role": {"type": "string"},
                        "appearance": {"type": "string"},
                        "wardrobe": {"type": "string"},
                        "accessories": {"type": "string"},
                        "personality": {"type": "string"},
                        "skin_tone": {"type": "string"},
                        "hair_description": {"type": "string"},
                        "body_type": {"type": "string"},
                        "accent": {"type": "string"},
                        "negative_prompt": {"type": "string"},
                        "prompt_template": {"type": "string"}
                    },
                    "required": ["name", "description", "age", "gender", "role", "appearance", "wardrobe", "accessories", "personality", "skin_tone", "hair_description", "body_type", "accent", "negative_prompt", "prompt_template"],
                    "additionalProperties": False
                }
            }
        }

        logger.info(f"Generating character profile for {character_name}")
        profile_data = await self.openai_client.generate_structured(
            prompt=prompt,
            system_prompt=system_prompt,
            response_format=response_format,
            temperature=0.7
        )

        if "parse_error" in profile_data:
            raise ValueError(f"Failed to generate valid character profile: {profile_data.get('raw_content')}")

        character = Character(
            id=uuid.uuid4(),
            user_id=user_id,
            project_id=project_id,
            name=profile_data.get("name", character_name),
            description=profile_data.get("description"),
            age=profile_data.get("age"),
            gender=profile_data.get("gender"),
            role=profile_data.get("role"),
            appearance=profile_data.get("appearance"),
            wardrobe=profile_data.get("wardrobe"),
            accessories=profile_data.get("accessories"),
            personality=profile_data.get("personality"),
            skin_tone=profile_data.get("skin_tone"),
            hair_description=profile_data.get("hair_description"),
            body_type=profile_data.get("body_type"),
            accent=profile_data.get("accent"),
            negative_prompt=profile_data.get("negative_prompt"),
            prompt_template=profile_data.get("prompt_template")
        )

        session.add(character)
        await session.commit()
        await session.refresh(character)
        
        return character
