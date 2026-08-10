from .client import get_openai_client

async def check_moderation(input_text: str) -> bool:
    """
    Checks if the input text passes OpenAI's moderation guidelines.
    Returns True if flagged, False otherwise.
    """
    client = get_openai_client()
    
    response = await client.moderations.create(input=input_text)
    
    return response.results[0].flagged
