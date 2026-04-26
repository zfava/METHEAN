"""enable_rls_all_household_tables

Enables Row-Level Security and a per-table household_isolation policy
on every table that carries a household_id column. The policy uses
``current_setting('app.current_household_id', true)`` (missing_ok=true)
so unset session variables return NULL instead of raising — required
for migrations and any test environment that doesn't pre-set the
tenant.

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


tables = [
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
    "audit_logs",
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


def upgrade() -> None:
    for table in tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(f"DROP POLICY IF EXISTS household_isolation_{table} ON {table}")
        op.execute(
            f"""
            CREATE POLICY household_isolation_{table} ON {table}
            USING (household_id = current_setting('app.current_household_id', true)::uuid)
            """
        )


def downgrade() -> None:
    for table in tables:
        op.execute(f"DROP POLICY IF EXISTS household_isolation_{table} ON {table}")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
