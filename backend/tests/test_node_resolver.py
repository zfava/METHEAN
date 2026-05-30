"""Tests for the native node-id namespace resolver.

Covers the three namespaces from docs/curriculum_pipeline_audit.md:
scope ref ("math_f_01") <-> content id ("mf-01") <-> persisted UUID.
"""

import pytest
from sqlalchemy import func, select

from app.api import curriculum as curriculum_api
from app.content.math_foundational_content import MATH_FOUNDATIONAL_CONTENT
from app.models.curriculum import LearningMap, LearningNode
from app.services import node_resolver, template_persistence
from app.services.node_resolver import (
    resolve_content_id_to_ref,
    resolve_content_id_to_uuid,
    resolve_ref_to_content_id,
    resolve_ref_to_uuid,
)
from app.services.templates import MATH_FOUNDATIONAL

# (namespace prefix, scope ref, content id). Vocational rows are identity.
NAMESPACE_CASES = [
    ("mf", "math_f_01", "mf-01"),
    ("md", "math_d_01", "md-01"),
    ("rf", "read_f_01", "rf-01"),
    ("rd", "read_d_01", "rd-01"),
    ("sf", "sci_f_01", "sf-01"),
    ("hf", "hist_f_01", "hf-01"),
    ("wf", "writ_f_01", "wf-01"),
    ("vocational", "woodworking-root", "woodworking-root"),
    ("vocational", "el-root", "el-root"),
]


# ── String translation ───────────────────────────────────────────────────


@pytest.mark.parametrize(("prefix", "ref", "content_id"), NAMESPACE_CASES)
def test_round_trip_every_namespace(prefix, ref, content_id):
    """ref -> content-id -> ref is lossless for every namespace."""
    assert resolve_ref_to_content_id(ref) == content_id
    assert resolve_content_id_to_ref(content_id) == ref
    # full round trip back to the original ref
    assert resolve_content_id_to_ref(resolve_ref_to_content_id(ref)) == ref


def test_coverage_every_prefix_resolves():
    """Every required namespace prefix has at least one passing resolution."""
    required = {"mf", "md", "rf", "rd", "sf", "hf", "wf", "vocational"}
    covered = set()
    for prefix, ref, content_id in NAMESPACE_CASES:
        if resolve_ref_to_content_id(ref) == content_id:
            covered.add(prefix)
    assert required <= covered


def test_known_example_directions():
    assert resolve_ref_to_content_id("math_f_01") == "mf-01"
    assert resolve_content_id_to_ref("mf-01") == "math_f_01"


def test_literature_is_documented_exception():
    """Literature does not map mechanically; resolver returns None, not a guess."""
    assert "lit" in node_resolver.NON_MECHANICAL_EXCEPTIONS
    assert resolve_ref_to_content_id("lit_m_01") is None
    assert resolve_content_id_to_ref("lit-craft-001") is None


def test_vocational_not_misread_as_academic():
    """ws-001 (woodworking) must stay identity, not become writ_s_001."""
    assert resolve_content_id_to_ref("ws-001") == "ws-001"
    assert resolve_content_id_to_ref("hs-001") == "hs-001"
    assert resolve_ref_to_content_id("woodworking-root") == "woodworking-root"


def test_unmapped_strings_return_none():
    assert resolve_ref_to_content_id("not a ref") is None
    assert resolve_content_id_to_ref("totally-unknown-123") is None


# ── Single-path reuse proof (no second persistence path) ─────────────────


def test_single_persistence_path():
    """Both the resolver and the from-template HTTP route call the one
    shared apply_template; no parallel persistence path was introduced."""
    assert node_resolver.apply_template is template_persistence.apply_template
    assert curriculum_api.apply_template is template_persistence.apply_template


# ── Persistence resolution ───────────────────────────────────────────────


async def test_persist_idempotent(db_session, household):
    """Two resolves of the same content id -> identical UUID, exactly one row."""
    first = await resolve_content_id_to_uuid(db_session, "mf-01", household.id)
    assert first.node_uuid is not None
    assert first.created is True
    assert first.unresolved is None

    second = await resolve_content_id_to_uuid(db_session, "mf-01", household.id)
    assert second.node_uuid == first.node_uuid
    assert second.created is False

    count = await db_session.scalar(
        select(func.count())
        .select_from(LearningNode)
        .where(LearningNode.source_ref == "mf-01", LearningNode.household_id == household.id)
    )
    assert count == 1


async def test_persist_reuses_from_template_mechanism(db_session, household):
    """Persistence lands a real from-template map: the owning template is
    materialized (subject + all nodes + injected content), proving it went
    through templates.py rather than an ad-hoc single-node insert."""
    result = await resolve_content_id_to_uuid(db_session, "mf-01", household.id)
    assert result.node_uuid is not None

    # A learning map matching the math-foundational template now exists.
    maps = (
        (await db_session.execute(select(LearningMap).where(LearningMap.household_id == household.id))).scalars().all()
    )
    assert any(m.name == MATH_FOUNDATIONAL.name for m in maps)

    # All template nodes were persisted with their source_ref recorded.
    nodes = (
        (await db_session.execute(select(LearningNode).where(LearningNode.household_id == household.id)))
        .scalars()
        .all()
    )
    persisted_refs = {n.source_ref for n in nodes}
    template_refs = {tn.ref for tn in MATH_FOUNDATIONAL.nodes}
    assert template_refs <= persisted_refs

    # The resolved node carries the pre-enriched content injected by the
    # from-template path.
    node = next(n for n in nodes if n.id == result.node_uuid)
    assert node.source_ref == "mf-01"
    assert node.content == MATH_FOUNDATIONAL_CONTENT["mf-01"]


async def test_unresolved_no_template_returns_record_not_exception(db_session, household):
    """Content authored but with no owning template -> None + unresolved
    record, no crash. (reading-foundational content exists but has no
    template, so it cannot be persisted yet.)"""
    res = await resolve_content_id_to_uuid(db_session, "rf-01", household.id)
    assert res.node_uuid is None
    assert res.unresolved is not None
    assert res.unresolved.reason == "no_template"

    # Entirely unknown id, also no exception.
    res2 = await resolve_content_id_to_uuid(db_session, "zz-99", household.id)
    assert res2.node_uuid is None
    assert res2.unresolved is not None


async def test_resolve_ref_to_uuid_unmapped_ref(db_session, household):
    """A ref with no content-id counterpart resolves to an unmapped record."""
    res = await resolve_ref_to_uuid(db_session, "lit_m_01", household.id)
    assert res.node_uuid is None
    assert res.unresolved is not None
    assert res.unresolved.reason == "unmapped_ref"


async def test_resolve_ref_to_uuid_happy_path(db_session, household):
    """End-to-end: scope ref -> content id -> persisted UUID."""
    res = await resolve_ref_to_uuid(db_session, "math_f_01", household.id)
    assert res.node_uuid is not None
    assert res.unresolved is None
