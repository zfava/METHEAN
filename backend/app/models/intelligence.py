"""Learner Intelligence model — persistent learning profile per child."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class LearnerIntelligence(Base):
    __tablename__ = "learner_intelligence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("children.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("households.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Accumulated observations (append-only JSONB arrays/dicts)
    learning_style_observations: Mapped[list] = mapped_column(JSONB, default=list)
    subject_patterns: Mapped[dict] = mapped_column(JSONB, default=dict)
    engagement_patterns: Mapped[dict] = mapped_column(JSONB, default=dict)
    tutor_interaction_analysis: Mapped[dict] = mapped_column(JSONB, default=dict)
    pace_trends: Mapped[dict] = mapped_column(JSONB, default=dict)
    parent_observations: Mapped[list] = mapped_column(JSONB, default=list)
    governance_learned_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Metadata
    last_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    observation_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TutorProfileEntry(Base):
    """One abstracted teaching strategy the tutor has learned works for
    a child (migration 057).

    Placed beside LearnerIntelligence because this is the same family
    of data: per-child adaptive intelligence consumed by AI context
    assembly. Privacy is structural: entries describe what WORKS for
    the learner (strategies, motivators, pacing, interests), never what
    the child said and never what is "wrong" with them; the validator
    in services/tutor_profile.py enforces that on every write path.

    Writes happen ONLY through services/tutor_profile.py, the single
    choke point (guard-tested), so the autonomy policy routing and the
    governance events can never be bypassed.
    """

    __tablename__ = "tutor_profile_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("households.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("children.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[str] = mapped_column(String(300), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="proposed")
    # Set only when an entry was applied autonomously: the hash of the
    # standing ai_autonomy_granted event in force at application time.
    grant_event_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    proposed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Null for autonomous application: no human decided per-item.
    decided_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    __table_args__ = (Index("ix_tutor_profile_child_status", "child_id", "status"),)
