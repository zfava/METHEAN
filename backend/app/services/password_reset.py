"""Password reset via email token."""

import secrets
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.models.identity import User
from app.services.email import send_email

# In-memory token store (production: use Redis or DB table)
_reset_tokens: dict[str, dict] = {}  # token -> { user_id, expires_at }


async def generate_reset_token(db: AsyncSession, email: str) -> bool:
    """Send password reset email. Returns True if email was sent (or would be)."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return True  # Don't leak whether email exists

    token = secrets.token_urlsafe(32)
    _reset_tokens[token] = {
        "user_id": str(user.id),
        "expires_at": datetime.now(UTC) + timedelta(hours=1),
    }

    reset_url = f"{settings.APP_URL}/auth/reset?token={token}"

    from app.services.email_templates import password_reset_email

    html = password_reset_email(reset_url)
    await send_email(user.email, "Reset your METHEAN password", html)
    return True


def verify_reset_token(token: str) -> str | None:
    """Verify token and return user_id if valid."""
    data = _reset_tokens.get(token)
    if not data:
        return None
    if datetime.now(UTC) > data["expires_at"]:
        del _reset_tokens[token]
        return None
    return data["user_id"]


async def reset_password(db: AsyncSession, token: str, new_password: str) -> bool:
    """Reset password using token."""
    user_id = verify_reset_token(token)
    if not user_id:
        return False

    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        return False

    user.password_hash = hash_password(new_password)
    del _reset_tokens[token]
    await db.flush()
    return True
