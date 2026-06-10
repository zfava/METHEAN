"""Tests for the Family Record: assembly, evidence chains, sealed export.

The record is a read-only lens over the event-sourced learner record;
these tests seed a real evidence chain (nodes, attempts, assessments,
governance approvals through log_governance_event so the hash chain is
genuine) and verify the record, the bundle, and its integrity model.
"""

import hashlib
import io
import json
import time
import uuid
import zipfile
from datetime import UTC, date, datetime, timedelta

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import event as sa_event
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password
from app.models.annual_curriculum import AnnualCurriculum
from app.models.assessment import Assessment
from app.models.curriculum import LearningMap, LearningNode
from app.models.enums import (
    ActivityType,
    AttemptStatus,
    GovernanceAction,
    MasteryLevel,
    NodeType,
    StateEventType,
)
from app.models.evidence import ReadingLogEntry
from app.models.governance import Activity, Attempt, GovernanceEvent, Plan, PlanWeek
from app.models.identity import Child, Household, User
from app.models.state import ChildNodeState, FSRSCard, StateEvent
from app.services.family_record import (
    assemble_family_record,
    build_record_bundle,
    export_family_record,
    record_content_hash,
)
from app.services.governance import (
    build_governance_hash_payload,
    compute_event_hash,
    log_governance_event,
    verify_chain,
)
from tests.conftest import test_engine as _test_engine

PASSWORD = "testpass123"


@pytest_asyncio.fixture(autouse=True)
def _no_s3(monkeypatch):
    """Export tests never touch S3; storage is patched at the service
    import site."""
    import app.services.family_record as fr

    monkeypatch.setattr(fr, "upload_artifact", lambda **kwargs: f"{kwargs['household_id']}/test/{kwargs['filename']}")
    monkeypatch.setattr(fr, "get_presigned_url", lambda s3_key, expires_in=3600: f"https://example.test/{s3_key}")


async def _seed_node_with_evidence(
    db: AsyncSession,
    household: Household,
    user: User,
    child: Child,
    learning_map: LearningMap,
    plan_week: PlanWeek,
    title: str,
    mastery: MasteryLevel,
    attempts: int = 2,
) -> dict:
    node = LearningNode(
        learning_map_id=learning_map.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title=title,
    )
    db.add(node)
    await db.flush()

    activity = Activity(
        plan_week_id=plan_week.id,
        household_id=household.id,
        title=f"Practice {title}",
        activity_type=ActivityType.practice,
        node_id=node.id,
    )
    db.add(activity)
    await db.flush()

    attempt_rows = []
    for i in range(attempts):
        attempt = Attempt(
            activity_id=activity.id,
            household_id=household.id,
            child_id=child.id,
            status=AttemptStatus.completed,
            score=0.8 + i * 0.05,
            duration_minutes=20,
            completed_at=datetime.now(UTC),
        )
        db.add(attempt)
        attempt_rows.append(attempt)
    await db.flush()

    db.add(
        Assessment(
            household_id=household.id,
            child_id=child.id,
            node_id=node.id,
            assessed_by=user.id,
            assessment_type="observation",
            title=f"Observed {title}",
            mastery_judgment=mastery.value,
        )
    )
    db.add(
        ChildNodeState(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            mastery_level=mastery,
            time_spent_minutes=40,
        )
    )
    db.add(
        StateEvent(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            event_type=StateEventType.mastery_change,
            from_state="developing",
            to_state=mastery.value,
        )
    )
    db.add(FSRSCard(child_id=child.id, household_id=household.id, node_id=node.id, stability=12.5))
    await db.flush()

    approval = await log_governance_event(
        db,
        household.id,
        user.id,
        GovernanceAction.approve,
        "activity",
        activity.id,
        reason=f"Approved {title}",
    )
    return {"node": node, "activity": activity, "attempts": attempt_rows, "approval": approval}


@pytest_asyncio.fixture
async def seeded_record(db_session, household, user, child, learning_map):
    """A child with two evidence-bearing nodes, one below threshold,
    a curriculum, and a reading log entry."""
    household.home_state = "NY"
    plan = Plan(household_id=household.id, child_id=child.id, name="Plan", status="active")
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 6, 8),
        end_date=date(2026, 6, 14),
    )
    db_session.add(week)
    await db_session.flush()

    proficient = await _seed_node_with_evidence(
        db_session, household, user, child, learning_map, week, "Addition", MasteryLevel.proficient
    )
    mastered = await _seed_node_with_evidence(
        db_session, household, user, child, learning_map, week, "Subtraction", MasteryLevel.mastered
    )
    below = await _seed_node_with_evidence(
        db_session, household, user, child, learning_map, week, "Multiplication", MasteryLevel.developing
    )

    db_session.add(
        AnnualCurriculum(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            subject_name="Mathematics",
            academic_year="2025-2026",
            grade_level="3",
            status="active",
            start_date=date(2025, 9, 1),
            end_date=date(2026, 6, 15),
            actual_record={"weeks": {"1": {}}, "overall_mastery": "proficient"},
        )
    )
    db_session.add(
        ReadingLogEntry(
            household_id=household.id,
            child_id=child.id,
            created_by=user.id,
            book_title="Charlotte's Web",
            book_author="E. B. White",
            status="finished",
            pages_total=192,
            pages_read=192,
        )
    )
    await db_session.flush()
    return {"proficient": proficient, "mastered": mastered, "below": below}


# ── Assembly ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_record_assembles_with_full_evidence(db_session, household, child, seeded_record):
    record = await assemble_family_record(db_session, household.id, child.id)

    assert record.identity.child_first_name == child.first_name
    assert record.identity.household_state == "NY"
    assert record.transcript.courses[0].subject_name == "Mathematics"
    assert record.attendance.total_hours > 0
    assert len(record.reading_log) == 1
    assert record.reading_log[0].title == "Charlotte's Web"

    titles = {m.node_title for m in record.mastery_evidence}
    assert titles == {"Addition", "Subtraction"}, "only proficient and above belong in evidence"
    for m in record.mastery_evidence:
        assert len(m.attempts) == 2
        assert len(m.assessments) == 1
        assert len(m.governance_events) >= 1
        assert m.fsrs_stability == 12.5
        assert m.achieved_at is not None
        assert m.subject == "Mathematics"


@pytest.mark.asyncio
async def test_identity_carries_birth_year_never_full_dob(db_session, household, child, seeded_record):
    child.date_of_birth = date(2017, 3, 14)
    await db_session.flush()
    record = await assemble_family_record(db_session, household.id, child.id)
    assert record.identity.birth_year == 2017
    dumped = json.dumps(record.model_dump(mode="json"), default=str)
    assert "2017-03-14" not in dumped


@pytest.mark.asyncio
async def test_evidence_event_hashes_exist_in_governance_chain(db_session, household, child, seeded_record):
    record = await assemble_family_record(db_session, household.id, child.id)
    chain = await db_session.execute(
        select(GovernanceEvent.event_hash).where(GovernanceEvent.household_id == household.id)
    )
    chain_hashes = {row[0] for row in chain.all()}
    evidence_hashes = [e.event_hash for m in record.mastery_evidence for e in m.governance_events]
    assert evidence_hashes, "seeded approvals must surface in the evidence chain"
    for event_hash in evidence_hashes:
        assert event_hash in chain_hashes


@pytest.mark.asyncio
async def test_integrity_chain_verified_true(db_session, household, child, seeded_record):
    record = await assemble_family_record(db_session, household.id, child.id)
    assert record.integrity.chain_verified is True
    assert record.integrity.event_count >= 3
    assert record.integrity.head_hash is not None


def test_tamper_detection_at_unit_level():
    """The pure verify_chain catches an altered event without any DB
    mutation (the append-only triggers forbid one anyway)."""
    chain = []
    prev = None
    for i in range(3):
        payload = build_governance_hash_payload(
            household_id=str(uuid.uuid4()),
            user_id=None,
            action=GovernanceAction.approve,
            target_type="activity",
            target_id=str(uuid.uuid4()),
            reason=f"r{i}",
            metadata={},
            created_at=f"2026-06-10T00:00:0{i}+00:00",
        )
        h = compute_event_hash(payload, prev)
        chain.append({**payload, "event_hash": h, "prev_event_hash": prev})
        prev = h
    assert verify_chain(chain)["valid"] is True
    chain[1]["reason"] = "tampered"
    report = verify_chain(chain)
    assert report["valid"] is False and report["first_break_index"] == 1


@pytest.mark.asyncio
async def test_transcript_section_matches_shared_assembly(db_session, household, child, seeded_record):
    from app.services.document_generator import assemble_transcript_data

    shared = await assemble_transcript_data(db_session, household.id, child.id)
    record = await assemble_family_record(db_session, household.id, child.id)

    assert [c.model_dump() for c in record.transcript.courses] == shared["courses"]
    assert record.transcript.cumulative_hours.total_hours == shared["hours"]["total_hours"]
    assert record.transcript.cumulative_hours.by_subject == shared["hours"]["by_subject"]


@pytest.mark.asyncio
async def test_transcript_pdf_still_generates_after_extraction(db_session, household, child, seeded_record):
    from app.services.document_generator import generate_transcript

    pdf = await generate_transcript(db_session, household.id, child.id)
    assert pdf[:4] == b"%PDF" or b"Academic Transcript" in pdf


# ── Sealed bundle ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_bundle_contains_required_files_and_hashes_match(db_session, household, child, seeded_record):
    bundle_bytes, manifest = await build_record_bundle(db_session, household.id, child.id)

    with zipfile.ZipFile(io.BytesIO(bundle_bytes)) as zf:
        names = set(zf.namelist())
        assert {"record.json", "manifest.json", "transcript.pdf", "attendance.pdf", "VERIFICATION.md"} <= names

        embedded = json.loads(zf.read("manifest.json"))
        assert embedded["bundle_hash"] == manifest["bundle_hash"]

        for name, expected_hash in manifest["files"].items():
            assert hashlib.sha256(zf.read(name)).hexdigest() == expected_hash, name

    hash_lines = "".join(f"{n}:{manifest['files'][n]}\n" for n in sorted(manifest["files"]))
    recomputed = hashlib.sha256((hash_lines + manifest["chain_head_hash"]).encode("utf-8")).hexdigest()
    assert recomputed == manifest["bundle_hash"]


@pytest.mark.asyncio
async def test_bundle_includes_ihip_when_inputs_exist(db_session, household, child, seeded_record):
    bundle_bytes, manifest = await build_record_bundle(db_session, household.id, child.id)
    with zipfile.ZipFile(io.BytesIO(bundle_bytes)) as zf:
        assert "ihip.pdf" in zf.namelist()
    skipped_names = {s["name"] for s in manifest["skipped_documents"]}
    assert "ihip.pdf" not in skipped_names
    assert "quarterly_report.pdf" in skipped_names


@pytest.mark.asyncio
async def test_skipped_documents_listed_not_fatal(db_session, household, child, seeded_record):
    household.home_state = None
    await db_session.flush()
    bundle_bytes, manifest = await build_record_bundle(db_session, household.id, child.id)
    with zipfile.ZipFile(io.BytesIO(bundle_bytes)) as zf:
        assert "ihip.pdf" not in zf.namelist()
    skipped = {s["name"]: s["reason"] for s in manifest["skipped_documents"]}
    assert "ihip.pdf" in skipped
    assert "home_state" in skipped["ihip.pdf"]


@pytest.mark.asyncio
async def test_record_content_is_deterministic(db_session, household, child, seeded_record):
    first = await assemble_family_record(db_session, household.id, child.id)
    second = await assemble_family_record(db_session, household.id, child.id)

    assert record_content_hash(first) == record_content_hash(second)

    a = first.model_dump(mode="json")
    b = second.model_dump(mode="json")
    a["identity"].pop("record_generated_at")
    b["identity"].pop("record_generated_at")
    assert a == b


@pytest.mark.asyncio
async def test_export_logs_governance_event_and_advances_chain(db_session, household, user, child, seeded_record):
    first = await export_family_record(db_session, household.id, child.id, user.id)

    logged = await db_session.execute(
        select(GovernanceEvent).where(
            GovernanceEvent.household_id == household.id,
            GovernanceEvent.target_type == "family_record_exported",
        )
    )
    events = list(logged.scalars().all())
    assert len(events) == 1
    assert events[0].metadata_["bundle_hash"] == first["bundle_hash"]

    second = await export_family_record(db_session, household.id, child.id, user.id)
    first_record = await assemble_family_record(db_session, household.id, child.id)
    # The first export's event is now in the chain, so the second
    # export sealed a different head.
    assert second["bundle_hash"] != first["bundle_hash"]
    assert first_record.integrity.event_count >= 5


@pytest.mark.asyncio
async def test_export_returns_download_url_and_artifact(db_session, household, user, child, seeded_record):
    result = await export_family_record(db_session, household.id, child.id, user.id)
    assert result["download_url"].startswith("https://example.test/")
    assert result["expires_in"] == 3600
    assert result["bundle_hash"]
    from app.models.evidence import Artifact

    artifact = await db_session.get(Artifact, result["artifact_id"])
    assert artifact is not None
    assert artifact.metadata_["kind"] == "family_record_bundle"


# ── Endpoints: auth, isolation, gating ──────────────────────────────


@pytest.mark.asyncio
async def test_get_endpoint_returns_record(auth_client: AsyncClient, child, seeded_record):
    response = await auth_client.get(f"/api/v1/children/{child.id}/family-record")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["format"] == "methean-family-record/1"
    assert data["integrity"]["chain_verified"] is True


@pytest.mark.asyncio
async def test_export_endpoint_and_listing(auth_client: AsyncClient, child, seeded_record):
    exported = await auth_client.post(f"/api/v1/children/{child.id}/family-record/export")
    assert exported.status_code == 200, exported.text
    body = exported.json()
    assert body["bundle_hash"] and body["download_url"]

    listing = await auth_client.get("/api/v1/family-record/exports")
    assert listing.status_code == 200
    items = listing.json()
    assert len(items) == 1
    assert items[0]["bundle_hash"] == body["bundle_hash"]


@pytest.mark.asyncio
async def test_household_isolation(client: AsyncClient, db_session, household, child, seeded_record):
    other = Household(
        name="Other Family",
        timezone="UTC",
        subscription_status="trialing",
        trial_ends_at=datetime.now(UTC) + timedelta(days=14),
    )
    db_session.add(other)
    await db_session.flush()
    from app.core.database import set_tenant

    await set_tenant(db_session, other.id)
    other_user = User(
        household_id=other.id,
        email="other-fr@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Other",
        role="owner",
        email_verified=True,
    )
    db_session.add(other_user)
    await db_session.flush()
    client.cookies.set("access_token", create_access_token(other_user.id, other.id, "owner"))

    read = await client.get(f"/api/v1/children/{child.id}/family-record")
    assert read.status_code == 404
    export = await client.post(f"/api/v1/children/{child.id}/family-record/export")
    assert export.status_code == 404
    listing = await client.get("/api/v1/family-record/exports")
    assert listing.status_code == 200 and listing.json() == []


@pytest.mark.asyncio
async def test_child_token_denied_on_all_three_endpoints(auth_client: AsyncClient, child, seeded_record):
    enter = await auth_client.post("/api/v1/auth/child-session/enter", json={"child_id": str(child.id)})
    assert enter.status_code == 200

    for method, path in (
        ("GET", f"/api/v1/children/{child.id}/family-record"),
        ("POST", f"/api/v1/children/{child.id}/family-record/export"),
        ("GET", "/api/v1/family-record/exports"),
    ):
        response = await auth_client.request(method, path)
        assert response.status_code == 403, path
        assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_unverified_email_denied(client: AsyncClient, db_session, household, child):
    unverified = User(
        household_id=household.id,
        email="unverified-fr@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Unverified",
        role="owner",
        email_verified=False,
    )
    db_session.add(unverified)
    await db_session.flush()
    client.cookies.set("access_token", create_access_token(unverified.id, household.id, "owner"))

    response = await client.get(f"/api/v1/children/{child.id}/family-record")
    assert response.status_code == 403
    assert response.json() == {"detail": "email_not_verified"}


@pytest.mark.asyncio
async def test_subscription_gating(client: AsyncClient, db_session):
    lapsed = Household(name="Lapsed Family", timezone="UTC", subscription_status="canceled")
    db_session.add(lapsed)
    await db_session.flush()
    from app.core.database import set_tenant

    await set_tenant(db_session, lapsed.id)
    lapsed_user = User(
        household_id=lapsed.id,
        email="lapsed-fr@test.com",
        password_hash=hash_password(PASSWORD),
        display_name="Lapsed",
        role="owner",
        email_verified=True,
    )
    lapsed_child = Child(household_id=lapsed.id, first_name="Kid")
    db_session.add_all([lapsed_user, lapsed_child])
    await db_session.flush()
    client.cookies.set("access_token", create_access_token(lapsed_user.id, lapsed.id, "owner"))

    response = await client.get(f"/api/v1/children/{lapsed_child.id}/family-record")
    assert response.status_code == 402


@pytest.mark.asyncio
async def test_allowed_state_with_active_trial(auth_client: AsyncClient, child, seeded_record):
    """The conftest household is trialing: the same surface that 402s a
    lapsed household serves a trialing one."""
    response = await auth_client.get(f"/api/v1/children/{child.id}/family-record")
    assert response.status_code == 200


# ── Read-only guarantee and performance ─────────────────────────────


@pytest.mark.asyncio
async def test_assembly_writes_nothing(db_session, household, child, seeded_record):
    """assemble_family_record and build_record_bundle leave the session
    with no pending new objects."""
    await db_session.flush()
    await assemble_family_record(db_session, household.id, child.id)
    assert not db_session.new and not db_session.dirty
    await build_record_bundle(db_session, household.id, child.id)
    assert not db_session.new and not db_session.dirty


@pytest.mark.asyncio
async def test_large_record_bounded_queries_and_under_two_seconds(db_session, household, user, child, learning_map):
    """300 evidence-bearing nodes and ~2,000 attempts: assembly must
    stay under 2 seconds with a bounded (non-N+1) query count."""
    plan = Plan(household_id=household.id, child_id=child.id, name="Big Plan", status="active")
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 6, 8),
        end_date=date(2026, 6, 14),
    )
    db_session.add(week)
    await db_session.flush()

    nodes = [
        LearningNode(
            learning_map_id=learning_map.id,
            household_id=household.id,
            node_type=NodeType.concept,
            title=f"Node {i}",
        )
        for i in range(300)
    ]
    db_session.add_all(nodes)
    await db_session.flush()

    activities = [
        Activity(
            plan_week_id=week.id,
            household_id=household.id,
            title=f"Activity {i}",
            activity_type=ActivityType.practice,
            node_id=node.id,
        )
        for i, node in enumerate(nodes)
    ]
    db_session.add_all(activities)
    await db_session.flush()

    rows = []
    for i, node in enumerate(nodes):
        rows.append(
            ChildNodeState(
                child_id=child.id,
                household_id=household.id,
                node_id=node.id,
                mastery_level=MasteryLevel.mastered if i % 2 else MasteryLevel.proficient,
                time_spent_minutes=30,
            )
        )
        for j in range(7):
            rows.append(
                Attempt(
                    activity_id=activities[i].id,
                    household_id=household.id,
                    child_id=child.id,
                    status=AttemptStatus.completed,
                    score=0.9,
                )
            )
    db_session.add_all(rows)
    await db_session.flush()

    statements: list[str] = []

    def _count(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    sa_event.listen(_test_engine.sync_engine, "before_cursor_execute", _count)
    try:
        started = time.monotonic()
        record = await assemble_family_record(db_session, household.id, child.id)
        elapsed = time.monotonic() - started
    finally:
        sa_event.remove(_test_engine.sync_engine, "before_cursor_execute", _count)

    assert len(record.mastery_evidence) == 300
    assert sum(len(m.attempts) for m in record.mastery_evidence) == 2100
    assert elapsed < 2.0, f"assembly took {elapsed:.2f}s"
    assert len(statements) <= 25, f"unbounded query count: {len(statements)}"
