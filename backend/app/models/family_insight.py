"""Family Intelligence models — cross-child pattern detection.

Identifies systemic issues no per-child model can see: shared struggles,
curriculum gaps, pacing divergence, environmental correlations, and
material effectiveness across siblings.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import FamilyPatternType, InsightStatus


class FamilyInsight(Base):
    __tablename__ = "family_insights"
    __table_args__ = (
        Index(
            "ix_faminsight_household_status_created",
            "household_id",
            "status",
            "created_at",
            postgresql_using="btree",
        ),
        Index(
            "ix_faminsight_household_pattern",
            "household_id",
            "pattern_type",
        ),
        Index(
            "ix_faminsight_household_predictive",
            "household_id",
            "predictive_child_id",
            postgresql_where="predictive_child_id IS NOT NULL",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )

    pattern_type: Mapped[FamilyPatternType] = mapped_column(nullable=False)
    affected_children: Mapped[list] = mapped_column(JSONB, default=list)
    affected_nodes: Mapped[list] = mapped_column(JSONB, default=list)
    affected_subjects: Mapped[list] = mapped_column(JSONB, default=list)

    evidence_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[InsightStatus] = mapped_column(nullable=False, default=InsightStatus.detected)
    parent_response: Mapped[str | None] = mapped_column(Text)
    false_positive: Mapped[bool | None] = mapped_column(Boolean)

    # Predictive scaffolding
    predictive_child_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="SET NULL")
    )
    predictive_node_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("learning_nodes.id", ondelete="SET NULL")
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class FamilyInsightConfig(Base):
    __tablename__ = "family_insight_configs"
    __table_args__ = (UniqueConstraint("household_id", name="uq_insight_config_household"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    pattern_settings: Mapped[dict] = mapped_column(
        JSONB,
        default=lambda: {
            "shared_struggle": {"enabled": True, "min_children": 2, "drift_threshold": 1.5},
            "curriculum_gap": {"enabled": True, "confidence_threshold": 0.5},
            "pacing_divergence": {"enabled": True, "divergence_factor": 2.0},
            "environmental_correlation": {"enabled": True, "window_days": 7},
            "material_effectiveness": {"enabled": True, "min_attempts": 5},
        },
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
