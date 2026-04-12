"""Learner Style Vector — computed learning profile per child.

Derived from raw LearnerIntelligence JSONB observations. Each dimension
is independently computed and can be null when insufficient data exists.
Parents can override or bound any dimension.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class LearnerStyleVector(Base):
    __tablename__ = "learner_style_vectors"
    __table_args__ = (UniqueConstraint("child_id", name="uq_style_vector_child"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )

    # ── Computed dimensions ──
    optimal_session_minutes: Mapped[int | None] = mapped_column(Integer)
    socratic_responsiveness: Mapped[float | None] = mapped_column(Float)
    frustration_threshold: Mapped[float | None] = mapped_column(Float)
    recovery_rate: Mapped[float | None] = mapped_column(Float)
    time_of_day_peak: Mapped[int | None] = mapped_column(Integer)
    subject_affinity_map: Mapped[dict] = mapped_column(JSONB, default=dict)
    modality_preference: Mapped[str | None] = mapped_column(String(20))
    pacing_preference: Mapped[float | None] = mapped_column(Float)
    independence_level: Mapped[float | None] = mapped_column(Float)
    attention_pattern: Mapped[str | None] = mapped_column(String(20))

    # ── Metadata ──
    data_points_count: Mapped[int] = mapped_column(Integer, default=0)
    dimensions_active: Mapped[int] = mapped_column(Integer, default=0)

    # ── Parent governance ──
    parent_overrides: Mapped[dict] = mapped_column(JSONB, default=dict)
    parent_bounds: Mapped[dict] = mapped_column(JSONB, default=dict)

    # ── Timestamps ──
    last_computed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
