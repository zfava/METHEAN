"""METHEAN Family Record assembly and sealed export.

Read-only lens over the event-sourced learner record. Assembles the
cumulative record (transcript, mastery evidence chains, attendance,
reading log) and seals exports into a ZIP bundle whose manifest hash
ties to the household's governance hash-chain head (migration 052).
Institutions issue credentials by authority; METHEAN issues them by
evidence, and this module is the data layer that proves it.

Writes NOTHING to learner state. The only persistence this module
performs is the export artifact row (S3 object + artifacts table) and
the governance log entry recording that an export happened.
"""

import hashlib
import io
import json
import uuid
import zipfile
from datetime import UTC, date, datetime, timedelta

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.annual_curriculum import AnnualCurriculum
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import ArtifactType, GovernanceAction, MasteryLevel, StateEventType
from app.models.evidence import Artifact, ReadingLogEntry
from app.models.governance import Activity, Attempt, GovernanceEvent
from app.models.identity import Child, Household
from app.models.state import ChildNodeState, FSRSCard, StateEvent
from app.schemas.family_record import (
    AttendanceSection,
    CumulativeHours,
    EvidenceAssessment,
    EvidenceAttempt,
    EvidenceGovernanceEvent,
    FamilyRecord,
    IdentitySection,
    IntegritySection,
    MasteryEvidence,
    ReadingLogItem,
    TranscriptCourse,
    TranscriptSection,
)
from app.services.document_generator import (
    assemble_transcript_data,
    generate_attendance_record,
    generate_ihip,
    generate_transcript,
)
from app.services.governance import build_governance_hash_payload, log_governance_event, verify_chain
from app.services.storage import get_presigned_url, upload_artifact

logger = structlog.get_logger()

# Mirrors the FastAPI app version in app/main.py. Kept as a constant
# here because importing app.main from a service would be circular.
METHEAN_VERSION = "0.1.0"

# Mastery levels that count as credentialed evidence in the record.
EVIDENCE_MASTERY_LEVELS = (MasteryLevel.proficient, MasteryLevel.mastered)

DOWNLOAD_URL_EXPIRES_SECONDS = 3600

_ASSESSMENT_PLACEHOLDER = "untitled assessment"


def _enum_value(value: object) -> str:
    return value.value if hasattr(value, "value") else str(value)


async def _load_chain(db: AsyncSession, household_id: uuid.UUID) -> tuple[list[GovernanceEvent], IntegritySection]:
    """Load the household's full governance chain and verify it.

    Reuses the pure verify_chain from services/governance.py: the same
    canonical payload and hash recomputation the /chain/verify endpoint
    uses, so the record's integrity section can never disagree with it.
    """
    result = await db.execute(
        select(GovernanceEvent)
        .where(GovernanceEvent.household_id == household_id)
        .order_by(GovernanceEvent.created_at.asc(), GovernanceEvent.id.asc())
    )
    events = list(result.scalars().all())
    chain_dicts = [
        {
            **build_governance_hash_payload(
                household_id=e.household_id,
                user_id=e.user_id,
                action=e.action,
                target_type=e.target_type,
                target_id=e.target_id,
                reason=e.reason,
                metadata=e.metadata_,
                created_at=e.created_at,
            ),
            "event_hash": e.event_hash,
            "prev_event_hash": e.prev_event_hash,
        }
        for e in events
    ]
    report = verify_chain(chain_dicts)
    integrity = IntegritySection(
        head_hash=events[-1].event_hash if events else None,
        chain_verified=bool(report["valid"]),
        event_count=len(events),
    )
    return events, integrity


async def assemble_family_record(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
) -> FamilyRecord:
    """Assemble the cumulative Family Record for one child.

    Bounded queries only: every collection is fetched with a single
    batched IN query keyed by the child's evidence-bearing nodes, so
    assembly cost does not grow per node (no N+1).
    """
    child_result = await db.execute(select(Child).where(Child.id == child_id, Child.household_id == household_id))
    child = child_result.scalar_one_or_none()
    if child is None:
        raise ValueError("Child not found")
    household_result = await db.execute(select(Household).where(Household.id == household_id))
    household = household_result.scalar_one()

    # Transcript: the exact data the PDF transcript uses (shared
    # assembly in document_generator, single source of truth).
    transcript_data = await assemble_transcript_data(db, household_id, child_id)

    # Evidence-bearing node states (proficient and above).
    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
            ChildNodeState.mastery_level.in_(EVIDENCE_MASTERY_LEVELS),
        )
    )
    states = list(states_result.scalars().all())
    node_ids = [s.node_id for s in states]

    nodes: dict[uuid.UUID, tuple[LearningNode, str | None]] = {}
    attempts_by_node: dict[uuid.UUID, list[EvidenceAttempt]] = {}
    assessments_by_node: dict[uuid.UUID, list[EvidenceAssessment]] = {}
    stability_by_node: dict[uuid.UUID, float] = {}
    achieved_by_node: dict[uuid.UUID, datetime] = {}
    attempt_ids: list[uuid.UUID] = []
    activity_ids: list[uuid.UUID] = []
    activity_node: dict[uuid.UUID, uuid.UUID] = {}
    attempt_node: dict[uuid.UUID, uuid.UUID] = {}

    if node_ids:
        nodes_result = await db.execute(
            select(LearningNode, Subject.name)
            .join(LearningMap, LearningNode.learning_map_id == LearningMap.id)
            .join(Subject, LearningMap.subject_id == Subject.id, isouter=True)
            .where(LearningNode.id.in_(node_ids))
        )
        for node, subject_name in nodes_result.all():
            nodes[node.id] = (node, subject_name)

        attempts_result = await db.execute(
            select(Attempt, Activity)
            .join(Activity, Attempt.activity_id == Activity.id)
            .where(Attempt.child_id == child_id, Activity.node_id.in_(node_ids))
            .order_by(Attempt.started_at.asc(), Attempt.id.asc())
        )
        for attempt, activity in attempts_result.all():
            node_id = activity.node_id
            attempt_ids.append(attempt.id)
            attempt_node[attempt.id] = node_id
            if activity.id not in activity_node:
                activity_ids.append(activity.id)
                activity_node[activity.id] = node_id
            attempts_by_node.setdefault(node_id, []).append(
                EvidenceAttempt(
                    id=attempt.id,
                    activity_id=activity.id,
                    activity_title=activity.title,
                    status=_enum_value(attempt.status),
                    score=attempt.score,
                    started_at=attempt.started_at,
                    completed_at=attempt.completed_at,
                    duration_minutes=attempt.duration_minutes,
                )
            )

        from app.models.assessment import Assessment

        assessments_result = await db.execute(
            select(Assessment)
            .where(Assessment.child_id == child_id, Assessment.node_id.in_(node_ids))
            .order_by(Assessment.assessed_at.asc(), Assessment.id.asc())
        )
        for assessment in assessments_result.scalars().all():
            assessments_by_node.setdefault(assessment.node_id, []).append(
                EvidenceAssessment(
                    id=assessment.id,
                    assessment_type=_enum_value(assessment.assessment_type),
                    title=assessment.title or _ASSESSMENT_PLACEHOLDER,
                    mastery_judgment=assessment.mastery_judgment,
                    assessed_at=assessment.assessed_at,
                )
            )

        cards_result = await db.execute(
            select(FSRSCard.node_id, FSRSCard.stability).where(
                FSRSCard.child_id == child_id, FSRSCard.node_id.in_(node_ids)
            )
        )
        for node_id, stability in cards_result.all():
            stability_by_node[node_id] = stability

        # achieved_at: the latest mastery_change state event whose
        # to_state matches the node's current mastery level.
        events_result = await db.execute(
            select(StateEvent)
            .where(
                StateEvent.child_id == child_id,
                StateEvent.node_id.in_(node_ids),
                StateEvent.event_type == StateEventType.mastery_change,
            )
            .order_by(StateEvent.created_at.asc())
        )
        current_level = {s.node_id: _enum_value(s.mastery_level) for s in states}
        for state_event in events_result.scalars().all():
            if state_event.to_state == current_level.get(state_event.node_id):
                achieved_by_node[state_event.node_id] = state_event.created_at

    # Governance events referencing the node, its activities, or its
    # attempts: one batched query over all referenced ids.
    governance_by_node: dict[uuid.UUID, list[EvidenceGovernanceEvent]] = {}
    referenced: dict[uuid.UUID, uuid.UUID] = {}
    for node_id in node_ids:
        referenced[node_id] = node_id
    referenced.update(activity_node)
    referenced.update(attempt_node)
    if referenced:
        gov_result = await db.execute(
            select(GovernanceEvent)
            .where(
                GovernanceEvent.household_id == household_id,
                GovernanceEvent.target_id.in_(list(referenced.keys())),
            )
            .order_by(GovernanceEvent.created_at.asc(), GovernanceEvent.id.asc())
        )
        for event in gov_result.scalars().all():
            node_id = referenced[event.target_id]
            governance_by_node.setdefault(node_id, []).append(
                EvidenceGovernanceEvent(
                    id=event.id,
                    action=_enum_value(event.action),
                    target_type=event.target_type,
                    target_id=event.target_id,
                    reason=event.reason,
                    created_at=event.created_at,
                    event_hash=event.event_hash,
                    prev_event_hash=event.prev_event_hash,
                )
            )

    mastery_evidence = []
    for state in sorted(states, key=lambda s: str(s.node_id)):
        node_pair = nodes.get(state.node_id)
        if node_pair is None:
            continue
        node, subject_name = node_pair
        mastery_evidence.append(
            MasteryEvidence(
                node_id=node.id,
                node_title=node.title,
                node_type=_enum_value(node.node_type),
                subject=subject_name,
                mastery_level=_enum_value(state.mastery_level),
                achieved_at=achieved_by_node.get(node.id),
                fsrs_stability=stability_by_node.get(node.id),
                attempts=attempts_by_node.get(node.id, []),
                assessments=assessments_by_node.get(node.id, []),
                governance_events=governance_by_node.get(node.id, []),
            )
        )

    hours = transcript_data["hours"]
    reading_result = await db.execute(
        select(ReadingLogEntry)
        .where(ReadingLogEntry.child_id == child_id, ReadingLogEntry.household_id == household_id)
        .order_by(ReadingLogEntry.created_at.asc())
    )
    reading_log = [
        ReadingLogItem(
            title=entry.book_title,
            author=entry.book_author,
            genre=entry.genre,
            status=_enum_value(entry.status) if entry.status is not None else None,
            pages_read=entry.pages_read,
            pages_total=entry.pages_total,
            child_rating=entry.child_rating,
        )
        for entry in reading_result.scalars().all()
    ]

    _, integrity = await _load_chain(db, household_id)

    return FamilyRecord(
        identity=IdentitySection(
            child_first_name=child.first_name,
            child_last_name=child.last_name,
            # Birth year only: the sealed export leaves the household,
            # so the full date of birth never rides along.
            birth_year=child.date_of_birth.year if child.date_of_birth else None,
            grade_level=child.grade_level,
            household_state=household.home_state,
            record_generated_at=datetime.now(UTC),
            methean_version=METHEAN_VERSION,
        ),
        transcript=TranscriptSection(
            grading_scale=transcript_data["grading_scale"],
            courses=[TranscriptCourse(**course) for course in transcript_data["courses"]],
            cumulative_hours=CumulativeHours(
                total_hours=hours["total_hours"],
                by_subject=hours["by_subject"],
            ),
        ),
        mastery_evidence=mastery_evidence,
        attendance=AttendanceSection(
            total_hours=hours["total_hours"],
            by_subject=hours["by_subject"],
        ),
        reading_log=reading_log,
        integrity=integrity,
    )


def record_content_hash(record: FamilyRecord) -> str:
    """Canonical content hash of a record, excluding generation metadata.

    record_generated_at varies per assembly; everything else is a pure
    function of the event-sourced record. Two assemblies with no
    intervening events therefore produce the same content hash, which
    is what the manifest certifies (the per-file hash of record.json
    additionally covers the generation timestamp).
    """
    payload = record.model_dump(mode="json")
    payload["identity"].pop("record_generated_at", None)
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _verification_md(manifest: dict) -> str:
    child_line = manifest["child"]
    head = manifest["chain_head_hash"] or "none (no governance events yet)"
    return f"""# How to verify this bundle

This ZIP is a METHEAN Family Record: the cumulative, evidence-backed
educational record for {child_line}, exported on {manifest["generated_at"]}.

## What is inside

- record.json: the full record. Every mastery claim lists the
  attempts, assessments, and parent governance decisions behind it.
- transcript.pdf and the other PDF documents: human-readable views of
  the same data.
- manifest.json: a fingerprint (SHA-256 hash) of every file above,
  plus the bundle hash described below.

## How the hashes work

A SHA-256 hash is a digital fingerprint: change a single character in
a file and its fingerprint changes completely. To check a file, hash
it with any standard tool (for example: `sha256sum record.json` on
most computers) and compare against the value in manifest.json.

The bundle hash at the bottom of manifest.json is computed from all
the file fingerprints together, combined with the chain head hash. If
it matches, nothing in this bundle has been altered since export.

## What the chain head hash means

Inside METHEAN, every parent governance decision (approving work,
overriding a result, exporting this record) is written to an
append-only log where each entry is cryptographically chained to the
one before it, like links that cannot be re-forged without breaking
every later link. The chain head hash in this bundle:

    {head}

is the latest link at the moment of export. The export action itself
was recorded into that same chain, so the family's METHEAN account
contains a permanent, tamper-evident receipt of this exact bundle.

## What this proves, and what it does not

It proves the record has not been modified since METHEAN exported it,
and that every claim in it traces to logged evidence. It does not, by
itself, prove the identity of the student; verify identity the same
way you would for any submitted document.
"""


async def build_record_bundle(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
) -> tuple[bytes, dict]:
    """Build the sealed export ZIP and its manifest.

    Pure assembly: no persistence happens here. The caller stores the
    bytes and logs the governance event.
    """
    record = await assemble_family_record(db, household_id, child_id)
    content_hash = record_content_hash(record)

    files: dict[str, bytes] = {}
    skipped: list[dict] = []

    record_payload = record.model_dump(mode="json")
    files["record.json"] = json.dumps(record_payload, indent=2, sort_keys=True, default=str).encode("utf-8")

    files["transcript.pdf"] = await generate_transcript(db, household_id, child_id)

    today = date.today()
    files["attendance.pdf"] = await generate_attendance_record(
        db, household_id, child_id, today - timedelta(days=365), today
    )

    # Compliance documents are included only when their required
    # inputs already exist; missing inputs are noted, never fatal.
    household_result = await db.execute(select(Household).where(Household.id == household_id))
    household = household_result.scalar_one()
    curricula_result = await db.execute(
        select(AnnualCurriculum.academic_year)
        .where(AnnualCurriculum.child_id == child_id, AnnualCurriculum.household_id == household_id)
        .order_by(AnnualCurriculum.academic_year.desc())
        .limit(1)
    )
    latest_year = curricula_result.scalar_one_or_none()

    if household.home_state and latest_year:
        try:
            files["ihip.pdf"] = await generate_ihip(db, household_id, child_id, household.home_state, latest_year)
        except Exception as exc:
            skipped.append({"name": "ihip.pdf", "reason": f"generation failed: {exc}"})
            logger.warning(
                "family_record_document_skipped",
                document="ihip.pdf",
                household_id=str(household_id),
                child_id=str(child_id),
                error=str(exc),
            )
    else:
        missing = []
        if not household.home_state:
            missing.append("household home_state")
        if not latest_year:
            missing.append("an annual curriculum")
        skipped.append({"name": "ihip.pdf", "reason": f"requires {' and '.join(missing)}"})

    # Quarterly reports need an explicit quarter selection, which the
    # sealed bundle has no basis to choose; always listed as skipped.
    skipped.append({"name": "quarterly_report.pdf", "reason": "requires explicit quarter selection"})

    generated_at = datetime.now(UTC).isoformat()
    birth = f" (b. {record.identity.birth_year})" if record.identity.birth_year else ""
    last = f" {record.identity.child_last_name}" if record.identity.child_last_name else ""
    manifest: dict = {
        "format": "methean-family-record-bundle/1",
        "generated_at": generated_at,
        "child": f"{record.identity.child_first_name}{last}{birth}",
        "household_state": record.identity.household_state,
        "methean_version": METHEAN_VERSION,
        "chain_head_hash": record.integrity.head_hash,
        "chain_verified": record.integrity.chain_verified,
        "chain_event_count": record.integrity.event_count,
        "content_hash": content_hash,
        "skipped_documents": skipped,
    }

    verification = _verification_md(manifest)
    files["VERIFICATION.md"] = verification.encode("utf-8")

    file_hashes = {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}
    manifest["files"] = file_hashes
    hash_lines = "".join(f"{name}:{file_hashes[name]}\n" for name in sorted(file_hashes))
    bundle_hash = hashlib.sha256((hash_lines + (record.integrity.head_hash or "GENESIS")).encode("utf-8")).hexdigest()
    manifest["bundle_hash"] = bundle_hash

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(files):
            zf.writestr(name, files[name])
        zf.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True))

    return buf.getvalue(), manifest


async def export_family_record(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    user_id: uuid.UUID,
) -> dict:
    """Build, store, and log a sealed Family Record export.

    The only writes in this module: the S3 object, the artifact row
    (mirroring the operations.py upload pattern), and the governance
    event that makes the export itself part of the immutable record.
    """
    bundle_bytes, manifest = await build_record_bundle(db, household_id, child_id)

    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    filename = f"FamilyRecord_{timestamp}.zip"
    s3_key = upload_artifact(
        file_bytes=bundle_bytes,
        filename=filename,
        content_type="application/zip",
        household_id=household_id,
        child_id=child_id,
    )

    artifact = Artifact(
        household_id=household_id,
        child_id=child_id,
        artifact_type=ArtifactType.document,
        title=filename,
        description="Sealed METHEAN Family Record bundle",
        s3_key=s3_key,
        mime_type="application/zip",
        file_size_bytes=len(bundle_bytes),
        metadata_={
            "kind": "family_record_bundle",
            "bundle_hash": manifest["bundle_hash"],
            "content_hash": manifest["content_hash"],
            "chain_head_hash": manifest["chain_head_hash"],
            "skipped_documents": manifest["skipped_documents"],
        },
    )
    db.add(artifact)
    await db.flush()

    await log_governance_event(
        db,
        household_id,
        user_id,
        GovernanceAction.approve,
        "family_record_exported",
        artifact.id,
        reason="Sealed Family Record bundle exported",
        metadata={
            "child_id": str(child_id),
            "bundle_hash": manifest["bundle_hash"],
            "content_hash": manifest["content_hash"],
            "chain_head_hash_at_export": manifest["chain_head_hash"],
        },
    )
    logger.info(
        "family_record_exported",
        household_id=str(household_id),
        child_id=str(child_id),
        artifact_id=str(artifact.id),
        bundle_hash=manifest["bundle_hash"],
        bundle_bytes=len(bundle_bytes),
    )

    download_url = get_presigned_url(s3_key, expires_in=DOWNLOAD_URL_EXPIRES_SECONDS)
    return {
        "bundle_hash": manifest["bundle_hash"],
        "content_hash": manifest["content_hash"],
        "download_url": download_url,
        "expires_in": DOWNLOAD_URL_EXPIRES_SECONDS,
        "artifact_id": artifact.id,
        "skipped_documents": manifest["skipped_documents"],
    }
