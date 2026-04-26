"""enable_rls_all_household_tables

Re-asserts Row-Level Security + a household_isolation policy on every
table that carries a ``household_id`` column. The historical RLS
migrations (001, 005, 007, 008, 015, 021-027, 031-033, 037, 039, 040)
covered every table when each was added, but ``test_rls_coverage`` is
the catch-all guard: any table that ever drifts off the list — by
naming, by environment, or by a missed migration — is flagged here
in one pass instead of via per-table archaeology.

The policy is named plainly ``household_isolation`` (not the historical
``<table>_household_isolation``) so it coexists with prior policies
without collision; PostgreSQL OR-combines permissive policies, so the
addition is safe and cumulative.

Revision ID: 042
Revises: 041
Create Date: 2026-04-26
"""

from collections.abc import Sequence

from alembic import op

revision: str = "042"
down_revision: str | None = "041"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# Every table with a NOT NULL household_id column in the current model.
HOUSEHOLD_TABLES: list[str] = [
    "achievements",
    "activities",
    "activity_feedback",
    "advisor_reports",
    "ai_runs",
    "alerts",
    "annual_curricula",
    "artifacts",
    "assessments",
    "attempts",
    "beta_feedback",
    "calibration_profiles",
    "calibration_snapshots",
    "child_map_enrollments",
    "child_node_states",
    "child_preferences",
    "children",
    "device_tokens",
    "education_plans",
    "evaluator_predictions",
    "family_insight_configs",
    "family_insights",
    "family_invites",
    "family_resources",
    "fitness_benchmarks",
    "fitness_logs",
    "fsrs_cards",
    "governance_events",
    "governance_rules",
    "learner_intelligence",
    "learner_style_vectors",
    "learning_edges",
    "learning_maps",
    "learning_nodes",
    "notification_logs",
    "plan_weeks",
    "plans",
    "portfolio_entries",
    "reading_log_entries",
    "refresh_tokens",
    "review_logs",
    "state_events",
    "streaks",
    "subjects",
    "usage_events",
    "usage_ledger",
    "user_permissions",
    "users",
    "weekly_snapshots",
    "wellbeing_anomalies",
    "wellbeing_configs",
]

# audit_logs has a nullable household_id; its policy must permit NULL
# rows so system-level audit entries (no tenant) remain reachable.
NULLABLE_HID_TABLE = "audit_logs"

USING_CLAUSE = "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
USING_CLAUSE_NULLABLE = (
    "USING (household_id = current_setting('app.current_household_id', true)::uuid OR household_id IS NULL)"
)


def upgrade() -> None:
    for table in HOUSEHOLD_TABLES:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(f"DROP POLICY IF EXISTS household_isolation ON {table}")
        op.execute(f"CREATE POLICY household_isolation ON {table} {USING_CLAUSE}")

    op.execute(f"ALTER TABLE {NULLABLE_HID_TABLE} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {NULLABLE_HID_TABLE} FORCE ROW LEVEL SECURITY")
    op.execute(f"DROP POLICY IF EXISTS household_isolation ON {NULLABLE_HID_TABLE}")
    op.execute(f"CREATE POLICY household_isolation ON {NULLABLE_HID_TABLE} {USING_CLAUSE_NULLABLE}")


def downgrade() -> None:
    # Drop only the household_isolation policy this migration added.
    # The pre-existing per-table policies (e.g. <table>_household_isolation)
    # remain in place, so RLS stays effective after a downgrade.
    for table in [*HOUSEHOLD_TABLES, NULLABLE_HID_TABLE]:
        op.execute(f"DROP POLICY IF EXISTS household_isolation ON {table}")
