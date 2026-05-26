"""add fsrs_weights to children

Adds the missing fsrs_weights column to the children table so the
database matches the Child model (backend/app/models/identity.py:159),
which declares fsrs_weights as a nullable JSONB column holding the
child's personalized FSRS parameter vector. Without this column, every
query against Child errors with: column children.fsrs_weights does not
exist. Schema-only fix; no model or app changes.

Revision ID: 047
Revises: 046
Create Date: 2026-05-26
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "047"
down_revision: str | None = "046"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "children",
        sa.Column("fsrs_weights", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("children", "fsrs_weights")
