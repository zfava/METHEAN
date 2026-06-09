"""Read-only child-wide demotion feed: GET /children/{child_id}/demotions.

The feed returns recent StateEvents that carry a ``demotion_explanation``
envelope (written in Phase 1), newest first, paginated, scoped to the child's
household. That single predicate captures both the attempt path and the decay
path; ordinary reviews never appear. No em dashes.
"""

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import set_tenant
from app.models.curriculum import LearningNode
from app.models.enums import MasteryLevel, NodeType, StateEventType
from app.models.identity import Child, Household
from app.models.state import ChildNodeState, FSRSCard
from app.services.state_engine import (
    build_demotion_explanation,
    emit_state_event,
    process_review,
)

DEMOTIONS_URL = "/api/v1/children/{child_id}/demotions"


# ── Helpers ──────────────────────────────────────────────────────────────


async def _make_node(db, household, learning_map, title) -> LearningNode:
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title=title,
    )
    db.add(node)
    await db.flush()
    return node


async def _emit_decay_demotion(db, child, household, node):
    """Reproduce the decay path's StateEvent row: mastered -> proficient,
    trigger='decay', carrying a retention_decay demotion_explanation."""
    db.add(
        ChildNodeState(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            mastery_level=MasteryLevel.proficient,
            attempts_count=5,
        )
    )
    await db.flush()
    return await emit_state_event(
        db,
        child.id,
        household.id,
        node.id,
        event_type=StateEventType.mastery_change,
        from_state=MasteryLevel.mastered.value,
        to_state=MasteryLevel.proficient.value,
        trigger="decay",
        metadata={
            "retrievability": 0.38,
            "fsrs_stability": 2.0,
            "demotion_explanation": build_demotion_explanation(
                MasteryLevel.mastered,
                MasteryLevel.proficient,
                cause="retention_decay",
                retrievability=0.38,
                fsrs_stability=2.0,
                threshold_crossed=0.5,
            ),
        },
    )


# ── Core feed behaviour ────────────────────────────────────────────────────


class TestDemotionFeed:
    @pytest.mark.asyncio
    async def test_feed_returns_both_causes_newest_first(self, auth_client, db_session, household, learning_map, child):
        # Attempt-caused demotion: reach mastered, then a below-line attempt.
        attempt_node = await _make_node(db_session, household, learning_map, "Attempt Node")
        await process_review(db_session, child.id, household.id, attempt_node.id, confidence=0.95)
        attempt_result = await process_review(db_session, child.id, household.id, attempt_node.id, confidence=0.7)
        assert attempt_result["previous_mastery"] == MasteryLevel.mastered
        assert attempt_result["mastery_level"] == MasteryLevel.proficient

        # Decay-caused demotion. In production this is a separate transaction;
        # here both events share one transaction (so server-side now() ties),
        # so we set an explicitly later created_at to make "newest" meaningful.
        decay_node = await _make_node(db_session, household, learning_map, "Decay Node")
        decay_event = await _emit_decay_demotion(db_session, child, household, decay_node)
        decay_event.created_at = datetime.now(UTC) + timedelta(minutes=1)

        # A normal review (promotion, no envelope) must never appear.
        normal_node = await _make_node(db_session, household, learning_map, "Normal Node")
        await process_review(db_session, child.id, household.id, normal_node.id, confidence=0.95)

        await db_session.flush()

        resp = await auth_client.get(DEMOTIONS_URL.format(child_id=child.id))
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 2
        assert body["skip"] == 0
        assert len(body["items"]) == 2

        # Newest first: the decay demotion was emitted last.
        first, second = body["items"]
        assert first["id"] == str(decay_event.id)
        assert first["trigger"] == "decay"
        assert first["explanation"]["cause"] == "retention_decay"
        assert second["trigger"] == "attempt"
        assert second["explanation"]["cause"] == "low_confidence_attempt"

        # Every item carries a populated explanation envelope; the normal node
        # never appears.
        node_ids = {it["node_id"] for it in body["items"]}
        assert str(normal_node.id) not in node_ids
        for it in body["items"]:
            assert it["explanation"]["from_level"]
            assert it["explanation"]["to_level"]
            assert it["explanation"]["human_summary"]
            assert it["event_type"] == StateEventType.mastery_change.value

    @pytest.mark.asyncio
    async def test_normal_review_only_yields_empty_feed(self, auth_client, db_session, household, learning_map, child):
        node = await _make_node(db_session, household, learning_map, "Only Normal")
        await process_review(db_session, child.id, household.id, node.id, confidence=0.95)
        await db_session.flush()

        resp = await auth_client.get(DEMOTIONS_URL.format(child_id=child.id))
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 0
        assert body["items"] == []

    @pytest.mark.asyncio
    async def test_pagination(self, auth_client, db_session, household, learning_map, child):
        # Three decay demotions across three nodes.
        for i in range(3):
            node = await _make_node(db_session, household, learning_map, f"Paginate {i}")
            await _emit_decay_demotion(db_session, child, household, node)
        await db_session.flush()

        page1 = (await auth_client.get(DEMOTIONS_URL.format(child_id=child.id), params={"skip": 0, "limit": 2})).json()
        assert page1["total"] == 3
        assert page1["limit"] == 2
        assert len(page1["items"]) == 2

        page2 = (await auth_client.get(DEMOTIONS_URL.format(child_id=child.id), params={"skip": 2, "limit": 2})).json()
        assert page2["total"] == 3
        assert page2["skip"] == 2
        assert len(page2["items"]) == 1

        # No overlap across pages.
        ids1 = {it["id"] for it in page1["items"]}
        ids2 = {it["id"] for it in page2["items"]}
        assert ids1.isdisjoint(ids2)

    @pytest.mark.asyncio
    async def test_real_decay_job_surfaces_in_feed(self, auth_client, db_session, household, learning_map, child):
        """End to end: the actual decay job's emitted event appears in the feed."""
        from app.tasks.decay import run_decay_batch
        from tests.conftest import test_engine

        node = await _make_node(db_session, household, learning_map, "Real Decay")
        db_session.add(
            ChildNodeState(
                child_id=child.id,
                household_id=household.id,
                node_id=node.id,
                mastery_level=MasteryLevel.mastered,
                attempts_count=5,
            )
        )
        last_rev = datetime.now(UTC) - timedelta(days=30)
        db_session.add(
            FSRSCard(
                child_id=child.id,
                household_id=household.id,
                node_id=node.id,
                stability=2.0,  # over 30 days -> retrievability ~0.38, below threshold
                difficulty=0.3,
                reps=3,
                last_review=last_rev,
                due=last_rev + timedelta(days=5),
            )
        )
        await db_session.commit()

        factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
        result = await run_decay_batch(session_factory=factory)
        assert result["cards_decayed"] >= 1

        resp = await auth_client.get(DEMOTIONS_URL.format(child_id=child.id))
        assert resp.status_code == 200
        items = resp.json()["items"]
        decay_items = [it for it in items if it["node_id"] == str(node.id)]
        assert len(decay_items) == 1
        assert decay_items[0]["trigger"] == "decay"
        assert decay_items[0]["explanation"]["cause"] == "retention_decay"


# ── Tenant scoping ─────────────────────────────────────────────────────────


class TestDemotionFeedScoping:
    @pytest.mark.asyncio
    async def test_cross_household_access_blocked(self, auth_client, db_session, household):
        """A child in another household yields 404 (never cross-tenant leak)."""
        other_hh = Household(name="Other Family", timezone="America/New_York")
        db_session.add(other_hh)
        await db_session.flush()
        await set_tenant(db_session, other_hh.id)
        other_child = Child(household_id=other_hh.id, first_name="Outsider")
        db_session.add(other_child)
        await db_session.flush()
        # Restore the authed household's tenant context.
        await set_tenant(db_session, household.id)

        resp = await auth_client.get(DEMOTIONS_URL.format(child_id=other_child.id))
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthenticated_blocked(self, client, child):
        resp = await client.get(DEMOTIONS_URL.format(child_id=child.id))
        assert resp.status_code == 401
