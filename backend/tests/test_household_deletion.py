"""Tests for self-service household deletion and the purge task.

Covers migration 054: the 7-day soft-delete window, password
re-authentication on delete and restore, governance event logging,
the metadata-driven total purge (including the sanctioned append-only
trigger bypass), and isolation of unaffected households.
"""

import importlib.util
import uuid
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import func, select, text, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base, set_tenant
from app.core.security import hash_password
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import ActivityType, GovernanceAction, NodeType, StateEventType
from app.models.governance import Activity, GovernanceEvent, GovernanceRule, Plan, PlanWeek
from app.models.identity import Child, Household, User
from app.models.state import ChildNodeState, StateEvent
from app.services.governance import log_governance_event
from app.tasks.purge import purge_eligible_households, purge_household
from tests.conftest import test_engine as _test_engine
from tests.conftest import test_session_factory as _session_factory

PASSWORD = "testpass123"  # matches the conftest user fixture

# Apply migration 052's trigger DDL from the migration module itself so
# the purge tests exercise the exact production triggers.
_MIGRATION_PATH = Path(__file__).resolve().parents[1] / "alembic" / "versions" / "052_append_only_enforcement.py"
_spec = importlib.util.spec_from_file_location("migration_052_for_purge", _MIGRATION_PATH)
assert _spec is not None and _spec.loader is not None
_migration_052 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_migration_052)


@pytest_asyncio.fixture
async def append_only_triggers(db_session: AsyncSession) -> None:
    async with _test_engine.begin() as conn:
        await conn.execute(text(_migration_052.FORBID_MUTATION_FUNCTION_SQL))
        for table in _migration_052.APPEND_ONLY_TABLES:
            await conn.execute(text(f"DROP TRIGGER IF EXISTS {table}_forbid_mutation ON {table}"))
            await conn.execute(text(_migration_052.forbid_mutation_trigger_sql(table)))


@pytest_asyncio.fixture(autouse=True)
def _no_s3(monkeypatch):
    """Purge tests never talk to S3; the sweep is a separate unit."""
    import app.tasks.purge as purge_module

    monkeypatch.setattr(purge_module, "_delete_household_objects", lambda household_id: 0)


async def _populate_household(db: AsyncSession, household: Household, user_id: uuid.UUID) -> dict:
    """Seed one household with rows across 10+ tables, including a
    governance event and a state event (the trigger-protected pair)."""
    await set_tenant(db, household.id)
    child = Child(household_id=household.id, first_name="Purged")
    db.add(child)
    await db.flush()
    subject = Subject(household_id=household.id, name="Math")
    db.add(subject)
    await db.flush()
    lmap = LearningMap(household_id=household.id, subject_id=subject.id, name="Map")
    db.add(lmap)
    await db.flush()
    node = LearningNode(
        learning_map_id=lmap.id, household_id=household.id, node_type=NodeType.concept, title="Addition"
    )
    db.add(node)
    await db.flush()
    rule = GovernanceRule(
        household_id=household.id,
        rule_type="approval_required",
        name="Approve everything",
        parameters={},
    )
    db.add(rule)
    plan = Plan(household_id=household.id, child_id=child.id, name="Plan", status="active")
    db.add(plan)
    await db.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 6, 8),
        end_date=date(2026, 6, 14),
    )
    db.add(week)
    await db.flush()
    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        title="Practice",
        activity_type=ActivityType.practice,
        node_id=node.id,
    )
    db.add(activity)
    state = ChildNodeState(child_id=child.id, household_id=household.id, node_id=node.id)
    db.add(state)
    state_event = StateEvent(
        child_id=child.id,
        household_id=household.id,
        node_id=node.id,
        event_type=StateEventType.node_unlocked,
    )
    db.add(state_event)
    await db.flush()
    event = await log_governance_event(
        db,
        household.id,
        user_id,
        GovernanceAction.approve,
        "activity",
        activity.id,
        reason="seed",
    )
    await db.flush()
    return {"child": child, "activity": activity, "governance_event": event}


async def _count_household_rows(db: AsyncSession, household_id: uuid.UUID) -> dict[str, int]:
    """Metadata-driven count of rows referencing a household across
    every table that has a household_id column."""
    counts: dict[str, int] = {}
    for table in Base.metadata.sorted_tables:
        if "household_id" not in table.c:
            continue
        result = await db.execute(select(func.count()).select_from(table).where(table.c.household_id == household_id))
        n = result.scalar() or 0
        if n:
            counts[table.name] = n
    return counts


# ── Deletion endpoint ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_delete_requires_password_field(auth_client: AsyncClient):
    response = await auth_client.request("DELETE", "/api/v1/household", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_wrong_password_403(auth_client: AsyncClient, db_session, household):
    response = await auth_client.request("DELETE", "/api/v1/household", json={"password": "wrong-pass"})
    assert response.status_code == 403
    refreshed = await db_session.get(Household, household.id)
    assert refreshed.deletion_requested_at is None


@pytest.mark.asyncio
async def test_child_token_cannot_delete(auth_client: AsyncClient, child):
    enter = await auth_client.post("/api/v1/auth/child-session/enter", json={"child_id": str(child.id)})
    assert enter.status_code == 200
    response = await auth_client.request("DELETE", "/api/v1/household", json={"password": PASSWORD})
    assert response.status_code == 403
    assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_co_parent_cannot_delete(co_parent_client: AsyncClient):
    response = await co_parent_client.request("DELETE", "/api/v1/household", json={"password": "xxxxxxxx"})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_sets_fields_cancels_subscription_emails_and_logs(
    auth_client: AsyncClient, db_session, household, user
):
    with (
        patch("app.services.billing.cancel_subscription", new_callable=AsyncMock, return_value=True) as cancel,
        patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True) as email,
    ):
        response = await auth_client.request("DELETE", "/api/v1/household", json={"password": PASSWORD})
    assert response.status_code == 200
    data = response.json()
    assert data["pending"] is True and data["purge_after"]

    refreshed = await db_session.get(Household, household.id)
    assert refreshed.deletion_requested_at is not None
    assert refreshed.deletion_requested_by == user.id

    cancel.assert_awaited_once()
    assert cancel.await_args.kwargs.get("at_period_end") is False
    email.assert_awaited_once()
    assert email.await_args.args[0] == user.email

    events = await db_session.execute(
        select(GovernanceEvent).where(
            GovernanceEvent.household_id == household.id,
            GovernanceEvent.target_type == "household_deletion_requested",
        )
    )
    assert events.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_delete_twice_conflicts(auth_client: AsyncClient):
    first = await auth_client.request("DELETE", "/api/v1/household", json={"password": PASSWORD})
    assert first.status_code == 200
    second = await auth_client.request("DELETE", "/api/v1/household", json={"password": PASSWORD})
    assert second.status_code == 409


# ── Restore endpoint ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_restore_requires_correct_password(auth_client: AsyncClient, db_session, household):
    assert (await auth_client.request("DELETE", "/api/v1/household", json={"password": PASSWORD})).status_code == 200
    denied = await auth_client.post("/api/v1/household/restore", json={"password": "nope"})
    assert denied.status_code == 403
    refreshed = await db_session.get(Household, household.id)
    assert refreshed.deletion_requested_at is not None


@pytest.mark.asyncio
async def test_restore_within_window_clears_fields_and_logs(auth_client: AsyncClient, db_session, household):
    assert (await auth_client.request("DELETE", "/api/v1/household", json={"password": PASSWORD})).status_code == 200
    with patch("app.services.email.send_email", new_callable=AsyncMock, return_value=True) as email:
        response = await auth_client.post("/api/v1/household/restore", json={"password": PASSWORD})
    assert response.status_code == 200
    assert response.json() == {"pending": False, "purge_after": None}

    refreshed = await db_session.get(Household, household.id)
    assert refreshed.deletion_requested_at is None
    assert refreshed.deletion_requested_by is None
    email.assert_awaited_once()

    events = await db_session.execute(
        select(GovernanceEvent).where(
            GovernanceEvent.household_id == household.id,
            GovernanceEvent.target_type == "household_deletion_restored",
        )
    )
    assert events.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_restore_without_pending_deletion_conflicts(auth_client: AsyncClient):
    response = await auth_client.post("/api/v1/household/restore", json={"password": PASSWORD})
    assert response.status_code == 409


# ── Status endpoint ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_status_reports_all_three_states(auth_client: AsyncClient):
    initial = await auth_client.get("/api/v1/household/deletion-status")
    assert initial.status_code == 200
    assert initial.json() == {"pending": False, "purge_after": None}

    assert (await auth_client.request("DELETE", "/api/v1/household", json={"password": PASSWORD})).status_code == 200
    pending = await auth_client.get("/api/v1/household/deletion-status")
    assert pending.json()["pending"] is True
    assert pending.json()["purge_after"] is not None

    assert (await auth_client.post("/api/v1/household/restore", json={"password": PASSWORD})).status_code == 200
    restored = await auth_client.get("/api/v1/household/deletion-status")
    assert restored.json() == {"pending": False, "purge_after": None}


# ── Purge task ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_purge_ignores_households_inside_window(db_session, household, user, append_only_triggers):
    await _populate_household(db_session, household, user.id)
    household.deletion_requested_at = datetime.now(UTC) - timedelta(days=3)
    household.deletion_requested_by = user.id
    await db_session.commit()

    report = await purge_eligible_households(session_factory=_session_factory)
    assert report["purged"] == 0

    async with _session_factory() as check:
        still_there = await check.get(Household, household.id)
        assert still_there is not None


@pytest.mark.asyncio
async def test_purge_removes_every_row_across_all_tables(db_session, household, user, append_only_triggers):
    await _populate_household(db_session, household, user.id)
    household.deletion_requested_at = datetime.now(UTC) - timedelta(days=8)
    household.deletion_requested_by = user.id
    await db_session.commit()

    before = await _count_household_rows(db_session, household.id)
    assert len(before) >= 10, f"seed produced rows in only {len(before)} tables: {before}"
    assert "governance_events" in before and "state_events" in before

    report = await purge_eligible_households(session_factory=_session_factory)
    assert report["purged"] == 1

    async with _session_factory() as check:
        leftovers = await _count_household_rows(check, household.id)
        assert leftovers == {}, f"orphan rows after purge: {leftovers}"
        assert await check.get(Household, household.id) is None


@pytest.mark.asyncio
async def test_purge_is_idempotent(db_session, household, user, append_only_triggers):
    await _populate_household(db_session, household, user.id)
    household.deletion_requested_at = datetime.now(UTC) - timedelta(days=8)
    await db_session.commit()

    first = await purge_eligible_households(session_factory=_session_factory)
    assert first["purged"] == 1
    second = await purge_eligible_households(session_factory=_session_factory)
    assert second["purged"] == 0 and second["eligible"] == 0


@pytest.mark.asyncio
async def test_purge_leaves_other_households_untouched(db_session, household, user, append_only_triggers):
    await _populate_household(db_session, household, user.id)

    other = Household(name="Survivor Family", timezone="UTC")
    db_session.add(other)
    await db_session.flush()
    other_user = User(
        household_id=other.id,
        email="survivor@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Survivor",
        role="owner",
        email_verified=True,
    )
    db_session.add(other_user)
    await db_session.flush()
    await _populate_household(db_session, other, other_user.id)

    household.deletion_requested_at = datetime.now(UTC) - timedelta(days=8)
    await db_session.commit()

    report = await purge_eligible_households(session_factory=_session_factory)
    assert report["purged"] == 1

    async with _session_factory() as check:
        await set_tenant(check, other.id)
        survivor_rows = await _count_household_rows(check, other.id)
        assert len(survivor_rows) >= 10
        assert await check.get(Household, other.id) is not None


@pytest.mark.asyncio
async def test_triggers_reenabled_after_purge(db_session, household, user, append_only_triggers):
    await _populate_household(db_session, household, user.id)

    other = Household(name="Other Family", timezone="UTC")
    db_session.add(other)
    await db_session.flush()
    await set_tenant(db_session, other.id)
    other_event = await log_governance_event(
        db_session, other.id, None, GovernanceAction.approve, "activity", uuid.uuid4(), reason="keep"
    )

    household.deletion_requested_at = datetime.now(UTC) - timedelta(days=8)
    await db_session.commit()

    report = await purge_eligible_households(session_factory=_session_factory)
    assert report["purged"] == 1

    async with _session_factory() as check:
        await set_tenant(check, other.id)
        with pytest.raises(DBAPIError, match="append-only"):
            await check.execute(
                update(GovernanceEvent).where(GovernanceEvent.id == other_event.id).values(reason="tampered")
            )
        await check.rollback()


@pytest.mark.asyncio
async def test_purge_household_returns_per_table_counts(db_session, household, user, append_only_triggers):
    await _populate_household(db_session, household, user.id)
    await db_session.commit()

    async with _session_factory() as session:
        counts = await purge_household(session, household.id)
        await session.commit()
    assert counts.get("governance_events", 0) >= 1
    assert counts.get("state_events", 0) >= 1
    assert counts.get("children", 0) >= 1
    assert counts.get("households") == 1
