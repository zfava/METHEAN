"""Qualified-human runtime presence gate (migration 058).

A node whose supervision_basis names a qualified human who must be
physically present at the work (requires_qualified_human_present_at_runtime)
is not surfaced to the learner, even after content review clears, until
a parent attests today that the qualified human is present for this
child and this node. These tests pin the contract:

1. The gate fails closed: no attestation, an expired attestation, an
   attestation for a different node or child, or a missing child_id all
   block surfacing with the awaiting_qualified_human shape (identical
   emptiness to the content-review gate's blocked shape).
2. The content-review gate stays first and independent: an uncleared
   hazardous node reports awaiting_human_safety_review, never the
   presence flag.
3. A valid attestation opens the gate for that child, node, and day.
4. The attestation endpoint is parent-only (child-scoped tokens and
   observers are rejected), validates the node actually requires the
   runtime check, expires at the household-local end of day, and
   hash-chains a supervision_attested governance event.
5. The parent day view (/children/{id}/today) flags which activities
   require supervision, whether today's attestation exists, and the
   role to pre-fill.
"""

import uuid
from datetime import UTC, date, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import select

from app.content.electrical_content import ELECTRICAL_CONTENT
from app.models.curriculum import LearningNode
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    GovernanceAction,
    NodeType,
    PlanStatus,
)
from app.models.governance import (
    Activity,
    GovernanceEvent,
    Plan,
    PlanWeek,
    SupervisionAttestation,
)
from app.services.learning_context import get_activity_learning_context
from app.services.node_content import requires_qualified_human_present_at_runtime
from app.services.supervision import (
    get_valid_attestation,
    local_end_of_day,
    required_role_from_content,
)

ATTEST_URL = "/api/v1/children/{child_id}/supervision-attestation"


def _cleared_hazardous_content() -> dict:
    """elc-021 (licensed-electrician-physically-present) with the
    content-review gate cleared via test fixture, so only the runtime
    presence gate stands between the node and the learner.
    """
    content = dict(ELECTRICAL_CONTENT["elc-021"])
    content["safety_review"] = {
        "reviewed": True,
        "reviewer": "Test Licensed Electrician (test fixture only)",
        "reviewed_on": "2026-06-11",
        "standard_refs": [],
    }
    assert requires_qualified_human_present_at_runtime(content) is True
    return content


async def _make_node(db_session, household, learning_map, content: dict) -> LearningNode:
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title=content.get("competency_name", "test node"),
        content=content,
    )
    db_session.add(node)
    await db_session.flush()
    return node


async def _make_activity(
    db_session, household, child, user, node, scheduled_date: date | None = None
) -> Activity:
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
        title="Live panel work",
        status=ActivityStatus.scheduled,
        governance_approved=True,
        scheduled_date=scheduled_date,
    )
    db_session.add(activity)
    await db_session.flush()
    return activity


async def _attest(db_session, household, child, node, user, expires_at: datetime) -> SupervisionAttestation:
    attestation = SupervisionAttestation(
        household_id=household.id,
        child_id=child.id,
        node_id=node.id,
        attested_by=user.id,
        role_claimed="licensed electrician",
        attested_at=datetime.now(UTC),
        expires_at=expires_at,
    )
    db_session.add(attestation)
    await db_session.flush()
    return attestation


def _assert_presence_blocked(ctx: dict) -> None:
    """The awaiting_qualified_human shape: identical emptiness to the
    content-review gate's blocked shape, under the presence flag.
    """
    assert ctx.get("awaiting_qualified_human") is True
    assert ctx.get("awaiting_human_safety_review") is not True
    assert ctx["lesson"] == {"widgets": []}
    assert ctx["assessment"] == {}
    assert ctx["practice"] == {"items": []}
    assert ctx["reading"] == {"passages": []}
    assert ctx["tutor_available"] is False
    assert ctx["philosophy"]["content"] is None
    assert ctx["philosophy"]["is_native"] is False


def _assert_surfaced(ctx: dict) -> None:
    assert ctx.get("awaiting_qualified_human") is not True
    assert ctx.get("awaiting_human_safety_review") is not True
    lesson = ctx.get("lesson") or {}
    assert lesson.get("introduction") or lesson.get("steps") or lesson.get("objectives")


# ── Pure units: role extraction + local end of day ────────────────────────


class TestRoleExtractionAndExpiry:
    def test_required_role_from_elc_021(self):
        assert required_role_from_content(ELECTRICAL_CONTENT["elc-021"]) == "licensed electrician"

    def test_required_role_fails_closed_on_malformed_content(self):
        assert required_role_from_content(None) is None
        assert required_role_from_content({}) is None
        assert required_role_from_content({"safety_basis": "not a dict"}) is None
        assert required_role_from_content({"safety_basis": {"supervision_basis": 42}}) is None
        assert required_role_from_content({"safety_basis": {"supervision_basis": "an adult nearby"}}) is None

    def test_local_end_of_day_is_household_local_not_utc(self):
        """02:00 UTC on June 11 is still June 10 in New York; the
        attestation must expire at the end of June 10 local, not June 11
        UTC. This is the no-standing-waiver property.
        """
        now = datetime(2026, 6, 11, 2, 0, tzinfo=UTC)
        expires = local_end_of_day("America/New_York", now)
        local = expires.astimezone(ZoneInfo("America/New_York"))
        assert local.date() == date(2026, 6, 10)
        assert (local.hour, local.minute, local.second) == (23, 59, 59)
        assert expires > now

    def test_local_end_of_day_unknown_timezone_falls_back_to_utc(self):
        now = datetime(2026, 6, 11, 2, 0, tzinfo=UTC)
        expires = local_end_of_day("Not/AZone", now)
        assert expires.astimezone(UTC).date() == date(2026, 6, 11)
        assert expires - now < timedelta(hours=24)


# ── Service gate: fail closed ──────────────────────────────────────────────


class TestPresenceGateFailsClosed:
    @pytest.mark.asyncio
    async def test_cleared_hazardous_node_blocked_without_attestation(
        self, db_session, household, child, user, subject, learning_map
    ):
        """Content review passed, but no one has attested a qualified
        human is present today: the node must NOT surface.
        """
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        activity = await _make_activity(db_session, household, child, user, node)
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_presence_blocked(ctx)
        assert ctx["activity"]["id"] == str(activity.id)

    @pytest.mark.asyncio
    async def test_content_review_gate_stays_first_and_independent(
        self, db_session, household, child, user, subject, learning_map
    ):
        """elc-021 unreviewed: the content-review gate fires, and the
        presence flag is NOT set. The two gates never blur together.
        """
        node = await _make_node(db_session, household, learning_map, dict(ELECTRICAL_CONTENT["elc-021"]))
        activity = await _make_activity(db_session, household, child, user, node)
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        assert ctx.get("awaiting_human_safety_review") is True
        assert "awaiting_qualified_human" not in ctx

    @pytest.mark.asyncio
    async def test_blocked_when_child_id_missing(
        self, db_session, household, child, user, subject, learning_map
    ):
        """Attestations are per child; a context built without a child_id
        cannot prove one. Fail closed.
        """
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        activity = await _make_activity(db_session, household, child, user, node)
        await _attest(db_session, household, child, node, user, datetime.now(UTC) + timedelta(hours=4))
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, None)
        _assert_presence_blocked(ctx)

    @pytest.mark.asyncio
    async def test_expired_attestation_blocks(
        self, db_session, household, child, user, subject, learning_map
    ):
        """Yesterday's attestation is not today's. No standing waivers."""
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        activity = await _make_activity(db_session, household, child, user, node)
        await _attest(db_session, household, child, node, user, datetime.now(UTC) - timedelta(hours=1))
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_presence_blocked(ctx)

    @pytest.mark.asyncio
    async def test_attestation_for_other_node_blocks(
        self, db_session, household, child, user, subject, learning_map
    ):
        """Attestations are per node: presence at the breaker panel does
        not cover the gas line.
        """
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        other_node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        activity = await _make_activity(db_session, household, child, user, node)
        await _attest(db_session, household, child, other_node, user, datetime.now(UTC) + timedelta(hours=4))
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_presence_blocked(ctx)

    @pytest.mark.asyncio
    async def test_attestation_for_other_child_blocks(
        self, db_session, household, child, second_child, user, subject, learning_map
    ):
        """Attestations are per child: supervising one sibling's work
        does not surface the node for the other.
        """
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        activity = await _make_activity(db_session, household, child, user, node)
        await _attest(db_session, household, second_child, node, user, datetime.now(UTC) + timedelta(hours=4))
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_presence_blocked(ctx)

    @pytest.mark.asyncio
    async def test_non_hazardous_node_unaffected(
        self, db_session, household, child, user, subject, learning_map
    ):
        """elc-003 (Ohm's law) needs no runtime presence; the gate must
        not block it and must not stamp either awaiting flag.
        """
        node = await _make_node(db_session, household, learning_map, dict(ELECTRICAL_CONTENT["elc-003"]))
        activity = await _make_activity(db_session, household, child, user, node)
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_surfaced(ctx)
        assert "awaiting_qualified_human" not in ctx


# ── Service gate: opens on a valid attestation ─────────────────────────────


class TestPresenceGateOpens:
    @pytest.mark.asyncio
    async def test_valid_attestation_surfaces_content(
        self, db_session, household, child, user, subject, learning_map
    ):
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        activity = await _make_activity(db_session, household, child, user, node)
        await _attest(db_session, household, child, node, user, datetime.now(UTC) + timedelta(hours=4))
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_surfaced(ctx)

    @pytest.mark.asyncio
    async def test_get_valid_attestation_household_scoped(
        self, db_session, household, child, user, subject, learning_map
    ):
        """The read helper requires the household to match; a forged
        household_id finds nothing.
        """
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        await _attest(db_session, household, child, node, user, datetime.now(UTC) + timedelta(hours=4))
        found = await get_valid_attestation(db_session, household.id, child.id, node.id)
        assert found is not None
        missing = await get_valid_attestation(db_session, uuid.uuid4(), child.id, node.id)
        assert missing is None


# ── Endpoint: POST /children/{child_id}/supervision-attestation ───────────


class TestAttestationEndpoint:
    @pytest.mark.asyncio
    async def test_attest_creates_row_and_hash_chained_event(
        self, auth_client, db_session, household, child, user, subject, learning_map
    ):
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        resp = await auth_client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(node.id), "role_claimed": "licensed electrician", "note": "On site all day."},
        )
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["child_id"] == str(child.id)
        assert body["node_id"] == str(node.id)
        assert body["role_claimed"] == "licensed electrician"

        row = (
            await db_session.execute(
                select(SupervisionAttestation).where(SupervisionAttestation.id == uuid.UUID(body["id"]))
            )
        ).scalar_one()
        assert row.attested_by == user.id
        assert row.note == "On site all day."

        gov = (
            await db_session.execute(
                select(GovernanceEvent).where(GovernanceEvent.id == uuid.UUID(body["governance_event_id"]))
            )
        ).scalar_one()
        assert gov.action == GovernanceAction.approve
        assert gov.target_type == "supervision_attested"
        assert gov.target_id == node.id
        assert gov.metadata_["role_claimed"] == "licensed electrician"
        assert gov.metadata_["child_id"] == str(child.id)
        assert gov.event_hash, "attestation events must ride the hash chain"

        verify = await auth_client.get("/api/v1/chain/verify")
        assert verify.status_code == 200
        assert verify.json()["valid"] is True

    @pytest.mark.asyncio
    async def test_expires_at_is_household_local_end_of_day(
        self, auth_client, db_session, household, child, subject, learning_map
    ):
        """The test household is America/New_York; the returned expiry
        must be the last moment of today in New York, regardless of the
        server's UTC clock.
        """
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        before = datetime.now(UTC)
        resp = await auth_client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(node.id), "role_claimed": "licensed electrician"},
        )
        assert resp.status_code == 201, resp.text
        expires = datetime.fromisoformat(resp.json()["expires_at"])
        local = expires.astimezone(ZoneInfo("America/New_York"))
        assert local.date() == before.astimezone(ZoneInfo("America/New_York")).date()
        assert (local.hour, local.minute, local.second) == (23, 59, 59)
        assert expires > before
        assert expires - before < timedelta(hours=24)

    @pytest.mark.asyncio
    async def test_attest_then_context_surfaces(
        self, auth_client, db_session, household, child, user, subject, learning_map
    ):
        """The full parent story: blocked, attest, surfaced."""
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        activity = await _make_activity(db_session, household, child, user, node)
        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_presence_blocked(ctx)

        resp = await auth_client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(node.id), "role_claimed": "licensed electrician"},
        )
        assert resp.status_code == 201, resp.text

        ctx = await get_activity_learning_context(db_session, activity.id, household.id, child.id)
        _assert_surfaced(ctx)

    @pytest.mark.asyncio
    async def test_attest_non_hazardous_node_400(
        self, auth_client, db_session, household, child, subject, learning_map
    ):
        node = await _make_node(db_session, household, learning_map, dict(ELECTRICAL_CONTENT["elc-003"]))
        resp = await auth_client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(node.id), "role_claimed": "qualified adult"},
        )
        assert resp.status_code == 400, resp.text

    @pytest.mark.asyncio
    async def test_attest_unknown_node_404(self, auth_client, child):
        resp = await auth_client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(uuid.uuid4()), "role_claimed": "qualified adult"},
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthenticated_401(self, client, child):
        resp = await client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(uuid.uuid4()), "role_claimed": "qualified adult"},
        )
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_observer_403(self, observer_client, db_session, household, child, subject, learning_map):
        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        resp = await observer_client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(node.id), "role_claimed": "licensed electrician"},
        )
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_child_scoped_token_403(
        self, client, db_session, household, child, user, subject, learning_map
    ):
        """A kid-mode session can never attest its own supervision."""
        from app.core.security import create_access_token

        node = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        token = create_access_token(user.id, household.id, "owner", scope="child", child_id=child.id)
        client.cookies.set("access_token", token)
        resp = await client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(node.id), "role_claimed": "licensed electrician"},
        )
        assert resp.status_code == 403


# ── Parent day view: /children/{child_id}/today flags ─────────────────────


class TestTodayViewSurfacesSupervisionState:
    @pytest.mark.asyncio
    async def test_today_flags_and_attestation_roundtrip(
        self, auth_client, db_session, household, child, user, subject, learning_map
    ):
        hazardous = await _make_node(db_session, household, learning_map, _cleared_hazardous_content())
        safe = await _make_node(db_session, household, learning_map, dict(ELECTRICAL_CONTENT["elc-003"]))
        await _make_activity(db_session, household, child, user, hazardous, scheduled_date=date.today())
        await _make_activity(db_session, household, child, user, safe, scheduled_date=date.today())

        resp = await auth_client.get(f"/api/v1/children/{child.id}/today")
        assert resp.status_code == 200, resp.text
        by_node = {a["node_id"]: a for a in resp.json()}
        hazardous_row = by_node[str(hazardous.id)]
        assert hazardous_row["requires_supervision"] is True
        assert hazardous_row["supervision_attested"] is False
        assert hazardous_row["required_role"] == "licensed electrician"
        safe_row = by_node[str(safe.id)]
        assert safe_row["requires_supervision"] is False
        assert safe_row["supervision_attested"] is False
        assert safe_row["required_role"] is None

        attest = await auth_client.post(
            ATTEST_URL.format(child_id=child.id),
            json={"node_id": str(hazardous.id), "role_claimed": "licensed electrician"},
        )
        assert attest.status_code == 201, attest.text

        resp = await auth_client.get(f"/api/v1/children/{child.id}/today")
        by_node = {a["node_id"]: a for a in resp.json()}
        assert by_node[str(hazardous.id)]["supervision_attested"] is True
