"""Evaluator Calibration models.

Tracks evaluator prediction accuracy and maintains per-child
calibration offsets to correct systematic bias in confidence scoring.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class EvaluatorPrediction(Base):
    __tablename__ = "evaluator_predictions"
    __table_args__ = (
        Index(
            "ix_evalpred_child_node_created",
            "child_id",
            "node_id",
            "created_at",
            postgresql_using="btree",
        ),
        Index(
            "ix_evalpred_child_unreconciled",
            "child_id",
            postgresql_where="actual_outcome IS NULL",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False
    )
    attempt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("attempts.id", ondelete="CASCADE"), nullable=False
    )
    predicted_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_fsrs_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    predicted_retention_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    actual_outcome: Mapped[int | None] = mapped_column(Integer)
    outcome_recorded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    drift_score: Mapped[float | None] = mapped_column(Float)
    calibration_offset_applied: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CalibrationProfile(Base):
    __tablename__ = "calibration_profiles"
    __table_args__ = (UniqueConstraint("child_id", name="uq_calibration_child"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    total_predictions: Mapped[int] = mapped_column(Integer, default=0)
    reconciled_predictions: Mapped[int] = mapped_column(Integer, default=0)
    mean_drift: Mapped[float] = mapped_column(Float, default=0.0)
    directional_bias: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_band_accuracy: Mapped[dict] = mapped_column(JSONB, default=dict)
    subject_drift_map: Mapped[dict] = mapped_column(JSONB, default=dict)
    recalibration_offset: Mapped[float] = mapped_column(Float, default=0.0)
    offset_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent_override_offset: Mapped[float | None] = mapped_column(Float)
    last_computed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CalibrationSnapshot(Base):
    """Point-in-time snapshot of calibration metrics, created on each recompute."""

    __tablename__ = "calibration_snapshots"
    __table_args__ = (
        Index(
            "ix_calsnap_child_computed",
            "child_id",
            "computed_at",
            postgresql_using="btree",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    mean_drift: Mapped[float] = mapped_column(Float, nullable=False)
    directional_bias: Mapped[float] = mapped_column(Float, nullable=False)
    recalibration_offset: Mapped[float] = mapped_column(Float, nullable=False)
    reconciled_count: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_band_accuracy: Mapped[dict] = mapped_column(JSONB, default=dict)
    subject_drift_map: Mapped[dict] = mapped_column(JSONB, default=dict)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
