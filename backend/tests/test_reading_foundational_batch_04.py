"""Gold-standard gate for the FOURTH reading-foundational batch rf-71..rf-85.

Two pieces (Phase 0 strand-boundary report, in the deliverable):
- rf-71 closes S6: the deferred CVC decoding automaticity capstone, a FLUENCY
  checkpoint spanning the CVC vowel-family decoding (rf-66/67/68) and word
  families (rf-70).
- rf-72..rf-80 are S7, Consonant Digraphs and Blends, the two-letters-one-sound
  conceptual shift. S7 ends at rf-80; S8 (Long Vowels, Silent-e, Vowel Teams)
  begins at rf-81. The 15-node target carries this batch into the start of S8:
  rf-81..rf-84 silent-e and rf-85 the first long-a vowel team. (S8 vowel teams
  continue rf-86+ in the next batch.)

Digraph vs blend (reported and asserted):
- BLEND nodes (two letters, BOTH sounds kept): rf-72, rf-73, rf-74. Each clarifies
  that, unlike a digraph, both sounds are heard.
- DIGRAPH / trigraph nodes (two or three letters, ONE sound): rf-75, rf-76, rf-77,
  rf-78 (combined), rf-79 (encode), rf-80 (automaticity). Each names the
  two-letters-one-sound confusion (sounding the letters separately, or, for the
  encode node, writing only one letter) with a correction.
- First-digraph handoff: rf-75 (sh, ch) lists rf-71 (CVC automaticity) as a
  prerequisite, so the child extends mastered CVC decoding to digraph words.

Carries forward the prior gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, and the WHOLE-LIBRARY
graph-integrity gate scanning rf-01..rf-85, INCLUDING the documented legacy
carve-out read_f_15 -> read_f_21/22. Everything this batch authors (rf-71+) is
strictly backward-only; in particular there is no gap at rf-71.
"""

from datetime import date

import pytest

from app.content.reading_foundational_content import READING_FOUNDATIONAL_CONTENT
from app.content.scope_sequences import get_scope_sequence
from app.services.native_curriculum_generator import generate_for_subject
from app.services.node_content import validate_content, validate_philosophy
from app.services.node_resolver import resolve_ref_to_uuid
from app.services.templates import READING_FOUNDATIONAL

# Canonical requirement sets, imported (not copied) from the schema test.
from tests.test_node_content import NATIVE_KEYS, PHILOSOPHIES, UNSCHOOLING_FORBIDDEN

NEW_NUMS = list(range(71, 86))
NEW_IDS = [f"rf-{n:02d}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n:02d}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-71..rf-85).
# rf-71 spans the CVC decoding nodes and word families (a cross-decoding fluency
# capstone). rf-72 and rf-75 are augmented to build on CVC automaticity (rf-71).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-71": ["rf-66", "rf-67", "rf-68", "rf-70"],
    "rf-72": ["rf-06", "rf-71"],
    "rf-73": ["rf-72"],
    "rf-74": ["rf-73", "rf-69"],
    "rf-75": ["rf-09", "rf-71"],
    "rf-76": ["rf-75"],
    "rf-77": ["rf-76"],
    "rf-78": ["rf-77", "rf-73"],
    "rf-79": ["rf-77", "rf-74"],
    "rf-80": ["rf-78"],
    "rf-81": ["rf-07"],
    "rf-82": ["rf-81"],
    "rf-83": ["rf-82"],
    "rf-84": ["rf-83", "rf-79"],
    "rf-85": ["rf-08"],
}

# rf-71 fluency-span: prerequisites must reach the CVC decoding nodes and word families.
FLUENCY_NODE = "rf-71"
CVC_DECODE_NODES = {"rf-66", "rf-67", "rf-68"}
WORD_FAMILIES_NODE = "rf-70"

# Digraph / trigraph nodes (two or three letters, ONE sound) and blend nodes
# (two letters, BOTH sounds). The digraph nodes must name the two-letters-one-sound
# confusion; the blend nodes must clarify both sounds are kept.
DIGRAPH_NODES = ["rf-75", "rf-76", "rf-77", "rf-78", "rf-79", "rf-80"]
BLEND_NODES = ["rf-72", "rf-73", "rf-74"]

# First-digraph handoff: rf-75 must list a CVC-decode/automaticity node.
FIRST_DIGRAPH_NODE = "rf-75"
CVC_DECODE_OR_AUTOMATICITY = {"rf-66", "rf-67", "rf-68", "rf-71"}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}

# The single legacy forward-reference pair in the un-editable original spine.
KNOWN_LEGACY_FORWARD_REFS: set[tuple[str, str]] = {
    ("read_f_15", "read_f_21"),
    ("read_f_15", "read_f_22"),
}


def _num(node_id: str) -> int:
    return int(node_id.split("_")[-1] if node_id.startswith("read_f_") else node_id.split("-")[1])


def _ref_for(num: int) -> str:
    return f"read_f_{num:02d}"


def _scope_by_ref() -> dict[str, dict]:
    return {t["ref"]: t for t in get_scope_sequence("phonics_reading", "foundational")}


def _template_nodes() -> dict[str, object]:
    return {tn.ref: tn for tn in READING_FOUNDATIONAL.nodes}


# ── Validator gate (real validator) ──────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_validate_content_passes(node_id):
    assert validate_content(READING_FOUNDATIONAL_CONTENT[node_id]) == []


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_validate_philosophy_no_hard_fail(node_id):
    errors = [i for i in validate_philosophy(READING_FOUNDATIONAL_CONTENT[node_id]) if i.startswith("error:")]
    assert errors == []


# ── NATIVE_KEYS gate ─────────────────────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_five_native_philosophy_variants(node_id):
    ps = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]
    for philosophy in PHILOSOPHIES:
        assert philosophy in ps, f"{node_id} missing {philosophy}"
        variant = ps[philosophy]
        assert isinstance(variant, dict)
        missing = NATIVE_KEYS[philosophy] - set(variant.keys())
        assert not missing, f"{node_id}/{philosophy} missing native keys: {sorted(missing)}"


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_unschooling_carries_no_forbidden_key(node_id):
    unschooling = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["unschooling"]
    forbidden = UNSCHOOLING_FORBIDDEN.intersection(unschooling.keys())
    assert not forbidden, f"{node_id} unschooling has forbidden keys: {sorted(forbidden)}"


# ── Depth floor (mf-01 standard) ─────────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_depth_floor(node_id):
    c = READING_FOUNDATIONAL_CONTENT[node_id]
    assert len(c["practice_items"]) >= 8, f"{node_id} has < 8 practice_items"
    assert len(c["assessment_items"]) >= 5, f"{node_id} has < 5 assessment_items"
    assert set(c["accommodations"].keys()) == ACCOMMODATION_KEYS
    assert set(c["philosophy_specific"].keys()) >= set(PHILOSOPHIES)
    diffs = [pi["difficulty"] for pi in c["practice_items"]]
    assert min(diffs) == 1 and max(diffs) == 3
    assert any("correct_answer" not in pi for pi in c["practice_items"])
    assert any("correct_answer" in ai for ai in c["assessment_items"])
    assert any("rubric" in ai for ai in c["assessment_items"])
    assert all(ai.get("target_concept") for ai in c["assessment_items"])


# ── Parent-directed: NO choice_space this batch ──────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_no_choice_space_parent_directed(node_id):
    assert "choice_space" not in READING_FOUNDATIONAL_CONTENT[node_id]


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_traditional_spiral_references_a_prior_node(node_id):
    spiral = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
    text = " ".join(spiral)
    num = _num(node_id)
    referenced = [f"rf-{m:02d}" for m in range(1, num) if f"rf-{m:02d}" in text]
    assert referenced, f"{node_id} spiral_review references no prior rf node: {spiral}"


# ── rf-71 fluency-span ───────────────────────────────────────────────────


def test_rf71_is_a_cross_decoding_fluency_capstone():
    """rf-71's prerequisites span the CVC decoding nodes (rf-66, rf-67, rf-68) and
    word families (rf-70), a cross-decoding automaticity checkpoint, not a
    single-vowel drill."""
    prereqs = set(EXPECTED_PREREQS[FLUENCY_NODE])
    assert prereqs >= CVC_DECODE_NODES, f"rf-71 must span the CVC decode nodes; got {sorted(prereqs)}"
    assert WORD_FAMILIES_NODE in prereqs, "rf-71 must build on word families (rf-70)"


# ── DIGRAPH conceptual-shift + BLEND clarification ───────────────────────


def _misconceptions(node_id: str) -> list[str]:
    return READING_FOUNDATIONAL_CONTENT[node_id]["teaching_guidance"]["common_misconceptions"]


@pytest.mark.parametrize("node_id", DIGRAPH_NODES)
def test_digraph_node_names_two_letters_one_sound_misconception(node_id):
    """Every digraph node's common_misconceptions names the two-letters-one-sound
    confusion (sounding the letters separately, or, for the encode node, writing
    only one letter) with the one-sound correction."""
    multi = (
        "separate",
        "two sounds",
        "two letters",
        "two- or three",
        "three letters",
        "each letter",
        "whole",
        "all of it",
        "more than one",
    )
    found = False
    for m in _misconceptions(node_id):
        ml = m.lower()
        if ("one sound" in ml or "one new sound" in ml) and any(k in ml for k in multi):
            found = True
            break
    assert found, f"{node_id} (digraph) lacks a two-letters-one-sound misconception: {_misconceptions(node_id)}"


@pytest.mark.parametrize("node_id", BLEND_NODES)
def test_blend_node_clarifies_both_sounds_kept(node_id):
    """Every blend node clarifies that, unlike a digraph, both letters' sounds are
    kept (a blend has two sounds / both letters / each letter)."""
    keys = ("both", "two sounds", "each letter")
    found = any(any(k in m.lower() for k in keys) for m in _misconceptions(node_id))
    assert found, f"{node_id} (blend) does not clarify both sounds are kept: {_misconceptions(node_id)}"


def test_first_digraph_node_bridges_cvc_decoding():
    """The first digraph node (rf-75) lists a CVC-decode/automaticity node
    (rf-66/67/68/71) as a prerequisite, so the child extends mastered CVC
    decoding to words with a digraph."""
    prereqs = set(EXPECTED_PREREQS[FIRST_DIGRAPH_NODE])
    bridge = prereqs & CVC_DECODE_OR_AUTOMATICITY
    assert bridge, f"{FIRST_DIGRAPH_NODE} reaches no CVC-decode/automaticity prerequisite: {sorted(prereqs)}"
    assert "rf-71" in prereqs


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"rf-{n:02d}" in READING_FOUNDATIONAL_CONTENT, f"rf-{n:02d} missing from content"
        assert f"read_f_{n:02d}" in scope, f"read_f_{n:02d} missing from scope_sequences"
        assert f"rf-{n:02d}" in tnodes, f"rf-{n:02d} missing from READING_FOUNDATIONAL template"


def test_counts_now_eighty_five():
    # Lower bound: rf-85 landed in this batch; later batches (rf-86+) raise these.
    assert len(READING_FOUNDATIONAL_CONTENT) >= 85
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) >= 85
    assert len(READING_FOUNDATIONAL.nodes) >= 85


# ── Prerequisite integrity (three files agree, earlier-only) ─────────────


def test_scope_prereqs_match_expected_and_are_earlier():
    scope = _scope_by_ref()
    for node_id, prereqs in EXPECTED_PREREQS.items():
        ref = _ref_for(_num(node_id))
        got = scope[ref]["prerequisites"]
        expected_refs = [_ref_for(_num(p)) for p in prereqs]
        assert got == expected_refs, f"{ref} scope prereqs {got} != {expected_refs}"
        num = _num(node_id)
        for p in prereqs:
            assert p in READING_FOUNDATIONAL_CONTENT, f"{node_id} prereq {p} not a real node"
            assert _num(p) < num, f"{node_id} prereq {p} is not earlier"


def test_template_edges_match_scope_prereqs_for_new_nodes():
    incoming: dict[str, set[str]] = {}
    for e in READING_FOUNDATIONAL.edges:
        incoming.setdefault(e.to_ref, set()).add(e.from_ref)
    for node_id, prereqs in EXPECTED_PREREQS.items():
        edges_in = incoming.get(node_id, set())
        assert edges_in == set(prereqs), f"{node_id} template edges {edges_in} != prereqs {set(prereqs)}"


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-85) ──────────────


def test_library_ids_are_contiguous_no_gaps_no_duplicates():
    keys = list(READING_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate rf ids: {[f'rf-{n:02d}' for n in duplicates]}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing rf ids (gaps): {[f'rf-{n:02d}' for n in missing]}"
    # In particular, there is no gap at rf-71 (the deferred capstone landed here).
    assert 71 in set(nums)
    assert set(nums) == expected, f"id set is not exactly rf-01..rf-{top:02d}"


def test_cross_file_count_parity():
    content_count = len(READING_FOUNDATIONAL_CONTENT)
    scope_count = len(
        [t for t in get_scope_sequence("phonics_reading", "foundational") if str(t["ref"]).startswith("read_f_")]
    )
    template_count = len({tn.ref for tn in READING_FOUNDATIONAL.nodes if str(tn.ref).startswith("rf-")})
    assert content_count == scope_count == template_count, (
        f"count mismatch: content={content_count}, scope={scope_count}, template={template_count}"
    )


def test_every_prerequisite_references_a_real_node():
    scope = _scope_by_ref()
    dangling: list[str] = []
    for ref, entry in scope.items():
        for p in entry.get("prerequisites", []):
            content_id = f"rf-{_num(p):02d}"
            if content_id not in READING_FOUNDATIONAL_CONTENT or p not in scope:
                dangling.append(f"{ref} -> {p}")
    assert not dangling, f"dangling prerequisite references: {dangling}"


def test_prerequisites_are_backward_only_except_known_legacy():
    scope = _scope_by_ref()
    forward: set[tuple[str, str]] = set()
    for ref, entry in scope.items():
        n = _num(ref)
        for p in entry.get("prerequisites", []):
            if _num(p) >= n:
                forward.add((ref, p))
    new_forward = forward - KNOWN_LEGACY_FORWARD_REFS
    assert not new_forward, f"new forward references (prerequisite id not strictly earlier): {sorted(new_forward)}"
    assert forward <= KNOWN_LEGACY_FORWARD_REFS, f"unexpected forward-reference set: {sorted(forward)}"
    new_forward_in_batch = {(r, p) for (r, p) in forward if _num(r) in NEW_NUMS}
    assert not new_forward_in_batch, f"authored batch introduced a forward reference: {sorted(new_forward_in_batch)}"


def test_prerequisite_graph_is_acyclic():
    scope = _scope_by_ref()
    graph = {ref: list(entry.get("prerequisites", [])) for ref, entry in scope.items()}

    WHITE, GREY, BLACK = 0, 1, 2
    color = dict.fromkeys(graph, WHITE)
    cycle_path: list[str] = []

    def visit(node: str, stack: list[str]) -> bool:
        color[node] = GREY
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt not in color:
                continue
            if color[nxt] == GREY:
                cycle_path.extend(stack[stack.index(nxt) :] + [nxt])
                return True
            if color[nxt] == WHITE and visit(nxt, stack):
                return True
        stack.pop()
        color[node] = BLACK
        return False

    for ref in graph:
        if color[ref] == WHITE and visit(ref, []):
            break
    assert not cycle_path, f"prerequisite cycle detected: {' -> '.join(cycle_path)}"


def test_spiral_review_references_resolve_to_real_prior_nodes():
    unresolved: list[str] = []
    for node_id in NEW_IDS:
        num = _num(node_id)
        spiral = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
        text = " ".join(spiral)
        referenced = [f"rf-{m:02d}" for m in range(1, 86) if f"rf-{m:02d}" in text]
        assert referenced, f"{node_id} spiral_review references no rf node"
        for r in referenced:
            if r not in READING_FOUNDATIONAL_CONTENT:
                unresolved.append(f"{node_id} -> {r} (missing)")
            elif _num(r) >= num:
                unresolved.append(f"{node_id} -> {r} (not earlier)")
    assert not unresolved, f"unresolvable spiral references: {unresolved}"


# ── Resolver + generator gates (DB) ──────────────────────────────────────


@pytest.mark.parametrize("ref", NEW_REFS)
async def test_resolver_resolves_each_new_ref(db_session, household, ref):
    res = await resolve_ref_to_uuid(db_session, ref, household.id)
    assert res.node_uuid is not None, f"{ref} did not resolve to a UUID"
    assert res.unresolved is None


async def test_generator_plan_reading_tier_zero_needs_content(db_session, household):
    """needs_content drops by exactly 15: before this batch, 70 of the 85 reading
    refs resolved (rf-01..rf-70) and 15 were needs_content (rf-71..rf-85); now all
    85 resolve, so the full 85-topic plan has zero needs_content weeks and 85
    distinct focus-node UUIDs."""
    scope = get_scope_sequence("phonics_reading", "foundational")
    out = await generate_for_subject(
        db_session,
        household.id,
        "phonics_reading",
        "foundational",
        hours_per_week=4.0,
        total_weeks=len(scope),
        start_date=date(2026, 9, 1),
    )
    needs = [w for w in out["weeks"] if w.get("needs_content")]
    assert needs == [], f"unexpected needs_content weeks: {[w['week_number'] for w in needs]}"
    resolved_ids = {fid for w in out["weeks"] for fid in w["focus_nodes"]}
    # Lower bound: rf-01..rf-85 all resolve; later batches add more resolvable refs.
    assert len(resolved_ids) >= 85

    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
