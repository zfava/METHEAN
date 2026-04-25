"""Annual Curriculum API — year-long curriculum management."""

import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db, require_active_subscription, require_child_access, require_permission
from app.models.annual_curriculum import AnnualCurriculum
from app.models.enums import ActivityStatus, ActivityType
from app.models.governance import Activity, Plan, PlanWeek
from app.models.identity import Child, User
from app.services.annual_curriculum import (
    approve_annual_curriculum,
    generate_annual_curriculum,
    get_curriculum_history,
    record_week_completion,
)

router = APIRouter(tags=["annual-curriculum"], dependencies=[Depends(require_active_subscription)])


# ── Schemas ───────────────────────────────────────


class GenerateRequest(BaseModel):
    subject_name: str
    academic_year: str  # "2026-2027"
    learning_map_id: uuid.UUID | None = None
    hours_per_week: float = 4.0
    total_weeks: int = 36
    start_date: date | None = None
    scope_notes: str | None = None


class WeekNotesRequest(BaseModel):
    notes: str


class AddActivityRequest(BaseModel):
    title: str
    activity_type: str = "lesson"
    description: str = ""
    estimated_minutes: int = 30
    scheduled_day: str = "Monday"  # Monday-Friday


class EditActivityRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    estimated_minutes: int | None = None
    scheduled_day: str | None = None
    activity_type: str | None = None


class MoveActivityRequest(BaseModel):
    target_week_number: int


# ── Helpers ───────────────────────────────────────


async def _get_child(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> Child:
    result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = result.scalar_one_or_none()
    if not child:
        raise HTTPException(404, "Child not found")
    return child


async def _get_curriculum(db: AsyncSession, cid: uuid.UUID, hid: uuid.UUID) -> AnnualCurriculum:
    result = await db.execute(
        select(AnnualCurriculum).where(AnnualCurriculum.id == cid, AnnualCurriculum.household_id == hid)
    )
    c = result.scalar_one_or_none()
    if not c:
        raise HTTPException(404, "Curriculum not found")
    return c


async def _get_plan_week(db: AsyncSession, curriculum: AnnualCurriculum, week_number: int) -> PlanWeek:
    plan_result = await db.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum.id))
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise HTTPException(404, "No plan for this curriculum")
    week_result = await db.execute(
        select(PlanWeek).where(PlanWeek.plan_id == plan.id, PlanWeek.week_number == week_number)
    )
    week = week_result.scalar_one_or_none()
    if not week:
        raise HTTPException(404, f"Week {week_number} not found")
    return week


# ── Endpoints ─────────────────────────────────────


@router.post("/children/{child_id}/curricula/generate", status_code=201)
async def generate_curriculum(
    child_id: uuid.UUID,
    body: GenerateRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("plans.generate")),
    _child: Child = Depends(require_child_access("write")),
):
    """Generate a new annual curriculum draft."""
    await _get_child(db, child_id, user.household_id)
    curriculum = await generate_annual_curriculum(
        db,
        user.household_id,
        child_id,
        user.id,
        subject_name=body.subject_name,
        academic_year=body.academic_year,
        learning_map_id=body.learning_map_id,
        hours_per_week=body.hours_per_week,
        total_weeks=body.total_weeks,
        start_date=body.start_date,
        scope_notes=body.scope_notes,
    )
    await db.commit()
    return {"id": str(curriculum.id), "status": curriculum.status, "subject": curriculum.subject_name}


@router.get("/children/{child_id}/curricula")
async def list_curricula(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
):
    """List all annual curricula for a child."""
    await _get_child(db, child_id, user.household_id)
    result = await db.execute(
        select(AnnualCurriculum)
        .where(AnnualCurriculum.child_id == child_id, AnnualCurriculum.household_id == user.household_id)
        .order_by(AnnualCurriculum.academic_year.desc(), AnnualCurriculum.subject_name)
    )
    curricula = result.scalars().all()
    return [
        {
            "id": str(c.id),
            "subject_name": c.subject_name,
            "academic_year": c.academic_year,
            "grade_level": c.grade_level,
            "status": c.status,
            "total_weeks": c.total_weeks,
            "hours_per_week": c.hours_per_week,
            "start_date": str(c.start_date),
            "end_date": str(c.end_date),
        }
        for c in curricula
    ]


@router.get("/curricula/{curriculum_id}")
async def get_curriculum(
    curriculum_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get full curriculum detail including scope_sequence."""
    c = await _get_curriculum(db, curriculum_id, user.household_id)
    return {
        "id": str(c.id),
        "subject_name": c.subject_name,
        "academic_year": c.academic_year,
        "grade_level": c.grade_level,
        "status": c.status,
        "total_weeks": c.total_weeks,
        "hours_per_week": c.hours_per_week,
        "start_date": str(c.start_date),
        "end_date": str(c.end_date),
        "scope_sequence": c.scope_sequence,
        "actual_record": c.actual_record,
        "approved_at": str(c.approved_at) if c.approved_at else None,
        "learning_map_id": str(c.learning_map_id) if c.learning_map_id else None,
    }


@router.get("/curricula/{curriculum_id}/weeks/{week_number}")
async def get_week_detail(
    curriculum_id: uuid.UUID,
    week_number: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get planned + actual for a specific week."""
    await _get_curriculum(db, curriculum_id, user.household_id)
    return await get_curriculum_history(db, curriculum_id, week_number)


@router.post("/curricula/{curriculum_id}/approve")
async def approve_curriculum(
    curriculum_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_permission("approve.activities")),
):
    """Approve curriculum and materialize ALL weeks."""
    curriculum = await approve_annual_curriculum(db, curriculum_id, user.id, user.household_id)
    await db.commit()
    return {"status": curriculum.status, "approved_at": str(curriculum.approved_at)}


@router.put("/curricula/{curriculum_id}/weeks/{week_number}/notes")
async def update_week_notes(
    curriculum_id: uuid.UUID,
    week_number: int,
    body: WeekNotesRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Add/update parent notes for a week."""
    curriculum = await _get_curriculum(db, curriculum_id, user.household_id)
    actual = dict(curriculum.actual_record or {})
    weeks = dict(actual.get("weeks", {}))
    week_data = dict(weeks.get(str(week_number), {}))
    week_data["parent_notes"] = body.notes
    weeks[str(week_number)] = week_data
    actual["weeks"] = weeks
    curriculum.actual_record = actual
    from sqlalchemy.orm.attributes import flag_modified

    flag_modified(curriculum, "actual_record")
    await db.commit()
    return {"week_number": week_number, "notes": body.notes}


@router.post("/curricula/{curriculum_id}/weeks/{week_number}/activities", status_code=201)
async def add_activity_to_week(
    curriculum_id: uuid.UUID,
    week_number: int,
    body: AddActivityRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Add a parent-authored activity to a specific week."""
    curriculum = await _get_curriculum(db, curriculum_id, user.household_id)
    week = await _get_plan_week(db, curriculum, week_number)

    day_offsets = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
    offset = day_offsets.get(body.scheduled_day, 0)
    scheduled = week.start_date + __import__("datetime").timedelta(days=offset)

    type_map = {
        "lesson": ActivityType.lesson,
        "practice": ActivityType.practice,
        "assessment": ActivityType.assessment,
        "review": ActivityType.review,
        "project": ActivityType.project,
        "field_trip": ActivityType.field_trip,
    }

    activity = Activity(
        plan_week_id=week.id,
        household_id=user.household_id,
        activity_type=type_map.get(body.activity_type, ActivityType.lesson),
        title=body.title,
        description=body.description,
        estimated_minutes=body.estimated_minutes,
        status=ActivityStatus.scheduled,
        scheduled_date=scheduled,
        sort_order=99,
        governance_approved=True,  # Parent-authored = auto-approved
    )
    db.add(activity)
    await db.commit()
    return {"id": str(activity.id), "title": activity.title, "week_number": week_number}


@router.delete("/curricula/{curriculum_id}/weeks/{week_number}/activities/{activity_id}")
async def remove_activity(
    curriculum_id: uuid.UUID,
    week_number: int,
    activity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Soft-delete an activity (set status to cancelled)."""
    await _get_curriculum(db, curriculum_id, user.household_id)
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(404, "Activity not found")
    activity.status = ActivityStatus.cancelled
    await db.commit()
    return {"id": str(activity.id), "status": "cancelled"}


@router.put("/curricula/{curriculum_id}/weeks/{week_number}/activities/{activity_id}")
async def edit_activity(
    curriculum_id: uuid.UUID,
    week_number: int,
    activity_id: uuid.UUID,
    body: EditActivityRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Edit an activity within a week."""
    await _get_curriculum(db, curriculum_id, user.household_id)
    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(404, "Activity not found")

    if body.title is not None:
        activity.title = body.title
    if body.description is not None:
        activity.description = body.description
    if body.estimated_minutes is not None:
        activity.estimated_minutes = body.estimated_minutes
    if body.activity_type is not None:
        type_map = {
            "lesson": ActivityType.lesson,
            "practice": ActivityType.practice,
            "assessment": ActivityType.assessment,
            "review": ActivityType.review,
            "project": ActivityType.project,
            "field_trip": ActivityType.field_trip,
        }
        activity.activity_type = type_map.get(body.activity_type, activity.activity_type)

    await db.commit()
    return {"id": str(activity.id), "title": activity.title}


@router.post("/curricula/{curriculum_id}/weeks/{week_number}/activities/{activity_id}/move")
async def move_activity(
    curriculum_id: uuid.UUID,
    week_number: int,
    activity_id: uuid.UUID,
    body: MoveActivityRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Move an activity to a different week."""
    curriculum = await _get_curriculum(db, curriculum_id, user.household_id)
    target_week = await _get_plan_week(db, curriculum, body.target_week_number)

    result = await db.execute(select(Activity).where(Activity.id == activity_id))
    activity = result.scalar_one_or_none()
    if not activity:
        raise HTTPException(404, "Activity not found")

    activity.plan_week_id = target_week.id
    # Update scheduled date to target week's Monday
    activity.scheduled_date = target_week.start_date
    await db.commit()
    return {"id": str(activity.id), "moved_to_week": body.target_week_number}


@router.post("/curricula/{curriculum_id}/weeks/{week_number}/complete")
async def complete_week(
    curriculum_id: uuid.UUID,
    week_number: int,
    notes: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Record week completion with actual data."""
    await _get_curriculum(db, curriculum_id, user.household_id)
    result = await record_week_completion(db, curriculum_id, week_number, notes)
    await db.commit()
    return result


@router.get("/children/{child_id}/curricula/history")
async def curriculum_history(
    child_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
):
    """Get complete historical record across all years and subjects."""
    await _get_child(db, child_id, user.household_id)
    result = await db.execute(
        select(AnnualCurriculum)
        .where(AnnualCurriculum.child_id == child_id, AnnualCurriculum.household_id == user.household_id)
        .order_by(AnnualCurriculum.academic_year.desc(), AnnualCurriculum.subject_name)
    )
    curricula = result.scalars().all()

    # Group by academic year
    by_year: dict[str, list] = {}
    for c in curricula:
        year_list = by_year.setdefault(c.academic_year, [])
        actual = c.actual_record or {}
        completed_weeks = len(actual.get("weeks", {}))
        year_list.append(
            {
                "id": str(c.id),
                "subject_name": c.subject_name,
                "grade_level": c.grade_level,
                "status": c.status,
                "total_weeks": c.total_weeks,
                "completed_weeks": completed_weeks,
                "hours_per_week": c.hours_per_week,
            }
        )

    return {"child_id": str(child_id), "years": by_year}


@router.get("/children/{child_id}/curricula/history/{academic_year}")
async def curriculum_history_year(
    child_id: uuid.UUID,
    academic_year: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    _child: Child = Depends(require_child_access("read")),
):
    """Get all curricula for a specific academic year."""
    await _get_child(db, child_id, user.household_id)
    result = await db.execute(
        select(AnnualCurriculum)
        .where(
            AnnualCurriculum.child_id == child_id,
            AnnualCurriculum.household_id == user.household_id,
            AnnualCurriculum.academic_year == academic_year,
        )
        .order_by(AnnualCurriculum.subject_name)
    )
    curricula = result.scalars().all()
    return [
        {
            "id": str(c.id),
            "subject_name": c.subject_name,
            "grade_level": c.grade_level,
            "status": c.status,
            "total_weeks": c.total_weeks,
            "hours_per_week": c.hours_per_week,
            "scope_overview": c.scope_sequence.get("overview", ""),
        }
        for c in curricula
    ]
