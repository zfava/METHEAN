"""widen_achievements_string_columns

The `icon` column on `achievements` was VARCHAR(10), which truncates
modern slug icons used by the fitness achievements (`trophy-running`,
`arrow-up-circle`, `calendar-check`). Widen to VARCHAR(50), the model
floor, so future achievement slugs fit without another migration.

Revision ID: 038
Revises: 037
Create Date: 2026-04-23
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "038"
down_revision: Union[str, None] = "037"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "achievements",
        "icon",
        existing_type=sa.String(length=10),
        type_=sa.String(length=50),
        existing_nullable=False,
        existing_server_default=None,
    )


def downgrade() -> None:
    op.alter_column(
        "achievements",
        "icon",
        existing_type=sa.String(length=50),
        type_=sa.String(length=10),
        existing_nullable=False,
        existing_server_default=None,
    )
