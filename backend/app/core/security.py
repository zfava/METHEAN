"""JWT token management and password hashing."""

import uuid
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(
    user_id: uuid.UUID,
    household_id: uuid.UUID,
    role: str,
    scope: str = "parent",
    child_id: uuid.UUID | None = None,
    expires_minutes: int | None = None,
) -> str:
    """Mint an access token.

    scope is "parent" for normal sessions and "child" for kid-mode
    sessions. Child tokens keep the parent's user id as sub (so the
    session can be restored on exit) and carry the bound child in the
    child_id claim. Tokens minted before the scope claim existed decode
    as parent scope: consumers must default a missing scope to "parent".
    """
    now = datetime.now(UTC)
    minutes = expires_minutes if expires_minutes is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    payload = {
        "sub": str(user_id),
        "hid": str(household_id),
        "role": role,
        "type": "access",
        "scope": scope,
        "iat": now,
        "exp": now + timedelta(minutes=minutes),
    }
    if child_id is not None:
        payload["child_id"] = str(child_id)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(
    user_id: uuid.UUID,
    household_id: uuid.UUID,
    token_id: uuid.UUID | None = None,
) -> tuple[str, uuid.UUID]:
    now = datetime.now(UTC)
    tid = token_id or uuid.uuid4()
    payload = {
        "sub": str(user_id),
        "hid": str(household_id),
        "tid": str(tid),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, tid


def decode_token(token: str) -> dict:
    """Verify JWT, trying current key first, then previous key for rotation."""
    for secret in [settings.JWT_SECRET, settings.PREVIOUS_JWT_SECRET]:
        if not secret:
            continue
        try:
            return jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            continue
    raise jwt.InvalidTokenError("Token verification failed with all available keys")
