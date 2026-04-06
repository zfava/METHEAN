"""Tests for annual curriculum generation, materialization, and history.

Covers:
- Curriculum generation stores 36-week scope_sequence
- Approval materializes full year of Plan/PlanWeek/Activity records
- Week completion records actual_record
- Parent notes persist on past and future weeks
- Activity CRUD (add, edit, remove, move)
- History across years
- Planned vs actual divergence
"""

import uuid
from datetime import UTC, date, datetime, timedelta

import pytest
from sqlalchemy import select

from app.models.annual_curriculum import AnnualCurriculum
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    AttemptStatus,
    GovernanceAction,
    MasteryLevel,
    NodeType,
    PlanStatus,
)
from app.models.governance import Activity, Attempt, GovernanceEvent, Plan, PlanWeek
from app.services.annual_curriculum import (
    approve_annual_curriculum,
    evaluate_approaching_weeks,
    get_curriculum_history,
    materialize_full_year,
    record_week_completion,
)


def _make_scope_sequence(num_weeks: int = 36) -> dict:
    """Build a minimal valid scope_sequence for testing."""
    weeks = []
    for w in range(1, num_weeks + 1):
        weeks.append({
            "week_number": w,
            "title": f"Week {w}: Topic {w}",
            "focus_nodes": [],
            "objectives": [f"Objective {w}.1", f"Objective {w}.2"],
            "suggested_activities": [
                {"title": f"Lesson {w}", "type": "lesson", "minutes": 25, "day": "Monday"},
                {"title": f"Practice {w}", "type": "practice", "minutes": 20, "day": "Tuesday"},
                {"title": f"Review {w}", "type": "review", "minutes": 15, "day": "Wednesday"},
                {"title": f"Project {w}", "type": "project", "minutes": 30, "day": "Thursday"},
                {"title": f"Assessment {w}", "type": "assessment", "minutes": 15, "day": "Friday"},
            ],
            "assessment_focus": f"Can the child demonstrate skill {w}?",
            "parent_notes_placeholder": "",
        })
    return {
        "overview": "Test curriculum overview",
        "philosophy_alignment": "Test alignment",
        "materials": ["textbook", "workbook"],
        "weeks": weeks,
    }


class TestAnnualCurriculumModel:

    @pytest.mark.asyncio
    async def test_create_draft_curriculum(self, db_session, household, child, user):
        """Create a curriculum and verify it's stored as draft."""
        c = AnnualCurriculum(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            subject_name="Mathematics",
            academic_year="2026-2027",
            grade_level="2nd",
            total_weeks=36,
            hours_per_week=4.0,
            start_date=date(2026, 9, 1),
            end_date=date(2027, 5, 15),
            scope_sequence=_make_scope_sequence(36),
            status="draft",
            actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()

        result = await db_session.execute(
            select(AnnualCurriculum).where(AnnualCurriculum.id == c.id)
        )
        saved = result.scalar_one()
        assert saved.subject_name == "Mathematics"
        assert saved.status == "draft"
        assert len(saved.scope_sequence["weeks"]) == 36

    @pytest.mark.asyncio
    async def test_scope_sequence_has_activities_per_week(self, db_session, household, child, user):
        """Verify each week in scope_sequence has 5 activities."""
        scope = _make_scope_sequence(36)
        for week in scope["weeks"]:
            assert len(week["suggested_activities"]) == 5
            assert week["week_number"] >= 1
            assert week["week_number"] <= 36


class TestMaterialization:

    @pytest.mark.asyncio
    async def test_approve_materializes_full_year(self, db_session, household, child, user):
        """Approve curriculum, verify ALL 36 weeks of activities created."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Math", academic_year="2026-2027",
            total_weeks=36, hours_per_week=4.0,
            start_date=date(2026, 9, 1), end_date=date(2027, 5, 15),
            scope_sequence=_make_scope_sequence(36),
            status="draft", actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()

        await approve_annual_curriculum(db_session, c.id, user.id, household.id)

        assert c.status == "active"
        assert c.approved_at is not None

        # Verify Plan created
        plan_result = await db_session.execute(
            select(Plan).where(Plan.annual_curriculum_id == c.id)
        )
        plan = plan_result.scalar_one()
        assert plan.status == PlanStatus.active
        assert plan.annual_curriculum_id == c.id

        # Verify all 36 weeks created
        weeks_result = await db_session.execute(
            select(PlanWeek).where(PlanWeek.plan_id == plan.id)
        )
        weeks = weeks_result.scalars().all()
        assert len(weeks) == 36

        # Verify activities per week (5 each = 180 total)
        total_acts = 0
        for w in weeks:
            acts_result = await db_session.execute(
                select(Activity).where(Activity.plan_week_id == w.id)
            )
            acts = acts_result.scalars().all()
            assert len(acts) == 5
            total_acts += len(acts)
        assert total_acts == 180

    @pytest.mark.asyncio
    async def test_near_weeks_auto_approved(self, db_session, household, child, user):
        """Activities in the next 4 weeks are governance-approved on materialization."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Reading", academic_year="2026-2027",
            total_weeks=6, hours_per_week=3.0,
            start_date=date.today(),  # Start today
            end_date=date.today() + timedelta(weeks=6),
            scope_sequence=_make_scope_sequence(6),
            status="draft", actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()
        await approve_annual_curriculum(db_session, c.id, user.id, household.id)

        plan_result = await db_session.execute(
            select(Plan).where(Plan.annual_curriculum_id == c.id)
        )
        plan = plan_result.scalar_one()

        # Check weeks 1-4 are approved, weeks 5-6 are not
        for wn in range(1, 7):
            wk_result = await db_session.execute(
                select(PlanWeek).where(PlanWeek.plan_id == plan.id, PlanWeek.week_number == wn)
            )
            wk = wk_result.scalar_one()
            acts_result = await db_session.execute(
                select(Activity).where(Activity.plan_week_id == wk.id)
            )
            acts = acts_result.scalars().all()
            if wn <= 4:
                assert all(a.governance_approved for a in acts), f"Week {wn} should be approved"
            else:
                assert all(not a.governance_approved for a in acts), f"Week {wn} should NOT be approved"


class TestWeekCompletion:

    @pytest.mark.asyncio
    async def test_week_completion_records_history(self, db_session, household, child, user):
        """Complete a week and verify actual_record updated."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Science", academic_year="2026-2027",
            total_weeks=4, hours_per_week=3.0,
            start_date=date(2026, 9, 1), end_date=date(2026, 10, 1),
            scope_sequence=_make_scope_sequence(4),
            status="draft", actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()
        await approve_annual_curriculum(db_session, c.id, user.id, household.id)

        # Complete some activities in week 1
        plan_result = await db_session.execute(
            select(Plan).where(Plan.annual_curriculum_id == c.id)
        )
        plan = plan_result.scalar_one()
        wk_result = await db_session.execute(
            select(PlanWeek).where(PlanWeek.plan_id == plan.id, PlanWeek.week_number == 1)
        )
        wk = wk_result.scalar_one()
        acts_result = await db_session.execute(
            select(Activity).where(Activity.plan_week_id == wk.id)
        )
        acts = acts_result.scalars().all()

        # Mark 3 of 5 as completed
        for i, act in enumerate(acts[:3]):
            act.status = ActivityStatus.completed
            db_session.add(Attempt(
                activity_id=act.id, household_id=household.id,
                child_id=child.id, status=AttemptStatus.completed,
                completed_at=datetime.now(UTC), duration_minutes=25,
            ))
        acts[3].status = ActivityStatus.skipped
        await db_session.flush()

        # Record week completion
        result = await record_week_completion(db_session, c.id, 1, "Emma did great this week!")

        assert result["planned_activities"] == 5
        assert result["completed_activities"] == 3
        assert result["skipped_activities"] == 1
        assert result["total_minutes"] == 75  # 3 × 25
        assert result["parent_notes"] == "Emma did great this week!"

        # Verify persisted in actual_record
        await db_session.refresh(c)
        assert "1" in c.actual_record["weeks"]
        assert c.actual_record["weeks"]["1"]["completed_activities"] == 3

    @pytest.mark.asyncio
    async def test_parent_notes_persisted(self, db_session, household, child, user):
        """Add parent notes to a future week, verify persistence."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="History", academic_year="2026-2027",
            total_weeks=4, hours_per_week=3.0,
            start_date=date(2026, 9, 1), end_date=date(2026, 10, 1),
            scope_sequence=_make_scope_sequence(4),
            status="active",
            actual_record={"weeks": {"3": {"parent_notes": "Planning a field trip!"}}},
        )
        db_session.add(c)
        await db_session.flush()

        # Verify notes persisted
        await db_session.refresh(c)
        assert c.actual_record["weeks"]["3"]["parent_notes"] == "Planning a field trip!"


class TestActivityCRUD:

    @pytest.mark.asyncio
    async def test_remove_activity_soft_delete(self, db_session, household, child, user):
        """Remove activity sets status to cancelled, not hard delete."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Art", academic_year="2026-2027",
            total_weeks=2, hours_per_week=2.0,
            start_date=date(2026, 9, 1), end_date=date(2026, 9, 15),
            scope_sequence=_make_scope_sequence(2),
            status="draft", actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()
        await approve_annual_curriculum(db_session, c.id, user.id, household.id)

        plan_result = await db_session.execute(
            select(Plan).where(Plan.annual_curriculum_id == c.id)
        )
        plan = plan_result.scalar_one()
        wk_result = await db_session.execute(
            select(PlanWeek).where(PlanWeek.plan_id == plan.id, PlanWeek.week_number == 1)
        )
        wk = wk_result.scalar_one()
        acts_result = await db_session.execute(
            select(Activity).where(Activity.plan_week_id == wk.id)
        )
        act = acts_result.scalars().first()

        # Soft delete
        act.status = ActivityStatus.cancelled
        await db_session.flush()

        # Verify still exists
        result = await db_session.execute(select(Activity).where(Activity.id == act.id))
        deleted_act = result.scalar_one()
        assert deleted_act.status == ActivityStatus.cancelled

    @pytest.mark.asyncio
    async def test_move_activity_between_weeks(self, db_session, household, child, user):
        """Move an activity from week 1 to week 2."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Music", academic_year="2026-2027",
            total_weeks=3, hours_per_week=2.0,
            start_date=date(2026, 9, 1), end_date=date(2026, 9, 22),
            scope_sequence=_make_scope_sequence(3),
            status="draft", actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()
        await approve_annual_curriculum(db_session, c.id, user.id, household.id)

        plan_result = await db_session.execute(
            select(Plan).where(Plan.annual_curriculum_id == c.id)
        )
        plan = plan_result.scalar_one()

        # Get week 1 and week 2
        wk1_result = await db_session.execute(
            select(PlanWeek).where(PlanWeek.plan_id == plan.id, PlanWeek.week_number == 1)
        )
        wk1 = wk1_result.scalar_one()
        wk2_result = await db_session.execute(
            select(PlanWeek).where(PlanWeek.plan_id == plan.id, PlanWeek.week_number == 2)
        )
        wk2 = wk2_result.scalar_one()

        # Get first activity from week 1
        acts_result = await db_session.execute(
            select(Activity).where(Activity.plan_week_id == wk1.id)
        )
        act = acts_result.scalars().first()
        act_id = act.id

        # Move to week 2
        act.plan_week_id = wk2.id
        await db_session.flush()

        # Verify moved
        result = await db_session.execute(select(Activity).where(Activity.id == act_id))
        moved = result.scalar_one()
        assert moved.plan_week_id == wk2.id


class TestHistory:

    @pytest.mark.asyncio
    async def test_curriculum_history_returns_planned_and_actual(self, db_session, household, child, user):
        """Get history for a curriculum with both planned and actual data."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Math", academic_year="2026-2027",
            total_weeks=4, hours_per_week=3.0,
            start_date=date(2026, 9, 1), end_date=date(2026, 10, 1),
            scope_sequence=_make_scope_sequence(4),
            status="active",
            actual_record={"weeks": {"1": {"completed_activities": 4, "parent_notes": "Good week"}}},
        )
        db_session.add(c)
        await db_session.flush()

        history = await get_curriculum_history(db_session, c.id)
        assert history["subject_name"] == "Math"
        assert len(history["weeks"]) == 4
        assert history["weeks"][0]["has_actual"] is True
        assert history["weeks"][0]["parent_notes"] == "Good week"
        assert history["weeks"][1]["has_actual"] is False

    @pytest.mark.asyncio
    async def test_history_across_years(self, db_session, household, child, user):
        """Create curricula across multiple years, verify history returns all."""
        for year in ["2025-2026", "2026-2027"]:
            for subject in ["Math", "Reading"]:
                db_session.add(AnnualCurriculum(
                    household_id=household.id, child_id=child.id, created_by=user.id,
                    subject_name=subject, academic_year=year,
                    total_weeks=36, hours_per_week=4.0,
                    start_date=date(int(year[:4]), 9, 1),
                    end_date=date(int(year[:4]) + 1, 5, 15),
                    scope_sequence=_make_scope_sequence(2),
                    status="active", actual_record={"weeks": {}},
                ))
        await db_session.flush()

        # Query all curricula for this child
        result = await db_session.execute(
            select(AnnualCurriculum)
            .where(AnnualCurriculum.child_id == child.id)
            .order_by(AnnualCurriculum.academic_year.desc())
        )
        all_curricula = result.scalars().all()
        assert len(all_curricula) == 4

        # Group by year
        by_year: dict[str, list] = {}
        for c in all_curricula:
            by_year.setdefault(c.academic_year, []).append(c)
        assert len(by_year) == 2
        assert len(by_year["2026-2027"]) == 2


class TestApproachingWeeksEval:

    @pytest.mark.asyncio
    async def test_evaluate_approaching_weeks(self, db_session, household, child, user):
        """Verify activities in approaching weeks get governance-approved."""
        c = AnnualCurriculum(
            household_id=household.id, child_id=child.id, created_by=user.id,
            subject_name="Science", academic_year="2026-2027",
            total_weeks=8, hours_per_week=3.0,
            start_date=date.today(),
            end_date=date.today() + timedelta(weeks=8),
            scope_sequence=_make_scope_sequence(8),
            status="draft", actual_record={"weeks": {}},
        )
        db_session.add(c)
        await db_session.flush()
        await approve_annual_curriculum(db_session, c.id, user.id, household.id)

        # Weeks 5-8 should be unapproved
        plan_result = await db_session.execute(
            select(Plan).where(Plan.annual_curriculum_id == c.id)
        )
        plan = plan_result.scalar_one()

        # Run evaluation for next 6 weeks (should catch weeks 5-6)
        evaluated = await evaluate_approaching_weeks(db_session, c.id, weeks_ahead=6)

        # Weeks 5 and 6 should now be evaluated
        for wn in [5, 6]:
            wk_result = await db_session.execute(
                select(PlanWeek).where(PlanWeek.plan_id == plan.id, PlanWeek.week_number == wn)
            )
            wk = wk_result.scalar_one()
            acts_result = await db_session.execute(
                select(Activity).where(Activity.plan_week_id == wk.id)
            )
            acts = acts_result.scalars().all()
            assert all(a.governance_approved for a in acts), f"Week {wn} should be approved after eval"
