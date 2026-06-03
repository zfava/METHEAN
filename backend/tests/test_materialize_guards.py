"""Guards against silent zero-materialization.

A year plan that materializes 0 weeks or 0 activities from a populated request
must raise MaterializationError, not silently create an empty Plan (audit
cross-cutting issue 2). A partial library (needs_content placeholders) must NOT
trip the guard.
"""

from datetime import date

import pytest
from sqlalchemy import func, select

from app.core.config import settings
from app.models.annual_curriculum import AnnualCurriculum
from app.models.governance import Plan, PlanWeek
from app.services.annual_curriculum import (
    MaterializationError,
    approve_annual_curriculum,
    generate_annual_curriculum,
    materialize_full_year,
)
from app.services.node_resolver import resolve_content_id_to_uuid

START = date(2026, 9, 1)
END = date(2027, 6, 1)


def _activity(day="Monday", atype="lesson"):
    return {"day": day, "type": atype, "title": f"{atype} {day}", "description": "d", "minutes": 25}


async def _curriculum(db, household, child, user, scope_sequence, subject_name="Mathematics"):
    c = AnnualCurriculum(
        household_id=household.id,
        child_id=child.id,
        created_by=user.id,
        subject_name=subject_name,
        academic_year="2026-2027",
        grade_level="1st",
        total_weeks=36,
        hours_per_week=4.0,
        start_date=START,
        end_date=END,
        scope_sequence=scope_sequence,
        status="active",
        actual_record={"weeks": {}},
    )
    db.add(c)
    await db.flush()
    return c


# ── Raise on broken shape ────────────────────────────────────────────────


async def test_raises_on_year_plans_mock_shape(db_session, household, child, user):
    """The old broken mock shape (year_plans, no weeks) raises, not silent 0."""
    broken = {
        "plan_name": "Classical Education Plan",
        "philosophy_alignment": "trivium",
        "year_plans": {"2026-2027": {"grade": "1st", "subjects": []}},
    }
    c = await _curriculum(db_session, household, child, user, broken)

    with pytest.raises(MaterializationError) as exc:
        await materialize_full_year(db_session, c)

    msg = str(exc.value)
    assert "Mathematics" in msg
    assert "year_plans" in msg  # names the likely cause
    assert "weeks" in msg  # names expected contract


async def test_raises_on_zero_activities(db_session, household, child, user):
    """Weeks present but every week has no activities -> raise."""
    scope = {
        "overview": "x",
        "weeks": [
            {"week_number": 1, "suggested_activities": [], "focus_nodes": [], "assessment_focus": "a"},
            {"week_number": 2, "suggested_activities": [], "focus_nodes": [], "assessment_focus": "b"},
        ],
    }
    c = await _curriculum(db_session, household, child, user, scope)

    with pytest.raises(MaterializationError) as exc:
        await materialize_full_year(db_session, c)
    assert "0 activities" in str(exc.value)

    # The broken plan left no half-built Plan rows behind.
    plan_count = await db_session.scalar(
        select(func.count()).select_from(Plan).where(Plan.annual_curriculum_id == c.id)
    )
    assert plan_count == 0


# ── No false positives ───────────────────────────────────────────────────


async def test_partial_library_materializes_without_raising(db_session, household, child, user):
    """Some real weeks + some needs_content placeholders -> materializes fine."""
    res = await resolve_content_id_to_uuid(db_session, "mf-01", household.id)
    real_node = str(res.node_uuid)

    scope = {
        "overview": "partial",
        "weeks": [
            {
                "week_number": 1,
                "assessment_focus": "real",
                "suggested_activities": [_activity("Monday", "lesson"), _activity("Tuesday", "practice")],
                "focus_nodes": [real_node],
            },
            {
                "week_number": 2,
                "assessment_focus": "placeholder",
                "suggested_activities": [_activity("Monday", "review")],
                "focus_nodes": [],
                "needs_content": True,
            },
            {
                "week_number": 3,
                "assessment_focus": "placeholder",
                "suggested_activities": [_activity("Monday", "review")],
                "focus_nodes": [],
                "needs_content": True,
            },
        ],
    }
    c = await _curriculum(db_session, household, child, user, scope)

    result = await materialize_full_year(db_session, c)
    assert result["weeks_created"] == 3
    assert result["activities_created"] == 4


async def test_all_needs_content_warns_but_does_not_raise(db_session, household, child, user, caplog):
    """All-placeholder plan still materializes (activities present) + warns."""
    scope = {
        "weeks": [
            {
                "week_number": w,
                "assessment_focus": "consolidation",
                "suggested_activities": [_activity("Monday", "review")],
                "focus_nodes": [],
                "needs_content": True,
            }
            for w in (1, 2)
        ],
    }
    c = await _curriculum(db_session, household, child, user, scope)

    with caplog.at_level("WARNING", logger="methean.annual_curriculum"):
        result = await materialize_full_year(db_session, c)

    assert result["weeks_created"] == 2
    assert result["activities_created"] == 2
    assert any("needs_content" in r.message for r in caplog.records)


async def test_empty_scope_unauthored_subject_warns_no_raise(db_session, household, child, user, caplog):
    """An empty scope_sequence for a subject with no authored scope is a
    genuine empty shell: warn, return 0, do not raise."""
    c = await _curriculum(db_session, household, child, user, {}, subject_name="Underwater Basket Weaving")

    with caplog.at_level("WARNING", logger="methean.annual_curriculum"):
        result = await materialize_full_year(db_session, c)

    assert result == {"weeks_created": 0, "activities_created": 0}
    assert any("empty_unauthored" in r.message for r in caplog.records)


# ── Regression: native path does not trip the guard ──────────────────────


async def test_native_path_materializes_without_tripping_guard(db_session, household, child, user, monkeypatch):
    """No API keys + mock off: the native generator produces real weeks and
    materialization succeeds (>0 weeks), never raising MaterializationError."""
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
        total_weeks=4,
        content_tier="foundational",
    )
    # Must not raise.
    await approve_annual_curriculum(db_session, curriculum.id, user.id, household.id)

    plan = (await db_session.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum.id))).scalar_one()
    week_count = await db_session.scalar(select(func.count()).select_from(PlanWeek).where(PlanWeek.plan_id == plan.id))
    assert week_count == 4
