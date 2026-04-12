"""Nightly family intelligence batch task.

Runs cross-child pattern detection for all multi-child households.
"""

import asyncio
import logging
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

BATCH_SIZE = 20


def run_family_intelligence_sync() -> dict:
    """Synchronous entry point for the Celery task."""
    return asyncio.run(_run_family_intelligence_batch())


async def _run_family_intelligence_batch() -> dict:
    """Run family intelligence for all eligible households."""
    from sqlalchemy import func, select
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from app.core.config import settings
    from app.models.identity import Child
    from app.models.state import ChildNodeState
    from app.services.family_intelligence import generate_predictive_scaffolding, run_family_intelligence

    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    start = time.monotonic()
    processed = 0
    errors = 0
    total_insights = 0
    pattern_counts: dict[str, int] = defaultdict(int)

    async with SessionLocal() as db:
        # Find households with 2+ children who each have at least 1 ChildNodeState
        children_with_data = (
            select(
                ChildNodeState.child_id,
            )
            .distinct()
            .subquery()
        )

        result = await db.execute(
            select(Child.household_id, func.count(Child.id).label("cnt"))
            .where(Child.id.in_(select(children_with_data.c.child_id)))
            .group_by(Child.household_id)
            .having(func.count(Child.id) >= 2)
        )
        eligible_households = [row[0] for row in result.all()]

        logger.info("Family intelligence batch: %d eligible households", len(eligible_households))

        # Process in batches
        for i in range(0, len(eligible_households), BATCH_SIZE):
            batch = eligible_households[i : i + BATCH_SIZE]
            for household_id in batch:
                processed += 1
                try:
                    result_info = await run_family_intelligence(db, household_id)
                    if not result_info.get("skipped"):
                        created = result_info.get("insights_created", 0)
                        total_insights += created
                        for ptype, count in result_info.get("counts", {}).items():
                            pattern_counts[ptype] += count

                    # Run predictive scaffolding after detection
                    try:
                        scaffolding = await generate_predictive_scaffolding(db, household_id)
                        total_insights += len(scaffolding)
                        if scaffolding:
                            pattern_counts["predictive_scaffolding"] = pattern_counts.get(
                                "predictive_scaffolding", 0
                            ) + len(scaffolding)
                    except Exception:
                        logger.exception("Predictive scaffolding failed for household %s", household_id)

                except Exception:
                    errors += 1
                    logger.exception("Family intelligence failed for household %s", household_id)

            await db.commit()

    await engine.dispose()

    duration_ms = int((time.monotonic() - start) * 1000)
    result_info = {
        "households_processed": processed,
        "insights_created": total_insights,
        "pattern_counts": dict(pattern_counts),
        "errors": errors,
        "duration_ms": duration_ms,
    }
    logger.info("Family intelligence batch complete: %s", result_info)
    return result_info
