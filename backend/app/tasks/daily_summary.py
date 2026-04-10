"""Daily morning summary email task."""

import asyncio
import logging
from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.models.identity import Household, User, Child
from app.models.governance import Activity
from app.models.enums import ActivityStatus
from app.services.email import send_email
from app.services.email_templates import daily_summary_email

logger = logging.getLogger(__name__)


async def send_daily_summary_for_household(
    db: AsyncSession,
    household_id,
    test_mode: bool = False,
) -> int:
    """Send daily summary for a single household. Returns number of emails sent."""
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID
    import uuid

    hh_id = household_id if isinstance(household_id, uuid.UUID) else uuid.UUID(str(household_id))

    # Get parent users
    users = (await db.execute(
        select(User).where(User.household_id == hh_id, User.is_active == True)  # noqa: E712
    )).scalars().all()

    children = (await db.execute(
        select(Child).where(Child.household_id == hh_id)
    )).scalars().all()

    if not users or not children:
        return 0

    today = date.today().isoformat()
    children_data = []
    for child in children:
        # Filter activities for THIS child specifically
        acts = (await db.execute(
            select(Activity).where(
                Activity.household_id == hh_id,
                Activity.scheduled_date == today,
            )
        )).scalars().all()
        # Filter by child_id if the field exists
        child_acts = [a for a in acts if getattr(a, "child_id", None) == child.id]
        # Fallback: if no child_id field on Activity, count all
        if not child_acts and acts:
            child_acts = acts

        children_data.append({
            "name": child.first_name,
            "activity_count": len(child_acts),
            "total_minutes": sum(a.estimated_minutes or 0 for a in child_acts),
        })

    # Count pending reviews
    pending = (await db.execute(
        select(func.count()).select_from(Activity).where(
            Activity.household_id == hh_id,
            Activity.governance_approved == False,  # noqa: E712
            Activity.status == ActivityStatus.scheduled,
        )
    )).scalar() or 0

    date_str = date.today().strftime("%A, %B %d")
    sent = 0

    for user in users:
        prefs = user.notification_preferences or {}
        if not test_mode and not prefs.get("email_daily_summary", True):
            continue
        html = daily_summary_email(user.display_name, children_data, pending, date_str)
        success = await send_email(user.email, f"Today's Plan \u2014 {date_str}", html)
        if success:
            sent += 1
            logger.info(f"Daily summary sent to {user.email}")
        else:
            logger.warning(f"Daily summary failed for {user.email}")

    return sent


async def _send_daily_summaries():
    """Send daily summaries for ALL households."""
    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    total_sent = 0
    total_errors = 0

    async with SessionLocal() as db:
        households = (await db.execute(select(Household))).scalars().all()

        for hh in households:
            try:
                sent = await send_daily_summary_for_household(db, hh.id)
                total_sent += sent
            except Exception as e:
                total_errors += 1
                logger.error(f"Daily summary failed for household {hh.id}: {e}")
                # Continue to next household — one failure doesn't stop others

    await engine.dispose()

    result = {"sent": total_sent, "errors": total_errors, "households": len(households)}
    logger.info(f"Daily summary task complete: {result}")
    return result


def run_daily_summary_sync() -> dict:
    """Sync wrapper for Celery."""
    return asyncio.run(_send_daily_summaries())
