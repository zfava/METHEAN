"""Nightly style vector computation batch task.

Recomputes LearnerStyleVectors for all children with 20+ observations
in their LearnerIntelligence profile.
"""

import asyncio
import logging
import time

logger = logging.getLogger(__name__)

BATCH_SIZE = 50


def run_style_vector_sync() -> dict:
    """Synchronous entry point for the Celery task."""
    return asyncio.run(_run_style_vector_batch())


async def _run_style_vector_batch() -> dict:
    """Recompute style vectors for eligible children."""
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from app.core.config import settings
    from app.core.database import set_tenant
    from app.models.intelligence import LearnerIntelligence
    from app.services.style_engine import MIN_OBSERVATIONS, compute_style_vector

    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    start = time.monotonic()
    processed = 0
    updated = 0
    errors = 0
    total_dimensions = 0

    async with SessionLocal() as db:
        # Find children with 20+ observations
        result = await db.execute(
            select(LearnerIntelligence.child_id, LearnerIntelligence.household_id).where(
                LearnerIntelligence.observation_count >= MIN_OBSERVATIONS
            )
        )
        eligible = result.all()

        logger.info("Style vector batch: %d eligible children", len(eligible))

        # Process in batches
        for i in range(0, len(eligible), BATCH_SIZE):
            batch = eligible[i : i + BATCH_SIZE]
            for child_id, household_id in batch:
                processed += 1
                try:
                    await set_tenant(db, household_id)
                    vector = await compute_style_vector(db, child_id, household_id)
                    total_dimensions += vector.dimensions_active
                    updated += 1
                except Exception:
                    errors += 1
                    logger.exception("Style vector compute failed for child %s", child_id)

            await db.commit()

    await engine.dispose()

    duration_ms = int((time.monotonic() - start) * 1000)
    avg_dims = round(total_dimensions / max(updated, 1), 1)

    result_info = {
        "children_processed": processed,
        "vectors_updated": updated,
        "errors": errors,
        "avg_dimensions_active": avg_dims,
        "duration_ms": duration_ms,
    }
    logger.info("Style vector batch complete: %s", result_info)
    return result_info
