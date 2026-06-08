"""Gold-standard gate for the FIFTH reading-foundational batch rf-86..rf-100.

Strand-boundary report (in the deliverable):
- rf-86..rf-92 complete S8 (Long Vowels and Vowel Teams): the long-e, long-o,
  long-i, long-u/oo teams, y as a vowel, open syllables, a vowel-team SPELL
  (encode) node, and a vowel-team decoding automaticity FLUENCY checkpoint
  (rf-92). S8 ends at rf-92.
- rf-93..rf-100 open S9 (R-Controlled Vowels and Diphthongs): r-controlled
  ar/or and er/ir/ur, diphthongs oi/oy and ou/ow, the aw/au patterns, soft c
  and g, silent-letter patterns, and an r-controlled/diphthong SPELL (encode)
  node. S9's automaticity checkpoint (rf-101) is deferred to the next batch.

This is the batch where English phonics becomes genuinely irregular, and the
METHEAN standard is to teach that irregularity HONESTLY:

- VARIABLE-SOUND honesty (asserted): every team that maps one spelling to more
  than one sound (rf-86 ea, rf-87 ow/ie, rf-88 oo, rf-89 y, rf-96 ow) names the
  variable-sound reality AND a flexible-decoding ("set for variability")
  strategy in its common_misconceptions.
- R-CONTROLLED third category (asserted): every r-controlled node (rf-93, rf-94)
  names the neither-short-nor-long confusion with a correction. The first
  r-controlled node (rf-93) lists a prior long/short-vowel node (rf-83) as a
  prerequisite, bridging the new third category to mastered short/long work.
- EXTEND integrity (asserted): the first in-batch vowel-team node (rf-86) lists
  the general vowel-teams node (rf-08) as a prerequisite, deepening rather than
  duplicating.

Carries forward the prior gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, and the WHOLE-LIBRARY
graph-integrity gate scanning rf-01..rf-100, INCLUDING the documented legacy
carve-out read_f_15 -> read_f_21/22. Everything this batch authors (rf-86+) is
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

NEW_NUMS = list(range(86, 101))
NEW_IDS = [f"rf-{n:02d}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n:02d}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-86..rf-100).
# rf-86 is augmented with rf-08 (EXTEND of the general vowel-teams node); rf-93 is
# augmented with rf-83 (the short/long-vowel contrast it builds the third category on).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-86": ["rf-85", "rf-08"],
    "rf-87": ["rf-86"],
    "rf-88": ["rf-87"],
    "rf-89": ["rf-88"],
    "rf-90": ["rf-89"],
    "rf-91": ["rf-88", "rf-84"],
    "rf-92": ["rf-90"],
    "rf-93": ["rf-92", "rf-83"],
    "rf-94": ["rf-93"],
    "rf-95": ["rf-94"],
    "rf-96": ["rf-95"],
    "rf-97": ["rf-96"],
    "rf-98": ["rf-97"],
    "rf-99": ["rf-98"],
    "rf-100": ["rf-97", "rf-91"],
}

# Variable-sound teams: one spelling, more than one sound. Each must name the
# variability AND a flexible-decoding strategy in its common_misconceptions.
VARIABLE_SOUND_NODES = ["rf-86", "rf-87", "rf-88", "rf-89", "rf-96"]

# R-controlled nodes: the third vowel category, neither short nor long. Each must
# name the neither-short-nor-long confusion with a correction.
R_CONTROLLED_NODES = ["rf-93", "rf-94"]

# First r-controlled node bridges to a prior long/short-vowel node.
FIRST_R_CONTROLLED_NODE = "rf-93"
LONG_SHORT_VOWEL_NODES = {"rf-81", "rf-82", "rf-83"}

# EXTEND: the first in-batch vowel-team node deepens the general vowel-teams node.
FIRST_VOWEL_TEAM_NODE = "rf-86"
GENERAL_VOWEL_TEAMS_NODE = "rf-08"

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


def _misconceptions(node_id: str) -> list[str]:
    return READING_FOUNDATIONAL_CONTENT[node_id]["teaching_guidance"]["common_misconceptions"]


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


# ── VARIABLE-SOUND honesty (one spelling, more than one sound) ───────────


@pytest.mark.parametrize("node_id", VARIABLE_SOUND_NODES)
def test_variable_sound_node_names_variability_and_flex(node_id):
    """Every variable-sound team's common_misconceptions both (a) names that the
    team makes more than one sound and (b) gives a flexible-decoding ("set for
    variability") strategy: try one sound, and if the word is not real, flex to
    the other. METHEAN teaches the irregularity honestly, with a strategy."""
    misc = _misconceptions(node_id)
    names_variability = any(
        ("more than one sound" in m.lower() or "two sounds" in m.lower() or "variable" in m.lower()) for m in misc
    )
    gives_flex = any(
        ("flex" in m.lower() or "try" in m.lower())
        and ("not real" in m.lower() or "real word" in m.lower() or "if the word" in m.lower())
        for m in misc
    )
    assert names_variability, f"{node_id} (variable-sound) never names the more-than-one-sound reality: {misc}"
    assert gives_flex, f"{node_id} (variable-sound) gives no flexible-decoding strategy: {misc}"


# ── R-CONTROLLED third category (neither short nor long) ──────────────────


@pytest.mark.parametrize("node_id", R_CONTROLLED_NODES)
def test_r_controlled_node_names_third_category(node_id):
    """Every r-controlled node names the third-category confusion: a child may
    read the vowel as its short or long sound, but the r changes it into a new
    r-controlled sound that is neither short nor long. The misconception must
    say so and correct it."""
    misc = _misconceptions(node_id)
    found = any(("neither short nor long" in m.lower()) and ("r " in m.lower() or "the r" in m.lower()) for m in misc)
    assert found, f"{node_id} (r-controlled) lacks a neither-short-nor-long misconception: {misc}"


def test_first_r_controlled_node_bridges_long_short_vowels():
    """The first r-controlled node (rf-93) lists a prior long/short-vowel node so
    the child builds the new third category on mastered short/long work."""
    prereqs = set(EXPECTED_PREREQS[FIRST_R_CONTROLLED_NODE])
    bridge = prereqs & LONG_SHORT_VOWEL_NODES
    assert bridge, f"{FIRST_R_CONTROLLED_NODE} reaches no long/short-vowel prerequisite: {sorted(prereqs)}"
    assert "rf-83" in prereqs


def test_first_vowel_team_node_extends_general_vowel_teams():
    """The first in-batch vowel-team node (rf-86) lists the general vowel-teams
    node (rf-08), deepening rather than duplicating it."""
    assert GENERAL_VOWEL_TEAMS_NODE in EXPECTED_PREREQS[FIRST_VOWEL_TEAM_NODE]


# ── Encode nodes confront the multiple-spellings choice ──────────────────


@pytest.mark.parametrize("node_id", ["rf-91", "rf-100"])
def test_encode_node_confronts_multiple_spellings(node_id):
    """The spell/encode nodes must confront that one sound can be spelled more
    than one way and that the speller (unlike the reader) must choose."""
    misc = _misconceptions(node_id)
    found = any(
        ("more than one way" in m.lower() or "three ways" in m.lower() or "three spellings" in m.lower())
        or ("spelled" in m.lower() and "choose" in m.lower())
        for m in misc
    )
    assert found, f"{node_id} (encode) never confronts the multiple-spellings choice: {misc}"


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"rf-{n:02d}" in READING_FOUNDATIONAL_CONTENT, f"rf-{n:02d} missing from content"
        assert f"read_f_{n:02d}" in scope, f"read_f_{n:02d} missing from scope_sequences"
        assert f"rf-{n:02d}" in tnodes, f"rf-{n:02d} missing from READING_FOUNDATIONAL template"


def test_counts_now_one_hundred():
    # Lower bound: rf-100 landed in this batch; later batches (rf-101+) raise these.
    assert len(READING_FOUNDATIONAL_CONTENT) >= 100
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) >= 100
    assert len(READING_FOUNDATIONAL.nodes) >= 100


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


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-100) ─────────────


def test_library_ids_are_contiguous_no_gaps_no_duplicates():
    keys = list(READING_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate rf ids: {[f'rf-{n:02d}' for n in duplicates]}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing rf ids (gaps): {[f'rf-{n:02d}' for n in missing]}"
    assert top >= 100, f"library top should be at least rf-100, got rf-{top:02d}"
    assert set(nums) == expected, f"id set is not exactly rf-01..rf-{top:02d}"


def test_cross_file_count_parity():
    content_count = len(READING_FOUNDATIONAL_CONTENT)
    scope_count = len(
        [t for t in get_scope_sequence("phonics_reading", "foundational") if str(t["ref"]).startswith("read_f_")]
    )
    template_count = len({tn.ref for tn in READING_FOUNDATIONAL.nodes if str(tn.ref).startswith("rf-")})
    assert content_count == scope_count == template_count >= 100, (
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
        referenced = [f"rf-{m:02d}" for m in range(1, 101) if f"rf-{m:02d}" in text]
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
    """needs_content drops by exactly 15: before this batch, 85 of the 100 reading
    refs resolved (rf-01..rf-85) and 15 were needs_content (rf-86..rf-100); now all
    100 resolve, so the full 100-topic plan has zero needs_content weeks and 100
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
    # Lower bound: rf-01..rf-100 all resolve; later batches add more resolvable refs.
    assert len(resolved_ids) >= 100

    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
