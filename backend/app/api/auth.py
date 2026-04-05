"""Auth API endpoints: register, login, logout, refresh."""

import hashlib
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status, Cookie
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.identity import Household, User
from app.models.operational import RefreshToken
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RefreshResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


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


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    response: Response,
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

    # Auto-grant owner permissions
    from app.core.permissions import grant_role_permissions
    await grant_role_permissions(db, user.id, household.id, "owner", user.id)

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

    return RegisterResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
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
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.id == token_id)
    )
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
            update(RefreshToken)
            .where(RefreshToken.user_id == stored_token.user_id)
            .values(is_revoked=True)
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token reuse detected",
        )

    # Verify hash matches (guards against forged token IDs)
    if stored_token.token_hash != _hash_token(refresh_token):
        await db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == stored_token.user_id)
            .values(is_revoked=True)
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
            result = await db.execute(
                select(RefreshToken).where(RefreshToken.id == token_id)
            )
            stored = result.scalar_one_or_none()
            if stored:
                stored.is_revoked = True
        except Exception:
            pass  # Best-effort revocation

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return MessageResponse(message="Logged out successfully")


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(user)
