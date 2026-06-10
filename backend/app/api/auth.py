# subscription_exempt: login/registration/refresh must work without an active subscription
# See fix/methean6-08-subscription-gating for classification rationale.
"""Auth API endpoints: register, login, logout, refresh, kid-mode sessions."""

import hashlib
import re
import secrets
import uuid
from datetime import UTC, datetime, timedelta

import structlog
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.rate_limit import POLICIES, check_and_consume, client_ip, rate_limit
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.enums import UserRole
from app.models.identity import Household, User
from app.models.operational import RefreshToken
from app.schemas.auth import (
    InstitutionalRegisterRequest,
    InviteResponse,
    LoginRequest,
    MessageResponse,
    RefreshResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)

# /auth/invite is the institutional invite endpoint and uses a richer
# schema. /auth/household/invite is the family invite endpoint and
# uses the small local InviteRequest below. The two collided on the
# bare name "InviteRequest" — aliasing the institutional one keeps
# the local family schema as the canonical InviteRequest.
from app.schemas.auth import InviteRequest as InstitutionalInviteRequest

# Canonical deletion window lives next to the purge task so the
# endpoint and the eraser can never disagree about when data becomes
# unrecoverable.
from app.tasks.purge import DELETION_WINDOW_DAYS

router = APIRouter(prefix="/auth", tags=["auth"])
logger = structlog.get_logger()


def _set_cookie(response: Response, name: str, value: str, max_age: int) -> None:
    response.set_cookie(
        key=name,
        value=value,
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
        max_age=max_age,
        path="/",
    )


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit("register"))],
)
async def register(
    body: RegisterRequest,
    response: Response,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
    # Check if email already exists
    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create household
    household = Household(name=body.household_name, timezone=body.timezone)
    db.add(household)
    await db.flush()

    # Create user as owner
    user = User(
        household_id=household.id,
        email=body.email,
        password_hash=hash_password(body.password),
        display_name=body.display_name,
        role="owner",
    )
    db.add(user)
    await db.flush()

    # With no email provider configured, the verification email can
    # never be delivered and the verified-email gate would lock every
    # new account out of child data forever. Outside production (the
    # config validator requires RESEND_API_KEY in production) treat
    # such accounts as verified so local dev and CI keep working.
    if not settings.RESEND_API_KEY and not settings.is_production:
        user.email_verified = True

    # Auto-grant owner permissions
    from app.core.permissions import grant_role_permissions

    await grant_role_permissions(db, user.id, household.id, "owner", user.id)

    # Self-directed registration: the registering user is both governor
    # and learner. Flip the household into self_governed mode and create
    # a Child record that represents the user as a learner.
    if body.is_self_learner:
        household.governance_mode = "self_governed"
        household.organization_type = "self_directed"
        user.is_self_learner = True

        from app.models.identity import Child, ChildPreferences

        first_token = body.display_name.split()
        self_child = Child(
            household_id=household.id,
            first_name=first_token[0] if first_token else body.display_name,
        )
        db.add(self_child)
        await db.flush()

        # Child.preferences is a relationship, so preferences are stored
        # in their own row. 120 minutes matches the spec default.
        db.add(
            ChildPreferences(
                child_id=self_child.id,
                household_id=household.id,
                daily_duration_minutes=120,
            )
        )

        user.linked_child_id = self_child.id
        await db.flush()

    # Generate tokens
    access_token = create_access_token(user.id, household.id, "owner")
    refresh_token_str, token_id = create_refresh_token(user.id, household.id)

    # Store refresh token
    refresh_record = RefreshToken(
        id=token_id,
        user_id=user.id,
        household_id=household.id,
        token_hash=_hash_token(refresh_token_str),
        expires_at=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_record)

    # Set cookies
    _set_cookie(response, "access_token", access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    _set_cookie(
        response,
        "refresh_token",
        refresh_token_str,
        settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    # Issue an email-verification token + send the verification email.
    # Failures are swallowed so a downed email provider doesn't block
    # account creation; the user can request a fresh token via
    # /auth/resend-verification.
    try:
        from app.services.email import send_email
        from app.services.email_templates import email_verification_email
        from app.services.email_verification import issue_token

        verify_plaintext = await issue_token(db, user, request)
        verify_url = f"{settings.APP_URL}/auth/verify?token={verify_plaintext}"
        await send_email(
            user.email,
            "Verify your METHEAN email",
            email_verification_email(verify_url),
        )
    except Exception:
        pass

    return RegisterResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/register-institution",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_institution(
    body: InstitutionalRegisterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> RegisterResponse:
    """Bootstrap an institution: creates the household, the admin user,
    and returns auth tokens so the admin is immediately logged in.
    """
    existing = await db.execute(select(User).where(User.email == body.admin_email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    household = Household(
        name=body.organization_name,
        governance_mode="institution_governed",
        organization_type=body.organization_type,
    )
    db.add(household)
    await db.flush()

    user = User(
        household_id=household.id,
        email=body.admin_email,
        password_hash=hash_password(body.admin_password),
        display_name=body.admin_display_name,
        role="owner",
        institutional_role="department_admin",
    )
    db.add(user)
    await db.flush()

    # Same no-email-provider escape as /auth/register above.
    if not settings.RESEND_API_KEY and not settings.is_production:
        user.email_verified = True

    from app.core.permissions import grant_role_permissions

    await grant_role_permissions(db, user.id, household.id, "owner", user.id)

    access_token = create_access_token(user.id, household.id, "owner")
    refresh_token_str, token_id = create_refresh_token(user.id, household.id)

    refresh_record = RefreshToken(
        id=token_id,
        user_id=user.id,
        household_id=household.id,
        token_hash=_hash_token(refresh_token_str),
        expires_at=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_record)

    _set_cookie(response, "access_token", access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    _set_cookie(
        response,
        "refresh_token",
        refresh_token_str,
        settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    return RegisterResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


_INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE = {
    "instructor": "co_parent",
    "teaching_assistant": "observer",
    "student": "observer",
}


@router.post(
    "/invite",
    response_model=InviteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def invite_user(
    body: InstitutionalInviteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> InviteResponse:
    """Invite a user into an institution-governed household.

    Only department admins may invite. Instructors get co_parent-level
    grants, TAs and students get observer. Students also receive a
    Child record and a self-scoped view_progress grant so one student
    cannot read another student's data.
    """
    household = await db.get(Household, current_user.household_id)
    if not household or household.governance_mode != "institution_governed":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Institutional invites require an institution-governed household",
        )
    if current_user.institutional_role != "department_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only department admins can invite users",
        )
    if body.institutional_role not in _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown institutional role: {body.institutional_role}",
        )
    if body.institutional_role == "student" and not body.learner_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="learner_name is required when inviting a student",
        )

    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    household_role = _INSTITUTIONAL_ROLE_TO_HOUSEHOLD_ROLE[body.institutional_role]

    # Invited users get an unguessable random sentinel hash: nobody can
    # authenticate against it, including the inviter. The invitee gains
    # access only by completing the password-reset (set password) flow.
    # Never derive this from the email or any other guessable input.
    placeholder_password = hash_password(secrets.token_urlsafe(32))

    new_user = User(
        household_id=current_user.household_id,
        email=body.email,
        password_hash=placeholder_password,
        display_name=body.display_name,
        role=household_role,
        institutional_role=body.institutional_role,
    )
    db.add(new_user)
    await db.flush()

    linked_child_id: uuid.UUID | None = None
    if body.institutional_role == "student":
        from app.core.permissions import OBSERVER_PERMISSIONS
        from app.models.identity import Child, UserPermission

        student_child = Child(
            household_id=current_user.household_id,
            first_name=body.learner_name,
        )
        db.add(student_child)
        await db.flush()
        new_user.is_self_learner = True
        new_user.linked_child_id = student_child.id
        linked_child_id = student_child.id

        # Scope every observer permission to the student's own child so
        # students cannot read each other's data at the permission layer.
        for perm in OBSERVER_PERMISSIONS:
            db.add(
                UserPermission(
                    user_id=new_user.id,
                    household_id=current_user.household_id,
                    permission=perm,
                    scope_type="child",
                    scope_id=student_child.id,
                    granted_by=current_user.id,
                )
            )
        await db.flush()
    else:
        from app.core.permissions import grant_role_permissions

        await grant_role_permissions(db, new_user.id, current_user.household_id, household_role, current_user.id)

    return InviteResponse(
        id=new_user.id,
        email=new_user.email,
        display_name=new_user.display_name,
        institutional_role=new_user.institutional_role,
        linked_child_id=linked_child_id,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    # Rate-limit per (ip, email) so a single attacker can't brute-force
    # one account and a compromised IP can't lock out unrelated users.
    # Skip in test environments — see _rate_limiting_disabled().
    if settings.APP_ENV != "test":
        allowed, retry_after = await check_and_consume(
            getattr(request.app.state, "redis", None),
            POLICIES["login"],
            {"ip": client_ip(request, settings.TRUSTED_PROXIES), "email": body.email.lower()},
        )
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Too many login attempts",
                headers={"Retry-After": str(retry_after)},
            )

    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    # Update last login
    user.last_login_at = datetime.now(UTC)

    # Generate tokens
    access_token = create_access_token(user.id, user.household_id, user.role.value)
    refresh_token_str, token_id = create_refresh_token(user.id, user.household_id)

    # Store refresh token
    refresh_record = RefreshToken(
        id=token_id,
        user_id=user.id,
        household_id=user.household_id,
        token_hash=_hash_token(refresh_token_str),
        expires_at=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_record)

    # Set cookies
    _set_cookie(response, "access_token", access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    _set_cookie(
        response,
        "refresh_token",
        refresh_token_str,
        settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> RefreshResponse:
    # No cookie → no credentials presented → 403. Every other
    # rejection (bad type, malformed JWT, expired exp, unknown tid,
    # revoked row, hash mismatch, dead user) is 401: credentials
    # WERE presented and they failed authentication.
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No refresh token provided",
        )

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        token_id = uuid.UUID(payload["tid"])
        user_id = uuid.UUID(payload["sub"])
        household_id = uuid.UUID(payload["hid"])
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Look up the token record (regardless of revocation status).
    result = await db.execute(select(RefreshToken).where(RefreshToken.id == token_id))
    stored_token = result.scalar_one_or_none()

    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )

    # If the token record is already revoked, this is a replay of a
    # previously rotated token — i.e. token reuse.  Revoke ALL tokens
    # for the user because the old token may have been stolen.
    if stored_token.is_revoked:
        await db.execute(
            update(RefreshToken).where(RefreshToken.user_id == stored_token.user_id).values(is_revoked=True)
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token reuse detected",
        )

    # Verify hash matches (guards against forged token IDs)
    if stored_token.token_hash != _hash_token(refresh_token):
        await db.execute(
            update(RefreshToken).where(RefreshToken.user_id == stored_token.user_id).values(is_revoked=True)
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token reuse detected",
        )

    # Rotate: revoke old, issue new
    stored_token.is_revoked = True

    # Get user role
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Issue new tokens
    new_access = create_access_token(user_id, household_id, user.role.value)
    new_refresh_str, new_token_id = create_refresh_token(user_id, household_id)

    new_refresh_record = RefreshToken(
        id=new_token_id,
        user_id=user_id,
        household_id=household_id,
        token_hash=_hash_token(new_refresh_str),
        expires_at=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(new_refresh_record)

    # Set new cookies
    _set_cookie(response, "access_token", new_access, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    _set_cookie(
        response,
        "refresh_token",
        new_refresh_str,
        settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )

    return RefreshResponse(
        access_token=new_access,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    if refresh_token:
        try:
            payload = decode_token(refresh_token)
            token_id = uuid.UUID(payload["tid"])
            result = await db.execute(select(RefreshToken).where(RefreshToken.id == token_id))
            stored = result.scalar_one_or_none()
            if stored:
                stored.is_revoked = True
                # Persist the revocation so a stolen cookie can't be
                # replayed against /auth/refresh after logout. Commit
                # is inside the try block so any DB error is swallowed
                # together with the decode/lookup errors — logout must
                # never fail from the user's perspective.
                await db.commit()
        except Exception:
            pass  # Best-effort revocation

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return MessageResponse(message="Logged out successfully")


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


@router.put("/password")
async def change_password(
    body: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Change the current user's password."""
    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    user.password_hash = hash_password(body.new_password)
    await db.commit()
    return {"success": True}


# ══════════════════════════════════════════════════
# Kid-mode (child-scoped) sessions
# ══════════════════════════════════════════════════

# A child session can never outlive 12 hours, even if the configured
# access expiry is longer.
CHILD_SESSION_MAX_MINUTES = 12 * 60

# After this many consecutive failed exit attempts within the window,
# the PIN path is rejected (even with the correct PIN) and exit
# requires the full parent password.
PIN_ATTEMPT_LIMIT = 5
PIN_ATTEMPT_WINDOW_SECONDS = 15 * 60

_PIN_FORMAT = re.compile(r"^\d{4,8}$")


def _require_parent_scope(user: User) -> None:
    if getattr(user, "token_scope", "parent") != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="child_session_forbidden",
        )


def _exit_attempts_key(household_id: uuid.UUID) -> str:
    return f"kid_exit_attempts:{household_id}"


def _role_value(user: User) -> str:
    return user.role.value if hasattr(user.role, "value") else str(user.role)


class SetPinRequest(BaseModel):
    current_password: str
    new_pin: str


class ChildSessionEnterRequest(BaseModel):
    child_id: uuid.UUID


class ChildSessionExitRequest(BaseModel):
    pin: str | None = None
    password: str | None = None


@router.post("/pin")
async def set_parent_pin(
    body: SetPinRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Set or change the kid-mode exit PIN.

    Parent scope required; requires the current password; the PIN is 4
    to 8 digits and is hashed with the same utility as passwords. The
    PIN value itself is never logged anywhere.
    """
    from app.models.enums import GovernanceAction
    from app.services.governance import log_governance_event

    _require_parent_scope(user)
    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if not _PIN_FORMAT.fullmatch(body.new_pin):
        raise HTTPException(status_code=422, detail="PIN must be 4 to 8 digits")

    had_pin = user.parent_pin_hash is not None
    user.parent_pin_hash = hash_password(body.new_pin)
    await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.modify,
        "parent_pin_changed",
        user.id,
        reason="Kid-mode exit PIN changed" if had_pin else "Kid-mode exit PIN set",
        metadata={"had_pin": had_pin},
    )
    logger.info(
        "parent_pin_changed",
        user_id=str(user.id),
        household_id=str(user.household_id),
        had_pin=had_pin,
    )
    await db.commit()
    return {"success": True}


@router.post("/child-session/enter")
async def enter_child_session(
    body: ChildSessionEnterRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Swap the parent session for a child-scoped one (kid mode).

    Parent scope required: a child token cannot nest another child
    session. The child must belong to the caller's household,
    mirroring require_child_access semantics. The minted token keeps
    the parent user id as sub so exit can restore the session; only
    scope and child_id change.
    """
    from app.models.enums import GovernanceAction
    from app.models.identity import Child
    from app.services.governance import log_governance_event

    _require_parent_scope(user)

    result = await db.execute(
        select(Child).where(
            Child.id == body.child_id,
            Child.household_id == user.household_id,
        )
    )
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    if user.linked_child_id is not None and body.child_id != user.linked_child_id:
        raise HTTPException(status_code=403, detail="Not authorized for this learner")

    expires_minutes = min(settings.ACCESS_TOKEN_EXPIRE_MINUTES, CHILD_SESSION_MAX_MINUTES)
    access_token = create_access_token(
        user.id,
        user.household_id,
        _role_value(user),
        scope="child",
        child_id=child.id,
        expires_minutes=expires_minutes,
    )
    _set_cookie(response, "access_token", access_token, expires_minutes * 60)
    # Non-HttpOnly marker so the frontend can render kid mode without
    # an API call. Carries no authority: the HttpOnly token's scope
    # claim is what the server enforces.
    response.set_cookie(
        key="kid_mode",
        value="1",
        httponly=False,
        secure=settings.is_production,
        samesite="lax",
        max_age=expires_minutes * 60,
        path="/",
    )

    await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.modify,
        "child_session_entered",
        child.id,
        reason="Kid mode entered",
        metadata={"child_id": str(child.id), "expires_minutes": expires_minutes},
    )
    logger.info(
        "child_session_entered",
        user_id=str(user.id),
        household_id=str(user.household_id),
        child_id=str(child.id),
        expires_minutes=expires_minutes,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_minutes * 60,
        "scope": "child",
        "child_id": str(child.id),
    }


@router.post("/child-session/exit")
async def exit_child_session(
    body: ChildSessionExitRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Exit kid mode and restore the parent-scoped session.

    Validates the parent PIN (preferred when one is set) or the parent
    password (always accepted, and required once the PIN path is
    locked by too many consecutive failures). The child token kept the
    parent user id as sub, so the restored session is the original
    parent's.
    """
    from app.core.cache import cache_delete, cache_get, cache_set
    from app.models.enums import GovernanceAction
    from app.services.governance import log_governance_event

    attempts_key = _exit_attempts_key(user.household_id)
    attempts = int(await cache_get(attempts_key) or 0)
    pin_locked = attempts >= PIN_ATTEMPT_LIMIT

    async def record_failure(reason: str) -> None:
        await cache_set(attempts_key, attempts + 1, ttl_seconds=PIN_ATTEMPT_WINDOW_SECONDS)
        logger.warning(
            "child_session_exit_failed",
            user_id=str(user.id),
            household_id=str(user.household_id),
            reason=reason,
            consecutive_failures=attempts + 1,
        )

    verified_with: str | None = None
    if body.password is not None and (pin_locked or not user.parent_pin_hash or body.pin is None):
        # Password path: always available, and the only path while the
        # PIN is locked or no PIN is set.
        if verify_password(body.password, user.password_hash):
            verified_with = "password"
        else:
            await record_failure("password_mismatch")
            raise HTTPException(status_code=401, detail="Invalid PIN or password")
    elif body.pin is not None and user.parent_pin_hash:
        if pin_locked:
            raise HTTPException(status_code=403, detail="pin_locked_use_password")
        if verify_password(body.pin, user.parent_pin_hash):
            verified_with = "pin"
        else:
            await record_failure("pin_mismatch")
            raise HTTPException(status_code=401, detail="Invalid PIN or password")
    elif body.pin is not None:
        raise HTTPException(status_code=400, detail="pin_not_set")
    else:
        raise HTTPException(status_code=400, detail="pin_or_password_required")

    await cache_delete(attempts_key)

    exited_child_id = getattr(user, "token_child_id", None)
    access_token = create_access_token(user.id, user.household_id, _role_value(user))
    _set_cookie(response, "access_token", access_token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    response.delete_cookie("kid_mode", path="/")

    await log_governance_event(
        db,
        user.household_id,
        user.id,
        GovernanceAction.modify,
        "child_session_exited",
        exited_child_id or user.id,
        reason="Kid mode exited",
        metadata={
            "child_id": str(exited_child_id) if exited_child_id else None,
            "verified_with": verified_with,
        },
    )
    logger.info(
        "child_session_exited",
        user_id=str(user.id),
        household_id=str(user.household_id),
        child_id=str(exited_child_id) if exited_child_id else None,
        verified_with=verified_with,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "scope": "parent",
    }


@router.get("/me/notification-preferences")
async def get_notification_preferences(
    user: User = Depends(get_current_user),
) -> dict:
    """Get current user's notification preferences."""
    return user.notification_preferences or {
        "email_daily_summary": True,
        "email_milestones": True,
        "email_governance_alerts": True,
        "email_weekly_digest": True,
        "email_compliance_warnings": True,
    }


@router.put("/me/notification-preferences")
async def update_notification_preferences(
    body: dict,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Update notification preferences."""
    allowed = {
        "email_daily_summary",
        "email_milestones",
        "email_governance_alerts",
        "email_weekly_digest",
        "email_compliance_warnings",
    }
    current = dict(user.notification_preferences or {})
    for key, val in body.items():
        if key in allowed and isinstance(val, bool):
            current[key] = val
    user.notification_preferences = current
    await db.commit()
    return current


# ── Password Reset ──


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


@router.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Send password reset email."""
    from app.services.password_reset import generate_reset_token

    # Per-(ip,email) hourly cap. The dependency form can't read the
    # body, so the check runs in-handler. Skip in test environments —
    # see _rate_limiting_disabled() in app.core.rate_limit.
    if settings.APP_ENV != "test":
        allowed, retry_after = await check_and_consume(
            getattr(request.app.state, "redis", None),
            POLICIES["forgot_password"],
            {"ip": client_ip(request, settings.TRUSTED_PROXIES), "email": body.email.lower()},
        )
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Too many password reset requests",
                headers={"Retry-After": str(retry_after)},
            )

    await generate_reset_token(db, body.email, request)
    await db.commit()
    return {"message": "If that email exists, a reset link has been sent."}


@router.post("/reset-password")
async def reset_password_endpoint(
    body: ResetPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Reset password with token."""
    from app.services.password_reset import reset_password

    success = await reset_password(db, body.token, body.new_password, request)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    await db.commit()
    return {"success": True}


# ── Email Verification ──


@router.post("/verify-email", dependencies=[Depends(rate_limit("verify_email"))])
async def verify_email(
    body: dict,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Consume a SHA-256-hashed, single-use, expiring verification token."""
    from app.services.email_verification import verify_token

    await verify_token(db, body.get("token"), request)
    await db.commit()
    return {"verified": True}


@router.post("/resend-verification")
async def resend_verification(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Re-issue a fresh verification token and email it to the user."""
    from app.core.config import settings
    from app.services.email import send_email
    from app.services.email_templates import email_verification_email
    from app.services.email_verification import issue_token

    if user.email_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    plaintext = await issue_token(db, user, request)
    verify_url = f"{settings.APP_URL}/auth/verify?token={plaintext}"
    await send_email(
        user.email,
        "Verify your METHEAN email",
        email_verification_email(verify_url),
    )
    await db.commit()
    return {"sent": True}


# ── Family Invites ──


# UserRole enum has only owner/co_parent/observer. Two legacy aliases
# ("parent", "viewer") survived in old invite payloads and DB rows, so
# every entry into the role-handling code paths flows through this
# normaliser before reaching the enum. Adding new aliases means just
# adding a new entry here — never adding new UserRole values.
_INVITE_ROLE_ALIASES: dict[str, UserRole] = {
    "owner": UserRole.owner,
    "co_parent": UserRole.co_parent,
    "parent": UserRole.co_parent,  # legacy alias
    "observer": UserRole.observer,
    "viewer": UserRole.observer,  # legacy alias
}


def _normalize_invite_role(raw: str) -> UserRole:
    try:
        return _INVITE_ROLE_ALIASES[raw.strip().lower()]
    except (KeyError, AttributeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid role: {raw}") from exc


class InviteRequest(BaseModel):
    email: str
    role: str = "co_parent"

    @field_validator("role")
    @classmethod
    def _validate_role(cls, v: str) -> str:
        if v.strip().lower() not in _INVITE_ROLE_ALIASES:
            raise ValueError(f"Invalid role: {v}")
        return v.strip().lower()


class AcceptInviteRequest(BaseModel):
    token: str
    password: str = Field(min_length=8)
    display_name: str


@router.post("/household/invite")
async def invite_family_member(
    body: InviteRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Invite a co-parent or observer to the household."""
    import secrets
    from datetime import timedelta

    from app.core.config import settings
    from app.models.identity import FamilyInvite
    from app.services.email import send_email

    # Observers can read but never invite — adding members to the
    # household is an authority that belongs to owner / co_parent only.
    if user.role == UserRole.observer:
        raise HTTPException(status_code=403, detail="Observers cannot invite household members")

    # Persist the canonical enum value so a legacy "parent"/"viewer" in
    # the request body never reaches the DB. _validate_role above has
    # already filtered unknown values; this just maps aliases.
    canonical_role = _normalize_invite_role(body.role)

    # One pending invite per (household, email). Stops accidental dupes
    # when the inviter retries; resending the email goes through a
    # separate "resend" path against the existing row.
    existing = await db.execute(
        select(FamilyInvite).where(
            FamilyInvite.household_id == user.household_id,
            FamilyInvite.email == body.email,
            FamilyInvite.status == "pending",
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="A pending invite for this email already exists")

    token = secrets.token_urlsafe(32)
    invite = FamilyInvite(
        household_id=user.household_id,
        email=body.email,
        role=canonical_role.value,
        invited_by=user.id,
        token=token,
        expires_at=datetime.now(UTC) + timedelta(days=7),
    )
    db.add(invite)
    await db.flush()

    invite_url = f"{settings.APP_URL}/auth?invite={token}"
    html = f"""
    <div style="font-family:-apple-system,sans-serif;max-width:480px;margin:0 auto;padding:20px;">
        <h2 style="color:#0F1B2D;">You've been invited to METHEAN</h2>
        <p style="color:#6B6B6B;">{user.display_name} has invited you to join their family's learning platform as a {body.role}.</p>
        <a href="{invite_url}" style="display:inline-block;background:#C6A24E;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">Accept Invitation</a>
        <p style="color:#9A9A9A;font-size:12px;margin-top:16px;">This invitation expires in 7 days.</p>
    </div>"""
    await send_email(body.email, f"{user.display_name} invited you to METHEAN", html)
    await db.commit()
    return {"invited": True, "email": body.email}


@router.get("/household/invites")
async def list_invites(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list:
    """List pending invites for the household."""
    from app.models.identity import FamilyInvite

    result = await db.execute(
        select(FamilyInvite).where(
            FamilyInvite.household_id == user.household_id,
            FamilyInvite.status == "pending",
        )
    )
    return [
        {"id": str(i.id), "email": i.email, "role": i.role, "created_at": str(i.created_at)}
        for i in result.scalars().all()
    ]


@router.delete("/household/invites/{invite_id}")
async def revoke_invite(
    invite_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Revoke a pending invite."""
    from app.models.identity import FamilyInvite

    if user.role == UserRole.observer:
        raise HTTPException(status_code=403, detail="Observers cannot revoke invites")

    result = await db.execute(
        select(FamilyInvite).where(
            FamilyInvite.id == invite_id,
            FamilyInvite.household_id == user.household_id,
        )
    )
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    invite.status = "revoked"
    await db.commit()
    return {"revoked": True}


@router.post("/accept-invite")
async def accept_invite(
    body: AcceptInviteRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Accept an invite, create account, and join household."""
    from app.models.identity import FamilyInvite

    result = await db.execute(
        select(FamilyInvite).where(
            FamilyInvite.token == body.token,
            FamilyInvite.status == "pending",
        )
    )
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=400, detail="Invalid or expired invitation")

    if invite.expires_at and invite.expires_at < datetime.now(UTC):
        invite.status = "expired"
        await db.commit()
        raise HTTPException(status_code=400, detail="Invitation has expired")

    # Check if user already exists
    existing = await db.execute(select(User).where(User.email == invite.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="An account with this email already exists. Log in and contact the household owner."
        )

    role_enum = _normalize_invite_role(invite.role)
    new_user = User(
        household_id=invite.household_id,
        email=invite.email,
        password_hash=hash_password(body.password),
        display_name=body.display_name,
        role=role_enum,
        email_verified=True,
    )
    db.add(new_user)
    invite.status = "accepted"
    await db.flush()

    token = create_access_token(new_user.id, invite.household_id, new_user.role.value)
    _set_cookie(response, "access_token", token, settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    await db.commit()

    return {"user_id": str(new_user.id), "household_id": str(invite.household_id)}


# ══════════════════════════════════════════════════
# Household deletion (COPPA/GDPR erasure rights)
# ══════════════════════════════════════════════════

# Deletion endpoints live at /household (not /auth/household) to sit
# beside the existing /household/export, so they get their own
# prefix-less router, wired in main.py. Ungated by email verification:
# the right to leave must never be blocked.
household_router = APIRouter(tags=["auth"])


class HouseholdDeletionRequest(BaseModel):
    password: str


def _require_owner(user: User) -> None:
    role = user.role.value if hasattr(user.role, "value") else str(user.role)
    if role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the household owner can manage deletion",
        )


def _purge_after(requested_at: datetime) -> datetime:
    return requested_at + timedelta(days=DELETION_WINDOW_DAYS)


@household_router.delete("/household")
async def request_household_deletion(
    body: HouseholdDeletionRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Schedule the household for permanent deletion after a 7-day window.

    Owner role, parent token scope, and password re-authentication
    required: a session cookie alone must never be enough to destroy a
    family's records. The subscription is canceled immediately; data
    stays intact (and exportable) until the purge task fires.
    """
    from app.models.enums import GovernanceAction
    from app.services.billing import cancel_subscription
    from app.services.governance import log_governance_event

    _require_parent_scope(user)
    _require_owner(user)
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password is incorrect")

    result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = result.scalar_one()
    if household.deletion_requested_at is not None:
        raise HTTPException(status_code=409, detail="deletion_already_pending")

    now = datetime.now(UTC)
    household.deletion_requested_at = now
    household.deletion_requested_by = user.id
    purge_after = _purge_after(now)

    try:
        canceled = await cancel_subscription(db, household.id, at_period_end=False)
    except Exception as exc:
        # A Stripe outage must not block the legal right to leave; the
        # purge task retries cancellation before erasing.
        canceled = False
        logger.warning(
            "household_deletion_stripe_cancel_failed",
            household_id=str(household.id),
            error=str(exc),
        )

    try:
        from app.services.email import send_email
        from app.services.email_templates import deletion_scheduled_email

        await send_email(
            user.email,
            "Your METHEAN household is scheduled for deletion",
            deletion_scheduled_email(
                user.display_name,
                purge_after.strftime("%B %d, %Y"),
                f"{settings.APP_URL}/settings",
                f"{settings.APP_URL}/settings",
            ),
        )
    except Exception as exc:
        logger.warning(
            "household_deletion_email_failed",
            household_id=str(household.id),
            error=str(exc),
        )

    await log_governance_event(
        db,
        household.id,
        user.id,
        GovernanceAction.modify,
        "household_deletion_requested",
        household.id,
        reason="Household deletion requested by owner",
        metadata={"purge_after": purge_after.isoformat(), "subscription_canceled": canceled},
    )
    logger.info(
        "household_deletion_requested",
        household_id=str(household.id),
        user_id=str(user.id),
        purge_after=purge_after.isoformat(),
        subscription_canceled=canceled,
    )
    return {"pending": True, "purge_after": purge_after.isoformat()}


@household_router.post("/household/restore")
async def restore_household(
    body: HouseholdDeletionRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Cancel a pending household deletion within the 7-day window."""
    from app.models.enums import GovernanceAction
    from app.services.governance import log_governance_event

    _require_parent_scope(user)
    _require_owner(user)
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password is incorrect")

    result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = result.scalar_one()
    if household.deletion_requested_at is None:
        raise HTTPException(status_code=409, detail="no_deletion_pending")

    household.deletion_requested_at = None
    household.deletion_requested_by = None

    try:
        from app.services.email import send_email
        from app.services.email_templates import deletion_canceled_email

        await send_email(
            user.email,
            "Your METHEAN deletion was canceled",
            deletion_canceled_email(user.display_name),
        )
    except Exception as exc:
        logger.warning(
            "household_restore_email_failed",
            household_id=str(household.id),
            error=str(exc),
        )

    await log_governance_event(
        db,
        household.id,
        user.id,
        GovernanceAction.modify,
        "household_deletion_restored",
        household.id,
        reason="Household deletion canceled by owner",
    )
    logger.info(
        "household_deletion_restored",
        household_id=str(household.id),
        user_id=str(user.id),
    )
    return {"pending": False, "purge_after": None}


@household_router.get("/household/deletion-status")
async def household_deletion_status(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Whether a deletion is pending and when the purge will run."""
    result = await db.execute(select(Household).where(Household.id == user.household_id))
    household = result.scalar_one()
    if household.deletion_requested_at is None:
        return {"pending": False, "purge_after": None}
    return {
        "pending": True,
        "purge_after": _purge_after(household.deletion_requested_at).isoformat(),
    }
