"""Learning context service.

Builds the complete teaching context for a child's activity,
including lesson content, practice prompts, and assessment criteria.
Generates content on the fly if the linked node is unenriched.
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningNode
from app.models.governance import Activity, Attempt
from app.models.identity import Child
from app.services.content_engine import enrich_single_node
from app.services.node_content import is_enriched


async def get_activity_learning_context(
    db: AsyncSession,
    activity_id: uuid.UUID,
    household_id: uuid.UUID,
    child_id: uuid.UUID | None = None,
) -> dict:
    """Build the complete learning context for a child's activity.

    Returns structured lesson content adapted from the node's teaching
    guidance, plus activity metadata and previous attempt history.
    """
    # Fetch activity
    act_result = await db.execute(
        select(Activity).where(
            Activity.id == activity_id,
            Activity.household_id == household_id,
        )
    )
    activity = act_result.scalar_one_or_none()
    if not activity:
        raise ValueError("Activity not found")

    # Fetch child's grade level for age-appropriate adaptation
    grade_level = None
    if child_id:
        child_result = await db.execute(select(Child).where(Child.id == child_id))
        child = child_result.scalar_one_or_none()
        if child:
            grade_level = child.grade_level

    # Base activity data
    context: dict = {
        "activity": {
            "id": str(activity.id),
            "title": activity.title,
            "description": activity.description or "",
            "activity_type": activity.activity_type.value,
            "estimated_minutes": activity.estimated_minutes or 30,
            "instructions": activity.instructions or {},
        },
        "lesson": {},
        "assessment": {},
        "tutor_available": activity.activity_type.value != "assessment",
        "previous_attempts": [],
        "grade_level": grade_level,
    }

    # Fetch previous attempts for this activity + child
    if child_id:
        prev_result = await db.execute(
            select(Attempt)
            .where(Attempt.activity_id == activity_id, Attempt.child_id == child_id)
            .order_by(Attempt.created_at.desc())
            .limit(5)
        )
        for att in prev_result.scalars().all():
            context["previous_attempts"].append({
                "date": str(att.created_at.date()) if att.created_at else None,
                "status": att.status.value,
                "duration_minutes": att.duration_minutes,
                "score": att.score,
            })

    # Fetch and potentially enrich linked node content
    if activity.node_id:
        node_result = await db.execute(
            select(LearningNode).where(LearningNode.id == activity.node_id)
        )
        node = node_result.scalar_one_or_none()
        if node:
            # Ensure content exists
            if not is_enriched(node.content):
                try:
                    await enrich_single_node(db, node.id, household_id)
                    await db.refresh(node)
                except Exception:
                    pass  # Use whatever content exists

            content = node.content or {}
            tg = content.get("teaching_guidance", {})
            ac = content.get("assessment_criteria", {})
            rg = content.get("resource_guidance", {})
            te = content.get("time_estimates", {})
            objectives = content.get("learning_objectives", [])

            # Build lesson structure
            steps = []
            # Introduction as a "read" step
            if tg.get("introduction"):
                steps.append({
                    "title": "Introduction",
                    "content": tg["introduction"],
                    "type": "read",
                })
            # Scaffolding as sequential steps
            for i, scaffold in enumerate(tg.get("scaffolding_sequence", [])):
                steps.append({
                    "title": f"Step {i + 1}",
                    "content": scaffold,
                    "type": "do",
                })
            # Socratic questions as "think" steps
            for q in tg.get("socratic_questions", []):
                steps.append({
                    "title": "Think about this",
                    "content": q,
                    "type": "think",
                })

            context["lesson"] = {
                "introduction": tg.get("introduction", ""),
                "objectives": objectives,
                "steps": steps,
                "key_questions": tg.get("socratic_questions", []),
                "practice_prompts": (
                    tg.get("practice_activities", [])
                    + ac.get("sample_assessment_prompts", [])
                ),
                "resources_needed": (
                    rg.get("required", []) + rg.get("recommended", [])
                ),
                "real_world_connection": (
                    "; ".join(tg.get("real_world_connections", []))
                    if tg.get("real_world_connections")
                    else ""
                ),
                "common_misconceptions": tg.get("common_misconceptions", []),
                "estimated_time": {
                    "introduction": te.get("first_exposure", 5) // 3,
                    "guided_work": te.get("first_exposure", 15),
                    "independent_practice": te.get("practice_session", 10),
                },
            }

            context["assessment"] = {
                "prompts": ac.get("sample_assessment_prompts", []),
                "mastery_criteria": "; ".join(ac.get("mastery_indicators", [])),
                "methods": ac.get("assessment_methods", ["written work"]),
            }

    return context
