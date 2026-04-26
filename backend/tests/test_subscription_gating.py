"""Subscription gating tests (METHEAN-6-08).

Verifies that ``require_active_subscription`` is wired into every
paid endpoint and that exempt endpoints stay reachable regardless of
subscription state. Locks down the structured 402 body shape so the
frontend can branch on ``error == "subscription_required"`` and
deep-link the user to the checkout URL.

The PAID_ROUTES below differ from the spec's literal list — the
spec called out URLs that don't exist as written, so per the
"verify paths against actual route definitions before running"
clause they're substituted with real, gated routes.
"""

from datetime import UTC, datetime, timedelta

import pytest

PAID_ROUTES = [
    ("GET", "/api/v1/children/{child_id}/intelligence"),
    ("POST", "/api/v1/children/{child_id}/education-plan/generate"),
    ("GET", "/api/v1/children/{child_id}/wellbeing/anomalies"),
    ("GET", "/api/v1/children/{child_id}/calibration"),
    ("POST", "/api/v1/children/{child_id}/counterfactual"),
]

EXEMPT_ROUTES = [
    ("GET", "/api/v1/auth/me"),
    ("GET", "/api/v1/billing/status"),
    ("POST", "/api/v1/billing/portal"),
    ("GET", "/api/v1/notifications"),
    ("GET", "/api/v1/compliance/states"),
]


def _format(path: str, child_id) -> str:
    return path.format(child_id=child_id)


async def _set_subscription(db_session, household, *, status, trial_ends_at=None):
    household.subscription_status = status
    household.trial_ends_at = trial_ends_at
    db_session.add(household)
    await db_session.flush()


async def _request(client, method: str, url: str):
    if method == "GET":
        return await client.get(url)
    if method == "POST":
        return await client.post(url, json={})
    raise AssertionError(f"unsupported method: {method}")


# ══════════════════════════════════════════════════════════════════════
# Paid routes: 402 when canceled, allowed when active/trialing
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "path"), PAID_ROUTES)
async def test_paid_route_requires_active_subscription(method, path, auth_client, db_session, household, child):
    await _set_subscription(db_session, household, status="canceled", trial_ends_at=None)

    resp = await _request(auth_client, method, _format(path, child.id))
    assert resp.status_code == 402, (
        f"{method} {path} should return 402 when subscription is canceled, got {resp.status_code}"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "path"), PAID_ROUTES)
async def test_paid_route_allows_active(method, path, auth_client, db_session, household, child):
    await _set_subscription(db_session, household, status="active", trial_ends_at=None)

    resp = await _request(auth_client, method, _format(path, child.id))
    assert resp.status_code != 402, (
        f"{method} {path} should NOT return 402 when subscription is active, got {resp.status_code}"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "path"), PAID_ROUTES)
async def test_paid_route_allows_trialing(method, path, auth_client, db_session, household, child):
    await _set_subscription(
        db_session,
        household,
        status="trialing",
        trial_ends_at=datetime.now(UTC) + timedelta(days=7),
    )

    resp = await _request(auth_client, method, _format(path, child.id))
    assert resp.status_code != 402, (
        f"{method} {path} should NOT return 402 when subscription is trialing, got {resp.status_code}"
    )


# ══════════════════════════════════════════════════════════════════════
# Exempt routes: never 402
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "path"), EXEMPT_ROUTES)
async def test_exempt_route_works_without_subscription(method, path, auth_client, db_session, household):
    await _set_subscription(db_session, household, status="canceled", trial_ends_at=None)

    resp = await _request(auth_client, method, path)
    assert resp.status_code != 402, (
        f"{method} {path} is on the EXEMPT list but returned 402 with a canceled subscription"
    )


# ══════════════════════════════════════════════════════════════════════
# 402 body shape
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_402_response_body_shape(auth_client, db_session, household, child):
    """The 402 detail must be a structured dict with the keys the
    frontend uses to render the upgrade banner.
    """
    await _set_subscription(db_session, household, status="canceled", trial_ends_at=None)

    resp = await auth_client.get(f"/api/v1/children/{child.id}/intelligence")
    assert resp.status_code == 402

    body = resp.json()
    assert "detail" in body
    detail = body["detail"]
    assert isinstance(detail, dict), f"expected structured detail dict, got {type(detail).__name__}"
    assert detail["error"] == "subscription_required"
    assert detail["status"] == "canceled"
    assert detail["checkout_url"] == "/billing/checkout"
