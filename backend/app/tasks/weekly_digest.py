"""Weekly digest email task."""

import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.database import set_tenant
from app.models.enums import GovernanceAction
from app.models.governance import GovernanceEvent
from app.models.identity import Household, User
from app.services.email import send_email
from app.services.email_templates import weekly_digest_email


async def _send_weekly_digests():
    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as db:
        households = (await db.execute(select(Household))).scalars().all()
        week_ago = datetime.now(UTC) - timedelta(days=7)

        for hh in households:
            await set_tenant(db, hh.id)
            users = (
                (
                    await db.execute(
                        select(User).where(User.household_id == hh.id, User.is_active == True)  # noqa: E712
                    )
                )
                .scalars()
                .all()
            )
            if not users:
                continue

            # Governance events this week
            events = (
                (
                    await db.execute(
                        select(GovernanceEvent).where(
                            GovernanceEvent.household_id == hh.id,
                            GovernanceEvent.created_at >= week_ago,
                        )
                    )
                )
                .scalars()
                .all()
            )

            approved = sum(1 for e in events if e.action == GovernanceAction.approve)
            rejected = sum(1 for e in events if e.action == GovernanceAction.reject)

            week_stats = {
                "activities_completed": len(events),
                "nodes_mastered": 0,
                "total_minutes": 0,
            }
            governance_summary = {"approved": approved, "rejected": rejected}

            for user in users:
                prefs = user.notification_preferences or {}
                if not prefs.get("email_weekly_digest", True):
                    continue
                html = weekly_digest_email(user.display_name, week_stats, governance_summary)
                await send_email(user.email, "Your weekly learning digest", html)

    await engine.dispose()


def run_weekly_digest_sync() -> dict:
    """Sync wrapper for Celery."""
    asyncio.run(_send_weekly_digests())
    return {"status": "sent"}
