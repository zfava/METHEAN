"""Pure-function unit tests for high-trust modules (METHEAN-6-14).

The existing httpx-driven auth and billing tests cover the request
paths but skip the small helpers (cookie setters, hashers, role
maps, pagination defaults, token verification). This module fills
those gaps without requiring a database or Redis fixture so they run
as fast unit tests and don't depend on integration infrastructure.

DB-bound integration tests for the same modules live in
test_auth_api.py, test_billing.py, test_password_reset.py, and
test_child_access.py.
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

    assert "Secure" in response.headers.get("set-cookie", "")


def test_institutional_role_mapping_covers_all_known_roles():
    from app.api.auth import _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE

    # Locking down the mapping prevents a silent rename from breaking
    # invite acceptance for institution accounts.
    assert _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE["instructor"] == "co_parent"
    assert _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE["teaching_assistant"] == "observer"
    assert _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE["student"] == "observer"


def test_invite_role_normaliser_maps_legacy_aliases():
    from app.api.auth import _normalize_invite_role
    from app.models.enums import UserRole

    # Canonical values pass through unchanged.
    assert _normalize_invite_role("owner") == UserRole.owner
    assert _normalize_invite_role("co_parent") == UserRole.co_parent
    assert _normalize_invite_role("observer") == UserRole.observer
    # Legacy aliases flatten to the modern enum values.
    assert _normalize_invite_role("parent") == UserRole.co_parent
    assert _normalize_invite_role("viewer") == UserRole.observer
    # Whitespace + case-insensitive matching.
    assert _normalize_invite_role("  CO_PARENT ") == UserRole.co_parent


def test_invite_role_normaliser_rejects_unknown():
    from app.api.auth import _normalize_invite_role

    with pytest.raises(HTTPException) as exc:
        _normalize_invite_role("admin")
    assert exc.value.status_code == 400
    assert "Invalid role" in str(exc.value.detail)


# ══════════════════════════════════════════════════════════════════════
# deps.py: PaginationParams + dependency factories
# ══════════════════════════════════════════════════════════════════════


def test_pagination_params_accepts_explicit_values():
    """The defaults are FastAPI ``Query()`` markers that are only
    resolved into ints when the dependency injector parses real query
    params. Direct instantiation with explicit values exercises the
    same constructor."""
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
    scoped = require_permission("plans.create", scope_type="child")
    assert callable(scoped)


def test_require_child_access_factory_returns_callable():
    from app.api.deps import require_child_access

    read_checker = require_child_access("read")
    write_checker = require_child_access("write")
    assert callable(read_checker)
    assert callable(write_checker)


# ══════════════════════════════════════════════════════════════════════
# password_reset / email_verification: pure helpers
# ══════════════════════════════════════════════════════════════════════


def test_password_reset_hash_is_sha256_hex():
    from app.services.password_reset import _hash

    assert _hash("plain") == hashlib.sha256(b"plain").hexdigest()
    assert len(_hash("plain")) == 64


def test_email_verification_hash_is_sha256_hex():
    from app.services.email_verification import _hash

    assert _hash("plain") == hashlib.sha256(b"plain").hexdigest()
    assert len(_hash("plain")) == 64


def test_email_verification_token_ttl_is_60_minutes():
    """Lock down the TTL constant so a silent change can't
    drop the validity window without a code review."""
    from app.services.email_verification import TOKEN_TTL_MINUTES

    assert TOKEN_TTL_MINUTES == 60


def test_password_reset_token_ttl_is_60_minutes():
    from app.services.password_reset import TOKEN_TTL_MINUTES

    assert TOKEN_TTL_MINUTES == 60


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


def test_invite_request_normalises_role_in_validator():
    """The local InviteRequest.role validator lowercases + strips
    whitespace before persisting, so a "Parent" input reaches the
    DB as "parent" and routes through _normalize_invite_role to the
    canonical enum value.
    """
    from app.api.auth import InviteRequest

    req = InviteRequest(email="x@y.com", role=" Parent ")
    assert req.role == "parent"


def test_invite_request_rejects_unknown_role_at_pydantic_layer():
    from pydantic import ValidationError

    from app.api.auth import InviteRequest

    with pytest.raises(ValidationError):
        InviteRequest(email="x@y.com", role="admin")


# ══════════════════════════════════════════════════════════════════════
# billing.py: schema sanity
# ══════════════════════════════════════════════════════════════════════


def test_checkout_body_accepts_optional_urls():
    from app.api.billing import CheckoutBody

    # All-default construction is valid (frontend may omit URLs).
    body = CheckoutBody()
    assert body.success_url is None
    assert body.cancel_url is None

    # Explicit values round-trip.
    full = CheckoutBody(success_url="https://m.app/ok", cancel_url="https://m.app/x")
    assert full.success_url == "https://m.app/ok"
    assert full.cancel_url == "https://m.app/x"


def test_portal_body_accepts_optional_return_url():
    from app.api.billing import PortalBody

    assert PortalBody().return_url is None
    assert PortalBody(return_url="https://m.app/back").return_url == "https://m.app/back"


# ══════════════════════════════════════════════════════════════════════
# Negative path: HTTPException construction (smoke test for fastapi)
# ══════════════════════════════════════════════════════════════════════


def test_http_exception_carries_detail_on_403():
    """Tiny smoke test that the HTTPException class still behaves."""
    exc = HTTPException(status_code=403, detail="Insufficient permissions")
    assert exc.status_code == 403
    assert exc.detail == "Insufficient permissions"
