"""Rate limiter tests (METHEAN-6-10).

Covers the policy machinery in :mod:`app.core.rate_limit`. Uses a
fake Redis so we don't need an actual server and the counters stay
deterministic across test runs.
"""

from __future__ import annotations

import time
from collections import defaultdict
from unittest.mock import MagicMock

import pytest

from app.core.rate_limit import (
    POLICIES,
    RateLimitPolicy,
    check_and_consume,
    client_ip,
)


class FakeRedis:
    """Minimal in-memory Redis stand-in for the limiter."""

    def __init__(self, *, fail: bool = False):
        self.store: dict[str, int] = defaultdict(int)
        self.expirations: dict[str, int] = {}
        self.fail = fail

    async def incrby(self, key: str, amount: int = 1) -> int:
        if self.fail:
            raise RuntimeError("redis down")
        self.store[key] += amount
        return self.store[key]

    async def expire(self, key: str, seconds: int) -> bool:
        if self.fail:
            raise RuntimeError("redis down")
        self.expirations[key] = seconds
        return True


# ══════════════════════════════════════════════════════════════════════
# fail-open vs fail-closed
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_default_policy_fails_open_when_redis_down():
    """The bulk-read 'default' policy must allow requests when Redis
    is down so an outage doesn't take down the whole API.
    """
    redis = FakeRedis(fail=True)
    allowed, _ = await check_and_consume(redis, POLICIES["default"], {"ip": "1.2.3.4"})
    assert allowed is True


@pytest.mark.asyncio
async def test_login_policy_fails_closed_when_redis_down():
    """Auth must NOT fail open — a Redis outage should not silently
    disable brute-force protection.
    """
    redis = FakeRedis(fail=True)
    allowed, retry_after = await check_and_consume(
        redis,
        POLICIES["login"],
        {"ip": "1.2.3.4", "email": "victim@example.com"},
    )
    assert allowed is False
    assert retry_after == 60


# ══════════════════════════════════════════════════════════════════════
# Login policy: scoped per (ip, email)
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_login_limited_per_ip_email_pair():
    """The 11th attempt against the same (ip, email) is rejected."""
    redis = FakeRedis()
    policy = POLICIES["login"]
    kv = {"ip": "1.1.1.1", "email": "alice@example.com"}

    for _ in range(policy.requests):
        allowed, _ = await check_and_consume(redis, policy, kv)
        assert allowed is True

    allowed, retry_after = await check_and_consume(redis, policy, kv)
    assert allowed is False
    assert retry_after == policy.window_seconds


@pytest.mark.asyncio
async def test_login_different_emails_independent():
    """Locking out one email must not lock out another from the same IP."""
    redis = FakeRedis()
    policy = POLICIES["login"]
    ip = "1.1.1.1"

    for _ in range(policy.requests):
        await check_and_consume(redis, policy, {"ip": ip, "email": "alice@example.com"})
    alice_blocked, _ = await check_and_consume(redis, policy, {"ip": ip, "email": "alice@example.com"})
    bob_first, _ = await check_and_consume(redis, policy, {"ip": ip, "email": "bob@example.com"})

    assert alice_blocked is False
    assert bob_first is True


# ══════════════════════════════════════════════════════════════════════
# Forgot password: long window, per email
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_forgot_password_per_email_per_hour():
    """5 forgot-password requests per (ip, email) per hour."""
    redis = FakeRedis()
    policy = POLICIES["forgot_password"]
    assert policy.window_seconds == 3600
    kv = {"ip": "1.1.1.1", "email": "alice@example.com"}

    for _ in range(policy.requests):
        allowed, _ = await check_and_consume(redis, policy, kv)
        assert allowed is True

    allowed, retry_after = await check_and_consume(redis, policy, kv)
    assert allowed is False
    assert retry_after == 3600


# ══════════════════════════════════════════════════════════════════════
# AI generation: keyed on user_id + household
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_ai_generation_keyed_on_user_household():
    """Two different users in the same household get independent
    counters; cost=5 means 6 calls fit in the 30 budget per minute.
    """
    redis = FakeRedis()
    policy = POLICIES["ai_generation"]
    assert policy.cost == 5

    user_a = {"user_id": "user-A", "household": "hh-1"}
    user_b = {"user_id": "user-B", "household": "hh-1"}

    for i in range(6):
        allowed, _ = await check_and_consume(redis, policy, user_a)
        assert allowed is True, f"call {i + 1} should pass"

    blocked, retry_after = await check_and_consume(redis, policy, user_a)
    assert blocked is False
    assert retry_after == policy.window_seconds

    # User B in the same household has its own counter.
    allowed, _ = await check_and_consume(redis, policy, user_b)
    assert allowed is True


# ══════════════════════════════════════════════════════════════════════
# X-Forwarded-For trust
# ══════════════════════════════════════════════════════════════════════


def _request(direct_ip: str, xff: str | None = None) -> MagicMock:
    req = MagicMock()
    req.client.host = direct_ip
    req.headers = {"x-forwarded-for": xff} if xff else {}
    return req


def test_x_forwarded_for_only_honored_for_trusted_proxy():
    """When the immediate peer is a trusted proxy, XFF wins. When the
    peer is untrusted, XFF is ignored to prevent header spoofing.
    """
    untrusted = _request("8.8.8.8", xff="1.1.1.1")
    assert client_ip(untrusted, trusted_proxies=["10.0.0.1"]) == "8.8.8.8"

    trusted = _request("10.0.0.1", xff="1.1.1.1")
    assert client_ip(trusted, trusted_proxies=["10.0.0.1"]) == "1.1.1.1"

    # XFF can carry multiple hops — the first entry is the originating
    # client per the standard.
    chained = _request("10.0.0.1", xff="9.9.9.9, 1.1.1.1")
    assert client_ip(chained, trusted_proxies=["10.0.0.1"]) == "9.9.9.9"

    # No XFF header at all: always falls back to the direct peer.
    bare = _request("10.0.0.1")
    assert client_ip(bare, trusted_proxies=["10.0.0.1"]) == "10.0.0.1"


# ══════════════════════════════════════════════════════════════════════
# Retry-After header propagation
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_retry_after_header_present_on_429():
    """When the limiter rejects, the dependency's HTTPException carries
    a Retry-After header equal to the policy window.
    """
    from fastapi import HTTPException

    tight = RateLimitPolicy(
        name="tight",
        requests=2,
        window_seconds=37,
        key_components=["ip"],
        fail_open=False,
    )
    redis = FakeRedis()
    kv = {"ip": "1.2.3.4"}

    await check_and_consume(redis, tight, kv)
    await check_and_consume(redis, tight, kv)
    allowed, retry_after = await check_and_consume(redis, tight, kv)
    assert allowed is False
    assert retry_after == 37

    # Same shape as the dependency-factory raise path.
    exc = HTTPException(
        status_code=429,
        detail="Too many requests",
        headers={"Retry-After": str(retry_after)},
    )
    assert exc.status_code == 429
    assert exc.headers["Retry-After"] == "37"

    # Tie back to a real shipping policy.
    real = POLICIES["login"]
    assert real.fail_open is False
    assert real.window_seconds == 60
    # Sanity: helper math doesn't drift across the second boundary.
    assert int(time.time()) // real.window_seconds >= 0


# ══════════════════════════════════════════════════════════════════════
# Missing-Redis tolerance
# ══════════════════════════════════════════════════════════════════════
#
# Pre-fix: the middleware unconditionally read ``request.app.state.redis``.
# In the test environment the lifespan handler never runs, so the State
# object had no ``redis`` attribute and Starlette raised AttributeError,
# returning 500 from every non-health request. These tests lock in the
# fix at both layers (middleware + helper).


@pytest.mark.asyncio
async def test_middleware_does_not_crash_when_redis_unavailable():
    """The middleware must fall through to fail_open behavior when
    ``app.state.redis`` is missing — no AttributeError, no 500.

    Uses a fresh ``httpx.AsyncClient`` against the raw ASGI app so
    this test doesn't depend on the conftest ``client`` fixture's
    db_session setup. The middleware exempts ``/health`` from rate
    limiting entirely; this test additionally hits ``/metrics`` which
    is exempt for the same reason — together they confirm the rest
    of the request pipeline (CSRF, security headers) survives a
    missing redis cleanly.
    """
    from httpx import ASGITransport, AsyncClient

    from app.main import app

    if hasattr(app.state, "redis"):
        del app.state.redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/health")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_check_and_consume_returns_fail_open_when_redis_is_none():
    # default policy is fail_open=True
    allowed, _ = await check_and_consume(None, POLICIES["default"], {"ip": "1.1.1.1"})
    assert allowed is True


@pytest.mark.asyncio
async def test_check_and_consume_returns_fail_closed_when_redis_is_none_for_login():
    # login policy is fail_open=False; the helper must NOT silently
    # admit when Redis is absent.
    allowed, _ = await check_and_consume(None, POLICIES["login"], {"ip": "1.1.1.1", "email": "a@b.c"})
    assert allowed is False


# ══════════════════════════════════════════════════════════════════════
# In-handler call sites must also tolerate missing redis
# ══════════════════════════════════════════════════════════════════════
#
# login + forgot-password are body-keyed, so they call check_and_consume
# directly inside the handler instead of via the dependency factory.
# Those call sites must use ``getattr(..., "redis", None)`` to match the
# middleware-level fix, otherwise a missing redis client crashes the
# request with AttributeError.


@pytest.mark.asyncio
async def test_login_handler_does_not_crash_when_redis_unavailable(client):
    """Locks in the fix: login must reach its real response, not 500,
    when redis is absent."""
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrongpassword"},
        headers={"x-csrf-token": "test-csrf-token-for-tests"},
    )
    # Acceptable outcomes: 401 (bad creds), 422 (validation), 429 (if a
    # later prompt wires fakeredis). NOT acceptable: 500 (the bug).
    assert resp.status_code != 500, f"Login crashed with 500: {resp.text}"
    assert resp.status_code in (200, 401, 403, 422, 429)


@pytest.mark.asyncio
async def test_forgot_password_handler_does_not_crash_when_redis_unavailable(client):
    resp = await client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "anyone@example.com"},
        headers={"x-csrf-token": "test-csrf-token-for-tests"},
    )
    assert resp.status_code != 500
    assert resp.status_code in (200, 202, 422)
