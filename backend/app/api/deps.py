"""Shared FastAPI dependencies."""

import logging
import re
import uuid
from typing import Literal

from fastapi import Cookie, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session, set_tenant
from app.core.security import decode_token
from app.models.enums import UserRole
from app.models.identity import Child, User

logger = logging.getLogger(__name__)

AccessMode = Literal["read", "write"]

# Module-level flag so the dev-bypass warning fires at most once per
# worker process. The Settings load already gates ``DEV_BYPASS_SUBSCRIPTION``
# against production via the config validator, so the only thing left to
# do at request time is log a visible reminder and short-circuit the gate.
_bypass_warning_logged: bool = False


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
        # Tokens minted before the scope claim existed default to
        # parent scope so existing sessions keep working.
        token_scope = payload.get("scope", "parent")
        raw_child_id = payload.get("child_id")
        token_child_id = uuid.UUID(raw_child_id) if raw_child_id else None
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
    # Transient (non-mapped) attributes so downstream dependencies can
    # enforce kid-mode scope without re-decoding the token. sub stays
    # the parent user id even under child scope; the scope and bound
    # child are what change. setattr keeps them out of the mapped
    # column namespace.
    setattr(user, "token_scope", token_scope)  # noqa: B010
    setattr(user, "token_child_id", token_child_id)  # noqa: B010
    return user


def require_role(*roles: str):
    async def check_role(user: User = Depends(get_current_user)) -> User:
        # A child-scoped token can never satisfy a parent/admin role
        # check, regardless of the role baked into the token.
        if getattr(user, "token_scope", "parent") == "child":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="child_session_forbidden",
            )
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
    2. Kid-mode binding. A child-scoped token is bound to exactly one
       child_id; any other child is a 403. Write mode for the bound
       child stays permitted (attempt/learning endpoints), consistent
       with the existing AccessMode semantics below.
    3. Observer write block. ``UserRole.observer`` is read-only.
    4. Linked-learner constraint. A user with ``linked_child_id`` set
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

        if getattr(user, "token_scope", "parent") == "child" and child_id != getattr(user, "token_child_id", None):
            raise HTTPException(
                status_code=403,
                detail="child_session_forbidden",
            )

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


async def require_verified_email(
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Router-level gate: an authenticated account must be verified.

    Applied in main.py to every surface that creates or reads child
    data, per the COPPA/GDPR posture: no child records until the
    parent has proven control of the contact address. Auth, billing,
    usage, feedback, and the verification flow itself stay ungated so
    an unverified user can verify, pay, export, or leave.

    Requests without a (valid) token pass through untouched: each
    route's own auth dependency still returns its usual 401, and the
    few deliberately public routes under gated routers (e.g. the
    compliance states reference list) stay public. Nothing is loosened
    for child data because every child-data route requires auth, and
    any authenticated-but-unverified caller is rejected here with a
    stable token the frontend maps to the verification banner.
    """
    if not access_token:
        return
    try:
        user = await get_current_user(access_token=access_token, db=db)
    except HTTPException:
        return
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="email_not_verified",
        )


# Paths a family in restricted/canceled dunning keeps, because losing
# payment must never mean losing reach to their own data. The list is
# the data-stewardship surface and nothing else, following the
# subscription-exempt classification convention (see the header of
# api/spec_coverage.py): household deletion and its status live in
# auth.py, which is subscription-exempt in full, so they need no entry
# here. Matched against the request path so the family-record router's
# own require_active_subscription dependency opens for exactly these
# routes without loosening any other gated router.
_DUNNING_DATA_ACCESS_PATTERNS = (
    # Family Record read: the cumulative evidence-backed record.
    re.compile(r"/children/[0-9a-fA-F-]+/family-record$"),
    # Sealed data export: build and download a complete bundle.
    re.compile(r"/children/[0-9a-fA-F-]+/family-record/export$"),
    # Prior exports list: re-reach bundles already issued.
    re.compile(r"/family-record/exports$"),
)


def _is_dunning_data_access_path(path: str) -> bool:
    return any(p.search(path) for p in _DUNNING_DATA_ACCESS_PATTERNS)


async def require_active_subscription(
    request: Request,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Gate: require active or trialing subscription.

    Pass-through statuses: ``active``, ``trialing`` (and households
    still inside their trial window even if the recorded status hasn't
    been refreshed yet). Every other status (``canceled``, ``past_due``,
    ``paused``, ``incomplete``, ``incomplete_expired``, ``unpaid``, or
    anything unrecognised) is rejected with a structured 402 the
    frontend can branch on to render the upgrade banner.

    Dunning (failed-payment recovery, services/billing.py):

    - ``grace`` passes like an active subscription: the first seven
      days after a payment failure change nothing for the family.
    - ``restricted`` and ``canceled`` are inactive, except for the
      data-stewardship carve-outs in _DUNNING_DATA_ACCESS_PATTERNS
      (family record read, sealed export, prior exports), which stay
      open so a payment problem can never wall a family off from
      their own records.

    Non-dunning states keep the exact pre-dunning semantics.

    Local-dev escape hatch: when ``settings.DEV_BYPASS_SUBSCRIPTION`` is
    true (set in docker-compose.override.yml, never in prod/staging),
    every household is treated as having an active subscription so
    developers can exercise premium features without a real Stripe
    subscription. The config layer refuses to boot if this flag is true
    in production or staging, so the check here is safe at request time.
    """
    global _bypass_warning_logged
    if settings.DEV_BYPASS_SUBSCRIPTION:
        if not _bypass_warning_logged:
            logger.warning(
                "DEV_BYPASS_SUBSCRIPTION is active. All households treated as having "
                "an active premium subscription. This MUST NOT be set in staging or "
                "production. Configured via docker-compose.override.yml."
            )
            _bypass_warning_logged = True
        return user

    from datetime import UTC, datetime

    from app.models.identity import Household

    result = await db.execute(select(Household).where(Household.id == user.household_id))
    hh = result.scalar_one_or_none()
    current_status = hh.subscription_status if hh else "unknown"
    dunning_state = getattr(hh, "dunning_state", "none") if hh else "none"

    if hh is not None:
        if hh.subscription_status in ("active", "trialing"):
            return user
        if hh.trial_ends_at and hh.trial_ends_at > datetime.now(UTC):
            return user
        if dunning_state == "grace":
            return user
        if dunning_state in ("restricted", "canceled") and _is_dunning_data_access_path(request.url.path):
            return user

    raise HTTPException(
        status_code=402,
        detail={
            "error": "subscription_required",
            "status": current_status,
            "dunning_state": dunning_state,
            "checkout_url": "/billing/checkout",
        },
    )


async def require_native_curriculum_access(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Gate: the user's household must hold the native-curriculum entitlement.

    Gates the native-library curriculum generation/materialization path (the
    "Approve and Create" / generate-year-plan endpoints that fire the NATIVE
    provider when API keys are blank). The entitlement
    (``Household.native_curriculum_access``) defaults OFF, so the feature is
    dark for every household until it is flipped to true for a specific
    household — a data write, no code change or deploy.

    This is the security boundary: the check is enforced here, in a request
    dependency that resolves BEFORE the route handler body, so an unentitled
    request does nothing (no generation, no DB write). It holds against a
    crafted direct API call, not just the UI. Unentitled households get a
    structured 403 the frontend can branch on.
    """
    from app.models.identity import Household

    result = await db.execute(select(Household).where(Household.id == user.household_id))
    hh = result.scalar_one_or_none()
    if hh is None or not hh.native_curriculum_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "native_curriculum_access_required",
                "message": ("Native curriculum generation is not enabled for this household."),
            },
        )
    return user
