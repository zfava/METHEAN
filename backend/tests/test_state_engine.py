"""Comprehensive tests for Learner State Engine (System 2).

Tests cover:
- State transitions: not_started -> emerging -> mastered
- FSRS integration: review card, verify stability/due
- Nightly decay: mastered -> proficient via retrievability
- Cascade unblock: mastering prereq unblocks downstream
- Attempt workflow end-to-end
- State query API endpoints
- Retention summary
- Idempotency of decay job
"""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningMap,
    LearningNode,
    Subject,
)
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    AttemptStatus,
    EdgeRelation,
    MasteryLevel,
    NodeType,
    PlanStatus,
    StateEventType,
)
from app.models.governance import Activity, Attempt, Plan, PlanWeek
from app.models.identity import Child, Household
from app.models.state import ChildNodeState, FSRSCard, ReviewLog, StateEvent
from app.services.state_engine import (
    _mastery_from_confidence,
    compute_retrievability,
    confidence_to_rating,
    emit_state_event,
    get_or_create_fsrs_card,
    get_or_create_node_state,
    process_review,
)
from fsrs import Rating


# ── Helpers ──

async def _make_node(db, lmap, household, title, node_type=NodeType.skill):
    node = LearningNode(
        learning_map_id=lmap.id,
        household_id=household.id,
        node_type=node_type,
        title=title,
    )
    db.add(node)
    await db.flush()
    return node


async def _make_edge(db, lmap, household, from_node, to_node):
    edge = LearningEdge(
        learning_map_id=lmap.id,
        household_id=household.id,
        from_node_id=from_node.id,
        to_node_id=to_node.id,
        relation=EdgeRelation.prerequisite,
    )
    db.add(edge)
    await db.flush()
    return edge


async def _make_activity_for_node(db, household, node, child, user):
    """Create a plan, week, and activity linked to a node."""
    from datetime import date

    plan = Plan(
        household_id=household.id,
        child_id=child.id,
        created_by=user.id,
        name="Test Plan",
        status=PlanStatus.active,
    )
    db.add(plan)
    await db.flush()

    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 7),
    )
    db.add(week)
    await db.flush()

    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        node_id=node.id,
        activity_type=ActivityType.lesson,
        title=f"Activity for {node.title}",
    )
    db.add(activity)
    await db.flush()
    return activity


# ══════════════════════════════════════════════════
# Unit Tests: Confidence Mapping
# ══════════════════════════════════════════════════

class TestConfidenceMapping:

    def test_low_confidence_again(self):
        assert confidence_to_rating(0.1) == Rating.Again
        assert confidence_to_rating(0.0) == Rating.Again
        assert confidence_to_rating(0.29) == Rating.Again

    def test_medium_confidence_hard(self):
        assert confidence_to_rating(0.3) == Rating.Hard
        assert confidence_to_rating(0.49) == Rating.Hard

    def test_good_confidence(self):
        assert confidence_to_rating(0.5) == Rating.Good
        assert confidence_to_rating(0.79) == Rating.Good

    def test_high_confidence_easy(self):
        assert confidence_to_rating(0.8) == Rating.Easy
        assert confidence_to_rating(1.0) == Rating.Easy

    def test_mastery_from_confidence(self):
        assert _mastery_from_confidence(0.9, MasteryLevel.not_started) == MasteryLevel.mastered
        assert _mastery_from_confidence(0.7, MasteryLevel.not_started) == MasteryLevel.proficient
        assert _mastery_from_confidence(0.5, MasteryLevel.not_started) == MasteryLevel.developing
        assert _mastery_from_confidence(0.3, MasteryLevel.not_started) == MasteryLevel.emerging
        assert _mastery_from_confidence(0.1, MasteryLevel.not_started) == MasteryLevel.emerging


# ══════════════════════════════════════════════════
# Unit Tests: State Transitions
# ══════════════════════════════════════════════════

class TestStateTransitions:

    @pytest.mark.asyncio
    async def test_not_started_to_emerging(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, learning_map, household, "Node A")
        result = await process_review(
            db_session, child.id, household.id, node.id,
            confidence=0.3, duration_minutes=10,
        )
        assert result["mastery_level"] == MasteryLevel.emerging
        assert result["previous_mastery"] == MasteryLevel.not_started
        assert result["state_event_id"] is not None

    @pytest.mark.asyncio
    async def test_emerging_to_mastered(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, learning_map, household, "Node B")

        # First review: not_started -> emerging
        await process_review(db_session, child.id, household.id, node.id, confidence=0.3)

        # Second review: high confidence -> mastered
        result = await process_review(db_session, child.id, household.id, node.id, confidence=0.9)
        assert result["mastery_level"] == MasteryLevel.mastered
        assert result["previous_mastery"] == MasteryLevel.emerging

    @pytest.mark.asyncio
    async def test_attempts_count_increments(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, learning_map, household, "Count Node")
        await process_review(db_session, child.id, household.id, node.id, confidence=0.5)
        await process_review(db_session, child.id, household.id, node.id, confidence=0.6)
        await process_review(db_session, child.id, household.id, node.id, confidence=0.7)

        state = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        assert state.attempts_count == 3

    @pytest.mark.asyncio
    async def test_state_event_emitted_on_mastery_change(
        self, db_session, household, learning_map, child,
    ):
        node = await _make_node(db_session, learning_map, household, "Event Node")
        result = await process_review(db_session, child.id, household.id, node.id, confidence=0.9)

        event_result = await db_session.execute(
            select(StateEvent).where(StateEvent.id == result["state_event_id"])
        )
        event = event_result.scalar_one()
        assert event.event_type == StateEventType.mastery_change
        assert event.from_state == "not_started"
        assert event.to_state == "mastered"
        assert event.trigger == "attempt"


# ══════════════════════════════════════════════════
# FSRS Integration Tests
# ══════════════════════════════════════════════════

class TestFSRSIntegration:

    @pytest.mark.asyncio
    async def test_fsrs_card_created_on_first_review(
        self, db_session, household, learning_map, child,
    ):
        node = await _make_node(db_session, learning_map, household, "FSRS Node")
        result = await process_review(db_session, child.id, household.id, node.id, confidence=0.7)

        card_result = await db_session.execute(
            select(FSRSCard).where(
                FSRSCard.child_id == child.id,
                FSRSCard.node_id == node.id,
            )
        )
        card = card_result.scalar_one()
        assert card.stability > 0
        assert card.due is not None
        assert card.last_review is not None

    @pytest.mark.asyncio
    async def test_fsrs_due_date_set(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, learning_map, household, "Due Node")
        result = await process_review(db_session, child.id, household.id, node.id, confidence=0.7)
        assert result["fsrs_due"] is not None

    @pytest.mark.asyncio
    async def test_review_log_created(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, learning_map, household, "Log Node")
        await process_review(db_session, child.id, household.id, node.id, confidence=0.7)

        log_result = await db_session.execute(
            select(ReviewLog).where(ReviewLog.child_id == child.id)
        )
        log = log_result.scalar_one()
        assert log.rating == Rating.Good.value  # 0.7 maps to Good

    @pytest.mark.asyncio
    async def test_multiple_reviews_increase_stability(
        self, db_session, household, learning_map, child,
    ):
        node = await _make_node(db_session, learning_map, household, "Stability Node")

        await process_review(db_session, child.id, household.id, node.id, confidence=0.7)
        card1 = await db_session.execute(
            select(FSRSCard).where(FSRSCard.child_id == child.id, FSRSCard.node_id == node.id)
        )
        stability_1 = card1.scalar_one().stability

        await process_review(db_session, child.id, household.id, node.id, confidence=0.8)
        card2 = await db_session.execute(
            select(FSRSCard).where(FSRSCard.child_id == child.id, FSRSCard.node_id == node.id)
        )
        stability_2 = card2.scalar_one().stability

        assert stability_2 > stability_1


# ══════════════════════════════════════════════════
# Cascade Unblock Tests
# ══════════════════════════════════════════════════

class TestCascadeUnblock:

    @pytest.mark.asyncio
    async def test_mastering_prereq_unblocks_downstream(
        self, db_session, household, learning_map, child,
    ):
        """A -> B: mastering A should unblock B."""
        a = await _make_node(db_session, learning_map, household, "Prereq A")
        b = await _make_node(db_session, learning_map, household, "Blocked B")
        await _make_edge(db_session, learning_map, household, a, b)

        result = await process_review(
            db_session, child.id, household.id, a.id, confidence=0.9,
        )
        assert b.id in result["nodes_unblocked"]

        # Verify unblock event was created
        event_result = await db_session.execute(
            select(StateEvent).where(
                StateEvent.child_id == child.id,
                StateEvent.node_id == b.id,
                StateEvent.event_type == StateEventType.node_unlocked,
            )
        )
        event = event_result.scalar_one()
        assert event.trigger == "prerequisite_met"

    @pytest.mark.asyncio
    async def test_partial_prereqs_dont_unblock(
        self, db_session, household, learning_map, child,
    ):
        """A -> C and B -> C: mastering only A doesn't unblock C."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        c = await _make_node(db_session, learning_map, household, "C")
        await _make_edge(db_session, learning_map, household, a, c)
        await _make_edge(db_session, learning_map, household, b, c)

        result = await process_review(
            db_session, child.id, household.id, a.id, confidence=0.9,
        )
        assert c.id not in result["nodes_unblocked"]

    @pytest.mark.asyncio
    async def test_all_prereqs_met_unblocks(
        self, db_session, household, learning_map, child,
    ):
        """A -> C and B -> C: mastering both A and B unblocks C."""
        a = await _make_node(db_session, learning_map, household, "A2")
        b = await _make_node(db_session, learning_map, household, "B2")
        c = await _make_node(db_session, learning_map, household, "C2")
        await _make_edge(db_session, learning_map, household, a, c)
        await _make_edge(db_session, learning_map, household, b, c)

        await process_review(db_session, child.id, household.id, a.id, confidence=0.9)
        result = await process_review(
            db_session, child.id, household.id, b.id, confidence=0.9,
        )
        assert c.id in result["nodes_unblocked"]


# ══════════════════════════════════════════════════
# Decay Tests
# ══════════════════════════════════════════════════

class TestDecay:

    @pytest.mark.asyncio
    async def test_retrievability_computation(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, learning_map, household, "Decay Node")
        card = FSRSCard(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            stability=5.0,
            last_review=datetime.now(UTC) - timedelta(days=30),
            due=datetime.now(UTC) - timedelta(days=25),
        )
        db_session.add(card)
        await db_session.flush()

        r = compute_retrievability(card)
        assert r is not None
        assert 0 < r < 1  # Should have decayed significantly

    @pytest.mark.asyncio
    async def test_fresh_card_high_retrievability(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, learning_map, household, "Fresh Node")
        card = FSRSCard(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            stability=10.0,
            last_review=datetime.now(UTC),
            due=datetime.now(UTC) + timedelta(days=10),
        )
        db_session.add(card)
        await db_session.flush()

        r = compute_retrievability(card)
        assert r is not None
        assert r > 0.9  # Should be very high

    @pytest.mark.asyncio
    async def test_decay_job_transitions_mastered(self, db_session, household, learning_map, child):
        """Run decay on a mastered node with overdue card."""
        from app.tasks.decay import run_decay_batch

        node = await _make_node(db_session, learning_map, household, "Overdue Node")

        # Set up mastered state
        state = ChildNodeState(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            mastery_level=MasteryLevel.mastered,
        )
        db_session.add(state)

        # Set up overdue FSRS card with low retrievability
        card = FSRSCard(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            stability=2.0,
            last_review=datetime.now(UTC) - timedelta(days=60),
            due=datetime.now(UTC) - timedelta(days=55),
        )
        db_session.add(card)
        await db_session.commit()

        # Run decay with the test session factory
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from sqlalchemy.pool import NullPool
        from app.core.config import settings as cfg

        test_url = cfg.DATABASE_URL.rsplit("/", 1)[0] + "/methean_test"
        eng = create_async_engine(test_url, poolclass=NullPool)
        sf = async_sessionmaker(eng, class_=AsyncSession, expire_on_commit=False)

        result = await run_decay_batch(session_factory=sf)
        assert result["cards_checked"] >= 1
        assert result["cards_decayed"] >= 1

        # Verify state changed
        async with sf() as check_db:
            state_result = await check_db.execute(
                select(ChildNodeState).where(
                    ChildNodeState.child_id == child.id,
                    ChildNodeState.node_id == node.id,
                )
            )
            updated_state = state_result.scalar_one()
            assert updated_state.mastery_level == MasteryLevel.proficient

            # Verify decay event emitted
            event_result = await check_db.execute(
                select(StateEvent).where(
                    StateEvent.child_id == child.id,
                    StateEvent.node_id == node.id,
                    StateEvent.trigger == "decay",
                )
            )
            event = event_result.scalar_one()
            assert event.from_state == "mastered"
            assert event.to_state == "proficient"

        await eng.dispose()

    @pytest.mark.asyncio
    async def test_decay_idempotent(self, db_session, household, learning_map, child):
        """Running decay twice should only create one event per transition."""
        from app.tasks.decay import run_decay_batch
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.core.config import settings as cfg

        node = await _make_node(db_session, learning_map, household, "Idempotent Node")

        state = ChildNodeState(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            mastery_level=MasteryLevel.mastered,
        )
        db_session.add(state)

        card = FSRSCard(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            stability=1.0,
            last_review=datetime.now(UTC) - timedelta(days=90),
            due=datetime.now(UTC) - timedelta(days=85),
        )
        db_session.add(card)
        await db_session.commit()

        test_url = cfg.DATABASE_URL.rsplit("/", 1)[0] + "/methean_test"
        eng = create_async_engine(test_url, poolclass=NullPool)
        sf = async_sessionmaker(eng, class_=AsyncSession, expire_on_commit=False)

        # Run twice
        r1 = await run_decay_batch(session_factory=sf)
        r2 = await run_decay_batch(session_factory=sf)

        # Second run should not decay again (already proficient)
        assert r2["cards_decayed"] == 0

        await eng.dispose()


# ══════════════════════════════════════════════════
# Attempt Workflow Tests
# ══════════════════════════════════════════════════

class TestAttemptWorkflow:

    @pytest.mark.asyncio
    async def test_start_and_submit_attempt(
        self, db_session, household, learning_map, child, user,
    ):
        from app.services.attempt_workflow import start_attempt, submit_attempt

        node = await _make_node(db_session, learning_map, household, "Attempt Node")
        activity = await _make_activity_for_node(db_session, household, node, child, user)

        # Start attempt
        attempt = await start_attempt(db_session, activity.id, child.id, household.id)
        assert attempt.status == AttemptStatus.started

        # Submit with Good confidence
        result = await submit_attempt(
            db_session, attempt.id, household.id,
            duration_minutes=15, score=0.7, confidence=0.7,
            user_id=user.id,
        )
        assert result["attempt"].status == AttemptStatus.completed
        assert result["mastery_level"] == MasteryLevel.proficient  # 0.7 confidence
        assert result["fsrs_due"] is not None
        assert result["fsrs_rating"] == Rating.Good.value

    @pytest.mark.asyncio
    async def test_submit_mastered_triggers_cascade(
        self, db_session, household, learning_map, child, user,
    ):
        from app.services.attempt_workflow import start_attempt, submit_attempt

        a = await _make_node(db_session, learning_map, household, "Prereq")
        b = await _make_node(db_session, learning_map, household, "Downstream")
        await _make_edge(db_session, learning_map, household, a, b)

        activity = await _make_activity_for_node(db_session, household, a, child, user)
        attempt = await start_attempt(db_session, activity.id, child.id, household.id)

        # Submit with mastery confidence
        result = await submit_attempt(
            db_session, attempt.id, household.id,
            confidence=0.9, user_id=user.id,
        )
        assert result["mastery_level"] == MasteryLevel.mastered
        assert b.id in result["nodes_unblocked"]


# ══════════════════════════════════════════════════
# API Integration Tests
# ══════════════════════════════════════════════════

class TestStateAPI:

    @pytest.mark.asyncio
    async def test_get_child_state(
        self, auth_client, db_session, household, subject, child,
    ):
        # Create map with node, enroll child, process review
        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="State API Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        node = await _make_node(db_session, lmap, household, "API Node")

        enrollment = ChildMapEnrollment(
            child_id=child.id, household_id=household.id,
            learning_map_id=lmap.id,
        )
        db_session.add(enrollment)
        await db_session.flush()

        # Process a review
        await process_review(db_session, child.id, household.id, node.id, confidence=0.6)

        resp = await auth_client.get(f"/api/v1/children/{child.id}/state")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_nodes"] >= 1
        assert len(data["nodes"]) >= 1

        # Find our node
        our_node = next(n for n in data["nodes"] if n["node_id"] == str(node.id))
        assert our_node["mastery_level"] == "proficient"
        assert our_node["attempts_count"] == 1

    @pytest.mark.asyncio
    async def test_get_node_history(
        self, auth_client, db_session, household, subject, child,
    ):
        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="History Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        node = await _make_node(db_session, lmap, household, "History Node")

        # Two reviews
        await process_review(db_session, child.id, household.id, node.id, confidence=0.5)
        await process_review(db_session, child.id, household.id, node.id, confidence=0.9)

        resp = await auth_client.get(
            f"/api/v1/children/{child.id}/nodes/{node.id}/history"
        )
        assert resp.status_code == 200
        events = resp.json()
        assert len(events) == 2
        # Chronological order
        assert events[0]["to_state"] == "developing"
        assert events[1]["to_state"] == "mastered"

    @pytest.mark.asyncio
    async def test_get_retention_summary(
        self, auth_client, db_session, household, subject, child,
    ):
        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Retention Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        node_a = await _make_node(db_session, lmap, household, "Mastered A")
        node_b = await _make_node(db_session, lmap, household, "In Progress B")
        node_c = await _make_node(db_session, lmap, household, "Not Started C")

        enrollment = ChildMapEnrollment(
            child_id=child.id, household_id=household.id,
            learning_map_id=lmap.id,
        )
        db_session.add(enrollment)
        await db_session.flush()

        # Master A
        await process_review(db_session, child.id, household.id, node_a.id, confidence=0.9)
        # In-progress B
        await process_review(db_session, child.id, household.id, node_b.id, confidence=0.5)

        resp = await auth_client.get(
            f"/api/v1/children/{child.id}/retention-summary"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_nodes"] == 3
        assert data["mastered_count"] == 1
        assert data["in_progress_count"] == 1  # developing counts as in_progress
        assert data["not_started_count"] >= 1

    @pytest.mark.asyncio
    async def test_attempt_api_endpoints(
        self, auth_client, db_session, household, subject, child, user,
    ):
        """End-to-end test: create activity -> start attempt -> submit."""
        from datetime import date

        lmap = LearningMap(
            household_id=household.id, subject_id=subject.id, name="Attempt Map"
        )
        db_session.add(lmap)
        await db_session.flush()

        node = await _make_node(db_session, lmap, household, "Attempt API Node")

        # Need plan/week/activity structure
        plan = Plan(
            household_id=household.id, child_id=child.id,
            created_by=user.id,
            name="API Plan", status=PlanStatus.active,
        )
        db_session.add(plan)
        await db_session.flush()

        week = PlanWeek(
            plan_id=plan.id, household_id=household.id,
            week_number=1, start_date=date(2026, 1, 1), end_date=date(2026, 1, 7),
        )
        db_session.add(week)
        await db_session.flush()

        activity = Activity(
            plan_week_id=week.id, household_id=household.id,
            node_id=node.id, activity_type=ActivityType.lesson,
            title="API Test Activity",
        )
        db_session.add(activity)
        await db_session.flush()

        # Start attempt
        resp1 = await auth_client.post(
            f"/api/v1/activities/{activity.id}/attempts",
            json={"child_id": str(child.id)},
        )
        assert resp1.status_code == 201
        attempt_id = resp1.json()["id"]
        assert resp1.json()["status"] == "started"

        # Submit attempt
        resp2 = await auth_client.put(
            f"/api/v1/attempts/{attempt_id}/submit",
            json={"confidence": 0.85, "duration_minutes": 20},
        )
        assert resp2.status_code == 200
        data = resp2.json()
        assert data["mastery_level"] == "mastered"
        assert data["fsrs_rating"] == Rating.Easy.value  # 0.85 -> Easy

        # Get attempt
        resp3 = await auth_client.get(f"/api/v1/attempts/{attempt_id}")
        assert resp3.status_code == 200
        assert resp3.json()["status"] == "completed"
