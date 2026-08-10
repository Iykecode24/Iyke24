import os

BASE_DIR = r"c:\Users\user\Downloads\iyke-content-studio\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "app/security/__init__.py": "",

    "app/security/auth.py": """from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config import settings
from app.database import get_db
from app.models.user import User, UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    result = await db.execute(select(User).where(User.id == user_id, User.is_active == True))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

def require_role(role: UserRole):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role != role and user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker

def require_roles(*roles: UserRole):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles and user.role != UserRole.admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker""",

    "app/security/encryption.py": """from cryptography.fernet import Fernet
from app.config import settings

f = Fernet(settings.ENCRYPTION_KEY.encode() if settings.ENCRYPTION_KEY else Fernet.generate_key())

def encrypt_value(value: str) -> str:
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted: str) -> str:
    return f.decrypt(encrypted.encode()).decode()

def mask_secret(value: str) -> str:
    if not value or len(value) <= 4:
        return "****"
    return "*" * (len(value) - 4) + value[-4:]""",

    "app/security/rate_limiter.py": """from fastapi import Request, HTTPException
import time

# Simple in-memory fallback if Redis is not connected yet
_limits = {}

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    if client_ip not in _limits:
        _limits[client_ip] = []
    
    # Clean old requests (e.g., last minute)
    _limits[client_ip] = [t for t in _limits[client_ip] if now - t < 60]
    
    if len(_limits[client_ip]) > 100:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    _limits[client_ip].append(now)
    return await call_next(request)""",

    "app/security/file_scanner.py": """import magic
from fastapi import UploadFile, HTTPException

def validate_file_type(file: UploadFile, allowed_types: list[str]) -> bool:
    # Read first 2048 bytes for magic
    header = file.file.read(2048)
    file.file.seek(0)
    mime = magic.from_buffer(header, mime=True)
    if mime not in allowed_types:
        raise HTTPException(status_code=400, detail=f"File type {mime} not allowed")
    return True

def validate_file_size(file: UploadFile, max_size: int):
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > max_size:
        raise HTTPException(status_code=400, detail="File too large")

def strip_metadata(file_path: str):
    pass  # Requires PIL implementation for images

def scan_image_quality(file_path: str):
    pass""",

    "app/security/content_filter.py": """from typing import List, Optional

class ContentCheckResult:
    is_safe: bool
    flagged_reasons: List[str]

def check_text_safety(text: str) -> ContentCheckResult:
    blocked_words = ["violence", "terrorism", "hate"]
    reasons = [w for w in blocked_words if w in text.lower()]
    result = ContentCheckResult()
    result.is_safe = len(reasons) == 0
    result.flagged_reasons = reasons
    return result

def check_consent_required(content_type: str) -> bool:
    return content_type in ["deepfake", "voice_clone"]

def flag_content(project_id: str, content: str, reason: str):
    pass  # Log to DB"""
}

for path, content in files.items():
    write_file(path, content)
