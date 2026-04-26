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
import uuid
from unittest.mock import MagicMock

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


# ══════════════════════════════════════════════════════════════════════
# email_verification.verify_token: error-path coverage without DB
# ══════════════════════════════════════════════════════════════════════
#
# verify_token raises a generic 400 on every failure mode (missing,
# unknown, expired, used, user-gone). The first three branches don't
# need a real database — None/empty short-circuits before any query,
# and an AsyncMock standing in for the session lets us drive the
# scalar_one_or_none paths.


def _mock_db_returning(*scalars):
    """Build an AsyncMock session whose successive db.execute().scalar_one_or_none()
    calls return the supplied values in order."""
    from unittest.mock import AsyncMock, MagicMock

    results = [MagicMock(scalar_one_or_none=MagicMock(return_value=s)) for s in scalars]
    db = AsyncMock()
    db.execute = AsyncMock(side_effect=results)
    db.flush = AsyncMock()
    db.add = MagicMock()
    return db


@pytest.mark.asyncio
async def test_verify_token_rejects_none_plaintext():
    from app.services.email_verification import verify_token

    with pytest.raises(HTTPException) as exc:
        await verify_token(None, None, None)  # type: ignore[arg-type]
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_verify_token_rejects_empty_string_plaintext():
    from app.services.email_verification import verify_token

    with pytest.raises(HTTPException) as exc:
        await verify_token(None, "", None)  # type: ignore[arg-type]
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_verify_token_rejects_unknown_token():
    """No matching row in email_verification_tokens — the helper sees
    ``None`` from the first scalar_one_or_none and raises."""
    from app.services.email_verification import verify_token

    db = _mock_db_returning(None)
    with pytest.raises(HTTPException) as exc:
        await verify_token(db, "definitely-not-a-real-token", None)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_verify_token_rejects_used_token():
    """A row whose used_at is already set must be rejected."""
    import datetime as _dt
    from unittest.mock import MagicMock

    from app.services.email_verification import verify_token

    used = MagicMock(
        used_at=_dt.datetime.now(_dt.UTC),
        expires_at=_dt.datetime.now(_dt.UTC) + _dt.timedelta(minutes=5),
    )
    db = _mock_db_returning(used)
    with pytest.raises(HTTPException) as exc:
        await verify_token(db, "fake-token", None)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_verify_token_rejects_expired_token():
    """A row whose expires_at is in the past must be rejected."""
    import datetime as _dt
    from unittest.mock import MagicMock

    from app.services.email_verification import verify_token

    expired = MagicMock(used_at=None, expires_at=_dt.datetime.now(_dt.UTC) - _dt.timedelta(minutes=5))
    db = _mock_db_returning(expired)
    with pytest.raises(HTTPException) as exc:
        await verify_token(db, "fake-token", None)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_verify_token_rejects_when_user_missing():
    """Token row exists but the user is gone — generic 400."""
    import datetime as _dt
    import uuid as _uuid
    from unittest.mock import MagicMock

    from app.services.email_verification import verify_token

    valid_row = MagicMock(
        used_at=None,
        expires_at=_dt.datetime.now(_dt.UTC) + _dt.timedelta(minutes=5),
        user_id=_uuid.uuid4(),
    )
    db = _mock_db_returning(valid_row, None)
    with pytest.raises(HTTPException) as exc:
        await verify_token(db, "fake-token", None)
    assert exc.value.status_code == 400


# ══════════════════════════════════════════════════════════════════════
# deps.get_current_user: token-shape rejections (pre-DB)
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_current_user_rejects_missing_cookie():
    from app.api.deps import get_current_user

    with pytest.raises(HTTPException) as exc:
        await get_current_user(access_token=None, db=None)  # type: ignore[arg-type]
    assert exc.value.status_code == 401
    assert "Not authenticated" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_get_current_user_rejects_garbage_token():
    """A non-decodable string falls into the bare-Except branch and
    becomes ``Invalid or expired token`` 401."""
    from app.api.deps import get_current_user

    with pytest.raises(HTTPException) as exc:
        await get_current_user(access_token="not-a-real-jwt", db=None)  # type: ignore[arg-type]
    assert exc.value.status_code == 401
    assert "Invalid or expired token" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_get_current_user_rejects_refresh_token_in_access_cookie():
    """A token whose ``type`` claim is "refresh" must be rejected even
    though it's structurally valid."""
    from app.api.deps import get_current_user
    from app.core.security import create_refresh_token

    refresh_str, _tid = create_refresh_token(uuid.uuid4(), uuid.uuid4())
    with pytest.raises(HTTPException) as exc:
        await get_current_user(access_token=refresh_str, db=None)  # type: ignore[arg-type]
    assert exc.value.status_code == 401


# ══════════════════════════════════════════════════════════════════════
# deps.require_role: role-check returns + 403 raise
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_require_role_admits_matching_role():
    from unittest.mock import MagicMock

    from app.api.deps import require_role
    from app.models.enums import UserRole

    user = MagicMock(role=UserRole.owner)
    checker = require_role("owner", "co_parent")
    assert await checker(user=user) is user


@pytest.mark.asyncio
async def test_require_role_rejects_non_matching_role():
    from unittest.mock import MagicMock

    from app.api.deps import require_role
    from app.models.enums import UserRole

    user = MagicMock(role=UserRole.observer)
    checker = require_role("owner")
    with pytest.raises(HTTPException) as exc:
        await checker(user=user)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_require_role_handles_str_role_attribute():
    """Some legacy fixtures store role as a plain string. The factory
    normalises via ``.value if hasattr`` so it works either way."""
    from unittest.mock import MagicMock

    from app.api.deps import require_role

    user = MagicMock(spec=["role"])
    user.role = "owner"
    checker = require_role("owner")
    assert await checker(user=user) is user


# ══════════════════════════════════════════════════════════════════════
# deps.require_active_subscription: branch coverage on subscription state
# ══════════════════════════════════════════════════════════════════════


def _mock_household(status_value, trial_ends_at=None):
    from unittest.mock import MagicMock

    return MagicMock(subscription_status=status_value, trial_ends_at=trial_ends_at)


def _mock_db_with_household(hh):
    from unittest.mock import AsyncMock, MagicMock

    result = MagicMock(scalar_one_or_none=MagicMock(return_value=hh))
    db = AsyncMock()
    db.execute = AsyncMock(return_value=result)
    return db


@pytest.mark.asyncio
async def test_require_active_subscription_admits_active():
    from unittest.mock import MagicMock

    from app.api.deps import require_active_subscription

    user = MagicMock(household_id=uuid.uuid4())
    db = _mock_db_with_household(_mock_household("active"))
    assert await require_active_subscription(user=user, db=db) is user


@pytest.mark.asyncio
async def test_require_active_subscription_admits_trialing():
    from unittest.mock import MagicMock

    from app.api.deps import require_active_subscription

    user = MagicMock(household_id=uuid.uuid4())
    db = _mock_db_with_household(_mock_household("trialing"))
    assert await require_active_subscription(user=user, db=db) is user


@pytest.mark.asyncio
async def test_require_active_subscription_admits_future_trial_window():
    """A household whose status hasn't been refreshed but is still
    inside the trial window must still be admitted."""
    from datetime import UTC, datetime, timedelta
    from unittest.mock import MagicMock

    from app.api.deps import require_active_subscription

    user = MagicMock(household_id=uuid.uuid4())
    db = _mock_db_with_household(_mock_household("trial", datetime.now(UTC) + timedelta(days=3)))
    assert await require_active_subscription(user=user, db=db) is user


@pytest.mark.asyncio
async def test_require_active_subscription_rejects_canceled():
    from unittest.mock import MagicMock

    from app.api.deps import require_active_subscription

    user = MagicMock(household_id=uuid.uuid4())
    db = _mock_db_with_household(_mock_household("canceled"))
    with pytest.raises(HTTPException) as exc:
        await require_active_subscription(user=user, db=db)
    assert exc.value.status_code == 402
    assert exc.value.detail["error"] == "subscription_required"
    assert exc.value.detail["status"] == "canceled"
    assert exc.value.detail["checkout_url"] == "/billing/checkout"


@pytest.mark.asyncio
async def test_require_active_subscription_rejects_expired_trial():
    """trial_ends_at in the past + status not in (active, trialing)."""
    from datetime import UTC, datetime, timedelta
    from unittest.mock import MagicMock

    from app.api.deps import require_active_subscription

    user = MagicMock(household_id=uuid.uuid4())
    db = _mock_db_with_household(_mock_household("trial", datetime.now(UTC) - timedelta(days=1)))
    with pytest.raises(HTTPException) as exc:
        await require_active_subscription(user=user, db=db)
    assert exc.value.status_code == 402
    assert exc.value.detail["status"] == "trial"


@pytest.mark.asyncio
async def test_require_active_subscription_rejects_when_household_missing():
    """No row for the user's household_id — defensive 402 with status
    ``unknown`` so the frontend renders the upgrade banner instead of
    leaking a 500."""
    from unittest.mock import MagicMock

    from app.api.deps import require_active_subscription

    user = MagicMock(household_id=uuid.uuid4())
    db = _mock_db_with_household(None)
    with pytest.raises(HTTPException) as exc:
        await require_active_subscription(user=user, db=db)
    assert exc.value.status_code == 402
    assert exc.value.detail["status"] == "unknown"


# ══════════════════════════════════════════════════════════════════════
# get_db is the un-tenant-scoped session yielder used by unauthenticated
# routes. We can drive it without a real database by patching get_session.
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_get_db_yields_session_from_get_session(monkeypatch):
    from app.api import deps

    sentinel = object()

    async def _fake_get_session():
        yield sentinel

    monkeypatch.setattr(deps, "get_session", _fake_get_session)
    agen = deps.get_db()
    received = await agen.__anext__()
    assert received is sentinel


# ══════════════════════════════════════════════════════════════════════
# auth.py: the rate-limit-only branch in login + forgot_password
# ══════════════════════════════════════════════════════════════════════
#
# When fail-closed limiters trip (real Redis would refuse the consume
# after the cap), the handlers raise 429 before touching the DB. We
# patch check_and_consume with a coroutine that returns
# ``(False, retry_seconds)`` and assert the early 429.


@pytest.mark.asyncio
async def test_login_returns_429_when_rate_limit_blocks(monkeypatch):
    from fastapi import Request

    from app.api import auth as auth_module
    from app.schemas.auth import LoginRequest

    async def _block(*_args, **_kwargs):
        return False, 30

    monkeypatch.setattr(auth_module, "check_and_consume", _block)

    request = Request(
        scope={
            "type": "http",
            "method": "POST",
            "path": "/login",
            "headers": [],
            "client": ("1.2.3.4", 0),
            "app": MagicMock(state=MagicMock(redis=None)),
        }
    )
    body = LoginRequest(email="who@example.com", password="whatever-long-enough")

    with pytest.raises(HTTPException) as exc:
        await auth_module.login(body=body, request=request, response=MagicMock(), db=MagicMock())
    assert exc.value.status_code == 429
    assert exc.value.headers["Retry-After"] == "30"


@pytest.mark.asyncio
async def test_forgot_password_returns_429_when_rate_limit_blocks(monkeypatch):
    from fastapi import Request

    from app.api import auth as auth_module

    async def _block(*_args, **_kwargs):
        return False, 60

    monkeypatch.setattr(auth_module, "check_and_consume", _block)

    request = Request(
        scope={
            "type": "http",
            "method": "POST",
            "path": "/forgot-password",
            "headers": [],
            "client": ("1.2.3.4", 0),
            "app": MagicMock(state=MagicMock(redis=None)),
        }
    )
    body = auth_module.ForgotPasswordRequest(email="anyone@example.com")

    with pytest.raises(HTTPException) as exc:
        await auth_module.forgot_password(body=body, request=request, db=MagicMock())
    assert exc.value.status_code == 429
    assert exc.value.headers["Retry-After"] == "60"


# ══════════════════════════════════════════════════════════════════════
# billing.py: handlers are thin pass-throughs to app.services.billing.
# Patching the service functions lets us drive the route logic — happy
# paths, 503-when-unconfigured, webhook signature errors — without a
# database or a real Stripe key.
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_billing_subscribe_returns_checkout_url(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    monkeypatch.setattr(billing_module, "create_checkout_session", AsyncMock(return_value="https://stripe.test/co"))

    db = MagicMock()
    db.commit = AsyncMock()
    user = MagicMock(household_id=uuid.uuid4(), email="x@y.com")

    out = await billing_module.subscribe(body=None, db=db, user=user)
    assert out == {"checkout_url": "https://stripe.test/co"}
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_billing_subscribe_returns_503_when_not_configured(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    monkeypatch.setattr(billing_module, "create_checkout_session", AsyncMock(return_value=None))
    user = MagicMock(household_id=uuid.uuid4(), email="x@y.com")

    with pytest.raises(HTTPException) as exc:
        await billing_module.subscribe(body=None, db=MagicMock(), user=user)
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_billing_subscribe_passes_explicit_urls(monkeypatch):
    """When the body carries success_url / cancel_url they get forwarded
    to the service. Locks down the kwargs so a future refactor can't
    silently drop them."""
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    spy = AsyncMock(return_value="https://stripe.test/co")
    monkeypatch.setattr(billing_module, "create_checkout_session", spy)

    db = MagicMock()
    db.commit = AsyncMock()
    user = MagicMock(household_id=uuid.uuid4(), email="x@y.com")
    body = billing_module.CheckoutBody(success_url="https://m.app/ok", cancel_url="https://m.app/x")

    await billing_module.subscribe(body=body, db=db, user=user)
    spy.assert_awaited_once()
    kwargs = spy.await_args.kwargs
    assert kwargs["success_url"] == "https://m.app/ok"
    assert kwargs["cancel_url"] == "https://m.app/x"


@pytest.mark.asyncio
async def test_billing_status_returns_service_payload(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    payload = {"status": "active", "trial_ends_at": None}
    monkeypatch.setattr(billing_module, "get_subscription_status", AsyncMock(return_value=payload))

    user = MagicMock(household_id=uuid.uuid4())
    out = await billing_module.status(db=MagicMock(), user=user)
    assert out is payload


@pytest.mark.asyncio
async def test_billing_cancel_returns_canceled_true_and_commits(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    monkeypatch.setattr(billing_module, "cancel_subscription", AsyncMock(return_value=True))

    db = MagicMock()
    db.commit = AsyncMock()
    user = MagicMock(household_id=uuid.uuid4())

    out = await billing_module.cancel(db=db, user=user)
    assert out == {"canceled": True}
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_billing_cancel_returns_canceled_false_without_commit(monkeypatch):
    """When the service reports failure, we must NOT commit (nothing to
    persist) and the response must reflect the failure honestly."""
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    monkeypatch.setattr(billing_module, "cancel_subscription", AsyncMock(return_value=False))

    db = MagicMock()
    db.commit = AsyncMock()
    user = MagicMock(household_id=uuid.uuid4())

    out = await billing_module.cancel(db=db, user=user)
    assert out == {"canceled": False}
    db.commit.assert_not_called()


@pytest.mark.asyncio
async def test_billing_portal_returns_url(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    monkeypatch.setattr(billing_module, "create_portal_session", AsyncMock(return_value="https://stripe.test/portal"))
    user = MagicMock(household_id=uuid.uuid4())

    out = await billing_module.portal(body=None, db=MagicMock(), user=user)
    assert out == {"portal_url": "https://stripe.test/portal"}


@pytest.mark.asyncio
async def test_billing_portal_returns_503_when_unavailable(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    monkeypatch.setattr(billing_module, "create_portal_session", AsyncMock(return_value=None))
    user = MagicMock(household_id=uuid.uuid4())

    with pytest.raises(HTTPException) as exc:
        await billing_module.portal(body=None, db=MagicMock(), user=user)
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_billing_portal_forwards_return_url(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api import billing as billing_module

    spy = AsyncMock(return_value="https://stripe.test/portal")
    monkeypatch.setattr(billing_module, "create_portal_session", spy)
    user = MagicMock(household_id=uuid.uuid4())
    body = billing_module.PortalBody(return_url="https://m.app/back")

    await billing_module.portal(body=body, db=MagicMock(), user=user)
    assert spy.await_args.kwargs["return_url"] == "https://m.app/back"


@pytest.mark.asyncio
async def test_billing_webhook_happy_path(monkeypatch):
    from unittest.mock import AsyncMock

    from fastapi import Request

    from app.api import billing as billing_module

    monkeypatch.setattr(billing_module, "handle_webhook", AsyncMock(return_value={"processed": True}))

    async def _body():
        return b'{"type": "fake.event"}'

    request = MagicMock(spec=Request)
    request.body = _body
    request.headers = {"stripe-signature": "test-sig"}

    db = MagicMock()
    db.commit = AsyncMock()

    out = await billing_module.webhook(request=request, db=db)
    assert out == {"processed": True}
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_billing_webhook_translates_value_error_to_400(monkeypatch):
    """Bad Stripe signatures bubble up as ValueError from the service;
    the route turns them into a 400 with the message preserved so we
    don't reflect raw stack traces back to a hostile caller."""
    from unittest.mock import AsyncMock

    from fastapi import Request

    from app.api import billing as billing_module

    monkeypatch.setattr(
        billing_module,
        "handle_webhook",
        AsyncMock(side_effect=ValueError("invalid signature")),
    )

    async def _body():
        return b"{}"

    request = MagicMock(spec=Request)
    request.body = _body
    request.headers = {"stripe-signature": "bad"}

    with pytest.raises(HTTPException) as exc:
        await billing_module.webhook(request=request, db=MagicMock())
    assert exc.value.status_code == 400
    assert "invalid signature" in str(exc.value.detail)


# ══════════════════════════════════════════════════════════════════════
# deps.require_permission + require_child_access: body coverage with
# patched check_permission / mocked Child queries.
# ══════════════════════════════════════════════════════════════════════


@pytest.mark.asyncio
async def test_require_permission_admits_when_check_returns_true(monkeypatch):
    """The factory's inner checker calls
    ``app.core.permissions.check_permission`` and admits the user when
    that returns True."""
    from unittest.mock import AsyncMock

    from app.api.deps import require_permission
    from app.core import permissions as permissions_module

    monkeypatch.setattr(permissions_module, "check_permission", AsyncMock(return_value=True))
    user = MagicMock()
    checker = require_permission("plans.create")
    assert await checker(user=user, db=MagicMock()) is user


@pytest.mark.asyncio
async def test_require_permission_rejects_when_check_returns_false(monkeypatch):
    from unittest.mock import AsyncMock

    from app.api.deps import require_permission
    from app.core import permissions as permissions_module

    monkeypatch.setattr(permissions_module, "check_permission", AsyncMock(return_value=False))
    user = MagicMock()
    checker = require_permission("plans.create")
    with pytest.raises(HTTPException) as exc:
        await checker(user=user, db=MagicMock())
    assert exc.value.status_code == 403
    assert "plans.create" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_require_child_access_returns_child_when_present():
    """Happy path: the household-scoped query returns a Child row, the
    role isn't observer, no linked-learner constraint — return the
    Child so the route handler can use it directly."""
    from unittest.mock import AsyncMock

    from app.api.deps import require_child_access
    from app.models.enums import UserRole

    child_id = uuid.uuid4()
    user = MagicMock(
        household_id=uuid.uuid4(),
        role=UserRole.owner,
        linked_child_id=None,
    )
    fake_child = MagicMock(id=child_id)
    result = MagicMock(scalar_one_or_none=MagicMock(return_value=fake_child))
    db = AsyncMock()
    db.execute = AsyncMock(return_value=result)

    checker = require_child_access("read")
    out = await checker(child_id=child_id, user=user, db=db)
    assert out is fake_child


@pytest.mark.asyncio
async def test_require_child_access_returns_404_when_no_row():
    """Cross-household access (or unknown id) is a 404 — never leak
    existence with a 403."""
    from unittest.mock import AsyncMock

    from app.api.deps import require_child_access
    from app.models.enums import UserRole

    user = MagicMock(household_id=uuid.uuid4(), role=UserRole.owner, linked_child_id=None)
    result = MagicMock(scalar_one_or_none=MagicMock(return_value=None))
    db = AsyncMock()
    db.execute = AsyncMock(return_value=result)

    checker = require_child_access("read")
    with pytest.raises(HTTPException) as exc:
        await checker(child_id=uuid.uuid4(), user=user, db=db)
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_require_child_access_blocks_observer_writes():
    """Observers can read but never write."""
    from unittest.mock import AsyncMock

    from app.api.deps import require_child_access
    from app.models.enums import UserRole

    child_id = uuid.uuid4()
    user = MagicMock(household_id=uuid.uuid4(), role=UserRole.observer, linked_child_id=None)
    result = MagicMock(scalar_one_or_none=MagicMock(return_value=MagicMock(id=child_id)))
    db = AsyncMock()
    db.execute = AsyncMock(return_value=result)

    checker = require_child_access("write")
    with pytest.raises(HTTPException) as exc:
        await checker(child_id=child_id, user=user, db=db)
    assert exc.value.status_code == 403
    assert "Observers" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_require_child_access_blocks_other_learners_for_self_learner():
    """A user with linked_child_id set can only touch their own child
    record; any other id must 403."""
    from unittest.mock import AsyncMock

    from app.api.deps import require_child_access
    from app.models.enums import UserRole

    own_child_id = uuid.uuid4()
    sibling_id = uuid.uuid4()
    user = MagicMock(
        household_id=uuid.uuid4(),
        role=UserRole.co_parent,
        linked_child_id=own_child_id,
    )
    result = MagicMock(scalar_one_or_none=MagicMock(return_value=MagicMock(id=sibling_id)))
    db = AsyncMock()
    db.execute = AsyncMock(return_value=result)

    checker = require_child_access("read")
    with pytest.raises(HTTPException) as exc:
        await checker(child_id=sibling_id, user=user, db=db)
    assert exc.value.status_code == 403
    assert "Not authorized for this learner" in str(exc.value.detail)
