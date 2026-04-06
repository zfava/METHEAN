"""Weekly curriculum evaluation task.

Evaluates governance on approaching weeks and finalizes
completed weeks that haven't been recorded yet.
"""

import asyncio

from sqlalchemy import select

from app.core.database import async_session_factory
from app.models.annual_curriculum import AnnualCurriculum
from app.services.annual_curriculum import evaluate_approaching_weeks, record_week_completion
from datetime import date


async def _run_curriculum_eval() -> dict:
    """Evaluate approaching weeks for all active curricula."""
    async with async_session_factory() as db:
        result = await db.execute(
            select(AnnualCurriculum).where(AnnualCurriculum.status == "active")
        )
        curricula = result.scalars().all()

        total_evaluated = 0
        total_completed = 0
        today = date.today()

        for curriculum in curricula:
            # Evaluate approaching weeks
            evaluated = await evaluate_approaching_weeks(db, curriculum.id, weeks_ahead=4)
            total_evaluated += len(evaluated)

            # Auto-complete past weeks that haven't been finalized
            actual = curriculum.actual_record or {}
            recorded_weeks = set(actual.get("weeks", {}).keys())

            # Check which weeks have passed
            for wn in range(1, curriculum.total_weeks + 1):
                from datetime import timedelta
                week_end = curriculum.start_date + timedelta(weeks=wn)
                if week_end < today and str(wn) not in recorded_weeks:
                    try:
                        await record_week_completion(db, curriculum.id, wn)
                        total_completed += 1
                    except (ValueError, Exception):
                        pass

        await db.commit()
        return {
            "curricula_processed": len(curricula),
            "activities_evaluated": total_evaluated,
            "weeks_auto_completed": total_completed,
        }


def run_curriculum_eval_sync() -> dict:
    return asyncio.get_event_loop().run_until_complete(_run_curriculum_eval())
