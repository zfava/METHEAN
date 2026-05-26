# METHEAN human-review backlog (consolidated, by reviewer profile)

Generated from the live content in `backend/app/content/` and the existing per-trade safety review checklists in `docs/ops/`. Updated whenever a node's `safety_review.reviewed` flips, or when new nodes are authored.

This document is the single hand-off surface for human review: each section below names the **exact node ids** for the **exact reviewer profile** that should clear them, what each node claims, and what the reviewer must confirm or correct. The detailed confirm-or-correct checkboxes per node live in the per-trade checklists already in `docs/ops/`; this doc points to them and adds the cross-cutting routing.

## The gate (cross-reference)

Per `app/services/learning_context.py` (the wiring committed in `fix(safety): enforce human-safety-review gate in learning_context surfacing path`), **every node where `requires_human_safety_review` returns True AND `safety_review.reviewed` is not exactly the boolean `True` is INERT and cannot be surfaced to a learner.** The check is fail-closed: missing, malformed, or non-bool-truthy `safety_review.reviewed` all block.

The clearance action that takes a node from inert to surfaceable is the same in every case:

1. The qualified reviewer works through the node's per-trade checklist row by row, marking confirm or correct on every checkbox.
2. Any required corrections are made in the content file by editing the node directly (not through this backlog).
3. In the node's content, set:
   - `safety_review.reviewed` = `True` (the boolean, not the string `"true"`)
   - `safety_review.reviewer` = the reviewer's name and credentials, e.g. `"Jane Smith, Licensed Master Electrician (NY 12345), current NFPA 70E"`
   - `safety_review.reviewed_on` = the ISO 8601 date, e.g. `"2026-06-01"`
4. The per-trade checklist is regenerated if any corrections were made; the review is repeated on the corrected node.

For `elc-021` and `hc-021` specifically, **the content-review gate is necessary but NOT sufficient**: those nodes name a qualified human physically present at a live moment, and the runtime governance layer must additionally confirm a session-time qualified-human-present record before the activity is surfaced. The runtime-presence seam is identified in `app/services/node_content.py::requires_qualified_human_present_at_runtime`; the governance layer is the owner of wiring the session-time check.

---

## Summary

| Domain | Total authored nodes | Currently cleared | Currently awaiting human review |
|---|---|---|---|
| Woodworking trade | 5 | 0 | 5 |
| Gardening trade | 5 | 0 | 5 |
| HVAC trade | 9 | 0 | 9 |
| Electrical trade | 15 | 0 | 15 |
| **Trades subtotal** | **34** | **0** | **34** |
| Literature (advanced + mastery nodes only) | 29 of 83 total | 0 | 29 (recommended; no safety gate) |
| **Grand total in scope of this backlog** | **63** | **0** | **63** |

Notes on the literature row: literature nodes carry no `safety_review` gate (literature is not life-safety content). The 29 nodes in scope here are the **advanced** craft nodes (6) and the **advanced + mastery** work nodes (23) where a literature practitioner's confirmation of interpretation, content suitability, and seminar framing is recommended before they reach learners. The remaining 54 literature nodes (emerging / developing / proficient band) are not in this backlog by default; a practitioner could review them on request but the highest-stakes review value is concentrated in the advanced and mastery readings.

---

## Reviewer profile 1: Experienced woodworker

**Scope: 5 nodes** (entire woodworking trade).

**Recommended reviewer**: a working woodworker with 5+ years of hand-tool practice, OR a community-college fine-woodworking instructor, OR a Society of American Period Furniture Makers member at the journeyman level or above. Familiarity with the hand-tool tradition is more important than power-tool fluency for this batch (power tools are out of scope at the foundation).

**Detailed per-node confirm-or-correct list**: `docs/ops/woodworking_safety_review_checklist.md`.

**Nodes to send**:

| id | type | what it claims | what the reviewer confirms |
|---|---|---|---|
| `woodworking-root` | root | Trade root with `default_supervision_policy` (hand-tool supervised through helper; power-tool through journeyman) and `safety_node = ws-001`. | The supervision policy honestly reflects how a working shop operates with a learner; the band structure (helper / apprentice / journeyman / qualified) is appropriate for a hand-tool-first curriculum. |
| `ws-001` | safety | Shop walkthrough naming 7 hazards (sharp edges, workpiece motion, shavings on floor, oily rags, eye injury, allergic / toxic woods, wrist-line cuts) and 5 PPE items (closed-toe shoes, glasses, hair tied back, no loose sleeves / jewelry, NO gloves on saws / chisels / planes / knives). Defers fire-extinguisher rating to local fire-safety authority (A:B:C conservative default); defers first-aid kit to ANSI/ISEA Z308.1 or current Red Cross. | Every hazard is named at the right scale; the no-gloves rule is honestly stated for the named hand tools; the deferral framings on fire extinguisher and first aid are appropriate; the oily-rag remedy is accurate. |
| `wc-001` | technique (helper) | Measuring to a marked dimension with a tape measure and a pencil. Supervision not required. | The tape-measure hook-play description is accurate; the 1/32-inch demonstration tolerance is reasonable at the helper band. |
| `wc-002` | technique (helper) | Marking a square line with a try square and a marking knife. Supervision required (first edged tool). | The knife-bevel-toward-waste rule, the keep-side / waste-side convention, the off-hand-clear rule, and the 1-degree squareness tolerance are accurate at the helper-to-apprentice band. |
| `wc-021` | technique (apprentice; gold standard) | Cross-cut to a line with a panel saw. Supervision required. Demonstration criteria include 1/32-inch line tolerance, 1-degree squareness, and the cut-time tolerances (under 90 seconds softwood, under 3 minutes hardwood, both for 1x4). | The cut-time tolerances are reasonable as teaching-band targets (not published standards); the start-with-pull-stroke-against-thumb-rest rule, the long-strokes / weight-of-the-saw rule, and the watch-the-line-not-the-saw rule are accurate to traditional hand-tool practice. |

**Eight author-flagged uncertainties (the U-list from the woodworking checklist)** — all need confirmation:

- **U1.** Fire-extinguisher rating (A:B:C conservative default; defer to local fire marshal).
- **U2.** First-aid kit standard (ANSI/ISEA Z308.1 or current Red Cross).
- **U3.** Tropical-hardwood sensitization list (cocobolo, padauk, rosewoods, yew; illustrative not exhaustive; the stop-and-ask rule is load-bearing).
- **U4.** Oily-rag remedy (lay flat outdoors OR sealed metal can; local waste-service disposal).
- **U5.** Saw cut-time tolerances (under 90s softwood, under 3min hardwood as teaching targets, not published standards).
- **U6.** Squareness 1-degree tolerance (teaching-band tolerance, not furniture-maker arc-minutes).
- **U7.** Workbench-height rule (roughly level with relaxed wrist when standing; one common teaching rule).
- **U8.** Sharp-tool-is-safer-than-dull claim (universally repeated shop wisdom but not a measured study).

---

## Reviewer profile 2: Experienced grower / horticulturist

**Scope: 5 nodes** (entire gardening trade).

**Recommended reviewer**: a master gardener (state cooperative extension certified), OR a working market gardener with 5+ years of season-long practice, OR a cooperative-extension agent, OR a horticulturist with formal credentialing. Regional familiarity matters because several uncertainties defer to state extension service for the household's region.

**Detailed per-node confirm-or-correct list**: `docs/ops/gardening_safety_review_checklist.md`.

**Nodes to send**:

| id | type | what it claims | what the reviewer confirms |
|---|---|---|---|
| `gardening-root` | root | Trade root with `default_supervision_policy` across four categories (hand-tool, power-tool, ladder, chemical), `safety_node = gs-001`, food-garden first. | The supervision policy is honest for a household-scale food garden; chemical and power-tool / ladder work are correctly gated out of the foundation. |
| `gs-001` | safety | Garden safety walkthrough naming 9 hazards (sun and heat, soil-borne wounds and tetanus, sharp hand tools, allergens / toxic plants, stinging insects, ticks region-dependent, lifting strain, water-borne, slips). PPE recommended INCLUDES gloves (opposite of woodworking's no-gloves rule, because puncture and allergen risks dominate in the garden). Defers tetanus interval to healthcare provider; sunscreen SPF to CDC / Skin Cancer Foundation; toxic-plant list to state cooperative extension; tick prevention to CDC; first-aid kit to ANSI/ISEA Z308.1 or Red Cross. | Every hazard is named at the right scale for a residential food garden; the gloves-allowed-and-recommended rule is correct for the named tools; the deferrals to CDC, state extension, and healthcare provider are appropriate. |
| `gc-001` | technique (helper) | Read a seed packet. Supervision not required. | The fields named (depth, spacing, sun, water, days-to-maturity, direct-sow vs transplant) are the operative fields on commercial packets; the days-to-maturity counting convention (from sowing for direct-sown, from transplant for transplanted) is accurate. |
| `gc-002` | technique (helper) | Use a trowel or hori-hori knife to dig a planting hole. Supervision required (first sharp tool). | The off-hand-in-path rule, the kneeling form, the rule about stopping on buried hazards, and the rule that the cover stays on at this band on any utility lines underground are all accurate. |
| `gc-021` | technique (apprentice; gold standard) | Transplant a tray of started seedlings to a prepared bed. Supervision required. Demonstration criteria include 1-inch spacing tolerance, crop-family planting-depth rules (tomato-family deeper, brassicas at soil-line, alliums shallow), root-ball handling, gentle watering-in. | The hardening-off duration (7-10 days as teaching tolerance), the planting-depth rules per crop family, the watering-in "visible pool and drain" criterion, and the next-session check (24-72h post-transplant) are accurate at the apprentice band. |

**Ten author-flagged uncertainties (U-list)** — all need confirmation:

- **U1.** Tetanus booster interval (deferred to healthcare provider; node names no interval).
- **U2.** Sunscreen SPF and reapplication interval (deferred to CDC / dermatology; no SPF number).
- **U3.** Hardening-off duration (7-10 days as teaching tolerance; mentor confirms readiness).
- **U4.** Planting-depth rules per crop family (tomato-family deeper, brassicas at soil-line, alliums shallow).
- **U5.** Watering-in volume rule ("visible pool and drain" criterion, not fluid-ounce target).
- **U6.** Spacing distances (deferred entirely to seed packet via gc-001 planting card).
- **U7.** Days-to-maturity counting convention (from-sowing vs from-transplant per crop).
- **U8.** Garden sharp-tool-is-safer-than-dull rule (universally repeated horticulture wisdom).
- **U9.** Tick-active region designation (deferred to current CDC regional information).
- **U10.** Regional toxic-plant list (deferred to state cooperative extension; node names only urushiol-bearing universal toxics).

---

## Reviewer profile 3: Licensed HVAC technician (+ EPA-608 holder / counsel for the legal claims)

**Scope: 9 nodes** (entire HVAC trade).

**Recommended reviewer**:

- For technical content and the live-work node: a licensed HVAC technician (state license per the AHJ; journeyman or master credential), with current field experience in residential service.
- **For `hc-021` specifically (live-dead-live verification, ELECTRICAL HAZARD)**: BOTH the licensed HVAC technician AND a licensed electrician (or an HVAC tech with explicit electrical scope per the AHJ). NFPA 70E currency required.
- **For the certification_prep nodes**: HVAC technician for the technical claims; an EPA-608 Universal certificate holder for the EPA-608 framing; counsel for the legal claims (cross-referenced in Profile 5 below).

**Detailed per-node confirm-or-correct list**: `docs/ops/hvac_safety_review_checklist.md`.

**Detailed certification spine and mastery ladder**: `docs/curriculum/HVAC_certification_and_mastery_map.md`.

**Nodes to send**:

| id | type | what it claims | what the reviewer confirms |
|---|---|---|---|
| `hvac-root` | root | Mastery-path trade root with four-tier supervision policy (knowledge AI-mentored, low-hazard hands-on adult-on-premises, higher-hazard licensed-human-present, regulated milestones deferred). Mastery ladder with 4 rungs and `credentials_NOT_substitutable_for` locks. | The four-tier policy is honest for HVAC; the credentials-NOT-substitutable-for clauses correctly state that EPA 608, state license, NATE, and OSHA 10/30 do not lower any supervision rule. |
| `hs-001` | safety | Walkthrough naming 18 hazards (electrocution, capacitor stored energy, arc flash, low-voltage shock, refrigerant exposure A1/A2L/A3 classes, frostbite, thermal burns, CO, NG/LP leaks, falls, lifting, sheet-metal cuts, eye injury, confined-space, asbestos pre-1980, IAQ contaminants, pinch points, fire from hot work) and 9 PPE items including CAT III 600V minimum DMM. Defers to OSHA, NFPA 70E, NFPA 70, NFPA 54, NFPA 720, EPA 608, ASHRAE 34/62.1/62.2, AHRI, UL 2034/2075, CDC, ANSI/ISEA Z308.1, ACIP / CDC tetanus. | Every hazard is named correctly; the refrigerant safety-class transition (R-410A A1 to R-454B / R-32 A2L under the AIM Act) is accurate; PPE list is complete; the deferrals to NFPA, OSHA, EPA, ASHRAE, and the AHJ are appropriate. |
| `hc-001` | technique (helper, AI-mentor-OK) | Read an HVAC equipment nameplate (voltage, MCA, MOP, refrigerant type, capacity, SEER2/HSPF2/EER2/AFUE, listing). | Field set is complete; the SEER/SEER2 (etc.) transition is accurately characterized; the AIC concept is correctly framed (downstream input for later install, not in scope at this band). |
| `hc-002` | technique (helper, AI-mentor-OK) | Identify residential split-system components by sight, covers closed. | Component list is accurate (cabinet, condenser coil, condenser fan, contactor named as internal-not-visible, capacitor named internal-not-visible, line set with insulation distinction, service ports NOT touched, disconnect, electrical whip, indoor cabinet with supply / return, access panels named-not-opened, evaporator coil and blower internal-not-visible, condensate drain, secondary drain pan and float switch for above-living-space, filter slot, thermostat). |
| `hc-021` | technique (apprentice; gold standard; ELECTRICAL HAZARD) | DMM + LOTO live-dead-live verification at residential AC condenser disconnect. `supervision_required: True`, `mentor_signoff_required: True`, qualified-human-physically-present at the live moment, AI does NOT stand in. Failure modes named: wrong CAT rating, meter failure, wrong disconnect, capacitor charge, backfeed. | **HIGHEST-STAKES NODE IN THE TRADE.** The licensed-electrician-physically-present rule is non-negotiable; the live-dead-live sequence (test on known live, test dead at work point, re-test on known live) matches NFPA 70E exactly; the CAT III 600V minimum is correct; the LOTO procedure matches OSHA 29 CFR 1910.147; the failure modes are completely named. |
| `hcert-epa608` | certification_prep | EPA Section 608 Technician Certification (Types I, II, III, Universal); federal legal requirement under Clean Air Act and 40 CFR Part 82 Subpart F; exam through EPA-approved certifying body; METHEAN does NOT administer. | Type definitions are accurate; legal-requirement language is accurate; deferral to EPA program page and named certifying bodies (ESCO Institute, RSES, Mainstream Engineering) reflects current EPA approvals; no exam content reproduced. **Counsel co-review recommended.** |
| `hcert-licensing` | certification_prep | State HVAC licensing path (apprenticeship / journeyman / master); jurisdiction-specific; AHJ-deferred; supervised hours through state-approved program NOT through METHEAN. | Apprenticeship-hours framing is honest (varies by AHJ); the jurisdiction-specific framing is correct; the explicit non-substitution for state-approved hours is correct. **Counsel co-review recommended.** |
| `hcert-nate` | certification_prep | NATE certifications (Ready to Work, HVAC Support Tech, Core / specialty, senior); optional; not a substitute for state licensing or EPA 608. | NATE specialty framing is current per natex.org; the not-a-substitute-for clauses are accurate. |
| `hcert-osha` | certification_prep | OSHA 10-Hour and 30-Hour Outreach Training; optional; not licenses in legal sense; not a substitute for site / task-specific OSHA-required training. | The not-a-substitute clauses are accurate; the OSHA-authorized trainer requirement is correctly stated. |

**HVAC-specific author-flagged uncertainties (U1-U14 from the HVAC checklist)** — confirmation needed on all 14. The list lives in `docs/ops/hvac_safety_review_checklist.md` and includes the refrigerant safety-class transition (U1), LOTO written procedure (U2), specific voltages (U3), SEER/SEER2 transition (U4), pre-1980 asbestos cutoff (U5), CO action levels (U6), multimeter CAT rating (U7), arc-flash boundaries (U8), refrigerant burn risk (U9), sheet-metal cut frequency (U10), CO alarm service life (U11), cut-resistant glove level (U12), insulating glove class (U13), and EPA 608 certification types (U14).

---

## Reviewer profile 4: Licensed electrician (+ safety professional for `elc-021`)

**Scope: 15 nodes** (entire electrical trade).

**HIGHEST-HAZARD TRADE IN THE CODEBASE.** Electrical is line-voltage lethal. This is the most rigorous review in scope.

**Recommended reviewer**:

- **For technical content (`el-root`, `els-001`, `elc-001` through `elc-009`, the cert spine)**: a licensed electrician with current field experience (state license per the AHJ; journeyman or master), current NFPA 70E familiarity.
- **For `elc-021` specifically**: BOTH the licensed electrician AND a safety professional familiar with OSHA 29 CFR 1910.147 (LOTO) and current NFPA 70E. The author of the node deliberately did not attempt to verify the procedure against the safety professional's checklist; that verification is the reviewer's job.
- **For `elcert-nec` and `elcert-safety`**: the licensed electrician plus, if available, an NFPA-approved code instructor for the NEC navigation framing.
- **For `elcert-licensing`**: licensed electrician for the technical scope claims; counsel for the legal claims (cross-referenced in Profile 5).

**Detailed per-node confirm-or-correct list**: `docs/ops/electrical_safety_review_checklist.md`.

**Detailed certification spine and mastery ladder**: `docs/curriculum/electrical_certification_and_mastery_map.md`.

**Nodes to send**:

| id | type | what it claims | what the reviewer confirms |
|---|---|---|---|
| `el-root` | root | Residential and low-voltage electrical mastery-path root. Four-tier supervision policy. Mastery ladder. `credentials_NOT_substitutable_for` lock: NEC / NFPA 70E knowledge, state license, OSHA 10/30, NFPA 70E training all NEVER lower a supervision rule. | The four-tier policy is honest for an electrical apprenticeship; the credentials-NOT-substitutable-for clauses correctly state that no credential lowers any supervision rule (the safety habit is non-negotiable); the foundation scope correctly STOPS at the load side of the main disconnect. |
| `els-001` | safety | Walkthrough naming 20 hazards including electrocution at residential 120V/240V, capacitor stored energy, arc flash, low-voltage shock, generator backfeed, solar PV backfeed, MWBC shared-neutral, neutral-to-ground bond fault, thermal burns, fire from arcing faults, sheet-metal / conductor-end cuts, falls, confined-space, wrong-circuit / wrong-disconnect, wrong CAT rating multimeter (a documented cause of injury), working-space and clearance, wet conditions, scope boundary, and CO from electrical-source-secondary failures. PPE list includes CAT III 600V minimum DMM, Class 00 insulating gloves with leather protectors, arc-rated clothing per NFPA 70E, IEC 60900 / ASTM F1505 insulated tools rated 1000V. | Every hazard is named at the right scale; the wrong-CAT-rating documented-cause framing is honest; the working-space-per-NEC rule is correct; the AHJ-adopted-edition-governs caveat is consistently present. |
| `elc-001` | technique (helper, AI-mentor-OK) | Read electrical nameplate / rating label (voltage, current, MCA, MOP, AIC, listing). | Field set is complete; the AIC concept is correctly framed (downstream input for later install); the listing-mark requirement (UL, ETL, CSA per NRTL) is accurate. |
| `elc-002` | technique (helper, AI-mentor-OK) | Identify residential components from diagrams and with covers closed. | Component list is accurate; the service-equipment vs subpanel neutral-to-ground bond rule is correctly framed; the symbol-set match between diagrams and physical components is accurate. |
| `elc-003` | knowledge (helper, AI-mentor-OK) | Ohm's law and basic DC and AC-resistive circuit theory; current (not voltage) named as cause of injury; introductory power-factor distinction. | The Ohm's law treatment is correct; the current-not-voltage-causes-injury rule is correctly stated; the apparent / real / power-factor distinction is introduced at the right level. |
| `elc-004` | knowledge (helper, AI-mentor-OK) | Series and parallel circuits; basic residential load calculation; the 80% continuous-load rule named as introductory. | The series / parallel formulae are correct; the residential branches wire in parallel is accurate; the 80%-rule introduction is honest as a starting point with deference to NEC. |
| `elc-005` | knowledge (helper, AI-mentor-OK) | Read residential wiring diagrams and schematics: one-line, wiring, schematic; standard symbol set; six common circuits (single switched, three-way, GFCI LINE/LOAD, AFCI, MWBC, smoke/CO interconnect). | The diagram-type distinctions are accurate; the GFCI LINE / LOAD framing is correct; the MWBC shared-neutral diagram-level introduction is accurate; the color-coding convention and re-identification exception are correctly stated. |
| `elc-006` | knowledge (helper, AI-mentor-OK) | Anatomy of a residential electrical service from utility supply through branch circuits; scope boundary at load side of main disconnect. | The component list is complete; the LINE / LOAD scope-boundary rule at the main disconnect is correctly stated as the foundation's hard stop; the neutral-to-ground bond-at-main-only rule is correct; the 120/240V split-phase residential convention is accurate. |
| `elc-007` | knowledge (helper, AI-mentor-OK) | Conductor sizing and ampacity basics; defers all article numbers and table values to AHJ-adopted NEC. | The ampacity-table structure description is accurate; the termination-temperature rule (60/75/90) is correctly framed; the ambient and conductor-count correction factors are correctly framed; the copper-vs-aluminum table separation is accurate; no specific table values are reproduced. |
| `elc-008` | knowledge (helper, AI-mentor-OK; **most safety-critical conceptual area**) | Grounding and bonding theory; explicitly NOT a license to perform energized grounding work; explicit grounding-vs-bonding distinction; fault-clearing path named explicitly; once-only bonding rule. | **The conceptual treatment is the load-bearing one in the foundation.** The grounding (to earth) vs bonding (between metal parts) distinction is the most-misunderstood residential area and must be correct; the fault-clearing path explanation (hot to metal → EGC → main bonding jumper → neutral → transformer) is correct; the ground-rod-is-not-a-fault-path framing is correct; the once-only bond at main rule is correct. |
| `elc-009` | technique (helper, AI-mentor-OK; **no live measurement at this band**) | Meter and tool literacy including the meaning of CAT ratings; insulated tool inspection; insulating glove inspection; no live measurement at this band. | The CAT II / III / IV definitions and the residential-240V-needs-CAT-III-at-600V-minimum rule (per NFPA 70E) are correct; the finger-guard probe (IEC 61010-031) requirement is accurate; the IEC 60900 / ASTM F1505 insulated tool requirement is accurate; the Class 00 insulating glove with leather protectors rule is correct; the no-live-measurement-at-this-band rule is honest. |
| `elc-021` | technique (apprentice; gold standard; **ELECTRICAL HAZARD; HIGHEST-STAKES NODE IN THE CODEBASE**) | De-energize / LOTO / live-dead-live verification on a residential branch circuit. `supervision_required: True`, `mentor_signoff_required: True`, **LICENSED ELECTRICIAN PHYSICALLY PRESENT** at the live moment, AI tutor does NOT stand in. 10 failure modes named: electrocution, arc flash, wrong-circuit / wrong-disconnect, meter failure, backfeed from generator, backfeed from solar PV, MWBC shared-neutral hazard, neutral-to-ground bond fault, stored capacitor energy, wet conditions, sharp sheet-metal edges. Verbatim supervision_basis locked by a guard test. | **HIGHEST-STAKES REVIEW.** Confirm: the live-dead-live sequence matches NFPA 70E exactly; every-pair-of-conductors dead test for 120V (H-N, H-G, N-G) and for 240V (L1-G, L2-G, L1-L2, L1-N, L2-N) is complete; MWBC-specific neutral check is correct; LOTO procedure matches OSHA 29 CFR 1910.147; CAT III at 600V minimum requirement is correct; Class 00 insulating gloves with leather protectors is correct; the licensed-electrician-physically-present rule is non-negotiable and the AI-does-not-stand-in clause is explicit. |
| `elcert-nec` | certification_prep | Working familiarity with NEC (NFPA 70) and NFPA 70E; codes obtained through NFPA; AHJ-adopted edition governs; METHEAN does NOT administer. | The NEC and NFPA 70E structural descriptions are accurate; the residential-focus article list (210, 220, 230, 240, 250, 310, 314, 330/334, 404, 406, 408, 410, 422, 430, 440, 460, 690, 702) is appropriate at this band; no code text reproduced. |
| `elcert-licensing` | certification_prep | State electrician licensing path (apprentice / journeyman / master / low-voltage); jurisdiction-specific; AHJ-deferred; supervised hours through state-approved apprenticeship (electrical training ALLIANCE for IBEW / NECA, state non-union sponsors, employer-based recognized by AHJ); METHEAN's portfolio NOT a substitute for hours. | The apprenticeship-hours framing is honest (~8,000 hours / 4 years "in many states"); the low-voltage / limited-energy as a distinct license in many states is accurate; the explicit METHEAN-not-a-substitute-for-hours is correct. **Counsel co-review recommended.** |
| `elcert-safety` | certification_prep | OSHA 10 / 30 Outreach + NFPA 70E training as adjacent credentials; not licenses in legal sense; not a substitute for site-specific or task-specific OSHA training. | The OSHA Outreach framing is accurate; the NFPA 70E training provider framing (employer programs, electrical training ALLIANCE, recognized independent providers) is current; the not-a-substitute clauses are accurate. |

**Electrical-specific author-flagged uncertainties (U1-U14 from the electrical checklist)** — confirmation needed on all 14. The list lives in `docs/ops/electrical_safety_review_checklist.md` and includes NEC edition variance (U1), apprenticeship hours variance (U2), low-voltage license variance (U3), multimeter CAT rating (U4), arc-flash boundaries (U5), bonding-vs-grounding terminology (U6), generator and solar backfeed (U7), MWBC shared-neutral (U8), insulating glove class (U9), LOTO written procedure (U10), service-entrance scope (U11), knob-and-tube / old aluminum (U12), AFCI / GFCI required locations (U13), permits and inspections (U14).

---

## Reviewer profile 5: Counsel familiar with regulated-trade licensing and EPA Section 608

**Scope: 7 nodes** (the cross-trade certification_prep nodes). These are deliberately routed to counsel because they make claims about federal regulations (EPA Section 608 / Clean Air Act / AIM Act), about state licensing rules, and about the limits of what METHEAN does and does not administer. Misstatement here has legal consequences.

**Recommended reviewer**:

- Counsel with experience in regulated-trade licensing (electrical, HVAC, plumbing). Familiarity with the state(s) the household is in is most valuable; a national review can confirm the deferral framing but cannot confirm jurisdiction-specific rules.
- For EPA-608 content specifically: counsel familiar with the Clean Air Act and the AIM Act, OR an EPA-608 Universal certificate holder who has worked through the current EPA program guidance.

**Nodes to send (cross-trade)**:

| id | trade | legal status | what counsel confirms |
|---|---|---|---|
| `hcert-epa608` | HVAC | **legally_required** (federal) | The Clean Air Act Section 608 citation, the 40 CFR Part 82 Subpart F citation, the four-type framework (Type I / II / III / Universal), the deferral to EPA-approved certifying bodies, and the explicit "METHEAN does not administer or proctor the exam" language. The AIM Act of 2020 reference for the R-410A to A2L transition. No reproduced exam content. |
| `hcert-licensing` | HVAC | **jurisdiction_specific** | The AHJ-deferral language; the apprenticeship hours framing; the explicit non-substitution of METHEAN's portfolio for AHJ-recognized hours; the testing-partner naming (Prov Inc., PSI, etc.) as illustrative, not authoritative. |
| `hcert-nate` | HVAC | **optional** | The "complementary to state licensing and EPA 608, not a substitute" framing; the not-a-license-in-legal-sense framing. |
| `hcert-osha` | HVAC | **optional** | The "not a license in the legal sense", "not a substitute for site-specific or task-specific OSHA training", and "METHEAN does not deliver or issue the cards" claims. |
| `elcert-nec` | Electrical | **jurisdiction_specific** | The NFPA standards framing; the AHJ-adopted edition governs deferral; the no-reproduced-code-text discipline (the validator enforces this). |
| `elcert-licensing` | Electrical | **jurisdiction_specific** | The state-by-state licensing variance language; the apprenticeship hours and journeyman / master / low-voltage framing; the explicit non-substitution of METHEAN for state-approved apprenticeship hours; the electrical training ALLIANCE (IBEW / NECA) framing as one recognized pathway among others. |
| `elcert-safety` | Electrical | **optional** | The OSHA Outreach trainer deferral and the NFPA 70E training provider framing; the not-a-substitute-for-OSHA-required-training clauses. |

**The four credentials-NOT-substitutable-for locks** (one set on each of `hvac-root.mastery_ladder` and `el-root.mastery_ladder`): counsel additionally reads these clauses with an eye to whether they are sufficient as a written representation that no credential held by the learner lowers a supervision tier in the curriculum. These clauses are the load-bearing legal framing for the supervision policy.

---

## Reviewer profile 6: Literature practitioner

**Scope: 29 nodes** (the 6 advanced craft nodes plus the 21 advanced and 2 mastery work nodes). Literature carries no `safety_review` gate (it is not life-safety content); the review here is for interpretation accuracy, content suitability, seminar framing, and the highest-stakes content warnings on the mastery-gated readings.

**Recommended reviewer**:

- A literature practitioner: a literature professor with classroom experience, an experienced literature teacher (high school AP English, IB Literature, or equivalent), or a writer with MFA-level training and reading practice. Strongest reviewer is someone who has TAUGHT the works at issue.
- **For the 2 mastery-gated works (Blood Meridian and The Bloody Chamber)**: a practitioner familiar with content-warning practice and the works' specific content (extreme violence in Blood Meridian; gothic / fairy-tale-with-violence-and-sexuality content in The Bloody Chamber). These are the highest-stakes content-suitability calls in the literature strand.

**Detailed content**: `backend/app/content/literature_mastery_content.py`.

### Advanced craft nodes (6) — interpretation and analytical-moves review

| id | objective (summary) | what to confirm |
|---|---|---|
| `lit-craft-004` | Sustained close reading as an inquiry method across whole difficult works. | The analytical moves and seminar questions are appropriate for the advanced band; the exemplar texts are well-chosen. |
| `lit-craft-014` | Read character as part of a work's argument. | The argumentative-character framing is honest (characters as positions, not just personas); seminar questions invite the right reading. |
| `lit-craft-023` | Argue a work's full thematic system as the way the work means. | The thematic-system framing is rigorous; seminar questions push beyond theme-naming to theme-as-structure. |
| `lit-craft-031` | Unreliable narrator: recognition, textual evidence, the writer's choice. | The textual-evidence framework is accurate; this is the gold-standard exemplar craft node and warrants special care. |
| `lit-craft-043` | Read irony as the writer's gap between figure and literal claim. | The irony-as-refusal framing is rigorous; seminar questions catch the writer's stance, not just the figure. |
| `lit-craft-053` | Argue a play's full dramatic argument. | Treats drama as drama (not novel-in-dialogue); seminar questions invite the right reading of dramatic structure. |

### Advanced work nodes (21) — classics-track and inheritance-track readings

These are the advanced-band readings the practitioner reviews for interpretive accuracy, exemplar-text choice, seminar question framing, and content suitability for the band. Each work below is identified by `lit-work-NNN` or `lit-work-inh-NNN`:

**Classics track (15 advanced)**: `lit-work-008` Oresteia, `lit-work-009` Bacchae, `lit-work-010` Inferno, `lit-work-011` Hamlet, `lit-work-013` King Lear, `lit-work-016` Don Quixote, `lit-work-017` Paradise Lost, `lit-work-022` Wuthering Heights, `lit-work-024` Moby-Dick, `lit-work-025` Crime and Punishment, `lit-work-026` War and Peace, `lit-work-028` Heart of Darkness, `lit-work-030` Mrs Dalloway, `lit-work-037` T. S. Eliot selected poems and essays.

**Inheritance track (6 advanced)**: `lit-work-inh-007` Le Morte d'Arthur selections, `lit-work-inh-012` Poetic Edda selections, `lit-work-inh-013` Prose Edda selections, `lit-work-inh-014` Nibelungenlied, `lit-work-inh-015` Njal's Saga, `lit-work-inh-018` The Border Trilogy, `lit-work-inh-022` Phantastes.

For each: confirm the close-reading passages chosen are the right ones; the structural and thematic analyses are accurate; the seminar questions invite the work's own questions rather than imposed ones; the comparative-threads suggestions land; the content-notes / context warnings are appropriate for an advanced learner.

### Mastery work nodes (2) — **HIGHEST-STAKES content-suitability calls**

| id | title | content stakes |
|---|---|---|
| `lit-work-inh-017` | **Blood Meridian, or the Evening Redness in the West** (Cormac McCarthy) | Extreme and sustained violence; theological darkness; not suitable for younger or unprepared readers regardless of band; the content_notes must be unambiguous; the mastery gating must be enforced. |
| `lit-work-inh-024` | **The Bloody Chamber and Other Stories** (Angela Carter) | Gothic fairy-tale retellings with adult content (violence and sexuality woven into the fairy-tale logic); not suitable for younger learners; content_notes and the mastery gating must be unambiguous. |

For each mastery work: confirm the `content_notes` / context framing is honest about the content; confirm the mastery-band gating is sufficient for the reader-readiness call; confirm the seminar questions hold the work to its own seriousness without softening or moralizing.

### Literature clearance action

Unlike the trades, literature nodes do not carry a `safety_review` block today. The recommended clearance action for literature nodes is: the literature practitioner's review is recorded in `docs/curriculum/` (a per-node review log or a literature_review_log.md) with date, reviewer, and confirm-or-correct notes per node. No content change to the literature nodes is required for the read; if the review identifies corrections, those are made by editing the literature content file directly and re-reviewing.

---

## Totals per reviewer profile

| Reviewer profile | Nodes to send | Highest-stakes within the set |
|---|---|---|
| **1.** Experienced woodworker | **5** | `wc-021` (cross-cut, sharp tool, apprentice band) |
| **2.** Experienced grower / horticulturist | **5** | `gc-021` (transplant, sharp tool, apprentice band) |
| **3.** Licensed HVAC technician (+ safety pro for `hc-021`) | **9** | `hc-021` (DMM + LOTO live-dead-live; electrical hazard; licensed-human-physically-present) |
| **4.** Licensed electrician (+ safety pro for `elc-021`) | **15** | `elc-021` (DMM + LOTO live-dead-live; **HIGHEST-STAKES NODE IN CODEBASE**); plus `elc-008` (grounding and bonding theory, most-misunderstood residential area) |
| **5.** Counsel familiar with regulated-trade licensing and EPA-608 | **7** (cross-trade certification_prep) | `hcert-epa608` (federal legal requirement under Clean Air Act); `elcert-licensing` (state licensing claims) |
| **6.** Literature practitioner | **29** (6 advanced craft + 21 advanced work + 2 mastery work) | `lit-work-inh-017` Blood Meridian (mastery; extreme violence); `lit-work-inh-024` The Bloody Chamber (mastery; adult content); `lit-craft-031` unreliable narrator (gold-standard craft exemplar) |

Sum across reviewer profiles: 5 + 5 + 9 + 15 + 7 + 29 = **70 review slots** across **63 distinct nodes** (the 7 certification_prep nodes are routed to both the trade-practitioner profile and counsel, so they appear in two slots).

---

## Until cleared, every gated node is inert

Cross-reference: `fix(safety): enforce human-safety-review gate in learning_context surfacing path` (already on `main`). The gate in `app/services/learning_context.py` calls `app/services/node_content.py::is_cleared_for_surfacing` at the single surfacing point. Any node where `requires_human_safety_review` returns True AND `safety_review.reviewed` is not exactly the boolean `True` returns an `awaiting_human_safety_review` state with empty `lesson` / `assessment` / `practice` / `reading` content, `tutor_available: False`, and the activity metadata visible so governance sees which activity is blocked.

The aggregate test `test_every_authored_hazardous_node_is_blocked_today` in `tests/test_learning_context_safety_gate.py` asserts this against the live `ELECTRICAL_CONTENT` and is parametrized so that if any node's `reviewed` flag flips to True the test forces a fresh review-evidence check; the parametrize set is also extensible to the other trades when reviews complete.

**Today, all 34 trade nodes return `awaiting_human_safety_review` for a hazardous node (where `requires_human_safety_review` is True) or surface normally (where it is False but the node is still recommended for human review of its technical claims). None of the 34 trade nodes have `safety_review.reviewed = True`.** The literature nodes have no gate today; they surface normally, and the recommended literature-practitioner review is advisory not gating.
