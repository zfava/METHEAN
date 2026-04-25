"""Tests for the security-headers middleware and the CSP report endpoint.

Production CSP must drop ``'unsafe-eval'`` and replace
``'unsafe-inline'`` on ``script-src`` with a per-request nonce. The
header name flips between ``Content-Security-Policy`` and
``Content-Security-Policy-Report-Only`` based on
``settings.CSP_ENFORCE``. Violation reports are accepted at
``/api/v1/csp-report`` and logged via structlog.
"""

from __future__ import annotations

import logging

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


class _FakeRedis:
    """Stand-in for app.state.redis. The rate-limit middleware reaches
    for it on every non-health request; the lifespan handler that sets
    it up doesn't run under TestClient."""

    async def incrby(self, *_args, **_kwargs):
        return 1

    async def expire(self, *_args, **_kwargs):
        return True


@pytest.fixture
def client(monkeypatch) -> TestClient:
    if not hasattr(app.state, "redis"):
        app.state.redis = _FakeRedis()
    return TestClient(app)


def _csp_value(response, *, enforced: bool) -> str:
    header = "Content-Security-Policy" if enforced else "Content-Security-Policy-Report-Only"
    assert header in response.headers, (
        f"expected {header} in headers, got: {sorted(response.headers.keys())}"
    )
    return response.headers[header]


# ══════════════════════════════════════════════════════════════════════
# Dev mode keeps unsafe-eval for HMR
# ══════════════════════════════════════════════════════════════════════


def test_csp_header_present_in_dev_with_unsafe_eval(client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "development")
    monkeypatch.setattr(settings, "CSP_ENFORCE", False)

    resp = client.get("/health")
    assert resp.status_code == 200

    csp = _csp_value(resp, enforced=False)
    assert "'unsafe-eval'" in csp, "dev CSP must keep 'unsafe-eval' for Next.js HMR"
    assert "'unsafe-inline'" in csp


# ══════════════════════════════════════════════════════════════════════
# Production hardens script-src
# ══════════════════════════════════════════════════════════════════════


def test_csp_header_in_prod_does_not_contain_unsafe_eval(client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "CSP_ENFORCE", True)

    resp = client.get("/health")
    assert resp.status_code == 200

    csp = _csp_value(resp, enforced=True)
    assert "'unsafe-eval'" not in csp, f"prod CSP must drop 'unsafe-eval'; got: {csp}"
    script_src = next(s for s in csp.split(";") if s.strip().startswith("script-src"))
    assert "'unsafe-inline'" not in script_src, (
        "prod script-src must use a nonce instead of 'unsafe-inline'"
    )


def test_csp_header_in_prod_contains_nonce(client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "CSP_ENFORCE", True)

    resp = client.get("/health")
    csp = _csp_value(resp, enforced=True)
    nonce_header = resp.headers.get("X-CSP-Nonce")

    assert nonce_header, "X-CSP-Nonce response header must be present"
    assert f"'nonce-{nonce_header}'" in csp, (
        "production script-src must reference the same nonce surfaced via X-CSP-Nonce"
    )
    assert "https://js.stripe.com" in csp


def test_nonce_is_unique_per_request(client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "CSP_ENFORCE", True)

    nonces = {client.get("/health").headers["X-CSP-Nonce"] for _ in range(8)}
    assert len(nonces) == 8, f"expected 8 unique nonces, got {len(nonces)}: {nonces}"


# ══════════════════════════════════════════════════════════════════════
# Report-only vs enforce
# ══════════════════════════════════════════════════════════════════════


def test_csp_report_only_used_when_enforce_is_false(client, monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    monkeypatch.setattr(settings, "CSP_ENFORCE", False)

    resp = client.get("/health")
    assert "Content-Security-Policy-Report-Only" in resp.headers
    assert "Content-Security-Policy" not in resp.headers

    body = resp.headers["Content-Security-Policy-Report-Only"]
    assert body.endswith("report-uri /api/v1/csp-report"), (
        f"report-only mode must point to /api/v1/csp-report, got: {body}"
    )


# ══════════════════════════════════════════════════════════════════════
# Report endpoint
# ══════════════════════════════════════════════════════════════════════


def test_csp_report_endpoint_accepts_post_returns_204_and_logs(client, monkeypatch):
    """The endpoint accepts a POSTed report, returns 204, and emits a
    structured ``csp_violation`` log event with the parsed report.
    """
    captured: list[dict] = []

    from app import main as main_module

    real_logger = main_module.logger

    class _SpyLogger:
        def warning(self, event, **kwargs):
            captured.append({"event": event, **kwargs})
            return real_logger.warning(event, **kwargs)

    monkeypatch.setattr(main_module, "logger", _SpyLogger())

    sample = {
        "csp-report": {
            "document-uri": "https://methean.app/dashboard",
            "violated-directive": "script-src",
            "blocked-uri": "https://evil.example.com/x.js",
        }
    }
    resp = client.post("/api/v1/csp-report", json=sample)

    assert resp.status_code == 204
    assert resp.content == b""
    violation_events = [c for c in captured if c["event"] == "csp_violation"]
    assert violation_events, f"expected csp_violation log, captured={captured}"
    assert violation_events[0]["report"] == sample
    assert "user_agent" in violation_events[0]
    assert "client_ip" in violation_events[0]


# Keep logging imported so future contributors can ratchet this back
# to a caplog-style assertion if structlog config changes.
_ = logging
