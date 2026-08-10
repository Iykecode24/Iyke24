from fastapi import APIRouter
router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/")
def list_characters(): pass
@router.post("/")
def create_character(): pass
@router.get("/{id}")
def get_character(id: str): pass
@router.put("/{id}")
def update_character(id: str): pass
@router.delete("/{id}")
def delete_character(id: str): pass
@router.post("/{id}/upload-reference")
def upload_reference(id: str): pass
@router.post("/{id}/save-to-library")
def save_library(id: str): pass
