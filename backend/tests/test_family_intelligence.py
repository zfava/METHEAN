"""Tests for the Family Intelligence cross-child pattern detection service."""

import uuid
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calibration import EvaluatorPrediction
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import FamilyPatternType, InsightStatus, MasteryLevel, NodeType
from app.models.family_insight import FamilyInsight, FamilyInsightConfig
from app.models.governance import Activity, Attempt
from app.models.identity import Child, Household
from app.models.state import ChildNodeState
from app.services.family_intelligence import (
    detect_shared_struggles,
    detect_curriculum_gaps,
    detect_pacing_divergence,
    detect_environmental_correlation,
    detect_material_effectiveness,
    run_family_intelligence,
)


# ── Fixtures ──


@pytest_asyncio.fixture
async def fi_household(db_session: AsyncSession) -> Household:
    h = Household(name="Family Intel Test")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def fi_child_a(db_session: AsyncSession, fi_household: Household) -> Child:
    c = Child(household_id=fi_household.id, first_name="Alice")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def fi_child_b(db_session: AsyncSession, fi_household: Household) -> Child:
    c = Child(household_id=fi_household.id, first_name="Bob")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def fi_subject(db_session: AsyncSession, fi_household: Household) -> Subject:
    s = Subject(household_id=fi_household.id, name="Mathematics")
    db_session.add(s)
    await db_session.flush()
    return s


@pytest_asyncio.fixture
async def fi_map(db_session, fi_household, fi_subject) -> LearningMap:
    m = LearningMap(household_id=fi_household.id, subject_id=fi_subject.id, name="Math Map")
    db_session.add(m)
    await db_session.flush()
    return m


@pytest_asyncio.fixture
async def fi_node(db_session, fi_household, fi_map) -> LearningNode:
    n = LearningNode(
        learning_map_id=fi_map.id, household_id=fi_household.id,
        node_type=NodeType.concept, title="Addition Facts",
    )
    db_session.add(n)
    await db_session.flush()
    return n


async def _make_attempt(db_session, fi_household, child, fi_node) -> Attempt:
    act = Activity(
        household_id=fi_household.id, title="Practice", activity_type="practice",
        node_id=fi_node.id,
    )
    db_session.add(act)
    await db_session.flush()
    att = Attempt(activity_id=act.id, household_id=fi_household.id, child_id=child.id)
    db_session.add(att)
    await db_session.flush()
    return att


# ═══════════════════════════════════════════
# SHARED STRUGGLE
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestSharedStruggle:
    async def test_detects_shared_struggle(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """Both children stuck on same node → insight created."""
        now = datetime.now(UTC)
        for child in [fi_child_a, fi_child_b]:
            db_session.add(ChildNodeState(
                child_id=child.id, household_id=fi_household.id, node_id=fi_node.id,
                mastery_level=MasteryLevel.emerging, attempts_count=5,
                last_activity_at=now - timedelta(days=1),
            ))
        await db_session.flush()

        children = [fi_child_a, fi_child_b]
        results = await detect_shared_struggles(db_session, fi_household.id, children, None)
        assert len(results) == 1
        assert results[0].pattern_type == FamilyPatternType.shared_struggle
        assert "Alice" in results[0].recommendation
        assert "Bob" in results[0].recommendation

    async def test_no_struggle_below_threshold(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """Only 1 child struggling → no insight."""
        now = datetime.now(UTC)
        db_session.add(ChildNodeState(
            child_id=fi_child_a.id, household_id=fi_household.id, node_id=fi_node.id,
            mastery_level=MasteryLevel.emerging, attempts_count=5,
            last_activity_at=now - timedelta(days=1),
        ))
        db_session.add(ChildNodeState(
            child_id=fi_child_b.id, household_id=fi_household.id, node_id=fi_node.id,
            mastery_level=MasteryLevel.mastered, attempts_count=3,
            last_activity_at=now - timedelta(days=1),
        ))
        await db_session.flush()

        results = await detect_shared_struggles(db_session, fi_household.id, [fi_child_a, fi_child_b], None)
        assert len(results) == 0


# ═══════════════════════════════════════════
# CURRICULUM GAP
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestCurriculumGap:
    async def test_detects_gap(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """Both children score low on first attempt → curriculum gap."""
        for child in [fi_child_a, fi_child_b]:
            att = await _make_attempt(db_session, fi_household, child, fi_node)
            db_session.add(EvaluatorPrediction(
                household_id=fi_household.id, child_id=child.id,
                node_id=fi_node.id, attempt_id=att.id,
                predicted_confidence=0.3, predicted_fsrs_rating=1,
            ))
        await db_session.flush()

        results = await detect_curriculum_gaps(db_session, fi_household.id, [fi_child_a, fi_child_b], None)
        assert len(results) == 1
        assert results[0].pattern_type == FamilyPatternType.curriculum_gap

    async def test_no_gap_when_one_scores_well(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """One child scores well → no gap."""
        att_a = await _make_attempt(db_session, fi_household, fi_child_a, fi_node)
        db_session.add(EvaluatorPrediction(
            household_id=fi_household.id, child_id=fi_child_a.id,
            node_id=fi_node.id, attempt_id=att_a.id,
            predicted_confidence=0.3, predicted_fsrs_rating=1,
        ))
        att_b = await _make_attempt(db_session, fi_household, fi_child_b, fi_node)
        db_session.add(EvaluatorPrediction(
            household_id=fi_household.id, child_id=fi_child_b.id,
            node_id=fi_node.id, attempt_id=att_b.id,
            predicted_confidence=0.8, predicted_fsrs_rating=3,
        ))
        await db_session.flush()

        results = await detect_curriculum_gaps(db_session, fi_household.id, [fi_child_a, fi_child_b], None)
        assert len(results) == 0


# ═══════════════════════════════════════════
# PACING DIVERGENCE
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestPacingDivergence:
    async def test_detects_divergence(self, db_session, fi_household, fi_child_a, fi_child_b, fi_map):
        """One child fast, one slow → divergence detected."""
        now = datetime.now(UTC)
        # Alice mastered 8 nodes in last 4 weeks (2/wk)
        for i in range(8):
            n = LearningNode(learning_map_id=fi_map.id, household_id=fi_household.id,
                             node_type=NodeType.concept, title=f"Node A{i}")
            db_session.add(n)
            await db_session.flush()
            db_session.add(ChildNodeState(
                child_id=fi_child_a.id, household_id=fi_household.id, node_id=n.id,
                mastery_level=MasteryLevel.mastered,
                last_activity_at=now - timedelta(days=i * 3),
            ))
        # Bob mastered 1 node (0.25/wk) → divergence 2/0.25 = 8x
        n2 = LearningNode(learning_map_id=fi_map.id, household_id=fi_household.id,
                          node_type=NodeType.concept, title="Node B0")
        db_session.add(n2)
        await db_session.flush()
        db_session.add(ChildNodeState(
            child_id=fi_child_b.id, household_id=fi_household.id, node_id=n2.id,
            mastery_level=MasteryLevel.mastered,
            last_activity_at=now - timedelta(days=1),
        ))
        await db_session.flush()

        results = await detect_pacing_divergence(db_session, fi_household.id, [fi_child_a, fi_child_b], None)
        assert len(results) == 1
        assert results[0].pattern_type == FamilyPatternType.pacing_divergence

    async def test_no_divergence_similar_pace(self, db_session, fi_household, fi_child_a, fi_child_b, fi_map):
        """Similar pace → no divergence."""
        now = datetime.now(UTC)
        for child in [fi_child_a, fi_child_b]:
            for i in range(4):
                n = LearningNode(learning_map_id=fi_map.id, household_id=fi_household.id,
                                 node_type=NodeType.concept, title=f"Node {child.first_name}{i}")
                db_session.add(n)
                await db_session.flush()
                db_session.add(ChildNodeState(
                    child_id=child.id, household_id=fi_household.id, node_id=n.id,
                    mastery_level=MasteryLevel.mastered,
                    last_activity_at=now - timedelta(days=i * 5),
                ))
        await db_session.flush()

        results = await detect_pacing_divergence(db_session, fi_household.id, [fi_child_a, fi_child_b], None)
        assert len(results) == 0


# ═══════════════════════════════════════════
# MATERIAL EFFECTIVENESS
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestMaterialEffectiveness:
    async def test_detects_difference(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """Same node, different outcomes → material effectiveness insight."""
        for i in range(6):
            att_a = await _make_attempt(db_session, fi_household, fi_child_a, fi_node)
            db_session.add(EvaluatorPrediction(
                household_id=fi_household.id, child_id=fi_child_a.id,
                node_id=fi_node.id, attempt_id=att_a.id,
                predicted_confidence=0.85, predicted_fsrs_rating=4,
            ))
            att_b = await _make_attempt(db_session, fi_household, fi_child_b, fi_node)
            db_session.add(EvaluatorPrediction(
                household_id=fi_household.id, child_id=fi_child_b.id,
                node_id=fi_node.id, attempt_id=att_b.id,
                predicted_confidence=0.35, predicted_fsrs_rating=2,
            ))
        await db_session.flush()

        results = await detect_material_effectiveness(
            db_session, fi_household.id, [fi_child_a, fi_child_b], None)
        assert len(results) == 1
        assert results[0].pattern_type == FamilyPatternType.material_effectiveness
        assert "Alice" in results[0].recommendation

    async def test_no_insight_similar_outcomes(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """Similar outcomes → no insight."""
        for i in range(6):
            for child in [fi_child_a, fi_child_b]:
                att = await _make_attempt(db_session, fi_household, child, fi_node)
                db_session.add(EvaluatorPrediction(
                    household_id=fi_household.id, child_id=child.id,
                    node_id=fi_node.id, attempt_id=att.id,
                    predicted_confidence=0.7, predicted_fsrs_rating=3,
                ))
        await db_session.flush()

        results = await detect_material_effectiveness(
            db_session, fi_household.id, [fi_child_a, fi_child_b], None)
        assert len(results) == 0


# ═══════════════════════════════════════════
# SINGLE CHILD & CONFIG
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestSingleChildHousehold:
    async def test_no_insights_single_child(self, db_session, fi_household, fi_child_a):
        """Single child household produces no insights."""
        result = await run_family_intelligence(db_session, fi_household.id)
        assert result["skipped"] is True
        assert result["reason"] == "fewer_than_2_children"


@pytest.mark.asyncio
class TestConfigDisable:
    async def test_disabled_config_skips(self, db_session, fi_household, fi_child_a, fi_child_b):
        """Disabled config produces no insights."""
        config = FamilyInsightConfig(household_id=fi_household.id, enabled=False)
        db_session.add(config)
        await db_session.flush()

        result = await run_family_intelligence(db_session, fi_household.id)
        assert result["skipped"] is True
        assert result["reason"] == "disabled"

    async def test_disabled_pattern_skipped(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """Disabled individual pattern produces no insights for that type."""
        now = datetime.now(UTC)
        for child in [fi_child_a, fi_child_b]:
            db_session.add(ChildNodeState(
                child_id=child.id, household_id=fi_household.id, node_id=fi_node.id,
                mastery_level=MasteryLevel.emerging, attempts_count=5,
                last_activity_at=now - timedelta(days=1),
            ))
        await db_session.flush()

        config = FamilyInsightConfig(
            household_id=fi_household.id, enabled=True,
            pattern_settings={
                "shared_struggle": {"enabled": False, "min_children": 2, "drift_threshold": 1.5},
                "curriculum_gap": {"enabled": True, "confidence_threshold": 0.5},
                "pacing_divergence": {"enabled": True, "divergence_factor": 2.0},
                "environmental_correlation": {"enabled": True, "window_days": 7},
                "material_effectiveness": {"enabled": True, "min_attempts": 5},
            },
        )
        db_session.add(config)
        await db_session.flush()

        results = await detect_shared_struggles(
            db_session, fi_household.id, [fi_child_a, fi_child_b], config)
        assert len(results) == 0


# ═══════════════════════════════════════════
# DEDUPLICATION
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestDeduplication:
    async def test_no_duplicate_insights(self, db_session, fi_household, fi_child_a, fi_child_b, fi_node):
        """Same pattern not flagged twice."""
        now = datetime.now(UTC)
        for child in [fi_child_a, fi_child_b]:
            db_session.add(ChildNodeState(
                child_id=child.id, household_id=fi_household.id, node_id=fi_node.id,
                mastery_level=MasteryLevel.emerging, attempts_count=5,
                last_activity_at=now - timedelta(days=1),
            ))
        await db_session.flush()

        children = [fi_child_a, fi_child_b]
        # First run
        r1 = await detect_shared_struggles(db_session, fi_household.id, children, None)
        await db_session.flush()
        assert len(r1) == 1

        # Second run — should be deduplicated
        r2 = await detect_shared_struggles(db_session, fi_household.id, children, None)
        assert len(r2) == 0


# ═══════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestRunFamilyIntelligence:
    async def test_runs_all_detectors(self, db_session, fi_household, fi_child_a, fi_child_b):
        """Main entry point runs without error and returns counts."""
        result = await run_family_intelligence(db_session, fi_household.id)
        assert result["skipped"] is False
        assert "counts" in result
        assert "insights_created" in result
