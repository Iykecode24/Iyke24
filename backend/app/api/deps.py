from app.database import get_db
from app.security.auth import get_current_user, require_role
from app.models.user import UserRole

def get_current_admin():
    return require_role(UserRole.admin)
