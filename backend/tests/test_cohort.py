"""Tests for cohort analytics (institutional mode)."""

import pytest

from app.models.curriculum import ChildMapEnrollment, LearningNode
from app.models.enums import MasteryLevel, NodeType
from app.models.identity import Child
from app.models.state import ChildNodeState


async def _make_map(auth_client, subject_id: str, name: str = "Cohort Map") -> str:
    resp = await auth_client.post(
        "/api/v1/learning-maps",
        json={"subject_id": subject_id, "name": name},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_cohort_stats_no_enrollments(auth_client, subject):
    map_id = await _make_map(auth_client, str(subject.id))
    resp = await auth_client.get(f"/api/v1/learning-maps/{map_id}/cohort")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["total_enrolled"] == 0
    assert data["completion_rate"] == 0.0
    assert data["total_nodes"] == 0
    assert data["mastery_distribution"] == {
        "not_started": 0,
        "emerging": 0,
        "developing": 0,
        "proficient": 0,
        "mastered": 0,
    }


@pytest.mark.asyncio
async def test_cohort_stats_with_students(auth_client, db_session, household, subject):
    import uuid as _uuid

    map_id = await _make_map(auth_client, str(subject.id), "Distrib Map")

    node_ids = []
    for title in ["N1", "N2", "N3"]:
        n = LearningNode(
            learning_map_id=_uuid.UUID(map_id),
            household_id=household.id,
            node_type=NodeType.concept,
            title=title,
        )
        db_session.add(n)
        await db_session.flush()
        node_ids.append(n.id)

    children = []
    for name in ["A", "B", "C"]:
        c = Child(household_id=household.id, first_name=name)
        db_session.add(c)
        await db_session.flush()
        children.append(c)
        db_session.add(
            ChildMapEnrollment(
                child_id=c.id, household_id=household.id, learning_map_id=_uuid.UUID(map_id)
            )
        )

    # Child A: all 3 mastered
    # Child B: 2 proficient, 1 developing
    # Child C: 1 emerging (others missing -> count as not_started)
    levels = [
        (children[0].id, node_ids[0], MasteryLevel.mastered),
        (children[0].id, node_ids[1], MasteryLevel.mastered),
        (children[0].id, node_ids[2], MasteryLevel.mastered),
        (children[1].id, node_ids[0], MasteryLevel.proficient),
        (children[1].id, node_ids[1], MasteryLevel.proficient),
        (children[1].id, node_ids[2], MasteryLevel.developing),
        (children[2].id, node_ids[0], MasteryLevel.emerging),
    ]
    for cid, nid, lvl in levels:
        db_session.add(
            ChildNodeState(
                child_id=cid, household_id=household.id, node_id=nid, mastery_level=lvl
            )
        )
    await db_session.flush()

    resp = await auth_client.get(f"/api/v1/learning-maps/{map_id}/cohort")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["total_enrolled"] == 3
    assert data["total_nodes"] == 3

    dist = data["mastery_distribution"]
    # Total cells = 3 children * 3 nodes = 9
    # mastered: 3 (child A), proficient: 2 (child B), developing: 1 (child B),
    # emerging: 1 (child C), not_started: 2 missing rows for child C
    assert dist["mastered"] == 3
    assert dist["proficient"] == 2
    assert dist["developing"] == 1
    assert dist["emerging"] == 1
    assert dist["not_started"] == 2
    assert sum(dist.values()) == 9


@pytest.mark.asyncio
async def test_cohort_completion_rate(auth_client, db_session, household, subject):
    import uuid as _uuid

    map_id = await _make_map(auth_client, str(subject.id), "Completion Map")

    node_ids = []
    for title in ["X", "Y"]:
        n = LearningNode(
            learning_map_id=_uuid.UUID(map_id),
            household_id=household.id,
            node_type=NodeType.concept,
            title=title,
        )
        db_session.add(n)
        await db_session.flush()
        node_ids.append(n.id)

    children = []
    for name in ["One", "Two", "Three"]:
        c = Child(household_id=household.id, first_name=name)
        db_session.add(c)
        await db_session.flush()
        children.append(c)
        db_session.add(
            ChildMapEnrollment(
                child_id=c.id, household_id=household.id, learning_map_id=_uuid.UUID(map_id)
            )
        )

    # Only child One masters all nodes
    for nid in node_ids:
        db_session.add(
            ChildNodeState(
                child_id=children[0].id,
                household_id=household.id,
                node_id=nid,
                mastery_level=MasteryLevel.mastered,
            )
        )
    await db_session.flush()

    resp = await auth_client.get(f"/api/v1/learning-maps/{map_id}/cohort")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    # 1 of 3 completed -> 33.3
    assert data["completion_rate"] == 33.3


@pytest.mark.asyncio
async def test_cohort_requires_auth(client, subject):
    # Create a map via authed client is not available; this test only
    # needs to hit the endpoint with a random UUID unauthenticated.
    import uuid as _uuid

    fake_map_id = _uuid.uuid4()
    resp = await client.get(f"/api/v1/learning-maps/{fake_map_id}/cohort")
    assert resp.status_code == 401
