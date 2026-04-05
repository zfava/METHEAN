"""Content enrichment engine.

Generates rich teaching/assessment/resource guidance for learning nodes
through the Content Architect AI role. Stores results in the node's
content JSONB field.
"""

import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import CONTENT_ARCHITECT_SYSTEM
from app.models.curriculum import LearningNode
from app.models.identity import Household
from app.services.node_content import is_enriched


async def enrich_nodes(
    db: AsyncSession,
    household_id: uuid.UUID,
    learning_map_id: uuid.UUID,
    node_ids: list[uuid.UUID] | None = None,
    user_id: uuid.UUID | None = None,
) -> dict:
    """Generate rich content guidance for unenriched nodes in a map."""

    # Fetch nodes
    query = select(LearningNode).where(
        LearningNode.learning_map_id == learning_map_id,
        LearningNode.household_id == household_id,
        LearningNode.is_active == True,  # noqa: E712
    )
    if node_ids:
        query = query.where(LearningNode.id.in_(node_ids))
    result = await db.execute(query)
    all_nodes = result.scalars().all()

    # Filter to unenriched nodes
    to_enrich = [n for n in all_nodes if not is_enriched(n.content)]
    if not to_enrich:
        return {"enriched": 0, "skipped": len(all_nodes), "ai_run_id": None}

    # Fetch philosophical profile
    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household = h_result.scalar_one_or_none()
    phil = household.philosophical_profile if household else None

    # Enrich each node (could batch, but individual calls are simpler and
    # produce better quality per node)
    enriched_count = 0
    last_ai_run_id = None

    for node in to_enrich:
        ntype = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
        user_prompt = f"""Generate rich content guidance for this learning node.

Node Title: {node.title}
Node Type: {ntype}
Description: {node.description or 'No description provided'}
Estimated Minutes: {node.estimated_minutes or 'Not specified'}

Generate complete teaching guidance, assessment criteria, resource guidance, accommodations, and time estimates."""

        ai_result = await call_ai(
            db,
            role=AIRole.content_architect,
            system_prompt=CONTENT_ARCHITECT_SYSTEM,
            user_prompt=user_prompt,
            household_id=household_id,
            triggered_by=user_id,
            philosophical_profile=phil,
        )

        output = ai_result["output"]
        if isinstance(output, dict) and output.get("learning_objectives"):
            node.content = output
            enriched_count += 1
            last_ai_run_id = ai_result["ai_run_id"]

    await db.flush()

    return {
        "enriched": enriched_count,
        "skipped": len(all_nodes) - enriched_count,
        "ai_run_id": str(last_ai_run_id) if last_ai_run_id else None,
    }


async def enrich_single_node(
    db: AsyncSession,
    node_id: uuid.UUID,
    household_id: uuid.UUID,
    user_id: uuid.UUID | None = None,
) -> dict:
    """Enrich a single node on demand."""
    result = await db.execute(
        select(LearningNode).where(
            LearningNode.id == node_id,
            LearningNode.household_id == household_id,
        )
    )
    node = result.scalar_one_or_none()
    if not node:
        raise ValueError("Node not found")

    h_result = await db.execute(select(Household).where(Household.id == household_id))
    household = h_result.scalar_one_or_none()
    phil = household.philosophical_profile if household else None

    ntype = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
    user_prompt = f"""Generate rich content guidance for this learning node.

Node Title: {node.title}
Node Type: {ntype}
Description: {node.description or 'No description provided'}
Estimated Minutes: {node.estimated_minutes or 'Not specified'}

Generate complete teaching guidance, assessment criteria, resource guidance, accommodations, and time estimates."""

    ai_result = await call_ai(
        db,
        role=AIRole.content_architect,
        system_prompt=CONTENT_ARCHITECT_SYSTEM,
        user_prompt=user_prompt,
        household_id=household_id,
        triggered_by=user_id,
        philosophical_profile=phil,
    )

    output = ai_result["output"]
    if isinstance(output, dict) and output.get("learning_objectives"):
        node.content = output
        await db.flush()

    return {
        "node_id": str(node_id),
        "content": node.content,
        "ai_run_id": str(ai_result["ai_run_id"]),
    }
