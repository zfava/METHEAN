"""Schema-level RLS coverage guard (METHEAN-6-13).

Migrations 032 and 033 created then re-applied RLS for
``beta_feedback`` because RLS coverage had drifted off the
household-scoped table list. This test queries the live PostgreSQL
catalog to confirm that every ``public.*`` table with a
``household_id`` column has Row-Level Security enabled and a policy
that scopes reads to ``current_setting('app.current_household_id')``.
A future migration that adds a household-scoped table without wiring
RLS will fail this check immediately — the failure list is the
actionable finding.

The CI ``backend-tests`` job runs ``alembic upgrade head`` and then
invokes this test as a dedicated pytest call before any other test
mutates the schema, so the introspection runs against the migrated
catalog.
"""

import pytest
from sqlalchemy import text

# Tables that intentionally lack RLS (e.g. global tables with no
# household scope). Every entry MUST include a comment justifying the
# exemption — a household_id column without RLS is almost always a bug.
ALLOWED_NO_RLS: set[str] = {
    # (no exemptions today — every household_id table is RLS-protected)
}


@pytest.mark.asyncio
async def test_every_household_scoped_table_has_rls(db_session):
    result = await db_session.execute(
        text(
            """
            SELECT table_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND column_name = 'household_id'
            """
        )
    )
    household_tables = {row[0] for row in result.all()}

    result = await db_session.execute(
        text(
            """
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
              AND rowsecurity = true
            """
        )
    )
    rls_enabled = {row[0] for row in result.all()}

    result = await db_session.execute(
        text(
            """
            SELECT DISTINCT tablename
            FROM pg_policies
            WHERE schemaname = 'public'
              AND qual LIKE '%app.current_household_id%'
            """
        )
    )
    policied = {row[0] for row in result.all()}

    missing_rls = household_tables - rls_enabled - ALLOWED_NO_RLS
    missing_policy = household_tables - policied - ALLOWED_NO_RLS

    assert not missing_rls, (
        f"Tables with household_id missing RLS: {sorted(missing_rls)}"
    )
    assert not missing_policy, (
        f"Tables with household_id missing isolation policy: {sorted(missing_policy)}"
    )
