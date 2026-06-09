"""Parent override of an automated mastery demotion.

POST /children/{child_id}/nodes/{node_id}/mastery-override restores a node to a
chosen mastery level with a recorded reason, dual-logged to an immutable
GovernanceEvent (the audit decision) and a StateEvent (append-only state
history), mirroring the blocked-node unlock override. Tests cover the service
function, the endpoint's dual-logging, the end-to-end demotion-then-override
story via /history, and validation/scoping. No em dashes.
"""

import uuid

import pytest
from sqlalchemy import func, select

from app.models.curriculum import LearningNode
from app.models.enums import GovernanceAction, MasteryLevel, NodeType, StateEventType
from app.models.governance import GovernanceEvent
from app.models.state import StateEvent
from app.services.state_engine import (
    apply_mastery_override,
    get_or_create_node_state,
    process_review,
)

OVERRIDE_URL = "/api/v1/children/{child_id}/nodes/{node_id}/mastery-override"


async def _make_node(db, household, learning_map, title) -> LearningNode:
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title=title,
    )
    db.add(node)
    await db.flush()
    return node


# ── Service: apply_mastery_override ───────────────────────────────────────


class TestApplyMasteryOverride:
    @pytest.mark.asyncio
    async def test_updates_state_and_appends_override_event(self, db_session, household, learning_map, child, user):
        node = await _make_node(db_session, household, learning_map, "Svc Node")
        # Start at proficient (a demoted node).
        state = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        state.mastery_level = MasteryLevel.proficient
        await db_session.flush()

        result = await apply_mastery_override(
            db_session,
            child.id,
            household.id,
            node.id,
            MasteryLevel.mastered,
            "Parent saw the work; this is solid.",
            user.id,
        )

        assert result["previous_level"] == MasteryLevel.proficient
        assert result["new_level"] == MasteryLevel.mastered

        refreshed = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        assert refreshed.mastery_level == MasteryLevel.mastered

        event = (
            await db_session.execute(select(StateEvent).where(StateEvent.id == result["state_event_id"]))
        ).scalar_one()
        assert event.event_type == StateEventType.override
        assert event.from_state == "proficient"
        assert event.to_state == "mastered"
        assert event.trigger == "parent_override"
        assert event.created_by == user.id
        assert event.metadata_["reason"] == "Parent saw the work; this is solid."
        assert event.metadata_["overridden_by"] == str(user.id)
        assert event.metadata_["override_kind"] == "mastery_demotion_reversal"

    @pytest.mark.asyncio
    async def test_no_op_is_recorded(self, db_session, household, learning_map, child, user):
        node = await _make_node(db_session, household, learning_map, "Svc No-op")
        state = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        state.mastery_level = MasteryLevel.proficient
        await db_session.flush()

        result = await apply_mastery_override(
            db_session,
            child.id,
            household.id,
            node.id,
            MasteryLevel.proficient,  # same as current
            "Reaffirming this is fine where it is.",
            user.id,
        )
        assert result["previous_level"] == MasteryLevel.proficient
        assert result["new_level"] == MasteryLevel.proficient
        event = (
            await db_session.execute(select(StateEvent).where(StateEvent.id == result["state_event_id"]))
        ).scalar_one()
        assert event.from_state == "proficient"
        assert event.to_state == "proficient"


# ── Endpoint: dual-logging + responses ────────────────────────────────────


class TestMasteryOverrideEndpoint:
    @pytest.mark.asyncio
    async def test_override_dual_logs_and_returns_ids(self, auth_client, db_session, household, learning_map, child):
        node = await _make_node(db_session, household, learning_map, "Endpoint Node")
        state = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        state.mastery_level = MasteryLevel.proficient
        await db_session.flush()

        resp = await auth_client.post(
            OVERRIDE_URL.format(child_id=child.id, node_id=node.id),
            json={"target_level": "mastered", "reason": "I reviewed it; restore mastery."},
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["child_id"] == str(child.id)
        assert body["node_id"] == str(node.id)
        assert body["new_mastery_level"] == "mastered"
        assert body["governance_event_id"]
        assert body["state_event_id"]

        # ChildNodeState updated in place.
        updated = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        assert updated.mastery_level == MasteryLevel.mastered

        # Exactly one GovernanceEvent: action=modify, target_type=child_node_state.
        gov = (
            await db_session.execute(
                select(GovernanceEvent).where(GovernanceEvent.id == uuid.UUID(body["governance_event_id"]))
            )
        ).scalar_one()
        assert gov.action == GovernanceAction.modify
        assert gov.target_type == "child_node_state"
        assert gov.target_id == node.id
        assert gov.reason == "I reviewed it; restore mastery."
        assert gov.user_id is not None

        # Exactly one StateEvent: event_type=override.
        se = (
            await db_session.execute(select(StateEvent).where(StateEvent.id == uuid.UUID(body["state_event_id"])))
        ).scalar_one()
        assert se.event_type == StateEventType.override
        assert se.trigger == "parent_override"
        assert se.to_state == "mastered"

    @pytest.mark.asyncio
    async def test_demotion_then_override_full_story_in_history(
        self, auth_client, db_session, household, learning_map, child
    ):
        node = await _make_node(db_session, household, learning_map, "Story Node")
        # Phase 1 attempt demotion: reach mastered, then a below-line attempt.
        await process_review(db_session, child.id, household.id, node.id, confidence=0.95)
        await process_review(db_session, child.id, household.id, node.id, confidence=0.7)
        await db_session.flush()

        # Parent overrides it back to mastered.
        resp = await auth_client.post(
            OVERRIDE_URL.format(child_id=child.id, node_id=node.id),
            json={"target_level": "mastered", "reason": "Overruling the demotion."},
        )
        assert resp.status_code == 200, resp.text

        history = (await auth_client.get(f"/api/v1/children/{child.id}/nodes/{node.id}/history")).json()
        events = history["items"]
        # History is chronological; find the demotion (mastery_change with a
        # demotion_explanation) followed by the override.
        demotion_idx = next(
            i
            for i, e in enumerate(events)
            if e["event_type"] == StateEventType.mastery_change.value and e["to_state"] == "proficient"
        )
        override_idx = next(i for i, e in enumerate(events) if e["event_type"] == StateEventType.override.value)
        assert demotion_idx < override_idx
        assert events[override_idx]["to_state"] == "mastered"
        assert events[override_idx]["trigger"] == "parent_override"

    @pytest.mark.asyncio
    async def test_empty_reason_422(self, auth_client, db_session, household, learning_map, child):
        node = await _make_node(db_session, household, learning_map, "Empty Reason")
        resp = await auth_client.post(
            OVERRIDE_URL.format(child_id=child.id, node_id=node.id),
            json={"target_level": "mastered", "reason": ""},
        )
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_unknown_node_404(self, auth_client, household, child):
        resp = await auth_client.post(
            OVERRIDE_URL.format(child_id=child.id, node_id=uuid.uuid4()),
            json={"target_level": "mastered", "reason": "valid reason"},
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_target_equal_current_is_accepted(self, auth_client, db_session, household, learning_map, child):
        node = await _make_node(db_session, household, learning_map, "Same Level")
        state = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        state.mastery_level = MasteryLevel.proficient
        await db_session.flush()

        resp = await auth_client.post(
            OVERRIDE_URL.format(child_id=child.id, node_id=node.id),
            json={"target_level": "proficient", "reason": "Keeping it here on purpose."},
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["new_mastery_level"] == "proficient"

        # The reaffirmation is still recorded as a governance + state event.
        gov_count = await db_session.scalar(
            select(func.count())
            .select_from(GovernanceEvent)
            .where(GovernanceEvent.target_id == node.id, GovernanceEvent.action == GovernanceAction.modify)
        )
        assert gov_count == 1
        override_count = await db_session.scalar(
            select(func.count())
            .select_from(StateEvent)
            .where(StateEvent.node_id == node.id, StateEvent.event_type == StateEventType.override)
        )
        assert override_count == 1


# ── Scoping ────────────────────────────────────────────────────────────────


class TestMasteryOverrideScoping:
    @pytest.mark.asyncio
    async def test_unauthenticated_blocked(self, client, child):
        node_id = uuid.uuid4()
        resp = await client.post(
            OVERRIDE_URL.format(child_id=child.id, node_id=node_id),
            json={"target_level": "mastered", "reason": "x"},
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_observer_cannot_override(self, client, db_session, household, child, learning_map, observer_user):
        from app.core.security import create_access_token

        node = await _make_node(db_session, household, learning_map, "Observer Node")
        await db_session.flush()

        token = create_access_token(observer_user.id, household.id, "observer")
        client.cookies.set("access_token", token)
        resp = await client.post(
            OVERRIDE_URL.format(child_id=child.id, node_id=node.id),
            json={"target_level": "mastered", "reason": "observer tries"},
        )
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_state_events_are_append_only(self, db_session, household, learning_map, child, user):
        """An override appends a new StateEvent; no prior event is mutated."""
        node = await _make_node(db_session, household, learning_map, "Append Only")
        state = await get_or_create_node_state(db_session, child.id, household.id, node.id)
        state.mastery_level = MasteryLevel.proficient
        await db_session.flush()

        before = await db_session.scalar(
            select(func.count()).select_from(StateEvent).where(StateEvent.node_id == node.id)
        )
        await apply_mastery_override(
            db_session, child.id, household.id, node.id, MasteryLevel.mastered, "append test", user.id
        )
        after = await db_session.scalar(
            select(func.count()).select_from(StateEvent).where(StateEvent.node_id == node.id)
        )
        assert after == before + 1
