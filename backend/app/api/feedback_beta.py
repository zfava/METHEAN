# subscription_exempt: beta feedback signal channel must remain open
# See fix/methean6-08-subscription-gating for classification rationale.
"""Beta feedback API — parent-submitted feedback about METHEAN itself."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.enums import BetaFeedbackStatus, BetaFeedbackType
from app.models.evidence import BetaFeedback
from app.models.identity import User

router = APIRouter(prefix="/feedback", tags=["beta-feedback"])


class BetaFeedbackCreate(BaseModel):
    feedback_type: BetaFeedbackType = BetaFeedbackType.general
    page_context: str | None = Field(None, max_length=255)
    rating: int | None = Field(None, ge=1, le=5)
    message: str = Field(..., min_length=1)
    screenshot_url: str | None = None


def _feedback_dict(f: BetaFeedback) -> dict:
    return {
        "id": str(f.id),
        "feedback_type": f.feedback_type,
        "page_context": f.page_context,
        "rating": f.rating,
        "message": f.message,
        "screenshot_url": f.screenshot_url,
        "status": f.status,
        "admin_notes": f.admin_notes,
        "created_at": f.created_at.isoformat() if f.created_at else None,
        "updated_at": f.updated_at.isoformat() if f.updated_at else None,
    }


@router.post("", status_code=201)
async def submit_feedback(
    body: BetaFeedbackCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Submit beta feedback from the parent dashboard."""
    fb = BetaFeedback(
        household_id=user.household_id,
        user_id=user.id,
        feedback_type=body.feedback_type.value,
        page_context=body.page_context,
        rating=body.rating,
        message=body.message,
        screenshot_url=body.screenshot_url,
        status=BetaFeedbackStatus.new.value,
    )
    db.add(fb)
    await db.commit()
    await db.refresh(fb)
    return _feedback_dict(fb)


@router.get("")
async def list_feedback(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List the current user's own feedback submissions, newest first."""
    result = await db.execute(
        select(BetaFeedback)
        .where(BetaFeedback.user_id == user.id)
        .order_by(BetaFeedback.created_at.desc())
        .limit(limit)
    )
    return [_feedback_dict(f) for f in result.scalars().all()]


@router.get("/{feedback_id}")
async def get_feedback(
    feedback_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Detail for a single feedback submission owned by the current user."""
    result = await db.execute(
        select(BetaFeedback).where(
            BetaFeedback.id == feedback_id,
            BetaFeedback.user_id == user.id,
        )
    )
    fb = result.scalar_one_or_none()
    if not fb:
        raise HTTPException(404, "Feedback not found")
    return _feedback_dict(fb)
