"""Pydantic v2 schemas for the METHEAN Family Record.

The Family Record is a read-only lens over the event-sourced learner
record: every mastery claim carries its evidence chain (attempts,
assessments, governance events with their hash-chain entries), so the
record is verifiable against the household's tamper-evident audit
chain rather than asserted by authority.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel


class IdentitySection(BaseModel):
    child_first_name: str
    child_last_name: str | None
    birth_year: int | None
    grade_level: str | None
    household_state: str | None
    record_generated_at: datetime
    methean_version: str


class TranscriptCourse(BaseModel):
    academic_year: str
    subject_name: str
    grade_level: str | None
    status: str
    weeks_completed: int
    total_weeks: int | None
    hours_per_week: float | None
    overall_mastery: str | None
    translated_grade: str | None = None


class CumulativeHours(BaseModel):
    total_hours: float
    by_subject: dict[str, float]


class TranscriptSection(BaseModel):
    grading_scale: str
    courses: list[TranscriptCourse]
    cumulative_hours: CumulativeHours


class EvidenceAttempt(BaseModel):
    id: uuid.UUID
    activity_id: uuid.UUID
    activity_title: str | None
    status: str
    score: float | None
    started_at: datetime | None
    completed_at: datetime | None
    duration_minutes: int | None


class EvidenceAssessment(BaseModel):
    id: uuid.UUID
    assessment_type: str
    title: str
    mastery_judgment: str | None
    assessed_at: datetime | None


class EvidenceGovernanceEvent(BaseModel):
    id: uuid.UUID
    action: str
    target_type: str
    target_id: uuid.UUID
    reason: str | None
    created_at: datetime
    # The hash-chain entry (migration 052) that makes this event
    # tamper-evident: recomputable from the event payload and the
    # previous event's hash.
    event_hash: str | None
    prev_event_hash: str | None


class MasteryEvidence(BaseModel):
    node_id: uuid.UUID
    node_title: str
    node_type: str
    subject: str | None
    mastery_level: str
    achieved_at: datetime | None
    fsrs_stability: float | None
    attempts: list[EvidenceAttempt]
    assessments: list[EvidenceAssessment]
    governance_events: list[EvidenceGovernanceEvent]


class AttendanceSection(BaseModel):
    total_hours: float
    by_subject: dict[str, float]


class ReadingLogItem(BaseModel):
    title: str
    author: str | None
    genre: str | None
    status: str | None
    pages_read: int | None
    pages_total: int | None
    child_rating: int | None


class IntegritySection(BaseModel):
    head_hash: str | None
    chain_verified: bool
    event_count: int


class FamilyRecord(BaseModel):
    format: str = "methean-family-record/1"
    identity: IdentitySection
    transcript: TranscriptSection
    mastery_evidence: list[MasteryEvidence]
    attendance: AttendanceSection
    reading_log: list[ReadingLogItem]
    integrity: IntegritySection


class ExportResponse(BaseModel):
    bundle_hash: str
    content_hash: str
    download_url: str | None
    expires_in: int
    artifact_id: uuid.UUID
    skipped_documents: list[dict]


class ExportListItem(BaseModel):
    artifact_id: uuid.UUID
    child_id: uuid.UUID
    title: str
    bundle_hash: str | None
    content_hash: str | None
    created_at: datetime | None
    file_size_bytes: int | None
