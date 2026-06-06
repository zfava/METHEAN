"""Governed-agency child choice routing.

PARENT-FINAL, CURRICULUM-AUTHORED, READINESS-INFORMED child choice.

This is the runtime companion to the optional ``choice_space`` block on a
node (see ``node_content.py``). It mirrors the existing AI input/oversight
dial: where that dial lets a parent tune AI autonomy per household via a
JSONB key (``philosophical_profile.ai_autonomy_level``) routed through the
governance layer, this lets a parent tune CHILD choice latitude per child
via a JSONB key (``ChildPreferences.personalization.child_choice_latitude``)
routed through the SAME governance event log. No parallel mechanism is
introduced.

Three roles, one governance primitive:

- CHILD PROPOSES within the bounded, all-acceptable ``choice_space``
  (never an open field).
- SYSTEM INFORMS: every proposal and its resolution is captured as an
  immutable governance event carrying child / node / option / outcome /
  timestamp, which is exactly what a FUTURE readiness service will read to
  derive a per-child, per-class readiness signal. The inference itself is
  NOT built here; only the events it will consume are captured.
- PARENT APPROVES: the parent is the final authority. Per choice class the
  parent can WIDEN (auto), TIGHTEN (review), or DISABLE the author default.
  Auto-class proposals apply immediately; review-class proposals queue for
  parent approval and DO NOT mutate any child learning state until approved.

This module is additive: it only reads the existing ``choice_space`` block
and writes through the existing ``log_governance_event`` path using a new
governance event TYPE (the ``target_type`` string ``child_choice_proposal``).
It does not modify governance core behavior on any existing event type.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import GovernanceAction
from app.models.governance import GovernanceEvent
from app.services.governance import log_governance_event
from app.services.node_content import (
    CHOICE_LATITUDES,
    choice_space_is_valid,
)

# The new governance event TYPE. It plugs into the existing immutable
# governance_events log purely as the free-form ``target_type`` string; no
# enum, table, or evaluate_activity branch is changed. This is the
# additive seam.
CHILD_CHOICE_PROPOSAL = "child_choice_proposal"

# The per-child JSONB key where parent-set choice latitude lives, inside
# ``ChildPreferences.personalization``. It mirrors how the AI dial lives in
# ``Household.philosophical_profile['ai_autonomy_level']``. Shape: a dict
# mapping choice class -> one of CHOICE_LATITUDES.
CHILD_CHOICE_LATITUDE_KEY = "child_choice_latitude"

# Safe default latitude when neither the parent nor the author has set
# anything resolvable: review (parent sees it before it takes effect).
_SAFE_DEFAULT_LATITUDE = "review"


@dataclass
class ChildChoiceOutcome:
    """Result of routing a child choice proposal.

    ``status`` is one of:
    - "applied": auto-class proposal accepted and applied immediately.
    - "queued": review-class proposal waiting for parent approval; the
      child sees "waiting for approval" and no learning state changes.
    - "rejected": the class is disabled by the parent, or the option is
      not in the bounded proposable set.

    ``state_mutated`` is always False from this module: a bounded child
    choice never mutates child learning state (mastery/progress). Applying
    an auto choice (e.g. honoring a chosen order or variant) is a
    downstream planner concern; the consequential decisions that WOULD
    change learning state are excluded from choice_space by construction.
    """

    status: str
    latitude: str
    event_id: uuid.UUID | None
    reason: str
    state_mutated: bool = False


def get_parent_latitude(personalization: dict | None) -> dict:
    """Read the per-child parent latitude map from a ChildPreferences
    personalization dict. Returns {} when unset, exactly mirroring how the
    AI dial defaults when ``ai_autonomy_level`` is absent.
    """
    if not isinstance(personalization, dict):
        return {}
    latitude = personalization.get(CHILD_CHOICE_LATITUDE_KEY)
    return latitude if isinstance(latitude, dict) else {}


def _author_default_for_class(choice_space: dict, choice_class: str) -> str:
    default = choice_space.get("author_default_latitude")
    if isinstance(default, dict):
        value = default.get(choice_class)
    elif isinstance(default, str):
        value = default
    else:
        value = None
    return value if value in CHOICE_LATITUDES else _SAFE_DEFAULT_LATITUDE


def resolve_latitude(choice_space: dict, parent_latitude: dict | None, choice_class: str) -> str:
    """Resolve the effective latitude for a choice class.

    Parent latitude WINS over the author default for that class (widen /
    tighten / disable). When the parent has set nothing for the class, the
    node's author_default_latitude applies. When neither resolves to a
    known latitude, the safe default (review) applies.
    """
    if parent_latitude:
        parent_value = parent_latitude.get(choice_class)
        if parent_value in CHOICE_LATITUDES:
            return parent_value
    return _author_default_for_class(choice_space, choice_class)


def is_option_proposable(choice_space: dict, choice_class: str, option: str) -> bool:
    """True iff (choice_class, option) is in the bounded proposable set.

    This enforces the "never an open field" rule: a child may only propose
    options the curriculum authority listed as all-acceptable.
    """
    proposable = choice_space.get("proposable")
    if not isinstance(proposable, list):
        return False
    for entry in proposable:
        if not isinstance(entry, dict):
            continue
        if entry.get("class") == choice_class and entry.get("option") == option:
            return True
    return False


def _proposal_metadata(
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    choice_class: str,
    option: str,
    latitude: str,
    outcome: str,
    proposal_event_id: uuid.UUID | None = None,
) -> dict:
    """Build the immutable governance event metadata.

    Carries everything a future readiness service needs to derive a
    per-child, per-class signal from event history: which child, which
    node, which class, which option, the latitude in force, and the
    outcome. The event's own created_at supplies the timestamp.
    """
    meta = {
        "source": "child_choice",
        "child_id": str(child_id),
        "node_id": str(node_id),
        "choice_class": choice_class,
        "option": option,
        "latitude": latitude,
        "outcome": outcome,
    }
    if proposal_event_id is not None:
        meta["proposal_event_id"] = str(proposal_event_id)
    return meta


async def propose_child_choice(
    db: AsyncSession,
    *,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    node_content: dict,
    choice_class: str,
    option: str,
    parent_latitude: dict | None = None,
) -> ChildChoiceOutcome:
    """Route a child's choice proposal through governance.

    Preconditions:
    - the node must carry a valid choice_space (raises ValueError
      otherwise: a node with no valid choice_space offers no choice and a
      proposal against it is a programming error, not a child action).

    Routing (parent latitude overriding the author default per class):
    - option not in the bounded proposable set -> rejected, NO event (it
      was never a legitimate, offered choice).
    - latitude "disabled" -> rejected (parent removed proposability for
      this class), event logged (action=reject), NO state mutation.
    - latitude "review" -> queued for parent (action=defer), child waits,
      NO state mutation until approved.
    - latitude "auto" -> applied immediately (action=approve), NO learning
      state mutation (the bounded choice is non-consequential).
    """
    choice_space = node_content.get("choice_space")
    if not isinstance(choice_space, dict) or not choice_space_is_valid(node_content):
        raise ValueError("node has no valid choice_space; nothing is child-proposable")

    if not is_option_proposable(choice_space, choice_class, option):
        return ChildChoiceOutcome(
            status="rejected",
            latitude="n/a",
            event_id=None,
            reason=(
                f"option {option!r} is not in the bounded proposable set for class "
                f"{choice_class!r}; child choice is never an open field"
            ),
        )

    latitude = resolve_latitude(choice_space, parent_latitude, choice_class)

    if latitude == "disabled":
        event = await log_governance_event(
            db,
            household_id=household_id,
            user_id=None,
            action=GovernanceAction.reject,
            target_type=CHILD_CHOICE_PROPOSAL,
            target_id=node_id,
            reason=f"child choice class {choice_class!r} is disabled by the parent",
            metadata=_proposal_metadata(child_id, node_id, choice_class, option, latitude, outcome="rejected_disabled"),
        )
        return ChildChoiceOutcome(
            status="rejected",
            latitude=latitude,
            event_id=event.id,
            reason=f"choice class {choice_class!r} disabled by parent",
        )

    if latitude == "review":
        event = await log_governance_event(
            db,
            household_id=household_id,
            user_id=None,
            action=GovernanceAction.defer,
            target_type=CHILD_CHOICE_PROPOSAL,
            target_id=node_id,
            reason=f"child proposed {option!r} ({choice_class}); queued for parent review",
            metadata=_proposal_metadata(child_id, node_id, choice_class, option, latitude, outcome="queued"),
        )
        return ChildChoiceOutcome(
            status="queued",
            latitude=latitude,
            event_id=event.id,
            reason="waiting for approval",
        )

    # latitude == "auto"
    event = await log_governance_event(
        db,
        household_id=household_id,
        user_id=None,
        action=GovernanceAction.approve,
        target_type=CHILD_CHOICE_PROPOSAL,
        target_id=node_id,
        reason=f"child proposed {option!r} ({choice_class}); auto-approved by parent latitude",
        metadata=_proposal_metadata(child_id, node_id, choice_class, option, latitude, outcome="applied"),
    )
    return ChildChoiceOutcome(
        status="applied",
        latitude=latitude,
        event_id=event.id,
        reason="auto-approved",
    )


async def resolve_pending_choice(
    db: AsyncSession,
    *,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    node_id: uuid.UUID,
    choice_class: str,
    option: str,
    approve: bool,
    user_id: uuid.UUID | None,
    proposal_event_id: uuid.UUID | None = None,
) -> ChildChoiceOutcome:
    """Record a parent's decision on a queued (review-class) proposal.

    Emits a second immutable governance event (action=approve or
    action=reject) carrying the same child / node / option metadata, linked
    to the originating proposal event. This is the parent-final step. It
    does not mutate child learning state here; honoring an approved bounded
    choice is a downstream planner concern.
    """
    action = GovernanceAction.approve if approve else GovernanceAction.reject
    outcome = "approved" if approve else "rejected"
    event = await log_governance_event(
        db,
        household_id=household_id,
        user_id=user_id,
        action=action,
        target_type=CHILD_CHOICE_PROPOSAL,
        target_id=node_id,
        reason=f"parent {outcome} child proposal {option!r} ({choice_class})",
        metadata=_proposal_metadata(
            child_id,
            node_id,
            choice_class,
            option,
            latitude="review",
            outcome=outcome,
            proposal_event_id=proposal_event_id,
        ),
    )
    return ChildChoiceOutcome(
        status="applied" if approve else "rejected",
        latitude="review",
        event_id=event.id,
        reason=f"parent {outcome}",
    )


async def pending_proposals_for_child(
    db: AsyncSession,
    *,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
) -> list[GovernanceEvent]:
    """Return queued (review-class) child choice proposals for a child.

    A thin read helper over the immutable governance log: queued
    proposals are events of type child_choice_proposal whose metadata
    outcome is "queued" for this child. (Whether each has since been
    resolved is derivable from later events; the future readiness service
    and any parent queue UI build on this same log.)
    """
    from sqlalchemy import select

    result = await db.execute(
        select(GovernanceEvent)
        .where(GovernanceEvent.household_id == household_id)
        .where(GovernanceEvent.target_type == CHILD_CHOICE_PROPOSAL)
        .order_by(GovernanceEvent.created_at.asc())
    )
    events = result.scalars().all()
    return [
        e
        for e in events
        if (e.metadata_ or {}).get("child_id") == str(child_id) and (e.metadata_ or {}).get("outcome") == "queued"
    ]
