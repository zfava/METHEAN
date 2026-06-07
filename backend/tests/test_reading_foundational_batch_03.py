"""Gold-standard gate for the THIRD reading-foundational batch rf-56..rf-70,
the LETTER-SOUND strand where both rails join (the real PA-to-phonics handoff).

Phase 0 reconciliation (reported in the deliverable): the existing rf-03
(Consonant Sounds), rf-04 (Short Vowels), and rf-05 (CVC Words) are GENERAL,
introductory nodes. The gap doc's rf-56..rf-70 are finer-grained, systematic,
mf-01-depth nodes that BUILD ON them. Classification: EXTEND. There is no
duplication: rf-56 lists rf-03 as a prerequisite, rf-61 lists rf-04, and rf-66
lists rf-05; each deepens rather than repeats the general node.

Strand boundaries: S5 letter-sound is rf-56..rf-64 (consonant sets rf-56..rf-59,
review rf-60, short vowels rf-61..rf-63, letter-sound automaticity rf-64); S6
CVC is rf-65 (blend VC/CVC), rf-66..rf-68 (decode by vowel family), rf-69
(encode), rf-70 (word families). This batch authors rf-56..rf-70 (15); rf-71
(CVC automaticity capstone) and S7 (digraphs/blends, rf-72+) are the next batch.

DUAL-RAIL handoff: the first letter-sound node rf-56 connects BOTH rails. It
lists as prerequisites the auditory rail (rf-43, phoneme blending) AND the
letter rail (rf-51, lowercase naming), plus the EXTEND parent rf-03. The dual
dependency IS the bridge: the child brings the heard sound and the known letter
to sound-to-letter mapping. (rf-65 and rf-69 likewise pair a phonics node with
an auditory PA node, rf-43 and rf-44.)

Carries forward the prior gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, and the WHOLE-LIBRARY
graph-integrity gate scanning rf-01..rf-70, INCLUDING the documented legacy
carve-out read_f_15 -> read_f_21/22. Everything this batch authors (rf-56+) is
strictly backward-only.
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

NEW_NUMS = list(range(56, 71))
NEW_IDS = [f"rf-{n:02d}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n:02d}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-56..rf-70),
# in content-id form. rf-56 is augmented with the dual-rail prerequisites
# (rf-51 letter rail, rf-43 auditory rail) on top of its EXTEND parent rf-03.
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-56": ["rf-03", "rf-51", "rf-43"],
    "rf-57": ["rf-56"],
    "rf-58": ["rf-57"],
    "rf-59": ["rf-58"],
    "rf-60": ["rf-59"],
    "rf-61": ["rf-04"],
    "rf-62": ["rf-61"],
    "rf-63": ["rf-62"],
    "rf-64": ["rf-60", "rf-63"],
    "rf-65": ["rf-64", "rf-43"],
    "rf-66": ["rf-05"],
    "rf-67": ["rf-66"],
    "rf-68": ["rf-67"],
    "rf-69": ["rf-68", "rf-44"],
    "rf-70": ["rf-66"],
}

# EXTEND links: each new node that deepens a general existing node lists it.
EXTEND_LINKS = {"rf-56": "rf-03", "rf-61": "rf-04", "rf-66": "rf-05"}

# DUAL-RAIL: the first letter-sound node and the rails it must reach.
FIRST_LETTER_SOUND_NODE = "rf-56"
AUDITORY_RAIL = {"rf-43", "rf-44", "rf-45", "rf-03", "rf-04", "rf-05"}
LETTER_RAIL = {"rf-50", "rf-51", "rf-52"}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}

# The single legacy forward-reference pair in the un-editable original spine
# (rf-15 Oral Narration -> rf-21, rf-22). Conceptually correct, id-order only.
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


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"rf-{n:02d}" in READING_FOUNDATIONAL_CONTENT, f"rf-{n:02d} missing from content"
        assert f"read_f_{n:02d}" in scope, f"read_f_{n:02d} missing from scope_sequences"
        assert f"rf-{n:02d}" in tnodes, f"rf-{n:02d} missing from READING_FOUNDATIONAL template"


def test_counts_now_seventy():
    assert len(READING_FOUNDATIONAL_CONTENT) == 70
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) == 70
    assert len(READING_FOUNDATIONAL.nodes) == 70


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


# ── NO-DUPLICATION (EXTEND): new nodes build on the general rf-03/04/05 ───


def test_extend_links_present_no_duplication():
    """The reconciliation classified the batch EXTEND: rf-56 deepens rf-03,
    rf-61 deepens rf-04, and rf-66 deepens rf-05, listing each general node as a
    prerequisite rather than duplicating it. The existing nodes are referenced,
    never modified (they are out of scope)."""
    for new_node, general in EXTEND_LINKS.items():
        assert general in EXPECTED_PREREQS[new_node], f"{new_node} must list {general} as a prerequisite (EXTEND)"
        assert general in READING_FOUNDATIONAL_CONTENT, f"general node {general} must still exist"
        # The general node is the introductory spine node; the new node is the deeper one.
        assert _num(general) < _num(new_node)


# ── DUAL-RAIL HANDOFF: the first letter-sound node joins both rails ───────


def test_first_letter_sound_node_bridges_both_rails():
    """rf-56, the first letter-sound node, lists prerequisites reaching BOTH the
    auditory rail (a terminal phoneme blend/segment PA node, or the existing
    letter-sound nodes) AND the letter rail (a letter-naming node). A node on
    only one rail would have cut the handoff."""
    prereqs = set(EXPECTED_PREREQS[FIRST_LETTER_SOUND_NODE])
    auditory = prereqs & AUDITORY_RAIL
    letter = prereqs & LETTER_RAIL
    assert auditory, f"{FIRST_LETTER_SOUND_NODE} reaches no auditory-rail prerequisite: {sorted(prereqs)}"
    assert letter, f"{FIRST_LETTER_SOUND_NODE} reaches no letter-rail prerequisite: {sorted(prereqs)}"
    # Specifically, rf-56 bridges rf-43 (auditory) and rf-51 (letter), extending rf-03.
    assert "rf-43" in prereqs and "rf-51" in prereqs and "rf-03" in prereqs


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-70) ──────────────


def test_library_ids_are_contiguous_no_gaps_no_duplicates():
    keys = list(READING_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate rf ids: {[f'rf-{n:02d}' for n in duplicates]}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing rf ids (gaps): {[f'rf-{n:02d}' for n in missing]}"
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
        referenced = [f"rf-{m:02d}" for m in range(1, 71) if f"rf-{m:02d}" in text]
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
    """needs_content drops by exactly 15: before this batch, 55 of the 70 reading
    refs resolved (rf-01..rf-55) and 15 were needs_content (rf-56..rf-70); now all
    70 resolve, so the full 70-topic plan has zero needs_content weeks and 70
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
    assert len(resolved_ids) == 70

    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
