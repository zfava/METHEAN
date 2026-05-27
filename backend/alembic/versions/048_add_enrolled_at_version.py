"""add enrolled_at_version to child_map_enrollments

The Child model has been kept in sync via this migration's sibling 047,
which added the missing fsrs_weights column. A drift audit (autogenerate
against head 047 with the live Base.metadata) surfaced exactly one
remaining REAL-MISSING column:

    child_map_enrollments.enrolled_at_version (Integer, NOT NULL)

The model declaration is:
    backend/app/models/curriculum.py:159
    enrolled_at_version: Mapped[int] = mapped_column(Integer, default=1)

This column is written on enrollment creation (backend/app/api/curriculum.py:852)
and is part of the response schema (backend/app/schemas/curriculum.py:177),
so its absence crashes the curriculum page with UndefinedColumnError.

NOT NULL backfill: existing rows are backfilled by setting
server_default=text('1'). The model carries a Python-side default of 1,
so the DB-side server_default is also 1 and stays attached to the column
after the migration. (Migration 046 follows the same pattern with the
curriculum_philosophy server_default.)

This migration is intentionally additive-only: the autogenerate diff
also surfaced ~155 cosmetic drift items (NOT NULL tightening, enum
coercion, default formatting) and several SPURIOUS drops driven by
incomplete model imports. None are crash-causing; all are flagged for
a separate audited pass, not handled here.

A drift-guard pytest (tests/test_schema_drift.py) was added alongside
this migration and asserts that no further crash-class drift
(add_column / add_table / add_index for things the model declares but
the DB lacks) accumulates silently.

Revision ID: 048
Revises: 047
Create Date: 2026-05-27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "048"
down_revision: str | None = "047"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "child_map_enrollments",
        sa.Column(
            "enrolled_at_version",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),
    )


def downgrade() -> None:
    op.drop_column("child_map_enrollments", "enrolled_at_version")
