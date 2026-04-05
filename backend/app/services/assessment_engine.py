"""Assessment engine: parent-driven assessment, transcripts, portfolio export."""

import uuid
from datetime import UTC, date, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessment import Assessment, PortfolioEntry
from app.models.curriculum import LearningNode, Subject
from app.models.enums import GovernanceAction, MasteryLevel, StateEventType
from app.models.governance import GovernanceEvent
from app.models.state import ChildNodeState, StateEvent
from app.services.state_engine import get_or_create_node_state, process_review


MASTERY_MAP = {
    "mastered": MasteryLevel.mastered,
    "proficient": MasteryLevel.proficient,
    "developing": MasteryLevel.developing,
    "emerging": MasteryLevel.emerging,
    "needs_review": MasteryLevel.not_started,
}

GRADE_MAP = {
    MasteryLevel.mastered: "A",
    MasteryLevel.proficient: "B",
    MasteryLevel.developing: "C",
    MasteryLevel.emerging: "D",
    MasteryLevel.not_started: "I",  # Incomplete
}


async def record_assessment(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    node_id: uuid.UUID | None,
    assessment_data: dict,
    user_id: uuid.UUID,
) -> Assessment:
    """Record a parent assessment and optionally update node mastery."""

    assessment = Assessment(
        household_id=household_id,
        child_id=child_id,
        node_id=node_id,
        assessed_by=user_id,
        assessment_type=assessment_data.get("assessment_type", "parent_observation"),
        title=assessment_data.get("title", "Assessment"),
        description=assessment_data.get("description"),
        qualitative_notes=assessment_data.get("qualitative_notes"),
        rubric_scores=assessment_data.get("rubric_scores"),
        mastery_judgment=assessment_data.get("mastery_judgment"),
        confidence_override=assessment_data.get("confidence_override"),
        artifact_ids=assessment_data.get("artifact_ids", []),
        subject=assessment_data.get("subject"),
    )
    db.add(assessment)
    await db.flush()

    # If mastery_judgment is provided and a node is linked, update state
    judgment = assessment_data.get("mastery_judgment")
    if judgment and node_id and judgment in MASTERY_MAP:
        target_mastery = MASTERY_MAP[judgment]
        state = await get_or_create_node_state(db, child_id, household_id, node_id)
        prev = state.mastery_level

        if prev != target_mastery:
            from app.services.state_engine import emit_state_event
            state.mastery_level = target_mastery
            state.attempts_count += 1
            state.last_activity_at = datetime.now(UTC)

            await emit_state_event(
                db, child_id, household_id, node_id,
                event_type=StateEventType.mastery_change,
                from_state=prev.value if hasattr(prev, "value") else str(prev),
                to_state=target_mastery.value,
                trigger="parent_assessment",
                metadata={
                    "assessment_id": str(assessment.id),
                    "assessment_type": assessment.assessment_type,
                    "qualitative_notes": assessment.qualitative_notes,
                },
                created_by=user_id,
            )

            # Log governance event for mastery override
            db.add(GovernanceEvent(
                household_id=household_id,
                user_id=user_id,
                action=GovernanceAction.modify,
                target_type="mastery_override",
                target_id=node_id,
                reason=f"Parent assessment: {prev.value if hasattr(prev, 'value') else prev} -> {target_mastery.value}",
                metadata_={"assessment_id": str(assessment.id)},
            ))

    # If confidence_override is provided, run through FSRS
    confidence = assessment_data.get("confidence_override")
    if confidence is not None and node_id:
        await process_review(
            db, child_id, household_id, node_id,
            confidence=confidence, created_by=user_id,
        )

    await db.flush()
    return assessment


async def generate_transcript(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    year: int | None = None,
) -> dict:
    """Generate an unofficial transcript from mastery data."""

    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
        )
    )
    states = states_result.scalars().all()

    # Get node titles and subjects
    node_ids = [s.node_id for s in states]
    nodes_map: dict[uuid.UUID, LearningNode] = {}
    if node_ids:
        nodes_result = await db.execute(select(LearningNode).where(LearningNode.id.in_(node_ids)))
        nodes_map = {n.id: n for n in nodes_result.scalars().all()}

    # Count assessments per child
    assess_count = await db.execute(
        select(func.count(Assessment.id)).where(
            Assessment.child_id == child_id,
            Assessment.household_id == household_id,
        )
    )

    # Group by subject (via map -> subject)
    subjects: dict[str, dict] = {}
    for state in states:
        node = nodes_map.get(state.node_id)
        subj_name = "General"
        if node:
            # Try to get subject name from the map
            from app.models.curriculum import LearningMap
            map_result = await db.execute(
                select(LearningMap).where(LearningMap.id == node.learning_map_id)
            )
            lmap = map_result.scalar_one_or_none()
            if lmap:
                s_result = await db.execute(select(Subject).where(Subject.id == lmap.subject_id))
                subj = s_result.scalar_one_or_none()
                if subj:
                    subj_name = subj.name

        if subj_name not in subjects:
            subjects[subj_name] = {
                "mastered": 0, "total": 0, "hours": 0.0, "assessments": 0,
                "highest_mastery": MasteryLevel.not_started,
            }
        entry = subjects[subj_name]
        entry["total"] += 1
        entry["hours"] += (state.time_spent_minutes or 0) / 60
        if state.mastery_level == MasteryLevel.mastered:
            entry["mastered"] += 1
        # Track highest mastery for grade assignment
        levels = [MasteryLevel.not_started, MasteryLevel.emerging, MasteryLevel.developing,
                  MasteryLevel.proficient, MasteryLevel.mastered]
        if levels.index(state.mastery_level) > levels.index(entry["highest_mastery"]):
            entry["highest_mastery"] = state.mastery_level

    rows = []
    for name, data in sorted(subjects.items()):
        grade = GRADE_MAP.get(data["highest_mastery"], "I")
        rows.append({
            "subject": name,
            "grade": grade,
            "nodes_mastered": data["mastered"],
            "nodes_total": data["total"],
            "hours_logged": round(data["hours"], 1),
        })

    gpa_map = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "I": 0.0}
    grades = [gpa_map.get(r["grade"], 0) for r in rows]
    gpa = round(sum(grades) / len(grades), 2) if grades else 0.0

    return {
        "child_id": str(child_id),
        "year": year or datetime.now().year,
        "subjects": rows,
        "gpa": gpa,
        "total_assessments": assess_count.scalar() or 0,
        "generated_at": datetime.now(UTC).isoformat(),
    }


async def generate_portfolio_export(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    period_start: date,
    period_end: date,
) -> dict:
    """Generate a portfolio summary organized by subject."""

    entries_result = await db.execute(
        select(PortfolioEntry).where(
            PortfolioEntry.child_id == child_id,
            PortfolioEntry.household_id == household_id,
        ).order_by(PortfolioEntry.date_completed.desc())
    )
    entries = entries_result.scalars().all()

    by_subject: dict[str, list] = {}
    for e in entries:
        subj = e.subject or "General"
        by_subject.setdefault(subj, []).append({
            "title": e.title,
            "type": e.entry_type,
            "date": e.date_completed.isoformat() if e.date_completed else None,
            "notes": e.parent_notes,
            "tags": e.tags or [],
        })

    return {
        "child_id": str(child_id),
        "period": {"start": period_start.isoformat(), "end": period_end.isoformat()},
        "subjects": by_subject,
        "total_entries": len(entries),
        "generated_at": datetime.now(UTC).isoformat(),
    }
