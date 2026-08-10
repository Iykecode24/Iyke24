from fastapi import APIRouter
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(): pass
@router.post("/login")
def login(): pass
@router.post("/logout")
def logout(): pass
@router.post("/refresh")
def refresh(): pass
@router.post("/password-reset/request")
def password_reset_req(): pass
@router.post("/password-reset/confirm")
def password_reset_confirm(): pass
@router.post("/mfa/setup")
def mfa_setup(): pass
@router.post("/mfa/verify")
def mfa_verify(): pass
@router.post("/mfa/disable")
def mfa_disable(): pass
@router.get("/me")
def get_me(): pass
@router.put("/me")
def update_me(): pass
