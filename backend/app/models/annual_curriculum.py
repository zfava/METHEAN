"""Annual Curriculum model — 36-week year-long plan for one subject."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class AnnualCurriculum(Base):
    """A complete year-long curriculum for one subject for one child.

    The scope_sequence is the ORIGINAL AI-GENERATED plan. It never changes
    after approval — this is the "what was planned" record.

    The actual_record accumulates over time as weeks are completed —
    this is the "what actually happened" record.

    Parent modifications (edits, moves, additions, removals) are tracked
    in the Activities themselves. The system always knows: what the AI
    planned, what the parent changed, and what actually happened.
    """

    __tablename__ = "annual_curricula"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    learning_map_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("learning_maps.id", ondelete="SET NULL")
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))

    # Identity
    subject_name: Mapped[str] = mapped_column(String(255), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)  # "2026-2027"
    grade_level: Mapped[str | None] = mapped_column(String(50))

    # Configuration
    total_weeks: Mapped[int] = mapped_column(Integer, default=36)
    hours_per_week: Mapped[float | None] = mapped_column(Float)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    # The full scope and sequence as generated/approved — IMMUTABLE after approval
    scope_sequence: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Status
    status: Mapped[str] = mapped_column(String(50), default="draft")  # draft, active, completed, archived
    ai_run_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    # Historical record of what actually happened — grows over time
    actual_record: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
