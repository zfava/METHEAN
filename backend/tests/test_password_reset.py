"""Tests for password reset flow."""

from datetime import UTC
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.identity import Household, User


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


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_generate_reset_token_sends_email(mock_email, db_session, reset_user):
    """Reset token generation sends an email."""
    from app.services.password_reset import generate_reset_token

    result = await generate_reset_token(db_session, reset_user.email)
    assert result is True
    mock_email.assert_called_once()
    args = mock_email.call_args
    assert args[0][0] == "reset@test.com"
    assert "Reset" in args[0][1] or "reset" in args[0][1]


@pytest.mark.asyncio
async def test_generate_reset_token_nonexistent_email(db_session):
    """Non-existent email doesn't raise (security: don't reveal email existence)."""
    from app.services.password_reset import generate_reset_token

    result = await generate_reset_token(db_session, "nobody@nowhere.com")
    assert result is True  # Always returns True


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_verify_reset_token_valid(mock_email, db_session, reset_user):
    """Valid token returns user_id."""
    from app.services.password_reset import _reset_tokens, generate_reset_token, verify_reset_token

    await generate_reset_token(db_session, reset_user.email)
    token = list(_reset_tokens.keys())[-1]
    user_id = verify_reset_token(token)
    assert user_id == str(reset_user.id)


@pytest.mark.asyncio
async def test_verify_reset_token_invalid():
    """Invalid token returns None."""
    from app.services.password_reset import verify_reset_token

    assert verify_reset_token("totally-bogus-token") is None


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_verify_reset_token_expired(mock_email, db_session, reset_user):
    """Expired token returns None."""
    from datetime import datetime

    from app.services.password_reset import _reset_tokens, generate_reset_token, verify_reset_token

    await generate_reset_token(db_session, reset_user.email)
    token = list(_reset_tokens.keys())[-1]
    _reset_tokens[token]["expires_at"] = datetime(2020, 1, 1, tzinfo=UTC)
    assert verify_reset_token(token) is None


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_success(mock_email, db_session, reset_user):
    """Successful password reset changes the hash."""
    from app.services.password_reset import _reset_tokens, generate_reset_token, reset_password

    await generate_reset_token(db_session, reset_user.email)
    token = list(_reset_tokens.keys())[-1]
    result = await reset_password(db_session, token, "newpassword456")
    assert result is True
    assert verify_password("newpassword456", reset_user.password_hash)


@pytest.mark.asyncio
@patch("app.services.password_reset.send_email", new_callable=AsyncMock, return_value=True)
async def test_reset_password_token_consumed(mock_email, db_session, reset_user):
    """Used token can't be reused."""
    from app.services.password_reset import _reset_tokens, generate_reset_token, reset_password

    await generate_reset_token(db_session, reset_user.email)
    token = list(_reset_tokens.keys())[-1]
    assert await reset_password(db_session, token, "newpassword456") is True
    assert await reset_password(db_session, token, "anotherpassword") is False


@pytest.mark.asyncio
async def test_forgot_password_api_returns_200(client):
    """POST /auth/forgot-password always returns 200."""
    resp = await client.post("/api/v1/auth/forgot-password", json={"email": "whatever@test.com"})
    assert resp.status_code == 200
    assert "message" in resp.json()
