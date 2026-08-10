"""
OpenAI API Client for Iyke Content Studio.

Handles text generation, structured output, and compatible LLM
providers through the OpenAI-compatible API format.
"""

import json
import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)


class OpenAIClient:
    """
    Client for interacting with OpenAI and compatible LLM APIs.

    Supports:
    - Text generation (chat completions)
    - Structured JSON output
    - Streaming responses
    - Multiple model providers (OpenAI, Azure, local endpoints)
    - Connection testing
    """

    def __init__(
        self,
        api_key: str,
        endpoint: str = "https://api.openai.com/v1",
        default_model: str = "gpt-4o",
        timeout: float = 120.0,
        max_retries: int = 3,
    ):
        """Initialize the OpenAI client.

        Args:
            api_key: API key for authentication.
            endpoint: Base URL for the API (supports Azure, local endpoints).
            default_model: Default model to use for generation.
            timeout: Request timeout in seconds.
            max_retries: Maximum retry attempts for transient failures.
        """
        self.api_key = api_key
        self.endpoint = endpoint.rstrip("/")
        self.default_model = default_model
        self.timeout = timeout
        self.max_retries = max_retries
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _client(self) -> httpx.AsyncClient:
        """Create a new async HTTP client."""
        return httpx.AsyncClient(
            headers=self._headers,
            timeout=self.timeout,
        )

    async def generate_text(
        self,
        prompt: str,
        system_prompt: str = "You are a professional scriptwriter and creative director.",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """Generate text using chat completions.

        Args:
            prompt: User message / prompt.
            system_prompt: System message for context.
            model: Model to use (defaults to configured model).
            temperature: Creativity parameter (0.0 - 2.0).
            max_tokens: Maximum response tokens.

        Returns:
            Generated text content.
        """
        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        for attempt in range(self.max_retries):
            try:
                async with self._client() as client:
                    response = await client.post(
                        f"{self.endpoint}/chat/completions",
                        json=payload,
                    )
                    response.raise_for_status()
                    data = response.json()

                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                logger.info(
                    f"Generated text: {usage.get('total_tokens', 0)} tokens, "
                    f"model={model or self.default_model}"
                )
                return content

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < self.max_retries - 1:
                    import asyncio
                    wait_time = 2 ** (attempt + 1)
                    logger.warning(f"Rate limited, retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue
                raise
            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Timeout, retrying (attempt {attempt + 2}/{self.max_retries})...")
                    continue
                raise

        return ""

    async def generate_structured(
        self,
        prompt: str,
        response_format: Optional[dict[str, Any]] = None,
        system_prompt: str = "You are a professional scriptwriter. Respond only in valid JSON.",
        model: Optional[str] = None,
        temperature: float = 0.5,
        max_tokens: int = 8192,
    ) -> dict[str, Any]:
        """Generate structured JSON output.

        Args:
            prompt: User prompt requesting structured data.
            response_format: JSON schema for structured output.
            system_prompt: System message.
            model: Model to use.
            temperature: Creativity parameter.
            max_tokens: Maximum response tokens.

        Returns:
            Parsed JSON response as dict.
        """
        payload: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            payload["response_format"] = response_format
        else:
            payload["response_format"] = {"type": "json_object"}

        async with self._client() as client:
            response = await client.post(
                f"{self.endpoint}/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            logger.error(f"Failed to parse JSON response: {content[:200]}")
            return {"raw_content": content, "parse_error": True}

    async def generate_text_stream(
        self,
        prompt: str,
        system_prompt: str = "You are a professional scriptwriter.",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ):
        """Stream text generation token by token.

        Args:
            prompt: User message.
            system_prompt: System message.
            model: Model to use.
            temperature: Creativity parameter.
            max_tokens: Maximum tokens.

        Yields:
            Text chunks as they are generated.
        """
        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        async with self._client() as client:
            async with client.stream(
                "POST",
                f"{self.endpoint}/chat/completions",
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue

    async def check_connection(self) -> bool:
        """Verify the API key and endpoint are valid."""
        try:
            async with self._client() as client:
                response = await client.get(f"{self.endpoint}/models")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"OpenAI connection check failed: {e}")
            return False

    async def list_models(self) -> list[str]:
        """List available models from the provider."""
        try:
            async with self._client() as client:
                response = await client.get(f"{self.endpoint}/models")
                response.raise_for_status()
                data = response.json()
                return [m["id"] for m in data.get("data", [])]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
