"""Shared FastAPI dependencies."""

import uuid
from typing import Literal

from fastapi import Cookie, Depends, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session, set_tenant
from app.core.security import decode_token
from app.models.enums import UserRole
from app.models.identity import Child, User

AccessMode = Literal["read", "write"]


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


def require_permission(permission: str, scope_type: str | None = None):
    """FastAPI dependency that checks a granular permission.

    Owners always pass. Other roles need an explicit UserPermission grant.
    """

    async def checker(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> User:
        from app.core.permissions import check_permission

        has_perm = await check_permission(db, user, permission, scope_type)
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission}",
            )
        return user

    return checker


def require_child_access(mode: AccessMode = "read"):
    """Factory: returns a FastAPI dependency that enforces per-child access.

    Pattern matches :func:`require_permission`. Wire it onto any
    learner-scoped route::

        child: Child = Depends(require_child_access("read"))   # GET
        child: Child = Depends(require_child_access("write"))  # POST/PUT/PATCH/DELETE

    The returned :class:`Child` row is the validated, household-scoped
    record — the surrounding handler can use it directly and skip
    the legacy ``_get_child_or_404`` lookup.

    Trust-boundary order:

    1. Tenant isolation. A child outside the user's household is a
       404 — never leak existence.
    2. Observer write block. ``UserRole.observer`` is read-only.
    3. Linked-learner constraint. A user with ``linked_child_id`` set
       can only touch that child; any other id is a 403.
    """

    async def checker(
        child_id: uuid.UUID = Path(...),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> Child:
        result = await db.execute(
            select(Child).where(
                Child.id == child_id,
                Child.household_id == user.household_id,
            )
        )
        child = result.scalar_one_or_none()
        if not child:
            raise HTTPException(status_code=404, detail="Child not found")

        if mode == "write" and user.role == UserRole.observer:
            raise HTTPException(
                status_code=403,
                detail="Observers cannot modify child records",
            )

        if user.linked_child_id is not None and child_id != user.linked_child_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized for this learner",
            )

        return child

    return checker


async def require_active_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Gate: require active or trialing subscription."""
    from datetime import UTC, datetime

    from app.models.identity import Household

    result = await db.execute(select(Household).where(Household.id == user.household_id))
    hh = result.scalar_one_or_none()
    if not hh:
        raise HTTPException(status_code=402, detail="Your subscription is inactive. Visit /billing to resubscribe.")

    if hh.subscription_status in ("active", "trialing"):
        return user

    if hh.trial_ends_at and hh.trial_ends_at > datetime.now(UTC):
        return user

    raise HTTPException(status_code=402, detail="Your subscription is inactive. Visit /billing to resubscribe.")
