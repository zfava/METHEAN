"""Learning context service.

Builds the complete teaching context for a child's activity,
including lesson content, practice prompts, and assessment criteria.
Generates content on the fly if the linked node is unenriched.
"""

import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.governance import Activity, Attempt
from app.models.identity import Child
from app.services.content_engine import enrich_single_node
from app.services.node_content import (
    is_cleared_for_surfacing,
    is_enriched,
    requires_qualified_human_present_at_runtime,
)
from app.services.supervision import get_valid_attestation

logger = structlog.get_logger()


async def build_session_signal_block(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    role: str,
) -> str:
    """The ephemeral within-session signal block injected for the tutor.

    Returns a delimited block naming the current signal plus its concrete
    directives, or an empty string. Fail closed to the tutor's default
    behavior: nothing for a non-tutor role, nothing when the tutor policy
    is off, and nothing when no live signal exists in Redis. The signal
    is read only here; it is never persisted and never shown to the child.
    """
    if role != "tutor":
        return ""

    from app.services.governance import AI_AUTONOMY_OFF, get_ai_role_policy

    try:
        policy = await get_ai_role_policy(db, household_id, "tutor")
    except Exception as exc:
        # Fail closed to the tutor's default behavior, but never silently:
        # an unreadable policy must not leak a signal block.
        logger.warning(
            "session_signal_policy_unreadable",
            household_id=str(household_id),
            child_id=str(child_id),
            error=str(exc),
        )
        return ""
    if policy == AI_AUTONOMY_OFF:
        return ""

    from app.services.tutor_session_signals import directives, read_signal

    signal = await read_signal(child_id)
    if signal is None:
        return ""

    lines = directives(signal)
    body = "\n".join(f"- {d}" for d in lines)
    return (
        "LIVE SESSION SIGNAL (ephemeral right-now read of this sitting; guidance for your "
        "next move only, never shown to the child and never a fact about mastery):\n"
        f"State: {signal}\n"
        "Do now:\n" + body
    )


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

    # Fetch child's grade level for age-appropriate adaptation, plus
    # the pedagogical philosophy selection used to surface philosophy
    # content with a clean fallback to neutral content.
    grade_level = None
    curriculum_philosophy = "traditional"
    subject_philosophies: dict = {}
    if child_id:
        child_result = await db.execute(select(Child).where(Child.id == child_id))
        child = child_result.scalar_one_or_none()
        if child:
            grade_level = child.grade_level
            curriculum_philosophy = child.curriculum_philosophy or "traditional"
            if isinstance(child.subject_philosophies, dict):
                subject_philosophies = child.subject_philosophies

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
        "lesson": {"widgets": []},
        "assessment": {},
        "practice": {"items": []},
        "reading": {"passages": []},
        "philosophy": {
            "approach": curriculum_philosophy if curriculum_philosophy != "eclectic" else "traditional",
            "content": None,
            "is_native": False,
        },
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
            context["previous_attempts"].append(
                {
                    "date": str(att.created_at.date()) if att.created_at else None,
                    "status": att.status.value,
                    "duration_minutes": att.duration_minutes,
                    "score": att.score,
                }
            )

    # Fetch and potentially enrich linked node content
    if activity.node_id:
        node_result = await db.execute(select(LearningNode).where(LearningNode.id == activity.node_id))
        node = node_result.scalar_one_or_none()
        if node:
            # SAFETY GATE (content-review): a node that requires human safety
            # review and is not cleared (safety_review.reviewed is anything
            # other than the boolean True) MUST NOT be surfaced to a learner.
            # Fail-closed: malformed or missing safety_review on a hazardous
            # node blocks surfacing. The check happens BEFORE any on-the-fly
            # enrichment, so the AI never generates content for a hazardous
            # uncleared node. is_cleared_for_surfacing is the single source
            # of truth; see app/services/node_content.py.
            if not is_cleared_for_surfacing(node.content):
                context["awaiting_human_safety_review"] = True
                context["lesson"] = {"widgets": []}
                context["assessment"] = {}
                context["practice"] = {"items": []}
                context["reading"] = {"passages": []}
                context["tutor_available"] = False
                context["philosophy"] = {
                    "approach": context["philosophy"]["approach"],
                    "content": None,
                    "is_native": False,
                }
                return context

            # SAFETY GATE (runtime presence): for nodes where the
            # supervision_basis names a qualified human who must be
            # physically present at the work, the content-review gate
            # above is necessary but NOT sufficient. A parent must have
            # attested, today, that the qualified human is present for
            # this child and this node (services/supervision.py).
            # Fail-closed: no attestation, an expired attestation, or a
            # missing child_id all block surfacing. The check runs
            # BEFORE enrichment so the AI never generates content for a
            # blocked hazardous node.
            if requires_qualified_human_present_at_runtime(node.content):
                attestation = None
                if child_id:
                    attestation = await get_valid_attestation(db, household_id, child_id, node.id)
                if attestation is None:
                    context["awaiting_qualified_human"] = True
                    context["lesson"] = {"widgets": []}
                    context["assessment"] = {}
                    context["practice"] = {"items": []}
                    context["reading"] = {"passages": []}
                    context["tutor_available"] = False
                    context["philosophy"] = {
                        "approach": context["philosophy"]["approach"],
                        "content": None,
                        "is_native": False,
                    }
                    return context

            # Ensure content exists
            if not is_enriched(node.content):
                try:
                    await enrich_single_node(db, node.id, household_id)
                    await db.refresh(node)
                except Exception as exc:
                    # Serve whatever content exists; the learner is not
                    # blocked by an enrichment outage, but the operator
                    # must see it.
                    logger.warning(
                        "enrichment_failed",
                        node_id=str(node.id),
                        household_id=str(household_id),
                        error=str(exc),
                    )

            content = node.content or {}
            tg = content.get("teaching_guidance", {})
            ac = content.get("assessment_criteria", {})
            rg = content.get("resource_guidance", {})
            te = content.get("time_estimates", {})
            objectives = content.get("learning_objectives", [])

            # Fallback: if content is still empty after enrichment, build from node title
            if not tg and not objectives:
                tg = {
                    "introduction": f"Today we're working on {node.title}. Take your time and do your best work.",
                    "scaffolding_sequence": [
                        f"Read about {node.title} carefully",
                        "Think about what you already know about this topic",
                        "Work through the activity step by step",
                        "Check your work before moving on",
                    ],
                    "socratic_questions": [
                        f"What do you already know about {node.title}?",
                        "Can you explain this in your own words?",
                        "How does this connect to something you learned before?",
                    ],
                    "practice_activities": [
                        f"Practice what you learned about {node.title}",
                    ],
                    "real_world_connections": [],
                    "common_misconceptions": [],
                }
                objectives = [
                    f"Understand the key ideas in {node.title}",
                    "Practice applying what you learn",
                ]
                ac = {
                    "sample_assessment_prompts": [
                        f"Explain what you learned about {node.title} in your own words.",
                    ],
                    "mastery_indicators": [f"Can explain {node.title} concepts clearly"],
                    "assessment_methods": ["oral narration", "written work"],
                }
                content["teaching_guidance"] = tg
                content["learning_objectives"] = objectives
                content["assessment_criteria"] = ac

            # Build lesson structure
            steps = []
            # Introduction as a "read" step
            if tg.get("introduction"):
                steps.append(
                    {
                        "title": "Introduction",
                        "content": tg["introduction"],
                        "type": "read",
                    }
                )
            # Scaffolding as sequential steps
            for i, scaffold in enumerate(tg.get("scaffolding_sequence", [])):
                steps.append(
                    {
                        "title": f"Step {i + 1}",
                        "content": scaffold,
                        "type": "do",
                    }
                )
            # Socratic questions as "think" steps
            for q in tg.get("socratic_questions", []):
                steps.append(
                    {
                        "title": "Think about this",
                        "content": q,
                        "type": "think",
                    }
                )

            context["lesson"] = {
                "introduction": tg.get("introduction", ""),
                "objectives": objectives,
                "steps": steps,
                "key_questions": tg.get("socratic_questions", []),
                "practice_prompts": (tg.get("practice_activities", []) + ac.get("sample_assessment_prompts", [])),
                "resources_needed": (rg.get("required", []) + rg.get("recommended", [])),
                "real_world_connection": (
                    "; ".join(tg.get("real_world_connections", [])) if tg.get("real_world_connections") else ""
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

            # Surface visual media and reading passages. Passed through
            # unchanged; legacy nodes without these keys yield [].
            context["lesson"]["media"] = content.get("media", [])
            context["reading"]["passages"] = content.get("passages", [])

            # Surface interactive widgets. Passed through unchanged;
            # legacy nodes without the key yield [].
            context["lesson"]["widgets"] = content.get("widgets", [])

            # Surface authored practice_items so PracticeView renders
            # auto-gradeable items instead of degrading to free text.
            practice_items = content.get("practice_items", []) or []
            context["practice"] = {"items": practice_items}

            # Assessment items prefer the dedicated authored
            # assessment_items list (carries rubric and target_concept).
            # AI-generated nodes that only produce practice_items fall
            # back to deriving items from those. "text" maps to
            # "open_response" defensively; None-valued keys are dropped.
            authored_assessment_items = content.get("assessment_items", []) or []
            assessment_items = []
            if authored_assessment_items:
                for ai_item in authored_assessment_items:
                    item = dict(ai_item)
                    item_type = ai_item.get("type", "open_response")
                    item["type"] = "open_response" if item_type == "text" else item_type
                    assessment_items.append({k: v for k, v in item.items() if v is not None})
            else:
                # Fallback: derive from practice_items. Hints and worked
                # explanations are intentionally dropped so assessments
                # do not leak them.
                for pi in practice_items:
                    expected_type = pi.get("expected_type", "open_response")
                    item = {
                        "prompt": pi["prompt"],
                        "type": "open_response" if expected_type == "text" else expected_type,
                        "options": pi.get("options"),
                        "correct_answer": pi.get("correct_answer"),
                    }
                    assessment_items.append({k: v for k, v in item.items() if v is not None})
            context["assessment"]["items"] = assessment_items

            # Resolve the pedagogical philosophy for this node and
            # surface its variant. Shape-agnostic: a native variant is
            # passed through as-is (a legacy one-line string included);
            # when there is none the child keeps the neutral content.
            chosen = curriculum_philosophy
            if curriculum_philosophy == "eclectic":
                chosen = "traditional"
                subject_result = await db.execute(
                    select(Subject.name)
                    .join(LearningMap, LearningMap.subject_id == Subject.id)
                    .where(LearningMap.id == node.learning_map_id)
                )
                subject_name = subject_result.scalar_one_or_none()
                if subject_name:
                    override = subject_philosophies.get(subject_name) or subject_philosophies.get(
                        subject_name.lower().replace(" ", "_")
                    )
                    if isinstance(override, str) and override:
                        chosen = override

            phil_specific = content.get("philosophy_specific", {})
            variant = phil_specific.get(chosen) if isinstance(phil_specific, dict) else None
            context["philosophy"] = {
                "approach": chosen,
                "content": variant or None,
                "is_native": variant is not None,
            }

    return context
