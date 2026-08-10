from typing import List
from .client import get_openai_client

async def generate_embedding(
    text: str,
    model: str = "text-embedding-3-small"
) -> List[float]:
    """
    Generates an embedding vector for the given text.
    """
    client = get_openai_client()
    
    response = await client.embeddings.create(
        input=text,
        model=model
    )
    
    return response.data[0].embedding
