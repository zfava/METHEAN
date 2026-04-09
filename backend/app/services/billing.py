"""Stripe billing integration.

Graceful degradation: no STRIPE_SECRET_KEY = billing features disabled.
"""

import uuid
from datetime import datetime, timezone

try:
    import stripe
except ImportError:
    stripe = None  # type: ignore

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.identity import Household


def _init_stripe():
    if stripe and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY


async def create_customer(db: AsyncSession, household_id: uuid.UUID, email: str) -> str | None:
    """Create a Stripe customer for a household."""
    _init_stripe()
    if not settings.STRIPE_SECRET_KEY:
        return None

    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh:
        raise ValueError("Household not found")

    if hasattr(hh, "stripe_customer_id") and hh.stripe_customer_id:
        return hh.stripe_customer_id

    customer = stripe.Customer.create(
        email=email,
        metadata={"household_id": str(household_id)},
    )
    hh.stripe_customer_id = customer.id
    await db.flush()
    return customer.id


async def create_checkout_session(
    db: AsyncSession, household_id: uuid.UUID, email: str,
) -> str | None:
    """Create a Stripe checkout session with 30-day trial. Returns session URL."""
    _init_stripe()
    if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_PRICE_ID:
        return None

    customer_id = await create_customer(db, household_id, email)
    if not customer_id:
        return None

    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        subscription_data={"trial_period_days": 30},
        success_url=f"{settings.APP_URL}/billing?success=true",
        cancel_url=f"{settings.APP_URL}/billing?canceled=true",
    )
    return session.url


async def create_portal_session(
    db: AsyncSession, household_id: uuid.UUID,
) -> str | None:
    """Create a Stripe customer portal session. Returns portal URL."""
    _init_stripe()
    if not settings.STRIPE_SECRET_KEY:
        return None

    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh or not getattr(hh, "stripe_customer_id", None):
        return None

    session = stripe.billing_portal.Session.create(
        customer=hh.stripe_customer_id,
        return_url=f"{settings.APP_URL}/billing",
    )
    return session.url


async def cancel_subscription(db: AsyncSession, household_id: uuid.UUID) -> bool:
    """Cancel subscription at period end."""
    _init_stripe()
    if not settings.STRIPE_SECRET_KEY:
        return False

    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh or not getattr(hh, "stripe_customer_id", None):
        return False

    subscriptions = stripe.Subscription.list(customer=hh.stripe_customer_id, limit=1)
    if subscriptions.data:
        stripe.Subscription.modify(subscriptions.data[0].id, cancel_at_period_end=True)
        return True
    return False


async def get_subscription_status(db: AsyncSession, household_id: uuid.UUID) -> dict:
    """Get current subscription status."""
    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh:
        return {"status": "unknown"}

    status_val = getattr(hh, "subscription_status", "trial") or "trial"
    trial_end = getattr(hh, "trial_ends_at", None)
    sub_end = getattr(hh, "subscription_ends_at", None)

    return {
        "status": status_val,
        "trial_ends_at": trial_end.isoformat() if trial_end else None,
        "subscription_ends_at": sub_end.isoformat() if sub_end else None,
        "stripe_configured": bool(settings.STRIPE_SECRET_KEY),
    }


async def handle_webhook(payload: bytes, signature: str) -> bool:
    """Process Stripe webhook events."""
    _init_stripe()
    if not settings.STRIPE_WEBHOOK_SECRET:
        return False

    try:
        event = stripe.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        return False

    # Import here to avoid circular imports
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    engine = create_async_engine(settings.DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as db:
        if event.type == "customer.subscription.created":
            await _update_subscription(db, event.data.object, "active")
        elif event.type == "customer.subscription.updated":
            sub = event.data.object
            status = "active" if sub.status == "active" else "trialing" if sub.status == "trialing" else sub.status
            await _update_subscription(db, sub, status)
        elif event.type == "customer.subscription.deleted":
            await _update_subscription(db, event.data.object, "canceled")
        elif event.type == "customer.subscription.trial_will_end":
            pass  # Could send warning email
        await db.commit()

    await engine.dispose()
    return True


async def _update_subscription(db: AsyncSession, subscription: object, status: str) -> None:
    """Update household subscription status from Stripe data."""
    customer_id = getattr(subscription, "customer", None)
    if not customer_id:
        return

    result = await db.execute(
        select(Household).where(Household.stripe_customer_id == str(customer_id))
    )
    hh = result.scalar_one_or_none()
    if not hh:
        return

    hh.subscription_status = status
    trial_end = getattr(subscription, "trial_end", None)
    if trial_end:
        hh.trial_ends_at = datetime.fromtimestamp(trial_end, tz=timezone.utc)
    period_end = getattr(subscription, "current_period_end", None)
    if period_end:
        hh.subscription_ends_at = datetime.fromtimestamp(period_end, tz=timezone.utc)
    await db.flush()
