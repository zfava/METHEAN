"""Performance indexes for /children/{id}/today.

The handler joins Activity → PlanWeek → Plan and filters on
``Plan.child_id``. As plans + activities accumulate, two cold paths
need backing indexes:

* ``ix_plans_child_id`` — supports the ``Plan.child_id == :child_id``
  filter in the join.
* ``ix_activities_scheduled_date_status`` — composite for the
  ``scheduled_date == today AND status IN (...)`` filter that runs
  after the join.

Both are created with ``IF NOT EXISTS`` so the migration is safe to
re-run on environments where they were created out-of-band.

Revision ID: 041
Revises: 040
Create Date: 2026-04-25
"""

from typing import Sequence, Union

from alembic import op

revision: str = "041"
down_revision: Union[str, None] = "040"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_plans_child_id ON plans (child_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_activities_scheduled_date_status "
        "ON activities (scheduled_date, status)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_activities_scheduled_date_status")
    op.execute("DROP INDEX IF EXISTS ix_plans_child_id")
