from typing import AsyncGenerator, Any
from .client import get_openai_client

async def generate_streaming_output(
    model: str,
    messages: list[dict[str, Any]],
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> AsyncGenerator[str, None]:
    """
    Generates streaming text output.
    """
    client = get_openai_client()
    
    stream = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
