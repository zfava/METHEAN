"""Email verification: hashed, expiring, single-use tokens.

Replaces the prior (broken) scheme where the verification "token" was the
user's UUID. The plaintext token is generated with `secrets.token_urlsafe`
and only the SHA-256 digest is stored at rest. Token rows are scoped to a
household via RLS through the users join (see migration 039).
"""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AuditAction
from app.models.identity import EmailVerificationToken, User
from app.models.operational import AuditLog

TOKEN_TTL_MINUTES = 60


def _hash(plaintext: str) -> str:
    return hashlib.sha256(plaintext.encode("utf-8")).hexdigest()


async def issue_token(db: AsyncSession, user: User, request: Request | None = None) -> str:
    """Mint a fresh verification token, persist its hash, audit, and return the plaintext."""
    plaintext = secrets.token_urlsafe(32)
    row = EmailVerificationToken(
        user_id=user.id,
        token_hash=_hash(plaintext),
        expires_at=datetime.now(UTC) + timedelta(minutes=TOKEN_TTL_MINUTES),
        ip_address=(request.client.host if request and request.client else None),
        user_agent=(request.headers.get("user-agent") if request else None),
    )
    db.add(row)
    await db.flush()
    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.email_verification_issued,
            resource_type="email_verification_token",
            resource_id=row.id,
        )
    )
    await db.flush()
    return plaintext


async def verify_token(
    db: AsyncSession,
    plaintext_token: str | None,
    request: Request | None = None,
) -> User:
    """Validate a plaintext token, mark the user verified, and burn the token.

    All failure modes raise the same generic 400 to deny token-existence
    oracles. `request` is accepted for symmetry with `issue_token`.
    """
    del request  # currently unused; reserved for future audit metadata
    generic = HTTPException(status_code=400, detail="Invalid or expired token")
    if not plaintext_token:
        raise generic
    result = await db.execute(
        select(EmailVerificationToken).where(EmailVerificationToken.token_hash == _hash(plaintext_token))
    )
    token = result.scalar_one_or_none()
    if not token or token.used_at is not None or token.expires_at < datetime.now(UTC):
        raise generic
    user_result = await db.execute(select(User).where(User.id == token.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise generic
    token.used_at = datetime.now(UTC)
    user.email_verified = True
    db.add(
        AuditLog(
            household_id=user.household_id,
            user_id=user.id,
            action=AuditAction.email_verification_succeeded,
            resource_type="email_verification_token",
            resource_id=token.id,
        )
    )
    await db.flush()
    return user
