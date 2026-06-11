"""Stripe billing integration.

Graceful degradation: no STRIPE_SECRET_KEY = billing features disabled.

Failed-payment recovery (dunning) lives at the bottom of this module:
Stripe remains the single source of truth for payment facts, and
``Household.dunning_state`` is METHEAN's derived policy walk over them
(none -> grace -> restricted -> canceled). Any successful payment
resets the walk to none regardless of where it was. Every transition
is idempotent: webhooks replay and the daily task reruns.
"""

import logging
import uuid
from datetime import UTC, datetime, timedelta

try:
    import stripe
except ImportError:
    stripe = None  # type: ignore

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.identity import Household, User

logger = logging.getLogger(__name__)
dunning_logger = structlog.get_logger()


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


async def cancel_subscription(db: AsyncSession, household_id: uuid.UUID, at_period_end: bool = True) -> bool:
    """Cancel subscription.

    Default cancels at period end (the normal billing flow). Household
    deletion passes at_period_end=False to cancel immediately: a family
    leaving with their data erased should not stay on an active plan.
    Tolerates missing config: no Stripe key or no customer means False.
    """
    _init_stripe()
    if not settings.STRIPE_SECRET_KEY:
        return False

    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh or not hh.stripe_customer_id:
        return False

    subscriptions = stripe.Subscription.list(customer=hh.stripe_customer_id, limit=1)
    if subscriptions.data:
        if at_period_end:
            stripe.Subscription.modify(subscriptions.data[0].id, cancel_at_period_end=True)
        else:
            stripe.Subscription.cancel(subscriptions.data[0].id)
        return True
    return False


async def get_subscription_status(db: AsyncSession, household_id: uuid.UUID) -> dict:
    """Get current subscription status, including the dunning walk."""
    result = await db.execute(select(Household).where(Household.id == household_id))
    hh = result.scalar_one_or_none()
    if not hh:
        return {"status": "unknown"}

    dunning_state = getattr(hh, "dunning_state", "none") or "none"
    started = getattr(hh, "dunning_started_at", None)
    grace_ends_at = started + timedelta(days=DUNNING_GRACE_DAYS) if started else None
    cancels_at = started + timedelta(days=DUNNING_RESTRICT_DAYS) if started else None

    return {
        "status": hh.subscription_status or "trial",
        "trial_ends_at": hh.trial_ends_at.isoformat() if hh.trial_ends_at else None,
        "subscription_ends_at": hh.subscription_ends_at.isoformat() if hh.subscription_ends_at else None,
        "stripe_customer_id": hh.stripe_customer_id,
        "stripe_subscription_id": hh.stripe_subscription_id,
        "stripe_configured": bool(settings.STRIPE_SECRET_KEY),
        "dunning_state": dunning_state,
        "dunning_started_at": started.isoformat() if started else None,
        "dunning_grace_ends_at": grace_ends_at.isoformat() if grace_ends_at else None,
        "dunning_cancels_at": cancels_at.isoformat() if cancels_at else None,
        "update_payment_url": _dunning_update_url(),
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
                await reset_dunning(db, hh)
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
        if mapped in ("active", "trialing"):
            # Stripe says the subscription is healthy again; whatever
            # dunning thought, the payment facts win.
            hh = await _get_household_by_customer(db, sub.customer)
            if hh:
                await reset_dunning(db, hh)
        logger.info("Subscription updated to %s for customer %s", mapped, sub.customer)

    elif event.type == "customer.subscription.deleted":
        sub = event.data.object
        await _sync_by_customer(db, sub.customer, "canceled", sub.id, sub)
        # If the family was mid-dunning, the subscription is now gone
        # (our own day-21 cancel replaying, a portal cancel, or Stripe
        # giving up): land the walk on canceled without another email.
        hh = await _get_household_by_customer(db, sub.customer)
        if hh and hh.dunning_state in ("grace", "restricted"):
            hh.dunning_state = "canceled"
            await _log_dunning_event(db, hh, "billing_dunning_advanced", "canceled", "subscription deleted at Stripe")
            await db.flush()
        logger.info("Subscription canceled for customer %s", sub.customer)

    elif event.type == "invoice.payment_failed":
        invoice = event.data.object
        await _sync_by_customer(db, invoice.customer, "past_due", None, None)
        hh = await _get_household_by_customer(db, invoice.customer)
        if hh:
            await start_dunning(db, hh)
        logger.warning("Payment failed for customer %s", invoice.customer)

    elif event.type in ("invoice.payment_succeeded", "invoice.paid"):
        invoice = event.data.object
        hh = await _get_household_by_customer(db, invoice.customer)
        if hh:
            await reset_dunning(db, hh)
        logger.info("Payment succeeded for customer %s", invoice.customer)

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


# ══════════════════════════════════════════════════
# Dunning: failed-payment recovery state machine
# ══════════════════════════════════════════════════
#
# none -> grace (payment fails; full access, fix-payment email)
# grace -> restricted (day 7; paid routes paused, data stays reachable)
# restricted -> canceled (day 21; subscription canceled at Stripe)
# anything -> none (any successful payment; silent, the banner
# disappearing is the confirmation)

DUNNING_GRACE_DAYS = 7
DUNNING_RESTRICT_DAYS = 21
DUNNING_EMAIL_THROTTLE_HOURS = 24

# Cumulative emails a household should have received by each state.
# The daily task retries a state's email until the count catches up,
# which makes sends idempotent across reruns and lets the 24h throttle
# defer (never lose) an email.
_DUNNING_EXPECTED_EMAILS = {"grace": 1, "restricted": 2, "canceled": 3}


def _dunning_update_url() -> str:
    """Where every dunning email sends the parent to fix payment.

    The billing page fronts the existing Stripe portal and checkout
    mechanisms (create_portal_session / create_checkout_session);
    portal sessions are short-lived so emails link to the page, not to
    a session URL minted hours earlier.
    """
    return f"{settings.APP_URL}/billing"


async def _get_household_by_customer(db: AsyncSession, customer_id: str) -> Household | None:
    result = await db.execute(select(Household).where(Household.stripe_customer_id == str(customer_id)))
    return result.scalar_one_or_none()


async def _dunning_owner(db: AsyncSession, household: Household) -> User | None:
    """The household owner receives dunning email."""
    from app.models.enums import UserRole

    result = await db.execute(
        select(User).where(User.household_id == household.id, User.role == UserRole.owner).limit(1)
    )
    return result.scalar_one_or_none()


async def _log_dunning_event(
    db: AsyncSession, household: Household, target_type: str, to_state: str, reason: str
) -> None:
    """Hash-chained governance event for a dunning transition."""
    from app.models.enums import GovernanceAction
    from app.services.governance import log_governance_event

    await log_governance_event(
        db,
        household.id,
        None,
        GovernanceAction.modify,
        target_type,
        household.id,
        reason=reason,
        metadata={
            "dunning_state": to_state,
            "dunning_started_at": (household.dunning_started_at.isoformat() if household.dunning_started_at else None),
        },
    )


async def _send_dunning_email(db: AsyncSession, household: Household, now: datetime) -> bool:
    """Send the email the household's current dunning state calls for.

    Idempotent and throttled: nothing is sent if the state's email was
    already sent (dunning_emails_sent has caught up) or if any dunning
    email went out within the last 24 hours. A throttled email is not
    lost; the next daily run sends it once the window clears.
    """
    expected = _DUNNING_EXPECTED_EMAILS.get(household.dunning_state, 0)
    if household.dunning_emails_sent >= expected:
        return False
    if household.last_dunning_email_at is not None:
        if now - household.last_dunning_email_at < timedelta(hours=DUNNING_EMAIL_THROTTLE_HOURS):
            return False

    owner = await _dunning_owner(db, household)
    if owner is None:
        dunning_logger.warning("dunning_email_no_owner", household_id=str(household.id))
        return False

    from app.services.email import send_email
    from app.services.email_templates import (
        final_notice_email,
        payment_failed_email,
        restriction_warning_email,
    )

    update_url = _dunning_update_url()
    started = household.dunning_started_at or now
    if household.dunning_state == "grace":
        grace_until = (started + timedelta(days=DUNNING_GRACE_DAYS)).strftime("%B %d, %Y")
        subject = "A payment didn't go through"
        html = payment_failed_email(owner.display_name, update_url, grace_until)
    elif household.dunning_state == "restricted":
        cancel_on = (started + timedelta(days=DUNNING_RESTRICT_DAYS)).strftime("%B %d, %Y")
        subject = "Your METHEAN subscription is paused"
        html = restriction_warning_email(owner.display_name, update_url, cancel_on)
    elif household.dunning_state == "canceled":
        subject = "Your METHEAN subscription was canceled"
        html = final_notice_email(owner.display_name, update_url)
    else:
        return False

    try:
        await send_email(owner.email, subject, html)
    except Exception as exc:
        dunning_logger.warning("dunning_email_send_failed", household_id=str(household.id), error=str(exc))
        return False

    household.last_dunning_email_at = now
    # Snap to the state's watermark rather than incrementing: if a
    # household skipped a state inside one sweep (e.g. straight to
    # canceled), only the current state's email goes out, once.
    household.dunning_emails_sent = expected
    await db.flush()
    dunning_logger.info(
        "dunning_email_sent",
        household_id=str(household.id),
        dunning_state=household.dunning_state,
        emails_sent=household.dunning_emails_sent,
    )
    return True


async def start_dunning(db: AsyncSession, household: Household, now: datetime | None = None) -> bool:
    """Enter grace on the first payment failure.

    Idempotent: a replayed invoice.payment_failed webhook (or repeated
    failures inside one dunning episode) is a no-op because the walk
    has already left ``none``.
    """
    if household.dunning_state != "none":
        return False
    current = now or datetime.now(UTC)
    household.dunning_state = "grace"
    household.dunning_started_at = current
    await _log_dunning_event(db, household, "billing_dunning_started", "grace", "Payment failed; grace period started")
    await _send_dunning_email(db, household, current)
    await db.flush()
    dunning_logger.info("dunning_started", household_id=str(household.id))
    return True


async def reset_dunning(db: AsyncSession, household: Household) -> bool:
    """Any successful payment resets the walk, wherever it was.

    No email on recovery: the banner disappearing is the confirmation.
    """
    if household.dunning_state == "none":
        return False
    household.dunning_state = "none"
    household.dunning_started_at = None
    household.last_dunning_email_at = None
    household.dunning_emails_sent = 0
    await _log_dunning_event(db, household, "billing_dunning_recovered", "none", "Payment recovered; dunning cleared")
    await db.flush()
    dunning_logger.info("dunning_recovered", household_id=str(household.id))
    return True


async def advance_dunning_for_household(db: AsyncSession, household: Household, now: datetime | None = None) -> str:
    """One daily-task step for one household. Returns the resulting state.

    Transitions apply on schedule regardless of the email throttle
    (access policy is never delayed by email pacing); the state's email
    follows as soon as the throttle allows. Safe to run twice: a
    household already past a threshold simply stays where it is.
    """
    current = now or datetime.now(UTC)
    if household.dunning_state not in ("grace", "restricted") or household.dunning_started_at is None:
        return household.dunning_state

    elapsed = current - household.dunning_started_at

    if household.dunning_state == "grace" and elapsed >= timedelta(days=DUNNING_GRACE_DAYS):
        household.dunning_state = "restricted"
        await _log_dunning_event(
            db,
            household,
            "billing_dunning_advanced",
            "restricted",
            f"No successful payment after {DUNNING_GRACE_DAYS} days; paid features paused",
        )
        dunning_logger.info("dunning_restricted", household_id=str(household.id))

    if household.dunning_state == "restricted" and elapsed >= timedelta(days=DUNNING_RESTRICT_DAYS):
        try:
            await cancel_subscription(db, household.id, at_period_end=False)
        except Exception as exc:
            dunning_logger.warning("dunning_stripe_cancel_failed", household_id=str(household.id), error=str(exc))
        household.dunning_state = "canceled"
        household.subscription_status = "canceled"
        await _log_dunning_event(
            db,
            household,
            "billing_dunning_advanced",
            "canceled",
            f"No successful payment after {DUNNING_RESTRICT_DAYS} days; subscription canceled",
        )
        dunning_logger.info("dunning_canceled", household_id=str(household.id))

    await _send_dunning_email(db, household, current)
    await db.flush()
    return household.dunning_state


async def advance_dunning(db: AsyncSession, now: datetime | None = None) -> dict:
    """Daily sweep: advance every household currently in the walk."""
    current = now or datetime.now(UTC)
    result = await db.execute(select(Household).where(Household.dunning_state.in_(("grace", "restricted"))))
    households = result.scalars().all()
    counts = {"checked": len(households), "grace": 0, "restricted": 0, "canceled": 0}
    for hh in households:
        state = await advance_dunning_for_household(db, hh, current)
        if state in counts:
            counts[state] += 1
    return counts
