"""Demotion explanation envelope on automated mastery demotions.

Both automated paths that lower a child's MasteryLevel now attach a
parent-legible ``demotion_explanation`` to the metadata of the StateEvent they
already emit:

- the attempt path (state_engine.process_review via _mastery_from_confidence),
  cause ``low_confidence_attempt``;
- the decay path (tasks.decay.run_decay_batch), cause ``retention_decay``.

These tests cover the pure helpers (is_demotion, build_demotion_explanation)
across every adjacent level pair and both causes, and the two emissions. The
decay path's event_type/trigger/from_state/to_state stay byte-for-byte
unchanged so the idempotency guard keeps matching.
"""

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.config import settings
from app.core.database import set_tenant
from app.models.curriculum import LearningNode
from app.models.enums import MasteryLevel, NodeType, StateEventType
from app.models.state import ChildNodeState, FSRSCard, StateEvent
from app.services.state_engine import (
    _MASTERY_ORDER,
    build_demotion_explanation,
    is_demotion,
    process_review,
)

M = MasteryLevel


# ══════════════════════════════════════════════════════════════════════
# Unit tests: is_demotion
# ══════════════════════════════════════════════════════════════════════


class TestIsDemotion:
    def test_every_adjacent_pair_down_is_demotion(self):
        # Each step DOWN the ladder is a demotion.
        for higher, lower in zip(_MASTERY_ORDER[1:], _MASTERY_ORDER[:-1]):
            assert is_demotion(higher, lower) is True

    def test_every_adjacent_pair_up_is_not_demotion(self):
        # Each step UP the ladder is a promotion, not a demotion.
        for lower, higher in zip(_MASTERY_ORDER[:-1], _MASTERY_ORDER[1:]):
            assert is_demotion(lower, higher) is False

    def test_hold_is_not_demotion(self):
        for level in _MASTERY_ORDER:
            assert is_demotion(level, level) is False

    def test_multi_step_demotion(self):
        assert is_demotion(M.mastered, M.emerging) is True
        assert is_demotion(M.proficient, M.not_started) is True

    def test_order_is_canonical(self):
        assert _MASTERY_ORDER == (
            M.not_started,
            M.emerging,
            M.developing,
            M.proficient,
            M.mastered,
        )


# ══════════════════════════════════════════════════════════════════════
# Unit tests: build_demotion_explanation
# ══════════════════════════════════════════════════════════════════════

_REQUIRED_KEYS = {
    "from_level",
    "to_level",
    "cause",
    "confidence",
    "retrievability",
    "fsrs_stability",
    "threshold_crossed",
    "human_summary",
}


class TestBuildDemotionExplanation:
    def test_attempt_cause_shape_and_summary(self):
        e = build_demotion_explanation(
            M.mastered,
            M.proficient,
            cause="low_confidence_attempt",
            confidence=0.65,
            fsrs_stability=4.2,
            threshold_crossed=settings.MASTERY_THRESHOLD,
        )
        assert set(e.keys()) == _REQUIRED_KEYS
        assert e["from_level"] == "mastered"
        assert e["to_level"] == "proficient"
        assert e["cause"] == "low_confidence_attempt"
        assert e["confidence"] == 0.65
        assert e["retrievability"] is None
        assert e["fsrs_stability"] == 4.2
        assert e["threshold_crossed"] == settings.MASTERY_THRESHOLD
        assert e["human_summary"] == (
            "This skill moved from mastered back to proficient after the last "
            "attempt scored below the mastery line, so it comes back for "
            "another practice round."
        )

    def test_decay_cause_shape_and_summary(self):
        e = build_demotion_explanation(
            M.mastered,
            M.proficient,
            cause="retention_decay",
            retrievability=0.42,
            fsrs_stability=5.0,
            threshold_crossed=settings.DECAY_RETRIEVABILITY_THRESHOLD,
        )
        assert set(e.keys()) == _REQUIRED_KEYS
        assert e["cause"] == "retention_decay"
        assert e["confidence"] is None
        assert e["retrievability"] == 0.42
        assert e["threshold_crossed"] == settings.DECAY_RETRIEVABILITY_THRESHOLD
        assert e["human_summary"] == (
            "It has been long enough since this skill was practiced that the "
            "system flagged it for review to keep it fresh."
        )

    def test_summary_uses_actual_level_names(self):
        e = build_demotion_explanation(
            M.developing,
            M.emerging,
            cause="low_confidence_attempt",
            confidence=0.25,
            fsrs_stability=1.0,
            threshold_crossed=settings.MASTERY_THRESHOLD,
        )
        assert "from developing back to emerging" in e["human_summary"]

    def test_no_em_dashes_in_any_summary(self):
        for cause in ("low_confidence_attempt", "retention_decay"):
            for higher, lower in zip(_MASTERY_ORDER[1:], _MASTERY_ORDER[:-1]):
                e = build_demotion_explanation(
                    higher,
                    lower,
                    cause=cause,
                    threshold_crossed=0.5,
                )
                assert "—" not in e["human_summary"]
                assert "--" not in e["human_summary"]


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════


async def _make_node(db, household, learning_map, title="Demotion Node") -> LearningNode:
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title=title,
    )
    db.add(node)
    await db.flush()
    return node


async def _make_mastered_state_and_overdue_card(
    db, household, child, node, *, days_ago: int = 30
) -> tuple[ChildNodeState, FSRSCard]:
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
    # stability=2.0 over days_ago=30 yields retrievability ~0.38, below the
    # DECAY_RETRIEVABILITY_THRESHOLD (0.5), so the card is actually decayed.
    card = FSRSCard(
        child_id=child.id,
        household_id=household.id,
        node_id=node.id,
        stability=2.0,
        difficulty=0.3,
        reps=3,
        last_review=last_rev,
        due=last_rev + timedelta(days=5),
    )
    db.add(card)
    await db.flush()
    return state, card


# ══════════════════════════════════════════════════════════════════════
# Attempt path: process_review emission
# ══════════════════════════════════════════════════════════════════════


class TestAttemptPathEmission:
    @pytest.mark.asyncio
    async def test_demotion_emits_explanation(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, household, learning_map, "Attempt Demote")

        # Reach mastered, then a below-line attempt demotes to proficient.
        await process_review(db_session, child.id, household.id, node.id, confidence=0.95)
        result = await process_review(db_session, child.id, household.id, node.id, confidence=0.7)

        assert result["previous_mastery"] == MasteryLevel.mastered
        assert result["mastery_level"] == MasteryLevel.proficient

        event = (
            await db_session.execute(select(StateEvent).where(StateEvent.id == result["state_event_id"]))
        ).scalar_one()
        assert event.event_type == StateEventType.mastery_change
        assert event.from_state == "mastered"
        assert event.to_state == "proficient"

        explanation = event.metadata_["demotion_explanation"]
        assert explanation["cause"] == "low_confidence_attempt"
        assert explanation["from_level"] == "mastered"
        assert explanation["to_level"] == "proficient"
        assert explanation["confidence"] == 0.7
        assert explanation["retrievability"] is None
        assert explanation["fsrs_stability"] is not None
        assert explanation["threshold_crossed"] == settings.MASTERY_THRESHOLD
        assert explanation["human_summary"].startswith("This skill moved from mastered back to proficient")
        # The original metadata is preserved alongside the new envelope.
        assert event.metadata_["confidence"] == 0.7
        assert "fsrs_due" in event.metadata_

    @pytest.mark.asyncio
    async def test_promotion_has_no_explanation(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, household, learning_map, "Attempt Promote")
        result = await process_review(db_session, child.id, household.id, node.id, confidence=0.95)

        assert result["mastery_level"] == MasteryLevel.mastered
        event = (
            await db_session.execute(select(StateEvent).where(StateEvent.id == result["state_event_id"]))
        ).scalar_one()
        assert "demotion_explanation" not in event.metadata_

    @pytest.mark.asyncio
    async def test_hold_has_no_explanation(self, db_session, household, learning_map, child):
        node = await _make_node(db_session, household, learning_map, "Attempt Hold")
        # Two reviews that land on the same level (proficient): a hold.
        await process_review(db_session, child.id, household.id, node.id, confidence=0.7)
        result = await process_review(db_session, child.id, household.id, node.id, confidence=0.7)

        assert result["previous_mastery"] == result["mastery_level"]
        event = (
            await db_session.execute(select(StateEvent).where(StateEvent.id == result["state_event_id"]))
        ).scalar_one()
        assert "demotion_explanation" not in event.metadata_


# ══════════════════════════════════════════════════════════════════════
# Decay path: run_decay_batch emission + idempotency
# ══════════════════════════════════════════════════════════════════════


class TestDecayPathEmission:
    @pytest.mark.asyncio
    async def test_decay_emits_explanation_with_unchanged_event_fields(
        self, db_session, household, learning_map, child
    ):
        from app.tasks.decay import run_decay_batch
        from tests.conftest import test_engine

        node = await _make_node(db_session, household, learning_map, "Decay Demote")
        await _make_mastered_state_and_overdue_card(db_session, household, child, node, days_ago=30)
        await db_session.commit()

        factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
        result = await run_decay_batch(session_factory=factory)
        assert result["cards_decayed"] >= 1

        async with factory() as fresh:
            await set_tenant(fresh, household.id)
            event = (
                await fresh.execute(
                    select(StateEvent).where(
                        StateEvent.node_id == node.id,
                        StateEvent.trigger == "decay",
                    )
                )
            ).scalar_one()

            # Idempotency-critical fields are byte-for-byte unchanged.
            assert event.event_type == StateEventType.mastery_change
            assert event.trigger == "decay"
            assert event.from_state == MasteryLevel.mastered.value
            assert event.to_state == MasteryLevel.proficient.value

            explanation = event.metadata_["demotion_explanation"]
            assert explanation["cause"] == "retention_decay"
            assert explanation["from_level"] == "mastered"
            assert explanation["to_level"] == "proficient"
            assert explanation["confidence"] is None
            assert explanation["retrievability"] is not None
            assert explanation["fsrs_stability"] is not None
            assert explanation["threshold_crossed"] == settings.DECAY_RETRIEVABILITY_THRESHOLD
            assert explanation["human_summary"].startswith("It has been long enough")
            # Pre-existing decay metadata is preserved alongside the envelope.
            assert "days_overdue" in event.metadata_
            assert event.metadata_["threshold"] == settings.DECAY_RETRIEVABILITY_THRESHOLD

    @pytest.mark.asyncio
    async def test_second_run_same_day_does_not_double_decay(self, db_session, household, learning_map, child):
        from app.tasks.decay import run_decay_batch
        from tests.conftest import test_engine

        node = await _make_node(db_session, household, learning_map, "Decay Idempotent")
        await _make_mastered_state_and_overdue_card(db_session, household, child, node, days_ago=30)
        await db_session.commit()

        factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
        first = await run_decay_batch(session_factory=factory)
        assert first["cards_decayed"] >= 1

        second = await run_decay_batch(session_factory=factory)
        assert second["cards_decayed"] == 0

        # Exactly one decay event exists for the node today (no double-decay).
        async with factory() as fresh:
            await set_tenant(fresh, household.id)
            events = (
                (
                    await fresh.execute(
                        select(StateEvent).where(
                            StateEvent.node_id == node.id,
                            StateEvent.event_type == StateEventType.mastery_change,
                            StateEvent.trigger == "decay",
                            StateEvent.to_state == MasteryLevel.proficient.value,
                        )
                    )
                )
                .scalars()
                .all()
            )
            assert len(events) == 1
