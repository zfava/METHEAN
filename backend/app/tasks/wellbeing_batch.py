"""Nightly wellbeing anomaly detection batch task.

Scans all children with 30+ days of learning activity for
wellbeing anomalies. PARENT-ONLY output.
"""

import asyncio
import logging
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

BATCH_SIZE = 50


def run_wellbeing_sync() -> dict:
    """Synchronous entry point for the Celery task."""
    return asyncio.run(_run_wellbeing_batch())


async def _run_wellbeing_batch() -> dict:
    """Scan all eligible children for wellbeing anomalies."""
    from sqlalchemy import func, select
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from app.core.config import settings
    from app.models.governance import Attempt
    from app.models.identity import Child

    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    start = time.monotonic()
    scanned = 0
    skipped = 0
    errors = 0
    anomaly_counts: dict[str, int] = defaultdict(int)

    async with SessionLocal() as db:
        # Find children with 30+ distinct activity days
        cutoff_days = 30
        eligible_subq = (
            select(
                Attempt.child_id,
                func.count(func.distinct(func.date(Attempt.created_at))).label("days"),
            )
            .where(Attempt.status == "completed")
            .group_by(Attempt.child_id)
            .having(func.count(func.distinct(func.date(Attempt.created_at))) >= cutoff_days)
            .subquery()
        )

        result = await db.execute(
            select(Child.id, Child.household_id).where(
                Child.id.in_(select(eligible_subq.c.child_id))
            )
        )
        eligible = result.all()

        logger.info("Wellbeing batch: %d eligible children", len(eligible))

        # Process in batches
        for i in range(0, len(eligible), BATCH_SIZE):
            batch = eligible[i : i + BATCH_SIZE]
            for child_id, household_id in batch:
                scanned += 1
                try:
                    from app.services.wellbeing_detection import (
                        run_wellbeing_detection,
                        check_for_resolution,
                        notify_parent_of_anomaly,
                    )

                    # Detect new anomalies
                    new_anomalies = await run_wellbeing_detection(db, child_id, household_id)
                    for anomaly in new_anomalies:
                        atype = anomaly.anomaly_type.value if hasattr(anomaly.anomaly_type, "value") else str(anomaly.anomaly_type)
                        anomaly_counts[atype] += 1

                        # Notify parent
                        try:
                            await notify_parent_of_anomaly(db, anomaly)
                        except Exception:
                            logger.warning("Failed to notify for anomaly %s", anomaly.id)

                    # Check for resolved anomalies
                    try:
                        await check_for_resolution(db, child_id, household_id)
                    except Exception:
                        logger.warning("Resolution check failed for child %s", child_id)

                except Exception:
                    errors += 1
                    logger.exception("Wellbeing detection failed for child %s", child_id)

            await db.commit()

    await engine.dispose()

    duration_ms = int((time.monotonic() - start) * 1000)
    total_anomalies = sum(anomaly_counts.values())

    result_info = {
        "children_scanned": scanned,
        "children_skipped_insufficient_data": len(eligible) - scanned + skipped,
        "anomalies_created": total_anomalies,
        "anomaly_counts": dict(anomaly_counts),
        "errors": errors,
        "duration_ms": duration_ms,
    }
    logger.info("Wellbeing batch complete: %s", result_info)
    return result_info
