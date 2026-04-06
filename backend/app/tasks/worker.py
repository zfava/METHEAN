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
    "weekly-fsrs-optimize": {
        "task": "app.tasks.worker.fsrs_optimize_task",
        "schedule": crontab(day_of_week="sunday", hour=2, minute=0),
    },
    "daily-temporal-triggers": {
        "task": "app.tasks.worker.temporal_triggers_task",
        "schedule": crontab(hour=3, minute=0),
    },
    "weekly-curriculum-eval": {
        "task": "app.tasks.worker.curriculum_eval_task",
        "schedule": crontab(day_of_week="monday", hour=5, minute=0),
    },
    "daily-check-alerts": {
        "task": "app.tasks.worker.check_alerts_task",
        "schedule": crontab(hour=7, minute=0),
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


@celery_app.task(name="app.tasks.worker.fsrs_optimize_task", bind=True, max_retries=3)
def fsrs_optimize_task(self) -> dict:
    """Run FSRS per-child weight optimization."""
    try:
        from app.tasks.optimizer import run_optimizer_sync
        return run_optimizer_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


@celery_app.task(name="app.tasks.worker.temporal_triggers_task", bind=True, max_retries=3)
def temporal_triggers_task(self) -> dict:
    """Evaluate temporal governance triggers daily."""
    try:
        from app.tasks.temporal_rules import run_temporal_sync
        return run_temporal_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


@celery_app.task(name="app.tasks.worker.check_alerts_task", bind=True, max_retries=3)
def check_alerts_task(self) -> dict:
    """Daily: check alert conditions for all households."""
    try:
        from app.tasks.check_alerts import run_check_alerts_sync
        return run_check_alerts_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


@celery_app.task(name="app.tasks.worker.curriculum_eval_task", bind=True, max_retries=3)
def curriculum_eval_task(self) -> dict:
    """Weekly: evaluate governance on approaching curriculum weeks."""
    try:
        from app.tasks.curriculum_eval import run_curriculum_eval_sync
        return run_curriculum_eval_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


# Alias for celery -A app.tasks.worker
app = celery_app
