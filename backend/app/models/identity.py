"""Identity & Tenancy models (Section 3.1)."""

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import UserRole


class Household(Base):
    __tablename__ = "households"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="America/New_York")
    home_state: Mapped[str | None] = mapped_column(String(2), nullable=True)
    settings: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    philosophical_profile: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    # Billing
    stripe_customer_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    subscription_status: Mapped[str] = mapped_column(String(50), default="trial")
    trial_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    subscription_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Governance mode (additive, defaults preserve existing behavior)
    governance_mode: Mapped[str] = mapped_column(String(30), nullable=False, server_default="parent_governed")
    organization_type: Mapped[str] = mapped_column(String(50), nullable=False, server_default="homeschool")
    organization_metadata: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    learner_age_range: Mapped[str] = mapped_column(String(20), nullable=False, server_default="k12")
    credit_system: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="household")
    children: Mapped[list["Child"]] = relationship(back_populates="household")
    personalization_policy: Mapped["PersonalizationPolicy | None"] = relationship(
        back_populates="household", uselist=False
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(nullable=False, default=UserRole.owner)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_preferences: Mapped[dict | None] = mapped_column(
        JSONB,
        default=lambda: {
            "email_daily_summary": True,
            "email_milestones": True,
            "email_governance_alerts": True,
            "email_weekly_digest": True,
            "email_compliance_warnings": True,
        },
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Governance mode (additive, defaults preserve existing behavior)
    is_self_learner: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    linked_child_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="SET NULL"), nullable=True
    )
    institutional_role: Mapped[str | None] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    household: Mapped["Household"] = relationship(back_populates="users")


class EmailVerificationToken(Base):
    """Hashed, expiring, single-use email-verification token.

    The plaintext token is delivered via email (URL query param). The
    DB only stores the SHA-256 hex digest, so a row leak does not let
    an attacker mint a verified-email account. ``used_at`` enforces
    single use; ``expires_at`` enforces a 60-minute TTL via
    ``app.services.email_verification.TOKEN_TTL_MINUTES``.
    """

    __tablename__ = "email_verification_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(500))


class PasswordResetToken(Base):
    """Hashed, expiring, single-use password-reset token.

    Mirrors :class:`EmailVerificationToken`. A partial unique index on
    ``(user_id) WHERE used_at IS NULL`` enforces at most one active
    reset token per user — issuing a fresh token requires marking the
    prior active one as used (handled in
    :mod:`app.services.password_reset`).
    """

    __tablename__ = "password_reset_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(500))


class Child(Base):
    __tablename__ = "children"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(100))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    grade_level: Mapped[str | None] = mapped_column(String(20))
    avatar_url: Mapped[str | None] = mapped_column(Text)
    fsrs_weights: Mapped[list | None] = mapped_column(JSONB)  # Personalized FSRS weights (21 params)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    household: Mapped["Household"] = relationship(back_populates="children")
    preferences: Mapped["ChildPreferences | None"] = relationship(back_populates="child", uselist=False)


class ChildPreferences(Base):
    __tablename__ = "child_preferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    learning_style: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    interests: Mapped[list | None] = mapped_column(JSONB, default=list)
    personalization: Mapped[dict] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb"), default=dict
    )
    accommodations: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    daily_duration_minutes: Mapped[int | None] = mapped_column()
    preferred_schedule: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    subject_levels: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    strengths: Mapped[list | None] = mapped_column(JSONB, default=list)
    areas_for_growth: Mapped[list | None] = mapped_column(JSONB, default=list)
    custom_subjects: Mapped[list | None] = mapped_column(JSONB, default=list)
    parent_notes: Mapped[str | None] = mapped_column(Text)
    certification_progress: Mapped[list | None] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    child: Mapped["Child"] = relationship(back_populates="preferences")


class UserPermission(Base):
    """Granular permission grants for users within a household."""

    __tablename__ = "user_permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    permission: Mapped[str] = mapped_column(String(100), nullable=False)
    scope_type: Mapped[str | None] = mapped_column(String(50))  # "child", "subject", "all"
    scope_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    granted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FamilyInvite(Base):
    __tablename__ = "family_invites"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="parent")
    invited_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    token: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class PersonalizationPolicy(Base):
    """Household-level policy that gates the personalization library.

    Each list column holds either the sentinel ``["*"]`` (meaning "any
    library entry is allowed") or an explicit list of library IDs.
    Expansion of the sentinel into the full ID set happens at the API
    layer so adding new library entries does not require a data
    migration. One row per household, RLS-isolated by household_id.
    """

    __tablename__ = "personalization_policy"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("households.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    allowed_vibes: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("ARRAY['*']::text[]"), default=lambda: ["*"]
    )
    allowed_interest_tags: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("ARRAY['*']::text[]"), default=lambda: ["*"]
    )
    allowed_voice_personas: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("ARRAY['*']::text[]"), default=lambda: ["*"]
    )
    allowed_iconography_packs: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("ARRAY['*']::text[]"), default=lambda: ["*"]
    )
    allowed_sound_packs: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("ARRAY['*']::text[]"), default=lambda: ["*"]
    )
    allowed_affirmation_tones: Mapped[list[str]] = mapped_column(
        ARRAY(Text()), nullable=False, server_default=text("ARRAY['*']::text[]"), default=lambda: ["*"]
    )
    companion_name_requires_review: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false"), default=False
    )
    max_interest_tags_per_child: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("5"), default=5
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    household: Mapped["Household"] = relationship(back_populates="personalization_policy")
