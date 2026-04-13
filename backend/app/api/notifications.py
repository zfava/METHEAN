"""Notification API endpoints."""

import uuid

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import User
from app.models.operational import DeviceToken
from app.services.notifications import get_notifications, mark_all_read, mark_read

router = APIRouter(tags=["notifications"])


# ── Device Token Registration ──


class RegisterDeviceBody(BaseModel):
    token: str
    platform: str  # "ios" | "android" | "web"


@router.post("/notifications/devices", status_code=201)
async def register_device(
    body: RegisterDeviceBody,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Register a push notification token. Upserts by token value."""
    result = await db.execute(
        select(DeviceToken).where(DeviceToken.token == body.token)
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.is_active = True
        existing.user_id = user.id
        existing.household_id = user.household_id
        existing.device_type = body.platform
    else:
        db.add(DeviceToken(
            user_id=user.id,
            household_id=user.household_id,
            device_type=body.platform,
            token=body.token,
            is_active=True,
        ))
    await db.commit()
    return {"status": "registered"}


@router.delete("/notifications/devices/{token}")
async def unregister_device(
    token: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Unregister a push token (e.g., on logout)."""
    await db.execute(
        delete(DeviceToken).where(
            DeviceToken.token == token,
            DeviceToken.user_id == user.id,
        )
    )
    await db.commit()
    return {"status": "unregistered"}


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
