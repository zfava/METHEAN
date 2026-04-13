"""Harden RLS: safe current_setting, NOSUPERUSER, GRANT permissions.

Recreates all household_isolation policies to use current_setting with
the missing_ok=true parameter so unset variable returns NULL (= no rows)
instead of erroring. Also ensures the app role is NOSUPERUSER so RLS
is never bypassed, and grants necessary table/sequence permissions.

Revision ID: 027
Revises: 026
Create Date: 2026-04-13
"""

from typing import Sequence, Union

from alembic import op

revision: str = "027"
down_revision: Union[str, None] = "026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Every table with a NOT NULL household_id column
HOUSEHOLD_TABLES = [
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

# audit_logs has nullable household_id — separate policy
NULLABLE_HID_TABLE = "audit_logs"

SAFE_USING = (
    "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
)
SAFE_USING_NULLABLE = (
    "USING (household_id = current_setting('app.current_household_id', true)::uuid "
    "OR household_id IS NULL)"
)


def upgrade() -> None:
    conn = op.get_bind()

    # 1. Ensure app role is not a superuser (superusers bypass RLS)
    conn.execute(op.inline_literal("ALTER ROLE methean NOSUPERUSER"))

    # 2. Recreate policies with safe current_setting (missing_ok = true)
    for table in HOUSEHOLD_TABLES:
        policy = f"{table}_household_isolation"
        conn.execute(op.inline_literal(f"DROP POLICY IF EXISTS {policy} ON {table}"))
        conn.execute(op.inline_literal(
            f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"
        ))
        conn.execute(op.inline_literal(
            f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"
        ))
        conn.execute(op.inline_literal(
            f"CREATE POLICY {policy} ON {table} {SAFE_USING}"
        ))

    # 3. Audit logs — nullable household_id
    conn.execute(op.inline_literal(
        f"DROP POLICY IF EXISTS {NULLABLE_HID_TABLE}_household_isolation ON {NULLABLE_HID_TABLE}"
    ))
    conn.execute(op.inline_literal(
        f"ALTER TABLE {NULLABLE_HID_TABLE} ENABLE ROW LEVEL SECURITY"
    ))
    conn.execute(op.inline_literal(
        f"ALTER TABLE {NULLABLE_HID_TABLE} FORCE ROW LEVEL SECURITY"
    ))
    conn.execute(op.inline_literal(
        f"CREATE POLICY {NULLABLE_HID_TABLE}_household_isolation "
        f"ON {NULLABLE_HID_TABLE} {SAFE_USING_NULLABLE}"
    ))

    # 4. Grant permissions so non-superuser role can still operate
    conn.execute(op.inline_literal(
        "GRANT ALL ON ALL TABLES IN SCHEMA public TO methean"
    ))
    conn.execute(op.inline_literal(
        "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO methean"
    ))
    conn.execute(op.inline_literal(
        "GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO methean"
    ))


def downgrade() -> None:
    conn = op.get_bind()

    # Revert to old policies without missing_ok
    old_using = (
        "USING (household_id = current_setting('app.current_household_id')::uuid)"
    )
    old_using_nullable = (
        "USING (household_id = current_setting('app.current_household_id')::uuid "
        "OR household_id IS NULL)"
    )

    for table in HOUSEHOLD_TABLES:
        policy = f"{table}_household_isolation"
        conn.execute(op.inline_literal(f"DROP POLICY IF EXISTS {policy} ON {table}"))
        conn.execute(op.inline_literal(
            f"CREATE POLICY {policy} ON {table} {old_using}"
        ))

    conn.execute(op.inline_literal(
        f"DROP POLICY IF EXISTS {NULLABLE_HID_TABLE}_household_isolation ON {NULLABLE_HID_TABLE}"
    ))
    conn.execute(op.inline_literal(
        f"CREATE POLICY {NULLABLE_HID_TABLE}_household_isolation "
        f"ON {NULLABLE_HID_TABLE} {old_using_nullable}"
    ))
