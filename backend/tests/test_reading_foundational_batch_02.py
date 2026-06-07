"""Gold-standard gate for the SECOND reading-foundational batch rf-41..rf-55.

This batch crosses the PA-to-phonics handoff per docs/reading_foundational_gap.md:
it COMPLETES the phonemic-awareness spine (rf-41..rf-49: medial-phoneme
isolation, categorization, full phoneme blend/segment, four-phoneme clusters,
deletion/substitution/addition, PA fluency) and lays the LETTER-knowledge rail
(rf-50..rf-55: name uppercase, name lowercase, match case, form uppercase, form
lowercase, letter-naming automaticity).

Scope note (reported in the deliverable): per the gap doc, the FIRST letter-SOUND
correspondence node is rf-56 (plus the existing rf-03/04/05); there is no
letter-sound node in rf-41..rf-55. So this batch does not contain the literal
letter-sound handoff edge. Instead it lays BOTH rails the letter-sound strand
needs: the terminal auditory phoneme skills (blend/segment, rf-43..rf-45) and
letter naming (rf-50..rf-52). The HANDOFF gate below asserts those rails are in
place; the letter-sound node that consumes them lands next batch at rf-56
(building on the existing rf-03).

Carries forward the batch-01 gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, the PA-AUDITORY gate
(phonemic-awareness nodes stay oral, never depend on the letter/phonics strand),
and the WHOLE-LIBRARY graph-integrity gate scanning rf-01..rf-55, INCLUDING the
documented legacy carve-out read_f_15 -> read_f_21/22 (the reading analogue of
math's mf-07/08 -> mf-09). Everything this batch authors (rf-41+) is strictly
backward-only.
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

NEW_NUMS = list(range(41, 56))
NEW_IDS = [f"rf-{n:02d}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n:02d}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-41..rf-55),
# in content-id form. Every prereq is a real, strictly-earlier reading node.
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-41": ["rf-40"],
    "rf-42": ["rf-40"],
    "rf-43": ["rf-39"],
    "rf-44": ["rf-43"],
    "rf-45": ["rf-44"],
    "rf-46": ["rf-44"],
    "rf-47": ["rf-46"],
    "rf-48": ["rf-47"],
    "rf-49": ["rf-47"],
    "rf-50": ["rf-01"],
    "rf-51": ["rf-50"],
    "rf-52": ["rf-51"],
    "rf-53": ["rf-50"],
    "rf-54": ["rf-51"],
    "rf-55": ["rf-52"],
}

# Phonemic-awareness (oral, "the ear") nodes authored in THIS batch.
PA_NODES_BATCH = ["rf-41", "rf-42", "rf-43", "rf-44", "rf-45", "rf-46", "rf-47", "rf-48", "rf-49"]
# Letter naming / formation (involve LETTERS, not sound mapping) nodes this batch.
LETTER_NODES_BATCH = ["rf-50", "rf-51", "rf-52", "rf-53", "rf-54", "rf-55"]

# The full phonemic-awareness strand across both reading batches (rf-31..rf-49).
ALL_PA_NODES = {f"rf-{n}" for n in range(31, 50)}

# The letter-naming / letter-sound / decoding / formation strand a PA node must
# NEVER depend on. Keeping PA distinct from and before letters is the gap doc's
# load-bearing ordering decision.
LETTER_PHONICS_NODES = {
    "rf-01",
    "rf-03",
    "rf-04",
    "rf-05",
    "rf-06",
    "rf-07",
    "rf-08",
    "rf-09",
    "rf-10",
    "rf-50",
    "rf-51",
    "rf-52",
    "rf-53",
    "rf-54",
    "rf-55",
}

# The only prior nodes a PA node may depend on: the oral PA root (rf-02),
# listening comprehension (rf-21), and any PA node (rf-31..rf-49).
PA_ALLOWED_PREREQS = {"rf-02", "rf-21", *ALL_PA_NODES}

# The letter-knowledge chain a letter-naming node may depend on (rf-01 plus the
# uppercase/lowercase naming nodes). Letter naming does NOT depend on PA.
LETTER_NAMING_ALLOWED = {"rf-01", "rf-50", "rf-51"}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}

# The single legacy forward-reference pair in the un-editable original spine
# (rf-15 Oral Narration -> rf-21, rf-22). Conceptually correct, id-order only;
# the graph stays acyclic. No NEW forward reference is permitted beyond these.
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
    assert "choice_space" not in READING_FOUNDATIONAL_CONTENT[node_id]


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_traditional_spiral_references_a_prior_node(node_id):
    """Every new node (all have prerequisites) carries a spiral_review naming a
    real, strictly-earlier rf node."""
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


def test_counts_now_fifty_five():
    assert len(READING_FOUNDATIONAL_CONTENT) == 55
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) == 55
    assert len(READING_FOUNDATIONAL.nodes) == 55


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


# ── PA-AUDITORY gate ─────────────────────────────────────────────────────


def test_pa_nodes_do_not_depend_on_letter_or_phonics_strand():
    """The phonemic-awareness nodes (rf-41..rf-49) must stay distinct from and
    before letters: none may depend on a letter-naming/letter-sound/formation
    node, and each may depend only on the oral PA root (rf-02), listening
    comprehension (rf-21), or another PA node."""
    for node_id in PA_NODES_BATCH:
        prereqs = set(EXPECTED_PREREQS[node_id])
        letter_dep = prereqs & LETTER_PHONICS_NODES
        assert not letter_dep, f"{node_id} (PA) depends on letter/phonics node(s): {sorted(letter_dep)}"
        stray = prereqs - PA_ALLOWED_PREREQS
        assert not stray, f"{node_id} (PA) depends on non-auditory prereq(s): {sorted(stray)}"


def test_pa_nodes_have_no_forward_dependency():
    for node_id in PA_NODES_BATCH:
        num = _num(node_id)
        for p in EXPECTED_PREREQS[node_id]:
            assert _num(p) < num, f"{node_id} (PA) has a forward dependency on {p}"


# ── HANDOFF gate (the PA-to-phonics bridge this batch lays) ──────────────


def test_handoff_rails_are_laid():
    """This batch lays the TWO rails the letter-sound strand (rf-56 next, and the
    existing rf-03) will join: (1) the terminal auditory phoneme skills, blending
    and segmenting (rf-43, rf-44, rf-45), which stay purely oral and PA-dependent;
    and (2) letter NAMING (rf-50, rf-51, rf-52), which builds on letter
    recognition (rf-01), not on PA. The literal letter-sound handoff edge lands
    next batch at rf-56; there is no letter-sound node in rf-41..rf-55 per the
    gap doc."""
    # Auditory rail: terminal phoneme blend/segment nodes, oral and PA-dependent.
    for nid in ["rf-43", "rf-44", "rf-45"]:
        assert nid in PA_NODES_BATCH
        prereqs = set(EXPECTED_PREREQS[nid])
        assert prereqs <= PA_ALLOWED_PREREQS, f"{nid} auditory rail depends outside PA: {sorted(prereqs)}"
        assert not (prereqs & LETTER_PHONICS_NODES), f"{nid} auditory rail must not touch letters"
    # Letter rail: letter-naming nodes build on letter recognition, not on PA.
    for nid in ["rf-50", "rf-51", "rf-52"]:
        assert nid in LETTER_NODES_BATCH
        prereqs = set(EXPECTED_PREREQS[nid])
        assert prereqs, f"{nid} letter rail should build on prior letter knowledge"
        assert prereqs <= LETTER_NAMING_ALLOWED, (
            f"{nid} letter rail depends outside letter-knowledge: {sorted(prereqs)}"
        )
        assert not (prereqs & ALL_PA_NODES), f"{nid} letter naming must not depend on a PA node"
    # The letter-knowledge rail traces back to rf-01 (Letter Recognition).
    assert EXPECTED_PREREQS["rf-50"] == ["rf-01"]


def test_letter_nodes_build_on_letter_recognition_not_pa():
    """Every letter naming/formation node (rf-50..rf-55) depends only on letter
    knowledge (rf-01 and earlier letter nodes), never on a phonemic-awareness
    node."""
    letter_chain = {"rf-01", *LETTER_NODES_BATCH}
    for node_id in LETTER_NODES_BATCH:
        prereqs = set(EXPECTED_PREREQS[node_id])
        assert prereqs <= letter_chain, f"{node_id} depends outside the letter chain: {sorted(prereqs)}"
        assert not (prereqs & ALL_PA_NODES), f"{node_id} (letter) must not depend on a PA node"


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-55) ──────────────


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
    """ZERO new forward references. Only the documented legacy pair
    (rf-15 -> rf-21/22) is permitted. Everything rf-41..rf-55 is backward-only."""
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
        referenced = [f"rf-{m:02d}" for m in range(1, 56) if f"rf-{m:02d}" in text]
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
    """needs_content drops by exactly 15: before this batch, 40 of the 55 reading
    refs resolved (rf-01..rf-40) and 15 were needs_content (rf-41..rf-55); now all
    55 resolve, so the full 55-topic plan has zero needs_content weeks and 55
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
    assert len(resolved_ids) == 55

    # The batch's exact contribution: each of the 15 new refs resolves.
    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
