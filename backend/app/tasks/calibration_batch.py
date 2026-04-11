"""Nightly calibration batch task.

Recomputes CalibrationProfiles for children with 50+ reconciled
predictions whose profile is stale (last_computed_at > 24h or NULL).
"""

import asyncio
import logging
import time
import uuid
from datetime import UTC, datetime, timedelta

logger = logging.getLogger(__name__)

BATCH_SIZE = 50


def run_calibration_sync() -> dict:
    """Synchronous entry point for the Celery task."""
    return asyncio.run(_run_calibration_batch())


async def _run_calibration_batch() -> dict:
    """Recompute calibration profiles for eligible children."""
    from sqlalchemy import func, select
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from app.core.config import settings
    from app.models.calibration import CalibrationProfile, EvaluatorPrediction
    from app.models.identity import Child
    from app.services.calibration import MIN_PREDICTIONS_FOR_CALIBRATION, recompute_profile

    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    start = time.monotonic()
    processed = 0
    updated = 0
    errors = 0

    async with SessionLocal() as db:
        # Find children with 50+ reconciled predictions
        eligible_subq = (
            select(
                EvaluatorPrediction.child_id,
                func.count().label("cnt"),
            )
            .where(EvaluatorPrediction.actual_outcome.isnot(None))
            .group_by(EvaluatorPrediction.child_id)
            .having(func.count() >= MIN_PREDICTIONS_FOR_CALIBRATION)
            .subquery()
        )

        # Filter to those whose profile is stale or missing
        cutoff = datetime.now(UTC) - timedelta(hours=24)

        # Get children who have enough data
        result = await db.execute(
            select(eligible_subq.c.child_id)
        )
        eligible_child_ids = [row[0] for row in result.all()]

        # Filter out those with fresh profiles
        stale_ids = []
        for child_id in eligible_child_ids:
            profile_result = await db.execute(
                select(CalibrationProfile).where(CalibrationProfile.child_id == child_id)
            )
            profile = profile_result.scalar_one_or_none()
            if profile is None or profile.last_computed_at is None or profile.last_computed_at < cutoff:
                stale_ids.append(child_id)

        logger.info(
            "Calibration batch: %d eligible children, %d stale",
            len(eligible_child_ids), len(stale_ids),
        )

        # Process in batches
        for i in range(0, len(stale_ids), BATCH_SIZE):
            batch = stale_ids[i : i + BATCH_SIZE]
            for child_id in batch:
                processed += 1
                try:
                    # Get household_id for this child
                    child_result = await db.execute(
                        select(Child.household_id).where(Child.id == child_id)
                    )
                    row = child_result.one_or_none()
                    if row is None:
                        continue

                    household_id = row[0]
                    await recompute_profile(db, child_id, household_id)
                    updated += 1
                except Exception:
                    errors += 1
                    logger.exception("Calibration recompute failed for child %s", child_id)

            await db.commit()

    await engine.dispose()

    duration_ms = int((time.monotonic() - start) * 1000)
    result_info = {
        "children_processed": processed,
        "profiles_updated": updated,
        "errors": errors,
        "duration_ms": duration_ms,
    }
    logger.info("Calibration batch complete: %s", result_info)
    return result_info
