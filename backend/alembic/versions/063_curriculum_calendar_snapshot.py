"""curriculum calendar snapshot: calendar_snapshot + calendar_version

Adds the resolved-academic-calendar snapshot to annual_curricula so a later
household calendar edit can detect drift and re-flow only the future,
uncompleted portion of an already-materialized plan deterministically.

  - annual_curricula.calendar_snapshot: the resolved household academic
    calendar (DEFAULT_CALENDAR merged with the household override) this
    curriculum was materialized against, captured at approval time.
  - annual_curricula.calendar_version: a stable SHA-256 hash of
    calendar_snapshot, recorded on the governance event emitted by a
    re-flow so the change is traceable to the exact calendar.

Both nullable: pre-063 rows and curricula approved before this column existed
degrade to "no snapshot" (re-flow reads the live calendar in that case).

Revision ID: 063
Revises: 062
Create Date: 2026-06-14
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "063"
down_revision: str | None = "062"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "annual_curricula",
        sa.Column("calendar_snapshot", JSONB, nullable=True),
    )
    op.add_column(
        "annual_curricula",
        sa.Column("calendar_version", sa.String(64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("annual_curricula", "calendar_version")
    op.drop_column("annual_curricula", "calendar_snapshot")
