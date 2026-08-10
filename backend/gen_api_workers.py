import os

BASE_DIR = r"c:\Users\user\Downloads\iyke-content-studio\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "app/api/v1/auth.py": """from fastapi import APIRouter
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
def update_me(): pass""",

    "app/api/v1/projects.py": """from fastapi import APIRouter
router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/")
def list_projects(): pass
@router.post("/")
def create_project(): pass
@router.get("/{id}")
def get_project(id: str): pass
@router.put("/{id}")
def update_project(id: str): pass
@router.delete("/{id}")
def delete_project(id: str): pass
@router.post("/{id}/duplicate")
def duplicate_project(id: str): pass
@router.get("/{id}/export")
def export_project(id: str): pass""",

    "app/api/v1/characters.py": """from fastapi import APIRouter
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
def save_library(id: str): pass""",

    "app/api/v1/render.py": """from fastapi import APIRouter
router = APIRouter(prefix="/render", tags=["render"])

@router.post("/estimate-cost")
def estimate_cost(): pass
@router.post("/start")
def start_render(): pass
@router.get("/jobs")
def list_jobs(): pass
@router.get("/jobs/{id}")
def get_job(id: str): pass
@router.post("/jobs/{id}/cancel")
def cancel_job(id: str): pass
@router.post("/jobs/{id}/retry")
def retry_job(id: str): pass
@router.get("/queue")
def get_queue(): pass""",

    "app/api/v1/media.py": """from fastapi import APIRouter
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
def signed_url(id: str): pass""",

    "app/api/v1/admin.py": """from fastapi import APIRouter
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/integrations")
def get_integrations(): pass
@router.post("/integrations")
def create_integration(): pass
@router.put("/integrations/{id}")
def update_integration(id: str): pass
@router.delete("/integrations/{id}")
def delete_integration(id: str): pass
@router.post("/integrations/{id}/test")
def test_integration(id: str): pass
@router.get("/models")
def get_models(): pass
@router.post("/models")
def create_model(): pass
@router.put("/models/{id}")
def update_model(id: str): pass
@router.delete("/models/{id}")
def delete_model(id: str): pass
@router.get("/gpu-instances")
def get_gpus(): pass
@router.post("/gpu-instances/{id}/stop")
def stop_gpu(id: str): pass
@router.post("/gpu-instances/{id}/terminate")
def terminate_gpu(id: str): pass
@router.get("/users")
def get_users(): pass
@router.put("/users/{id}/role")
def update_user_role(id: str): pass
@router.put("/users/{id}/status")
def update_user_status(id: str): pass
@router.get("/cost-limits")
def get_cost_limits(): pass
@router.put("/cost-limits")
def update_cost_limits(): pass
@router.get("/audit-logs")
def get_audit_logs(): pass
@router.get("/stats")
def get_stats(): pass""",

    "app/api/v1/health.py": """from fastapi import APIRouter
router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health(): return {"status": "ok"}
@router.get("/detailed")
def detailed_health(): return {"status": "ok"}""",

    "app/workers/__init__.py": "",

    "app/workers/celery_app.py": """from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)
celery_app.conf.task_routes = {'app.workers.*': {'queue': 'default'}}""",

    "app/workers/script_tasks.py": """from app.workers.celery_app import celery_app

@celery_app.task
def generate_full_script_task(project_id: str): pass

@celery_app.task
def regenerate_scene_task(scene_id: str): pass""",

    "app/workers/render_tasks.py": """from app.workers.celery_app import celery_app

@celery_app.task
def start_render_task(job_id: str): pass
@celery_app.task
def check_render_progress_task(job_id: str): pass
@celery_app.task
def gpu_lifecycle_task(instance_id: str): pass
@celery_app.task
def emergency_shutdown_task(): pass""",

    "alembic.ini": """[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///./test.db
[loggers]
keys = root,sqlalchemy,alembic
[handlers]
keys = console
[formatters]
keys = generic
[logger_root]
level = WARN
handlers = console
qualname =
[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine
[logger_alembic]
level = INFO
handlers =
qualname = alembic
[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic
[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S""",

    "alembic/env.py": """import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.config import settings
from app.database import Base
import app.models

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

run_migrations_online()""",

    "alembic/script.py.mako": """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
\"\"\"
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    ${downgrades if downgrades else "pass"}""",

    "alembic/versions/.gitkeep": ""
}

for path, content in files.items():
    write_file(path, content)
