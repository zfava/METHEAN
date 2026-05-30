"""Deterministic resolver across the three node-id namespaces.

The curriculum stack carries the same pedagogical node under three different
id schemes (see docs/curriculum_pipeline_audit.md):

1. scope_sequences ref   e.g. ``"math_f_01"``   (``{subject}_{level}_{NN}``)
2. content-module id      e.g. ``"mf-01"``       (``{initial}{level}-{NN}``)
3. persisted LearningNode  a database UUID

This module is the SINGLE SOURCE OF TRUTH for translating between them.
Nothing else may hardcode a ref<->content-id or ref<->uuid mapping.

Layers:
- ``resolve_ref_to_content_id`` / ``resolve_content_id_to_ref`` are pure
  string translation. The academic mapping is *derived* mechanically; it is
  never hand-maintained per node. Non-mechanical refs are listed as explicit
  exceptions below.
- ``resolve_content_id_to_uuid`` persists the content node (idempotently)
  through the existing from-template mechanism and returns its UUID, or a
  structured ``Unresolved`` record when no template owns the content id yet
  (this is what lets a partial content library still be generated against).
"""

import re
import uuid
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningNode
from app.services.template_persistence import apply_template
from app.services.templates import TEMPLATES

# ── Mechanical academic mapping ──────────────────────────────────────────
#
# scope ref ``{subject}_{level}_{NN}``  <->  content id ``{initial}{level}-{NN}``
#
# The subject token differs between the two schemes (scope uses a 3-4 letter
# abbreviation, content uses a single initial). That single mapping is the
# only thing that is not literally identical between the two ids, so it is
# the only thing we encode. Everything else (level letter, ordinal) is
# carried through unchanged.

SUBJECT_ABBR_TO_INITIAL: dict[str, str] = {
    "math": "m",
    "read": "r",
    "sci": "s",
    "hist": "h",
    "writ": "w",
}
INITIAL_TO_SUBJECT_ABBR: dict[str, str] = {v: k for k, v in SUBJECT_ABBR_TO_INITIAL.items()}

# Known level letters: foundational, developing, intermediate, mastery,
# advanced. Constraining the level token to this set is what keeps vocational
# ids like "ws-001" (woodworking) from being mis-read as academic "writ_s".
_LEVELS = "fdima"
# scope ref: math_f_01, sci_d_12, read_i_03 ...
_ACADEMIC_REF_RE = re.compile(rf"^([a-z]+)_([{_LEVELS}])_(\d+)$")
# content id: mf-01, rd-12, sh-03 ... (single subject initial + level letter)
_ACADEMIC_CONTENT_RE = re.compile(rf"^([mrshw])([{_LEVELS}])-(\d+)$")

# ── Vocational namespace ─────────────────────────────────────────────────
#
# Vocational content ids use a ``<slug>-root`` / ``<abbr>-NNN`` form and have
# no scope_sequences counterpart (scope_sequences defines academic subjects
# only). For these the ref and the content id are the SAME string, so the
# translation is the identity. Detection is data-driven from the known
# vocational module prefixes plus the documented ``-root`` form.

VOCATIONAL_PREFIXES: frozenset[str] = frozenset(
    {
        "el",
        "els",
        "elc",  # electrical
        "gardening",
        "gs",
        "gc",  # gardening
        "hvac",
        "hs",
        "hc",  # hvac
        "woodworking",
        "ws",
        "wc",  # woodworking
    }
)

# ── Explicit non-mechanical exceptions ───────────────────────────────────
#
# Refs whose two ids do NOT relate by the mechanical academic rule and are
# therefore deliberately left unmapped here until they are wired explicitly:
#
#   literature: scope refs ``lit_{level}_{NN}`` vs content ids
#               ``lit-craft-{NNN}``. The "craft" infix and 3-digit ordinal
#               are not a positional transform of the scope ref, and the
#               per-node correspondence is not 1:1-by-order in the data, so
#               we do not guess it. ``resolve_*`` returns ``None`` for the
#               ``lit`` family rather than inventing a mapping.
NON_MECHANICAL_EXCEPTIONS: frozenset[str] = frozenset({"lit"})


def _is_vocational(token: str) -> bool:
    if token.endswith("-root"):
        return True
    return token.split("-", 1)[0] in VOCATIONAL_PREFIXES


def resolve_ref_to_content_id(ref: str) -> str | None:
    """scope_sequences ref -> content-module id.

    Returns ``None`` for refs that have no mechanical content-id counterpart
    (e.g. the literature exception) and for ids that are not refs.
    """
    m = _ACADEMIC_REF_RE.match(ref)
    if m:
        abbr, level, ordinal = m.groups()
        initial = SUBJECT_ABBR_TO_INITIAL.get(abbr)
        if initial is None:
            # Recognized ref shape but a non-mechanical subject (e.g. "lit").
            return None
        return f"{initial}{level}-{ordinal}"
    if _is_vocational(ref):
        return ref  # identity: vocational ref == content id
    return None


def resolve_content_id_to_ref(content_id: str) -> str | None:
    """content-module id -> scope_sequences ref (inverse of the above)."""
    m = _ACADEMIC_CONTENT_RE.match(content_id)
    if m:
        initial, level, ordinal = m.groups()
        abbr = INITIAL_TO_SUBJECT_ABBR.get(initial)
        if abbr is None:
            return None
        return f"{abbr}_{level}_{ordinal}"
    if _is_vocational(content_id):
        return content_id  # identity
    return None


# ── Persistence resolution ───────────────────────────────────────────────


@dataclass(frozen=True)
class Unresolved:
    """Structured record describing why a content id could not be persisted.

    reason:
        "no_template"     no code-defined template owns this content id yet
        "not_in_template" template matched but did not yield the node
        "unmapped_ref"    a ref that has no content-id counterpart
    """

    content_id: str
    reason: str
    detail: str


@dataclass
class ContentResolution:
    """Outcome of ``resolve_content_id_to_uuid``.

    On success ``node_uuid`` is set and ``unresolved`` is ``None``. On
    failure ``node_uuid`` is ``None`` and ``unresolved`` carries the reason.
    """

    content_id: str
    node_uuid: uuid.UUID | None
    created: bool
    unresolved: Unresolved | None


def template_for_content_id(content_id: str):
    """Return the first registered template that owns a node with this ref.

    Reuses the global TEMPLATES registry; no separate mapping is maintained.
    """
    for template in TEMPLATES.values():
        for node in template.nodes:
            if node.ref == content_id:
                return template
    return None


async def resolve_content_id_to_uuid(
    db: AsyncSession,
    content_id: str,
    household_id: uuid.UUID,
) -> ContentResolution:
    """Resolve a content-module id to a persisted LearningNode UUID.

    Idempotent: if a node with this ``source_ref`` already exists for the
    household it is returned unchanged. Otherwise the owning template is
    materialized through the shared from-template path (``apply_template``)
    and the freshly persisted node's UUID is returned.

    If no template owns the content id, returns a ``ContentResolution`` with
    ``node_uuid is None`` and an ``Unresolved`` record (no exception), so a
    partial content library can still be generated against.
    """
    # 1. Idempotency: already persisted for this household?
    existing = (
        (
            await db.execute(
                select(LearningNode)
                .where(
                    LearningNode.source_ref == content_id,
                    LearningNode.household_id == household_id,
                    LearningNode.is_active.is_(True),
                )
                .order_by(LearningNode.created_at, LearningNode.id)
                .limit(1)
            )
        )
        .scalars()
        .first()
    )
    if existing is not None:
        return ContentResolution(content_id, existing.id, created=False, unresolved=None)

    # 2. Find the owning template.
    template = template_for_content_id(content_id)
    if template is None:
        return ContentResolution(
            content_id,
            None,
            created=False,
            unresolved=Unresolved(
                content_id,
                "no_template",
                "No code-defined template owns this content id; nothing to persist yet.",
            ),
        )

    # 3. Persist through the single shared from-template mechanism.
    application = await apply_template(db, template, household_id)
    node_uuid = application.ref_to_uuid.get(content_id)
    if node_uuid is None:
        return ContentResolution(
            content_id,
            None,
            created=False,
            unresolved=Unresolved(
                content_id,
                "not_in_template",
                f"Template '{template.template_id}' did not yield node '{content_id}'.",
            ),
        )
    return ContentResolution(content_id, node_uuid, created=True, unresolved=None)


async def resolve_ref_to_uuid(
    db: AsyncSession,
    ref: str,
    household_id: uuid.UUID,
) -> ContentResolution:
    """Convenience: scope ref -> content id -> persisted UUID in one call.

    Returns an ``unmapped_ref`` ``Unresolved`` when the ref has no content-id
    counterpart (e.g. the literature exception), without persisting anything.
    """
    content_id = resolve_ref_to_content_id(ref)
    if content_id is None:
        return ContentResolution(
            ref,
            None,
            created=False,
            unresolved=Unresolved(ref, "unmapped_ref", f"Ref '{ref}' has no content-id counterpart."),
        )
    return await resolve_content_id_to_uuid(db, content_id, household_id)
