from fastapi import APIRouter
router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health(): return {"status": "ok"}
@router.get("/detailed")
def detailed_health(): return {"status": "ok"}
