"""Tests for Stripe billing integration."""

import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Household


@pytest_asyncio.fixture
async def billing_household(db_session: AsyncSession) -> Household:
    h = Household(name="Billing Test Family")
    h.subscription_status = "trial"
    h.trial_ends_at = datetime.now(UTC) + timedelta(days=30)
    db_session.add(h)
    await db_session.flush()
    return h


@pytest.mark.asyncio
async def test_get_subscription_status_trial(db_session, billing_household):
    """Trial household returns trial status."""
    from app.services.billing import get_subscription_status

    status = await get_subscription_status(db_session, billing_household.id)
    assert status["status"] == "trial"
    assert status["trial_ends_at"] is not None


@pytest.mark.asyncio
async def test_get_subscription_status_active(db_session, billing_household):
    """Active subscription returns active status."""
    billing_household.subscription_status = "active"
    billing_household.subscription_ends_at = datetime.now(UTC) + timedelta(days=30)
    await db_session.flush()

    from app.services.billing import get_subscription_status

    status = await get_subscription_status(db_session, billing_household.id)
    assert status["status"] == "active"
    assert status["subscription_ends_at"] is not None


@pytest.mark.asyncio
async def test_get_subscription_status_unknown_household(db_session):
    """Unknown household returns unknown status."""
    from app.services.billing import get_subscription_status

    status = await get_subscription_status(db_session, uuid.uuid4())
    assert status["status"] == "unknown"


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_create_customer_no_stripe_key(mock_settings, db_session, billing_household):
    """No Stripe key returns None gracefully."""
    mock_settings.STRIPE_SECRET_KEY = ""
    from app.services.billing import create_customer

    result = await create_customer(db_session, billing_household.id, "test@test.com")
    assert result is None


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_create_checkout_no_stripe_key(mock_settings, db_session, billing_household):
    """No Stripe key returns None for checkout."""
    mock_settings.STRIPE_SECRET_KEY = ""
    mock_settings.STRIPE_PRICE_ID = ""
    from app.services.billing import create_checkout_session

    result = await create_checkout_session(db_session, billing_household.id, "test@test.com")
    assert result is None


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_cancel_no_stripe_key(mock_settings, db_session, billing_household):
    """No Stripe key returns False for cancel."""
    mock_settings.STRIPE_SECRET_KEY = ""
    from app.services.billing import cancel_subscription

    result = await cancel_subscription(db_session, billing_household.id)
    assert result is False


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_handle_webhook_no_secret(mock_settings):
    """No webhook secret raises ValueError."""
    mock_settings.STRIPE_WEBHOOK_SECRET = ""
    from app.services.billing import handle_webhook

    with pytest.raises(ValueError, match="not configured"):
        await handle_webhook(b"payload", "sig", None)


@pytest.mark.asyncio
async def test_billing_status_api_requires_auth(client):
    """GET /billing/status requires authentication."""
    resp = await client.get("/api/v1/billing/status")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_billing_subscribe_api_requires_auth(client):
    """POST /billing/subscribe requires authentication."""
    resp = await client.post("/api/v1/billing/subscribe")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_billing_cancel_api_requires_auth(client):
    """POST /billing/cancel requires authentication."""
    resp = await client.post("/api/v1/billing/cancel")
    assert resp.status_code == 401


# ═══════════════════════════════════════════
# Webhook Event Processing Tests
# ═══════════════════════════════════════════


@pytest.mark.asyncio
async def test_webhook_rejects_no_signature(client):
    """POST /billing/webhook without stripe-signature returns 400."""
    resp = await client.post("/api/v1/billing/webhook", content=b"{}")
    assert resp.status_code in (400, 403)


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_handle_webhook_unknown_event_returns_processed(mock_settings, db_session, billing_household):
    """Unhandled event type returns processed=True without error."""
    from unittest.mock import MagicMock

    mock_settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    mock_settings.STRIPE_SECRET_KEY = "sk_test"

    from app.services.billing import handle_webhook

    # Mock the stripe.Webhook.construct_event
    with patch("app.services.billing.stripe") as mock_stripe:
        mock_event = MagicMock()
        mock_event.type = "some.unknown.event"
        mock_event.data.object = MagicMock()
        mock_stripe.Webhook.construct_event.return_value = mock_event

        result = await handle_webhook(b"payload", "sig", db_session)
        assert result["event_type"] == "some.unknown.event"
        assert result["processed"] is True


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_checkout_completed_activates_subscription(mock_settings, db_session, billing_household):
    """checkout.session.completed sets status to active and clears trial."""
    from unittest.mock import MagicMock

    mock_settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    mock_settings.STRIPE_SECRET_KEY = "sk_test"

    from app.services.billing import handle_webhook

    with patch("app.services.billing.stripe") as mock_stripe:
        mock_event = MagicMock()
        mock_event.type = "checkout.session.completed"
        mock_event.data.object.metadata = {"household_id": str(billing_household.id)}
        mock_event.data.object.subscription = "sub_test123"
        mock_event.data.object.customer = "cus_test"
        mock_stripe.Webhook.construct_event.return_value = mock_event

        result = await handle_webhook(b"payload", "sig", db_session)
        assert result["event_type"] == "checkout.session.completed"

        await db_session.refresh(billing_household)
        assert billing_household.subscription_status == "active"
        assert billing_household.stripe_subscription_id == "sub_test123"
        assert billing_household.trial_ends_at is None


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_subscription_deleted_cancels(mock_settings, db_session, billing_household):
    """customer.subscription.deleted sets status to canceled."""
    from unittest.mock import MagicMock

    mock_settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    mock_settings.STRIPE_SECRET_KEY = "sk_test"
    billing_household.stripe_customer_id = "cus_cancel_test"
    billing_household.subscription_status = "active"
    await db_session.flush()

    from app.services.billing import handle_webhook

    with patch("app.services.billing.stripe") as mock_stripe:
        mock_sub = MagicMock()
        mock_sub.customer = "cus_cancel_test"
        mock_sub.id = "sub_del"
        mock_sub.status = "canceled"
        mock_sub.trial_end = None
        mock_sub.current_period_end = None

        mock_event = MagicMock()
        mock_event.type = "customer.subscription.deleted"
        mock_event.data.object = mock_sub
        mock_stripe.Webhook.construct_event.return_value = mock_event

        await handle_webhook(b"payload", "sig", db_session)
        await db_session.refresh(billing_household)
        assert billing_household.subscription_status == "canceled"


@pytest.mark.asyncio
@patch("app.services.billing.settings")
async def test_payment_failed_sets_past_due(mock_settings, db_session, billing_household):
    """invoice.payment_failed sets status to past_due."""
    from unittest.mock import MagicMock

    mock_settings.STRIPE_WEBHOOK_SECRET = "whsec_test"
    mock_settings.STRIPE_SECRET_KEY = "sk_test"
    billing_household.stripe_customer_id = "cus_fail_test"
    billing_household.subscription_status = "active"
    await db_session.flush()

    from app.services.billing import handle_webhook

    with patch("app.services.billing.stripe") as mock_stripe:
        mock_invoice = MagicMock()
        mock_invoice.customer = "cus_fail_test"

        mock_event = MagicMock()
        mock_event.type = "invoice.payment_failed"
        mock_event.data.object = mock_invoice
        mock_stripe.Webhook.construct_event.return_value = mock_event

        await handle_webhook(b"payload", "sig", db_session)
        await db_session.refresh(billing_household)
        assert billing_household.subscription_status == "past_due"


# ═══════════════════════════════════════════
# Subscription Gate Tests
# ═══════════════════════════════════════════


@pytest.mark.asyncio
async def test_gate_allows_active_subscription(db_session, household, user):
    """Active subscription passes the gate."""
    household.subscription_status = "active"
    await db_session.flush()

    from app.api.deps import require_active_subscription

    # Should not raise
    result = await require_active_subscription(user=user, db=db_session)
    assert result.id == user.id


@pytest.mark.asyncio
async def test_gate_allows_trial(db_session, household, user):
    """Trial within period passes the gate."""
    household.subscription_status = "trialing"
    await db_session.flush()

    from app.api.deps import require_active_subscription

    result = await require_active_subscription(user=user, db=db_session)
    assert result.id == user.id


@pytest.mark.asyncio
async def test_gate_blocks_canceled(db_session, household, user):
    """Canceled subscription returns 402."""
    from fastapi import HTTPException

    household.subscription_status = "canceled"
    household.trial_ends_at = None
    await db_session.flush()

    from app.api.deps import require_active_subscription

    with pytest.raises(HTTPException) as exc_info:
        await require_active_subscription(user=user, db=db_session)
    assert exc_info.value.status_code == 402


@pytest.mark.asyncio
async def test_gate_blocks_expired_trial(db_session, household, user):
    """Expired trial returns 402."""
    from fastapi import HTTPException

    household.subscription_status = "trial"
    household.trial_ends_at = datetime.now(UTC) - timedelta(days=1)
    await db_session.flush()

    from app.api.deps import require_active_subscription

    with pytest.raises(HTTPException) as exc_info:
        await require_active_subscription(user=user, db=db_session)
    assert exc_info.value.status_code == 402
