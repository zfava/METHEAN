"""Add temporal governance fields to governance_rules.

Revision ID: 006
Revises: 005
Create Date: 2026-04-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("governance_rules", sa.Column("effective_from", sa.Date, nullable=True))
    op.add_column("governance_rules", sa.Column("effective_until", sa.Date, nullable=True))
    op.add_column("governance_rules", sa.Column("trigger_conditions", JSONB, server_default="{}", nullable=True))


def downgrade() -> None:
    op.drop_column("governance_rules", "trigger_conditions")
    op.drop_column("governance_rules", "effective_until")
    op.drop_column("governance_rules", "effective_from")
