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
    "daily-summary-email": {
        "task": "app.tasks.worker.daily_summary_task",
        "schedule": crontab(hour=7, minute=15),
    },
    "weekly-digest-email": {
        "task": "app.tasks.worker.weekly_digest_task",
        "schedule": crontab(day_of_week="sunday", hour=18, minute=0),
    },
    "nightly-calibration": {
        "task": "app.tasks.worker.calibration_nightly_task",
        "schedule": crontab(hour=3, minute=30),
    },
    "style-vector-nightly": {
        "task": "app.tasks.worker.style_vector_nightly_task",
        "schedule": crontab(hour=4, minute=0),
    },
    "family-intelligence-nightly": {
        "task": "app.tasks.worker.family_intelligence_nightly_task",
        "schedule": crontab(hour=4, minute=30),
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


@celery_app.task(name="app.tasks.worker.daily_summary_task", bind=True, max_retries=2)
def daily_summary_task(self) -> dict:
    """Send daily morning summary emails."""
    try:
        from app.tasks.daily_summary import run_daily_summary_sync
        return run_daily_summary_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=120)


@celery_app.task(name="app.tasks.worker.weekly_digest_task", bind=True, max_retries=3)
def weekly_digest_task(self) -> dict:
    """Send weekly digest emails."""
    try:
        from app.tasks.weekly_digest import run_weekly_digest_sync
        return run_weekly_digest_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


@celery_app.task(name="app.tasks.worker.enrich_map_task", bind=True, max_retries=2)
def enrich_map_task(self, learning_map_id: str, household_id: str) -> dict:
    """Background task: enrich all nodes in a learning map."""
    try:
        from app.tasks.enrichment import enrich_learning_map_sync
        return enrich_learning_map_sync(learning_map_id, household_id)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@celery_app.task(name="app.tasks.worker.calibration_nightly_task", bind=True, max_retries=3)
def calibration_nightly_task(self) -> dict:
    """Nightly: recompute calibration profiles for eligible children."""
    try:
        from app.tasks.calibration_batch import run_calibration_sync
        return run_calibration_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


@celery_app.task(name="app.tasks.worker.style_vector_nightly_task", bind=True, max_retries=3)
def style_vector_nightly_task(self) -> dict:
    """Nightly: recompute style vectors for eligible children."""
    try:
        from app.tasks.style_vector_batch import run_style_vector_sync
        return run_style_vector_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


@celery_app.task(name="app.tasks.worker.family_intelligence_nightly_task", bind=True, max_retries=3)
def family_intelligence_nightly_task(self) -> dict:
    """Nightly: run cross-child pattern detection for multi-child households."""
    try:
        from app.tasks.family_intelligence_batch import run_family_intelligence_sync
        return run_family_intelligence_sync()
    except Exception as exc:
        self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


# Alias for celery -A app.tasks.worker
app = celery_app
