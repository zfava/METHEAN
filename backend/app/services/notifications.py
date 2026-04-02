"""Notification Rules Engine (Section 9).

Event-driven notifications with dedup windows and quiet hours.
Quiet hours are evaluated in the household's local timezone.
"""

import uuid
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operational import NotificationLog

# Dedup windows per event type (in seconds)
DEDUP_WINDOWS = {
    "plan_ready": 3600,        # 1h
    "review_needed": 14400,    # 4h
    "node_mastered": 0,        # none
    "node_decayed": 86400,     # 24h
    "alert_triggered": 86400,  # 24h
    "attempt_evaluated": 3600, # 1h
    "advisor_report_ready": 0, # none
    "plan_reminder": 86400,    # 24h
    "review_overdue": 86400,   # 24h
}

# Quiet hours: no notifications between these hours (household timezone)
DEFAULT_QUIET_START = 21  # 9 PM
DEFAULT_QUIET_END = 7     # 7 AM


def _is_quiet_hours(
    now_hour: int,
    quiet_start: int = DEFAULT_QUIET_START,
    quiet_end: int = DEFAULT_QUIET_END,
) -> bool:
    """Check if current hour is within quiet hours."""
    if quiet_start > quiet_end:
        return now_hour >= quiet_start or now_hour < quiet_end
    return quiet_start <= now_hour < quiet_end


async def should_send(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID,
    event_type: str,
    dedup_key: str | None = None,
    timezone: str = "UTC",
) -> bool:
    """Check dedup window and quiet hours before sending.

    Quiet hours are evaluated in the household's local timezone,
    not UTC.
    """
    window = DEDUP_WINDOWS.get(event_type, 0)

    if window > 0 and dedup_key:
        cutoff = datetime.now(UTC) - timedelta(seconds=window)
        result = await db.execute(
            select(NotificationLog.id).where(
                NotificationLog.household_id == household_id,
                NotificationLog.user_id == user_id,
                NotificationLog.title.contains(dedup_key),
                NotificationLog.created_at > cutoff,
            ).limit(1)
        )
        if result.scalar_one_or_none():
            return False

    # Check quiet hours in household timezone (skip for critical alerts)
    if event_type != "alert_triggered":
        try:
            tz = ZoneInfo(timezone)
        except (KeyError, ValueError):
            tz = ZoneInfo("UTC")
        local_now = datetime.now(UTC).astimezone(tz)
        if _is_quiet_hours(local_now.hour):
            return False

    return True


async def send_notification(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID,
    event_type: str,
    title: str,
    body: str,
    channel: str = "in_app",
    timezone: str = "UTC",
) -> NotificationLog | None:
    """Send a notification if dedup and quiet hours allow.

    Args:
        timezone: The household's IANA timezone string (e.g. "America/Denver").
            Quiet hours are checked in this timezone.
    """
    if not await should_send(
        db, household_id, user_id, event_type,
        dedup_key=title, timezone=timezone,
    ):
        return None

    log = NotificationLog(
        household_id=household_id,
        user_id=user_id,
        channel=channel,
        title=title,
        body=body,
        sent=True,
        sent_at=datetime.now(UTC),
    )
    db.add(log)
    await db.flush()
    return log


async def get_unread_notifications(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID,
    limit: int = 20,
) -> list[NotificationLog]:
    """Get recent notifications for a user."""
    result = await db.execute(
        select(NotificationLog).where(
            NotificationLog.household_id == household_id,
            NotificationLog.user_id == user_id,
        ).order_by(NotificationLog.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())
