"""Retroactive RLS policies for unprotected tables.

SECURITY FIX: 9 tables with household_id were missing Row Level Security
policies. Additionally, 10 tables from migrations 021-025 had ENABLE but
not FORCE ROW LEVEL SECURITY (inconsistent with migration 001 pattern).

Revision ID: 026
Revises: 025
Create Date: 2026-04-12
"""

from typing import Sequence, Union

from alembic import op

revision: str = "026"
down_revision: Union[str, None] = "025"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Tables missing RLS entirely (from migrations 009-020)
MISSING_RLS = [
    "achievements",
    "activity_feedback",
    "annual_curricula",
    "family_invites",
    "family_resources",
    "reading_log_entries",
    "streaks",
    "usage_events",
    "usage_ledger",
]

# Tables from migrations 021-025 that have ENABLE but not FORCE
MISSING_FORCE = [
    "evaluator_predictions",
    "calibration_profiles",
    "calibration_snapshots",
    "learner_style_vectors",
    "family_insights",
    "family_insight_configs",
    "wellbeing_anomalies",
    "wellbeing_configs",
]


def upgrade() -> None:
    # 1. Add full RLS (ENABLE + FORCE + POLICY) to 9 unprotected tables
    for table in MISSING_RLS:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY {table}_household_isolation ON {table} "
            f"USING (household_id = current_setting('app.current_household_id')::uuid)"
        )

    # 2. Add FORCE to tables from 021-025 that only had ENABLE
    for table in MISSING_FORCE:
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")


def downgrade() -> None:
    # Remove FORCE from 021-025 tables (restore to their original state)
    for table in MISSING_FORCE:
        op.execute(f"ALTER TABLE {table} NO FORCE ROW LEVEL SECURITY")

    # Remove RLS from the 9 newly-protected tables
    for table in MISSING_RLS:
        op.execute(f"DROP POLICY IF EXISTS {table}_household_isolation ON {table}")
        op.execute(f"ALTER TABLE {table} NO FORCE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
