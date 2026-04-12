"""Tests for the DAG Engine — cycle detection, closure, prerequisites."""

import uuid

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningEdge, LearningMap, LearningMapClosure, LearningNode, Subject
from app.models.enums import EdgeRelation, MasteryLevel, NodeType
from app.models.identity import Child, Household
from app.models.state import ChildNodeState
from app.services.dag_engine import (
    add_closure_entries,
    check_prerequisites_met,
    compute_map_state,
    get_prerequisite_node_ids,
    rebuild_closure_for_map,
    would_create_cycle,
)


@pytest_asyncio.fixture
async def dag_household(db_session):
    h = Household(name="DAG Test")
    db_session.add(h)
    await db_session.flush()
    return h


@pytest_asyncio.fixture
async def dag_map(db_session, dag_household):
    s = Subject(household_id=dag_household.id, name="Math")
    db_session.add(s)
    await db_session.flush()
    m = LearningMap(household_id=dag_household.id, subject_id=s.id, name="Map")
    db_session.add(m)
    await db_session.flush()
    return m


@pytest_asyncio.fixture
async def dag_chain(db_session, dag_household, dag_map):
    """Create A -> B -> C chain."""
    nodes = []
    for title in ["A", "B", "C"]:
        n = LearningNode(learning_map_id=dag_map.id, household_id=dag_household.id,
                         node_type=NodeType.concept, title=title)
        db_session.add(n)
        await db_session.flush()
        nodes.append(n)
    # A -> B
    e1 = LearningEdge(learning_map_id=dag_map.id, household_id=dag_household.id,
                       from_node_id=nodes[0].id, to_node_id=nodes[1].id,
                       relation=EdgeRelation.prerequisite)
    db_session.add(e1)
    # B -> C
    e2 = LearningEdge(learning_map_id=dag_map.id, household_id=dag_household.id,
                       from_node_id=nodes[1].id, to_node_id=nodes[2].id,
                       relation=EdgeRelation.prerequisite)
    db_session.add(e2)
    await db_session.flush()
    # Build closure
    await add_closure_entries(db_session, dag_map.id, nodes[0].id, nodes[1].id)
    await add_closure_entries(db_session, dag_map.id, nodes[1].id, nodes[2].id)
    return nodes


@pytest.mark.asyncio
class TestCycleDetection:
    async def test_detects_cycle(self, db_session, dag_map, dag_chain):
        # C -> A would create a cycle
        result = await would_create_cycle(db_session, dag_map.id, dag_chain[2].id, dag_chain[0].id)
        assert result is True

    async def test_allows_valid_edge(self, db_session, dag_map, dag_chain):
        # A -> C is valid (already implied by A->B->C, but direct edge is fine)
        result = await would_create_cycle(db_session, dag_map.id, dag_chain[0].id, dag_chain[2].id)
        assert result is False


@pytest.mark.asyncio
class TestClosure:
    async def test_rebuild_closure(self, db_session, dag_map, dag_chain):
        await rebuild_closure_for_map(db_session, dag_map.id)
        result = await db_session.execute(
            select(LearningMapClosure).where(LearningMapClosure.learning_map_id == dag_map.id)
        )
        entries = result.scalars().all()
        assert len(entries) >= 2  # A->B (depth 1), A->C (depth 2), B->C (depth 1)


@pytest.mark.asyncio
class TestPrerequisites:
    async def test_get_prerequisite_ids(self, db_session, dag_map, dag_chain):
        prereqs = await get_prerequisite_node_ids(db_session, dag_map.id, dag_chain[2].id)
        prereq_ids = set(prereqs)
        assert dag_chain[1].id in prereq_ids  # B is direct prereq of C

    async def test_check_met_all_mastered(self, db_session, dag_household, dag_map, dag_chain):
        child = Child(household_id=dag_household.id, first_name="T")
        db_session.add(child)
        await db_session.flush()
        # Master A and B
        for n in dag_chain[:2]:
            db_session.add(ChildNodeState(child_id=child.id, household_id=dag_household.id,
                                           node_id=n.id, mastery_level=MasteryLevel.mastered))
        await db_session.flush()
        met = await check_prerequisites_met(db_session, child.id, dag_household.id, dag_map.id, dag_chain[2].id)
        assert met is True

    async def test_check_not_met(self, db_session, dag_household, dag_map, dag_chain):
        child = Child(household_id=dag_household.id, first_name="T2")
        db_session.add(child)
        await db_session.flush()
        met = await check_prerequisites_met(db_session, child.id, dag_household.id, dag_map.id, dag_chain[2].id)
        assert met is False
