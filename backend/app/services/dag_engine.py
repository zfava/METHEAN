"""DAG Engine: cycle detection, transitive closure, prerequisite enforcement.

This is the core of METHEAN's curriculum architecture. Every structural
change to a learning map flows through this engine to maintain DAG integrity.
"""

import uuid

from sqlalchemy import and_, delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import (
    LearningEdge,
    LearningMap,
    LearningMapClosure,
    LearningNode,
)
from app.models.enums import EdgeRelation, MasteryLevel
from app.models.state import ChildNodeState


async def would_create_cycle(
    db: AsyncSession,
    learning_map_id: uuid.UUID,
    from_node_id: uuid.UUID,
    to_node_id: uuid.UUID,
) -> bool:
    """Check if adding from_node -> to_node would create a cycle.

    A cycle exists if to_node is already an ancestor of from_node
    (i.e., there's already a path from to_node to from_node).
    Adding from_node -> to_node would then complete the cycle.

    Also catches self-loops (from_node == to_node).
    """
    if from_node_id == to_node_id:
        return True

    # Check if to_node is an ancestor of from_node via the closure table
    result = await db.execute(
        select(LearningMapClosure.id).where(
            LearningMapClosure.learning_map_id == learning_map_id,
            LearningMapClosure.ancestor_id == to_node_id,
            LearningMapClosure.descendant_id == from_node_id,
        ).limit(1)
    )
    return result.scalar_one_or_none() is not None


async def add_closure_entries(
    db: AsyncSession,
    learning_map_id: uuid.UUID,
    from_node_id: uuid.UUID,
    to_node_id: uuid.UUID,
) -> None:
    """Insert transitive closure entries for a new edge from_node -> to_node.

    New reachable pairs:
    1. (from_node, to_node) at depth 1  (the direct edge itself)
    2. (ancestor_of_from, to_node) — every node that can reach from_node
       can now also reach to_node
    3. (from_node, descendant_of_to) — from_node can now reach everything
       to_node could already reach
    4. (ancestor_of_from, descendant_of_to) — cross products of the above
    """
    # 1. Direct edge: from -> to at depth 1
    direct = LearningMapClosure(
        learning_map_id=learning_map_id,
        ancestor_id=from_node_id,
        descendant_id=to_node_id,
        depth=1,
    )
    db.add(direct)

    # 2. All ancestors of from_node can now reach to_node
    ancestors = await db.execute(
        select(LearningMapClosure).where(
            LearningMapClosure.learning_map_id == learning_map_id,
            LearningMapClosure.descendant_id == from_node_id,
        )
    )
    ancestor_rows = ancestors.scalars().all()

    for anc in ancestor_rows:
        db.add(LearningMapClosure(
            learning_map_id=learning_map_id,
            ancestor_id=anc.ancestor_id,
            descendant_id=to_node_id,
            depth=anc.depth + 1,
        ))

    # 3. from_node can now reach all descendants of to_node
    descendants = await db.execute(
        select(LearningMapClosure).where(
            LearningMapClosure.learning_map_id == learning_map_id,
            LearningMapClosure.ancestor_id == to_node_id,
        )
    )
    descendant_rows = descendants.scalars().all()

    for desc in descendant_rows:
        db.add(LearningMapClosure(
            learning_map_id=learning_map_id,
            ancestor_id=from_node_id,
            descendant_id=desc.descendant_id,
            depth=1 + desc.depth,
        ))

    # 4. Cross-product: ancestors of from_node × descendants of to_node
    for anc in ancestor_rows:
        for desc in descendant_rows:
            db.add(LearningMapClosure(
                learning_map_id=learning_map_id,
                ancestor_id=anc.ancestor_id,
                descendant_id=desc.descendant_id,
                depth=anc.depth + 1 + desc.depth,
            ))

    await db.flush()


async def rebuild_closure_for_map(
    db: AsyncSession,
    learning_map_id: uuid.UUID,
) -> None:
    """Full recompute of transitive closure for a map using recursive CTE.

    Called after edge deletion when incremental update is not feasible.
    """
    # Clear existing closure entries for this map
    await db.execute(
        delete(LearningMapClosure).where(
            LearningMapClosure.learning_map_id == learning_map_id
        )
    )
    await db.flush()

    # Use recursive CTE to compute all reachable pairs
    cte_query = text("""
        WITH RECURSIVE reachable AS (
            -- Base case: direct edges
            SELECT
                from_node_id AS ancestor_id,
                to_node_id AS descendant_id,
                1 AS depth
            FROM learning_edges
            WHERE learning_map_id = :map_id

            UNION ALL

            -- Recursive step: extend paths
            SELECT
                r.ancestor_id,
                e.to_node_id AS descendant_id,
                r.depth + 1 AS depth
            FROM reachable r
            JOIN learning_edges e
                ON e.from_node_id = r.descendant_id
                AND e.learning_map_id = :map_id
            WHERE r.depth < 100  -- safety guard against bugs
        )
        SELECT DISTINCT ON (ancestor_id, descendant_id)
            ancestor_id, descendant_id, MIN(depth) as depth
        FROM reachable
        GROUP BY ancestor_id, descendant_id
    """)

    result = await db.execute(cte_query, {"map_id": str(learning_map_id)})
    rows = result.fetchall()

    for row in rows:
        db.add(LearningMapClosure(
            learning_map_id=learning_map_id,
            ancestor_id=row.ancestor_id,
            descendant_id=row.descendant_id,
            depth=row.depth,
        ))

    await db.flush()


async def get_prerequisite_node_ids(
    db: AsyncSession,
    learning_map_id: uuid.UUID,
    node_id: uuid.UUID,
) -> list[uuid.UUID]:
    """Get direct prerequisite node IDs for a given node."""
    result = await db.execute(
        select(LearningEdge.from_node_id).where(
            LearningEdge.learning_map_id == learning_map_id,
            LearningEdge.to_node_id == node_id,
            LearningEdge.relation == EdgeRelation.prerequisite,
        )
    )
    return list(result.scalars().all())


async def check_prerequisites_met(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    learning_map_id: uuid.UUID,
    node_id: uuid.UUID,
) -> bool:
    """Check if all prerequisite nodes for a given node are mastered by the child."""
    prereq_ids = await get_prerequisite_node_ids(db, learning_map_id, node_id)
    if not prereq_ids:
        return True  # No prerequisites means available

    # Check mastery for all prerequisites
    result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
            ChildNodeState.node_id.in_(prereq_ids),
            ChildNodeState.mastery_level == MasteryLevel.mastered,
        )
    )
    mastered_states = result.scalars().all()
    return len(mastered_states) == len(prereq_ids)


async def compute_map_state(
    db: AsyncSession,
    child_id: uuid.UUID,
    household_id: uuid.UUID,
    learning_map_id: uuid.UUID,
) -> list[dict]:
    """Compute the full map state for a child.

    Each node is annotated with:
    - "available": prerequisites met, not yet mastered
    - "blocked": prerequisites not met
    - "mastered": mastery_level == mastered
    - "in_progress": mastery_level in (emerging, developing, proficient) AND prerequisites met
    """
    # Get all active nodes in the map
    nodes_result = await db.execute(
        select(LearningNode).where(
            LearningNode.learning_map_id == learning_map_id,
            LearningNode.household_id == household_id,
            LearningNode.is_active == True,  # noqa: E712
        ).order_by(LearningNode.sort_order)
    )
    nodes = nodes_result.scalars().all()

    if not nodes:
        return []

    node_ids = [n.id for n in nodes]

    # Get all child node states for this map in one query
    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
            ChildNodeState.node_id.in_(node_ids),
        )
    )
    states = {s.node_id: s for s in states_result.scalars().all()}

    # Get all prerequisite edges in this map (only prerequisite type)
    edges_result = await db.execute(
        select(LearningEdge).where(
            LearningEdge.learning_map_id == learning_map_id,
            LearningEdge.relation == EdgeRelation.prerequisite,
        )
    )
    edges = edges_result.scalars().all()

    # Build prerequisite map: node_id -> list of prerequisite node_ids
    prereqs: dict[uuid.UUID, list[uuid.UUID]] = {n.id: [] for n in nodes}
    for edge in edges:
        if edge.to_node_id in prereqs:
            prereqs[edge.to_node_id].append(edge.from_node_id)

    # Build mastered set for fast lookup
    mastered_set = {
        nid for nid, state in states.items()
        if state.mastery_level == MasteryLevel.mastered
    }

    in_progress_levels = {
        MasteryLevel.emerging,
        MasteryLevel.developing,
        MasteryLevel.proficient,
    }

    result = []
    for node in nodes:
        state = states.get(node.id)
        mastery = state.mastery_level if state else MasteryLevel.not_started
        is_unlocked = state.is_unlocked if state else False
        attempts = state.attempts_count if state else 0
        time_spent = state.time_spent_minutes if state else 0

        prereq_ids = prereqs.get(node.id, [])
        all_prereqs_met = all(pid in mastered_set for pid in prereq_ids)

        # Determine status
        if mastery == MasteryLevel.mastered:
            status = "mastered"
        elif is_unlocked or (not prereq_ids):
            # Unlocked via override or no prerequisites
            if mastery in in_progress_levels:
                status = "in_progress"
            else:
                status = "available"
        elif all_prereqs_met:
            if mastery in in_progress_levels:
                status = "in_progress"
            else:
                status = "available"
        else:
            status = "blocked"

        result.append({
            "node_id": node.id,
            "node_type": node.node_type,
            "title": node.title,
            "mastery_level": mastery,
            "status": status,
            "is_unlocked": is_unlocked,
            "prerequisites_met": all_prereqs_met or (not prereq_ids),
            "prerequisite_node_ids": prereq_ids,
            "attempts_count": attempts,
            "time_spent_minutes": time_spent,
        })

    return result


async def increment_map_version(
    db: AsyncSession,
    learning_map_id: uuid.UUID,
) -> int:
    """Increment the version of a learning map on structural change."""
    result = await db.execute(
        select(LearningMap).where(LearningMap.id == learning_map_id)
    )
    lmap = result.scalar_one()
    lmap.version += 1
    await db.flush()
    return lmap.version
