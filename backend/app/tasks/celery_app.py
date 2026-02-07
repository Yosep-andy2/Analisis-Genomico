"""Celery application configuration."""

from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "genomics_analysis",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.analysis_tasks",
        "app.tasks.download_tasks"
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3000,  # 50 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

# Task routes (optional - for multiple queues)
celery_app.conf.task_routes = {
    "app.tasks.download_tasks.*": {"queue": "downloads"},
    "app.tasks.analysis_tasks.*": {"queue": "analysis"},
}
