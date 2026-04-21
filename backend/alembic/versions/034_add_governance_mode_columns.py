"""add_governance_mode_columns

Additive only. Introduces governance mode support on Household and User
with server defaults that preserve existing behavior (every existing
row lands as parent_governed / homeschool / k12, non-self-learner,
no linked child, no institutional role).

Revision ID: 034
Revises: 033
Create Date: 2026-04-19
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "034"
down_revision: Union[str, None] = "033"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Household governance columns
    op.add_column(
        "households",
        sa.Column(
            "governance_mode",
            sa.String(length=30),
            nullable=False,
            server_default="parent_governed",
        ),
    )
    op.add_column(
        "households",
        sa.Column(
            "organization_type",
            sa.String(length=50),
            nullable=False,
            server_default="homeschool",
        ),
    )
    op.add_column(
        "households",
        sa.Column("organization_metadata", JSONB, nullable=True),
    )
    op.add_column(
        "households",
        sa.Column(
            "learner_age_range",
            sa.String(length=20),
            nullable=False,
            server_default="k12",
        ),
    )
    op.add_column(
        "households",
        sa.Column("credit_system", JSONB, nullable=True),
    )

    # User governance columns
    op.add_column(
        "users",
        sa.Column(
            "is_self_learner",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "linked_child_id",
            UUID(as_uuid=True),
            sa.ForeignKey("children.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column(
        "users",
        sa.Column("institutional_role", sa.String(length=50), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "institutional_role")
    op.drop_column("users", "linked_child_id")
    op.drop_column("users", "is_self_learner")

    op.drop_column("households", "credit_system")
    op.drop_column("households", "learner_age_range")
    op.drop_column("households", "organization_metadata")
    op.drop_column("households", "organization_type")
    op.drop_column("households", "governance_mode")
