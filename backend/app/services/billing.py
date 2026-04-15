"""Stripe billing integration.

Graceful degradation: no STRIPE_SECRET_KEY = billing features disabled.
"""

import logging
import uuid
from datetime import UTC, datetime

try:
    import stripe
except ImportError:
    stripe = None  # type: ignore

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.identity import Household

logger = logging.getLogger(__name__)


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

    if hh.stripe_customer_id:
        return hh.stripe_customer_id

    customer = stripe.Customer.create(
        email=email,
        metadata={"household_id": str(household_id)},
    )
    hh.stripe_customer_id = customer.id
    await db.flush()
    return customer.id


async def create_checkout_session(
    db: AsyncSession,
    household_id: uuid.UUID,
    email: str,
    success_url: str | None = None,
    cancel_url: str | None = None,
) -> str | None:
    """Create a Stripe checkout session. Returns session URL."""
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
        subscription_data={"trial_period_days": settings.STRIPE_TRIAL_DAYS},
        success_url=success_url or f"{settings.APP_URL}/billing?success=true",
        cancel_url=cancel_url or f"{settings.APP_URL}/billing?canceled=true",
        metadata={"household_id": str(household_id)},
    )
    return session.url


async def create_portal_session(
    db: AsyncSession,
    household_id: uuid.UUID,
    return_url: str | None = None,
) -> str | None:
    """Create a Stripe customer portal session. Returns portal URL."""
    _init_stripe()
    if not settings.STRIPE_SECRET_KEY:
        return None

    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh or not hh.stripe_customer_id:
        return None

    session = stripe.billing_portal.Session.create(
        customer=hh.stripe_customer_id,
        return_url=return_url or f"{settings.APP_URL}/billing",
    )
    return session.url


async def cancel_subscription(db: AsyncSession, household_id: uuid.UUID) -> bool:
    """Cancel subscription at period end."""
    _init_stripe()
    if not settings.STRIPE_SECRET_KEY:
        return False

    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh or not hh.stripe_customer_id:
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

    return {
        "status": hh.subscription_status or "trial",
        "trial_ends_at": hh.trial_ends_at.isoformat() if hh.trial_ends_at else None,
        "subscription_ends_at": hh.subscription_ends_at.isoformat() if hh.subscription_ends_at else None,
        "stripe_customer_id": hh.stripe_customer_id,
        "stripe_subscription_id": hh.stripe_subscription_id,
        "stripe_configured": bool(settings.STRIPE_SECRET_KEY),
    }


async def handle_webhook(payload: bytes, signature: str, db: AsyncSession) -> dict:
    """Process Stripe webhook events. Returns event type and status."""
    _init_stripe()
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise ValueError("Webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(payload, signature, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise ValueError("Invalid webhook signature")

    if event.type == "checkout.session.completed":
        session = event.data.object
        hid = session.metadata.get("household_id")
        if hid:
            await _update_subscription_status(db, uuid.UUID(hid), "active", session.subscription)
            # Clear trial — they paid
            result = await db.execute(select(Household).where(Household.id == uuid.UUID(hid)))
            hh = result.scalar_one_or_none()
            if hh:
                hh.trial_ends_at = None
                await db.flush()
            logger.info("Subscription activated for household %s", hid)

    elif event.type == "customer.subscription.updated":
        sub = event.data.object
        status_map = {
            "active": "active",
            "past_due": "past_due",
            "canceled": "canceled",
            "trialing": "trialing",
            "unpaid": "past_due",
        }
        mapped = status_map.get(sub.status, sub.status)
        await _sync_by_customer(db, sub.customer, mapped, sub.id, sub)
        logger.info("Subscription updated to %s for customer %s", mapped, sub.customer)

    elif event.type == "customer.subscription.deleted":
        sub = event.data.object
        await _sync_by_customer(db, sub.customer, "canceled", sub.id, sub)
        logger.info("Subscription canceled for customer %s", sub.customer)

    elif event.type == "invoice.payment_failed":
        invoice = event.data.object
        await _sync_by_customer(db, invoice.customer, "past_due", None, None)
        logger.warning("Payment failed for customer %s", invoice.customer)

    else:
        logger.debug("Unhandled webhook event: %s", event.type)

    return {"event_type": event.type, "processed": True}


async def _update_subscription_status(
    db: AsyncSession, household_id: uuid.UUID, status: str, subscription_id: str | None
) -> None:
    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if hh:
        hh.subscription_status = status
        if subscription_id:
            hh.stripe_subscription_id = subscription_id
        await db.flush()


async def _sync_by_customer(
    db: AsyncSession, customer_id: str, status: str, subscription_id: str | None, sub_obj: object | None
) -> None:
    result = await db.execute(select(Household).where(Household.stripe_customer_id == str(customer_id)))
    hh = result.scalar_one_or_none()
    if not hh:
        logger.warning("Webhook: no household found for customer %s", customer_id)
        return

    hh.subscription_status = status
    if subscription_id:
        hh.stripe_subscription_id = subscription_id
    if sub_obj:
        trial_end = getattr(sub_obj, "trial_end", None)
        if trial_end:
            hh.trial_ends_at = datetime.fromtimestamp(trial_end, tz=UTC)
        period_end = getattr(sub_obj, "current_period_end", None)
        if period_end:
            hh.subscription_ends_at = datetime.fromtimestamp(period_end, tz=UTC)
    await db.flush()
