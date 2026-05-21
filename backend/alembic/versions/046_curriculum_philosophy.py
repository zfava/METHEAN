"""curriculum_philosophy

Adds per-child pedagogical philosophy selection to the children
table: curriculum_philosophy (the chosen approach) and
subject_philosophies (per-subject overrides used only for the
eclectic case). Existing rows backfill to "traditional" via the
column server default.

Revision ID: 046
Revises: 045
Create Date: 2026-05-21
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "046"
down_revision: str | None = "045"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # curriculum_philosophy: not null, server default backfills
    # existing rows to "traditional".
    op.add_column(
        "children",
        sa.Column(
            "curriculum_philosophy",
            sa.String(length=32),
            nullable=False,
            server_default=sa.text("'traditional'"),
        ),
    )
    # subject_philosophies: nullable JSONB, defaults to an empty map.
    op.add_column(
        "children",
        sa.Column(
            "subject_philosophies",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("children", "subject_philosophies")
    op.drop_column("children", "curriculum_philosophy")
