"""Daily alert checking task."""

import asyncio

from sqlalchemy import select

from app.core.database import async_session_factory
from app.models.identity import Household
from app.services.notifications import check_and_send_alerts


async def _run_check_alerts() -> dict:
    async with async_session_factory() as db:
        result = await db.execute(select(Household))
        households = result.scalars().all()
        total_alerts = 0
        for hh in households:
            alerts = await check_and_send_alerts(db, hh.id)
            total_alerts += len(alerts)
        await db.commit()
        return {"households_checked": len(households), "alerts_sent": total_alerts}


def run_check_alerts_sync() -> dict:
    return asyncio.get_event_loop().run_until_complete(_run_check_alerts())
