"""Academic Calendar API.

Exposes GET and PUT endpoints for the household academic calendar,
stored inside household.settings["academic_calendar"]. The underlying
service (app.services.academic_calendar) is already used by the
planner, curriculum, and compliance layers; this router lets the
frontend read and write the same structure.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.identity import Household, User
from app.services.academic_calendar import DEFAULT_CALENDAR, get_academic_calendar

router = APIRouter(tags=["academic-calendar"])


_VALID_DAYS = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
_VALID_SCHEDULE_TYPES = {"traditional", "year_round", "custom"}


class AcademicCalendarUpdate(BaseModel):
    """All fields optional so partial updates work."""

    schedule_type: str | None = None
    total_instructional_weeks: int | None = None
    instruction_days_per_week: int | None = None
    instruction_days: list[str] | None = None
    breaks: list[dict] | None = None
    start_date: str | None = None
    daily_target_minutes: dict | None = None


@router.get("/household/academic-calendar")
async def get_calendar(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Return the household's academic calendar, merged with defaults."""
    return await get_academic_calendar(db, user.household_id)


@router.put("/household/academic-calendar")
async def update_calendar(
    body: AcademicCalendarUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """Persist calendar preferences under household.settings.academic_calendar.

    Validates:
    - total_instructional_weeks is between 1 and 52
    - instruction_days_per_week is between 1 and 7
    - instruction_days are real weekday names
    - schedule_type is one of the allowed values
    """
    if body.total_instructional_weeks is not None and not (1 <= body.total_instructional_weeks <= 52):
        raise HTTPException(status_code=400, detail="total_instructional_weeks must be between 1 and 52")

    if body.instruction_days_per_week is not None and not (1 <= body.instruction_days_per_week <= 7):
        raise HTTPException(status_code=400, detail="instruction_days_per_week must be between 1 and 7")

    if body.instruction_days is not None:
        invalid = [d for d in body.instruction_days if d.lower() not in _VALID_DAYS]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Invalid day names: {invalid}")

    if body.schedule_type is not None and body.schedule_type not in _VALID_SCHEDULE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"schedule_type must be one of {sorted(_VALID_SCHEDULE_TYPES)}",
        )

    household = (
        await db.execute(select(Household).where(Household.id == user.household_id))
    ).scalar_one()

    # Merge with existing calendar so partial updates preserve other fields.
    settings = dict(household.settings or {})
    current = {**DEFAULT_CALENDAR, **settings.get("academic_calendar", {})}
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    current.update(updates)
    settings["academic_calendar"] = current
    household.settings = settings
    await db.flush()

    return current
