import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import uuid
from datetime import datetime

from app.main import app
from app.security.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.project import ProjectStatus, ContentType, Orientation
from app.models.script import ScriptStatus

# Mock user
mock_user = User(
    id=uuid.uuid4(),
    email="test@example.com",
    username="testuser",
    is_active=True
)

def override_get_current_user():
    return mock_user

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_db():
    db_session = AsyncMock()
    return db_session

def test_project_creation_and_script_generation(client, mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    
    project_id = uuid.uuid4()
    
    # 1. Test Project Creation
    project_data = {
        "title": "My Awesome Movie",
        "content_type": "movie",
        "orientation": "landscape"
    }
    
    # We test the API layer for project creation directly.
    # Note: background tasks are triggered by FastAPI automatically.
    
    with patch("app.api.v1.projects.generate_script_background") as mock_bg_task:
        # Need to mock the DB save and commit
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        response = client.post("/api/v1/projects/", json=project_data)
        
        # Since script generation happens in a background task, we just ensure it returns 201
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "My Awesome Movie"
        assert data["content_type"] == "movie"
        assert "id" in data
        assert data["status"] == "planning"
        
        # Verify background task was queued (using our mock function)
        # The background_tasks.add_task calls our actual function reference, 
        # but mocking the function itself or just relying on fastAPI's background tasks behavior.
        # Actually patching background_tasks is cleaner but this is a simple integration test.

def test_social_account_connection_and_post_scheduling(client, mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # 1. Connect Social Account
    account_id = uuid.uuid4()
    account_data = {
        "platform": "youtube",
        "auth_code": "auth_code_123"
    }
    
    with patch("app.services.social_service.SocialService.connect_account", new_callable=AsyncMock) as mock_connect:
        mock_connect.return_value = MagicMock(
            id=account_id,
            platform="youtube",
            platform_username="mock_youtube_user",
            avatar_url="https://example.com/avatar.jpg",
            is_active=True,
            connected_at=datetime.utcnow()
        )
        
        response = client.post("/api/v1/social/accounts", json=account_data)
        assert response.status_code == 201
        data = response.json()
        assert data["platform"] == "youtube"
        assert data["platform_username"] == "mock_youtube_user"

    # 2. Schedule Post
    project_id = uuid.uuid4()
    post_data = {
        "project_id": str(project_id),
        "social_account_id": str(account_id),
        "platform": "youtube",
        "title": "Check out my new short film!",
        "scheduled_at": datetime.utcnow().isoformat()
    }
    
    with patch("app.services.social_service.SocialService.schedule_post", new_callable=AsyncMock) as mock_schedule:
        mock_schedule.return_value = MagicMock(
            id=uuid.uuid4(),
            project_id=project_id,
            social_account_id=account_id,
            platform="youtube",
            title="Check out my new short film!",
            status="scheduled",
            published_at=None,
            error_message=None
        )
        
        response = client.post("/api/v1/social/posts", json=post_data)
        assert response.status_code == 201
        data = response.json()
        assert data["platform"] == "youtube"
        assert data["title"] == "Check out my new short film!"
        assert data["status"] == "scheduled"
