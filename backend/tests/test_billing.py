"""Tests for Stripe billing integration."""

import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Household


@pytest_asyncio.fixture
async def billing_household(db_session: AsyncSession) -> Household:
    h = Household(name="Billing Test Family")
    h.subscription_status = "trial"
    h.trial_ends_at = datetime.now(timezone.utc) + timedelta(days=30)
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
    billing_household.subscription_ends_at = datetime.now(timezone.utc) + timedelta(days=30)
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
    """No webhook secret returns False."""
    mock_settings.STRIPE_WEBHOOK_SECRET = ""
    from app.services.billing import handle_webhook
    result = await handle_webhook(b"payload", "sig")
    assert result is False


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
