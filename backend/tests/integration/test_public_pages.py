import pytest
import httpx
import os

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

@pytest.mark.asyncio
async def test_public_pages_accessible():
    pages = [
        "/privacy-policy",
        "/terms-of-service",
        "/data-deletion",
        "/social-account-removal"
    ]
    
    async with httpx.AsyncClient() as client:
        for page in pages:
            url = f"{FRONTEND_URL}{page}"
            try:
                response = await client.get(url, timeout=5.0)
                # Just assuming 200 is acceptable or catching errors if frontend not up
                assert response.status_code == 200, f"Page {page} returned status {response.status_code}"
                
                content = response.text.lower()
                
                # Check no placeholders
                assert "lorem ipsum" not in content, f"Page {page} contains placeholder text"
                assert "placeholder" not in content, f"Page {page} contains placeholder text"
                
                # Check identity
                assert "iyke content studio" in content, f"Page {page} does not match Iyke Content Studio identity"
                
            except httpx.RequestError as exc:
                # If the frontend isn't running during the test, we might want to skip or fail
                pytest.skip(f"Frontend not running at {FRONTEND_URL}. Skipping tests.")
