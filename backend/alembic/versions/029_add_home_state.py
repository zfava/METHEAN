"""Add home_state to households.

Revision ID: 029
Revises: 028
Create Date: 2026-04-15
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "029"
down_revision: Union[str, None] = "028"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("households", sa.Column("home_state", sa.String(2), nullable=True))


def downgrade() -> None:
    op.drop_column("households", "home_state")
