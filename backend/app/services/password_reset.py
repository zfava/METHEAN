"""Password reset via email token, persisted in PostgreSQL.

The legacy implementation kept tokens in a process-local dict, so
under the production Gunicorn 4-worker setup the token issued by
worker A landed in worker A's memory and worker B (which served the
reset POST 3/4 of the time) couldn't find it. This module persists
hashed tokens to the ``password_reset_tokens`` table introduced in
migration 040, so any worker — and any replica — can redeem.

Failure modes for ``reset_password`` all return ``False``; the caller
is responsible for translating that into the generic 400 the API
already exposes. We never distinguish "expired" from "unknown" from
"already used" so an attacker can't enumerate by error message.

A successful reset also revokes every active refresh token for the
user (same UPDATE pattern as ``app.api.auth`` line 462) so a stolen
session can't survive the password rotation.
"""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password
from app.models.enums import AuditAction
from app.models.identity import PasswordResetToken, User
from app.models.operational import AuditLog, RefreshToken
from app.services.email import send_email

TOKEN_TTL_MINUTES = 60


def _hash(plaintext: str) -> str:
    return hashlib.sha256(plaintext.encode("utf-8")).hexdigest()


async def generate_reset_token(
    db: AsyncSession,
    email: str,
    request: Request | None = None,
) -> bool:
    """Issue a fresh reset token + send the reset email.

    Always returns True so callers can't infer whether the address is
    registered. When the email matches a real user, marks any prior
    active token used (the partial unique index would otherwise
    refuse the insert), persists the new hashed row, and dispatches
    the email.
    """
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return True

    now = datetime.now(UTC)
    # Mark any prior active token used so the partial unique index
    # admits the new row. A single transaction keeps the invariant
    # "at most one unused row per user" intact even under concurrency.
    await db.execute(
        update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
        .values(used_at=now)
    )

    plaintext = secrets.token_urlsafe(32)
    row = PasswordResetToken(
        user_id=user.id,
        token_hash=_hash(plaintext),
        expires_at=now + timedelta(minutes=TOKEN_TTL_MINUTES),
        ip_address=(request.client.host if request and request.client else None),
        user_agent=(request.headers.get("user-agent") if request else None),
    )
    db.add(row)
    await db.flush()

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.password_reset_requested,
            resource_type="password_reset_token",
            resource_id=row.id,
        )
    )
    await db.flush()

    reset_url = f"{settings.APP_URL}/auth/reset?token={plaintext}"

    from app.services.email_templates import password_reset_email

    html = password_reset_email(reset_url)
    await send_email(user.email, "Reset your METHEAN password", html)
    return True


async def reset_password(
    db: AsyncSession,
    plaintext_token: str,
    new_password: str,
    request: Request | None = None,
) -> bool:
    """Consume a reset token and rotate the user's password.

    Returns False on every failure path (unknown / expired / reused /
    user gone). On success: updates the password hash, marks the
    token used, revokes all active refresh tokens, and emits an audit
    log row.
    """
    if not plaintext_token:
        return False

    result = await db.execute(select(PasswordResetToken).where(PasswordResetToken.token_hash == _hash(plaintext_token)))
    token = result.scalar_one_or_none()
    if not token or token.used_at is not None or token.expires_at < datetime.now(UTC):
        return False

    result = await db.execute(select(User).where(User.id == token.user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False

    user.password_hash = hash_password(new_password)
    token.used_at = datetime.now(UTC)

    # Revoke every active refresh token so a stolen cookie can't
    # outlive the password rotation. Mirrors the pattern in
    # app.api.auth around line 462.
    await db.execute(
        update(RefreshToken)
        .where(
            RefreshToken.user_id == user.id,
            RefreshToken.is_revoked == False,  # noqa: E712 — SQL three-valued
        )
        .values(is_revoked=True)
    )

    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.password_reset_completed,
            resource_type="password_reset_token",
            resource_id=token.id,
        )
    )
    await db.flush()
    return True
