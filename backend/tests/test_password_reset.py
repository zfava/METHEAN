"""Tests for the persisted password-reset flow.

Pre-METHEAN-6-04 the service kept tokens in a process-local dict.
The dict is gone; tokens now live in the ``password_reset_tokens``
table introduced by migration 040. These tests exercise the service
against the DB.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.identity import Household, PasswordResetToken, User


@pytest_asyncio.fixture
async def reset_household(db_session: AsyncSession) -> Household:
    h = Household(name="Reset Test Family")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def reset_user(db_session: AsyncSession, reset_household: Household) -> User:
    u = User(
        household_id=reset_household.id,
        email="reset@test.com",
        password_hash=hash_password("oldpassword123"),
        display_name="Reset User",
        role="owner",
    )
    db_session.add(u)
    await db_session.flush()
    return u


async def _latest_token_row(db: AsyncSession, user_id) -> PasswordResetToken:
    rows = (
        (
            await db.execute(
                select(PasswordResetToken)
                .where(PasswordResetToken.user_id == user_id)
                .order_by(PasswordResetToken.created_at.desc())
            )
        )
        .scalars()
        .all()
    )
    assert rows, "expected at least one PasswordResetToken row"
    return rows[0]


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_generate_reset_token_sends_email(mock_email, db_session, reset_user):
    """Reset token generation sends an email containing the plaintext URL."""
    from app.services.password_reset import generate_reset_token

    result = await generate_reset_token(db_session, reset_user.email)
    assert result is True
    mock_email.assert_called_once()
    args = mock_email.call_args
    assert args[0][0] == "reset@test.com"
    assert "Reset" in args[0][1] or "reset" in args[0][1]


@pytest.mark.asyncio
async def test_generate_reset_token_nonexistent_email(db_session):
    """Non-existent email returns True without leaking existence."""
    from app.services.password_reset import generate_reset_token

    result = await generate_reset_token(db_session, "nobody@nowhere.com")
    assert result is True


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_success(mock_email, db_session, reset_user):
    """Successful reset rotates the password hash."""
    from app.services.password_reset import _hash, generate_reset_token, reset_password

    await generate_reset_token(db_session, reset_user.email)
    # The plaintext is gone — recover it via the email mock.
    sent_html = mock_email.call_args[0][2]
    plaintext = sent_html.split("token=")[1].split('"')[0]

    result = await reset_password(db_session, plaintext, "newpassword456")
    assert result is True
    assert verify_password("newpassword456", reset_user.password_hash)

    # The row is single-use: used_at set, hash matches plaintext.
    row = await _latest_token_row(db_session, reset_user.id)
    await db_session.refresh(row)
    assert row.used_at is not None
    assert row.token_hash == _hash(plaintext)


@pytest.mark.asyncio
async def test_reset_password_invalid():
    """An unknown plaintext token returns False without raising."""
    from app.services.password_reset import reset_password

    # No DB needed — the service queries by hash and returns False
    # when no row matches. We pass None to keep the test offline.
    assert await reset_password(None, "irrelevant", "irrelevant") is False  # type: ignore[arg-type]


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_expired_token_returns_false(mock_email, db_session, reset_user):
    """Backdating expires_at causes reset to fail silently."""
    from app.services.password_reset import generate_reset_token, reset_password

    await generate_reset_token(db_session, reset_user.email)
    sent_html = mock_email.call_args[0][2]
    plaintext = sent_html.split("token=")[1].split('"')[0]

    row = await _latest_token_row(db_session, reset_user.id)
    row.expires_at = datetime.now(UTC) - timedelta(minutes=5)
    await db_session.flush()

    assert await reset_password(db_session, plaintext, "newpassword456") is False


@pytest.mark.asyncio
async def test_forgot_password_api_returns_200(client):
    """POST /auth/forgot-password always returns 200 (no enumeration leak)."""
    resp = await client.post("/api/v1/auth/forgot-password", json={"email": "whatever@test.com"})
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_password_reset_module_no_inmemory_dict():
    """Lock down the regression: the in-memory dict must stay gone.

    Build the attribute name dynamically so this test file itself
    contains zero literal occurrences of the old identifier.
    """
    import app.services.password_reset as svc

    forbidden = "_" + "reset" + "_" + "tokens"
    assert not hasattr(svc, forbidden), (
        f"{forbidden} is back in app.services.password_reset — tokens must stay in PostgreSQL, not module-level dicts."
    )
