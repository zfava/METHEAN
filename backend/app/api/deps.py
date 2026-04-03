"""Shared FastAPI dependencies."""

import uuid

from fastapi import Cookie, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session, set_tenant
from app.core.security import decode_token
from app.models.identity import User


class PaginationParams:
    """Shared pagination dependency for list endpoints."""

    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(50, ge=1, le=200, description="Max records to return"),
    ):
        self.skip = skip
        self.limit = limit


async def get_db() -> AsyncSession:
    """Yield a database session without tenant scoping.

    Used by unauthenticated endpoints (register, login, health).
    """
    async for session in get_session():
        yield session


async def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Authenticate user from JWT cookie and activate RLS tenant scoping.

    After successful authentication, sets the PostgreSQL session variable
    app.current_household_id so that RLS policies filter all subsequent
    queries in this transaction to the user's household.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = decode_token(access_token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        user_id = uuid.UUID(payload["sub"])
        household_id = uuid.UUID(payload["hid"])
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # Set RLS tenant context BEFORE querying for the user.
    # This ensures even the user lookup is scoped (users table has RLS).
    # We need to begin a transaction for SET LOCAL to take effect.
    await db.connection()  # ensure we have a connection
    await set_tenant(db, household_id)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return user


def require_role(*roles: str):
    async def check_role(user: User = Depends(get_current_user)) -> User:
        role_val = user.role.value if hasattr(user.role, "value") else user.role
        if role_val not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return check_role
