"""Daily temporal governance trigger evaluation.

Checks rules with trigger_conditions and fires them when met:
- age_threshold: child reaches specified age
- mastery_milestone: child completes specified % of a map
- date_scheduled: a specific date arrives

Each trigger fires only once (sets triggered_at to prevent re-firing).
"""

import asyncio
import time
from datetime import UTC, date, datetime

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.models.curriculum import LearningNode
from app.models.enums import GovernanceAction, MasteryLevel
from app.models.governance import GovernanceEvent, GovernanceRule
from app.models.identity import Child
from app.models.state import ChildNodeState

logger = structlog.get_logger()


async def evaluate_temporal_triggers(
    session_factory: async_sessionmaker | None = None,
) -> dict:
    """Evaluate all temporal rule triggers. Returns stats."""
    start = time.monotonic()

    if session_factory is None:
        engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    triggers_checked = 0
    triggers_fired = 0
    today = date.today()

    async with session_factory() as db:
        # Get all rules with trigger_conditions
        result = await db.execute(
            select(GovernanceRule).where(
                GovernanceRule.trigger_conditions.isnot(None),
            )
        )
        rules = result.scalars().all()

        for rule in rules:
            tc = rule.trigger_conditions or {}
            if not tc or not tc.get("type"):
                continue
            if tc.get("triggered_at"):
                continue  # Already fired

            triggers_checked += 1
            should_fire = False
            fire_reason = ""

            trigger_type = tc["type"]
            action = tc.get("action", "activate")

            if trigger_type == "age_threshold":
                child_id = tc.get("child_id")
                age_years = tc.get("age_years")
                if child_id and age_years:
                    child_result = await db.execute(select(Child).where(Child.id == child_id))
                    child = child_result.scalar_one_or_none()
                    if child and child.date_of_birth:
                        age = (today - child.date_of_birth).days / 365.25
                        if age >= age_years:
                            should_fire = True
                            fire_reason = f"{child.first_name} turned {age_years}"

            elif trigger_type == "mastery_milestone":
                child_id = tc.get("child_id")
                map_id = tc.get("map_id")
                threshold = tc.get("mastery_percentage", 100)
                if child_id and map_id:
                    # Count nodes in map
                    total_result = await db.execute(
                        select(LearningNode).where(
                            LearningNode.learning_map_id == map_id,
                            LearningNode.is_active == True,  # noqa: E712
                        )
                    )
                    total_nodes = len(total_result.scalars().all())
                    if total_nodes > 0:
                        mastered_result = await db.execute(
                            select(ChildNodeState).where(
                                ChildNodeState.child_id == child_id,
                                ChildNodeState.mastery_level == MasteryLevel.mastered,
                            )
                        )
                        mastered = len(mastered_result.scalars().all())
                        pct = (mastered / total_nodes) * 100
                        if pct >= threshold:
                            should_fire = True
                            fire_reason = f"Mastery reached {pct:.0f}% (threshold: {threshold}%)"

            elif trigger_type == "date_scheduled":
                target_date = tc.get("date")
                if target_date:
                    if isinstance(target_date, str):
                        target_date = date.fromisoformat(target_date)
                    if today >= target_date:
                        should_fire = True
                        fire_reason = f"Scheduled date {target_date} reached"

            if should_fire:
                # Apply action
                if action == "activate":
                    rule.is_active = True
                elif action == "deactivate":
                    rule.is_active = False

                # Mark as triggered — use flag_modified so SQLAlchemy detects the JSONB change
                from sqlalchemy.orm.attributes import flag_modified

                tc["triggered_at"] = datetime.now(UTC).isoformat()
                rule.trigger_conditions = tc
                flag_modified(rule, "trigger_conditions")

                # Log governance event
                db.add(
                    GovernanceEvent(
                        household_id=rule.household_id,
                        user_id=rule.created_by,
                        action=GovernanceAction.modify,
                        target_type="temporal_trigger",
                        target_id=rule.id,
                        reason=f"Temporal trigger fired: {fire_reason}. Rule '{rule.name}' {action}d.",
                        metadata_={
                            "trigger_type": trigger_type,
                            "action": action,
                            "reason": fire_reason,
                        },
                    )
                )

                triggers_fired += 1
                logger.info(
                    "temporal_trigger_fired",
                    rule_id=str(rule.id),
                    rule_name=rule.name,
                    trigger_type=trigger_type,
                    action=action,
                    reason=fire_reason,
                )

        await db.commit()

    elapsed_ms = int((time.monotonic() - start) * 1000)
    return {
        "triggers_checked": triggers_checked,
        "triggers_fired": triggers_fired,
        "duration_ms": elapsed_ms,
    }


def run_temporal_sync() -> dict:
    return asyncio.run(evaluate_temporal_triggers())
