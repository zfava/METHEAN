# METHEAN trades and skilled-work curriculum: design proposal

Status: design only. No curriculum nodes, no schema code changes. This document
proposes the content model; authoring follows on sign-off.

## 1. Scope and intent

A content model for trades and skilled work that fits the existing METHEAN
architecture: competency-based, project-based, apprenticeship-style learning
where competence is judged by the quality of real output and safe correct
practice. Oriented to a homesteading and self-reliance path.

The academic content model already in METHEAN was built for lessons. A trade
is not mastered by lessons and recitation: it is mastered by demonstrated
doing (build it, fix it, grow it, run it). This document proposes a parallel
content shape that reuses the existing DAG, node, edge, plan, attempt, and
artifact machinery, and names the small extensions needed to honor safety as
a first-class gating concern.

## 2. Architecture investigation: what already fits

The investigation below is what the existing repo supports today.

### 2.1 The DAG and node machinery fit trades unchanged
`backend/app/models/curriculum.py` defines `LearningMap`, `LearningNode`,
`LearningEdge`, `LearningMapClosure`, `ChildMapEnrollment`. None of these are
academic-specific. `LearningEdge` carries `relation` (prerequisite |
corequisite | recommended) and a `weight`. A trade's competency graph is a
DAG with prerequisites; this fits.

### 2.2 `NodeType` already carries vocational types
`backend/app/models/enums.py`:

```
class NodeType(str, enum.Enum):
    # Academic
    root, milestone, concept, skill
    # Vocational
    safety, knowledge, technique, project, certification_prep
    ...
```

The five vocational node types are already enumerated. `safety` exists as a
distinct first-class type, which is what the trades design needs. The trades
model proposed below uses `safety`, `technique`, and `project` directly;
`knowledge` for the few cases where a trade has a real cognitive prereq
(reading a wiring diagram, understanding the calorie-counter on an animal
feed bag); `certification_prep` left for trades that lead to a real
external credential.

### 2.3 `AssessmentType` already carries vocational types
`backend/app/api/spec_coverage.py` already defines, alongside the academic
set:

```
"vocational": [
    "practical_demo",
    "weld_inspection",
    "clinical_evaluation",
    "lab_report",
    "competency_signoff",
    "safety_check",
    "tool_qualification",
],
```

Trades will use `practical_demo`, `competency_signoff`, `safety_check`, and
`tool_qualification` directly. `weld_inspection` and `clinical_evaluation`
are domain-specific and already wait for their trades.

### 2.4 `SUBJECT_CATALOG["vocational"]` already lists thirteen trades
`backend/app/core/learning_levels.py` already has woodworking, electrical,
welding, automotive, plumbing, hvac, cooking_nutrition, agriculture,
sewing_textiles, small_engine, construction, first_aid, entrepreneurship.
The proposal below uses this list as the source of truth and recommends
which to author first.

### 2.5 The vocational prompts are written for an apprenticeship pedagogy
`backend/app/ai/prompts.py` carries `VOCATIONAL_CURRICULUM_SYSTEM` and
`VOCATIONAL_TUTOR_SYSTEM`. The curriculum prompt's RULES include "SAFETY is
always the first node. It is a prerequisite for ALL hands-on work" and "Tool
identification and care comes before tool use" and "Assessment is primarily
by demonstration and output quality." The pedagogy this document proposes
matches what the prompts already ask for; authoring the content lets the
prompts actually have content to plan with.

### 2.6 The planner branches on `is_vocational`
`backend/app/services/annual_curriculum.py:186-196` selects
`VOCATIONAL_CURRICULUM_SYSTEM` when the subject is vocational. The planner
treats vocational subjects as first-class today; it just lacks authored
nodes to plan against.

### 2.7 The Artifact and Attempt models support evidence by output
`backend/app/models/evidence.py` defines `Artifact` (photo, video, document,
audio, link) attached to attempts. `backend/app/models/governance.py`'s
`Attempt` carries `score`, `duration_minutes`, `feedback` (JSONB), and links
to artifacts. A trade competency's demonstration is a photo or video plus a
mentor signoff: the evidence shape exists.

### 2.8 The fitness templates are the closest existing analog
`backend/app/services/fitness_templates.py` carries a content payload of
`benchmark_criteria` + `assessment_type (timed | counted | pass_fail |
observed)` + `measurement_unit` + `suggested_frequency`. This is the right
neighborhood for trades: concrete, demonstrable, measurable, frequent
practice. The trades model below extends this pattern with safety, tools,
materials, mentor signoff, and the apprenticeship pedagogy block.

### 2.9 `MasteryLevel` will hold helper-to-journeyman semantics directly
`MasteryLevel(not_started, emerging, developing, proficient, mastered)` can
host the trades progression without a schema change. The semantics shift:
`emerging` is helper, `developing` is apprentice, `proficient` is
journeyman-level, `mastered` is qualified. The UI surface label changes per
subject category; the enum stays.

## 3. Where the academic lesson-shaped model does NOT fit

Listed precisely because the design must depart from the academic shape at
exactly these points.

| Academic shape | Why it does not fit a trade |
|---|---|
| `learning_objectives` (cognitive verbs) | A trade objective is a thing a learner does, not a thing they understand. "Cut to a line" is the objective, not "understand cutting." |
| `teaching_guidance.scaffolding_sequence` | A trade is scaffolded by the apprenticeship pattern (I do, we do, you do supervised, you do unsupervised), not by cognitive scaffolding. |
| `teaching_guidance.socratic_questions` | A skill is demonstrated by output, not surfaced by discussion. The trade equivalent is the mentor's running check ("show me your kerf" / "where is your finger") which is a different speech act. |
| `practice_items` (prompts with correct_answer, hints, explanation) | There is no correct_answer to a board cut. The answer is the cut. |
| `assessment_criteria.mastery_indicators` (observable but written) | Replace with `demonstration_criteria` (observable and measurable on the work itself). |
| `assessment_methods` (oral narration, written work) | Replace with `practical_demo`, `competency_signoff`, `safety_check`, `tool_qualification`. |
| The five-philosophy frame (classical / charlotte_mason / montessori / traditional / unschooling) | A trade has one pedagogy, the apprenticeship pattern. The five philosophies were honest about literature because each had a distinct native claim; they have no distinct native claim about cutting a tenon. The trades model proposes a single `pedagogy` block describing the apprenticeship pattern, not a five-way variant dict. |
| `band` (emerging → mastery) as a comprehension ladder | The same enum is used, but the semantics are helper → qualified, defined by the supervision and independence the learner has earned, not by analytic depth. |

## 4. The trades content model

Two content shapes: `competency` and `project`. Both live as
`LearningNode.content` payloads, the same way academic and literature
content do. Both reuse the existing DAG.

### 4.1 The competency shape (a thing a learner must be able to DO)

Fields:

```
{
    "node_type": "technique" | "safety" | "knowledge" | "certification_prep",
    "trade": "<one of SUBJECT_CATALOG['vocational'] ids>",
    "competency_name": "<short, doing-shaped name>",
    "progression_band": "helper" | "apprentice" | "journeyman" | "qualified",
    "prerequisites": [<list of competency or safety node ids/refs>],
    "safety_basis": {
        "hazards": [<the actual hazards: blade, electrical, fume, chemical, biological, heat, pinch, fall>],
        "ppe_required": [<what the learner must be wearing: eye, ear, gloves
            (note: gloves are forbidden for some power tools), boots, hair
            tied back, no loose sleeves, respirator with named cartridge>],
        "supervision_required": true | false,
        "supervision_basis": "<one sentence on why and to what standard>",
        "fresh_safety_signoff_within_days": <int | null>
    },
    "tools_required": [
        {"name": "<tool>", "specification": "<size, type, condition>",
         "alternatives": ["<acceptable substitutes, if any>"]}
    ],
    "materials_required": [
        {"name": "<material>", "quantity": "<amount>",
         "approximate_cost_usd": <number | null>}
    ],
    "workspace_requirements": {
        "surface": "<flat workbench, level ground, etc>",
        "ventilation": "<none required | open air | active extraction>",
        "lighting": "<natural | task lighting required>",
        "power": "<none | 15A 120V | 20A 240V | other>",
        "containment": "<none | drop cloth | enclosed booth>"
    },
    "skill_description": "<plain prose, one paragraph, what the doing looks
        like; what it feels like in the hand; what the eye watches for>",
    "demonstration_criteria": [
        "<each criterion measurable on the work itself; e.g., 'kerf falls on
            the waste side of the line, no further than 1/32 inch from the
            line, across the full length of the cut'>"
    ],
    "common_errors": [
        {"error": "<named failure mode>", "cause": "<what the learner did>",
         "remedy": "<what to try next>"}
    ],
    "artifact_expected": {
        "type": "photo" | "video" | "document" | "audio",
        "what_to_capture": "<a workpiece, a setup, a process step>",
        "what_the_evidence_shows": "<the criteria that can be read from the
            artifact alone>"
    },
    "mentor_signoff_required": true | false,
    "pedagogy": {
        "i_do": "<mentor demonstrates: what the mentor names and shows>",
        "we_do": "<mentor and learner share the work, with named transition
            points where the learner takes over>",
        "you_do_supervised": "<learner performs, mentor on premises watching,
            with a named threshold for when to intervene>",
        "you_do_unsupervised": "<learner performs alone; the condition for
            entering this stage is the prior demonstration plus mentor
            signoff>"
    },
    "estimated_practice_sessions_to_signoff": <int>,
    "session_length_minutes": <int>,
    "related_projects": [<list of project node refs that exercise this
        competency>]
}
```

### 4.2 The project shape (a real piece of work that demonstrates competencies)

Fields:

```
{
    "node_type": "project",
    "trade": "<vocational subject id>",
    "project_name": "<short, build-it-shaped name>",
    "progression_band": "helper" | "apprentice" | "journeyman" | "qualified",
    "competencies_exercised": [<list of competency node refs>],
    "prerequisites": [<list; typically the safety competencies and the named
        techniques required to begin>],
    "safety_briefing": {
        "hazards_specific_to_this_project": [<>],
        "ppe_required": [<>],
        "supervision_required": true | false,
        "supervision_basis": "<>",
        "fresh_safety_signoff_within_days": <int | null>
    },
    "tools_list": [<as in competency, but project-scoped>],
    "materials_list": [<as in competency, but project-scoped>],
    "estimated_total_hours": <number>,
    "workspace_requirements": {<as in competency>},
    "staged_milestones": [
        {
            "milestone_name": "<>",
            "what_is_done": "<>",
            "artifact_expected": "<photo or video at this stage>",
            "approximate_hours_to_reach": <number>
        }
    ],
    "success_criteria": [
        "<each criterion measurable on the finished work itself; honest and
            specific (e.g., 'the bench supports a 200lb adult standing on it
            without visible rocking on a flat floor')>"
    ],
    "mentor_signoff_required": true | false,
    "portfolio_record": {
        "what_enters_the_portfolio": "<the completed object, plus the
            staged-milestone artifacts; this is the child's evidence of
            skilled work that persists across years>",
        "kept_by_the_household": true
    },
    "follow_on_projects": [<refs that build on this one>]
}
```

### 4.3 What the trades model does NOT carry

- `learning_objectives`, `teaching_guidance`, `practice_items`,
  `assessment_criteria` in their academic dict shape: omitted. The
  equivalent information lives in `skill_description`,
  `demonstration_criteria`, `pedagogy`, and `common_errors`.
- The five-philosophy dict: omitted. The trade pedagogy is a single
  `pedagogy` block. No `philosophy_neutral` either: there is nothing to be
  neutral about.
- Socratic questions, seminar questions, writing invitations: omitted.

## 5. Progression model

The existing `MasteryLevel` enum is reused. The enum values stay; the
semantics map onto trades as follows:

| `MasteryLevel` value | Trades band | What this means in the shop |
|---|---|---|
| `not_started` | unstarted | Learner has not yet attempted the competency. |
| `emerging` | helper | Learner can assist a mentor's project; mentor handles the dangerous and decisive parts. Learner does setup, marking, fetching, finishing. |
| `developing` | apprentice | Learner can perform most steps with mentor checking key cuts, joints, or connections. Mentor on premises, attention divided. |
| `proficient` | journeyman | Learner completes the competency independently to acceptable quality. Mentor available but not required step by step. |
| `mastered` | qualified | Learner performs the competency reliably under varied conditions. Can teach a helper through the helper-band steps. |

Above qualified (using the existing `mastery` band reserved by the literary
strand for the same purpose): the learner is doing original projects,
adapting techniques, mentoring through whole projects.

The UI surface label is per subject category. Internally the enum is one.

### 5.1 What signoff each band requires

| Band | Signoff requirement |
|---|---|
| helper | None required. Helper work is supervised in any case. |
| apprentice | Mentor `competency_signoff` (an `Attempt` with `AssessmentType.competency_signoff` whose `score` is the mentor's pass call, with `feedback` JSON capturing the demonstration criteria checked off). |
| journeyman | Three independent demonstrations across at least three separate sessions, with artifact evidence for each, plus a mentor `competency_signoff` that the work was unprompted. |
| qualified | A journeyman-band signoff PLUS the learner having signed off a helper-band attempt for another learner (taught the helper steps), OR a project of journeyman-band scope completed entirely unsupervised. |

The number-three threshold for journeyman is a starting recommendation, not a
schema constant; authoring may tune it per trade.

## 6. Safety as first-class gating

This is the single most important departure from the academic model.

### 6.1 The contract
A learner may not advance past a competency whose safety basis is not
demonstrated and signed off. This is gating, not advisory.

### 6.2 How it is wired into the existing DAG
- Every trade has at least one `NodeType.safety` competency at the entry of
  its DAG. Concrete first safety competencies: `ws-001` "Shop safety: hand
  tools and the workbench" for woodworking; `we-001` "Electrical safety:
  lockout-tagout, the meter, and the panel" for electrical; `wf-001` "Fire,
  fume, and UV safety: the welding hood, the booth, and the extinguisher"
  for welding; `aa-001` "Animal handling safety: stance, escape route, large
  animal awareness" for agriculture with livestock.
- Safety competencies use `AssessmentType.safety_check`.
- Every hands-on competency in the trade has a `prerequisite` edge to the
  relevant safety competency.
- `mentor_signoff_required` is `true` for every safety competency. No
  self-attestation.

### 6.3 The freshness check (the small extension required)
Safety competencies need not just "ever signed off" but "currently signed off
within N months." Today's `LearningEdge` is binary. The proposal: add an
optional `freshness_days` to `LearningEdge.metadata` (the table has no
metadata column today; this is the smallest schema extension, a single new
nullable JSONB column on `learning_edges`, OR equivalently encoded in
`LearningNode.content` of the dependent competency as a `safety_basis.
fresh_safety_signoff_within_days` field with the planner enforcing it).

The second option requires no schema change. The trades model's
`safety_basis.fresh_safety_signoff_within_days` field (already in section
4.1) is the preferred encoding. The planner reads it, looks at the most
recent `Attempt` of `AssessmentType.safety_check` on the named safety
competency, and refuses to schedule any dependent competency whose safety is
stale. This is a planner change, not a schema change.

### 6.4 Adult supervision as a trade-level default
Some trades carry hazard high enough that supervision is the default for the
entire trade until the qualified band. The trade-level default is encoded in
the trade's root node (a `NodeType.root` or trade-overview node) and read by
the planner before scheduling any project. The trades whose default is
"adult supervision required through journeyman":

- Welding and metalwork
- Electrical
- Automotive (under-vehicle work, fuel system, battery work)
- Woodworking with power tools (any tool with a rotating blade or bit)
- Pressure canning in food preservation
- Large-animal husbandry (cattle, horses, hogs of significant weight)

Hand-tool woodworking, sewing, dry food preservation, small-animal
husbandry, and most agriculture below the large-animal line are
supervised-at-helper-band but can move to unsupervised practice at apprentice
band with a clear safety signoff.

### 6.5 Honesty about what the model does and does not do
This model does not make trade work safe. It makes the safety basis
explicit, gating, and reviewable. The parent or mentor is the safety
authority. The product's role is to refuse to schedule unsafe practice and
to make the safety state legible.

## 7. The prerequisite graph for trades

### 7.1 What the existing machinery handles unchanged
- Vertical prereqs within a trade: helper-band feeds apprentice-band feeds
  journeyman-band. `LearningEdge.relation = prerequisite`. Done.
- Cross-trade shared skills: a `shared_skills` learning map containing
  competencies like "read a tape measure to 1/16 inch", "use a digital
  caliper", "use a torque wrench", which other trade maps reference by
  cross-map prerequisite. The DAG supports this; the planner already loads
  all enrolled maps.
- Corequisites (two competencies that must be learned together, neither
  before the other): `LearningEdge.relation = corequisite`. Used for, for
  example, "stance for the saw cut" and "marking the line": neither makes
  sense without the other.

### 7.2 The one place the machinery must extend
The freshness check on safety prerequisites, as in section 6.3. The
proposal is to encode it in `LearningNode.content` rather than schema, so no
migration is required.

### 7.3 What does NOT need a change
- The DAG itself.
- `ChildNodeState.is_unlocked` and `mastery_level`.
- `Activity` with `ActivityType.project`.
- `Attempt` and `Artifact`.
- The annual-curriculum generator (it already branches on vocational).
- The plan generator.

## 8. Starter set of trades

Oriented to homesteading and self-reliance. One-line rationale per trade. In
order of recommended pilot priority.

| # | Trade (catalog id) | One-line rationale |
|---|---|---|
| 1 | woodworking | Foundational manual literacy; safe at helper band with hand tools; small affordable tool set; output is real furniture. |
| 2 | construction | Builds on woodworking; needed for shelter, fence, shed, and the workbench itself. |
| 3 | agriculture | Multi-year practice; daily and unavoidable on a homestead; safety profile is different (large animal, food safety) but the practice is constant. |
| 4 | cooking_nutrition (extended to preservation) | Daily practice, low hazard except pressure canning; compounds with agriculture; seasonal cadence. |
| 5 | small_engine | Mechanical literacy on the homestead's real machines (mower, generator, pump). |
| 6 | automotive | Higher-stakes mechanical work; full adult supervision through journeyman. |
| 7 | plumbing | Needed for any inhabited structure; failure modes are visible; lower hazard than electrical. |
| 8 | electrical | High hazard; learn alongside a licensed electrician or in a defined supervised path; default supervised through journeyman. |
| 9 | welding | High hazard (UV, fume, fire); requires dedicated PPE and ventilation; defer until shop foundations are in. |
| 10 | sewing_textiles | Real practical-life skill; low hazard; high learn-to-do return. |
| 11 | first_aid | Distinct from other trades: practice is on simulated patients; partner with a recognized curriculum (Red Cross / AHA). |
| 12 | hvac | Cross-cutting (electrical + refrigerant handling); defer until electrical foundations are in. |
| 13 | entrepreneurship | Different category (business literacy); fits the model but is not skilled physical work; lowest pilot priority for the trades track. |

### 8.1 Recommended first pilot: woodworking, hand-tool first

Authoring should begin with **woodworking** for these reasons:

1. **Lowest entry hazard with adult supervision in place.** Hand tools cut
   slowly. A panel saw, a marking gauge, a chisel, a plane: none of these
   start without the learner starting them. Power tools enter later, behind
   their own safety gate.
2. **Tool set is small, affordable, and durable.** A learner can be fully
   equipped to build a workbench with under twenty tools, each of which
   lasts decades.
3. **Project ladder is well-established and pedagogically clean.** Saw
   bench, then tool tote, then shooting board, then small bookshelf, then
   the workbench itself, then joinery exercises (mortise-and-tenon,
   dovetail), then small furniture. Every project exercises competencies the
   next project reuses.
4. **The tradition is well-documented.** Roy Underhill's televised work,
   Christopher Schwarz's `The Anarchist's Tool Chest`, Paul Sellers's
   teaching, the pre-industrial period of the trade. We do not have to
   invent the curriculum; we have to author it from the tradition.
5. **The competencies built are foundational for the other trades.**
   Measure, mark, square, cut, fasten, finish: every other physical trade
   on the list reuses these. A learner who has done two years of hand-tool
   woodworking comes to construction, plumbing, and automotive already
   knowing what a square line means.
6. **Failure modes are honest and visible.** A saw cut that wanders is
   plain. The mentor signoff is grounded in what the parent can see on the
   wood.
7. **Output is portfolio-grade artifacts the child keeps and uses.** The
   saw bench in the family's shop, decades later, is the proof.

The other trades will be authored against the patterns the woodworking pilot
establishes. Welding and electrical will require additional safety
ceremonies the woodworking pilot does not need; the design above already
accommodates them.

## 9. Gold-standard worked example

The literature strand uses `lit-craft-031` (the unreliable narrator) as its
gold standard: a single fully realized node that sets the bar for the
strand. The trades model needs the same. The competency below is the
proposed gold standard for woodworking. It is authored as a design example,
not as a curriculum node; it is reproduced here in the design doc and
nowhere else in the repo.

The competency is intentionally at the apprentice band rather than helper.
Helper-band competencies are minimal by design (most fields are short). The
apprentice-band example exercises every field of the model honestly.

The competency is true to real hand-tool practice. The PPE recommendation,
the hazards, the demonstration criteria, the common errors, and the
pedagogy are drawn from the tradition (Underhill, Schwarz, Sellers) and
from how the work actually goes in a shop. Nothing in this example is
invented or unsafe.

---

### `wc-021` Cross-cut to a line with a panel saw

```yaml
node_type: technique
trade: woodworking
competency_name: "Cross-cut to a line with a panel saw"
progression_band: apprentice

prerequisites:
  - ws-001  # Shop safety: hand tools and the workbench (safety, helper)
  - wc-010  # Measure and mark to 1/16 inch (technique, helper)
  - wc-012  # Mark a square line across a board with knife and square (technique, helper)
  - wc-015  # Secure stock to the bench with a holdfast or vise (technique, helper)

safety_basis:
  hazards:
    - "Sharp teeth: the saw's teeth are sharper than they look, especially a recently filed crosscut blade"
    - "Slip-into-the-finger: the saw can skip out of the kerf at the start of the cut"
    - "Workpiece movement: a board not held still moves under the saw and walks the cut"
    - "Eye injury from kerf dust on a dry, dusty board"
  ppe_required:
    - "Eyes: safety glasses if the board is dry or pitchy, otherwise optional"
    - "No loose sleeves or cuffs near the saw path"
    - "Hair tied back if long enough to fall forward over the work"
    - "No jewelry on the sawing hand"
    - "No gloves: gloves reduce control of the saw and are forbidden for this technique"
  supervision_required: true
  supervision_basis: "Mentor on premises with sight of the cut; mentor's role is to watch the off-hand position and the start of the kerf, the two places where a learner can hurt themselves. Mentor steps back once the learner has demonstrated start-and-finish on three boards."
  fresh_safety_signoff_within_days: 365

tools_required:
  - name: "Panel saw, crosscut filed"
    specification: "20 to 26 inches long, 8 to 11 points per inch, recently sharpened"
    alternatives:
      - "A back saw of 14 inches or larger may substitute for stock under 4 inches wide"
  - name: "Bench with a vise or holdfast"
    specification: "A flat surface that does not move under the cut, at a height where the learner's elbow is roughly level with the cut"
    alternatives:
      - "A saw bench with the learner's knee holding the work"
      - "Two saw horses with a board across, the work clamped to the board"
  - name: "Pencil and a marking knife"
    specification: "Marking knife sharp enough to leave a visible line in the wood; pencil for the waste-side mark"
    alternatives: []

materials_required:
  - name: "Practice stock, softwood"
    quantity: "Three to five boards, each 1x4 nominal, 12 to 24 inches long"
    approximate_cost_usd: 8
  - name: "Practice stock, hardwood (after softwood)"
    quantity: "Two boards, each 1x4 nominal, 12 to 24 inches long"
    approximate_cost_usd: 18

workspace_requirements:
  surface: "Flat workbench or saw bench at the learner's elbow height"
  ventilation: "Open air or a normally ventilated shop; saw dust is minimal at hand-tool rates"
  lighting: "Daylight or strong task lighting positioned to throw a shadow on the marked line, so the line is plainly visible from the sawing side"
  power: "None"
  containment: "None required"

skill_description: |
  The learner secures a board to the bench with the marked line just clear
  of the bench edge, the waste side of the line toward the floor or hanging
  off the bench. The sawing hand grips the saw with the index finger
  pointing down the spine of the handle. The off-hand thumb rests on the
  board, well away from the kerf, as a reference for the saw to start
  against. The first stroke is a backward pull to nick the corner of the
  board, beginning the kerf on the waste side of the marked line. The
  learner then takes long, full-length strokes with the weight of the saw
  doing the work, not downward pressure from the arm. The eye watches the
  line, not the saw. The cut is finished by easing pressure in the last
  inch so the offcut does not tear away from the board.

demonstration_criteria:
  - "The kerf falls on the waste side of the marked line, no further than 1/32 inch from the line, across the full length of the cut"
  - "The cut face is square to the reference face of the board within roughly 1 degree, checked with a try square against the reference face"
  - "The cut face is square to the edge of the board within roughly 1 degree, checked from the edge"
  - "No tear-out at the exit corner: the offcut releases cleanly, not by snapping or splintering"
  - "The learner can complete a crosscut on softwood in under 90 seconds for a 1x4, with relaxed shoulders"
  - "The learner can complete a crosscut on hardwood in under 3 minutes for a 1x4, with the same demonstration criteria as softwood"

common_errors:
  - error: "Kerf wanders off the line"
    cause: "The learner is pushing down on the saw, forcing the teeth, or watching the saw instead of the line"
    remedy: "Let the weight of the saw cut. Take longer strokes. Watch the line, not the saw. If the kerf has already wandered, ease back to the line over the next two strokes rather than yanking the saw back."
  - error: "Cut is not square to the reference face"
    cause: "The saw is being held tilted, usually because the wrist is bent"
    remedy: "Check the wrist is straight, the saw's plate vertical. Some learners benefit from sighting along the saw's spine before each stroke until it becomes habit."
  - error: "The saw skips out of the kerf at the start"
    cause: "The first stroke was a push, not a pull, OR the thumb-rest was not in place"
    remedy: "Always start the cut with a backward pull stroke against the thumb-rest. Once the kerf is established (about 1/8 inch deep), move the thumb away and proceed with full strokes."
  - error: "The offcut tears away from the board at the exit"
    cause: "The learner finished the cut with full pressure"
    remedy: "Ease the pressure in the last inch of the cut. If supporting the offcut by hand, do so without lifting it; let it fall straight down or to the side, depending on grain."
  - error: "The board moves during the cut"
    cause: "The board was not adequately secured, or the vise or holdfast was not tight"
    remedy: "Re-secure before continuing. Check that the bench itself does not rack under the cut."

artifact_expected:
  type: "photo"
  what_to_capture: "Three completed crosscuts on three different boards, laid out flat with their mating offcuts beside them. Include a try square against one cut face and one cut edge for each board."
  what_the_evidence_shows: "The kerf placement relative to the marked line (still visible in pencil on the offcut side), the squareness checked by the try square, and the absence of exit tear-out."

mentor_signoff_required: true

pedagogy:
  i_do: |
    The mentor crosscuts a 1x4 in softwood, narrating each step: how the
    board is secured, where the off-hand thumb sits, the starting pull
    stroke, the long working strokes, the watching of the line, the easing
    at the exit. The mentor finishes by showing the cut against the try
    square and pointing to the side of the line the kerf fell on.
  we_do: |
    The mentor marks the line on a fresh board, secures it, and begins the
    cut with the starting pull stroke and the first three working strokes,
    then hands the saw to the learner without pausing the cut. The learner
    finishes. The mentor watches the off-hand thumb and the kerf line. The
    transition point is partway through the cut, not at the start: the
    learner is taking over an in-progress cut so they feel what the saw is
    already doing rather than starting cold.
  you_do_supervised: |
    The learner marks, secures, starts, and finishes a crosscut on softwood
    while the mentor watches from a position with sight of the kerf and the
    off-hand. The mentor intervenes only if the off-hand drifts into the
    saw path, if the saw is being forced, or if the board is moving. After
    the cut, the learner shows the result against the try square and names,
    out loud, which side of the line the kerf fell on. Repeat for three
    cuts on softwood and two cuts on hardwood across at least two separate
    sessions.
  you_do_unsupervised: |
    The learner is signed off for unsupervised crosscutting on softwood
    stock under 1 inch thick once the supervised demonstrations are
    complete, the artifact is in the portfolio, and the safety signoff
    (ws-001) is current within the last twelve months. Hardwood
    crosscutting and stock over 1 inch thick remain supervised until the
    journeyman band.

estimated_practice_sessions_to_signoff: 6
session_length_minutes: 30

related_projects:
  - wp-001  # Saw bench (the first project, built entirely with crosscuts and a few rip cuts)
  - wp-003  # Tool tote
  - wp-005  # Shooting board
```

### What this example illustrates

- Every field is populated with real, true content.
- The hazards are real and named at the right scale (sharp teeth, slip, workpiece motion, kerf dust). The PPE recommendation honestly says glasses are optional on green wood and forbidden gloves.
- The demonstration criteria are measurable on the work itself: line position to 1/32 inch, squareness within 1 degree by try square, exit tear-out absent.
- The common errors are the actual errors a learner makes with a panel saw, not invented ones.
- The pedagogy block is the apprenticeship pattern, not the five-philosophy variant dict.
- The artifact is a photo of work the learner can take with the parent's phone.
- The mentor signoff is required and the safety prerequisite (`ws-001`) carries a freshness check (365 days).
- The competency feeds three named projects in the project graph.

## 10. Coexistence with the academic curriculum

### 10.1 At enrollment
A child can be enrolled in academic learning maps and trade learning maps
simultaneously, via the existing `ChildMapEnrollment`. No change.

### 10.2 At the planner
The planner reads `is_vocational` per subject and branches to the vocational
prompt. The plan items for trades are activities with
`ActivityType.project`. The plan can mix academic lessons and trade
sessions across the week. A homestead-heavy household may set daily minutes
toward trades; an academic-heavy household may set a single weekly trade
block. The existing daily minutes machinery handles this.

### 10.3 At the activity surface
When the child's current activity is on a trade node, the lesson view
should render a trade panel instead of the practice-items widget. The panel
includes: the safety briefing, the tool and material list, the
demonstration criteria, the artifact-capture prompt, and the mentor-signoff
form. The `AssessmentType` switch already exists; the UI must read the node
type and select the right panel.

### 10.4 At evaluation
An `Attempt` for a trade node carries the photo or video as an
`Artifact`, the demonstration-criteria checklist in `Attempt.feedback`
(JSONB), the mentor's pass/no-pass in `Attempt.score`, and the duration in
`Attempt.duration_minutes`. The mastery state advances when the mentor
signs off the required number of independent demonstrations (see section
5.1). The existing state-event log captures the transitions.

### 10.5 At time accounting
`backend/app/services/compliance_engine.py` already cross-credits
vocational activities against academic subjects where the work genuinely
exercises the academic skill (board-foot calculation crediting applied
math; moisture-content reading on firewood crediting applied science). This
already works; trades content makes the cross-credit honest.

### 10.6 In the portfolio
Each completed project becomes a portfolio entry: the photos of the staged
milestones, the final piece, the mentor signoff, and the date. Over years
the portfolio is a serious record of skilled work the child carries
forward.

## 11. What the design proposal is NOT proposing

- No new tables.
- No new model classes.
- No new node types, edge relations, mastery levels, or assessment types.
  Everything needed is already in the enums.
- No change to the academic content model. Academic and trade content
  coexist as parallel content shapes inside `LearningNode.content`.
- No removal of the five-philosophy frame for academic content. The frame
  is honest for literature, where each philosophy has a native claim; it is
  not honest for cutting a tenon, so trades do not carry it.

## 12. What this proposal IS asking for, on sign-off

1. **Approval of the content model** in sections 4 and 5.
2. **Approval of safety as gating** with the freshness-check mechanism in
   section 6, encoded in `LearningNode.content` rather than a new schema
   column.
3. **Approval of the woodworking pilot** in section 8.1, with the
   gold-standard competency in section 9 serving as the authoring bar.
4. **Approval of one small planner change** (section 6.3 and 7.2): the
   planner, before scheduling a trade competency, must read its
   `safety_basis.fresh_safety_signoff_within_days` and the most recent
   `safety_check` attempt on the named safety prerequisite, and refuse to
   schedule if the safety is stale. This is the only code change the design
   asks for, and it is bounded.

After sign-off, the first authoring batch should be: the trade-root node
for woodworking, the entry safety competency (`ws-001`), the helper-band
measuring and marking competencies (the prereqs of the gold-standard
example), and the gold-standard competency itself (`wc-021`). The first
project node (`wp-001`, the saw bench) follows once the competencies it
exercises are authored. The literature precedent of authoring the gold
standard first, then the chain that supports it, transfers.

## 13. Honest open questions, flagged for review

1. **The mentor model when no skilled mentor is available.** The design
   above assumes a parent or other mentor who can demonstrate the work. For
   households where no adult is yet competent in a trade, the model needs a
   path: paired video demonstrations, a community-mentor model, deferring
   the trade until a mentor is available. This is a real product question,
   not a design defect, and the design accommodates each path without
   change. But it should be answered before woodworking is broadly rolled
   out.
2. **The freshness-check mechanism.** Section 6.3 proposes encoding
   freshness in `LearningNode.content` rather than in a new edge column.
   This works but is slightly less clean than a real schema attribute. If
   freshness becomes a recurring concept across the product (for
   re-certifications, annual reviews, etc.), promoting it to a real
   `LearningEdge` attribute is the right move. The design recommends
   starting with the content-encoded form and promoting later if the
   pattern recurs.
3. **The qualified-band "teach a helper" requirement.** Section 5.1
   proposes that to reach qualified, the learner must have signed off a
   helper-band attempt for another learner. This requires a second
   learner. For only-children or for one-learner-per-trade households, the
   equivalent is to substitute "completed an unprompted journeyman-band
   project" for the teaching requirement. Both paths to qualified should
   be in the authored content.
4. **Trades that lead to a real external credential.** The
   `NodeType.certification_prep` slot is for trades like electrical (toward
   journeyman license), welding (toward an AWS qualification), first aid
   (toward Red Cross / AHA), and the food preservation trade where master
   food preserver certifications exist in some states. These should be
   left open in the content model for those trades and authored against
   the specific credential when the trade itself is authored.
