"""Add philosophical_profile to households.

Revision ID: 003
Revises: 002
Create Date: 2026-04-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "households",
        sa.Column(
            "philosophical_profile",
            JSONB,
            server_default="{}",
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("households", "philosophical_profile")
