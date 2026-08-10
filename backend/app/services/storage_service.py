import boto3
from app.config import settings

def get_client():
    return boto3.client('s3')

def upload_file(file, path: str) -> str:
    return f"https://storage.example.com/{path}"

def generate_signed_url(path: str, expires: int) -> str:
    return f"https://storage.example.com/{path}?signed=true"

def delete_file(path: str):
    pass

def list_files(prefix: str):
    return []

def get_storage_usage(user_id: str) -> int:
    return 0
