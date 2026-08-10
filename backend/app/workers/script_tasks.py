from app.workers.celery_app import celery_app

@celery_app.task
def generate_full_script_task(project_id: str): pass

@celery_app.task
def regenerate_scene_task(scene_id: str): pass
