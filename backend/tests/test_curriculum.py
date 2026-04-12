"""Comprehensive tests for Curriculum Architecture (System 1).

Tests cover:
- Cycle detection in DAG
- Transitive closure maintenance
- Prerequisite blocking / availability
- Parent override with GovernanceEvent logging
- Template deep copy
- Map versioning
- Full API endpoint coverage
"""

import uuid

import pytest
from sqlalchemy import select

from app.models.curriculum import (
    ChildMapEnrollment,
    LearningEdge,
    LearningMap,
    LearningMapClosure,
    LearningNode,
)
from app.models.enums import (
    EdgeRelation,
    GovernanceAction,
    MasteryLevel,
    NodeType,
    StateEventType,
)
from app.models.governance import GovernanceEvent
from app.models.state import ChildNodeState, StateEvent
from app.services.dag_engine import (
    add_closure_entries,
    check_prerequisites_met,
    compute_map_state,
    increment_map_version,
    rebuild_closure_for_map,
    would_create_cycle,
)


# ── Helper to create nodes quickly ──


async def _make_node(db, lmap, household, title, node_type=NodeType.concept):
    node = LearningNode(
        learning_map_id=lmap.id,
        household_id=household.id,
        node_type=node_type,
        title=title,
    )
    db.add(node)
    await db.flush()
    return node


async def _make_edge(db, lmap, household, from_node, to_node):
    edge = LearningEdge(
        learning_map_id=lmap.id,
        household_id=household.id,
        from_node_id=from_node.id,
        to_node_id=to_node.id,
        relation=EdgeRelation.prerequisite,
    )
    db.add(edge)
    await db.flush()
    await add_closure_entries(db, lmap.id, from_node.id, to_node.id)
    return edge


# ══════════════════════════════════════════════════
# DAG Engine Unit Tests
# ══════════════════════════════════════════════════


class TestCycleDetection:
    """Test that adding an edge that would create a cycle is rejected."""

    @pytest.mark.asyncio
    async def test_self_loop_detected(self, db_session, household, learning_map):
        a = await _make_node(db_session, learning_map, household, "A")
        assert await would_create_cycle(db_session, learning_map.id, a.id, a.id) is True

    @pytest.mark.asyncio
    async def test_direct_cycle_detected(self, db_session, household, learning_map):
        """A -> B, then B -> A should be a cycle."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        await _make_edge(db_session, learning_map, household, a, b)

        assert await would_create_cycle(db_session, learning_map.id, b.id, a.id) is True

    @pytest.mark.asyncio
    async def test_transitive_cycle_detected(self, db_session, household, learning_map):
        """A -> B -> C, then C -> A should be a cycle."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        c = await _make_node(db_session, learning_map, household, "C")

        await _make_edge(db_session, learning_map, household, a, b)
        await _make_edge(db_session, learning_map, household, b, c)

        assert await would_create_cycle(db_session, learning_map.id, c.id, a.id) is True

    @pytest.mark.asyncio
    async def test_valid_edge_not_flagged_as_cycle(self, db_session, household, learning_map):
        """A -> B -> C, adding A -> C is valid (not a cycle)."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        c = await _make_node(db_session, learning_map, household, "C")

        await _make_edge(db_session, learning_map, household, a, b)
        await _make_edge(db_session, learning_map, household, b, c)

        # A -> C is valid (shortcut, not a cycle)
        assert await would_create_cycle(db_session, learning_map.id, a.id, c.id) is False

    @pytest.mark.asyncio
    async def test_unrelated_nodes_no_cycle(self, db_session, household, learning_map):
        """Two unrelated nodes: no cycle."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")

        assert await would_create_cycle(db_session, learning_map.id, a.id, b.id) is False


class TestTransitiveClosure:
    """Test that the closure table is maintained correctly."""

    @pytest.mark.asyncio
    async def test_direct_edge_creates_closure(self, db_session, household, learning_map):
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        await _make_edge(db_session, learning_map, household, a, b)

        result = await db_session.execute(
            select(LearningMapClosure).where(
                LearningMapClosure.learning_map_id == learning_map.id,
                LearningMapClosure.ancestor_id == a.id,
                LearningMapClosure.descendant_id == b.id,
            )
        )
        closure = result.scalar_one()
        assert closure.depth == 1

    @pytest.mark.asyncio
    async def test_transitive_closure_depth(self, db_session, household, learning_map):
        """A -> B -> C should create closure entry (A, C, depth=2)."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        c = await _make_node(db_session, learning_map, household, "C")

        await _make_edge(db_session, learning_map, household, a, b)
        await _make_edge(db_session, learning_map, household, b, c)

        result = await db_session.execute(
            select(LearningMapClosure).where(
                LearningMapClosure.learning_map_id == learning_map.id,
                LearningMapClosure.ancestor_id == a.id,
                LearningMapClosure.descendant_id == c.id,
            )
        )
        closure = result.scalar_one()
        assert closure.depth == 2

    @pytest.mark.asyncio
    async def test_rebuild_closure(self, db_session, household, learning_map):
        """Rebuild closure after edge deletion."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        c = await _make_node(db_session, learning_map, household, "C")

        await _make_edge(db_session, learning_map, household, a, b)
        edge_bc = await _make_edge(db_session, learning_map, household, b, c)

        # Remove B -> C edge
        await db_session.delete(edge_bc)
        await db_session.flush()

        # Rebuild
        await rebuild_closure_for_map(db_session, learning_map.id)

        # A -> C should no longer exist in closure
        result = await db_session.execute(
            select(LearningMapClosure).where(
                LearningMapClosure.learning_map_id == learning_map.id,
                LearningMapClosure.ancestor_id == a.id,
                LearningMapClosure.descendant_id == c.id,
            )
        )
        assert result.scalar_one_or_none() is None

        # A -> B should still exist
        result2 = await db_session.execute(
            select(LearningMapClosure).where(
                LearningMapClosure.learning_map_id == learning_map.id,
                LearningMapClosure.ancestor_id == a.id,
                LearningMapClosure.descendant_id == b.id,
            )
        )
        assert result2.scalar_one() is not None


class TestPrerequisiteEnforcement:
    """Test prerequisite checking and map state computation."""

    @pytest.mark.asyncio
    async def test_no_prerequisites_means_available(
        self, db_session, household, learning_map, child,
    ):
        a = await _make_node(db_session, learning_map, household, "A")
        met = await check_prerequisites_met(
            db_session, child.id, household.id, learning_map.id, a.id
        )
        assert met is True

    @pytest.mark.asyncio
    async def test_unmastered_prereq_blocks(
        self, db_session, household, learning_map, child,
    ):
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        await _make_edge(db_session, learning_map, household, a, b)

        # B requires A, but A is not mastered
        met = await check_prerequisites_met(
            db_session, child.id, household.id, learning_map.id, b.id
        )
        assert met is False

    @pytest.mark.asyncio
    async def test_mastered_prereq_unlocks(
        self, db_session, household, learning_map, child,
    ):
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        await _make_edge(db_session, learning_map, household, a, b)

        # Master node A
        state = ChildNodeState(
            child_id=child.id,
            household_id=household.id,
            node_id=a.id,
            mastery_level=MasteryLevel.mastered,
        )
        db_session.add(state)
        await db_session.flush()

        met = await check_prerequisites_met(
            db_session, child.id, household.id, learning_map.id, b.id
        )
        assert met is True

    @pytest.mark.asyncio
    async def test_compute_map_state_blocked_and_available(
        self, db_session, household, learning_map, child,
    ):
        """A -> B -> C: A is available, B and C are blocked."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        c = await _make_node(db_session, learning_map, household, "C")

        await _make_edge(db_session, learning_map, household, a, b)
        await _make_edge(db_session, learning_map, household, b, c)

        states = await compute_map_state(
            db_session, child.id, household.id, learning_map.id
        )

        state_map = {s["title"]: s["status"] for s in states}
        assert state_map["A"] == "available"
        assert state_map["B"] == "blocked"
        assert state_map["C"] == "blocked"

    @pytest.mark.asyncio
    async def test_compute_map_state_mastered_unlocks_next(
        self, db_session, household, learning_map, child,
    ):
        """A -> B: After mastering A, B becomes available."""
        a = await _make_node(db_session, learning_map, household, "A")
        b = await _make_node(db_session, learning_map, household, "B")
        await _make_edge(db_session, learning_map, household, a, b)

        # Master A
        db_session.add(ChildNodeState(
            child_id=child.id, household_id=household.id,
            node_id=a.id, mastery_level=MasteryLevel.mastered,
        ))
        await db_session.flush()

        states = await compute_map_state(
            db_session, child.id, household.id, learning_map.id
        )
        state_map = {s["title"]: s["status"] for s in states}
        assert state_map["A"] == "mastered"
        assert state_map["B"] == "available"

    @pytest.mark.asyncio
    async def test_in_progress_status(
        self, db_session, household, learning_map, child,
    ):
        """Node with no prereqs and emerging mastery shows in_progress."""
        a = await _make_node(db_session, learning_map, household, "A")
        db_session.add(ChildNodeState(
            child_id=child.id, household_id=household.id,
            node_id=a.id, mastery_level=MasteryLevel.emerging,
        ))
        await db_session.flush()

        states = await compute_map_state(
            db_session, child.id, household.id, learning_map.id
        )
        assert states[0]["status"] == "in_progress"


class TestMapVersioning:
    """Test that version increments on structural changes."""

    @pytest.mark.asyncio
    async def test_version_increments(self, db_session, household, learning_map):
        assert learning_map.version == 1
        new_version = await increment_map_version(db_session, learning_map.id)
        assert new_version == 2


# ══════════════════════════════════════════════════
# API Integration Tests
# ══════════════════════════════════════════════════


class TestLearningMapAPI:

    @pytest.mark.asyncio
    async def test_create_and_list_maps(self, auth_client, db_session, household, subject):
        # Create
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id),
            "name": "Test Map",
            "description": "A test learning map",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Test Map"
        assert data["version"] == 1
        map_id = data["id"]

        # List
        resp2 = await auth_client.get("/api/v1/learning-maps")
        assert resp2.status_code == 200
        maps = resp2.json()["items"]
        assert any(m["id"] == map_id for m in maps)

    @pytest.mark.asyncio
    async def test_get_map_detail(self, auth_client, db_session, household, subject):
        # Create map
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Detail Map",
        })
        map_id = resp.json()["id"]

        # Add node
        resp2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "Node A",
        })
        assert resp2.status_code == 201

        # Get detail
        resp3 = await auth_client.get(f"/api/v1/learning-maps/{map_id}")
        assert resp3.status_code == 200
        detail = resp3.json()
        assert len(detail["nodes"]) == 1
        assert detail["nodes"][0]["title"] == "Node A"

    @pytest.mark.asyncio
    async def test_update_map(self, auth_client, db_session, household, subject):
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Old Name",
        })
        map_id = resp.json()["id"]

        resp2 = await auth_client.put(f"/api/v1/learning-maps/{map_id}", json={
            "name": "New Name", "is_published": True,
        })
        assert resp2.status_code == 200
        assert resp2.json()["name"] == "New Name"
        assert resp2.json()["is_published"] is True


class TestNodeAPI:

    @pytest.mark.asyncio
    async def test_create_update_delete_node(self, auth_client, db_session, household, subject):
        # Create map
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Node Test Map",
        })
        map_id = resp.json()["id"]

        # Create node
        resp2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "skill", "title": "Addition", "estimated_minutes": 30,
        })
        assert resp2.status_code == 201
        node_id = resp2.json()["id"]

        # Update node
        resp3 = await auth_client.put(
            f"/api/v1/learning-maps/{map_id}/nodes/{node_id}",
            json={"title": "Advanced Addition"},
        )
        assert resp3.status_code == 200
        assert resp3.json()["title"] == "Advanced Addition"

        # Delete node (soft delete)
        resp4 = await auth_client.delete(
            f"/api/v1/learning-maps/{map_id}/nodes/{node_id}"
        )
        assert resp4.status_code == 204

    @pytest.mark.asyncio
    async def test_node_creation_increments_version(
        self, auth_client, db_session, household, subject,
    ):
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Version Test",
        })
        map_id = resp.json()["id"]
        assert resp.json()["version"] == 1

        # Add node -> version should increment
        await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "V Node",
        })

        resp2 = await auth_client.get(f"/api/v1/learning-maps/{map_id}")
        assert resp2.json()["version"] == 2


class TestEdgeAPI:

    @pytest.mark.asyncio
    async def test_create_edge(self, auth_client, db_session, household, subject):
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Edge Test",
        })
        map_id = resp.json()["id"]

        # Create two nodes
        r1 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "A",
        })
        r2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "B",
        })
        a_id, b_id = r1.json()["id"], r2.json()["id"]

        resp2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": a_id, "to_node_id": b_id,
        })
        assert resp2.status_code == 201
        assert resp2.json()["from_node_id"] == a_id
        assert resp2.json()["to_node_id"] == b_id

    @pytest.mark.asyncio
    async def test_cycle_detection_409(self, auth_client, db_session, household, subject):
        """A -> B -> C, then C -> A should return 409."""
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Cycle Test",
        })
        map_id = resp.json()["id"]

        nodes = {}
        for name in ["A", "B", "C"]:
            r = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
                "node_type": "concept", "title": name,
            })
            nodes[name] = r.json()["id"]

        # A -> B
        await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": nodes["A"], "to_node_id": nodes["B"],
        })
        # B -> C
        await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": nodes["B"], "to_node_id": nodes["C"],
        })
        # C -> A should fail with 409
        resp_cycle = await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": nodes["C"], "to_node_id": nodes["A"],
        })
        assert resp_cycle.status_code == 409
        assert "cycle" in resp_cycle.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_duplicate_edge_409(self, auth_client, db_session, household, subject):
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Dup Edge Test",
        })
        map_id = resp.json()["id"]

        r1 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "X",
        })
        r2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "Y",
        })

        edge_body = {
            "from_node_id": r1.json()["id"], "to_node_id": r2.json()["id"],
        }
        await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json=edge_body)
        resp2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json=edge_body)
        assert resp2.status_code == 409

    @pytest.mark.asyncio
    async def test_delete_edge(self, auth_client, db_session, household, subject):
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Del Edge Test",
        })
        map_id = resp.json()["id"]

        r1 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "P",
        })
        r2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "Q",
        })

        edge_resp = await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": r1.json()["id"], "to_node_id": r2.json()["id"],
        })
        edge_id = edge_resp.json()["id"]

        del_resp = await auth_client.delete(
            f"/api/v1/learning-maps/{map_id}/edges/{edge_id}"
        )
        assert del_resp.status_code == 204


class TestChildMapState:

    @pytest.mark.asyncio
    async def test_enrollment_and_map_state(
        self, auth_client, db_session, household, subject, child,
    ):
        # Create map with A -> B -> C
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "State Test",
        })
        map_id = resp.json()["id"]

        nodes = {}
        for name in ["A", "B", "C"]:
            r = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
                "node_type": "skill", "title": name,
            })
            nodes[name] = r.json()["id"]

        await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": nodes["A"], "to_node_id": nodes["B"],
        })
        await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": nodes["B"], "to_node_id": nodes["C"],
        })

        # Enroll child
        enroll_resp = await auth_client.post(
            f"/api/v1/children/{child.id}/enrollments",
            json={"learning_map_id": map_id},
        )
        assert enroll_resp.status_code == 201
        assert enroll_resp.json()["enrolled_at_version"] >= 1

        # Get map state
        state_resp = await auth_client.get(
            f"/api/v1/children/{child.id}/map-state/{map_id}"
        )
        assert state_resp.status_code == 200
        data = state_resp.json()
        assert data["enrolled"] is True

        node_status = {n["title"]: n["status"] for n in data["nodes"]}
        assert node_status["A"] == "available"
        assert node_status["B"] == "blocked"
        assert node_status["C"] == "blocked"

    @pytest.mark.asyncio
    async def test_duplicate_enrollment_409(
        self, auth_client, db_session, household, subject, child,
    ):
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Dup Enroll",
        })
        map_id = resp.json()["id"]

        await auth_client.post(
            f"/api/v1/children/{child.id}/enrollments",
            json={"learning_map_id": map_id},
        )
        resp2 = await auth_client.post(
            f"/api/v1/children/{child.id}/enrollments",
            json={"learning_map_id": map_id},
        )
        assert resp2.status_code == 409


class TestParentOverride:

    @pytest.mark.asyncio
    async def test_override_creates_governance_event(
        self, auth_client, db_session, household, subject, child, user,
    ):
        # Create map with A -> B
        resp = await auth_client.post("/api/v1/learning-maps", json={
            "subject_id": str(subject.id), "name": "Override Test",
        })
        map_id = resp.json()["id"]

        r1 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "concept", "title": "Prereq",
        })
        r2 = await auth_client.post(f"/api/v1/learning-maps/{map_id}/nodes", json={
            "node_type": "skill", "title": "Blocked Skill",
        })
        blocked_id = r2.json()["id"]

        await auth_client.post(f"/api/v1/learning-maps/{map_id}/edges", json={
            "from_node_id": r1.json()["id"], "to_node_id": blocked_id,
        })

        # Override the blocked node
        override_resp = await auth_client.post(
            f"/api/v1/children/{child.id}/nodes/{blocked_id}/override",
            json={"reason": "Child demonstrated competency in testing"},
        )
        assert override_resp.status_code == 200
        data = override_resp.json()
        assert "governance_event_id" in data
        assert data["node_id"] == blocked_id

        # Verify GovernanceEvent was created
        gov_result = await db_session.execute(
            select(GovernanceEvent).where(
                GovernanceEvent.id == uuid.UUID(data["governance_event_id"])
            )
        )
        gov_event = gov_result.scalar_one()
        assert gov_event.action == GovernanceAction.approve
        assert gov_event.target_type == "child_node_state"
        assert gov_event.user_id == user.id

        # Verify StateEvent was created
        se_result = await db_session.execute(
            select(StateEvent).where(
                StateEvent.child_id == child.id,
                StateEvent.node_id == uuid.UUID(blocked_id),
                StateEvent.event_type == StateEventType.override,
            )
        )
        state_event = se_result.scalar_one()
        assert state_event.trigger == "parent_override"

        # Verify ChildNodeState is now unlocked
        cns_result = await db_session.execute(
            select(ChildNodeState).where(
                ChildNodeState.child_id == child.id,
                ChildNodeState.node_id == uuid.UUID(blocked_id),
            )
        )
        cns = cns_result.scalar_one()
        assert cns.is_unlocked is True

        # Now the node should show as "available" in map state
        state_resp = await auth_client.get(
            f"/api/v1/children/{child.id}/map-state/{map_id}"
        )
        node_status = {n["title"]: n["status"] for n in state_resp.json()["nodes"]}
        assert node_status["Blocked Skill"] == "available"


class TestTemplates:

    @pytest.mark.asyncio
    async def test_list_templates(self, auth_client):
        resp = await auth_client.get("/api/v1/learning-maps/templates")
        assert resp.status_code == 200
        templates = resp.json()
        assert len(templates) == 7
        ids = {t["template_id"] for t in templates}
        assert "math-foundational" in ids
        assert "elementary-core" in ids
        assert "classical-logic" in ids

    @pytest.mark.asyncio
    async def test_copy_template_creates_independent_copy(
        self, auth_client, db_session, household,
    ):
        resp = await auth_client.post(
            "/api/v1/learning-maps/from-template/elementary-core"
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Elementary Core"
        assert data["node_count"] == 13
        assert data["edge_count"] == 10

        # Verify nodes were created with new UUIDs
        map_id = data["learning_map_id"]
        detail = await auth_client.get(f"/api/v1/learning-maps/{map_id}")
        assert detail.status_code == 200
        nodes = detail.json()["nodes"]
        assert len(nodes) == 13

        # Verify edges exist
        edges = detail.json()["edges"]
        assert len(edges) == 10

        # Verify closure table was built
        closure_result = await db_session.execute(
            select(LearningMapClosure).where(
                LearningMapClosure.learning_map_id == uuid.UUID(map_id)
            )
        )
        closures = closure_result.scalars().all()
        # Elementary Core has chains: math-root->mult->div->frac->dec (depth up to 4)
        assert len(closures) > 10  # More than just direct edges

    @pytest.mark.asyncio
    async def test_template_not_found(self, auth_client):
        resp = await auth_client.post(
            "/api/v1/learning-maps/from-template/nonexistent"
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_two_copies_are_independent(self, auth_client, db_session, household):
        """Copying same template twice creates independent maps."""
        r1 = await auth_client.post(
            "/api/v1/learning-maps/from-template/elementary-core"
        )
        r2 = await auth_client.post(
            "/api/v1/learning-maps/from-template/elementary-core"
        )
        assert r1.json()["learning_map_id"] != r2.json()["learning_map_id"]
        assert r1.json()["subject_id"] != r2.json()["subject_id"]


class TestSubjectAPI:

    @pytest.mark.asyncio
    async def test_create_and_list_subjects(self, auth_client):
        resp = await auth_client.post("/api/v1/subjects", json={
            "name": "Science", "color": "#FF5722", "icon": "flask",
        })
        assert resp.status_code == 201
        assert resp.json()["name"] == "Science"
        assert resp.json()["color"] == "#FF5722"

        resp2 = await auth_client.get("/api/v1/subjects")
        assert resp2.status_code == 200
        # At least the one we created (might have more from other fixtures)
        assert any(s["name"] == "Science" for s in resp2.json()["items"])
