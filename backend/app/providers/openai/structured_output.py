from typing import Type, Any, TypeVar
from pydantic import BaseModel
from .client import get_openai_client

T = TypeVar('T', bound=BaseModel)

async def generate_structured_output(
    model: str,
    messages: list[dict[str, Any]],
    response_model: Type[T],
    temperature: float = 0.7,
    max_tokens: int = 1000,
) -> T:
    """
    Generates a structured output matching the provided Pydantic model.
    Requires openai >= 1.40.0 for `beta.chat.completions.parse`.
    """
    client = get_openai_client()
    
    completion = await client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=response_model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    
    return completion.choices[0].message.parsed
