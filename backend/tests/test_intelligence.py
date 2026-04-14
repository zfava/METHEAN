"""Tests for the Learner Intelligence service."""

import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Child, Household
from app.models.intelligence import LearnerIntelligence
from app.services.intelligence import (
    get_intelligence_context,
    record_attempt_engagement,
    record_evaluation_insight,
    record_governance_pattern,
    record_mastery_transition,
    record_tutor_interaction,
)


@pytest_asyncio.fixture
async def intel_household(db_session: AsyncSession) -> Household:
    h = Household(name="Intelligence Test Family")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def intel_child(db_session: AsyncSession, intel_household: Household) -> Child:
    c = Child(household_id=intel_household.id, first_name="Emma", last_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest.mark.asyncio
async def test_get_intelligence_context_empty(db_session, intel_child, intel_household):
    """No profile yet — returns empty dict (graceful degradation)."""
    ctx = await get_intelligence_context(db_session, intel_child.id, intel_household.id)
    assert ctx == {}


@pytest.mark.asyncio
async def test_record_evaluation_insight_creates_profile(db_session, intel_child, intel_household):
    """Recording an evaluation insight creates a LearnerIntelligence profile if none exists."""
    await record_evaluation_insight(
        db_session,
        intel_child.id,
        intel_household.id,
        evaluation_result={"strengths": ["mental math"], "areas_for_improvement": ["word problems"]},
        activity_title="Math Lesson 1",
        subject="math",
    )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one_or_none()
    assert profile is not None
    assert "math" in profile.subject_patterns
    assert len(profile.subject_patterns["math"]["strengths"]) == 1
    assert profile.subject_patterns["math"]["strengths"][0]["text"] == "mental math"
    assert len(profile.subject_patterns["math"]["struggles"]) == 1
    assert profile.observation_count == 1


@pytest.mark.asyncio
async def test_record_evaluation_deduplicates(db_session, intel_child, intel_household):
    """Repeated observations increase confidence instead of duplicating."""
    for _ in range(4):
        await record_evaluation_insight(
            db_session,
            intel_child.id,
            intel_household.id,
            evaluation_result={"strengths": ["pattern recognition"], "areas_for_improvement": []},
            activity_title="Math Practice",
            subject="math",
        )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one()
    strengths = profile.subject_patterns["math"]["strengths"]
    # Should have ONE entry with increased confidence and evidence_count
    pattern_rec = [s for s in strengths if s["text"] == "pattern recognition"]
    assert len(pattern_rec) == 1
    assert pattern_rec[0]["evidence_count"] == 1
    assert pattern_rec[0]["confidence"] == 0.5


@pytest.mark.asyncio
async def test_record_attempt_engagement(db_session, intel_child, intel_household):
    """Engagement patterns track rolling averages and time of day."""
    for i in range(5):
        await record_attempt_engagement(
            db_session,
            intel_child.id,
            intel_household.id,
            duration_minutes=20 + i * 5,
            activity_type="lesson",
            time_of_day="morning",
            completed=True,
            estimated_minutes=30,
        )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one()
    eng = profile.engagement_patterns
    assert eng["avg_focus_minutes"] > 0
    assert eng["best_time_of_day"] == "morning"
    assert "lesson" in eng["activity_type_preferences"]
    assert eng["activity_type_preferences"]["lesson"] == 1.0  # All completed


@pytest.mark.asyncio
async def test_record_attempt_flags_focus(db_session, intel_child, intel_household):
    """Short durations relative to estimate flag potential focus issues."""
    await record_attempt_engagement(
        db_session,
        intel_child.id,
        intel_household.id,
        duration_minutes=5,
        activity_type="lesson",
        time_of_day="afternoon",
        completed=True,
        estimated_minutes=30,
    )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one()
    assert len(profile.engagement_patterns.get("focus_flags", [])) == 1


@pytest.mark.asyncio
async def test_record_tutor_interaction(db_session, intel_child, intel_household):
    """Tutor interactions track hint usage and self-correction rates."""
    await record_tutor_interaction(
        db_session,
        intel_child.id,
        intel_household.id,
        subject="science",
        messages_count=10,
        hints_used=3,
        self_corrections=2,
    )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one()
    analysis = profile.tutor_interaction_analysis
    assert analysis["hint_usage_rate"] == 0.3
    assert analysis["self_correction_rate"] == 0.2
    assert analysis["question_frequency_by_subject"]["science"] == 10


@pytest.mark.asyncio
async def test_record_mastery_transition(db_session, intel_child, intel_household):
    """Mastery transitions update pace trends."""
    await record_mastery_transition(
        db_session,
        intel_child.id,
        intel_household.id,
        subject="math",
        from_level="developing",
        to_level="proficient",
        node_title="Fractions",
    )
    await record_mastery_transition(
        db_session,
        intel_child.id,
        intel_household.id,
        subject="math",
        from_level="proficient",
        to_level="mastered",
        node_title="Decimals",
    )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one()
    pace = profile.pace_trends
    assert pace["overall_mastery_rate"] == 1.0  # 1 up, 0 down
    assert pace["subject_rates"]["math"] == 1.0
    assert len(pace["transitions"]) == 1


@pytest.mark.asyncio
async def test_record_governance_pattern_computes_ceiling(db_session, intel_child, intel_household):
    """After 20+ decisions, computes auto_approve_difficulty_ceiling."""
    # Create the profile first
    profile = LearnerIntelligence(child_id=intel_child.id, household_id=intel_household.id)
    db_session.add(profile)
    await db_session.flush()

    # Record 25 approve decisions at difficulty 3
    for _ in range(25):
        await record_governance_pattern(
            db_session,
            intel_household.id,
            action="approve",
            activity_type="lesson",
            difficulty=3,
        )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one()
    prefs = profile.governance_learned_preferences
    assert prefs.get("auto_approve_difficulty_ceiling") == 3
    assert len(prefs["decisions"]) == 25


@pytest.mark.asyncio
async def test_get_intelligence_context_with_data(db_session, intel_child, intel_household):
    """Context synthesis returns structured summary from populated data."""
    # Populate some data
    await record_evaluation_insight(
        db_session,
        intel_child.id,
        intel_household.id,
        evaluation_result={"strengths": ["critical thinking"], "areas_for_improvement": ["time management"]},
        activity_title="Science Lab",
        subject="science",
    )
    await record_attempt_engagement(
        db_session,
        intel_child.id,
        intel_household.id,
        duration_minutes=25,
        activity_type="practice",
        time_of_day="morning",
        completed=True,
    )

    ctx = await get_intelligence_context(db_session, intel_child.id, intel_household.id)
    assert ctx != {}
    assert "science" in ctx["subject_patterns"]
    assert ctx["subject_patterns"]["science"]["strengths"] == ["critical thinking"]
    assert ctx["engagement"]["avg_focus_minutes"] == 25.0
    assert ctx["observation_count"] >= 2


@pytest.mark.asyncio
async def test_parent_observations_in_context(db_session, intel_child, intel_household):
    """Parent observations are included verbatim in synthesis."""
    profile = LearnerIntelligence(
        child_id=intel_child.id,
        household_id=intel_household.id,
        parent_observations=[
            {"observation": "Emma learns best through stories", "created_at": "2026-01-01T00:00:00Z"},
        ],
    )
    db_session.add(profile)
    await db_session.flush()

    ctx = await get_intelligence_context(db_session, intel_child.id, intel_household.id)
    assert "Emma learns best through stories" in ctx["parent_observations"]


@pytest.mark.asyncio
async def test_parent_override_replaces_data(db_session, intel_child, intel_household):
    """Parent override directly replaces AI-accumulated data."""
    # Build some AI data first
    await record_evaluation_insight(
        db_session,
        intel_child.id,
        intel_household.id,
        evaluation_result={"strengths": ["ai-observed-strength"]},
        activity_title="Test",
        subject="math",
    )

    from sqlalchemy import select

    result = await db_session.execute(select(LearnerIntelligence).where(LearnerIntelligence.child_id == intel_child.id))
    profile = result.scalar_one()

    # Parent overrides strengths
    patterns = dict(profile.subject_patterns)
    patterns["math"]["strengths"] = [{"text": "parent-says-geometry", "confidence": 1.0, "evidence_count": 1}]
    profile.subject_patterns = patterns
    await db_session.flush()

    ctx = await get_intelligence_context(db_session, intel_child.id, intel_household.id)
    assert ctx["subject_patterns"]["math"]["strengths"] == ["parent-says-geometry"]
