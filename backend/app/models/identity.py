"""Identity & Tenancy models (Section 3.1)."""

import uuid
from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Date, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import UserRole


class Household(Base):
    __tablename__ = "households"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="America/New_York")
    settings: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    philosophical_profile: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    # Billing
    stripe_customer_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    subscription_status: Mapped[str] = mapped_column(String(50), default="trial")
    trial_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    subscription_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="household")
    children: Mapped[list["Child"]] = relationship(back_populates="household")


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        nullable=False, default=UserRole.owner
    )
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    household: Mapped["Household"] = relationship(back_populates="users")


class Child(Base):
    __tablename__ = "children"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    household: Mapped["Household"] = relationship(back_populates="children")
    preferences: Mapped["ChildPreferences | None"] = relationship(
        back_populates="child", uselist=False
    )


class ChildPreferences(Base):
    __tablename__ = "child_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    learning_style: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    interests: Mapped[list | None] = mapped_column(JSONB, default=list)
    accommodations: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    daily_duration_minutes: Mapped[int | None] = mapped_column()
    preferred_schedule: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    subject_levels: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    strengths: Mapped[list | None] = mapped_column(JSONB, default=list)
    areas_for_growth: Mapped[list | None] = mapped_column(JSONB, default=list)
    custom_subjects: Mapped[list | None] = mapped_column(JSONB, default=list)
    parent_notes: Mapped[str | None] = mapped_column(Text)
    certification_progress: Mapped[list | None] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    child: Mapped["Child"] = relationship(back_populates="preferences")


class UserPermission(Base):
    """Granular permission grants for users within a household."""

    __tablename__ = "user_permissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    permission: Mapped[str] = mapped_column(String(100), nullable=False)
    scope_type: Mapped[str | None] = mapped_column(String(50))  # "child", "subject", "all"
    scope_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    granted_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


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
