import os
from openai import AsyncOpenAI
from app.config import settings

# Initialize AsyncOpenAI client
# Make sure to have OPENAI_API_KEY in the environment or settings
api_key = getattr(settings, "OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))

# Use a singleton client to avoid re-initializing
client = AsyncOpenAI(api_key=api_key)

def get_openai_client() -> AsyncOpenAI:
    return client
