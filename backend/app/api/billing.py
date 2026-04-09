"""Billing API endpoints: subscribe, cancel, webhook, portal."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import User
from app.services.billing import (
    create_checkout_session,
    create_portal_session,
    cancel_subscription,
    get_subscription_status,
    handle_webhook,
)

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/subscribe")
async def subscribe(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Create Stripe checkout session and return URL."""
    url = await create_checkout_session(db, user.household_id, user.email)
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
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Get Stripe customer portal URL."""
    url = await create_portal_session(db, user.household_id)
    if not url:
        raise HTTPException(status_code=503, detail="Billing not configured or no customer")
    return {"portal_url": url}


@router.post("/webhook")
async def webhook(request: Request) -> dict:
    """Process Stripe webhook (no auth — verified by signature)."""
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    success = await handle_webhook(payload, signature)
    if not success:
        raise HTTPException(status_code=400, detail="Webhook verification failed")
    return {"received": True}
