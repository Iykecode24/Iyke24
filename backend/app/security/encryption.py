from cryptography.fernet import Fernet
from app.config import settings

f = Fernet(settings.ENCRYPTION_KEY.encode() if settings.ENCRYPTION_KEY else Fernet.generate_key())

def encrypt_value(value: str) -> str:
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted: str) -> str:
    return f.decrypt(encrypted.encode()).decode()

def mask_secret(value: str) -> str:
    if not value or len(value) <= 4:
        return "****"
    return "*" * (len(value) - 4) + value[-4:]
