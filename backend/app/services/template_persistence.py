"""Shared from-template persistence.

This is the single mechanism that lands a code-defined ``Template`` (from
``templates.py`` and its registered libraries) into the database as a
``Subject`` + ``LearningMap`` + ``LearningNode`` rows (new UUIDs) + edges,
injecting any pre-enriched content module keyed by node ref.

It was extracted verbatim from the ``POST /learning-maps/from-template``
endpoint so that both the HTTP path and the namespace resolver create nodes
through *one* code path (no second, divergent persistence path). The only
behavioral addition is that each node now records ``source_ref`` (the
template node ref, e.g. ``"mf-01"``) so a node can be found again by its
content id, which is what makes resolver-driven persistence idempotent.

Background enrichment queueing intentionally stays with the API caller; this
helper performs only the synchronous DB work.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import LearningEdge, LearningMap, LearningNode, Subject
from app.services.dag_engine import rebuild_closure_for_map
from app.services.templates import Template


@dataclass
class TemplateApplication:
    """Result of materializing a template into a household's database."""

    learning_map_id: uuid.UUID
    subject_id: uuid.UUID
    ref_to_uuid: dict[str, uuid.UUID]
    node_count: int
    edge_count: int


def _inject_pre_enriched_content(template: Template, ref: str) -> dict | None:
    """Return the pre-enriched content payload for a template node ref, if a
    matching content module is authored. Mirrors the per-template lookups in
    the original copy_template endpoint."""
    try:
        from app.content.math_foundational_content import MATH_FOUNDATIONAL_CONTENT

        if template.template_id == "math-foundational" and ref in MATH_FOUNDATIONAL_CONTENT:
            return MATH_FOUNDATIONAL_CONTENT[ref]
    except ImportError:
        pass
    try:
        from app.content.reading_foundational_content import READING_FOUNDATIONAL_CONTENT

        if template.template_id == "reading-foundational" and ref in READING_FOUNDATIONAL_CONTENT:
            return READING_FOUNDATIONAL_CONTENT[ref]
    except ImportError:
        pass
    try:
        from app.content.history_foundational_content import HISTORY_FOUNDATIONAL_CONTENT

        if template.template_id == "history-foundational" and ref in HISTORY_FOUNDATIONAL_CONTENT:
            return HISTORY_FOUNDATIONAL_CONTENT[ref]
    except ImportError:
        pass
    try:
        from app.content.writing_foundational_content import WRITING_FOUNDATIONAL_CONTENT

        if template.template_id == "writing-foundational" and ref in WRITING_FOUNDATIONAL_CONTENT:
            return WRITING_FOUNDATIONAL_CONTENT[ref]
    except ImportError:
        pass
    try:
        from app.content.science_foundational_content import SCIENCE_FOUNDATIONAL_CONTENT

        if template.template_id == "science-foundational" and ref in SCIENCE_FOUNDATIONAL_CONTENT:
            return SCIENCE_FOUNDATIONAL_CONTENT[ref]
    except ImportError:
        pass
    return None


async def apply_template(
    db: AsyncSession,
    template: Template,
    household_id: uuid.UUID,
) -> TemplateApplication:
    """Deep-copy a template into a new Subject + LearningMap for a household.

    Creates a fresh Subject and LearningMap, copies every TemplateNode into a
    LearningNode with a new UUID (recording ``source_ref``), injects any
    pre-enriched content module payload, wires edges, and rebuilds the
    transitive closure. Returns the new ids plus the ref -> uuid map.
    """
    # Create subject
    subject = Subject(
        household_id=household_id,
        name=template.subject_name,
        color=template.subject_color,
        description=template.description,
    )
    db.add(subject)
    await db.flush()

    # Create learning map
    lmap = LearningMap(
        household_id=household_id,
        subject_id=subject.id,
        name=template.name,
        description=template.description,
    )
    db.add(lmap)
    await db.flush()

    # Create nodes with new UUIDs, maintain ref -> uuid mapping
    ref_to_uuid: dict[str, uuid.UUID] = {}
    for tnode in template.nodes:
        node = LearningNode(
            learning_map_id=lmap.id,
            household_id=household_id,
            node_type=tnode.node_type,
            title=tnode.title,
            description=tnode.description,
            estimated_minutes=tnode.estimated_minutes,
            sort_order=tnode.sort_order,
            source_ref=tnode.ref,
        )
        db.add(node)
        await db.flush()
        ref_to_uuid[tnode.ref] = node.id

        # Inline content on the template node takes precedence.
        if tnode.content is not None:
            node.content = tnode.content

        # Inject pre-enriched content module payload if available.
        enriched = _inject_pre_enriched_content(template, tnode.ref)
        if enriched is not None:
            node.content = enriched

    # Create edges
    edge_count = 0
    for tedge in template.edges:
        from_id = ref_to_uuid[tedge.from_ref]
        to_id = ref_to_uuid[tedge.to_ref]
        edge = LearningEdge(
            learning_map_id=lmap.id,
            household_id=household_id,
            from_node_id=from_id,
            to_node_id=to_id,
            relation=tedge.relation,
        )
        db.add(edge)
        edge_count += 1

    await db.flush()

    # Build transitive closure for the new map
    await rebuild_closure_for_map(db, lmap.id)

    return TemplateApplication(
        learning_map_id=lmap.id,
        subject_id=subject.id,
        ref_to_uuid=ref_to_uuid,
        node_count=len(template.nodes),
        edge_count=edge_count,
    )
