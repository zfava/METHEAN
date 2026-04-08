"""Academic Calendar service.

Reads household academic calendar preferences from settings JSONB.
Provides utilities for instruction days, break detection, and date math.
All downstream systems (planner, curriculum, compliance) use this.
"""

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.identity import Household


DEFAULT_CALENDAR = {
    "schedule_type": "traditional",
    "total_instructional_weeks": 36,
    "instruction_days_per_week": 5,
    "instruction_days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
    "breaks": [],
    "daily_target_minutes": {
        "default": 120,
        "K-2": 90,
        "3-5": 120,
        "6-8": 150,
        "9-12": 180,
    },
}


async def get_academic_calendar(db: AsyncSession, household_id) -> dict:
    """Return the household's academic calendar preferences, with defaults."""
    result = await db.execute(select(Household).where(Household.id == household_id))
    household = result.scalar_one_or_none()
    if not household or not household.settings:
        return dict(DEFAULT_CALENDAR)
    cal = household.settings.get("academic_calendar", {})
    return {**DEFAULT_CALENDAR, **cal}


def get_daily_minutes_for_grade(calendar: dict, grade_level: str) -> int:
    """Return the daily target minutes for a grade level."""
    targets = calendar.get("daily_target_minutes", DEFAULT_CALENDAR["daily_target_minutes"])
    band = "default"
    if grade_level in ("K", "1st", "2nd"):
        band = "K-2"
    elif grade_level in ("3rd", "4th", "5th"):
        band = "3-5"
    elif grade_level in ("6th", "7th", "8th"):
        band = "6-8"
    elif grade_level in ("9th", "10th", "11th", "12th"):
        band = "9-12"
    return targets.get(band, targets.get("default", 120))


def get_instruction_days(calendar: dict) -> list[str]:
    """Return the list of instruction day names (lowercase)."""
    return calendar.get("instruction_days", DEFAULT_CALENDAR["instruction_days"])


def is_break_date(calendar: dict, check_date: date) -> bool:
    """Check if a date falls within a break period."""
    for brk in calendar.get("breaks", []):
        start = date.fromisoformat(brk["start"]) if isinstance(brk["start"], str) else brk["start"]
        end = date.fromisoformat(brk["end"]) if isinstance(brk["end"], str) else brk["end"]
        if start <= check_date <= end:
            return True
    return False


def calculate_end_date(start_date: date, total_weeks: int, calendar: dict) -> date:
    """Calculate the end date by counting instructional weeks, skipping breaks."""
    instruction_days = get_instruction_days(calendar)
    if not instruction_days:
        return start_date + timedelta(weeks=total_weeks)

    first_day = instruction_days[0]
    current = start_date
    weeks_counted = 0

    while weeks_counted < total_weeks:
        if not is_break_date(calendar, current):
            day_name = current.strftime("%A").lower()
            if day_name == first_day:
                weeks_counted += 1
        current += timedelta(days=1)
        if (current - start_date).days > 730:
            break

    return current


def get_week_end_for_start(week_start: date, calendar: dict) -> date:
    """Find the last instruction day in the week starting from week_start."""
    instruction_days = get_instruction_days(calendar)
    week_end = week_start
    for i in range(7):
        d = week_start + timedelta(days=i)
        if d.strftime("%A").lower() in instruction_days:
            week_end = d
    return week_end
