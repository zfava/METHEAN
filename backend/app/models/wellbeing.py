"""Wellbeing Anomaly Detection models.

Detects when a child's performance drops across multiple subjects
simultaneously, often signaling factors outside the curriculum:
stress, sleep disruption, health issues, family transitions.

# PARENT-ONLY: Never expose to child-facing endpoints or UI.
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
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import AnomalyStatus, AnomalyType, SensitivityLevel


class WellbeingAnomaly(Base):
    """Detected wellbeing anomaly for a child.

    # PARENT-ONLY: Never expose to child-facing endpoints or UI.
    """

    __tablename__ = "wellbeing_anomalies"
    __table_args__ = (
        Index(
            "ix_wellbeing_child_status_created",
            "child_id",
            "status",
            "created_at",
            postgresql_using="btree",
        ),
        Index(
            "ix_wellbeing_household_status",
            "household_id",
            "status",
        ),
        Index(
            "ix_wellbeing_child_type_created",
            "child_id",
            "anomaly_type",
            "created_at",
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

    anomaly_type: Mapped[AnomalyType] = mapped_column(nullable=False)
    severity: Mapped[float] = mapped_column(Float, nullable=False)
    affected_subjects: Mapped[list] = mapped_column(JSONB, default=list)
    evidence_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    parent_message: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[AnomalyStatus] = mapped_column(nullable=False, default=AnomalyStatus.detected)
    sensitivity_level: Mapped[SensitivityLevel] = mapped_column(nullable=False)
    false_positive: Mapped[bool | None] = mapped_column(Boolean)

    parent_response: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class WellbeingConfig(Base):
    """Per-child wellbeing detection configuration.

    # PARENT-ONLY: Never expose to child-facing endpoints or UI.
    """

    __tablename__ = "wellbeing_configs"
    __table_args__ = (UniqueConstraint("child_id", name="uq_wellbeing_config_child"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    household_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("households.id", ondelete="CASCADE"), nullable=False
    )
    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sensitivity_level: Mapped[SensitivityLevel] = mapped_column(nullable=False, default=SensitivityLevel.balanced)

    custom_thresholds: Mapped[dict] = mapped_column(JSONB, default=dict)
    threshold_adjustments: Mapped[dict] = mapped_column(JSONB, default=dict)
    total_false_positives: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
