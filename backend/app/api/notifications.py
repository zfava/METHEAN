"""Notification API endpoints."""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import User
from app.services.notifications import get_notifications, mark_all_read, mark_read

router = APIRouter(tags=["notifications"])


@router.get("/notifications")
async def list_notifications(
    unread: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get recent notifications."""
    return await get_notifications(db, user.id, user.household_id, unread_only=unread, limit=limit)


@router.put("/notifications/{notification_id}/read")
async def read_notification(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Mark a notification as read."""
    await mark_read(db, notification_id, user.household_id)
    await db.commit()
    return {"status": "ok"}


@router.put("/notifications/read-all")
async def read_all_notifications(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Mark all notifications as read."""
    count = await mark_all_read(db, user.id, user.household_id)
    await db.commit()
    return {"marked_read": count}


@router.post("/notifications/test-daily-summary")
async def test_daily_summary(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Send a test daily summary email to the current user's household."""
    from app.tasks.daily_summary import send_daily_summary_for_household
    sent = await send_daily_summary_for_household(db, user.household_id, test_mode=True)
    return {"sent": sent, "test_mode": True}
