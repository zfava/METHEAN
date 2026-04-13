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
    # 1. Strip superuser (if we have it) and grant table/sequence permissions.
    #    The ALTER ROLE requires superuser privilege, so guard with an IF check
    #    to avoid failure on managed PG services and CI where the role is not superuser.
    op.execute("""
DO $$
BEGIN
    -- Only strip superuser if current role actually has it
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = current_user AND rolsuper = true) THEN
        EXECUTE 'ALTER ROLE ' || quote_ident(current_user) || ' NOSUPERUSER';
    END IF;
    -- GRANTs are safe regardless of role privileges
    EXECUTE 'GRANT ALL ON ALL TABLES IN SCHEMA public TO ' || quote_ident(current_user);
    EXECUTE 'GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ' || quote_ident(current_user);
END $$;
""")

    # 2. Recreate policies with safe current_setting (missing_ok = true)
    for table in HOUSEHOLD_TABLES:
        policy = f"{table}_household_isolation"
        op.execute(f"DROP POLICY IF EXISTS {policy} ON {table}")
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(f"CREATE POLICY {policy} ON {table} {SAFE_USING}")

    # 3. Audit logs — nullable household_id
    op.execute(
        f"DROP POLICY IF EXISTS {NULLABLE_HID_TABLE}_household_isolation ON {NULLABLE_HID_TABLE}"
    )
    op.execute(f"ALTER TABLE {NULLABLE_HID_TABLE} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {NULLABLE_HID_TABLE} FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY {NULLABLE_HID_TABLE}_household_isolation "
        f"ON {NULLABLE_HID_TABLE} {SAFE_USING_NULLABLE}"
    )

    # 4. Grants already handled in step 1 above


def downgrade() -> None:
    # Restore superuser if we can (requires current role to already be superuser).
    # In non-superuser environments this is a no-op — you can't grant yourself superuser.
    op.execute("""
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = current_user AND rolsuper = true) THEN
        -- Already superuser, nothing to restore
        NULL;
    ELSE
        RAISE NOTICE 'Skipping SUPERUSER restore - current role is not superuser';
    END IF;
END $$;
""")

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
        op.execute(f"DROP POLICY IF EXISTS {policy} ON {table}")
        op.execute(f"CREATE POLICY {policy} ON {table} {old_using}")

    op.execute(
        f"DROP POLICY IF EXISTS {NULLABLE_HID_TABLE}_household_isolation ON {NULLABLE_HID_TABLE}"
    )
    op.execute(
        f"CREATE POLICY {NULLABLE_HID_TABLE}_household_isolation "
        f"ON {NULLABLE_HID_TABLE} {old_using_nullable}"
    )
