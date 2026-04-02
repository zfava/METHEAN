"""Celery worker configuration with all scheduled tasks."""

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
    task_default_retry_delay=30,
    task_max_retries=3,
)

# Beat schedule
celery_app.conf.beat_schedule = {
    "nightly-decay": {
        "task": "app.tasks.worker.nightly_decay_task",
        "schedule": crontab(hour=settings.DECAY_CRON_HOUR, minute=settings.DECAY_CRON_MINUTE),
    },
    "weekly-snapshots": {
        "task": "app.tasks.worker.weekly_snapshot_task",
        "schedule": crontab(day_of_week="sunday", hour=0, minute=0),
    },
}


@celery_app.task(name="app.tasks.worker.nightly_decay_task", bind=True, max_retries=3)
def nightly_decay_task(self) -> dict:
    """Run the nightly FSRS decay batch job."""
    try:
        from app.tasks.decay import run_decay_sync
        return run_decay_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


@celery_app.task(name="app.tasks.worker.weekly_snapshot_task", bind=True, max_retries=3)
def weekly_snapshot_task(self) -> dict:
    """Capture weekly state snapshots for all children."""
    try:
        from app.tasks.snapshots import run_snapshots_sync
        return run_snapshots_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


# Alias for celery -A app.tasks.worker
app = celery_app
