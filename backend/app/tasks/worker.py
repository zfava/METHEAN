"""Celery worker configuration."""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "methean",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Beat schedule for nightly decay
celery_app.conf.beat_schedule = {
    "nightly-decay": {
        "task": "app.tasks.worker.nightly_decay_task",
        "schedule": crontab(
            hour=settings.DECAY_CRON_HOUR,
            minute=settings.DECAY_CRON_MINUTE,
        ),
    },
}


@celery_app.task(name="app.tasks.worker.nightly_decay_task")
def nightly_decay_task() -> dict:
    """Run the nightly FSRS decay batch job."""
    from app.tasks.decay import run_decay_sync
    return run_decay_sync()


# Alias for celery -A app.tasks.worker
app = celery_app
