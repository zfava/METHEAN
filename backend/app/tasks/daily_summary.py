"""Daily morning summary email task."""

import asyncio
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.models.identity import Household, User, Child
from app.models.governance import Activity
from app.models.enums import ActivityStatus
from app.services.email import send_email
from app.services.email_templates import daily_summary_email


async def _send_daily_summaries():
    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as db:
        # Get all households
        households = (await db.execute(select(Household))).scalars().all()

        for hh in households:
            # Get parent users with email_daily_summary enabled
            users = (await db.execute(
                select(User).where(User.household_id == hh.id, User.is_active == True)  # noqa: E712
            )).scalars().all()

            children = (await db.execute(
                select(Child).where(Child.household_id == hh.id)
            )).scalars().all()

            if not users or not children:
                continue

            today = date.today().isoformat()
            children_data = []
            for child in children:
                acts = (await db.execute(
                    select(Activity).where(
                        Activity.household_id == hh.id,
                        Activity.scheduled_date == today,
                    )
                )).scalars().all()
                child_acts = [a for a in acts if getattr(a, "child_id", None) == child.id or True]
                children_data.append({
                    "name": child.first_name,
                    "activity_count": len(child_acts),
                    "total_minutes": sum(a.estimated_minutes or 0 for a in child_acts),
                })

            # Count pending reviews
            pending = (await db.execute(
                select(Activity).where(
                    Activity.household_id == hh.id,
                    Activity.governance_approved == False,  # noqa: E712
                    Activity.status == ActivityStatus.scheduled,
                )
            )).scalars().all()
            pending_count = len(pending)

            date_str = date.today().strftime("%A, %B %d")

            for user in users:
                prefs = user.notification_preferences or {}
                if not prefs.get("email_daily_summary", True):
                    continue
                html = daily_summary_email(user.display_name, children_data, pending_count, date_str)
                await send_email(user.email, f"Today's Plan — {date_str}", html)

    await engine.dispose()


def run_daily_summary_sync() -> dict:
    """Sync wrapper for Celery."""
    asyncio.run(_send_daily_summaries())
    return {"status": "sent"}
