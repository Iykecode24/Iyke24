from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.projects import router as projects_router
from app.api.v1.characters import router as characters_router
from app.api.v1.render import router as render_router
from app.api.v1.media import router as media_router
from app.api.v1.admin import router as admin_router
from app.api.v1.health import router as health_router
from app.api.v1.scripts import router as scripts_router
from app.api.v1.social import router as social_router
from app.api.v1.privacy import router as privacy_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(auth_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(characters_router, prefix="/api/v1")
app.include_router(render_router, prefix="/api/v1")
app.include_router(media_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(scripts_router, prefix="/api/v1")
app.include_router(social_router, prefix="/api/v1")
app.include_router(privacy_router, prefix="/api/privacy")

@app.get("/")
def read_root():
    return {"status": "ok"}
