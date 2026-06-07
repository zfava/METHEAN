"""Gold-standard gate for the FIRST reading-foundational batch rf-26..rf-40,
the first authoring batch of the reading tier (explicit, systematic phonics).

Carries the per-batch gold-standard gates (validator, NATIVE_KEYS, depth floor,
parent-directed: no choice_space), three-file integrity, the PA-AUDITORY gate
(phonological/phonemic-awareness nodes stay oral and never depend on the
letter-sound phonics strand), and the WHOLE-LIBRARY graph-integrity gate
scanning every reading-foundational node rf-01..rf-40.

Architecture note (reported in the deliverable): the reading tier had no
template before this batch, so this batch stands the reading-foundational
template up, owning rf-01..rf-40 (the existing 25 content nodes are wired
unchanged plus the 15 new ones). That is what lets three-file count parity hold
at 40/40/40 and the whole tier resolve and generate.

Legacy forward-reference note: the ORIGINAL rf-01..rf-25 scope (which this
contract is forbidden to edit) places rf-15 Oral Narration after its
conceptual prerequisites rf-21 and rf-22, so read_f_15 -> read_f_21/22 are
backward in concept but forward in id NUMBERING. The dependency is correct and
the graph stays acyclic; this is the reading analogue of the math tier's
documented mf-07/08 -> mf-09 legacy pair. Every node this batch authors
(rf-26 onward) is strictly backward-only.
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

NEW_NUMS = list(range(26, 41))
NEW_IDS = [f"rf-{n:02d}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n:02d}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-26..rf-40),
# expressed in content-id form. Every prereq is a real, strictly-earlier reading
# node (an existing rf-01..rf-25 or an earlier node in this batch).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-26": [],
    "rf-27": ["rf-20"],
    "rf-28": ["rf-27"],
    "rf-29": ["rf-28"],
    "rf-30": ["rf-29"],
    "rf-31": ["rf-21"],
    "rf-32": ["rf-31"],
    "rf-33": ["rf-21"],
    "rf-34": ["rf-33"],
    "rf-35": ["rf-34"],
    "rf-36": ["rf-34"],
    "rf-37": ["rf-36"],
    "rf-38": ["rf-31"],
    "rf-39": ["rf-02"],
    "rf-40": ["rf-39"],
}

# The phonological- and phonemic-awareness nodes in THIS batch (the "ear"
# strands: rhyme, syllables, onset-rime, phoneme isolation). rf-26..rf-30 are
# print-concept nodes, not PA. Reported and asserted auditory below.
PA_NODES = ["rf-31", "rf-32", "rf-33", "rf-34", "rf-35", "rf-36", "rf-37", "rf-38", "rf-39", "rf-40"]

# The letter-naming / letter-sound / decoding (phonics) strand a PA node must
# NEVER depend on. Keeping PA distinct from and before phonics is the gap doc's
# load-bearing ordering decision.
PHONICS_LETTER_NODES = {"rf-01", "rf-03", "rf-04", "rf-05", "rf-06", "rf-07", "rf-08", "rf-09", "rf-10"}

# The only prior reading nodes a PA node in this batch may depend on: the oral
# phonemic-awareness root (rf-02), listening comprehension (rf-21), and earlier
# PA nodes in this batch.
PA_ALLOWED_PREREQS = {"rf-02", "rf-21", *PA_NODES}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}

# The single legacy forward-reference pair living in the un-editable original
# rf-01..rf-25 scope (rf-15 Oral Narration -> rf-21, rf-22). Conceptually
# correct, id-order only; the graph stays acyclic. No NEW forward reference is
# permitted beyond these.
KNOWN_LEGACY_FORWARD_REFS: set[tuple[str, str]] = {
    ("read_f_15", "read_f_21"),
    ("read_f_15", "read_f_22"),
}


def _num(node_id: str) -> int:
    """Numeric part of an rf-NN or read_f_NN id."""
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
    """This batch is authored parent-directed: no node defines a choice_space."""
    assert "choice_space" not in READING_FOUNDATIONAL_CONTENT[node_id]


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_traditional_spiral_references_a_prior_node(node_id):
    """Every non-root new node's spiral_review names a real, strictly-earlier rf
    node. rf-26 is the root of the print-concepts strand (no prerequisite) and,
    like mf-01, references a precursor sub-skill instead."""
    spiral = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
    text = " ".join(spiral)
    num = _num(node_id)
    if not EXPECTED_PREREQS[node_id]:
        # Root node: exempt from the prior-node reference, exactly as mf-01 is.
        return
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


def test_counts_now_forty():
    assert len(READING_FOUNDATIONAL_CONTENT) == 40
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) == 40
    assert len(READING_FOUNDATIONAL.nodes) == 40


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
    """For every new node, the template's incoming edges equal its scope
    prerequisites (three-file agreement)."""
    incoming: dict[str, set[str]] = {}
    for e in READING_FOUNDATIONAL.edges:
        incoming.setdefault(e.to_ref, set()).add(e.from_ref)
    for node_id, prereqs in EXPECTED_PREREQS.items():
        edges_in = incoming.get(node_id, set())
        assert edges_in == set(prereqs), f"{node_id} template edges {edges_in} != prereqs {set(prereqs)}"


# ── PA-AUDITORY gate ─────────────────────────────────────────────────────


def test_pa_nodes_do_not_depend_on_phonics_strand():
    """Phonological/phonemic-awareness nodes (the 'ear' strands) must stay
    distinct from and before letter-sound phonics: none may depend on a
    letter-naming/letter-sound/decoding node, and each may depend only on the
    oral PA root (rf-02), listening comprehension (rf-21), or an earlier PA node
    in this batch."""
    for node_id in PA_NODES:
        prereqs = set(EXPECTED_PREREQS[node_id])
        phonics_dep = prereqs & PHONICS_LETTER_NODES
        assert not phonics_dep, f"{node_id} (PA) depends on phonics/letter-sound node(s): {sorted(phonics_dep)}"
        stray = prereqs - PA_ALLOWED_PREREQS
        assert not stray, f"{node_id} (PA) depends on non-auditory prereq(s): {sorted(stray)}"


def test_pa_nodes_have_no_forward_dependency_into_phonics():
    """A PA node must not depend on any later-numbered node (which would reach
    forward into the phonics strand that follows). All PA prereqs are strictly
    earlier."""
    for node_id in PA_NODES:
        num = _num(node_id)
        for p in EXPECTED_PREREQS[node_id]:
            assert _num(p) < num, f"{node_id} (PA) has a forward dependency on {p}"


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-40) ──────────────


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
    """ZERO new forward references. The only forward references permitted are the
    documented legacy pair in the un-editable original spine (rf-15 -> rf-21/22).
    Every node this batch authored (rf-26..rf-40) is strictly backward-only."""
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
    # Everything this batch authored is strictly backward-only.
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
    """Every new node's spiral_review names only real, strictly-earlier rf nodes
    (root rf-26 carries no rf reference and is skipped)."""
    unresolved: list[str] = []
    for node_id in NEW_IDS:
        if not EXPECTED_PREREQS[node_id]:
            continue  # root node, exempt
        num = _num(node_id)
        spiral = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
        text = " ".join(spiral)
        referenced = [f"rf-{m:02d}" for m in range(1, 41) if f"rf-{m:02d}" in text]
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


async def test_generator_plan_reading_tier_resolves_new_batch(db_session, household):
    """The reading tier now generates. The 15 newly-authored refs each resolve
    (the batch's contribution: needs_content drops by exactly 15 versus a world
    without these nodes), and with the reading-foundational template standing the
    full tier up, the 40-topic plan has zero needs_content weeks."""
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
    assert len(resolved_ids) == 40

    # The batch's exact contribution: each of the 15 new refs resolves.
    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
