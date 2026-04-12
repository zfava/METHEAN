"""Achievement system — celebrates effort and growth, not speed or competition.

Every achievement is parent-governed via achievement_visibility rules.
"""

import uuid
from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.achievements import Achievement, Streak
from app.models.governance import Activity, Attempt

# ── Built-in achievement definitions ──

ACHIEVEMENT_DEFS = [
    {
        "type": "first_steps",
        "title": "First Steps",
        "description": "Completed your very first activity",
        "icon": "🌱",
        "category": "milestone",
    },
    {
        "type": "week_warrior",
        "title": "Week Warrior",
        "description": "Kept a 5-day learning streak",
        "icon": "🔥",
        "category": "streak",
    },
    {
        "type": "fortnight_force",
        "title": "Fortnight Force",
        "description": "Kept a 14-day learning streak",
        "icon": "⚡",
        "category": "streak",
    },
    {
        "type": "century_club",
        "title": "Century Club",
        "description": "Completed 100 activities",
        "icon": "💯",
        "category": "milestone",
    },
    {
        "type": "subject_star",
        "title": "Subject Star",
        "description": "Achieved first mastery in a subject",
        "icon": "🌟",
        "category": "mastery",
    },
    {
        "type": "speed_learner",
        "title": "Speed Learner",
        "description": "Mastered a concept in fewer attempts than average",
        "icon": "🚀",
        "category": "mastery",
    },
    {
        "type": "comeback_kid",
        "title": "Comeback Kid",
        "description": "Re-mastered a concept that had decayed",
        "icon": "💪",
        "category": "mastery",
    },
    {
        "type": "deep_thinker",
        "title": "Deep Thinker",
        "description": "Spent 10+ minutes in a single tutor conversation",
        "icon": "🧠",
        "category": "engagement",
    },
    {
        "type": "explorer",
        "title": "Explorer",
        "description": "Completed activities in 5 different subjects",
        "icon": "🧭",
        "category": "breadth",
    },
]

DEFS_BY_TYPE = {d["type"]: d for d in ACHIEVEMENT_DEFS}


async def _has_achievement(db: AsyncSession, child_id: uuid.UUID, achievement_type: str) -> bool:
    result = await db.execute(
        select(Achievement.id)
        .where(
            Achievement.child_id == child_id,
            Achievement.achievement_type == achievement_type,
        )
        .limit(1)
    )
    return result.scalar_one_or_none() is not None


async def _grant(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    achievement_type: str,
    title_override: str | None = None,
    metadata: dict | None = None,
) -> Achievement | None:
    if await _has_achievement(db, child_id, achievement_type):
        return None

    defn = DEFS_BY_TYPE.get(achievement_type, {})
    ach = Achievement(
        child_id=child_id,
        household_id=household_id,
        achievement_type=achievement_type,
        title=title_override or defn.get("title", achievement_type),
        description=defn.get("description"),
        icon=defn.get("icon", "⭐"),
        metadata_=metadata or {},
    )
    db.add(ach)
    await db.flush()
    return ach


async def check_achievements(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    trigger_event: str,
    context: dict | None = None,
) -> list[Achievement]:
    """Check and grant any newly earned achievements. Returns list of new ones."""
    earned: list[Achievement] = []
    ctx = context or {}

    # Count total completed activities
    total_result = await db.execute(
        select(func.count())
        .select_from(Attempt)
        .where(
            Attempt.child_id == child_id,
            Attempt.status == "completed",
        )
    )
    total_completed = total_result.scalar() or 0

    # First Steps
    if total_completed >= 1:
        ach = await _grant(db, child_id, household_id, "first_steps")
        if ach:
            earned.append(ach)

    # Century Club
    if total_completed >= 100:
        ach = await _grant(db, child_id, household_id, "century_club")
        if ach:
            earned.append(ach)

    # Subject Star (first mastery in any subject)
    if trigger_event == "mastery_change" and ctx.get("new_level") == "mastered":
        subject = ctx.get("subject", "")
        f"subject_star_{subject.lower().replace(' ', '_')}" if subject else "subject_star"
        ach = await _grant(
            db,
            child_id,
            household_id,
            "subject_star",
            title_override=f"Subject Star: {subject}" if subject else "Subject Star",
            metadata={"subject": subject},
        )
        if ach:
            earned.append(ach)

    # Comeback Kid (re-mastered after decay)
    if (
        trigger_event == "mastery_change"
        and ctx.get("new_level") == "mastered"
        and ctx.get("old_level") in ("developing", "emerging")
    ):
        ach = await _grant(db, child_id, household_id, "comeback_kid", metadata=ctx)
        if ach:
            earned.append(ach)

    # Speed Learner (mastered in fewer attempts than average)
    if trigger_event == "mastery_change" and ctx.get("new_level") == "mastered":
        node_id = ctx.get("node_id")
        if node_id:
            attempt_count_result = await db.execute(
                select(func.count())
                .select_from(Attempt)
                .where(
                    Attempt.child_id == child_id,
                )
            )
            avg_attempts = (attempt_count_result.scalar() or 0) / max(total_completed, 1)
            node_attempts = ctx.get("attempts", 1)
            if node_attempts < avg_attempts * 0.7 and avg_attempts > 2:
                ach = await _grant(db, child_id, household_id, "speed_learner", metadata=ctx)
                if ach:
                    earned.append(ach)

    # Explorer (5 different subjects)
    if trigger_event == "activity_complete":
        subject_count_result = await db.execute(
            select(func.count(func.distinct(Activity.subject_area))).where(
                Activity.household_id == household_id,
                Activity.status == "completed",
                Activity.subject_area.isnot(None),
            )
        )
        subject_count = subject_count_result.scalar() or 0
        if subject_count >= 5:
            ach = await _grant(db, child_id, household_id, "explorer")
            if ach:
                earned.append(ach)

    # Streak-based achievements (check current streak)
    streak = await _get_or_create_streak(db, child_id, household_id)
    if streak.current_streak >= 5:
        ach = await _grant(db, child_id, household_id, "week_warrior")
        if ach:
            earned.append(ach)
    if streak.current_streak >= 14:
        ach = await _grant(db, child_id, household_id, "fortnight_force")
        if ach:
            earned.append(ach)

    return earned


async def _get_or_create_streak(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> Streak:
    result = await db.execute(select(Streak).where(Streak.child_id == child_id))
    streak = result.scalar_one_or_none()
    if streak:
        return streak
    streak = Streak(child_id=child_id, household_id=household_id)
    db.add(streak)
    await db.flush()
    return streak


async def update_streak(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
) -> Streak:
    """Update streak based on activity completion today."""
    streak = await _get_or_create_streak(db, child_id, household_id)
    today = date.today()

    if streak.last_activity_date == today:
        return streak  # Already counted today

    if streak.last_activity_date == today - timedelta(days=1):
        # Consecutive day
        streak.current_streak += 1
    elif streak.last_activity_date is None or streak.last_activity_date < today - timedelta(days=1):
        # Streak broken (or first ever)
        streak.current_streak = 1

    streak.last_activity_date = today
    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    await db.flush()
    return streak


async def get_achievements(db: AsyncSession, child_id: uuid.UUID) -> list[dict]:
    """Get all earned achievements for a child."""
    result = await db.execute(
        select(Achievement).where(Achievement.child_id == child_id).order_by(Achievement.earned_at.desc())
    )
    return [
        {
            "id": str(a.id),
            "type": a.achievement_type,
            "title": a.title,
            "description": a.description,
            "icon": a.icon,
            "earned_at": a.earned_at.isoformat() if a.earned_at else None,
            "metadata": a.metadata_ or {},
        }
        for a in result.scalars().all()
    ]


async def get_streak(db: AsyncSession, child_id: uuid.UUID, household_id: uuid.UUID) -> dict:
    """Get streak info for a child."""
    streak = await _get_or_create_streak(db, child_id, household_id)
    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "last_activity_date": streak.last_activity_date.isoformat() if streak.last_activity_date else None,
    }


def get_all_definitions() -> list[dict]:
    """Return all possible achievement definitions (for gallery display)."""
    return [
        {
            "type": d["type"],
            "title": d["title"],
            "description": d["description"],
            "icon": d["icon"],
            "category": d["category"],
        }
        for d in ACHIEVEMENT_DEFS
    ]
