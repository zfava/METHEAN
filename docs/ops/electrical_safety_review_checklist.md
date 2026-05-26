# Electrical safety review checklist

Generated from `backend/app/content/electrical_content.py`. The checklist below renders the actual hazards, PPE, supervision basis, and demonstration criteria for every authored node. Do not edit the node content from this checklist; edit `electrical_content.py` and regenerate this file. No node may be surfaced to a learner until its `safety_review.reviewed` is set to True by a qualified human reviewer, with `reviewer` and `reviewed_on` recorded.

**HIGHEST-HAZARD TRADE AUTHORED TO DATE.** Electrical is line-voltage lethal. This trade requires the most rigorous human review of any trade in this codebase. Recommended reviewer profile:

- **For `el-root`, `els-001`, the helper-band knowledge nodes (`elc-001` through `elc-009`), and the certification spine**: a licensed electrician (state license per the AHJ; current journeyman or master credential) with current NFPA 70E familiarity, AND counsel familiar with state electrical-licensing regulations for the certification claims.
- **For `elc-021` specifically (the apprentice-band gold standard, LOTO live-dead-live)**: a licensed electrician AND a safety professional familiar with OSHA 1910.147 and NFPA 70E. This is the highest-stakes node in the batch.
- The author of this batch did not perform any of the verification work; the reviewer is the load-bearing safety authority.

## Reviewer identification

- Reviewer name: ____________________________________________
- Relevant electrical experience (years, type, credentials; state license number and type; NFPA 70E currency): ____________________________________________
- Date of this review: ____________________________________________

## Completion contract

On completion of this review, for each node confirmed correct:

1. In `backend/app/content/electrical_content.py`, set the node's `safety_review.reviewed` to `True`, `safety_review.reviewer` to the reviewer's name and credentials, and `safety_review.reviewed_on` to the date in ISO 8601 (`YYYY-MM-DD`).
2. If any item below requires correction, the correction is made in `electrical_content.py` and this checklist is regenerated; the review is repeated on the corrected node.
3. No node where `safety_review.reviewed` is `False` may be surfaced to a learner. The integration gate is the responsibility of `learning_context` (see the TODO in `backend/app/services/node_content.py::requires_human_safety_review`).
4. For `elc-021` specifically, the integration gate must additionally confirm that any learner attempting the competency has a licensed electrician physically present at the live-dead-live verification per the node's `supervision_basis`. The AI tutor does NOT stand in.

---

## Per-node review

### el-root: Residential and low-voltage electrical (intro to master electrician, mastery path)

- Node type: `root`
- Supervision policy: four tiers (knowledge_work AI-mentor; low-hazard de-energized adult-on-premises; energized / backfeed-possible licensed-electrician-physically-present; regulated milestones deferred to AHJ and official bodies)
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Supervision policy categories (confirm each is honest and complete)

- [ ] `tier_1_knowledge_work`: AI tutor end-to-end
- [ ] `tier_2_low_hazard_hands_on_de_energized_and_verified_dead_only`: adult on premises
- [ ] `tier_3_energized_or_near_energized_work_or_any_work_where_re_energization_or_backfeed_is_possible`: LICENSED ELECTRICIAN physically present at the work; AI does not stand in
- [ ] `tier_4_regulated_credentialed_milestones`: deferred to NFPA, OSHA, AHJ
- [ ] `households_without_a_resident_licensed_electrician`: paid professional session, vocational program, apprentice arrangement, or defer
- [ ] `all_bands`: no credential held by the learner ever lowers a supervision tier
- [ ] Mastery framing: portfolio + credential + qualified-band signoff; portfolio and credential complementary

#### credentials_NOT_substitutable_for clauses (confirm all four locks)

- [ ] NEC and NFPA 70E knowledge does NOT substitute for any supervision rule
- [ ] State electrician license does NOT substitute for any safety competency (live-dead-live still on every job)
- [ ] OSHA 10 / 30 Outreach does NOT substitute for site-specific or task-specific OSHA training (LOTO, fall, confined-space)
- [ ] NFPA 70E training does NOT substitute for supervision tier or safety competency

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in electrical_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### els-001: Electrical shop and site safety (entry safety competency)

- Node type: `safety`
- Progression band: `helper`
- Supervision required: `True`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Hazards (confirm each is named correctly and at the right scale)

- [ ] Electrocution from line voltage (120V or 240V residential; nameplate and panel labeling are authorities; live-dead-live per elc-021)
- [ ] Shock from low-voltage and control circuits (24VAC typical; lower shock risk but real involuntary-reaction risk)
- [ ] Arc flash from a short during energized work (NFPA 70E; default is de-energize and verify dead)
- [ ] Stored energy in capacitors (lethal for minutes to hours; capacitor contact NOT in scope at this band)
- [ ] Backfeed from a generator (transfer switch or interlock per NEC required; documented line-worker and homeowner deaths)
- [ ] Backfeed from solar PV (rapid-shutdown and interconnection per AHJ-adopted NEC)
- [ ] MWBC shared-neutral hazard (opening neutral on energized MWBC places full line-to-line voltage on loads and on the formerly-neutral wire)
- [ ] Neutral-to-ground bond fault (neutral and ground bonded only at main service equipment per AHJ-adopted NEC)
- [ ] Thermal burns from hot conductors and heated components
- [ ] Fire from arcing faults, overloaded circuits, damaged insulation, improper terminations (AFCI per AHJ-adopted NEC)
- [ ] CO from electrical sources is rare directly but secondary to failure (failed thermostat, generator indoors)
- [ ] Sheet-metal and conductor-end cuts (cut-resistant gloves default for any handling)
- [ ] Eye injury from metal swarf, insulation fragments, arc flash, solvent splash
- [ ] Falls from ladders and elevated work (OSHA 1910.23 and 1926 Subpart M)
- [ ] Confined-space exposure (OSHA 1910.146; not in scope at this band)
- [ ] Wrong-circuit and wrong-disconnect failure (panel labels commonly wrong; verification at work point is the safeguard)
- [ ] Wrong meter Category (CAT) rating (documented cause of injury in working electricians; CAT III at 600V minimum per NFPA 70E)
- [ ] Working space and clearance per AHJ-adopted NEC (escape path)
- [ ] Wet conditions
- [ ] Scope boundary: foundation stops at load side of main disconnect

#### PPE required (confirm each item; what is required, what is permitted)

- [ ] Closed-toe leather work boots with non-slip soles (EH-rated for tier-3 work)
- [ ] Safety glasses (ANSI Z87.1) default; face shield for energized work per NFPA 70E
- [ ] Insulating gloves rated for voltage (Class 00 / 500V minimum for residential 240V per NFPA 70E)
- [ ] Leather protectors over insulating gloves
- [ ] Arc-rated clothing per NFPA 70E for calculated incident energy
- [ ] Cut-resistant gloves (ANSI/ISEA 105 A4 or higher) for conductor and panel handling (after dead)
- [ ] Hearing protection per OSHA / NIOSH
- [ ] No metal jewelry on hands, wrists, neck
- [ ] Long sleeves rolled down near energized; hair tied back
- [ ] Multimeter CAT III at 600V minimum (CAT IV acceptable; CAT II or unrated NOT acceptable)
- [ ] Fall protection per OSHA 1926 Subpart M for elevated work (not in this batch)
- [ ] Insulated tools rated 1000V per IEC 60900 / ASTM F1505

#### Supervision basis (confirm the AI-mentor framing is correct)

- [ ] Walkthrough is human-supervised by an adult on premises (parent counts; no electrical credentials needed for the walkthrough itself)
- [ ] AI tutor guides what to look for and reviews recorded walkthrough video
- [ ] No self-attestation on safety; mentor confirms household plans for CO alarm, fire extinguisher (Class C required for electrical fires), first aid, tetanus, main disconnect location, panel labeling state, backfeed sources, and the licensed-electrician-present requirement for tier-3 work

#### Demonstration criteria (confirm each is measurable and correctly states the bar)

- [ ] Names every PPE item and when each is required / permitted
- [ ] Locates first aid kit per ANSI/ISEA Z308.1 or Red Cross
- [ ] Locates fire extinguisher; rating includes Class C for electrical fires
- [ ] Locates CO alarm(s); UL 2034 / 2075; within service life; placed per NFPA 720 and AHJ
- [ ] Locates main disconnect; working space and headroom per AHJ-adopted NEC
- [ ] Names backfeed sources on the property; transfer arrangement installed by licensed electrician
- [ ] Names household tetanus immunization arrangement
- [ ] Names the live-dead-live rule and points to elc-021
- [ ] Names the capacitor-treated-as-charged rule
- [ ] Names the MWBC shared-neutral rule
- [ ] Names the panel-labels-commonly-wrong rule
- [ ] Names the wrong-CAT-rating failure mode; identifies household meter's CAT rating; CAT III at 600V available for tier-3
- [ ] Names the wet-conditions defer rule
- [ ] Names that hot work, elevated work, confined-space work are each gated separately and not in scope at this band
- [ ] Names the scope boundary: foundation stops at load side of main disconnect; above 600V out of scope; three-phase out of scope
- [ ] Locates the household's AHJ-adopted NEC and NFPA 70E references and demonstrates looking up a topic
- [ ] Names the rule that manufacturer's literature and AHJ-adopted code are the authorities, not the AI tutor
- [ ] Demonstrates safe tool storage at end of session

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail (do not surface)`

Corrections / notes:

```

```

---

### elc-001: Read electrical nameplate / rating label

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `False` (AI-mentor end-to-end; cover-closed only)
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Hazards (confirm each)

- [ ] Misreading voltage propagates to elc-021 / energized work
- [ ] Misreading current draw / full-load ampacity propagates to NEC sizing
- [ ] Misreading AIC; a breaker with insufficient AIC can explode during a short
- [ ] Reaching into a panel to find a hidden label (cover stays on at this band)

#### Demonstration criteria

- [ ] Locates rating label on each of: panel, breaker, receptacle, fixture, appliance, low-voltage adapter (cover closed)
- [ ] Photographs each clearly; every printed field legible
- [ ] Extracts every operative field onto a nameplate card
- [ ] Names what MCA / MOP / AIC fields mean in plain language
- [ ] Names listing-mark requirement
- [ ] Reads three different labels and submits cards

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-002: Identify components from diagrams and with covers closed

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `False`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Demonstration criteria

- [ ] Names every visible exterior component of the residential service
- [ ] Names every visible branch-circuit and low-voltage component
- [ ] Matches each physical component to its standard schematic symbol
- [ ] Names hot / neutral / equipment-grounding conductor color conventions
- [ ] Names neutral-to-ground bond at main service equipment ONLY per AHJ
- [ ] Names that access panels NOT opened at this band; breakers / disconnects / switches NOT operated at this band
- [ ] Reads three different equipment categories and submits cards
- [ ] Names difference between AC and heat pump in one sentence
- [ ] Names what is and is not in this band

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-003: Ohm's law and basic circuit theory

- Node type: `knowledge`
- Progression band: `helper`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Demonstration criteria

- [ ] V from I and R; I from V and R; R from V and I (10+ problems)
- [ ] P from V and I; P from I and R; P from V and R (5+ problems)
- [ ] Correct units (volts, amperes, ohms, watts; sensible prefixes)
- [ ] Names current (not voltage) as cause of injury
- [ ] Names apparent / real / power-factor distinction for inductive loads
- [ ] Solves 3 real-residential word problems
- [ ] Sanity-checks against expected residential values

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-004: Series and parallel circuits; basic load calculation

- Node type: `knowledge`
- Progression band: `helper`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Demonstration criteria

- [ ] Series circuits: 3 problems with total R, I, V across each resistor
- [ ] Parallel circuits: 3 problems with equivalent R, total I, branch currents
- [ ] Names residential branches wire receptacles / switches / fixtures in PARALLEL
- [ ] Residential load-calc problem with 80% continuous-load rule applied
- [ ] Names voltage-drop concept; defers to AHJ-adopted NEC guidance
- [ ] Sanity-checks against expected residential values

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-005: Read wiring diagrams and schematics

- Node type: `knowledge`
- Progression band: `helper`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Demonstration criteria

- [ ] Names every standard residential symbol
- [ ] Annotates single switched fixture diagram
- [ ] Annotates three-way switched fixture (common and travelers)
- [ ] Annotates GFCI receptacle (LINE and LOAD distinction)
- [ ] Annotates AFCI branch
- [ ] Annotates MWBC (shared neutral; safety habit for elc-021)
- [ ] Annotates interconnected smoke / CO alarms
- [ ] Names color-coding convention and re-identification exception

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-006: Residential electrical service anatomy

- Node type: `knowledge`
- Progression band: `helper`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Demonstration criteria

- [ ] Names every major component of a residential service in order with function
- [ ] Identifies in household's actual service: utility entry, meter, main, panel, subpanels, grounding electrode
- [ ] Names LINE / LOAD distinction at main disconnect; service-entrance work OUT OF SCOPE at foundation
- [ ] Names neutral-to-ground bond at main only; subpanel neutral isolated
- [ ] Names grounding electrode system components
- [ ] Names overcurrent protection (NEC Article 240) and ampacity (Article 310)
- [ ] Names 120/240V split-phase residential convention
- [ ] Annotates representative one-line diagram

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-007: Conductor sizing and ampacity basics

- Node type: `knowledge`
- Progression band: `helper`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Demonstration criteria

- [ ] Names Article 310 as source; locates the relevant tables in AHJ-adopted edition
- [ ] Names ampacity table structure (rows AWG, columns 60/75/90 deg C)
- [ ] Names termination-temperature rule (60/75/90; lower of conductor and termination)
- [ ] Names ambient and conductor-count correction factors
- [ ] Names copper vs aluminum separate tables
- [ ] Solves 3 guided ampacity look-ups in AHJ-adopted edition
- [ ] Names overcurrent-device-protects-conductor rule (Article 240)
- [ ] Catches unreasonable answer (14 AWG on 30A breaker)

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-008: Grounding and bonding theory

- Node type: `knowledge`
- Progression band: `helper`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Demonstration criteria

- [ ] Names GROUNDING vs BONDING distinction with one-paragraph explanation
- [ ] Names grounding electrode system components
- [ ] Names GEC and role
- [ ] Names main bonding jumper and once-only bond rule
- [ ] Names EGC and role (fault path, not normal current)
- [ ] Names fault-clearing path explicitly: hot to metal -> EGC -> main bonding jumper -> neutral -> transformer
- [ ] Names ground rod's role (stabilize to earth; NOT a fault path)
- [ ] Names rule against bonding neutral to ground at subpanel; names failure modes
- [ ] Names that hands-on grounding work is licensed-electrician work; NOT in scope at foundation
- [ ] Annotates residential grounding-and-bonding diagram

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-009: Meter and tool literacy (CAT ratings)

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `False`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Hazards (confirm each)

- [ ] Wrong CAT rating multimeter (CAT II on CAT III circuit; one of the most documented causes of injury)
- [ ] Damaged test leads (short to user or surface)
- [ ] Un-inspected insulating gloves (ozone cracking, pinholes)
- [ ] Non-insulated tools near energized equipment (slip causes arc flash)
- [ ] No live measurement at this band; live measurement is elc-021

#### Demonstration criteria

- [ ] Identifies meter's CAT rating and voltage; confirms CAT III at 600V minimum or names upgrade needed
- [ ] Names each CAT Category and example application
- [ ] Identifies every range on selector
- [ ] Identifies test-lead connectors and color coding
- [ ] Inspects test leads visually; reports damage
- [ ] Identifies finger-guard probes per IEC 61010-031
- [ ] Identifies current-circuit fuse; names manufacturer-fuse-only rule
- [ ] Identifies IEC 60900 / ASTM F1505 marking on insulated tools (1000V residential standard)
- [ ] Inspects insulated tool visually; reports damage
- [ ] Identifies insulating glove rating (Class 00 / 500V minimum); performs air-roll inspection
- [ ] Names NO LIVE MEASUREMENT at this band
- [ ] Builds meter-and-tool card

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elc-021: De-energize, LOTO, live-dead-live verification (apprentice gold standard, ELECTRICAL HAZARD)

- Node type: `technique`
- Progression band: `apprentice`
- Supervision required: `True` (LICENSED ELECTRICIAN physically present)
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

**THIS NODE REQUIRES THE MOST RIGOROUS REVIEW IN THE BATCH.** Reviewer must hold (or co-review with someone who holds) current electrical credentials and NFPA 70E familiarity. The supervision_basis carries the verbatim licensed-electrician-physically-present language; a test in `test_electrical_content.py::TestElc021HardLimit` enforces this language remains.

#### Hazards (confirm each is named correctly and at the right scale)

- [ ] ELECTROCUTION RISK at 120V or 240V residential
- [ ] ARC FLASH from a short during energized work
- [ ] WRONG-CIRCUIT or WRONG-DISCONNECT FAILURE (panel labels commonly wrong)
- [ ] METER FAILURE (depleted battery, blown fuse, broken probe lead, wrong CAT rating)
- [ ] BACKFEED from generator or solar PV
- [ ] MWBC shared-neutral hazard
- [ ] NEUTRAL-TO-GROUND BOND FAULT
- [ ] STORED ENERGY IN CAPACITORS (capacitor work is separate competency)
- [ ] WET CONDITIONS
- [ ] Sharp sheet-metal edges

#### PPE required

- [ ] Trade PPE per els-001
- [ ] ANSI Z87.1 safety glasses throughout
- [ ] Insulating gloves Class 00 / 500V minimum; manufacturer + OSHA inspection
- [ ] Leather protectors over insulating gloves per NFPA 70E
- [ ] Long sleeves and arc-rated clothing per NFPA 70E
- [ ] No metal jewelry
- [ ] CAT III at 600V minimum DMM with finger-guard probes
- [ ] Insulated tools rated 1000V per IEC 60900 / ASTM F1505
- [ ] Lockout-tagout hardware (breaker lockout device, padlock, tag per OSHA 1910.145)

#### Supervision basis (confirm the licensed-electrician-physically-present rule and the AI-mentor limit)

- [ ] LICENSED ELECTRICIAN (or journeyman/master per AHJ) PHYSICALLY PRESENT
- [ ] Licensed electrician watches meter reading, probe placement, LOTO sequence
- [ ] AI tutor mentors procedure walkthrough and reviews artifacts; does NOT stand in
- [ ] Households without resident licensed electrician arrange paid session, vocational program, apprentice arrangement, or defer
- [ ] AI tutor and supervising adult do NOT substitute at the live moment

#### Demonstration criteria

- [ ] Reviews nameplate (elc-001) and component ID (elc-002) before starting
- [ ] Confirms no active backfeed sources; licensed electrician confirms isolation
- [ ] Inspects multimeter and leads; CAT III at 600V confirmed
- [ ] Inspects insulating gloves; air-roll test with electrician's coaching
- [ ] Confirms panel working space and headroom per AHJ-adopted NEC
- [ ] FIRST live test on known live source; reading announced; electrician confirms
- [ ] Operates breaker to OFF correctly per panel type
- [ ] Applies lockout device, padlock, tag; key kept exclusively
- [ ] DEAD test at work point: every pair of conductors (120V: H-N, H-G, N-G; 240V: L1-G, L2-G, L1-L2, L1-N, L2-N; MWBC: each H-N plus explicit confirmation of unshared neutral)
- [ ] SECOND live test on same source; reading announced; electrician confirms dead test valid
- [ ] Photographs locked breaker with tag; written narration countersigned by electrician
- [ ] Names lockout release rule (only person who applied it, only after work complete)
- [ ] Names what invalidates dead reading
- [ ] Names that this covers only line-voltage at work point; LV / capacitor / service-entrance / refrigerant work separate

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail (do not surface)`

Corrections / notes:

```

```

---

### elcert-nec: NEC (NFPA 70) and NFPA 70E familiarity

- Node type: `certification_prep`
- Credential body: NFPA (codes themselves; AHJ adopts edition)
- Legal status: `jurisdiction_specific`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Confirm

- [ ] `credential_body` names NFPA correctly
- [ ] `authorizing_scope` correctly describes the NEC and NFPA 70E as standards (not credentials in legal sense)
- [ ] `knowledge_domains_covered` lists residential focus topics (Articles 210, 220, 230, 240, 250, 310, 314, 330/334, 404, 406, 408, 410, 422, 430, 440, 460, 690, 702) without reproducing code text
- [ ] `exam_taken_through`: NFPA-approved providers / AHJ for journeyman exam
- [ ] `prepares_understanding_only` is True
- [ ] No reproduced exam fields
- [ ] AHJ-adopted-edition-governs caveat present throughout

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elcert-licensing: State electrician licensing path

- Node type: `certification_prep`
- Credential body: AHJ (state, county, or municipality)
- Legal status: `jurisdiction_specific`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Confirm

- [ ] `credential_body` names AHJ correctly with state / county / municipality framing
- [ ] `authorizing_scope` distinguishes apprentice / journeyman / master / contractor and names low-voltage / limited-energy specialty
- [ ] `knowledge_domains_covered` lists journeyman-exam scope and master business-and-law scope
- [ ] `eligibility.experience_requirements` cites the ~8,000 hours / 4 years range with "varies by AHJ" caveat
- [ ] `prerequisites` name the electrical training ALLIANCE plus state non-union and employer-based pathways
- [ ] `exam_taken_through`: AHJ or PSI / Prov Inc. authorized testing partner; METHEAN does not administer
- [ ] `supervised_hours_through` explicitly states METHEAN is NOT a substitute for registered apprenticeship hours
- [ ] `prepares_understanding_only` is True
- [ ] No reproduced exam fields

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

### elcert-safety: OSHA 10 / 30 + NFPA 70E training (adjacent credentials)

- Node type: `certification_prep`
- Credential body: OSHA (Outreach trainers) / NFPA + providers (70E training)
- Legal status: `optional`
- Current review state: `reviewed=False`, `reviewer=None`, `reviewed_on=None`

#### Confirm

- [ ] `credential_body` names OSHA-authorized Outreach Training Program trainers AND NFPA-approved or employer-program providers
- [ ] `authorizing_scope` states OSHA Outreach is NOT a license in the legal sense and NOT a substitute for site-specific OSHA training
- [ ] `knowledge_domains_covered` lists OSHA 10 / 30 topics and NFPA 70E topics
- [ ] `exam_taken_through`: OSHA-authorized trainers for OSHA Outreach; recognized providers for NFPA 70E; METHEAN does not deliver
- [ ] `prepares_understanding_only` is True
- [ ] No reproduced exam fields

**Reviewer's verdict:**  `[ ] Pass`  `[ ] Pass with corrections`  `[ ] Fail`

Corrections / notes: ```                  ```

---

## Author-flagged uncertainties (U1 through U14)

The author of these nodes named the following as places where they leaned conservative but could not claim independent verification. Reviewer confirms or corrects each.

### U1. NEC edition variance

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  The NEC is on a 3-year cycle. AHJ-adopted editions vary by state and by municipality. The trade defers all article-number citations to "the relevant NEC articles (e.g. Article 250 for grounding and bonding)" with the explicit caveat that the AHJ-adopted edition governs. No specific code text is reproduced. Reviewer confirms the no-reproduction-and-defer-to-AHJ framing is correct.

  Reviewer's correction:

  ```

  ```

### U2. Apprenticeship hours requirement variance

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  The trade names approximately 8,000 hours / 4 years for journeyman eligibility "in many states" and explicitly states "the AHJ's current published requirements are authoritative and the learner confirms them." No specific hours are written into the node beyond the common range. Reviewer confirms the framing is correct.

  Reviewer's correction:

  ```

  ```

### U3. Low-voltage / limited-energy license variance

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  Many states have low-voltage / limited-energy as a distinct license; some include it in the regular electrician license; some don't license it at all. The trade names this as a likely specialty path the learner confirms with their state AHJ. Reviewer confirms the framing accurately reflects the state-by-state variance.

  Reviewer's correction:

  ```

  ```

### U4. Multimeter CAT rating

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  elc-009 and elc-021 specify CAT III at 600V minimum as the residential standard per NFPA 70E for 240V residential measurement; CAT IV acceptable; CAT II or unrated NOT acceptable. This mirrors HVAC hc-021. Defers to NFPA 70E and IEC 61010-1 / UL 61010-1 for category definitions. Reviewer confirms this matches current NFPA 70E.

  Reviewer's correction:

  ```

  ```

### U5. Arc-flash boundaries on residential

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  els-001 and elc-021 name arc-flash hazard on residential as smaller than commercial but real; defer boundary calculation to NFPA 70E and the licensed electrician present. The default is de-energize and verify dead before opening, which removes the arc-flash hazard at the work point. Reviewer confirms this framing is correct and the deferral to NFPA 70E is appropriate.

  Reviewer's correction:

  ```

  ```

### U6. Bonding vs grounding terminology

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  elc-008 explicitly distinguishes grounding (connection to earth) from bonding (connection between metal parts to keep them at same potential), names that both are required and serve different safety functions, and defers code requirements to AHJ-adopted NEC Article 250. The fault-clearing path is named explicitly. Reviewer confirms the conceptual treatment is accurate.

  Reviewer's correction:

  ```

  ```

### U7. Generator and solar PV backfeed risk

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  els-001 and elc-021 name generator backfeed (without transfer switch or interlock) and solar PV backfeed (without proper anti-islanding / rapid-shutdown) as documented failure modes. Code-specific rules deferred to AHJ-adopted NEC. Reviewer confirms the framing is accurate to current NEC requirements.

  Reviewer's correction:

  ```

  ```

### U8. MWBC shared-neutral hazard

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  els-001, elc-005, and elc-021 name the MWBC shared-neutral hazard explicitly: opening the neutral on an energized MWBC places full line-to-line voltage on the loads and produces voltage on the formerly-neutral wire. elc-021's dead-test procedure includes explicit MWBC neutral verification with the licensed electrician identifying the MWBC at the panel. Reviewer confirms the description is technically accurate and the verification procedure is sound.

  Reviewer's correction:

  ```

  ```

### U9. Insulating glove class for 240V

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  Class 00 (rated 500V) minimum per NFPA 70E for residential 120V or 240V verification. Mirrors HVAC hc-021. Defers to NFPA 70E and the glove manufacturer for inspection (visual and air-roll test). Leather protectors required per NFPA 70E. Reviewer confirms Class 00 minimum is correct for residential and that the leather-protector requirement is named.

  Reviewer's correction:

  ```

  ```

### U10. LOTO written procedure

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  elc-021 defers the equipment-specific written LOTO procedure to the employer's program per OSHA 29 CFR 1910.147 or, if no written procedure exists, the licensed electrician produces one before the work begins. Reviewer confirms this deferral is correct and the written-procedure requirement under OSHA is honored.

  Reviewer's correction:

  ```

  ```

### U11. Service-entrance vs branch-circuit scope

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  el-root, els-001, and elc-006 explicitly name the foundation's scope boundary at the load side of the main disconnect. Service-entrance work (line side, meter work, utility supply) is regulated more strictly, may require utility involvement, and is OUT OF SCOPE at the foundation. Reviewer confirms this scope boundary is correctly drawn and consistently enforced across nodes.

  Reviewer's correction:

  ```

  ```

### U12. Knob-and-tube and old aluminum branch-circuit wiring

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  els-001 names pre-1950s knob-and-tube and 1965-1973 aluminum branch-circuit wiring as recognition-only knowledge at the helper band (don't touch; defer to the licensed electrician). Treatment competencies are gated for later batches. Reviewer confirms the recognition-only framing is appropriate at this band and the deferral to licensed electrician for treatment is correct.

  Reviewer's correction:

  ```

  ```

### U13. AFCI / GFCI requirements per NEC

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  AFCI and GFCI required locations expand each NEC cycle. els-001, elc-002, and elc-005 name AFCI and GFCI as required by the AHJ-adopted NEC without enumerating specific locations (which depend on edition). Reviewer confirms the deferral to AHJ-adopted edition is correct.

  Reviewer's correction:

  ```

  ```

### U14. Permits and inspections

- [ ] **Confirmed as authored.** Notes:

- [ ] **Correction required.** Authored framing:

  Residential electrical work in most jurisdictions requires permits and inspections by the AHJ. The foundation does not include any work requiring a permit (no terminations, no install, no service work). Future batches authoring hands-on install / service work must include permit and inspection content. Reviewer confirms the foundation correctly stays below the permit threshold and notes any work in the foundation that might otherwise trigger a permit requirement.

  Reviewer's correction:

  ```

  ```

---

## After this review

Once every node above is set to `safety_review.reviewed = True` in `electrical_content.py` (with `reviewer` and `reviewed_on` recorded), the electrical trade's first authoring batch is cleared for surfacing through the integration gate. Until then, the gate (per `requires_human_safety_review`) refuses every node where the helper returns True and `safety_review.reviewed` is False.

**For `elc-021` specifically**, the integration must additionally confirm at the time of each learner's attempt that a licensed electrician is physically present at the live-dead-live verification. The AI tutor does NOT stand in. This is a runtime gate above the content-review gate.

**Subsequent batches** for this trade will add (in priority order) low-hazard de-energized hands-on competencies (receptacle / switch / fixture replacement after live-dead-live verification, with adult on premises and the licensed electrician available for the verification step), the apprentice-band knowledge work for advanced NEC topics (commercial chapters, motor work, solar PV) and NFPA 70E arc-flash analysis, the journeyman-band install and service competencies (each behind its own safety gate, all under licensed electrician physically present for energized acts), and the qualified-band project nodes (a complete residential install, a service-call portfolio, a training-of-apprentice record). Each batch will go through the same checklist process before surfacing.
