from fastapi import APIRouter
router = APIRouter(prefix="/media", tags=["media"])

@router.get("/")
def list_media(): pass
@router.post("/upload")
def upload_media(): pass
@router.get("/{id}")
def get_media(id: str): pass
@router.delete("/{id}")
def delete_media(id: str): pass
@router.get("/{id}/signed-url")
def signed_url(id: str): pass
