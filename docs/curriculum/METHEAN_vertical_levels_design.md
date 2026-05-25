# METHEAN vertical level structure: design and scope scaffold

Status: design only. No lesson nodes authored. Output is a single design
doc, a small scaffold of three empty level keys in `scope_sequences.py`,
and three sample topic-metadata entries as the gold-standard target for
the one authoring gap I found.

## 1. Goal

Define the level structure above foundational for the five core
subjects (mathematics, reading, writing, science, history) so the
vertical curriculum can be authored coherently against a stable scope-
and-sequence skeleton, and confirm the lesson-node shape that vertical
authoring will reuse.

## 2. Investigation: what already exists

What I found does not match what the goal statement assumes. The
scope-and-sequence skeleton above foundational is largely already in
place; the gap is in authored lesson nodes, not in the topic-metadata
skeleton. Honest report of the actual state:

### 2.1 The level ladder is already defined

`backend/app/core/learning_levels.py` defines `LEARNING_LEVELS` with
five tiers: `foundational`, `developing`, `intermediate`, `advanced`,
`mastery`. The system is per-subject, per-child, parent-defined:

> A child can be 'advanced' in math and 'foundational' in Latin
> simultaneously.

This is the right design and is the ladder this proposal recommends
keeping. No new level names. No grade banding (a grade-banded scheme
would lose the per-subject claim the existing model makes).

### 2.2 `SCOPE_SEQUENCES` is populated across most of the matrix

`backend/app/content/scope_sequences.py` already holds topic-metadata
across most subject/level pairs. Counts as found:

| subject (scope id) | f | d | i | a | m | total |
|---|---|---|---|---|---|---|
| `mathematics` | 30 | 30 | 35 | 30 | 25 | **150** |
| `phonics_reading` | 25 | 25 | — | — | — | **50** |
| `writing_grammar` | 20 | 25 | 25 | 20 | 15 | **105** |
| `science` | 20 | 25 | 25 | 20 | 15 | **105** |
| `history` | 20 | 25 | 25 | 20 | 13 | **103** |
| `literature` (6th) | — | — | 25 | 20 | 15 | **60** |

Each entry in those lists is a real topic-metadata dict with `ref`,
`title`, `description`, `prerequisites`, `estimated_weeks`,
`key_concepts`, `assessment_indicators`, `classical_alignment`,
`charlotte_mason_alignment`, and `standard_alignment`. Math mastery
includes calculus topics (`math_m_01` Limits Intuitive Understanding,
`math_m_02` Limits Formal Definition with epsilon-delta). Writing
mastery includes academic rhetoric. Science mastery includes AP-level
content. History mastery extends to the modern period and historiography.

The skeleton above foundational is real, sequenced, and standards-
aligned. The user's goal statement assumed it was empty; it is not.

### 2.3 The actual scope-skeleton gaps

Four of five core subjects are complete across all five levels. The
only core-subject scope-skeleton gap is:

- **`phonics_reading`**: intermediate, advanced, mastery — three levels
  missing.

The 6th subject `literature` is the inverse: foundational and
developing are missing. This appears intentional: the design implied
by the existing scope_sequences is that reading-as-decoding lives in
`phonics_reading` (early), reading-as-analysis lives in `literature`
(later), and the two together form the reading ladder.

I address both in section 6.

### 2.4 Authored lesson nodes are only at foundational

The per-topic lesson-node content files in
`backend/app/content/<subject>_foundational_content.py` are authored
at full apparatus for foundational only:

| content file | authored nodes |
|---|---|
| `math_foundational_content.py` | 30 (matches 30 math foundational topics) |
| `reading_foundational_content.py` | 25 (matches 25 phonics_reading foundational topics) |
| `writing_foundational_content.py` | 20 (matches 20 writing_grammar foundational topics) |
| `science_foundational_content.py` | 20 (matches 20 science foundational topics) |
| `history_foundational_content.py` | 20 (matches 20 history foundational topics) |

Each foundational node uses the proven shape documented in
`backend/app/services/node_content.py::NODE_CONTENT_SCHEMA`:
`learning_objectives`, `teaching_guidance` (introduction,
scaffolding_sequence, socratic_questions, practice_activities,
real_world_connections, common_misconceptions), `assessment_criteria`,
`philosophy_specific` (five native shapes: traditional, classical,
charlotte_mason, montessori, unschooling), `practice_items`,
`assessment_items`, `media`, `passages`, `widgets`, `accommodations`,
`time_estimates`. This is the model vertical authoring will reuse.

### 2.5 What the vertical authoring task actually is

Given 2.2 through 2.4, the vertical-authoring task is:

1. **Author lesson nodes** for every above-foundational topic the
   scope-and-sequence already names. The math developing scope has 30
   topics; 30 new lesson nodes need authoring in a new
   `math_developing_content.py`, each using the foundational node shape
   with the full five-philosophy `philosophy_specific` block. Same for
   math intermediate (35 nodes), math advanced (30), math mastery (25).
   Same arithmetic across writing, science, history.
2. **Fill the one scope-skeleton gap**: scaffold `phonics_reading`
   intermediate / advanced / mastery, and either populate them with
   reading-mechanics topics (recommended) or document explicitly that
   `literature` takes over.

The scope-and-sequence skeleton above foundational is largely the
*input* to vertical authoring, not the *output* of it.

## 3. Level ladder, confirmed

| level | semantic | typical entry age (per-child, not enforced) |
|---|---|---|
| `foundational` | building core concepts; no prerequisites assumed | early (whenever a child begins formal work in the subject) |
| `developing` | working through fundamentals; some foundation in place | following foundational; varies by child |
| `intermediate` | solid foundation; ready for deeper exploration | following developing |
| `advanced` | strong mastery of fundamentals; ready for complex work | following intermediate |
| `mastery` | deep expertise; self-directed; teaching others; original work | following advanced |

The ages above are typical, not enforced. The system holds that a
child can be `mastery` in math and `developing` in foreign language.
Grade banding (K-2 / 3-5 / 6-8 / 9-12) was considered and rejected for
this proposal because it would impose a coupling the existing model
intentionally avoids and would conflict with `get_level_for_subject`
and the rest of `learning_levels.py`.

## 4. Lesson-node shape, confirmed

Vertical lesson nodes (`md-01`, `md-02`, ..., `wd-NN`, `si-NN`, etc.)
reuse the foundational node shape exactly. Concretely each above-
foundational node carries:

- `enriched: true`
- `learning_objectives: [list]`
- `teaching_guidance: {introduction, scaffolding_sequence, socratic_questions, practice_activities, real_world_connections, common_misconceptions}`
- `assessment_criteria: {mastery_indicators, assessment_methods, sample_assessment_prompts}`
- `philosophy_specific: {traditional, classical, charlotte_mason, montessori, unschooling}` with each variant's native shape per `NODE_CONTENT_SCHEMA`
- `practice_items: [list]` with `{type, difficulty, prompt, expected_type, correct_answer, hints, explanation}`
- `assessment_items: [list]`
- `accommodations: {dyslexia, adhd, gifted, visual_learner, kinesthetic_learner, auditory_learner}`
- `time_estimates: {first_exposure, practice_session, review_session, estimated_sessions_to_mastery}`

The vertical authoring engine therefore is the proven foundational
engine pointed at the above-foundational scope topics. The five-
philosophy treatment is preserved at every band; the philosophies do
not collapse upward into a single voice. This matches the design
commitment in `node_content.py`'s schema documentation and the
existing foundational nodes' implementation.

For ID conventions, the recommended pattern follows the foundational
short-prefix convention:
- math: `mf-NN` (foundational, existing), `md-NN` (developing), `mi-NN`
  (intermediate), `ma-NN` (advanced), `mm-NN` (mastery)
- writing: `wf-NN`, `wd-NN`, `wi-NN`, `wa-NN`, `wm-NN`
- science: `sf-NN`, `sd-NN`, `si-NN`, `sa-NN`, `sm-NN`
- history: `hf-NN`, `hd-NN`, `hi-NN`, `ha-NN`, `hm-NN`
- reading: `rf-NN`, `rd-NN`, `ri-NN`, `ra-NN`, `rm-NN`

Each subject/level gets its own content file:
`math_developing_content.py`, `math_intermediate_content.py`, and so
on. Each file is a flat dict keyed by node id, matching the existing
foundational files' shape exactly.

## 5. Recommended authoring order

The order below maximizes the consumer wedge: the experience a family
can have with METHEAN past the foundational entry. Each authoring
unit is one subject/level pair (e.g. math developing = 30 nodes).
Recommended sequence:

**Phase 1 (continuity wedge for the youngest enrolled families)**

1. **math developing** (30 nodes). The single most-asked-for next step
   after foundational. The scope is well-defined (three-digit operations,
   place value, multiplication and division facts and algorithms,
   fractions introduction). The proof that METHEAN math continues
   past K-2.
2. **reading developing** (25 nodes; already in scope). Bedrock pair
   with math; lets families continue past phonics into early elementary
   reading.

**Phase 2 (round out elementary)**

3. **writing developing** (25 nodes). Writing extends naturally from
   reading; sentence- and paragraph-level work that families ask for.
4. **science developing** (25 nodes).
5. **history developing** (25 nodes).

**Phase 3 (deepen the bedrock pair before broadening)**

6. **math intermediate** (35 nodes; the largest single level). Middle
   school math — fractions, decimals, percentages, ratios, pre-algebra.
   Continues the math depth wedge.
7. **reading intermediate** (gap: see section 6; author the
   intermediate-band reading mechanics nodes after the scope-skeleton
   is filled).

**Phase 4 (round out middle)**

8. writing intermediate (25)
9. science intermediate (25)
10. history intermediate (25)

**Phase 5 (high school depth)**

11. math advanced (30) — algebra, geometry
12. reading advanced (gap: see section 6)
13. writing advanced (20)
14. science advanced (20)
15. history advanced (20)

**Phase 6 (mastery; advanced/AP work)**

16. math mastery (25) — pre-calculus, calculus
17-20. mastery for reading, writing, science, history (gap on reading)

This sequence keeps the consumer-wedge value compounding: a family
who picks METHEAN at K can see depth in math and reading first
(Phase 1), then breadth at developing (Phase 2), then depth again in
math (Phase 3), and so on.

### Prerequisite-threading rule

Each level builds on the one below. Concretely:
- A developing topic's `prerequisites` may name foundational topic refs
  (e.g. `math_d_01` prereqs `["math_f_07", "math_f_08", "math_f_09"]`,
  which is already the case in the existing math developing scope).
- An intermediate topic's `prerequisites` may name developing or
  foundational topic refs.
- And so on upward.

The scope-and-sequence prerequisites already follow this convention
for math, writing, science, history. The vertical lesson nodes will
inherit the same prerequisite structure: the lesson node for a topic
inherits the topic's prerequisites from the scope-and-sequence entry,
plus any node-level prerequisites the authoring may add (per the
existing per-node `prerequisite_skills_from_other_subjects` field in
`NODE_CONTENT_SCHEMA`).

A guard test analogous to the literature strand's
`test_all_prerequisites_resolve_to_authored_nodes` should be added
when above-foundational lesson nodes start landing, to catch dangling
prerequisite refs early.

## 6. The phonics_reading scope-skeleton gap

`phonics_reading` has only foundational and developing populated in
scope_sequences. Three levels are missing. The design choice the
existing code reflects is ambiguous:

- **Option A**: `phonics_reading` covers foundational + developing
  only (early-reading subject); higher-level reading work moves into
  `literature` (which is populated at intermediate / advanced /
  mastery). The two together form the reading ladder.
- **Option B**: `phonics_reading` covers all five levels (reading
  mechanics, fluency, vocabulary, comprehension strategies, study
  skills continue developing through high school); `literature`
  covers literary analysis (a distinct skill set, the lit-craft
  strand we have built out separately).

**This proposal recommends Option B.** The reasoning:

1. Reading mechanics continue developing past elementary. Fluency
   rate, vocabulary depth, comprehension strategy, study skills, and
   reading stamina are real reading skills distinct from literary
   analysis, and they continue advancing through high school.
2. The 5-level ladder is uniform across the other four core subjects;
   keeping `phonics_reading` 2-level is an inconsistency.
3. The existing `literature` track (with its 60 scope topics +
   lit-craft + lit-work strands already authored) is rich enough to
   stand on its own as the analytical-reading subject without
   absorbing reading-mechanics work.
4. A family wanting to continue reading-mechanics work past developing
   should have a place to do so; Option A leaves that place empty.

Per the recommendation, this proposal scaffolds the three empty
`phonics_reading` level keys in `scope_sequences.py` as empty lists,
and populates 3 sample topic-metadata entries in the intermediate
slot as the gold-standard target for the authoring engine. Section 7
documents the scaffold.

For `literature`: the missing foundational/developing levels are left
as a design decision deferred to a separate proposal. The literary
mastery strand (`lit-craft-001` through `lit-craft-053` plus the
`lit-work-NNN` nodes) handles the deeper analytical reading already,
and authoring `literature` foundational/developing in the
scope-and-sequence form might duplicate work or might honestly fill
a gap; either way it is a separate decision from this proposal.

## 7. Scaffolds and sample

This proposal commits one small change to `scope_sequences.py`:

1. Add three new keys `SCOPE_SEQUENCES["phonics_reading"]["intermediate"]`,
   `SCOPE_SEQUENCES["phonics_reading"]["advanced"]`, and
   `SCOPE_SEQUENCES["phonics_reading"]["mastery"]`.
2. The `advanced` and `mastery` keys are scaffolded as empty lists
   `[]`, with a comment naming them as the scaffold awaiting authoring.
3. The `intermediate` key is populated with three sample topic-metadata
   entries (`read_i_01`, `read_i_02`, `read_i_03`) as the gold-standard
   target for the authoring engine. The three sample topics are honest
   intermediate-band reading skills distinct from the literature
   track's literary analysis: fluency-at-grade-level, vocabulary
   through morphology, and inference. They follow the same
   topic-metadata shape as the existing `math_i_NN` and `writ_i_NN`
   entries (ref, title, description, prerequisites, estimated_weeks,
   key_concepts, assessment_indicators, classical_alignment,
   charlotte_mason_alignment, standard_alignment).

No lesson nodes are authored in this proposal. The full lesson-node
content files (`reading_intermediate_content.py` etc.) are deferred to
the authoring runs that follow this proposal's approval.

For the other four core subjects (math, writing, science, history),
no scope-and-sequence scaffolding is required: all five level keys
are already populated with rich topic-metadata. Those subjects'
existing scope entries already serve as the gold-standard target for
the authoring engine. The authoring runs need only point the engine
at them.

## 8. Implications for the authoring engine

When authoring runs are initiated against this scope-and-sequence
skeleton:

1. For each subject/level pair, create a new content file (e.g.
   `math_developing_content.py`) following the foundational file's
   shape: a flat dict keyed by node id (`md-01`, `md-02`, ...).
2. Each lesson node uses the full apparatus per `NODE_CONTENT_SCHEMA`,
   including the five-philosophy `philosophy_specific` block.
3. Each lesson node's `prerequisites` (in its content payload, if
   carried) and the scope-and-sequence topic's `prerequisites` agree.
4. A guard test asserts: every authored lesson node id matches a
   topic ref in the corresponding scope-and-sequence level; every
   topic ref in the scope-and-sequence level has an authored lesson
   node by the time the level is "complete"; every prerequisite ref
   on every lesson node resolves to an authored node.

When the engine is ready, the first run is math developing (30
nodes) per the order in section 5.

## 9. What this proposal does NOT do

- No lesson nodes authored.
- No schema changes; the foundational `NODE_CONTENT_SCHEMA` already
  supports the vertical authoring.
- No new level names; the existing 5-level ladder
  (foundational/developing/intermediate/advanced/mastery) is reused.
- No grade banding.
- No scope-and-sequence rewrites for math, writing, science, history;
  the existing topic-metadata is preserved unchanged.
- No literature foundational/developing decision; that is a separate
  proposal.

## 10. Asks for review

1. Approval of the level ladder (the existing 5; no grade banding).
2. Approval of Option B for phonics_reading (5-level ladder; reading
   mechanics distinct from literary analysis).
3. Approval of the recommended authoring order in section 5 (math
   developing first; reading developing in parallel; round out
   elementary; deepen the bedrock pair).
4. Acknowledgement of the scope-and-sequence skeleton's actual state
   (largely populated for math/writing/science/history; the
   investigation showed the assumption in the goal statement was off).
