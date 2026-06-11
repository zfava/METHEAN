"""Tutor continuity: parent-governed, per-child tutor memory.

The tutor learns what works for each child (explanation styles,
motivators, pacing, interests) as abstracted strategy entries. The
parent's per-role autonomy policy decides how entries are written:

- off: no memory forms. The extraction step never runs, no calls,
  no data.
- standard: every proposed entry routes through parent review; nothing
  influences the tutor until the parent approves it.
- autonomous: entries apply immediately under the standing grant, each
  one citing the grant event's hash.

This module is the SINGLE writer of TutorProfileEntry rows, mirroring
the log_governance_event single-writer pattern and covered by the same
kind of guard test. The tutor reads the profile through context
assembly; it can never write it directly.

Privacy is structural, not aspirational: entries are abstracted
teaching strategies, never records of what the child said. The
validator below rejects quoted speech, clinical and diagnostic
language, and negative characterizations by construction (entries
describe what works), on every write path regardless of autonomy.
"""

import json
import re
import uuid
from datetime import UTC, datetime

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import GovernanceAction
from app.models.intelligence import TutorProfileEntry
from app.services.governance import (
    AI_AUTONOMY_AUTONOMOUS,
    AI_AUTONOMY_OFF,
    AI_AUTONOMY_STANDARD,
    get_active_autonomy_grant,
    get_ai_role_policy,
    log_governance_event,
)

logger = structlog.get_logger()

CATEGORIES = ("explanation_style", "motivation", "pacing", "interest", "other")

ENTRY_MAX_CHARS = 300

# Hard caps. At cap, new proposals are DROPPED with a log line; the
# system never silently evicts older entries. Pruning is the parent's
# act, not the system's.
MAX_ACTIVE_ENTRIES = 12
MAX_PENDING_PROPOSALS = 5

# Clinical and diagnostic vocabulary that must never appear in a tutor
# profile entry. Entries describe teaching strategies; they are not a
# medical chart, and METHEAN is not qualified to keep one. Matched as
# whole words, case-insensitive. Deliberately broad: a false rejection
# costs one proposal, a false acceptance costs trust.
CLINICAL_DENYLIST = (
    "adhd",
    "add",
    "asd",
    "autism",
    "autistic",
    "asperger",
    "aspergers",
    "dyslexia",
    "dyslexic",
    "dyscalculia",
    "dysgraphia",
    "dyspraxia",
    "disorder",
    "diagnosis",
    "diagnosed",
    "diagnostic",
    "deficit",
    "disability",
    "disabled",
    "impairment",
    "impaired",
    "syndrome",
    "medication",
    "medicated",
    "therapy",
    "therapist",
    "anxiety",
    "anxious",
    "depression",
    "depressed",
    "ocd",
    "ptsd",
    "trauma",
    "traumatized",
    "spectrum",
    "neurodivergent",
    "comorbid",
)

_DENYLIST_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(term) for term in CLINICAL_DENYLIST) + r")\b",
    re.IGNORECASE,
)

# Any double quotation mark, straight or curly. Strategy descriptions
# never need to quote anyone; a quote is the signature of verbatim
# child speech, which must never be persisted.
_QUOTE_PATTERN = re.compile(r'["“”„«»]')


class TutorProfileValidationError(ValueError):
    """An entry violated the structural privacy rules."""


class TutorProfileStateError(ValueError):
    """A decision was attempted on an entry in the wrong status."""


def validate_entry(category: str, content: str) -> None:
    """Structural privacy validator, applied on EVERY write path
    regardless of autonomy level. Raises TutorProfileValidationError."""
    if category not in CATEGORIES:
        raise TutorProfileValidationError(f"Unknown category '{category}'")
    if not content or not content.strip():
        raise TutorProfileValidationError("Entry content is empty")
    if len(content) > ENTRY_MAX_CHARS:
        raise TutorProfileValidationError(f"Entry exceeds {ENTRY_MAX_CHARS} characters")
    if _QUOTE_PATTERN.search(content):
        raise TutorProfileValidationError(
            "Entries may not contain quotation marks: strategies are abstracted, never verbatim speech"
        )
    match = _DENYLIST_PATTERN.search(content)
    if match:
        raise TutorProfileValidationError(
            f"Entries may not contain clinical or diagnostic language ('{match.group(0)}')"
        )


async def route_proposal(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    proposal: dict,
) -> TutorProfileEntry | None:
    """Route one extracted proposal according to the autonomy policy.

    Fail-closed: if the policy cannot be read, or the standing grant
    cannot be resolved while autonomous, the proposal is DROPPED and
    logged, never auto-applied. Returns the created entry or None when
    dropped.
    """
    category = str(proposal.get("category", ""))
    content = str(proposal.get("content", ""))

    try:
        policy = await get_ai_role_policy(db, household_id, "tutor")
    except Exception as exc:
        logger.warning(
            "tutor_profile_proposal_dropped",
            reason="policy_unreadable",
            household_id=str(household_id),
            child_id=str(child_id),
            error=str(exc),
        )
        return None

    if policy == AI_AUTONOMY_OFF:
        # Unreachable by design: extraction never runs at off. If we
        # got here anyway, drop loudly rather than form memory.
        logger.error(
            "tutor_profile_proposal_dropped",
            reason="policy_off_unreachable_path",
            household_id=str(household_id),
            child_id=str(child_id),
        )
        return None

    try:
        validate_entry(category, content)
    except TutorProfileValidationError as exc:
        logger.info(
            "tutor_profile_proposal_dropped",
            reason="validation",
            detail=str(exc),
            household_id=str(household_id),
            child_id=str(child_id),
        )
        return None

    active_count = (
        await db.execute(
            select(func.count())
            .select_from(TutorProfileEntry)
            .where(TutorProfileEntry.child_id == child_id, TutorProfileEntry.status == "active")
        )
    ).scalar() or 0
    pending_count = (
        await db.execute(
            select(func.count())
            .select_from(TutorProfileEntry)
            .where(TutorProfileEntry.child_id == child_id, TutorProfileEntry.status == "proposed")
        )
    ).scalar() or 0

    if policy == AI_AUTONOMY_AUTONOMOUS and active_count >= MAX_ACTIVE_ENTRIES:
        logger.info(
            "tutor_profile_proposal_dropped",
            reason="active_cap",
            cap=MAX_ACTIVE_ENTRIES,
            household_id=str(household_id),
            child_id=str(child_id),
        )
        return None
    if policy == AI_AUTONOMY_STANDARD and pending_count >= MAX_PENDING_PROPOSALS:
        logger.info(
            "tutor_profile_proposal_dropped",
            reason="pending_cap",
            cap=MAX_PENDING_PROPOSALS,
            household_id=str(household_id),
            child_id=str(child_id),
        )
        return None

    if policy == AI_AUTONOMY_AUTONOMOUS:
        try:
            grant_hash = await get_active_autonomy_grant(db, household_id, "tutor")
        except Exception as exc:
            logger.warning(
                "tutor_profile_proposal_dropped",
                reason="grant_unresolvable",
                household_id=str(household_id),
                child_id=str(child_id),
                error=str(exc),
            )
            return None
        if grant_hash is None:
            # Race with a revoke: the policy row said autonomous but no
            # standing grant is in force. Fail closed.
            logger.warning(
                "tutor_profile_proposal_dropped",
                reason="no_active_grant",
                household_id=str(household_id),
                child_id=str(child_id),
            )
            return None

        entry = TutorProfileEntry(
            household_id=household_id,
            child_id=child_id,
            category=category,
            content=content,
            status="active",
            grant_event_hash=grant_hash,
            decided_at=datetime.now(UTC),
            decided_by=None,
        )
        db.add(entry)
        await db.flush()
        await log_governance_event(
            db,
            household_id,
            None,
            GovernanceAction.modify,
            "tutor_profile_applied_autonomously",
            entry.id,
            reason=f"Tutor memory applied under standing grant: {content[:120]}",
            metadata={
                "child_id": str(child_id),
                "category": category,
                "grant_event_hash": grant_hash,
            },
        )
        logger.info(
            "tutor_profile_applied_autonomously",
            entry_id=str(entry.id),
            household_id=str(household_id),
            child_id=str(child_id),
            grant_event_hash=grant_hash,
        )
        return entry

    # standard: propose for parent review.
    entry = TutorProfileEntry(
        household_id=household_id,
        child_id=child_id,
        category=category,
        content=content,
        status="proposed",
    )
    db.add(entry)
    await db.flush()
    await log_governance_event(
        db,
        household_id,
        None,
        GovernanceAction.modify,
        "tutor_profile_proposed",
        entry.id,
        reason=f"Tutor proposed a memory entry for parent review: {content[:120]}",
        metadata={"child_id": str(child_id), "category": category},
    )
    logger.info(
        "tutor_profile_proposed",
        entry_id=str(entry.id),
        household_id=str(household_id),
        child_id=str(child_id),
    )
    return entry


async def decide_entry(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    entry_id: uuid.UUID,
    action: str,
    user_id: uuid.UUID,
) -> TutorProfileEntry:
    """Parent decision on a proposed entry: approve or reject.

    Only valid on status=proposed. Repeat decisions raise
    TutorProfileStateError, surfaced as 409: decided entries are
    immutable to further decisions (the record is the record).
    """
    if action not in ("approve", "reject"):
        raise TutorProfileValidationError("action must be approve or reject")

    entry = (
        await db.execute(
            select(TutorProfileEntry).where(
                TutorProfileEntry.id == entry_id,
                TutorProfileEntry.household_id == household_id,
                TutorProfileEntry.child_id == child_id,
            )
        )
    ).scalar_one_or_none()
    if entry is None:
        raise LookupError("Entry not found")
    if entry.status != "proposed":
        raise TutorProfileStateError(f"Entry is {entry.status}; only proposed entries can be decided")

    entry.status = "active" if action == "approve" else "rejected"
    entry.decided_at = datetime.now(UTC)
    entry.decided_by = user_id
    await db.flush()

    event_type = "tutor_profile_approved" if action == "approve" else "tutor_profile_rejected"
    await log_governance_event(
        db,
        household_id,
        user_id,
        GovernanceAction.approve if action == "approve" else GovernanceAction.reject,
        event_type,
        entry.id,
        reason=f"Parent {action}d tutor memory entry: {entry.content[:120]}",
        metadata={"child_id": str(child_id), "category": entry.category},
    )
    logger.info(
        event_type,
        entry_id=str(entry.id),
        household_id=str(household_id),
        child_id=str(child_id),
        user_id=str(user_id),
    )
    return entry


async def revoke_entry(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    entry_id: uuid.UUID,
    user_id: uuid.UUID,
) -> TutorProfileEntry:
    """Revoke an active entry. Only valid on status=active. Revoked
    entries are never injected and never deleted."""
    entry = (
        await db.execute(
            select(TutorProfileEntry).where(
                TutorProfileEntry.id == entry_id,
                TutorProfileEntry.household_id == household_id,
                TutorProfileEntry.child_id == child_id,
            )
        )
    ).scalar_one_or_none()
    if entry is None:
        raise LookupError("Entry not found")
    if entry.status != "active":
        raise TutorProfileStateError(f"Entry is {entry.status}; only active entries can be revoked")

    entry.status = "revoked"
    entry.decided_at = datetime.now(UTC)
    entry.decided_by = user_id
    await db.flush()

    await log_governance_event(
        db,
        household_id,
        user_id,
        GovernanceAction.modify,
        "tutor_profile_entry_revoked",
        entry.id,
        reason=f"Parent revoked tutor memory entry: {entry.content[:120]}",
        metadata={"child_id": str(child_id), "category": entry.category},
    )
    logger.info(
        "tutor_profile_entry_revoked",
        entry_id=str(entry.id),
        household_id=str(household_id),
        child_id=str(child_id),
        user_id=str(user_id),
    )
    return entry


async def list_entries(db: AsyncSession, household_id: uuid.UUID, child_id: uuid.UUID) -> list[TutorProfileEntry]:
    result = await db.execute(
        select(TutorProfileEntry)
        .where(
            TutorProfileEntry.household_id == household_id,
            TutorProfileEntry.child_id == child_id,
        )
        .order_by(TutorProfileEntry.proposed_at.desc())
    )
    return list(result.scalars().all())


async def get_active_entries_block(db: AsyncSession, household_id: uuid.UUID, child_id: uuid.UUID) -> str:
    """The guidance block injected into tutor context.

    Empty string when the policy is off (the tutor starts fresh every
    session) or when nothing is active. Entries influence tone and
    approach only; they are never presented as facts about mastery.
    """
    policy = await get_ai_role_policy(db, household_id, "tutor")
    if policy == AI_AUTONOMY_OFF:
        return ""

    result = await db.execute(
        select(TutorProfileEntry)
        .where(
            TutorProfileEntry.household_id == household_id,
            TutorProfileEntry.child_id == child_id,
            TutorProfileEntry.status == "active",
        )
        .order_by(
            TutorProfileEntry.decided_at.desc().nulls_last(),
            TutorProfileEntry.proposed_at.desc(),
        )
        .limit(8)
    )
    entries = list(result.scalars().all())
    if not entries:
        return ""

    lines = [f"- ({e.category.replace('_', ' ')}) {e.content}" for e in entries]
    return (
        "WHAT WORKS FOR THIS LEARNER (parent-governed tutor memory; "
        "guidance for tone and approach only, never facts about mastery):\n" + "\n".join(lines)
    )


_EXTRACTION_PROMPT = """Review this tutoring exchange and identify zero to two reusable teaching strategies that clearly worked for this learner.

Rules, all mandatory:
- Each strategy is an abstracted observation about HOW to teach this learner, never WHAT they said.
- Never quote the learner. Never include names. Never use clinical, diagnostic, or deficit language.
- Describe what works, never what is wrong with the learner.
- category must be one of: explanation_style, motivation, pacing, interest, other.
- content is one sentence, maximum 250 characters.
- Only include a strategy if the exchange gives real evidence for it. Zero strategies is a good answer.

Respond with STRICT JSON only: {"proposals": [{"category": "...", "content": "...", "confidence": 0.0}]}

Exchange summary:
"""


async def extract_and_route_proposals(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    exchange_text: str,
    triggered_by: uuid.UUID | None = None,
) -> list[TutorProfileEntry]:
    """Post-exchange extraction step.

    Runs one bounded extraction call through the tutor role's normal
    budget, then routes each well-formed candidate. When the policy is
    off this returns immediately: no calls, no data. Anything malformed
    is discarded, never repaired.
    """
    policy = await get_ai_role_policy(db, household_id, "tutor")
    if policy == AI_AUTONOMY_OFF:
        return []

    from app.ai.gateway import AIRole, call_ai

    try:
        result = await call_ai(
            db,
            AIRole.tutor,
            "You distill tutoring exchanges into abstracted teaching strategies. You output strict JSON only.",
            _EXTRACTION_PROMPT + exchange_text[:2000],
            household_id,
            triggered_by=triggered_by,
            expected_json=True,
            max_tokens=300,
        )
    except Exception as exc:
        logger.info(
            "tutor_profile_extraction_skipped",
            reason=str(exc)[:200],
            household_id=str(household_id),
            child_id=str(child_id),
        )
        return []

    output = result.get("output")
    if isinstance(output, str):
        try:
            output = json.loads(output)
        except json.JSONDecodeError:
            output = None
    proposals = output.get("proposals") if isinstance(output, dict) else None
    if not isinstance(proposals, list):
        logger.info(
            "tutor_profile_extraction_discarded",
            reason="malformed_output",
            household_id=str(household_id),
            child_id=str(child_id),
        )
        return []

    created: list[TutorProfileEntry] = []
    for candidate in proposals[:2]:
        if not isinstance(candidate, dict):
            continue
        entry = await route_proposal(db, household_id, child_id, candidate)
        if entry is not None:
            created.append(entry)
    return created
