"""Tests for governed-agency child choice routing.

Covers the safety invariants and acceptance criteria for PARENT-FINAL,
CURRICULUM-AUTHORED, READINESS-INFORMED child choice:

- parent latitude widen / tighten / disable overrides the author default;
  unset = author default (pure resolution).
- auto-class proposal applies immediately; review-class proposal queues and
  does NOT mutate child learning state until parent approval.
- parent DISABLE removes proposability for a class regardless of author
  default.
- an option not in the bounded proposable set is rejected and never an open
  field.
- an approved and a rejected proposal both leave immutable governance
  events carrying child / node / option / outcome sufficient for a future
  readiness service.
"""

import uuid

import pytest
from sqlalchemy import select

from app.models.governance import GovernanceEvent
from app.models.state import ChildNodeState, StateEvent
from app.services.child_choice import (
    CHILD_CHOICE_PROPOSAL,
    ChildChoiceOutcome,
    is_option_proposable,
    propose_child_choice,
    resolve_latitude,
    resolve_pending_choice,
)


def _choice_space(author_default="auto") -> dict:
    return {
        "choice_space": {
            "proposable": [
                {"class": "order", "option": "addition_first"},
                {"class": "order", "option": "subtraction_first"},
                {"class": "practice_variant", "option": "objects"},
                {"class": "practice_variant", "option": "number_line"},
            ],
            "excluded_note": (
                "Consequential decisions (prerequisite-skip, mastery-declaration, subject-exit) "
                "are not in scope and never child-proposable."
            ),
            "author_default_latitude": author_default,
        }
    }


# ── Pure latitude resolution (B: mirror the AI oversight dial) ──


class TestResolveLatitude:
    def test_unset_parent_uses_author_default(self):
        cs = _choice_space("auto")["choice_space"]
        assert resolve_latitude(cs, None, "order") == "auto"
        assert resolve_latitude(cs, {}, "order") == "auto"

    def test_parent_tighten_overrides_author_default(self):
        cs = _choice_space("auto")["choice_space"]
        assert resolve_latitude(cs, {"order": "review"}, "order") == "review"

    def test_parent_widen_overrides_author_default(self):
        cs = _choice_space("review")["choice_space"]
        assert resolve_latitude(cs, {"order": "auto"}, "order") == "auto"

    def test_parent_disable_overrides_author_default(self):
        cs = _choice_space("auto")["choice_space"]
        assert resolve_latitude(cs, {"order": "disabled"}, "order") == "disabled"

    def test_parent_override_is_per_class(self):
        cs = _choice_space("auto")["choice_space"]
        parent = {"order": "review"}
        assert resolve_latitude(cs, parent, "order") == "review"
        # other classes fall back to the author default
        assert resolve_latitude(cs, parent, "practice_variant") == "auto"

    def test_per_class_author_default_dict(self):
        cs = {
            "proposable": [{"class": "order", "option": "a"}],
            "excluded_note": "x",
            "author_default_latitude": {"order": "review", "practice_variant": "auto"},
        }
        assert resolve_latitude(cs, None, "order") == "review"
        assert resolve_latitude(cs, None, "practice_variant") == "auto"
        # unlisted class falls back to the safe default
        assert resolve_latitude(cs, None, "pacing_within_bounds") == "review"

    def test_missing_author_default_is_safe_review(self):
        cs = {"proposable": [{"class": "order", "option": "a"}], "excluded_note": "x"}
        assert resolve_latitude(cs, None, "order") == "review"

    def test_is_option_proposable(self):
        cs = _choice_space()["choice_space"]
        assert is_option_proposable(cs, "order", "addition_first") is True
        assert is_option_proposable(cs, "order", "made_up") is False
        assert is_option_proposable(cs, "practice_variant", "addition_first") is False


# ── Governance routing (C + D) ──


async def _learning_state_rows(db, child_id):
    states = (await db.execute(select(ChildNodeState).where(ChildNodeState.child_id == child_id))).scalars().all()
    events = (await db.execute(select(StateEvent).where(StateEvent.child_id == child_id))).scalars().all()
    return states, events


class TestChildChoiceRouting:
    @pytest.mark.asyncio
    async def test_auto_class_applies_immediately(self, db_session, household, child):
        node_id = uuid.uuid4()
        outcome = await propose_child_choice(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=node_id,
            node_content=_choice_space("auto"),
            choice_class="order",
            option="addition_first",
        )
        assert isinstance(outcome, ChildChoiceOutcome)
        assert outcome.status == "applied"
        assert outcome.latitude == "auto"
        assert outcome.state_mutated is False

        events = (
            (
                await db_session.execute(
                    select(GovernanceEvent).where(GovernanceEvent.target_type == CHILD_CHOICE_PROPOSAL)
                )
            )
            .scalars()
            .all()
        )
        assert len(events) == 1
        assert (events[0].metadata_ or {}).get("outcome") == "applied"

    @pytest.mark.asyncio
    async def test_review_class_queues_and_does_not_mutate_state(self, db_session, household, child):
        node_id = uuid.uuid4()
        states_before, events_before = await _learning_state_rows(db_session, child.id)

        outcome = await propose_child_choice(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=node_id,
            node_content=_choice_space("review"),
            choice_class="order",
            option="addition_first",
        )
        assert outcome.status == "queued"
        assert outcome.reason == "waiting for approval"
        assert outcome.state_mutated is False

        # No learning state may change before parent approval.
        states_after, events_after = await _learning_state_rows(db_session, child.id)
        assert len(states_after) == len(states_before)
        assert len(events_after) == len(events_before)

        # The queued proposal is recorded as a deferred governance event.
        gov = (
            (
                await db_session.execute(
                    select(GovernanceEvent).where(GovernanceEvent.target_type == CHILD_CHOICE_PROPOSAL)
                )
            )
            .scalars()
            .all()
        )
        assert len(gov) == 1
        assert (gov[0].metadata_ or {}).get("outcome") == "queued"

    @pytest.mark.asyncio
    async def test_parent_disable_removes_proposability(self, db_session, household, child):
        node_id = uuid.uuid4()
        outcome = await propose_child_choice(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=node_id,
            node_content=_choice_space("auto"),
            choice_class="order",
            option="addition_first",
            parent_latitude={"order": "disabled"},
        )
        assert outcome.status == "rejected"
        assert outcome.latitude == "disabled"
        assert outcome.state_mutated is False

        gov = (
            (
                await db_session.execute(
                    select(GovernanceEvent).where(GovernanceEvent.target_type == CHILD_CHOICE_PROPOSAL)
                )
            )
            .scalars()
            .all()
        )
        assert len(gov) == 1
        assert (gov[0].metadata_ or {}).get("outcome") == "rejected_disabled"

    @pytest.mark.asyncio
    async def test_option_not_proposable_rejected_no_event(self, db_session, household, child):
        node_id = uuid.uuid4()
        outcome = await propose_child_choice(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=node_id,
            node_content=_choice_space("auto"),
            choice_class="order",
            option="some_open_field_value",
        )
        assert outcome.status == "rejected"
        assert outcome.event_id is None
        # No governance event is logged for an option that was never offered.
        gov = (
            (
                await db_session.execute(
                    select(GovernanceEvent).where(GovernanceEvent.target_type == CHILD_CHOICE_PROPOSAL)
                )
            )
            .scalars()
            .all()
        )
        assert gov == []

    @pytest.mark.asyncio
    async def test_invalid_choice_space_raises(self, db_session, household, child):
        # A node whose choice_space smuggles in a consequential decision is
        # not a valid choice_space; proposing against it is a programming
        # error.
        bad = {
            "choice_space": {
                "proposable": [{"class": "prerequisite_skip", "option": "skip_it"}],
                "excluded_note": "x",
            }
        }
        with pytest.raises(ValueError):
            await propose_child_choice(
                db_session,
                household_id=household.id,
                child_id=child.id,
                node_id=uuid.uuid4(),
                node_content=bad,
                choice_class="prerequisite_skip",
                option="skip_it",
            )

    @pytest.mark.asyncio
    async def test_event_capture_approved_and_rejected_immutable(self, db_session, household, child, user):
        """An approved and a rejected proposal both leave immutable events
        carrying child / node / option / outcome for future readiness
        derivation."""
        node_id = uuid.uuid4()

        # Queue a review-class proposal, then the parent approves it.
        proposal = await propose_child_choice(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=node_id,
            node_content=_choice_space("review"),
            choice_class="order",
            option="addition_first",
        )
        approved = await resolve_pending_choice(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=node_id,
            choice_class="order",
            option="addition_first",
            approve=True,
            user_id=user.id,
            proposal_event_id=proposal.event_id,
        )
        assert approved.status == "applied"

        # A separate proposal the parent rejects.
        node_id2 = uuid.uuid4()
        rejected = await resolve_pending_choice(
            db_session,
            household_id=household.id,
            child_id=child.id,
            node_id=node_id2,
            choice_class="practice_variant",
            option="objects",
            approve=False,
            user_id=user.id,
        )
        assert rejected.status == "rejected"

        events = (
            (
                await db_session.execute(
                    select(GovernanceEvent)
                    .where(GovernanceEvent.target_type == CHILD_CHOICE_PROPOSAL)
                    .order_by(GovernanceEvent.created_at.asc())
                )
            )
            .scalars()
            .all()
        )
        # proposal (queued) + approve + reject = 3 immutable events
        outcomes = [(e.metadata_ or {}).get("outcome") for e in events]
        assert "queued" in outcomes
        assert "approved" in outcomes
        assert "rejected" in outcomes

        # Every event carries the fields a readiness service needs.
        for e in events:
            meta = e.metadata_ or {}
            assert meta.get("child_id") == str(child.id)
            assert meta.get("node_id") in {str(node_id), str(node_id2)}
            assert meta.get("choice_class") in {"order", "practice_variant"}
            assert meta.get("option") in {"addition_first", "objects"}
            assert meta.get("outcome") is not None
            assert e.created_at is not None
