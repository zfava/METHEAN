"""Cohort-level analytics for institutional mode.

Aggregates mastery progress across every learner enrolled in a given
learning map. Intended for instructors and department admins who need
a class-wide view rather than a per-student dashboard.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import ChildMapEnrollment, LearningNode
from app.models.enums import MasteryLevel
from app.models.state import ChildNodeState


def _level_str(level) -> str:
    return level.value if hasattr(level, "value") else str(level)


async def get_cohort_stats(
    map_id: uuid.UUID,
    household_id: uuid.UUID,
    db: AsyncSession,
) -> dict:
    """Summarize a map's enrolled learners: mastery distribution and
    completion rate. Returns a zero-state shape when there are no
    enrollments so callers do not need to special-case empty cohorts.
    """
    enrolled_q = await db.execute(
        select(ChildMapEnrollment).where(
            ChildMapEnrollment.learning_map_id == map_id,
            ChildMapEnrollment.household_id == household_id,
        )
    )
    enrolled = enrolled_q.scalars().all()
    child_ids = [e.child_id for e in enrolled]

    if not child_ids:
        return {
            "total_enrolled": 0,
            "mastery_distribution": {
                "not_started": 0,
                "emerging": 0,
                "developing": 0,
                "proficient": 0,
                "mastered": 0,
            },
            "completion_rate": 0.0,
            "total_nodes": 0,
            "at_risk": [],
        }

    nodes_q = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id == map_id,
            LearningNode.household_id == household_id,
            LearningNode.is_active.is_(True),
        )
    )
    node_list = nodes_q.scalars().all()
    total_nodes = len(node_list)
    node_ids = [n.id for n in node_list]

    states: list[ChildNodeState] = []
    if node_ids:
        states_q = await db.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id.in_(child_ids),
                ChildNodeState.node_id.in_(node_ids),
            )
        )
        states = list(states_q.scalars().all())

    mastery_counts = {
        "not_started": 0,
        "emerging": 0,
        "developing": 0,
        "proficient": 0,
        "mastered": 0,
    }

    # Every (child, node) pair is a potential state. Missing rows count
    # as not_started so the distribution sums to total_enrolled * total_nodes.
    observed: set[tuple[uuid.UUID, uuid.UUID]] = set()
    for s in states:
        level = _level_str(s.mastery_level)
        if level in mastery_counts:
            mastery_counts[level] += 1
        observed.add((s.child_id, s.node_id))

    missing = (len(child_ids) * total_nodes) - len(observed)
    if missing > 0:
        mastery_counts["not_started"] += missing

    # Per-child completion: every node must be proficient or mastered.
    earned_levels = {MasteryLevel.proficient, MasteryLevel.mastered}
    child_mastered_count: dict[uuid.UUID, int] = {cid: 0 for cid in child_ids}
    for s in states:
        if s.mastery_level in earned_levels:
            child_mastered_count[s.child_id] += 1

    completed_children = [
        cid for cid in child_ids if total_nodes > 0 and child_mastered_count[cid] == total_nodes
    ]
    completion_rate = (len(completed_children) / len(child_ids)) * 100 if child_ids else 0.0

    at_risk = [
        str(cid)
        for cid in child_ids
        if total_nodes > 0 and child_mastered_count[cid] == 0
    ]

    return {
        "total_enrolled": len(child_ids),
        "mastery_distribution": mastery_counts,
        "completion_rate": round(completion_rate, 1),
        "total_nodes": total_nodes,
        "at_risk": at_risk,
    }
