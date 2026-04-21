"""Attendance tracking from activity completion data.

A "school day" is any day where the child completed at least one
activity or logged at least 30 minutes of learning time. No manual
logging needed — METHEAN tracks automatically.
"""

import uuid
from collections import defaultdict
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AttemptStatus
from app.models.governance import Attempt


async def get_attendance_record(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    start_date: date,
    end_date: date,
) -> dict:
    """Generate an attendance record from attempt completion data."""

    # Get all completed attempts in the period
    result = await db.execute(
        select(Attempt).where(
            Attempt.child_id == child_id,
            Attempt.household_id == household_id,
            Attempt.status == AttemptStatus.completed,
        )
    )
    attempts = result.scalars().all()

    # Group by date
    daily: dict[date, dict] = defaultdict(lambda: {"hours": 0.0, "activities": 0, "subjects": set()})

    for attempt in attempts:
        if attempt.completed_at:
            d = attempt.completed_at.date()
            if start_date <= d <= end_date:
                mins = attempt.duration_minutes or 15
                daily[d]["hours"] += mins / 60
                daily[d]["activities"] += 1

    # Build daily log
    daily_log = []
    current = start_date
    school_days = 0

    while current <= end_date:
        day_data = daily.get(current)
        is_weekend = current.weekday() >= 5
        is_school_day = day_data is not None and (day_data["hours"] >= 0.5 or day_data["activities"] > 0)

        entry = {
            "date": current.isoformat(),
            "is_school_day": is_school_day,
            "hours": round(day_data["hours"], 1) if day_data else 0,
            "activities_completed": day_data["activities"] if day_data else 0,
        }
        if not is_school_day:
            entry["reason"] = "weekend" if is_weekend else "no activity"

        daily_log.append(entry)
        if is_school_day:
            school_days += 1
        current += timedelta(days=1)

    # Monthly summary
    monthly: dict[str, dict] = defaultdict(lambda: {"school_days": 0, "total_hours": 0.0})
    for entry in daily_log:
        month_key = entry["date"][:7]  # YYYY-MM
        if entry["is_school_day"]:
            monthly[month_key]["school_days"] += 1
            monthly[month_key]["total_hours"] += entry["hours"]

    monthly_summary = [
        {
            "month": k,
            "school_days": v["school_days"],
            "total_hours": round(v["total_hours"], 1),
            "avg_hours_per_day": round(v["total_hours"] / v["school_days"], 1) if v["school_days"] else 0,
        }
        for k, v in sorted(monthly.items())
    ]

    return {
        "period": {"start": start_date.isoformat(), "end": end_date.isoformat()},
        "total_school_days": school_days,
        "daily_log": daily_log,
        "monthly_summary": monthly_summary,
    }
