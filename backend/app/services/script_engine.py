import logging
import uuid
from typing import Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field

from app.models.project import Project, ProjectStatus, ContentType

from app.models.script import Script, ScriptStatus
from app.models.scene import Scene, SceneStatus
from app.integrations.openai_client import OpenAIClient
from app.config import settings

logger = logging.getLogger(__name__)

class SceneSchema(BaseModel):
    title: str = Field(description="Title of the scene")
    description: str = Field(description="Detailed description of the scene action")
    dialogue: str | None = Field(None, description="Dialogue in the scene")
    narration: str | None = Field(None, description="Narration or voiceover")
    camera_direction: str | None = Field(None, description="Camera movement and placement")
    shot_type: str | None = Field(None, description="Type of shot (e.g., Close-up, Wide)")
    lighting: str | None = Field(None, description="Lighting description")
    visual_prompt: str | None = Field(None, description="Prompt for AI image/video generation")
    audio_prompt: str | None = Field(None, description="Prompt for AI audio/SFX generation")
    transition: str | None = Field(None, description="Transition to next scene")
    duration_seconds: int = Field(default=5, description="Estimated duration in seconds")

class ScriptGenerationSchema(BaseModel):
    title: str = Field(description="Title of the project")
    logline: str = Field(description="One-sentence logline")
    synopsis: str = Field(description="A short paragraph summarizing the story")
    full_text: str = Field(description="The complete script text")
    scenes: List[SceneSchema] = Field(description="Breakdown of scenes")


class ScriptEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        api_key = getattr(settings, "OPENAI_API_KEY", "dummy-key")
        self.client = OpenAIClient(api_key=api_key)

    async def generate_script(self, project_id: uuid.UUID) -> Script:
        """
        Generate a full script and scenes for a given project using its title/genre.
        """
        stmt = select(Project).where(Project.id == project_id)
        result = await self.db.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            raise ValueError(f"Project {project_id} not found")

        logger.info(f"Generating script for project {project.id}: {project.title} ({project.content_type.value})")
        project.status = ProjectStatus.scriptwriting
        await self.db.commit()

        system_prompt = "You are a creative writer and director. Output strictly in the requested JSON format."
        prompt_addons = ""
        
        if project.content_type == ContentType.news:
            system_prompt = "You are a professional news producer and writer. Output strictly in the requested JSON format."
            prompt_addons = "Structure the script as a news broadcast with a news anchor. Include B-roll scene descriptions. Ensure a professional and objective tone."
        elif project.content_type == ContentType.cartoon:
            system_prompt = "You are a children's cartoon writer and director. Output strictly in the requested JSON format."
            prompt_addons = "Ensure the tone, language, and themes are highly appropriate and engaging for kids. Use playful, imaginative elements."
        elif project.content_type == ContentType.explainer:
            system_prompt = "You are an educational content creator and director. Output strictly in the requested JSON format."
            prompt_addons = "Structure the script clearly to explain the concept step-by-step. Use a narrator or presenter, with helpful on-screen graphics."
        elif project.content_type == ContentType.advertisement:
            system_prompt = "You are a commercial copywriter and director. Output strictly in the requested JSON format."
            prompt_addons = "Focus on the value proposition. Make it punchy, persuasive, and visually striking. Include a strong call to action."
        elif project.content_type == ContentType.movie:
            system_prompt = "You are a professional screenwriter and film director. Output strictly in the requested JSON format."
            prompt_addons = "Structure the script with clear three-act storytelling, strong character development, and cinematic visual descriptions."

        prompt = f"""
        Generate a complete script for a {project.content_type.value} project.
        Title/Idea: {project.title}
        Genre: {project.genre or 'Not specified'}
        Target Audience: {project.target_audience or 'General'}
        Style: {project.visual_style or 'Standard'}
        
        Specific Instructions:
        {prompt_addons}
        
        CRITICAL: For dialogue, ensure "actor-first" natural delivery. Insert SSML <break time="Xs"/> tags for pregnant pauses. Maintain emotional continuity across scenes. Write dialogue exactly as it should be spoken, enforcing natural conversational flows.
        """

        try:
            # We use json_schema to force structure
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": "script_generation",
                    "schema": ScriptGenerationSchema.model_json_schema(),
                    "strict": True
                }
            }

            result_data = await self.client.generate_structured(
                prompt=prompt,
                response_format=response_format,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=8000
            )

            validated_data = ScriptGenerationSchema.model_validate(result_data)

            # Create Script
            script = Script(
                project_id=project.id,
                title=validated_data.title,
                logline=validated_data.logline,
                synopsis=validated_data.synopsis,
                full_text=validated_data.full_text,
                genre=project.genre,
                status=ScriptStatus.approved
            )
            self.db.add(script)
            await self.db.flush()

            # Create Scenes
            for idx, scene_data in enumerate(validated_data.scenes):
                scene = Scene(
                    script_id=script.id,
                    project_id=project.id,
                    order_index=idx,
                    title=scene_data.title,
                    description=scene_data.description,
                    dialogue=scene_data.dialogue,
                    narration=scene_data.narration,
                    camera_direction=scene_data.camera_direction,
                    shot_type=scene_data.shot_type,
                    lighting=scene_data.lighting,
                    visual_prompt=scene_data.visual_prompt,
                    audio_prompt=scene_data.audio_prompt,
                    transition=scene_data.transition,
                    duration_seconds=scene_data.duration_seconds,
                    status=SceneStatus.draft
                )
                self.db.add(scene)
            
            project.status = ProjectStatus.character_creation
            await self.db.commit()
            
            return script

        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            project.status = ProjectStatus.failed
            await self.db.commit()
            raise e
