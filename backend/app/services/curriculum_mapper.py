"""Curriculum Mapper service.

Maps existing curriculum materials (Saxon Math, Story of the World, etc.)
into METHEAN's DAG structure so the system can track progress without
replacing what the family already uses.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import CURRICULUM_MAPPER_SYSTEM
from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningMap,
    LearningNode,
    Subject,
)
from app.models.enums import EdgeRelation, GovernanceAction, MasteryLevel
from app.models.governance import GovernanceEvent
from app.models.identity import Child, Household
from app.models.state import ChildNodeState, FSRSCard


async def map_existing_curriculum(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    user_id: uuid.UUID,
    material_name: str,
    material_description: str,
    table_of_contents: str,
    current_position: str,
    subject_area: str,
) -> dict:
    """Map an existing curriculum into METHEAN's DAG structure.

    Returns a proposal dict for parent review.
    """
    # Fetch context
    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child = child_result.scalar_one()

    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household = h_result.scalar_one()
    phil = household.philosophical_profile or {}

    user_prompt = f"""Map this existing curriculum material into a METHEAN learning map.

MATERIAL:
- Name: {material_name}
- Description: {material_description}
- Subject area: {subject_area}

TABLE OF CONTENTS / STRUCTURE:
{table_of_contents}

CHILD'S CURRENT POSITION:
{current_position}

CHILD: {child.first_name}, grade {child.grade_level or 'K'}

Map this into a DAG structure with root, milestone, concept, and skill nodes.
Mark already-completed sections as mastered."""

    ai_result = await call_ai(
        db,
        role=AIRole.curriculum_mapper,
        system_prompt=CURRICULUM_MAPPER_SYSTEM,
        user_prompt=user_prompt,
        household_id=household_id,
        triggered_by=user_id,
        philosophical_profile=phil,
    )

    output = ai_result["output"]

    return {
        "proposal_type": "existing_material",
        "source_material": output.get("source_material", material_name) if isinstance(output, dict) else material_name,
        "material_name": material_name,
        "subject_area": subject_area,
        "nodes": output.get("nodes", []) if isinstance(output, dict) else [],
        "edges": output.get("edges", []) if isinstance(output, dict) else [],
        "nodes_already_mastered": output.get("nodes_already_mastered", []) if isinstance(output, dict) else [],
        "current_position": output.get("current_position", {}) if isinstance(output, dict) else {},
        "ai_run_id": str(ai_result["ai_run_id"]),
        "is_mock": ai_result["is_mock"],
    }


async def apply_curriculum_mapping(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    user_id: uuid.UUID,
    proposal: dict,
) -> dict:
    """Apply an approved curriculum mapping: create map, nodes, edges, mastery state."""

    # Create subject
    subj = Subject(
        household_id=household_id,
        name=proposal.get("subject_area", proposal.get("material_name", "Mapped Curriculum")),
    )
    db.add(subj)
    await db.flush()

    # Create map
    lmap = LearningMap(
        household_id=household_id,
        subject_id=subj.id,
        name=proposal.get("material_name", "Mapped Curriculum"),
        description=f"Mapped from: {proposal.get('source_material', '')}",
    )
    db.add(lmap)
    await db.flush()

    # Create nodes
    ref_to_id: dict[str, uuid.UUID] = {}
    for node_data in proposal.get("nodes", []):
        node = LearningNode(
            learning_map_id=lmap.id,
            household_id=household_id,
            node_type=node_data.get("node_type", "concept"),
            title=node_data.get("title", "Untitled"),
            description=node_data.get("description", ""),
            estimated_minutes=node_data.get("estimated_minutes"),
            sort_order=node_data.get("sort_order", 0),
        )
        db.add(node)
        await db.flush()
        ref = node_data.get("ref", str(node.id))
        ref_to_id[ref] = node.id

    # Create edges
    for edge_data in proposal.get("edges", []):
        from_ref = edge_data.get("from_ref")
        to_ref = edge_data.get("to_ref")
        if from_ref in ref_to_id and to_ref in ref_to_id:
            db.add(LearningEdge(
                learning_map_id=lmap.id,
                household_id=household_id,
                from_node_id=ref_to_id[from_ref],
                to_node_id=ref_to_id[to_ref],
                relation=EdgeRelation.prerequisite,
            ))
    await db.flush()

    # Enroll child
    db.add(ChildMapEnrollment(
        child_id=child_id,
        household_id=household_id,
        learning_map_id=lmap.id,
    ))

    # Set mastery state for already-completed nodes
    mastered_refs = proposal.get("nodes_already_mastered", [])
    mastered_count = 0
    for ref in mastered_refs:
        node_id = ref_to_id.get(ref)
        if node_id:
            db.add(ChildNodeState(
                child_id=child_id,
                household_id=household_id,
                node_id=node_id,
                mastery_level=MasteryLevel.mastered,
                is_unlocked=True,
                attempts_count=1,
            ))
            db.add(FSRSCard(
                child_id=child_id,
                household_id=household_id,
                node_id=node_id,
                stability=10.0,
                difficulty=2.5,
                reps=1,
                state=2,
                last_review=datetime.now(UTC),
                due=datetime.now(UTC),
            ))
            mastered_count += 1

    # Set current position
    current = proposal.get("current_position", {})
    current_ref = current.get("ref")
    if current_ref and current_ref in ref_to_id:
        db.add(ChildNodeState(
            child_id=child_id,
            household_id=household_id,
            node_id=ref_to_id[current_ref],
            mastery_level=MasteryLevel.developing,
            is_unlocked=True,
        ))

    # Log governance event
    db.add(GovernanceEvent(
        household_id=household_id,
        user_id=user_id,
        action=GovernanceAction.approve,
        target_type="curriculum_mapping",
        target_id=lmap.id,
        reason=f"Mapped '{proposal.get('material_name', '')}' into METHEAN",
    ))
    await db.flush()

    # Queue background enrichment
    try:
        from app.tasks.worker import enrich_map_task
        enrich_map_task.delay(str(lmap.id), str(household_id))
    except Exception:
        pass

    return {
        "learning_map_id": str(lmap.id),
        "subject_id": str(subj.id),
        "nodes_created": len(ref_to_id),
        "nodes_mastered": mastered_count,
        "current_position_node_id": str(ref_to_id[current_ref]) if current_ref and current_ref in ref_to_id else None,
    }
