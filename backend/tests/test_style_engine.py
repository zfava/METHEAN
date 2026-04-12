"""Tests for the Learner Style Vector computation engine, batch, prompt injection, and API."""

import math
import uuid
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Child, Household
from app.models.intelligence import LearnerIntelligence
from app.models.style_vector import LearnerStyleVector
from app.services.style_engine import (
    _compute_attention_pattern,
    _compute_independence_level,
    _compute_modality_preference,
    _compute_optimal_session_minutes,
    _compute_pacing_preference,
    _compute_recovery_rate,
    _compute_socratic_responsiveness,
    _compute_subject_affinity_map,
    _compute_time_of_day_peak,
    _compute_frustration_threshold,
    _count_active_dimensions,
    _level_label,
    build_style_context,
    build_tutor_style_guidance,
    build_planner_style_guidance,
    build_advisor_style_guidance,
    compute_style_vector,
    decay_weighted_average,
    MIN_OBSERVATIONS,
)


# ── Fixtures ──


@pytest_asyncio.fixture
async def sv_household(db_session: AsyncSession) -> Household:
    h = Household(name="Style Vector Test Family")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def sv_child(db_session: AsyncSession, sv_household: Household) -> Child:
    c = Child(household_id=sv_household.id, first_name="Aria", last_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


def _build_rich_intelligence(child_id: uuid.UUID, household_id: uuid.UUID) -> LearnerIntelligence:
    """Build a LearnerIntelligence with enough data to activate all dimensions."""
    durations = [20, 22, 25, 18, 30, 28, 15, 20, 25, 22,
                 18, 20, 24, 26, 19, 21, 23, 27, 20, 22,
                 25, 18, 20, 24, 22]

    sessions = []
    for i in range(25):
        if i < 12:
            sessions.append({"hints": 5, "messages": 10, "self_corrections": 4})
        else:
            sessions.append({"hints": 0, "messages": 8, "self_corrections": 1})

    activity_type_stats = {
        "lesson": {"completed": 8, "total": 10},
        "practice": {"completed": 12, "total": 15},
        "review": {"completed": 5, "total": 5},
        "assessment": {"completed": 4, "total": 5},
    }

    time_of_day_counts = {"morning": 15, "afternoon": 8, "evening": 2}

    subject_patterns = {
        "math": {
            "strengths": [
                {"text": "mental math", "confidence": 0.8, "evidence_count": 5},
                {"text": "number sense", "confidence": 0.7, "evidence_count": 3},
            ],
            "struggles": [
                {"text": "word problems", "confidence": 0.6, "evidence_count": 4},
            ],
            "notes": [{"activity": f"Math {i}", "quality": 3 + (i % 3), "at": "2026-01-01"} for i in range(15)],
        },
        "reading": {
            "strengths": [{"text": "fluency", "confidence": 0.9, "evidence_count": 6}],
            "struggles": [{"text": "inference", "confidence": 0.5, "evidence_count": 2}],
            "notes": [{"activity": f"Read {i}", "quality": 4, "at": "2026-01-01"} for i in range(12)],
        },
    }

    transitions = []
    for i in range(30):
        if i % 3 == 0:
            transitions.append({"subject": "math", "node": f"N{i}", "from": "developing", "to": "emerging", "direction": "down", "at": "2026-01-01"})
        else:
            transitions.append({"subject": "math", "node": f"N{i}", "from": "emerging", "to": "developing", "direction": "up", "at": "2026-01-01"})

    return LearnerIntelligence(
        child_id=child_id,
        household_id=household_id,
        observation_count=80,
        engagement_patterns={
            "recent_durations": durations,
            "avg_focus_minutes": sum(durations) / len(durations),
            "time_of_day_counts": time_of_day_counts,
            "best_time_of_day": "morning",
            "activity_type_stats": activity_type_stats,
            "activity_type_preferences": {
                k: round(v["completed"] / v["total"], 2) for k, v in activity_type_stats.items()
            },
        },
        tutor_interaction_analysis={"sessions": sessions, "hint_usage_rate": 0.3, "self_correction_rate": 0.2},
        subject_patterns=subject_patterns,
        pace_trends={
            "transitions": transitions,
            "overall_mastery_rate": 0.68,
            "subject_rates": {"math": 0.65, "reading": 0.80},
        },
        parent_observations=[],
        learning_style_observations=[],
        governance_learned_preferences={},
    )


# ═══════════════════════════════════════════
# COMPUTATION TESTS
# ═══════════════════════════════════════════


class TestDecayWeightedAverage:
    def test_empty_list(self):
        assert decay_weighted_average([]) == 0.0

    def test_single_value(self):
        assert decay_weighted_average([5.0]) == 5.0

    def test_recent_values_weighted_more(self):
        result = decay_weighted_average([1.0, 1.0, 1.0, 10.0])
        assert result > 3.0

    def test_uniform_values(self):
        result = decay_weighted_average([5.0, 5.0, 5.0, 5.0])
        assert abs(result - 5.0) < 0.001


@pytest.mark.asyncio
class TestEmptyIntelligence:
    async def test_empty_intelligence_all_null(self, db_session, sv_child, sv_household):
        """No intelligence profile → all dimensions null."""
        vector = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        assert vector.dimensions_active == 0
        assert vector.optimal_session_minutes is None
        assert vector.socratic_responsiveness is None
        assert vector.frustration_threshold is None
        assert vector.recovery_rate is None
        assert vector.time_of_day_peak is None
        assert vector.modality_preference is None
        assert vector.pacing_preference is None
        assert vector.independence_level is None
        assert vector.attention_pattern is None
        assert vector.subject_affinity_map == {}
        assert vector.data_points_count == 0

    async def test_low_observation_count_all_null(self, db_session, sv_child, sv_household):
        """< 20 observations → all null."""
        intel = LearnerIntelligence(child_id=sv_child.id, household_id=sv_household.id, observation_count=10)
        db_session.add(intel)
        await db_session.flush()
        vector = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        assert vector.dimensions_active == 0
        assert vector.data_points_count == 10


class TestOptimalSessionFromDurations:
    def test_computes_from_durations(self):
        eng = {"recent_durations": list(range(15, 36))}
        result = _compute_optimal_session_minutes(eng, {})
        assert result is not None
        assert 10 <= result <= 60

    def test_insufficient_durations(self):
        eng = {"recent_durations": [20, 25]}
        assert _compute_optimal_session_minutes(eng, {}) is None


class TestSocraticFromTutorSessions:
    def test_computes_from_sessions(self):
        sessions = [{"hints": 5, "messages": 10, "self_corrections": 4}] * 12 + [{"hints": 0, "messages": 8, "self_corrections": 1}] * 13
        result = _compute_socratic_responsiveness({"sessions": sessions})
        assert result is not None
        assert 0.0 <= result <= 1.0

    def test_insufficient_sessions(self):
        sessions = [{"hints": 1, "messages": 5, "self_corrections": 1}] * 5
        assert _compute_socratic_responsiveness({"sessions": sessions}) is None


class TestFrustrationFromSubjectPatterns:
    def test_computes_from_patterns(self):
        subj = {
            "math": {
                "strengths": [{"text": "a", "confidence": 0.8, "evidence_count": 8}],
                "struggles": [{"text": "b", "confidence": 0.6, "evidence_count": 6}],
            },
            "reading": {
                "strengths": [{"text": "c", "confidence": 0.9, "evidence_count": 4}],
                "struggles": [{"text": "d", "confidence": 0.5, "evidence_count": 3}],
            },
        }
        result = _compute_frustration_threshold(subj)
        assert result is not None
        assert 0.0 <= result <= 1.0


class TestRecoveryFromTransitions:
    def test_computes_recovery(self):
        transitions = []
        for i in range(30):
            if i % 3 == 0:
                transitions.append({"direction": "down"})
            else:
                transitions.append({"direction": "up"})
        result = _compute_recovery_rate({"transitions": transitions})
        assert result is not None
        assert 0.0 <= result <= 1.0

    def test_insufficient_downs(self):
        transitions = [{"direction": "up"}] * 20
        assert _compute_recovery_rate({"transitions": transitions}) is None


class TestTimeOfDayFromCounts:
    def test_peak_morning(self):
        eng = {"time_of_day_counts": {"morning": 15, "afternoon": 8, "evening": 2}}
        assert _compute_time_of_day_peak(eng) == 9

    def test_peak_afternoon(self):
        eng = {"time_of_day_counts": {"morning": 5, "afternoon": 18, "evening": 2}}
        assert _compute_time_of_day_peak(eng) == 14

    def test_insufficient_data(self):
        eng = {"time_of_day_counts": {"morning": 5}}
        assert _compute_time_of_day_peak(eng) is None


class TestSubjectAffinityComputation:
    def test_computes_per_subject(self):
        subj = {"math": {"notes": [{"quality": 4, "activity": f"A{i}", "at": "2026-01-01"} for i in range(15)]}}
        result = _compute_subject_affinity_map({}, subj)
        assert "math" in result
        assert 0.0 <= result["math"] <= 1.0


class TestModalityFromActivityTypes:
    def test_computes_modality(self):
        eng = {"activity_type_stats": {
            "lesson": {"completed": 8, "total": 10},
            "practice": {"completed": 12, "total": 15},
            "review": {"completed": 5, "total": 5},
            "assessment": {"completed": 4, "total": 5},
        }}
        result = _compute_modality_preference(eng)
        assert result in ("visual", "auditory", "kinesthetic", "reading_writing", "mixed")

    def test_insufficient_attempts(self):
        eng = {"activity_type_stats": {"lesson": {"completed": 2, "total": 3}}}
        assert _compute_modality_preference(eng) is None


class TestPacingFromMasteryRate:
    def test_high_rate_positive(self):
        pace = {"transitions": [{"direction": "up"}] * 25, "overall_mastery_rate": 0.85}
        result = _compute_pacing_preference(pace)
        assert result is not None
        assert result > 0

    def test_low_rate_negative(self):
        pace = {"transitions": [{"direction": "down"}] * 25, "overall_mastery_rate": 0.35}
        result = _compute_pacing_preference(pace)
        assert result is not None
        assert result < 0


class TestIndependenceFromHintRate:
    def test_high_independence(self):
        sessions = [{"hints": 0, "messages": 10, "self_corrections": 1}] * 20
        result = _compute_independence_level({"sessions": sessions})
        assert result is not None
        assert result > 0.8

    def test_low_independence(self):
        sessions = [{"hints": 5, "messages": 10, "self_corrections": 1}] * 20
        result = _compute_independence_level({"sessions": sessions})
        assert result is not None
        assert result < 0.2


class TestAttentionSustained:
    def test_sustained_low_variance(self):
        durations = [20] * 25
        result = _compute_attention_pattern({"recent_durations": durations})
        assert result == "sustained"


class TestAttentionVariable:
    def test_variable_high_variance(self):
        durations = [10, 50, 15, 45, 12, 48, 10, 55, 14, 42,
                     10, 50, 15, 45, 12, 48, 10, 55, 14, 42, 35]
        result = _compute_attention_pattern({"recent_durations": durations})
        assert result == "variable"


# ═══════════════════════════════════════════
# PARENT GOVERNANCE TESTS
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestParentGovernance:
    async def test_override_locks_value(self, db_session, sv_child, sv_household):
        intel = _build_rich_intelligence(sv_child.id, sv_household.id)
        db_session.add(intel)
        await db_session.flush()
        vector = LearnerStyleVector(
            child_id=sv_child.id, household_id=sv_household.id,
            parent_overrides={"optimal_session_minutes": {"value": 25, "locked": True}},
        )
        db_session.add(vector)
        await db_session.flush()
        result = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        assert result.optimal_session_minutes == 25

    async def test_override_unlock_restores_computed(self, db_session, sv_child, sv_household):
        intel = _build_rich_intelligence(sv_child.id, sv_household.id)
        db_session.add(intel)
        await db_session.flush()
        vector = LearnerStyleVector(
            child_id=sv_child.id, household_id=sv_household.id,
            parent_overrides={"optimal_session_minutes": {"value": 45, "locked": False}},
        )
        db_session.add(vector)
        await db_session.flush()
        result = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        # Computed ~22, not the unlocked 45
        assert result.optimal_session_minutes != 45

    async def test_bounds_clamp_value(self, db_session, sv_child, sv_household):
        intel = _build_rich_intelligence(sv_child.id, sv_household.id)
        db_session.add(intel)
        await db_session.flush()
        vector = LearnerStyleVector(
            child_id=sv_child.id, household_id=sv_household.id,
            parent_bounds={"optimal_session_minutes": {"min": 15, "max": 18}},
        )
        db_session.add(vector)
        await db_session.flush()
        result = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        assert result.optimal_session_minutes is not None
        assert result.optimal_session_minutes <= 18


@pytest.mark.asyncio
class TestDimensionsActiveCount:
    async def test_count_matches_non_null(self, db_session, sv_child, sv_household):
        intel = _build_rich_intelligence(sv_child.id, sv_household.id)
        db_session.add(intel)
        await db_session.flush()
        vector = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        # Count manually
        fields = ["optimal_session_minutes", "socratic_responsiveness", "frustration_threshold",
                   "recovery_rate", "time_of_day_peak", "modality_preference",
                   "pacing_preference", "independence_level", "attention_pattern"]
        manual = sum(1 for f in fields if getattr(vector, f) is not None)
        if vector.subject_affinity_map:
            manual += 1
        assert vector.dimensions_active == manual


# ═══════════════════════════════════════════
# UPSERT + IDEMPOTENT TESTS
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestUpsert:
    async def test_second_compute_updates_existing(self, db_session, sv_child, sv_household):
        intel = _build_rich_intelligence(sv_child.id, sv_household.id)
        db_session.add(intel)
        await db_session.flush()
        v1 = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        id1 = v1.id
        v2 = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        assert v2.id == id1
        count = (await db_session.execute(
            select(LearnerStyleVector).where(LearnerStyleVector.child_id == sv_child.id)
        )).scalars().all()
        assert len(count) == 1


# ═══════════════════════════════════════════
# PROMPT INJECTION TESTS
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestBuildStyleContext:
    async def test_no_vector_empty_string(self, db_session, sv_child, sv_household):
        ctx = await build_style_context(db_session, sv_child.id, sv_household.id)
        assert ctx == ""

    async def test_partial_vector(self, db_session, sv_child, sv_household):
        intel = LearnerIntelligence(
            child_id=sv_child.id, household_id=sv_household.id,
            observation_count=25,
            engagement_patterns={
                "recent_durations": list(range(15, 36)),
                "time_of_day_counts": {"morning": 15, "afternoon": 5, "evening": 2},
                "activity_type_stats": {},
            },
            subject_patterns={}, tutor_interaction_analysis={}, pace_trends={},
        )
        db_session.add(intel)
        await db_session.flush()
        await compute_style_vector(db_session, sv_child.id, sv_household.id)
        ctx = await build_style_context(db_session, sv_child.id, sv_household.id)
        assert "LEARNER STYLE PROFILE" in ctx
        assert "Optimal session" in ctx
        assert "Socratic" not in ctx

    async def test_full_vector_all_labels(self, db_session, sv_child, sv_household):
        intel = _build_rich_intelligence(sv_child.id, sv_household.id)
        db_session.add(intel)
        await db_session.flush()
        await compute_style_vector(db_session, sv_child.id, sv_household.id)
        ctx = await build_style_context(db_session, sv_child.id, sv_household.id)
        assert "LEARNER STYLE PROFILE" in ctx
        assert "observations" in ctx
        # Should contain dimension labels
        for keyword in ["Optimal session", "Morning", "Subject affinities"]:
            assert keyword in ctx


class TestContextLabels:
    def test_labels_low(self):
        assert _level_label(0.2) == "LOW"

    def test_labels_moderate(self):
        assert _level_label(0.5) == "MODERATE"

    def test_labels_high(self):
        assert _level_label(0.8) == "HIGH"

    def test_labels_boundary_low(self):
        assert _level_label(0.29) == "LOW"

    def test_labels_boundary_high(self):
        assert _level_label(0.71) == "HIGH"


class TestGuidanceBuilders:
    def test_tutor_guidance_none(self):
        assert build_tutor_style_guidance(None) == ""

    def test_planner_guidance_none(self):
        assert build_planner_style_guidance(None) == ""

    def test_advisor_guidance_content(self):
        assert "Learning Style Insights" in build_advisor_style_guidance()


# ═══════════════════════════════════════════
# INTEGRATION TEST
# ═══════════════════════════════════════════


@pytest.mark.asyncio
class TestFullLifecycle:
    async def test_full_lifecycle(self, db_session, sv_child, sv_household):
        """Seed data → compute → context → override → recompute → verify override persists."""
        # 1. Seed intelligence
        intel = _build_rich_intelligence(sv_child.id, sv_household.id)
        db_session.add(intel)
        await db_session.flush()

        # 2. Compute vector
        vector = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        assert vector.dimensions_active >= 5
        original_session = vector.optimal_session_minutes

        # 3. Build style context
        ctx = await build_style_context(db_session, sv_child.id, sv_household.id)
        assert ctx != ""
        assert "LEARNER STYLE PROFILE" in ctx

        # 4. Set parent override
        overrides = dict(vector.parent_overrides or {})
        overrides["optimal_session_minutes"] = {"value": 30, "locked": True}
        vector.parent_overrides = overrides
        await db_session.flush()

        # 5. Recompute — override should persist
        vector2 = await compute_style_vector(db_session, sv_child.id, sv_household.id)
        assert vector2.optimal_session_minutes == 30  # Parent override wins
        assert vector2.dimensions_active >= 5
