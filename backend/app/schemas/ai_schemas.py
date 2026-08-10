from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SceneSchema(BaseModel):
    id: str = Field(description="Unique identifier for the scene")
    title: str = Field(description="Title of the scene")
    setting: str = Field(description="Setting of the scene (e.g., 'Interior, Living Room')")
    action: str = Field(description="Description of the action taking place")
    dialogue: Optional[List[Dict[str, str]]] = Field(description="Dialogue exchanges, e.g., [{'speaker': 'John', 'text': 'Hello'}]")
    duration_estimate: int = Field(description="Estimated duration in seconds")

class MicroClip(BaseModel):
    id: str = Field(description="Unique identifier for the micro-clip")
    scene_id: str = Field(description="ID of the scene this clip belongs to")
    description: str = Field(description="Visual description of the clip")
    camera_angle: str = Field(description="Camera angle (e.g., 'Close up', 'Wide shot')")
    prompt: str = Field(description="Prompt for the video generation model")
    duration: int = Field(description="Duration in seconds")

class MovieProjectSchema(BaseModel):
    title: str = Field(description="Title of the movie project")
    logline: str = Field(description="A brief summary of the movie")
    genre: str = Field(description="Genre of the movie")
    target_audience: str = Field(description="Target audience for the movie")
    scenes: List[SceneSchema] = Field(description="List of scenes in the movie")
    micro_clips: Optional[List[MicroClip]] = Field(description="Generated micro-clips for the movie")
