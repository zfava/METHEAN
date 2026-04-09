"""Learner Intelligence model — persistent learning profile per child."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class LearnerIntelligence(Base):
    __tablename__ = "learner_intelligence"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
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
    last_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    observation_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
