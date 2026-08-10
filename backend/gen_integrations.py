import os

BASE_DIR = r"c:\Users\user\Downloads\iyke-content-studio\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "app/integrations/__init__.py": "",

    "app/integrations/openai_client.py": """import httpx

class OpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    async def generate_text(self, prompt: str, system_prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        return "Generated text"
        
    async def generate_structured(self, prompt: str, response_format: dict, model: str) -> dict:
        return {}
        
    async def check_connection(self) -> bool:
        return True""",

    "app/integrations/elevenlabs_client.py": """from typing import AsyncGenerator
from app.models.voice import Voice

class ElevenLabsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def list_voices(self) -> list[Voice]:
        return []

    async def generate_speech(self, text: str, voice_id: str, settings: dict) -> bytes:
        return b""

    async def generate_speech_stream(self, text: str, voice_id: str) -> AsyncGenerator:
        yield b""

    async def check_connection(self) -> bool:
        return True

    async def get_usage(self) -> dict:
        return {}""",

    "app/integrations/runpod_client.py": """class Pod:
    pass
class PodStatus:
    pass
class Volume:
    pass
class GpuType:
    pass
class JobStatus:
    pass

class RunPodClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def create_pod(self, name: str, image: str, gpu_type: str, volume_id: str, env: dict) -> Pod:
        return Pod()
    async def start_pod(self, pod_id: str): pass
    async def stop_pod(self, pod_id: str): pass
    async def terminate_pod(self, pod_id: str): pass
    async def get_pod_status(self, pod_id: str) -> PodStatus: return PodStatus()
    async def list_pods(self) -> list[Pod]: return []
    async def submit_serverless_job(self, endpoint_id: str, input_data: dict) -> str: return "job_id"
    async def get_job_status(self, endpoint_id: str, job_id: str) -> JobStatus: return JobStatus()
    async def cancel_job(self, endpoint_id: str, job_id: str): pass
    async def list_network_volumes(self) -> list[Volume]: return []
    async def check_connection(self) -> bool: return True
    async def get_gpu_types(self) -> list[GpuType]: return []""",

    "app/integrations/storage_client.py": """class StorageClient:
    def __init__(self, provider: str, config: dict):
        self.provider = provider
        self.config = config

    def upload(self, file_data, path: str): pass
    def download(self, path: str): pass
    def delete(self, path: str): pass
    def list(self, prefix: str): pass
    def signed_url(self, path: str): return ""
    def check_connection(self) -> bool: return True""",

    "app/api/__init__.py": "",

    "app/api/deps.py": """from app.database import get_db
from app.security.auth import get_current_user, require_role
from app.models.user import UserRole

def get_current_admin():
    return require_role(UserRole.admin)""",

    "app/api/v1/__init__.py": "",

    "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

@app.get("/")
def read_root():
    return {"status": "ok"}
"""
}

for path, content in files.items():
    write_file(path, content)
