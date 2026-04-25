"""Email-verification token issuance and consumption.

The plaintext token (a 32-byte URL-safe random string) is delivered
to the user via email. Only its SHA-256 hex digest is persisted, so a
DB leak does not let an attacker mint verified accounts. Every token
expires after ``TOKEN_TTL_MINUTES`` and can be redeemed exactly once.

Audit logs (``AuditAction.email_verification_issued`` and
``email_verification_succeeded``) record the issuance and consumption
moments so we can correlate suspicious activity (e.g. a successful
verification far from where the token was issued).
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


async def issue_token(
    db: AsyncSession,
    user: User,
    request: Request | None = None,
) -> str:
    """Issue a fresh verification token. Returns the plaintext value
    so the caller can drop it into the verification URL."""
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
    """Consume a verification token and mark the user verified.

    All failure modes raise the same generic 400 so an attacker can't
    distinguish "expired" from "unknown" from "already used" by
    timing or message content.
    """
    generic = HTTPException(status_code=400, detail="Invalid or expired token")
    if not plaintext_token:
        raise generic

    result = await db.execute(
        select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == _hash(plaintext_token)
        )
    )
    token = result.scalar_one_or_none()
    if (
        not token
        or token.used_at is not None
        or token.expires_at < datetime.now(UTC)
    ):
        raise generic

    result = await db.execute(select(User).where(User.id == token.user_id))
    user = result.scalar_one_or_none()
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
