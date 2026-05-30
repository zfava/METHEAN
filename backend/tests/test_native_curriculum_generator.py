"""Tests for the deterministic native curriculum generator.

Validates the output against the EXACT contract materialize_full_year reads
(per docs/curriculum_pipeline_audit.md), determinism, the unresolved-node
path, the provider-chain insertion, and end-to-end materialization with no AI
providers configured.
"""

import uuid
from datetime import date

from sqlalchemy import func, select

from app.ai.gateway import AIProvider, _get_provider_chain
from app.core.config import settings
from app.models.governance import Activity, Plan, PlanWeek
from app.services.annual_curriculum import approve_annual_curriculum, generate_annual_curriculum
from app.services.native_curriculum_generator import (
    Topic,
    generate_for_subject,
    generate_native_curriculum,
    parse_prompt,
)

START = date(2026, 9, 1)
ACTIVITY_TYPES = {"lesson", "practice", "assessment", "review", "project", "field_trip"}


# ── Output contract ──────────────────────────────────────────────────────


async def test_contract_shape_and_uuid_focus_nodes(db_session, household):
    """Output validates field-by-field against materialize_full_year's reads."""
    out = await generate_for_subject(
        db_session,
        household.id,
        "mathematics",
        "foundational",
        hours_per_week=4.0,
        total_weeks=12,
        start_date=START,
        child_age=8.0,
    )

    assert isinstance(out.get("weeks"), list)
    weeks = out["weeks"]
    assert len(weeks) == 12
    assert [w["week_number"] for w in weeks] == list(range(1, 13))

    any_focus = False
    for w in weeks:
        assert isinstance(w["week_number"], int)
        assert isinstance(w["assessment_focus"], str)
        assert isinstance(w["focus_nodes"], list)
        assert isinstance(w["suggested_activities"], list)
        for act in w["suggested_activities"]:
            assert set(act) >= {"day", "type", "title", "description", "minutes"}
            assert act["type"] in ACTIVITY_TYPES
            assert isinstance(act["minutes"], int) and act["minutes"] > 0
            assert act["day"] in {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
        for fid in w["focus_nodes"]:
            # Must be a valid UUID string (materialize calls uuid.UUID on it).
            uuid.UUID(fid)
            any_focus = True

    # mathematics/foundational resolves to the math-foundational template, so
    # at least one week carries real focus-node UUIDs.
    assert any_focus


async def test_negative_no_year_plans_no_per_week_title_or_objectives(db_session, household):
    """The materialization output must NOT carry the broken mock shape nor the
    per-week fields materialize does not read."""
    out = await generate_for_subject(
        db_session,
        household.id,
        "mathematics",
        "foundational",
        hours_per_week=4.0,
        total_weeks=8,
        start_date=START,
    )
    assert "year_plans" not in out
    for w in out["weeks"]:
        assert "title" not in w
        assert "objectives" not in w


async def test_determinism_identical_inputs_deep_equal(db_session, household):
    """Two calls with identical inputs produce deep-equal output (the resolver
    is idempotent, so even the UUIDs match)."""
    kwargs = dict(
        subject_id="mathematics",
        level="foundational",
        hours_per_week=4.0,
        total_weeks=10,
        start_date=START,
        child_age=7.0,
    )
    first = await generate_for_subject(db_session, household.id, **kwargs)
    second = await generate_for_subject(db_session, household.id, **kwargs)
    assert first == second


async def test_unresolved_node_flags_needs_content_no_exception(db_session, household):
    """A ref with no persistable node (math/developing -> md-* has no template)
    yields a needs_content placeholder with empty focus_nodes, not a crash."""
    out = await generate_for_subject(
        db_session,
        household.id,
        "mathematics",
        "developing",
        hours_per_week=3.0,
        total_weeks=12,
        start_date=START,
    )
    weeks_with_topics = [w for w in out["weeks"] if w.get("needs_content")]
    assert weeks_with_topics, "expected at least one needs_content week"
    for w in weeks_with_topics:
        assert w["focus_nodes"] == []
    # Still a valid, fully-formed plan.
    assert len(out["weeks"]) == 12
    assert all(w["suggested_activities"] for w in out["weeks"])


# ── Pure helpers ─────────────────────────────────────────────────────────


def test_parse_prompt_extracts_scope_block_and_params():
    prompt = (
        "SUBJECT: Mathematics\n"
        "TIME BUDGET: 4.0 hours per week (240 minutes)\n"
        "TOTAL WEEKS: 36\n"
        "START DATE: 2026-09-01\n"
        "- Age: 7.0 years\n"
        "SCOPE AND SEQUENCE (2 topics in pedagogical order for foundational level):\n"
        "  math_f_01: Counting to 20 (prereqs: [none], ~2wk, concepts: counting)\n"
        "  math_f_02: Number Recognition 0-100 (prereqs: [math_f_01], ~2wk, concepts: numerals)\n"
    )
    parsed = parse_prompt(prompt)
    assert parsed is not None
    assert [t.ref for t in parsed["topics"]] == ["math_f_01", "math_f_02"]
    assert parsed["total_weeks"] == 36
    assert parsed["hours_per_week"] == 4.0
    assert parsed["start_date"] == date(2026, 9, 1)
    assert parsed["child_age"] == 7.0


def test_parse_prompt_returns_none_without_scope_block():
    # The multi-year education plan prompt has no scope block -> native defers.
    assert parse_prompt("SUBJECT: anything\nGoals: graduate") is None


async def test_topics_passed_directly(db_session, household):
    """The core accepts an explicit topic list (no scope lookup)."""
    out = await generate_native_curriculum(
        db_session,
        household.id,
        topics=[Topic("math_f_01", "Counting to 20", 2)],
        hours_per_week=5.0,
        total_weeks=3,
        start_date=START,
    )
    assert len(out["weeks"]) == 3
    # 5h/week over 5 activities -> 60 min each.
    assert out["weeks"][0]["suggested_activities"][0]["minutes"] == 60


# ── Provider chain insertion ─────────────────────────────────────────────


def test_native_inserted_before_mock(monkeypatch):
    monkeypatch.setattr(settings, "AI_API_KEY", "")
    monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")

    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)
    assert _get_provider_chain() == [AIProvider.native]

    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", True)
    chain = _get_provider_chain()
    assert AIProvider.native in chain
    assert chain.index(AIProvider.native) < chain.index(AIProvider.mock)


def test_native_after_real_providers(monkeypatch):
    monkeypatch.setattr(settings, "AI_API_KEY", "key")
    monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "fallback")
    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)
    chain = _get_provider_chain()
    assert chain == [AIProvider.claude, AIProvider.openai, AIProvider.native]


# ── End-to-end integration through the gateway ───────────────────────────


async def test_native_provider_materializes_real_weeks(db_session, household, child, user, monkeypatch):
    """No API keys and mock disabled: generate_annual_curriculum routes through
    the native provider and materialize_full_year produces real weeks."""
    monkeypatch.setattr(settings, "AI_API_KEY", "")
    monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)

    curriculum = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name="Mathematics",
        academic_year="2026-2027",
        total_weeks=6,
        content_tier="foundational",
    )

    scope = curriculum.scope_sequence
    assert "year_plans" not in scope
    assert isinstance(scope.get("weeks"), list)
    assert len(scope["weeks"]) == 6

    await approve_annual_curriculum(db_session, curriculum.id, user.id, household.id)

    plan = (await db_session.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum.id))).scalar_one()
    week_count = await db_session.scalar(select(func.count()).select_from(PlanWeek).where(PlanWeek.plan_id == plan.id))
    activity_count = await db_session.scalar(
        select(func.count())
        .select_from(Activity)
        .join(PlanWeek, Activity.plan_week_id == PlanWeek.id)
        .where(PlanWeek.plan_id == plan.id)
    )
    assert week_count == 6
    assert activity_count > 0
