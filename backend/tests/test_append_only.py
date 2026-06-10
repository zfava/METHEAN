"""Tests for database-enforced append-only audit and the governance hash chain.

Covers migration 052: BEFORE UPDATE OR DELETE triggers on
governance_events and state_events, the canonical SHA-256 hash chain
written by log_governance_event, the pure verify_chain function, and
the parent-facing GET /chain/verify endpoint.

The conftest schema is built with create_all (no alembic), so the
trigger DDL is loaded straight from the migration module and applied
by a fixture: the tests exercise the exact DDL production runs.
"""

import asyncio
import hashlib
import importlib.util
import json
import uuid
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete, select, text, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import set_tenant
from app.core.security import create_access_token, hash_password
from app.models.curriculum import LearningMap, LearningNode
from app.models.enums import GovernanceAction, NodeType, StateEventType
from app.models.governance import GovernanceEvent
from app.models.identity import Child, Household, User
from app.models.state import StateEvent
from app.services.governance import (
    GENESIS_SENTINEL,
    build_governance_hash_payload,
    compute_event_hash,
    log_governance_event,
    verify_chain,
)

# Aliased so pytest does not try to collect the imported names as tests.
from tests.conftest import test_engine as _test_engine
from tests.conftest import test_session_factory as _session_factory

# Load migration 052 by path (the module name starts with a digit, so a
# normal import cannot reach it). This keeps a single source of truth
# for the trigger DDL instead of copying SQL into the tests.
_MIGRATION_PATH = Path(__file__).resolve().parents[1] / "alembic" / "versions" / "052_append_only_enforcement.py"
_spec = importlib.util.spec_from_file_location("migration_052_append_only", _MIGRATION_PATH)
assert _spec is not None and _spec.loader is not None
_migration_052 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_migration_052)


@pytest_asyncio.fixture
async def append_only_triggers(db_session: AsyncSession) -> None:
    """Apply migration 052's trigger function and triggers to the test schema.

    Runs on its own committed connection so the DDL is visible to the
    test session. The triggers are dropped with the tables at teardown.
    """
    async with _test_engine.begin() as conn:
        await conn.execute(text(_migration_052.FORBID_MUTATION_FUNCTION_SQL))
        for table in _migration_052.APPEND_ONLY_TABLES:
            await conn.execute(text(f"DROP TRIGGER IF EXISTS {table}_forbid_mutation ON {table}"))
            await conn.execute(text(_migration_052.forbid_mutation_trigger_sql(table)))


async def _log_event(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID | None = None,
    reason: str = "approved",
) -> GovernanceEvent:
    return await log_governance_event(
        db,
        household_id,
        user_id,
        GovernanceAction.approve,
        "activity",
        uuid.uuid4(),
        reason=reason,
        metadata={"source": "test"},
    )


async def _make_state_event(
    db: AsyncSession,
    household: Household,
    child: Child,
    learning_map: LearningMap,
) -> StateEvent:
    node = LearningNode(
        household_id=household.id,
        learning_map_id=learning_map.id,
        node_type=NodeType.skill,
        title="Counting to 10",
    )
    db.add(node)
    await db.flush()
    state_event = StateEvent(
        child_id=child.id,
        household_id=household.id,
        node_id=node.id,
        event_type=StateEventType.node_unlocked,
        from_state="locked",
        to_state="unlocked",
    )
    db.add(state_event)
    await db.flush()
    return state_event


def _event_chain_dict(event: GovernanceEvent) -> dict:
    return {
        **build_governance_hash_payload(
            household_id=event.household_id,
            user_id=event.user_id,
            action=event.action,
            target_type=event.target_type,
            target_id=event.target_id,
            reason=event.reason,
            metadata=event.metadata_,
            created_at=event.created_at,
        ),
        "event_hash": event.event_hash,
        "prev_event_hash": event.prev_event_hash,
    }


def _fabricate_chain(count: int = 5) -> list[dict]:
    household_id = str(uuid.uuid4())
    events: list[dict] = []
    prev_hash: str | None = None
    for i in range(count):
        payload = build_governance_hash_payload(
            household_id=household_id,
            user_id=None,
            action=GovernanceAction.approve,
            target_type="activity",
            target_id=str(uuid.uuid4()),
            reason=f"reason {i}",
            metadata={"index": i},
            created_at=f"2026-06-09T00:00:0{i}+00:00",
        )
        event_hash = compute_event_hash(payload, prev_hash)
        events.append({**payload, "event_hash": event_hash, "prev_event_hash": prev_hash})
        prev_hash = event_hash
    return events


# ── Trigger enforcement ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_update_governance_event_raises(db_session, household, append_only_triggers):
    event = await _log_event(db_session, household.id)
    with pytest.raises(DBAPIError, match="append-only"):
        await db_session.execute(
            update(GovernanceEvent).where(GovernanceEvent.id == event.id).values(reason="tampered")
        )
    await db_session.rollback()


@pytest.mark.asyncio
async def test_delete_governance_event_raises(db_session, household, append_only_triggers):
    event = await _log_event(db_session, household.id)
    with pytest.raises(DBAPIError, match="append-only"):
        await db_session.execute(delete(GovernanceEvent).where(GovernanceEvent.id == event.id))
    await db_session.rollback()


@pytest.mark.asyncio
async def test_update_state_event_raises(db_session, household, child, learning_map, append_only_triggers):
    state_event = await _make_state_event(db_session, household, child, learning_map)
    with pytest.raises(DBAPIError, match="append-only"):
        await db_session.execute(update(StateEvent).where(StateEvent.id == state_event.id).values(to_state="mastered"))
    await db_session.rollback()


@pytest.mark.asyncio
async def test_delete_state_event_raises(db_session, household, child, learning_map, append_only_triggers):
    state_event = await _make_state_event(db_session, household, child, learning_map)
    with pytest.raises(DBAPIError, match="append-only"):
        await db_session.execute(delete(StateEvent).where(StateEvent.id == state_event.id))
    await db_session.rollback()


# ── Canonical hash algorithm ────────────────────────────────────────


def test_compute_event_hash_deterministic_and_key_order_insensitive():
    payload_a = {"household_id": "h1", "action": "approve", "metadata": {"x": 1}}
    payload_b = {"metadata": {"x": 1}, "action": "approve", "household_id": "h1"}
    assert compute_event_hash(payload_a, None) == compute_event_hash(payload_a, None)
    assert compute_event_hash(payload_a, None) == compute_event_hash(payload_b, None)
    assert compute_event_hash(payload_a, "aa") != compute_event_hash(payload_a, "bb")
    assert compute_event_hash({"household_id": "h2"}, None) != compute_event_hash(payload_a, None)


def test_genesis_event_hashes_with_genesis_sentinel():
    payload = {"household_id": "h1", "action": "approve"}
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    expected = hashlib.sha256((GENESIS_SENTINEL + serialized).encode("utf-8")).hexdigest()
    assert GENESIS_SENTINEL == "GENESIS"
    assert compute_event_hash(payload, None) == expected
    assert compute_event_hash(payload, "GENESIS") == expected


@pytest.mark.asyncio
async def test_sequential_events_chain(db_session, household, user):
    first = await _log_event(db_session, household.id, user.id, reason="first")
    second = await _log_event(db_session, household.id, user.id, reason="second")
    assert first.prev_event_hash is None
    assert first.event_hash is not None and len(first.event_hash) == 64
    assert second.prev_event_hash == first.event_hash
    assert second.event_hash != first.event_hash


# ── verify_chain (pure) ─────────────────────────────────────────────


def test_verify_chain_empty_is_valid():
    assert verify_chain([]) == {"valid": True, "checked": 0, "first_break_index": None}


def test_verify_chain_valid_on_intact_chain():
    events = _fabricate_chain(5)
    assert verify_chain(events) == {"valid": True, "checked": 5, "first_break_index": None}


def test_verify_chain_pinpoints_altered_detail():
    events = _fabricate_chain(5)
    events[2]["reason"] = "tampered after the fact"
    report = verify_chain(events)
    assert report["valid"] is False
    assert report["first_break_index"] == 2


def test_verify_chain_pinpoints_swapped_prev_hash():
    events = _fabricate_chain(5)
    events[3]["prev_event_hash"] = events[0]["event_hash"]
    report = verify_chain(events)
    assert report["valid"] is False
    assert report["first_break_index"] == 3


# ── Concurrency and household isolation in the service ──────────────


@pytest.mark.asyncio
async def test_concurrent_appends_produce_unbroken_chain(db_session, household):
    household_id = household.id
    # Commit so the household row is visible to the workers' own sessions.
    await db_session.commit()

    async def append(i: int) -> None:
        async with _session_factory() as session:
            await set_tenant(session, household_id)
            await log_governance_event(
                session,
                household_id,
                None,
                GovernanceAction.approve,
                "activity",
                uuid.uuid4(),
                reason=f"concurrent {i}",
            )
            await session.commit()

    await asyncio.gather(*(append(i) for i in range(5)))

    async with _session_factory() as session:
        await set_tenant(session, household_id)
        result = await session.execute(
            select(GovernanceEvent)
            .where(GovernanceEvent.household_id == household_id)
            .order_by(GovernanceEvent.created_at.asc(), GovernanceEvent.id.asc())
        )
        events = result.scalars().all()
        report = verify_chain([_event_chain_dict(e) for e in events])
    assert report == {"valid": True, "checked": 5, "first_break_index": None}


@pytest.mark.asyncio
async def test_two_households_interleave_without_cross_linking(db_session, household):
    other = Household(name="Other Family", timezone="UTC")
    db_session.add(other)
    await db_session.flush()

    a1 = await _log_event(db_session, household.id, reason="a1")
    await set_tenant(db_session, other.id)
    b1 = await _log_event(db_session, other.id, reason="b1")
    await set_tenant(db_session, household.id)
    a2 = await _log_event(db_session, household.id, reason="a2")

    assert a1.prev_event_hash is None
    assert b1.prev_event_hash is None
    assert a2.prev_event_hash == a1.event_hash
    assert b1.event_hash not in {a1.event_hash, a2.event_hash}


# ── GET /chain/verify endpoint ──────────────────────────────────────


@pytest.mark.asyncio
async def test_chain_verify_endpoint_valid(auth_client: AsyncClient, db_session, household, user):
    events = [await _log_event(db_session, household.id, user.id, reason=f"event {i}") for i in range(3)]
    response = await auth_client.get("/api/v1/chain/verify")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["checked"] == 3
    assert data["head_hash"] == events[-1].event_hash
    assert data["first_break_index"] is None


@pytest.mark.asyncio
async def test_chain_verify_endpoint_requires_auth(client: AsyncClient):
    response = await client.get("/api/v1/chain/verify")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_chain_verify_endpoint_rejects_observer(observer_client: AsyncClient):
    response = await observer_client.get("/api/v1/chain/verify")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_chain_verify_endpoint_household_isolation(client: AsyncClient, db_session, household, user):
    a_events = [await _log_event(db_session, household.id, user.id, reason=f"a{i}") for i in range(2)]

    other = Household(name="Household B", timezone="UTC")
    db_session.add(other)
    await db_session.flush()
    await set_tenant(db_session, other.id)
    user_b = User(
        household_id=other.id,
        email="parent-b@test.com",
        password_hash=hash_password("testpass123"),
        display_name="Parent B",
        role="owner",
        email_verified=True,
    )
    db_session.add(user_b)
    await db_session.flush()

    token = create_access_token(user_b.id, other.id, "owner")
    client.cookies.set("access_token", token)
    response = await client.get("/api/v1/chain/verify")
    assert response.status_code == 200
    data = response.json()
    assert data["checked"] == 0
    assert data["head_hash"] is None
    assert data["head_hash"] != a_events[-1].event_hash
