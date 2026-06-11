"""Tests that the safety gate in learning_context blocks uncleared hazardous nodes.

This file is the proof that the safety hole identified in the prior commit
(hazardous trade nodes marked safety_review.reviewed=False being surfaceable
to a learner) is closed. The tests run against real authored content
(electrical_content.ELECTRICAL_CONTENT) plus deliberate fail-closed
fixtures (missing safety_review, malformed safety_review, non-bool truthy
reviewed value).

The gate is enforced at app/services/learning_context.py and consults
app/services/node_content.is_cleared_for_surfacing. The tests assert the
observable contract:

1. A real hazardous node with reviewed:false (els-001) returns an
   awaiting_human_safety_review context with blank lesson/assessment/
   practice content; the activity is never surfaced as a real lesson.
2. The gold-standard elc-021 (apprentice band, ELECTRICAL HAZARD,
   licensed-electrician-physically-present) is identically blocked.
3. Fail-closed: a hazardous node with safety_review missing or malformed
   is blocked.
4. A non-hazardous knowledge node (elc-003 Ohm's law) IS surfaceable
   normally (the gate does not block what it should not).
5. A hazardous node cleared via fixture (safety_review.reviewed=True
   with reviewer and reviewed_on populated) IS surfaceable, proving the
   gate opens correctly when content is reviewed.
6. The awaiting state carries explicit activity metadata so the
   parent / governance layer can see which activity is blocked.
"""

from datetime import date

import pytest

from app.content.electrical_content import ELECTRICAL_CONTENT
from app.models.curriculum import LearningNode
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    NodeType,
    PlanStatus,
)
from app.models.governance import Activity, Plan, PlanWeek
from app.services.learning_context import get_activity_learning_context
from app.services.node_content import (
    is_cleared_for_surfacing,
    requires_human_safety_review,
    requires_qualified_human_present_at_runtime,
)


# ---------------------------------------------------------------------------
# Pure-unit tests for the gate logic itself. These tests do NOT require a
# database and run in any environment. They prove the gate's contract
# (fail-closed, strict-bool, real-content) directly against the helper.
# The DB-backed integration tests below additionally prove the gate is
# wired into learning_context's surfacing path.
# ---------------------------------------------------------------------------


class TestGateLogicPureUnit:
    def test_real_els_001_blocked_by_gate(self):
        """els-001 (electrical safety entry) has safety_review.reviewed=False
        in the authored content. is_cleared_for_surfacing must return False.
        """
        node = ELECTRICAL_CONTENT["els-001"]
        assert requires_human_safety_review(node) is True
        assert is_cleared_for_surfacing(node) is False

    def test_real_elc_021_blocked_by_gate(self):
        """elc-021 (apprentice gold standard, ELECTRICAL HAZARD) has
        safety_review.reviewed=False. is_cleared_for_surfacing must return
        False, and requires_qualified_human_present_at_runtime must return
        True (the runtime-presence seam is identified).
        """
        node = ELECTRICAL_CONTENT["elc-021"]
        assert requires_human_safety_review(node) is True
        assert is_cleared_for_surfacing(node) is False
        assert requires_qualified_human_present_at_runtime(node) is True

    def test_real_elc_003_not_blocked_by_gate(self):
        """elc-003 (Ohm's law, knowledge node) does not require human
        safety review and is_cleared_for_surfacing must return True.
        """
        node = ELECTRICAL_CONTENT["elc-003"]
        assert requires_human_safety_review(node) is False
        assert is_cleared_for_surfacing(node) is True
        assert requires_qualified_human_present_at_runtime(node) is False

    def test_blocked_when_safety_review_missing(self):
        """Fail-closed: missing safety_review on a hazardous node blocks."""
        content = {k: v for k, v in ELECTRICAL_CONTENT["els-001"].items() if k != "safety_review"}
        assert is_cleared_for_surfacing(content) is False

    def test_blocked_when_safety_review_is_string(self):
        """Fail-closed: a non-dict safety_review on a hazardous node blocks."""
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = "not a dict"
        assert is_cleared_for_surfacing(content) is False

    def test_blocked_when_safety_review_is_empty_dict(self):
        """Fail-closed: an empty safety_review dict means reviewed is missing."""
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = {}
        assert is_cleared_for_surfacing(content) is False

    def test_blocked_when_reviewed_is_truthy_string(self):
        """Fail-closed: reviewed='true' (a string) does NOT clear; only the
        boolean True clears.
        """
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = {"reviewed": "true", "reviewer": "X", "reviewed_on": "2026-05-26", "standard_refs": []}
        assert is_cleared_for_surfacing(content) is False

    def test_blocked_when_reviewed_is_int_one(self):
        """Fail-closed: reviewed=1 is truthy but is NOT the boolean True."""
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = {"reviewed": 1, "reviewer": "X", "reviewed_on": "2026-05-26", "standard_refs": []}
        assert is_cleared_for_surfacing(content) is False

    def test_cleared_when_reviewed_is_bool_true(self):
        """Cleared: the boolean True clears the gate for a hazardous node
        (test fixture only; in real content this is set after a licensed
        electrician's review per the safety checklist).
        """
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = {
            "reviewed": True,
            "reviewer": "Test Licensed Electrician (test fixture only)",
            "reviewed_on": "2026-05-26",
            "standard_refs": [],
        }
        assert is_cleared_for_surfacing(content) is True

    def test_non_dict_content_not_blocked(self):
        """A non-dict content payload (None, string, etc.) is NOT itself a
        hazardous-node payload (the validator would reject it). The gate
        returns True so the surfacing path's title-fallback can run.
        """
        assert is_cleared_for_surfacing(None) is True
        assert is_cleared_for_surfacing("garbage") is True  # type: ignore[arg-type]
        assert is_cleared_for_surfacing({}) is True  # empty dict: no hazard, no gate

    @pytest.mark.parametrize(
        "node_id",
        [
            nid
            for nid in sorted(ELECTRICAL_CONTENT.keys())
            if ELECTRICAL_CONTENT[nid].get("node_type") == "safety"
            or (ELECTRICAL_CONTENT[nid].get("safety_basis") or {}).get("supervision_required") is True
        ],
    )
    def test_every_authored_hazardous_node_is_blocked_today(self, node_id):
        """Aggregate proof: every node in the authored electrical content
        where requires_human_safety_review returns True must be blocked,
        because none of them are reviewed:true. If this fails on a future
        commit, either someone set reviewed:true in real content (which is
        only correct after a licensed electrician's review per the
        checklist) or the gate logic was weakened.
        """
        node = ELECTRICAL_CONTENT[node_id]
        assert is_cleared_for_surfacing(node) is False, (
            f"hazardous node {node_id} would reach a learner without human safety review; "
            f"safety_review.reviewed is {node.get('safety_review', {}).get('reviewed')!r}"
        )


async def _make_activity_with_content(
    db_session, household, child, user, learning_map, content: dict
):
    """Create a LearningNode carrying the given content and an Activity
    pointing at it. Returns the Activity ORM object so the test can call
    get_activity_learning_context against it.
    """
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title=content.get("title") or content.get("competency_name", "test node"),
        content=content,
    )
    db_session.add(node)
    await db_session.flush()
    plan = Plan(
        household_id=household.id,
        child_id=child.id,
        created_by=user.id,
        name="Trade plan",
        status=PlanStatus.active,
    )
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 5),
    )
    db_session.add(week)
    await db_session.flush()
    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        node_id=node.id,
        activity_type=ActivityType.lesson,
        title="Lesson",
        status=ActivityStatus.scheduled,
        governance_approved=True,
    )
    db_session.add(activity)
    await db_session.flush()
    return activity


def _assert_blocked(ctx: dict) -> None:
    """Assertion bundle for the awaiting_human_safety_review state.

    The activity metadata stays (governance must know which activity is
    blocked). Everything else is empty / unavailable.
    """
    assert ctx.get("awaiting_human_safety_review") is True
    # Lesson content is empty
    lesson = ctx.get("lesson") or {}
    assert lesson.get("steps", None) in (None, [])
    assert lesson.get("introduction", "") == ""
    assert lesson.get("objectives", None) in (None, [])
    # Assessment is empty
    assessment = ctx.get("assessment") or {}
    assert not assessment.get("items"), "assessment items must not leak from a blocked node"
    assert not assessment.get("prompts"), "assessment prompts must not leak from a blocked node"
    # Practice items must not be served
    practice = ctx.get("practice") or {}
    assert not practice.get("items"), "practice items must not leak from a blocked node"
    # No reading passages
    reading = ctx.get("reading") or {}
    assert not reading.get("passages")
    # Tutor is unavailable on a blocked node
    assert ctx.get("tutor_available") is False
    # Philosophy variant must not leak
    philosophy = ctx.get("philosophy") or {}
    assert philosophy.get("content") is None
    assert philosophy.get("is_native") is False


def _assert_surfaced(ctx: dict) -> None:
    """Assertion bundle for the normal-surfacing state (gate open)."""
    # Gate did not block
    assert ctx.get("awaiting_human_safety_review") is not True
    # Real lesson content is present (either from authored teaching_guidance
    # or the title-fallback path)
    lesson = ctx.get("lesson") or {}
    assert lesson.get("introduction") or lesson.get("steps") or lesson.get("objectives"), (
        "a surfaced node must produce at least one of: introduction, steps, or objectives"
    )


class TestSafetyGateBlocksUnclearedHazardousNodes:
    @pytest.mark.asyncio
    async def test_real_els_001_blocked(
        self, db_session, household, child, user, subject, learning_map
    ):
        """els-001 is the real electrical safety competency. Its
        safety_review.reviewed is False in the authored content. The gate
        must block it. This is the highest-stakes proof case for the trade.
        """
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, ELECTRICAL_CONTENT["els-001"]
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_blocked(ctx)
        # Activity metadata still surfaces so governance can see which
        # activity is blocked
        assert ctx["activity"]["id"] == str(activity.id)

    @pytest.mark.asyncio
    async def test_real_elc_021_blocked(
        self, db_session, household, child, user, subject, learning_map
    ):
        """elc-021 is the apprentice-band gold standard: ELECTRICAL HAZARD,
        licensed-electrician-physically-present at the live moment. The
        content-review gate MUST block it while safety_review.reviewed is
        False, before the runtime presence check even comes into play.
        """
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, ELECTRICAL_CONTENT["elc-021"]
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_blocked(ctx)


class TestSafetyGateFailsClosed:
    @pytest.mark.asyncio
    async def test_blocked_when_safety_review_missing(
        self, db_session, household, child, user, subject, learning_map
    ):
        """A hazardous node with safety_review removed entirely must be
        blocked. Fail-closed: missing safety_review on a hazardous node
        means NOT cleared.
        """
        content = {k: v for k, v in ELECTRICAL_CONTENT["els-001"].items() if k != "safety_review"}
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, content
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_blocked(ctx)

    @pytest.mark.asyncio
    async def test_blocked_when_safety_review_malformed_as_string(
        self, db_session, household, child, user, subject, learning_map
    ):
        """A hazardous node with safety_review set to a non-dict (a string,
        in this case) must be blocked. Fail-closed: malformed safety_review
        on a hazardous node means NOT cleared.
        """
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = "not a dict"
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, content
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_blocked(ctx)

    @pytest.mark.asyncio
    async def test_blocked_when_reviewed_is_truthy_string_not_bool(
        self, db_session, household, child, user, subject, learning_map
    ):
        """reviewed='true' (a string) is NOT cleared. Only the boolean True
        clears. Fail-closed against accidental type coercion.
        """
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = {
            "reviewed": "true",
            "reviewer": "X",
            "reviewed_on": "2026-05-26",
            "standard_refs": [],
        }
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, content
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_blocked(ctx)

    @pytest.mark.asyncio
    async def test_blocked_when_reviewed_is_one_not_bool(
        self, db_session, household, child, user, subject, learning_map
    ):
        """reviewed=1 is truthy but is NOT the boolean True. Strict-bool
        comparison; not cleared.
        """
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = {
            "reviewed": 1,
            "reviewer": "X",
            "reviewed_on": "2026-05-26",
            "standard_refs": [],
        }
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, content
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_blocked(ctx)


class TestSafetyGateDoesNotBlockSafeNodes:
    @pytest.mark.asyncio
    async def test_real_elc_003_surfaced_normally(
        self, db_session, household, child, user, subject, learning_map
    ):
        """elc-003 (Ohm's law) is a knowledge node, supervision_required=False,
        not a safety competency. The gate must NOT block it; it surfaces
        with real lesson content.
        """
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, ELECTRICAL_CONTENT["elc-003"]
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_surfaced(ctx)
        # Real content surfaces: the introduction from teaching_guidance is non-empty
        lesson = ctx["lesson"]
        # elc-003 is authored without the academic teaching_guidance dict
        # (it carries a trades-shaped competency content). The learning_context
        # falls back to the title-built lesson; either way, objectives or
        # steps must be non-empty per the surfacing contract.
        assert lesson.get("objectives") or lesson.get("steps") or lesson.get("introduction")

    @pytest.mark.asyncio
    async def test_hazardous_node_surfaced_when_reviewed_true_fixture(
        self, db_session, household, child, user, subject, learning_map
    ):
        """A hazardous node with safety_review.reviewed=True (test fixture
        only — never set this in real content without a real review) IS
        surfaceable. This proves the gate OPENS correctly when content is
        cleared.

        This test uses els-001's actual content but overrides safety_review
        as if a qualified human had reviewed it. In production this would
        only be set after a licensed electrician has worked through the
        safety review checklist.

        els-001 also names a licensed electrician physically present, so
        since migration 058 the runtime presence gate stands behind the
        content-review gate. A same-day attestation is created here so
        this test isolates the content-review gate; the presence gate's
        own contract is pinned in test_runtime_presence_gate.py.
        """
        content = dict(ELECTRICAL_CONTENT["els-001"])
        content["safety_review"] = {
            "reviewed": True,
            "reviewer": "Test Licensed Electrician (test fixture only)",
            "reviewed_on": "2026-05-26",
            "standard_refs": list(ELECTRICAL_CONTENT["els-001"]["safety_review"]["standard_refs"]),
        }
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, content
        )

        from datetime import UTC, datetime, timedelta

        from app.models.governance import SupervisionAttestation

        db_session.add(
            SupervisionAttestation(
                household_id=household.id,
                child_id=child.id,
                node_id=activity.node_id,
                attested_by=user.id,
                role_claimed="licensed electrician",
                attested_at=datetime.now(UTC),
                expires_at=datetime.now(UTC) + timedelta(hours=4),
            )
        )
        await db_session.flush()

        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        _assert_surfaced(ctx)
        # Real content surfaced: this is the test-fixture-cleared safety
        # walkthrough; either authored or title-fallback content arrives
        lesson = ctx["lesson"]
        assert lesson.get("objectives") or lesson.get("steps") or lesson.get("introduction")


class TestAwaitingHumanSafetyReviewStateIsObservable:
    @pytest.mark.asyncio
    async def test_blocked_activity_metadata_visible_for_governance(
        self, db_session, household, child, user, subject, learning_map
    ):
        """When a node is blocked, the activity metadata (id, title, etc.)
        must remain visible so the parent / governance layer can see which
        activity is blocked. Only the *content* is suppressed.
        """
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, ELECTRICAL_CONTENT["els-001"]
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        # The block flag is set
        assert ctx.get("awaiting_human_safety_review") is True
        # Activity metadata remains visible
        assert ctx["activity"]["id"] == str(activity.id)
        assert ctx["activity"]["title"] == "Lesson"
        assert ctx["activity"]["activity_type"] == "lesson"
        # Tutor is unavailable on a blocked node
        assert ctx["tutor_available"] is False
        # Grade level (a learner-context field) remains visible for governance
        assert "grade_level" in ctx

    @pytest.mark.asyncio
    async def test_blocked_activity_emits_no_practice_or_assessment_items(
        self, db_session, household, child, user, subject, learning_map
    ):
        """elc-021's authored practice_items and assessment_items must NOT
        leak through the blocked-state response. This is the critical
        non-regression: a learner who hits a blocked activity sees no
        problem prompts that could be attempted unsupervised.
        """
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, ELECTRICAL_CONTENT["elc-021"]
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        assert ctx.get("awaiting_human_safety_review") is True
        # elc-021 carries no practice_items by design, but assert defensively:
        assert ctx["practice"] == {"items": []}
        assert ctx["assessment"] == {}
        # Lesson is empty
        assert ctx["lesson"] == {"widgets": []}


class TestEveryAuthoredHazardousNodeInElectricalIsBlockedToday:
    """Aggregate proof against the live authored content. Every node where
    requires_human_safety_review returns True in the current electrical
    trade content must be blocked, because none of them are reviewed:true.
    If this test starts failing on a future commit, either someone set
    reviewed:true in a node (which is only correct after a licensed
    electrician's review per the checklist) or someone weakened the gate.
    """

    @pytest.mark.parametrize(
        "node_id",
        [
            nid
            for nid in sorted(ELECTRICAL_CONTENT.keys())
            if ELECTRICAL_CONTENT[nid].get("node_type") == "safety"
            or (ELECTRICAL_CONTENT[nid].get("safety_basis") or {}).get("supervision_required") is True
        ],
    )
    @pytest.mark.asyncio
    async def test_real_hazardous_node_is_blocked(
        self, db_session, household, child, user, subject, learning_map, node_id
    ):
        activity = await _make_activity_with_content(
            db_session, household, child, user, learning_map, ELECTRICAL_CONTENT[node_id]
        )
        ctx = await get_activity_learning_context(
            db_session, activity.id, household.id, child.id
        )
        assert ctx.get("awaiting_human_safety_review") is True, (
            f"hazardous node {node_id} reached a learner without human safety review; "
            f"safety_review.reviewed is {ELECTRICAL_CONTENT[node_id].get('safety_review', {}).get('reviewed')!r}"
        )
