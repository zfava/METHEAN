"""Pure-function unit tests for high-trust modules.

The existing httpx-driven auth and billing tests cover the request
paths but skip the small helpers (cookie setters, hashers, role
maps, pagination defaults). This module fills those gaps without
requiring a database or Redis fixture so they run as fast unit
tests and don't depend on integration infrastructure.

Routes that require DB roundtrips live in test_auth_api.py and
test_billing.py.
"""

from __future__ import annotations

import hashlib

import pytest
from fastapi import HTTPException, Response

# ══════════════════════════════════════════════════════════════════════
# auth.py helpers
# ══════════════════════════════════════════════════════════════════════


def test_hash_token_is_sha256_hex_digest():
    from app.api.auth import _hash_token

    token = "test-refresh-token-value"
    assert _hash_token(token) == hashlib.sha256(token.encode()).hexdigest()
    # 256-bit digest = 64 hex chars
    assert len(_hash_token(token)) == 64


def test_hash_token_is_deterministic():
    from app.api.auth import _hash_token

    assert _hash_token("a") == _hash_token("a")
    assert _hash_token("a") != _hash_token("b")


def test_hash_token_handles_empty_string():
    from app.api.auth import _hash_token

    # Hashing an empty string is well-defined and useful for sentinel checks.
    assert _hash_token("") == hashlib.sha256(b"").hexdigest()


def test_set_cookie_sets_httponly_lax_path(monkeypatch):
    from app.api.auth import _set_cookie
    from app.core.config import settings

    monkeypatch.setattr(settings, "APP_ENV", "development")

    response = Response()
    _set_cookie(response, "access_token", "abc123", max_age=900)

    set_cookie_header = response.headers.get("set-cookie")
    assert set_cookie_header is not None
    assert "access_token=abc123" in set_cookie_header
    assert "HttpOnly" in set_cookie_header
    assert "SameSite=lax" in set_cookie_header
    assert "Path=/" in set_cookie_header
    assert "Max-Age=900" in set_cookie_header
    # Dev mode: Secure flag is OFF so localhost http:// works.
    assert "Secure" not in set_cookie_header


def test_set_cookie_marks_secure_in_production(monkeypatch):
    from app.api.auth import _set_cookie
    from app.core.config import settings

    monkeypatch.setattr(settings, "APP_ENV", "production")

    response = Response()
    _set_cookie(response, "refresh_token", "xyz789", max_age=86400)

    set_cookie_header = response.headers.get("set-cookie")
    assert "Secure" in set_cookie_header


def test_institutional_role_mapping_covers_all_known_roles():
    from app.api.auth import _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE

    # Locking down the mapping prevents a silent rename from breaking
    # invite acceptance for institution accounts.
    assert _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE["instructor"] == "co_parent"
    assert _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE["teaching_assistant"] == "observer"
    assert _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE["student"] == "observer"


# ══════════════════════════════════════════════════════════════════════
# deps.py: PaginationParams + dependency factories
# ══════════════════════════════════════════════════════════════════════


def test_pagination_params_accepts_explicit_values():
    """The defaults are FastAPI ``Query()`` markers that are only
    resolved into ints when the dependency injector parses real query
    params. Direct instantiation with explicit values exercises the
    same constructor and is the path other tests use."""
    from app.api.deps import PaginationParams

    p = PaginationParams(skip=20, limit=100)
    assert p.skip == 20
    assert p.limit == 100

    zero = PaginationParams(skip=0, limit=1)
    assert zero.skip == 0
    assert zero.limit == 1


def test_require_role_factory_returns_callable():
    from app.api.deps import require_role

    checker = require_role("owner", "co_parent")
    assert callable(checker)


def test_require_permission_factory_returns_callable():
    from app.api.deps import require_permission

    checker = require_permission("plans.create")
    assert callable(checker)
    # scope_type is optional; passing it must not blow up.
    scoped = require_permission("plans.create", scope_type="child")
    assert callable(scoped)


# ══════════════════════════════════════════════════════════════════════
# password_reset: pure-function token verification paths
# ══════════════════════════════════════════════════════════════════════


def test_verify_reset_token_rejects_unknown_token():
    from app.services.password_reset import verify_reset_token

    assert verify_reset_token("does-not-exist") is None


def test_verify_reset_token_expires_and_purges():
    """An expired token returns None AND is removed from the store so a
    later attempt cannot resurrect it via a clock change.
    """
    from datetime import UTC, datetime

    from app.services.password_reset import _reset_tokens, verify_reset_token

    token = "fixture-expired-token"
    _reset_tokens[token] = {
        "user_id": "00000000-0000-0000-0000-000000000000",
        "expires_at": datetime(2020, 1, 1, tzinfo=UTC),
    }
    assert verify_reset_token(token) is None
    assert token not in _reset_tokens


def test_verify_reset_token_accepts_fresh_token():
    from datetime import UTC, datetime, timedelta

    from app.services.password_reset import _reset_tokens, verify_reset_token

    token = "fixture-fresh-token"
    user_id = "11111111-1111-1111-1111-111111111111"
    _reset_tokens[token] = {
        "user_id": user_id,
        "expires_at": datetime.now(UTC) + timedelta(hours=1),
    }
    try:
        assert verify_reset_token(token) == user_id
    finally:
        _reset_tokens.pop(token, None)


# ══════════════════════════════════════════════════════════════════════
# auth.py request schemas — Pydantic validation
# ══════════════════════════════════════════════════════════════════════


def test_register_request_requires_min_password_length():
    from pydantic import ValidationError

    from app.schemas.auth import RegisterRequest

    with pytest.raises(ValidationError):
        RegisterRequest(
            email="x@y.com",
            password="short",  # below floor
            display_name="X",
            household_name="X",
        )


def test_register_request_accepts_valid_payload():
    from app.schemas.auth import RegisterRequest

    body = RegisterRequest(
        email="x@y.com",
        password="long-enough-password",
        display_name="X",
        household_name="X",
    )
    assert body.email == "x@y.com"
    assert body.is_self_learner is False  # default


# ══════════════════════════════════════════════════════════════════════
# Negative path: HTTPException construction in dep code paths
# ══════════════════════════════════════════════════════════════════════


def test_http_exception_carries_detail_on_403():
    """Tiny smoke test that the HTTPException class still behaves —
    catches a regression in fastapi's exception module before it
    surfaces as a confusing 500.
    """
    exc = HTTPException(status_code=403, detail="Insufficient permissions")
    assert exc.status_code == 403
    assert exc.detail == "Insufficient permissions"
