"""Learner Intelligence model — persistent learning profile per child."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
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
    # The content tier (LEARNING_LEVELS key) the child was at, in the
    # relevant subject, when this entry was proposed (migration 062). Lets
    # the efficacy engine retire a strategy tied to an outgrown stage.
    # Distinct from MasteryLevel: this is the curriculum tier axis.
    tier_band: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # Set only when an entry was applied autonomously: the hash of the
    # standing ai_autonomy_granted event in force at application time.
    grant_event_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    proposed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Null for autonomous application: no human decided per-item.
    decided_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Efficacy signals (migration 061). The tutor's memory becomes
    # evidence-bearing: each active entry is measured against the child's
    # real attempt outcomes by services/tutor_efficacy.py, the SINGLE
    # writer of these fields and of TutorEntryObservation. The label is a
    # conservative word (working_well, no_clear_effect, may_have_outgrown,
    # insufficient_data), never a score: these are observational
    # correlations on small samples, a signal and not proof. 'retired' is
    # a valid status value: an entry the child has outgrown, retired
    # through the same autonomy policy as everything else; retired entries
    # are never injected and never deleted.
    efficacy_label: Mapped[str | None] = mapped_column(String(30), nullable=True)
    observations_count: Mapped[int] = mapped_column(Integer, server_default="0", default=0, nullable=False)
    last_evaluated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (Index("ix_tutor_profile_child_status", "child_id", "status"),)


class TutorEntryObservation(Base):
    """One efficacy evaluation of a tutor profile entry (migration 061).

    Each row is a single observational reading: the child's success rate
    on attempts inside the entry's active window versus a baseline window
    before the entry was activated, and the delta between them. The rate
    uses the SAME definition of success the mastery system uses (an
    attempt's FSRS rating is not Again); it is never a new metric.

    These are correlations on small samples, not causal proof, so every
    row records its own sample sizes: a delta is meaningless without the N
    it came from. subject_scope records whether the sample was narrowed to
    one subject family (derived conservatively from the entry's content)
    or left as all attempts.

    Written ONLY through services/tutor_efficacy.py, the single choke
    point (guard-tested), mirroring the TutorProfileEntry writer guard.
    The efficacy engine reads attempts and mastery outcomes and writes
    nothing else: observation rows here, and proposals through
    tutor_profile.route_proposal.
    """

    __tablename__ = "tutor_entry_observations"

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
    entry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tutor_profile_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    window_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    active_attempts: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", default=0)
    active_success_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    baseline_attempts: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0", default=0)
    baseline_success_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    delta: Mapped[float | None] = mapped_column(Float, nullable=True)
    # "math", "reading", etc. when the entry content named a subject, else
    # "all": the sample was every attempt because the scope was ambiguous.
    subject_scope: Mapped[str] = mapped_column(String(30), nullable=False, server_default="all", default="all")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ChildTutorPreferences(Base):
    """One row per child: the parent's control surface over the tutor's
    developmental voice register (migration 062).

    register_override is absolute when set: it overrides the tier derived
    from the child's curriculum stage entirely, per child, until cleared.
    Null means automatic (derive from content tier). relationship_memory
    ships 'off' and is consumed by a later prompt; the column lives here
    now so register and that feature share one table and one migration.
    Writes go through the preferences API, which logs a governance event
    on every override change.
    """

    __tablename__ = "child_tutor_preferences"

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
        unique=True,
    )
    # One of the five LEARNING_LEVELS keys, or null for automatic.
    register_override: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # off|on. Ships off; activated by the relationship memory prompt.
    relationship_memory: Mapped[str] = mapped_column(String(8), nullable=False, server_default="off", default="off")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
