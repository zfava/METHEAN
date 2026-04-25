# subscription_exempt: users must reach billing endpoints to subscribe or recover
# See fix/methean6-08-subscription-gating for classification rationale.
"""Billing API endpoints: subscribe, cancel, webhook, portal."""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import User
from app.services.billing import (
    cancel_subscription,
    create_checkout_session,
    create_portal_session,
    get_subscription_status,
    handle_webhook,
)

router = APIRouter(prefix="/billing", tags=["billing"])


class CheckoutBody(BaseModel):
    success_url: str | None = None
    cancel_url: str | None = None


class PortalBody(BaseModel):
    return_url: str | None = None


@router.post("/subscribe")
async def subscribe(
    body: CheckoutBody | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Create Stripe checkout session and return URL."""
    url = await create_checkout_session(
        db,
        user.household_id,
        user.email,
        success_url=body.success_url if body else None,
        cancel_url=body.cancel_url if body else None,
    )
    if not url:
        raise HTTPException(status_code=503, detail="Billing not configured")
    await db.commit()
    return {"checkout_url": url}


@router.get("/status")
async def status(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get current subscription status."""
    return await get_subscription_status(db, user.household_id)


@router.post("/cancel")
async def cancel(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Cancel subscription at period end."""
    success = await cancel_subscription(db, user.household_id)
    if success:
        await db.commit()
    return {"canceled": success}


@router.post("/portal")
async def portal(
    body: PortalBody | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get Stripe customer portal URL."""
    url = await create_portal_session(
        db,
        user.household_id,
        return_url=body.return_url if body else None,
    )
    if not url:
        raise HTTPException(status_code=503, detail="Billing not configured or no customer")
    return {"portal_url": url}


@router.post("/webhook")
async def webhook(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    """Process Stripe webhook (no auth — verified by signature)."""
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    try:
        result = await handle_webhook(payload, signature, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return result
