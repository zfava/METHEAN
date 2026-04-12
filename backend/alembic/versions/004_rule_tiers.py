"""Add rule tier enum and column to governance_rules.

Revision ID: 004
Revises: 003
Create Date: 2026-04-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sa.Enum("constitutional", "policy", name="ruletier", create_type=False).create(op.get_bind())
    op.add_column("governance_rules", sa.Column(
        "tier",
        sa.Enum("constitutional", "policy", name="ruletier", create_type=False),
        server_default="policy",
        nullable=False,
    ))


def downgrade() -> None:
    op.drop_column("governance_rules", "tier")
    sa.Enum(name="ruletier", create_type=False).drop(op.get_bind())
