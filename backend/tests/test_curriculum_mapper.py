"""Tests for curriculum mapper (mapping existing materials into METHEAN).

Covers:
- Mapping creates a proposal with nodes and edges
- Applying a mapping creates the map with mastered nodes
- Current position is set correctly
"""

import uuid

import pytest
from sqlalchemy import select

from app.models.curriculum import LearningMap, LearningNode
from app.models.enums import MasteryLevel
from app.models.state import ChildNodeState, FSRSCard


class TestMapExistingCurriculum:

    @pytest.mark.asyncio
    async def test_map_existing_creates_proposal(
        self, auth_client, db_session, household, child, user,
    ):
        resp = await auth_client.post(
            f"/api/v1/children/{child.id}/curriculum/map-existing",
            json={
                "material_name": "Saxon Math 5/4",
                "material_description": "Traditional math curriculum for 4th-5th grade",
                "table_of_contents": "Lesson 1: Addition Review\nLesson 2: Place Value\nLesson 3: Subtraction",
                "current_position": "We're on Lesson 15",
                "subject_area": "Mathematics",
            },
        )
        assert resp.status_code == 201, f"Map existing failed: {resp.text}"
        data = resp.json()
        assert data["proposal_type"] == "existing_material"
        assert data["material_name"] == "Saxon Math 5/4"
        assert len(data["nodes"]) > 0
        assert len(data["edges"]) > 0
        assert data["ai_run_id"] is not None


class TestApplyMapping:

    @pytest.mark.asyncio
    async def test_apply_sets_mastered_nodes(
        self, auth_client, db_session, household, child, user,
    ):
        """When applying a mapping, already-mastered nodes get ChildNodeState + FSRSCard."""
        from app.services.curriculum_mapper import apply_curriculum_mapping

        proposal = {
            "material_name": "Test Curriculum",
            "source_material": "Test",
            "subject_area": "Test Subject",
            "nodes": [
                {"ref": "root", "node_type": "root", "title": "Root", "sort_order": 0},
                {"ref": "ch1", "node_type": "milestone", "title": "Chapter 1", "sort_order": 1},
                {"ref": "ch2", "node_type": "milestone", "title": "Chapter 2", "sort_order": 2},
                {"ref": "ch3", "node_type": "milestone", "title": "Chapter 3", "sort_order": 3},
            ],
            "edges": [
                {"from_ref": "root", "to_ref": "ch1"},
                {"from_ref": "ch1", "to_ref": "ch2"},
                {"from_ref": "ch2", "to_ref": "ch3"},
            ],
            "nodes_already_mastered": ["root", "ch1"],
            "current_position": {"ref": "ch2", "status": "in_progress"},
        }

        result = await apply_curriculum_mapping(
            db_session, household.id, child.id, user.id, proposal,
        )

        assert result["nodes_created"] == 4
        assert result["nodes_mastered"] == 2
        assert result["current_position_node_id"] is not None

        # Verify mastered states
        states = await db_session.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child.id,
                ChildNodeState.mastery_level == MasteryLevel.mastered,
            )
        )
        mastered = states.scalars().all()
        assert len(mastered) == 2

        # Verify FSRS cards created for mastered nodes
        cards = await db_session.execute(
            select(FSRSCard).where(FSRSCard.child_id == child.id)
        )
        assert len(cards.scalars().all()) == 2

    @pytest.mark.asyncio
    async def test_current_position_set_to_developing(
        self, auth_client, db_session, household, child, user,
    ):
        from app.services.curriculum_mapper import apply_curriculum_mapping

        proposal = {
            "material_name": "Position Test",
            "subject_area": "Test",
            "nodes": [
                {"ref": "a", "node_type": "root", "title": "A", "sort_order": 0},
                {"ref": "b", "node_type": "concept", "title": "B", "sort_order": 1},
            ],
            "edges": [{"from_ref": "a", "to_ref": "b"}],
            "nodes_already_mastered": ["a"],
            "current_position": {"ref": "b", "status": "in_progress"},
        }

        result = await apply_curriculum_mapping(
            db_session, household.id, child.id, user.id, proposal,
        )

        # Current position node should be developing
        current_id = uuid.UUID(result["current_position_node_id"])
        state = await db_session.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child.id,
                ChildNodeState.node_id == current_id,
            )
        )
        node_state = state.scalar_one()
        assert node_state.mastery_level == MasteryLevel.developing
