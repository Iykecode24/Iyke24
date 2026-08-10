import magic
from fastapi import UploadFile, HTTPException

def validate_file_type(file: UploadFile, allowed_types: list[str]) -> bool:
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
    pass

def scan_image_quality(file_path: str):
    pass
