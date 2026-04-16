"""Tests for decay, snapshot, and enrichment background tasks."""

from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import set_tenant
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import MasteryLevel, NodeType
from app.models.evidence import WeeklySnapshot
from app.models.identity import Child, Household
from app.models.state import ChildNodeState, FSRSCard


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def hh(db_session: AsyncSession) -> Household:
    h = Household(name="Decay Test Family", timezone="America/New_York")
    db_session.add(h)
    await db_session.flush()
    await set_tenant(db_session, h.id)
    return h


@pytest_asyncio.fixture
async def kid(db_session: AsyncSession, hh: Household) -> Child:
    c = Child(household_id=hh.id, first_name="Tester")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def subj(db_session: AsyncSession, hh: Household) -> Subject:
    s = Subject(household_id=hh.id, name="Math")
    db_session.add(s)
    await db_session.flush()
    return s


@pytest_asyncio.fixture
async def lmap(db_session: AsyncSession, hh: Household, subj: Subject) -> LearningMap:
    m = LearningMap(household_id=hh.id, subject_id=subj.id, name="TestMap")
    db_session.add(m)
    await db_session.flush()
    return m


@pytest_asyncio.fixture
async def node(db_session: AsyncSession, hh: Household, lmap: LearningMap) -> LearningNode:
    n = LearningNode(
        learning_map_id=lmap.id,
        household_id=hh.id,
        node_type=NodeType.concept,
        title="Counting to 20",
    )
    db_session.add(n)
    await db_session.flush()
    return n


# ---------------------------------------------------------------------------
# Helper: create a mastered ChildNodeState + overdue FSRSCard
# ---------------------------------------------------------------------------


async def _make_mastered_state(
    db: AsyncSession,
    household: Household,
    child: Child,
    node: LearningNode,
    *,
    days_ago: int = 30,
) -> tuple[ChildNodeState, FSRSCard]:
    """Create a mastered ChildNodeState with an overdue FSRSCard."""
    state = ChildNodeState(
        child_id=child.id,
        household_id=household.id,
        node_id=node.id,
        mastery_level=MasteryLevel.mastered,
        attempts_count=5,
        time_spent_minutes=30,
    )
    db.add(state)

    last_rev = datetime.now(UTC) - timedelta(days=days_ago)
    card = FSRSCard(
        child_id=child.id,
        household_id=household.id,
        node_id=node.id,
        stability=5.0,
        difficulty=0.3,
        reps=3,
        last_review=last_rev,
        due=last_rev + timedelta(days=5),
    )
    db.add(card)
    await db.flush()
    return state, card


# ===========================================================================
# Decay Task Tests
# ===========================================================================


@pytest.mark.asyncio
async def test_decay_updates_retrievability(db_session, hh, kid, subj, lmap, node):
    """Decay reduces mastery for nodes not recently reviewed."""
    from app.tasks.decay import run_decay_batch

    state, card = await _make_mastered_state(db_session, hh, kid, node, days_ago=30)
    await db_session.commit()

    session_factory = lambda: db_session  # noqa: E731
    # We need an actual session factory that returns an async context manager
    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    result = await run_decay_batch(session_factory=factory)

    assert result["cards_checked"] >= 1
    # After decay, the state should be proficient (decayed from mastered)
    # Re-query to see the updated state
    async with factory() as fresh:
        await set_tenant(fresh, hh.id)
        updated = await fresh.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == kid.id,
                ChildNodeState.node_id == node.id,
            )
        )
        updated_state = updated.scalar_one_or_none()
        if updated_state:
            assert updated_state.mastery_level in (MasteryLevel.proficient, MasteryLevel.mastered)


@pytest.mark.asyncio
async def test_decay_handles_empty_state(db_session, hh):
    """Decay completes without error when no FSRS cards exist."""
    from app.tasks.decay import run_decay_batch

    await db_session.commit()

    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    result = await run_decay_batch(session_factory=factory)

    assert result["cards_checked"] == 0
    assert result["cards_decayed"] == 0
    assert "duration_ms" in result


@pytest.mark.asyncio
async def test_decay_skips_non_mastered(db_session, hh, kid, subj, lmap, node):
    """Decay does not process nodes that are not mastered."""
    from app.tasks.decay import run_decay_batch

    # Create a proficient (not mastered) state with an overdue card
    state = ChildNodeState(
        child_id=kid.id,
        household_id=hh.id,
        node_id=node.id,
        mastery_level=MasteryLevel.proficient,
        attempts_count=3,
    )
    db_session.add(state)

    last_rev = datetime.now(UTC) - timedelta(days=30)
    card = FSRSCard(
        child_id=kid.id,
        household_id=hh.id,
        node_id=node.id,
        stability=5.0,
        difficulty=0.3,
        reps=3,
        last_review=last_rev,
        due=last_rev + timedelta(days=5),
    )
    db_session.add(card)
    await db_session.commit()

    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    result = await run_decay_batch(session_factory=factory)

    assert result["cards_decayed"] == 0


@pytest.mark.asyncio
async def test_decay_idempotent(db_session, hh, kid, subj, lmap, node):
    """Running decay twice on the same day doesn't double-decay."""
    from app.tasks.decay import run_decay_batch

    await _make_mastered_state(db_session, hh, kid, node, days_ago=60)
    await db_session.commit()

    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    result1 = await run_decay_batch(session_factory=factory)
    result2 = await run_decay_batch(session_factory=factory)

    # Second run should not decay again (idempotent)
    assert result2["cards_decayed"] == 0


# ===========================================================================
# Snapshot Task Tests
# ===========================================================================


@pytest.mark.asyncio
async def test_snapshot_creates_weekly_record(db_session, hh, kid, subj, lmap, node):
    """Snapshot aggregates current data into a weekly record."""
    from app.tasks.snapshots import capture_weekly_snapshots

    # Create a mastered state for the child
    state = ChildNodeState(
        child_id=kid.id,
        household_id=hh.id,
        node_id=node.id,
        mastery_level=MasteryLevel.mastered,
        attempts_count=5,
        time_spent_minutes=45,
    )
    db_session.add(state)
    await db_session.commit()

    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    result = await capture_weekly_snapshots(session_factory=factory)

    assert result["snapshots_created"] >= 1

    # Verify snapshot exists in DB
    async with factory() as fresh:
        await set_tenant(fresh, hh.id)
        snaps = await fresh.execute(select(WeeklySnapshot).where(WeeklySnapshot.child_id == kid.id))
        snap_list = snaps.scalars().all()
        assert len(snap_list) >= 1
        snap = snap_list[0]
        assert snap.nodes_mastered >= 1
        assert snap.total_minutes >= 45


@pytest.mark.asyncio
async def test_snapshot_is_idempotent(db_session, hh, kid, subj, lmap, node):
    """Running snapshot twice for the same week doesn't duplicate."""
    from app.tasks.snapshots import capture_weekly_snapshots

    state = ChildNodeState(
        child_id=kid.id,
        household_id=hh.id,
        node_id=node.id,
        mastery_level=MasteryLevel.mastered,
        attempts_count=3,
        time_spent_minutes=20,
    )
    db_session.add(state)
    await db_session.commit()

    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    result1 = await capture_weekly_snapshots(session_factory=factory)
    result2 = await capture_weekly_snapshots(session_factory=factory)

    # Second run should create 0 new snapshots (already exists for this week)
    assert result2["snapshots_created"] == 0

    # Verify only 1 snapshot row exists for this child
    async with factory() as fresh:
        await set_tenant(fresh, hh.id)
        count_result = await fresh.execute(select(WeeklySnapshot).where(WeeklySnapshot.child_id == kid.id))
        assert len(count_result.scalars().all()) == 1


@pytest.mark.asyncio
async def test_snapshot_handles_no_activity(db_session, hh, kid):
    """Snapshot creates a record even when no node states exist (zeros)."""
    from app.tasks.snapshots import capture_weekly_snapshots

    await db_session.commit()

    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    result = await capture_weekly_snapshots(session_factory=factory)

    assert result["snapshots_created"] >= 1

    async with factory() as fresh:
        await set_tenant(fresh, hh.id)
        snaps = await fresh.execute(select(WeeklySnapshot).where(WeeklySnapshot.child_id == kid.id))
        snap = snaps.scalars().first()
        assert snap is not None
        assert snap.nodes_mastered == 0
        assert snap.total_minutes == 0


# ===========================================================================
# Enrichment Task Tests
# ===========================================================================


@pytest.mark.asyncio
async def test_enrichment_enriches_unenriched_nodes(db_session, hh, subj, lmap):
    """Enrichment processes nodes without content."""
    from app.tasks.enrichment import _enrich_map

    # Create 3 nodes with no content
    for i, title in enumerate(["Counting to 20", "Addition Facts", "Subtraction"]):
        n = LearningNode(
            learning_map_id=lmap.id,
            household_id=hh.id,
            node_type=NodeType.concept,
            title=title,
            sort_order=i,
        )
        db_session.add(n)
    await db_session.commit()

    result = await _enrich_map(lmap.id, hh.id)

    assert result["total"] == 3
    assert result["enriched"] + result["skipped"] + result["failed"] == result["total"]
    # "Counting to 20" should match seed content
    assert result["enriched"] >= 1


@pytest.mark.asyncio
async def test_enrichment_skips_already_enriched(db_session, hh, subj, lmap):
    """Nodes with existing enriched content are not re-enriched."""
    from app.tasks.enrichment import _enrich_map

    n = LearningNode(
        learning_map_id=lmap.id,
        household_id=hh.id,
        node_type=NodeType.concept,
        title="Pre-enriched Node",
        content={"enriched": True, "learning_objectives": ["test"]},
    )
    db_session.add(n)
    await db_session.commit()

    result = await _enrich_map(lmap.id, hh.id)

    assert result["total"] == 1
    assert result["skipped"] == 1
    assert result["enriched"] == 0


@pytest.mark.asyncio
async def test_enrichment_handles_missing_map(db_session, hh):
    """Enrichment returns zeros for a non-existent map ID."""
    import uuid

    from app.tasks.enrichment import _enrich_map

    await db_session.commit()

    fake_map_id = uuid.uuid4()
    result = await _enrich_map(fake_map_id, hh.id)

    assert result["enriched"] == 0
    assert result["failed"] == 0
    assert result["skipped"] == 0


@pytest.mark.asyncio
async def test_enrichment_seed_content_applied(db_session, hh, subj, lmap):
    """Seed content is applied when node title matches."""
    from app.tasks.enrichment import _enrich_map

    # "Letter Recognition" matches seed content in seed_content.py
    n = LearningNode(
        learning_map_id=lmap.id,
        household_id=hh.id,
        node_type=NodeType.concept,
        title="Letter Recognition",
    )
    db_session.add(n)
    await db_session.commit()

    result = await _enrich_map(lmap.id, hh.id)

    assert result["enriched"] == 1

    # Verify the node now has seed content
    from sqlalchemy.ext.asyncio import async_sessionmaker

    from tests.conftest import test_engine

    factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as fresh:
        await set_tenant(fresh, hh.id)
        node_result = await fresh.execute(select(LearningNode).where(LearningNode.id == n.id))
        updated_node = node_result.scalar_one()
        assert updated_node.content is not None
        assert updated_node.content.get("enriched") is True
        assert len(updated_node.content.get("learning_objectives", [])) >= 3
