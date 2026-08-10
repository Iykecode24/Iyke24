from celery import Celery
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.workers.render_tasks', 'app.workers.script_tasks', 'app.workers.social_tasks']
)
celery_app.conf.task_routes = {'app.workers.*': {'queue': 'default'}}

celery_app.conf.beat_schedule = {
    'sync-daily-social-analytics': {
        'task': 'app.workers.social_tasks.sync_daily_analytics',
        'schedule': 86400.0, # Every 24 hours
    },
}
