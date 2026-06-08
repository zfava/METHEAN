"""Gold-standard gate for the SIXTH reading-foundational batch rf-101..rf-115.

Strand-boundary report (in the deliverable):
- rf-101 closes S9 (Advanced Patterns): the deferred advanced-phonics decoding
  automaticity FLUENCY checkpoint, spanning the S9 patterns (r-controlled,
  diphthongs, aw/au, soft c/g, silent letters).
- rf-102..rf-114 are S10 (Syllable Types, Multisyllabic Decoding, Affixes): the
  six syllable types (rf-102 closed/open, rf-103 VCe/vowel-team/r-controlled,
  rf-104 consonant-le), the syllable-division procedure (rf-105), two- and
  three-syllable decoding (rf-106, rf-108), schwa (rf-107), inflectional endings
  and affixes (rf-109..rf-112), a multisyllabic/affix SPELL (encode) node
  (rf-113), and the multisyllabic decoding automaticity FLUENCY checkpoint
  (rf-114) that closes S10.
- rf-115 opens S11 (High-Frequency / Irregular Sight Words): irregular
  high-frequency words by the heart-word method, included to complete the
  15-node target; S11 continues rf-116+ in the next batch.

Honesty / leap standards enforced by this gate:
- rf-101 FLUENCY span (asserted): its prerequisites span the S9 advanced-phonics
  families (r-controlled, diphthong, soft c/g, silent letter), a cross-pattern
  automaticity checkpoint, not single-pattern drill.
- SYLLABLE-TYPE bridge (asserted): each syllable-type node names, in its content,
  the single-syllable phonics pattern it now treats as a syllable type
  (closed -> short vowels, open -> long, VCe -> silent-e, vowel-team -> teams,
  r-controlled -> the ar/or/er patterns, consonant-le -> the -le ending).
- FIRST-MULTISYLLABIC handoff (asserted): the first S10 node (rf-102) lists a
  single-syllable automaticity node (rf-101) as a prerequisite, extending
  mastered single-syllable decoding to syllables within longer words.
- SYLLABLE-DIVISION procedure (asserted): the division nodes (rf-104, rf-105)
  carry a concrete, parent-deliverable division procedure, not just the rule's
  name.

Carries forward the prior gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, and the WHOLE-LIBRARY
graph-integrity gate scanning rf-01..rf-115, INCLUDING the documented legacy
carve-out read_f_15 -> read_f_21/22. Everything this batch authors (rf-101+) is
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

NEW_NUMS = list(range(101, 116))
NEW_IDS = [f"rf-{n}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-101..rf-115).
# rf-101 is augmented to span the S9 advanced-phonics families (a cross-pattern
# automaticity checkpoint); rf-102 is augmented with rf-101 (the first-multisyllabic
# handoff to single-syllable automaticity).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-101": ["rf-94", "rf-96", "rf-97", "rf-98", "rf-99"],
    "rf-102": ["rf-90", "rf-101"],
    "rf-103": ["rf-102", "rf-93"],
    "rf-104": ["rf-103"],
    "rf-105": ["rf-104"],
    "rf-106": ["rf-105"],
    "rf-107": ["rf-106"],
    "rf-108": ["rf-107"],
    "rf-109": ["rf-106"],
    "rf-110": ["rf-109"],
    "rf-111": ["rf-106"],
    "rf-112": ["rf-111"],
    "rf-113": ["rf-110", "rf-100"],
    "rf-114": ["rf-108", "rf-112"],
    "rf-115": ["rf-71"],
}

# rf-101 advanced-phonics fluency span: its prerequisites must reach each S9 family.
FLUENCY_NODE = "rf-101"
S9_FAMILIES = {
    "r_controlled": {"rf-93", "rf-94"},
    "diphthong": {"rf-95", "rf-96"},
    "soft_c_g": {"rf-98"},
    "silent_letter": {"rf-99"},
}

# Syllable-type nodes and the single-syllable pattern keywords each must name.
SYLLABLE_TYPE_KEYWORDS: dict[str, list[str]] = {
    "rf-102": ["closed", "open", "short", "long"],
    "rf-103": ["silent e", "vowel team", "r-controlled"],
    "rf-104": ["consonant-le"],
}

# First multisyllabic node bridges to single-syllable automaticity/decoding.
FIRST_MULTISYLLABIC_NODE = "rf-102"
SINGLE_SYLLABLE_AUTOMATICITY = {"rf-71", "rf-101"}

# Division nodes that must carry a concrete, parent-deliverable procedure.
DIVISION_NODES = ["rf-104", "rf-105"]

# The multisyllabic FLUENCY checkpoint that closes S10.
MULTISYLLABIC_FLUENCY_NODE = "rf-114"

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}

# The single legacy forward-reference pair in the un-editable original spine.
KNOWN_LEGACY_FORWARD_REFS: set[tuple[str, str]] = {
    ("read_f_15", "read_f_21"),
    ("read_f_15", "read_f_22"),
}


def _num(node_id: str) -> int:
    return int(node_id.split("_")[-1] if node_id.startswith("read_f_") else node_id.split("-")[1])


def _ref_for(num: int) -> str:
    return f"read_f_{num}"


def _scope_by_ref() -> dict[str, dict]:
    return {t["ref"]: t for t in get_scope_sequence("phonics_reading", "foundational")}


def _template_nodes() -> dict[str, object]:
    return {tn.ref: tn for tn in READING_FOUNDATIONAL.nodes}


def _node_text(node_id: str) -> str:
    import json

    return json.dumps(READING_FOUNDATIONAL_CONTENT[node_id]).lower()


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
    referenced = [f"rf-{m:02d}" for m in range(1, num) if f"rf-{m:02d}" in text] + [
        f"rf-{m}" for m in range(1, num) if f"rf-{m}" in text
    ]
    assert referenced, f"{node_id} spiral_review references no prior rf node: {spiral}"


# ── rf-101 advanced-phonics fluency span ─────────────────────────────────


def test_rf101_spans_s9_advanced_phonics():
    """rf-101's prerequisites span the S9 advanced-phonics families (r-controlled,
    diphthong, soft c/g, silent letter), a cross-pattern automaticity checkpoint,
    not a single-pattern drill."""
    prereqs = set(EXPECTED_PREREQS[FLUENCY_NODE])
    for family, members in S9_FAMILIES.items():
        assert prereqs & members, f"rf-101 reaches no {family} prerequisite; got {sorted(prereqs)}"
    assert len(prereqs) >= 4, f"rf-101 should span multiple S9 families; got {sorted(prereqs)}"


# ── SYLLABLE-TYPE bridge: each type names its single-syllable pattern ─────


@pytest.mark.parametrize("node_id", list(SYLLABLE_TYPE_KEYWORDS.keys()))
def test_syllable_type_names_single_syllable_pattern(node_id):
    """Each syllable-type node names, in its content, the single-syllable phonics
    pattern it now treats as a syllable type."""
    text = _node_text(node_id)
    missing = [kw for kw in SYLLABLE_TYPE_KEYWORDS[node_id] if kw not in text]
    assert not missing, f"{node_id} does not name single-syllable pattern keyword(s): {missing}"


@pytest.mark.parametrize("node_id", ["rf-102", "rf-103"])
def test_syllable_type_names_short_vowel_misconception(node_id):
    """Syllable-type nodes name the common stumble: reading every vowel as short
    regardless of syllable type, with the correction that the type signals the
    vowel sound."""
    misc = " ".join(_misconceptions(node_id)).lower()
    assert "every vowel as short" in misc or "short regardless" in misc, (
        f"{node_id} lacks the read-every-vowel-as-short misconception: {_misconceptions(node_id)}"
    )
    assert "type" in misc, f"{node_id} misconception does not name the syllable type as the signal"


def test_first_multisyllabic_node_bridges_single_syllable_decoding():
    """The first S10 node (rf-102) lists a single-syllable automaticity node
    (rf-71 or rf-101) as a prerequisite, extending mastered single-syllable
    decoding to syllables within longer words."""
    prereqs = set(EXPECTED_PREREQS[FIRST_MULTISYLLABIC_NODE])
    bridge = prereqs & SINGLE_SYLLABLE_AUTOMATICITY
    assert bridge, f"{FIRST_MULTISYLLABIC_NODE} reaches no single-syllable automaticity prereq: {sorted(prereqs)}"
    assert "rf-101" in prereqs


# ── SYLLABLE-DIVISION: concrete, parent-deliverable procedure ─────────────


@pytest.mark.parametrize("node_id", DIVISION_NODES)
def test_division_node_carries_concrete_procedure(node_id):
    """The division nodes provide a concrete division procedure (a splitting verb
    plus a location cue), not merely the rule's name."""
    text = _node_text(node_id)
    has_split_verb = "split" in text or "divide" in text or "division" in text
    has_location_cue = (
        "between" in text
        or "vc/cv" in text
        or "v/cv" in text
        or "before it" in text
        or "before the" in text
        or "consonant before" in text
    )
    assert has_split_verb and has_location_cue, f"{node_id} lacks a concrete division procedure"


def test_division_node_has_step_sequence():
    """rf-105 (the general division node) gives a multi-step procedure in its
    scaffolding sequence."""
    steps = READING_FOUNDATIONAL_CONTENT["rf-105"]["teaching_guidance"]["scaffolding_sequence"]
    assert len(steps) >= 4, "rf-105 should give a step-by-step division procedure"


# ── COMPREHENSION connection for decoding-in-service-of-meaning nodes ─────


@pytest.mark.parametrize("node_id", ["rf-106", "rf-108", "rf-114"])
def test_decoding_node_ties_to_meaning(node_id):
    """Multisyllabic reading exists to read real text for meaning; these nodes
    frame longer-word decoding in service of meaning."""
    text = _node_text(node_id)
    assert "meaning" in text or "makes sense" in text, f"{node_id} does not tie decoding to meaning"


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"rf-{n}" in READING_FOUNDATIONAL_CONTENT, f"rf-{n} missing from content"
        assert f"read_f_{n}" in scope, f"read_f_{n} missing from scope_sequences"
        assert f"rf-{n}" in tnodes, f"rf-{n} missing from READING_FOUNDATIONAL template"


def test_counts_now_one_hundred_fifteen():
    assert len(READING_FOUNDATIONAL_CONTENT) == 115
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) == 115
    assert len(READING_FOUNDATIONAL.nodes) == 115


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


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-115) ─────────────


def test_library_ids_are_contiguous_no_gaps_no_duplicates():
    keys = list(READING_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate rf ids: {sorted(duplicates)}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing rf ids (gaps): {missing}"
    # In particular, there is no gap at rf-101 (the deferred capstone landed here).
    assert 101 in set(nums)
    assert top == 115, f"library top should be rf-115, got rf-{top}"
    assert set(nums) == expected, f"id set is not exactly rf-01..rf-{top}"


def test_cross_file_count_parity():
    content_count = len(READING_FOUNDATIONAL_CONTENT)
    scope_count = len(
        [t for t in get_scope_sequence("phonics_reading", "foundational") if str(t["ref"]).startswith("read_f_")]
    )
    template_count = len({tn.ref for tn in READING_FOUNDATIONAL.nodes if str(tn.ref).startswith("rf-")})
    assert content_count == scope_count == template_count == 115, (
        f"count mismatch: content={content_count}, scope={scope_count}, template={template_count}"
    )


def test_every_prerequisite_references_a_real_node():
    scope = _scope_by_ref()
    dangling: list[str] = []
    for ref, entry in scope.items():
        for p in entry.get("prerequisites", []):
            content_id = f"rf-{_num(p)}"
            content_id_padded = f"rf-{_num(p):02d}"
            if (
                content_id not in READING_FOUNDATIONAL_CONTENT and content_id_padded not in READING_FOUNDATIONAL_CONTENT
            ) or p not in scope:
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
        referenced = {f"rf-{m:02d}" for m in range(1, 116) if f"rf-{m:02d}" in text}
        referenced |= {f"rf-{m}" for m in range(1, 116) if f"rf-{m}" in text}
        assert referenced, f"{node_id} spiral_review references no rf node"
        for r in referenced:
            rn = _num(r)
            if f"rf-{rn}" not in READING_FOUNDATIONAL_CONTENT and f"rf-{rn:02d}" not in READING_FOUNDATIONAL_CONTENT:
                unresolved.append(f"{node_id} -> {r} (missing)")
            elif rn >= num:
                unresolved.append(f"{node_id} -> {r} (not earlier)")
    assert not unresolved, f"unresolvable spiral references: {unresolved}"


# ── Resolver + generator gates (DB) ──────────────────────────────────────


@pytest.mark.parametrize("ref", NEW_REFS)
async def test_resolver_resolves_each_new_ref(db_session, household, ref):
    res = await resolve_ref_to_uuid(db_session, ref, household.id)
    assert res.node_uuid is not None, f"{ref} did not resolve to a UUID"
    assert res.unresolved is None


async def test_generator_plan_reading_tier_zero_needs_content(db_session, household):
    """needs_content drops by exactly 15: before this batch, 100 of the 115 reading
    refs resolved (rf-01..rf-100) and 15 were needs_content (rf-101..rf-115); now all
    115 resolve, so the full 115-topic plan has zero needs_content weeks and 115
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
    assert len(resolved_ids) == 115

    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
