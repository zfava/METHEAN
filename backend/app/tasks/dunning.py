"""Daily dunning advance: walk every in-dunning household forward.

The state machine itself lives in services/billing.py (single writer
for dunning fields); this task is just the clock that calls it once a
day. Reruns are safe: transitions are threshold checks against
dunning_started_at and emails are per-state idempotent behind a 24h
throttle, so running the sweep twice changes nothing.
"""

import asyncio

import structlog

from app.core.database import async_session_factory

logger = structlog.get_logger()


async def advance_all_dunning(session_factory=None) -> dict:
    factory = session_factory or async_session_factory
    async with factory() as db:
        from app.services.billing import advance_dunning

        try:
            counts = await advance_dunning(db)
            await db.commit()
        except Exception as exc:
            await db.rollback()
            logger.error("dunning_advance_failed", error=str(exc))
            raise
    logger.info("dunning_advance_complete", **counts)
    return counts


def run_dunning_sync() -> dict:
    return asyncio.get_event_loop().run_until_complete(advance_all_dunning())
