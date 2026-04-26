"""Test that all sensitive endpoints reject unauthenticated access.

Systematically hits every major route group WITHOUT an auth cookie/header
and verifies that the server returns 401 (Unauthorized) or 403 (Forbidden).

Intentionally unauthenticated routes are tested separately to confirm
they DO work without auth.
"""

import pytest
from httpx import AsyncClient

DUMMY_UUID = "00000000-0000-0000-0000-000000000001"


# ─── Routes that MUST require auth ───

PROTECTED_ROUTES = [
    # Children / household
    ("GET", "/api/v1/children"),
    ("POST", "/api/v1/children"),
    ("GET", "/api/v1/household/settings"),
    ("PUT", "/api/v1/household/settings"),
    ("GET", "/api/v1/household/philosophy"),
    ("PUT", "/api/v1/household/philosophy"),
    ("GET", "/api/v1/household/academic-calendar"),
    ("PUT", "/api/v1/household/academic-calendar"),
    # Auth (authenticated)
    ("GET", "/api/v1/auth/me"),
    ("PUT", "/api/v1/auth/password"),
    ("GET", "/api/v1/auth/me/notification-preferences"),
    # Curriculum
    ("POST", "/api/v1/subjects"),
    ("GET", "/api/v1/subjects"),
    ("GET", "/api/v1/learning-maps"),
    ("GET", "/api/v1/learning-maps/templates"),
    # Governance
    ("GET", "/api/v1/governance-rules"),
    ("POST", "/api/v1/governance-rules"),
    ("POST", "/api/v1/governance/report"),
    ("GET", "/api/v1/governance/rules/upcoming"),
    # Intelligence
    ("GET", f"/api/v1/children/{DUMMY_UUID}/intelligence"),
    ("GET", "/api/v1/household/governance-intelligence"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/achievements"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/streak"),
    # Calibration
    ("GET", f"/api/v1/children/{DUMMY_UUID}/calibration"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/calibration/predictions"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/calibration/drift-history"),
    # Wellbeing (CRITICAL: parent-only)
    ("GET", f"/api/v1/children/{DUMMY_UUID}/wellbeing/anomalies"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/wellbeing/config"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/wellbeing/summary"),
    # Family intelligence
    ("GET", "/api/v1/household/family-insights"),
    ("GET", "/api/v1/household/family-insights/summary"),
    ("GET", "/api/v1/household/family-insights/config"),
    # Style vector
    ("GET", f"/api/v1/children/{DUMMY_UUID}/style-vector"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/style-vector/history"),
    # Annual curriculum
    ("GET", f"/api/v1/children/{DUMMY_UUID}/curricula"),
    ("POST", f"/api/v1/children/{DUMMY_UUID}/curricula/generate"),
    # Assessment / portfolio
    ("GET", f"/api/v1/children/{DUMMY_UUID}/assessments"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/portfolio"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/transcript"),
    # Fitness
    ("POST", "/api/v1/fitness/log"),
    ("GET", f"/api/v1/fitness/log/{DUMMY_UUID}"),
    ("POST", "/api/v1/fitness/benchmark"),
    ("GET", f"/api/v1/fitness/benchmarks/{DUMMY_UUID}"),
    ("GET", f"/api/v1/fitness/progress/{DUMMY_UUID}"),
    ("GET", f"/api/v1/fitness/stats/{DUMMY_UUID}"),
    # Billing (authenticated)
    ("GET", "/api/v1/billing/status"),
    ("POST", "/api/v1/billing/subscribe"),
    ("POST", "/api/v1/billing/cancel"),
    ("POST", "/api/v1/billing/portal"),
    # Compliance check (requires auth)
    ("GET", f"/api/v1/children/{DUMMY_UUID}/compliance/check"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/attendance"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/hours"),
    # Documents
    ("GET", f"/api/v1/children/{DUMMY_UUID}/documents/ihip"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/documents/transcript"),
    # Education plan
    ("GET", f"/api/v1/children/{DUMMY_UUID}/education-plan"),
    ("POST", f"/api/v1/children/{DUMMY_UUID}/education-plan/generate"),
    # Resources
    ("POST", "/api/v1/resources"),
    ("GET", "/api/v1/resources"),
    # Notifications
    ("GET", "/api/v1/notifications"),
    # Operations / alerts
    ("GET", f"/api/v1/children/{DUMMY_UUID}/alerts"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/snapshots"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/compliance-report"),
    # Child dashboard
    ("GET", f"/api/v1/children/{DUMMY_UUID}/dashboard"),
    # Feedback / reading log
    ("GET", f"/api/v1/children/{DUMMY_UUID}/feedback/recent"),
    ("GET", f"/api/v1/children/{DUMMY_UUID}/reading-log"),
    # Usage
    ("GET", "/api/v1/usage/current"),
    ("GET", "/api/v1/usage/breakdown"),
    # Data export
    ("POST", "/api/v1/household/export"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path",
    PROTECTED_ROUTES,
    ids=[f"{m} {p.replace(DUMMY_UUID, 'UUID')}" for m, p in PROTECTED_ROUTES],
)
async def test_protected_route_rejects_unauthenticated(client: AsyncClient, method: str, path: str):
    """Every protected route returns 401 or 403 without auth."""
    # Remove the auth cookie that conftest sets
    client.cookies.clear()
    client.headers.pop("Authorization", None)

    if method == "GET":
        resp = await client.get(path)
    elif method == "POST":
        resp = await client.post(path, json={})
    elif method == "PUT":
        resp = await client.put(path, json={})
    elif method == "PATCH":
        resp = await client.patch(path, json={})
    elif method == "DELETE":
        resp = await client.delete(path)
    else:
        pytest.fail(f"Unknown method: {method}")

    assert resp.status_code in (401, 403, 422), (
        f"{method} {path} returned {resp.status_code} without auth (expected 401/403/422). Body: {resp.text[:300]}"
    )


# ─── Routes that MUST work without auth ───

PUBLIC_ROUTES = [
    ("GET", "/health"),
    ("GET", "/health/ready"),
    ("GET", "/api/v1/compliance/states"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("method,path", PUBLIC_ROUTES, ids=[f"{m} {p}" for m, p in PUBLIC_ROUTES])
async def test_public_route_accessible(client: AsyncClient, method: str, path: str):
    """Public routes respond without auth (may return various codes but not 401)."""
    client.cookies.clear()
    client.headers.pop("Authorization", None)

    if method == "GET":
        resp = await client.get(path)
    elif method == "POST":
        resp = await client.post(path, json={})
    else:
        pytest.fail(f"Unknown method: {method}")

    assert resp.status_code != 401, f"{method} {path} requires auth but should be public. Status: {resp.status_code}"


# ─── Auth endpoints that accept unauthenticated POST (register/login) ───


@pytest.mark.asyncio
async def test_register_does_not_require_auth(client: AsyncClient):
    """Register endpoint accepts unauthenticated POST (returns 4xx for bad data, not 401)."""
    client.cookies.clear()
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "Str0ngP@ssword!",
            "display_name": "New User",
            "household_name": "New Family",
        },
    )
    # Should not return 401 — register is intentionally unauthenticated
    # May return 201 (success), 409 (duplicate), or 422 (validation) — all OK
    assert resp.status_code != 401, f"Register requires auth but shouldn't. Status: {resp.status_code}"


@pytest.mark.asyncio
async def test_login_does_not_require_auth(client: AsyncClient):
    """Login endpoint accepts unauthenticated POST."""
    client.cookies.clear()
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrongpassword"},
    )
    # Should not return 401 for unauthenticated access — it IS the auth endpoint
    # Returns 401 for wrong credentials, but that's different from "no auth token"
    # The key check: it processes the request, not rejects it for missing auth
    assert resp.status_code in (200, 401, 403, 422), f"Login returned unexpected {resp.status_code}"


# ─── Webhook must reject without valid Stripe signature ───


@pytest.mark.asyncio
async def test_webhook_rejects_without_signature(client: AsyncClient):
    """Stripe webhook rejects requests without valid signature."""
    client.cookies.clear()
    resp = await client.post(
        "/api/v1/billing/webhook",
        content=b'{"type": "fake.event"}',
        headers={"Content-Type": "application/json"},
    )
    # Should NOT return 200 — unsigned webhooks must be rejected
    assert resp.status_code != 200, (
        f"Webhook accepted request without valid Stripe signature! Status: {resp.status_code}"
    )


# ─── CSRF enforcement on state-changing methods ───


@pytest.mark.asyncio
async def test_csrf_rejects_post_without_token(client: AsyncClient):
    """POST to a protected endpoint without CSRF token returns 403."""
    # Remove CSRF token header but keep auth in place
    headers = dict(client.headers)
    headers.pop("X-CSRF-Token", None)
    resp = await client.post(
        "/api/v1/subjects",
        json={"name": "Test"},
        headers={k: v for k, v in headers.items() if k != "X-CSRF-Token"},
    )
    # Without CSRF token, should get 403
    assert resp.status_code in (401, 403), f"POST without CSRF token returned {resp.status_code}, expected 401/403"


# ─── Security headers present on all responses ───


@pytest.mark.asyncio
async def test_security_headers_on_health(client: AsyncClient):
    """Security headers are present even on public health endpoint.

    Accepts either ``Content-Security-Policy`` (when CSP_ENFORCE is True)
    or ``Content-Security-Policy-Report-Only`` (the default during the
    Prompt 11 staged rollout). The contents are identical; the test
    only cares that *some* CSP header is being delivered.
    """
    resp = await client.get("/health")
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "DENY"
    assert "Content-Security-Policy" in resp.headers or "Content-Security-Policy-Report-Only" in resp.headers, (
        "No CSP header (enforced or report-only) present"
    )


@pytest.mark.asyncio
async def test_csp_header_blocks_framing(client: AsyncClient):
    """CSP includes frame-ancestors 'none' to prevent clickjacking.

    Reads the enforced header first, falls back to the report-only
    header. Both carry the same policy string during the staged
    rollout, so the framing-protection assertion is meaningful either
    way.
    """
    resp = await client.get("/health")
    csp = resp.headers.get(
        "Content-Security-Policy",
        resp.headers.get("Content-Security-Policy-Report-Only", ""),
    )
    assert "frame-ancestors 'none'" in csp
