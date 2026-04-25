"""Per-endpoint rate limiting with multi-component keys.

Replaces the legacy IP-only middleware that fail-opened on every Redis
exception. Auth and AI policies fail closed; bulk read endpoints can
opt into the historical fail-open behavior via the ``default`` policy.

Two integration patterns:

* :func:`rate_limit` — FastAPI dependency factory keyed on IP +
  endpoint. Use for routes whose key components are visible without
  reading the request body.
* :func:`rate_limit_user` — dependency factory that also pulls
  ``user_id`` and ``household_id`` off the authenticated user.
* :func:`check_and_consume` — call directly inside a handler when the
  key depends on the parsed request body (login email,
  forgot-password email).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from fastapi import Depends, HTTPException, Request

from app.api.deps import get_current_user
from app.core.config import settings

if TYPE_CHECKING:
    from app.models.identity import User

KeyComponent = Literal["ip", "user_id", "email", "endpoint", "household"]


@dataclass(frozen=True)
class RateLimitPolicy:
    name: str
    requests: int
    window_seconds: int
    key_components: list[KeyComponent] = field(default_factory=lambda: ["ip", "endpoint"])
    fail_open: bool = False
    cost: int = 1


# Tuned per-route. ``fail_open`` is False on anything an attacker
# could weaponise (auth + AI); the wider ``default`` policy fails
# open so a Redis outage doesn't take down the whole API.
POLICIES: dict[str, RateLimitPolicy] = {
    "default": RateLimitPolicy("default", 60, 60, ["ip", "endpoint"], fail_open=True),
    "login": RateLimitPolicy("login", 10, 60, ["ip", "email"], fail_open=False),
    "register": RateLimitPolicy("register", 5, 60, ["ip"], fail_open=False),
    "forgot_password": RateLimitPolicy("forgot_password", 5, 3600, ["ip", "email"], fail_open=False),
    "verify_email": RateLimitPolicy("verify_email", 20, 3600, ["ip"], fail_open=False),
    "ai_generation": RateLimitPolicy("ai_generation", 30, 60, ["user_id", "household"], fail_open=False, cost=5),
    "tutor_message": RateLimitPolicy("tutor_message", 60, 60, ["user_id", "household"], fail_open=False, cost=2),
}


async def check_and_consume(
    redis,
    policy: RateLimitPolicy,
    key_values: dict[str, str],
) -> tuple[bool, int]:
    """Increment the counter for this policy + key tuple.

    Returns ``(allowed, retry_after_seconds)``. ``retry_after_seconds``
    is meaningful only when ``allowed`` is False.
    """
    window = int(time.time()) // policy.window_seconds
    parts = [policy.name, str(window)] + [f"{k}={key_values.get(k, '_')}" for k in policy.key_components]
    redis_key = ":".join(["ratelimit"] + parts)
    try:
        count = await redis.incrby(redis_key, policy.cost)
        if count == policy.cost:
            await redis.expire(redis_key, policy.window_seconds)
        if count > policy.requests:
            return False, policy.window_seconds
        return True, 0
    except Exception:
        # Auth + AI policies declare fail_open=False so the gate stays
        # closed when Redis is unreachable; a Redis outage must not
        # disable brute-force protection.
        return policy.fail_open, 60


def client_ip(request: Request, trusted_proxies: list[str]) -> str:
    """Resolve the originating client IP.

    ``X-Forwarded-For`` is only consulted when the immediate peer
    appears in ``trusted_proxies`` — otherwise an external client
    could spoof a header to bypass per-IP limits.
    """
    direct = request.client.host if request.client else "unknown"
    xff = request.headers.get("x-forwarded-for")
    if xff and direct in trusted_proxies:
        return xff.split(",")[0].strip()
    return direct


def rate_limit(policy_name: str):
    """Anonymous-friendly limiter keyed on IP + endpoint."""

    async def checker(request: Request) -> None:
        policy = POLICIES[policy_name]
        key_values = {
            "ip": client_ip(request, settings.TRUSTED_PROXIES),
            "endpoint": request.url.path,
        }
        allowed, retry_after = await check_and_consume(request.app.state.redis, policy, key_values)
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Too many requests",
                headers={"Retry-After": str(retry_after)},
            )

    return checker


def rate_limit_user(policy_name: str):
    """Authenticated limiter that also keys on user/household."""

    async def checker(
        request: Request,
        user: User = Depends(get_current_user),
    ) -> None:
        policy = POLICIES[policy_name]
        key_values = {
            "ip": client_ip(request, settings.TRUSTED_PROXIES),
            "endpoint": request.url.path,
            "user_id": str(user.id),
            "household": str(user.household_id),
        }
        allowed, retry_after = await check_and_consume(request.app.state.redis, policy, key_values)
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Too many requests",
                headers={"Retry-After": str(retry_after)},
            )

    return checker
