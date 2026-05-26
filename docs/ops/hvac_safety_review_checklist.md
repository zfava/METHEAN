# HVAC safety review checklist

Generated from `backend/app/content/hvac_content.py`. The checklist below renders the actual hazards, PPE, and demonstration criteria for every authored node. Do not edit the node content from this checklist; edit `hvac_content.py` and regenerate this file. No node may be surfaced to a learner until its `safety_review.reviewed` is set to True by a qualified human reviewer, with `reviewer` and `reviewed_on` recorded; this is the contract this checklist exists to support.

**HIGHER-HAZARD TRADE.** HVAC is one of the highest-hazard trades in the catalog: it combines line-voltage and low-voltage electrical, refrigerant (EPA Section 608 regulated), combustion gases and carbon monoxide, hot surfaces, falls and ladders, lifting, sharp sheet-metal edges, confined spaces, asbestos in older systems, and indoor air contaminants. This trade requires the MOST RIGOROUS shop / trade review before any node is cleared for surfacing. Recommended reviewer profile:

- **For `hvac-root`, `hs-001`, `hc-001`, `hc-002`**: a licensed HVAC technician (state license OR journeyman/master credential per the local AHJ) with current field experience in residential service.
- **For `hc-021` (DMM + LOTO live-dead-live)**: BOTH the licensed HVAC technician AND a licensed electrician (or an HVAC technician with explicit electrical scope per the local AHJ). Familiarity with current NFPA 70E and OSHA 29 CFR 1910.147 is required for the reviewer.
- **Recommended additional reviewer**: a safety professional familiar with OSHA general industry standards for the LOTO content; a person with EPA Section 608 certification for any deferrals to refrigerant-related material.

## Reviewer identification

- Reviewer name: ____________________________________________
- Relevant HVAC / electrical trade experience (years, type, credentials; license type and state; EPA-608 status; NFPA 70E currency): ____________________________________________
- Date of this review: ____________________________________________

## Completion contract

On completion of this review, for each node confirmed correct:

1. In `backend/app/content/hvac_content.py`, set the node's `safety_review.reviewed` to `True`, `safety_review.reviewer` to the reviewer's name and credentials, and `safety_review.reviewed_on` to the date in ISO 8601 (`YYYY-MM-DD`).
2. If any item below requires correction, the correction is made in `hvac_content.py` and this checklist is regenerated, and the review is repeated on the corrected node.
3. No node where `safety_review.reviewed` is `False` may be surfaced to a learner. The integration gate is the responsibility of `learning_context` (see the TODO in `backend/app/services/node_content.py::requires_human_safety_review`).
4. For `hc-021` specifically, the integration gate must additionally confirm that any learner attempting the competency has a qualified human (licensed HVAC technician or licensed electrician) physically present at the live-dead-live verification per the node's `supervision_basis`. The AI tutor does NOT stand in for the qualified human at the live moment.

---

## Per-node review

### hvac-root: HVAC (intro to master technician, mastery path)

- Node type: `root`
- Supervision required: see `default_supervision_policy` (four categories: knowledge_work AI-tutor-mentored; low_hazard_hands_on_work adult-on-premises; higher_hazard_hands_on_work qualified-human-physically-present per subsystem; mastery framing, not certification)
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Supervision policy categories (confirm each is honest and complete; check or correct)

- [ ] `knowledge_work`: AI tutor mentors end-to-end (nameplate reading, component ID from photographs, code interpretation, procedure walkthroughs on paper, troubleshooting trees, artifact review)
- [ ] `low_hazard_hands_on_work`: adult on premises (parent or other resident adult; no HVAC credentials required for this category)
- [ ] `higher_hazard_hands_on_work`: qualified human physically present, named per subsystem (licensed electrician for line voltage; EPA-608-certified person for refrigerant; licensed gas fitter for gas piping per the AHJ; OSHA-defined competent person for fall protection per 1926.32; OSHA 1910.146-trained entrant and attendant for confined spaces)
- [ ] `households_without_a_resident_qualified_mentor`: paid professional session, vocational-school program, apprentice arrangement with a working contractor, or defer until the qualified human is arranged
- [ ] `all_bands`: power tools and any operation that opens an enclosure containing refrigerant, gas, or live conductors is supervised; no unsupervised hands-on work on hazardous subsystems below the qualified band
- [ ] Mastery framing: this trade is mastery-first; certification (EPA-608, journeyman, NATE) is a later step, not the immediate gate

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in hvac_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### hs-001: HVAC safety (electrical, refrigerant, combustion/CO, thermal, falls, lifting, sheet-metal, confined spaces, asbestos, IAQ)

- Node type: `safety`
- Progression band: `helper`
- Supervision required: `True`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly and at the right scale; check or correct)

- [ ] Electrical shock and electrocution from line voltage (residential 240V/60Hz/1-phase typical; commercial 208V/3-phase or 480V/3-phase; nameplate per hc-001 is the authority); at residential fault current, 240V across the heart can stop it; absence of voltage is verified per hc-021 before any wiring contact
- [ ] Electrical shock from stored energy in start and run capacitors (lethal charge for minutes to hours after de-energization; discharged with manufacturer-specified resistor before direct contact; capacitor discharge is its own competency, not in this batch)
- [ ] Arc flash from a short during energized work (arc-rated PPE per NFPA 70E for energized work; the default in this trade is to de-energize and verify dead before opening)
- [ ] Low-voltage control circuits (24VAC typical; lower shock risk than line voltage but real, with involuntary-reaction risk; treated as live until verified dead)
- [ ] Refrigerant exposure (ASHRAE 34 classes A1, A2L, A3; R-410A A1 dominant in residential through 2020s; R-454B and R-32 A2L now replacing R-410A under AIM Act and EPA SNAP; A2L has ignition risk and different leak-detection requirements; refrigerant type on nameplate governs; EPA Section 608 regulates hands-on; not in this batch)
- [ ] Frostbite from direct skin contact with escaping refrigerant (high-pressure flash to below freezing; PPE per ASHRAE 34 and refrigerant SDS)
- [ ] Thermal burns from hot surfaces (furnace heat exchangers, vent pipes, draft inducer motors; brazed joints; brazing not in this batch and has its own gate)
- [ ] Carbon monoxide (CO) poisoning from incomplete combustion (NG, LP, fuel oil; CO colorless and odorless; alarm activation is a stop-work event; CDC action levels and recognition; node does not name action-level ppm)
- [ ] Natural gas (NG) and propane (LP) leaks (mercaptan odorant; smell-of-gas stop-work event; ventilate area; no ignition sources operated; gas utility's emergency line called from outside; NFPA 54 regulates gas-system work; not in this batch)
- [ ] Falls from ladders, rooftops, and elevated air-handler platforms (OSHA 1926 Subpart M for fall protection; OSHA 1910.23 for ladders; rooftop and ladder competencies not in this batch)
- [ ] Lifting injuries (compressors, condensers, air handlers, packaged units 50-several-hundred-lb; two-person or mechanical assist is the rule; OSHA / NIOSH lifting guidance)
- [ ] Sheet-metal edge cuts (one of the most frequent HVAC injuries per industry observation; cut-resistant gloves default for any sheet-metal handling)
- [ ] Eye injury from metal swarf, insulation fibers, refrigerant or chemicals (safety glasses default; face shield for chemicals and refrigerant per SDS)
- [ ] Confined-space exposure (crawl spaces, attics in summer, mechanical rooms; OSHA 1910.146 permit-required confined space; written program, attendant, gas testing, rescue plan required; not in this batch)
- [ ] Asbestos in pre-1980 systems (duct mastic, boiler insulation, pipe lagging, gaskets, some furnace components; visual ID unreliable; EPA and state asbestos rules; pre-1980 components treated as suspect; no cutting/scraping/replacing in this batch)
- [ ] Indoor air quality contaminants (mold in coil pans and ducts, bacterial growth in condensate, rodent/bird debris in attic equipment; N95 or higher per the contaminant)
- [ ] Pinch points and rotating equipment (blower wheels, condenser fans, draft inducers, compressor pulleys; power verified off per hc-021 before contact; loose clothing, jewelry, long hair controlled)
- [ ] Fire hazard during brazing, soldering, and any hot work (combustibles cleared, fire watch, rated extinguisher; hot work not in this batch)

#### PPE required (confirm each item is correctly named, including what is required and what is permitted; check or correct)

- [ ] Closed-toe leather work boots with non-slip soles; steel-toe or composite-toe for any equipment lifting or work where dropped tool/part is a hazard; no sneakers in mechanical room or on rooftop
- [ ] Safety glasses (ANSI Z87.1) as shop-wide default any time enclosure is open, sheet metal handled, or refrigerant/chemical operation performed; full face shield in addition for refrigerant operations per SDS and ASHRAE 34, for battery work, and for chemical operations per SDS
- [ ] Cut-resistant gloves (ANSI/ISEA 105 cut level A4 or higher recommended for sheet-metal handling; actual cut level per household or employer program; node names cut-rated requirement without prescribing level)
- [ ] Insulating gloves rated for the voltage actually being worked for any energized electrical work per NFPA 70E (default is to de-energize per hc-021; energized work requires rated gloves AND arc-rated PPE for calculated incident energy AND documented energized-work justification; energized work not in this batch)
- [ ] Hearing protection (ANSI/ASA S3.19) in spaces with running equipment requiring raised voice per current OSHA / NIOSH noise exposure guidance
- [ ] Respiratory protection (N95 or higher per contaminant; current NIOSH guidance and local AHJ) for dust, biological contamination, fiberglass in confined attics, or chemical operations per SDS; fit-testing per household or employer program
- [ ] Fall protection per OSHA 29 CFR 1926 Subpart M for any work above OSHA-defined threshold (personal fall arrest system inspected before each use per manufacturer and OSHA; rooftop/elevated work not in this batch; requirement named here so it appears in the walkthrough)
- [ ] Long sleeves rolled down near hot surfaces, brazing, or biological contamination; hair tied back if long enough to fall into fan or onto hot surface; no loose jewelry near rotating equipment or live electrical
- [ ] Sun protection (brimmed hat, long sleeves, sunscreen per current public-health guidance) for outdoor or rooftop work in warm months; hydration per current CDC / NIOSH guidance

#### Supervision basis (confirm the basis is honest and the AI-mentor framing is correct)

- [ ] Adult on premises walks learner through every hazard in the actual mechanical room, actual equipment, actual tool kit; signs off only when learner can name and locate each
- [ ] Supervising adult does NOT need HVAC credentials for the walkthrough itself; a parent or resident adult counts
- [ ] AI tutor may guide what to look for and review the recorded walkthrough video
- [ ] No self-attestation on safety
- [ ] Mentor confirms household's plans for: tetanus immunization status; CO alarm presence/function per current NFPA 720 and AHJ; fire extinguisher rating/placement per local fire-safety authority confirmation; first aid kit per ANSI/ISEA Z308.1 or current American Red Cross guidance
- [ ] Mentor confirms household's understanding that higher-hazard hands-on work on electrical, refrigerant, gas, combustion, rooftop, or confined-space subsystems requires a qualified human physically present per the trade root's supervision policy

#### Demonstration criteria (confirm each is measurable and correctly states the bar; check or correct)

- [ ] Names every PPE item on the list and explains when each is required and when each is permitted
- [ ] Locates the first aid kit and confirms it meets ANSI/ISEA Z308.1 or current American Red Cross guidance
- [ ] Locates the fire extinguisher within reach of the mechanical space, names its rating, confirms rating is appropriate per household's confirmation with local fire-safety authority
- [ ] Locates the CO alarm(s), confirms each is listed (UL 2034 residential or UL 2075 commercial), within manufacturer's service-life window, placed per current NFPA 720 and local AHJ
- [ ] Names the household's tetanus immunization status arrangement; mentor confirms every working household member is current per their healthcare provider's recommendation
- [ ] Names the absence-of-voltage rule (live-dead-live per NFPA 70E and OSHA 1910.147) and points to where hc-021 lives in the helper-to-apprentice path
- [ ] Names the capacitor-treated-as-charged rule and the no-capacitor-contact-at-this-band rule
- [ ] Names that refrigerant operations are EPA Section 608 work requiring 608-certified person physically present; not in scope at this band
- [ ] Names the smell-of-gas stop-work sequence (leave area without operating switch/phone/ignition; call gas utility emergency line from outside; do not re-enter until cleared)
- [ ] Names the CO alarm activation sequence (evacuate; call emergency services from outside; do not re-enter until cleared by emergency services or gas utility)
- [ ] Names the asbestos suspect rule for pre-1980 components and the stop-and-ask rule when encountering suspect material
- [ ] Demonstrates safe lifting form on a real component within learner's safe carry weight, OR refuses heavier component and names the two-person / mechanical assist rule
- [ ] Demonstrates safe handling of cut sheet metal with cut-resistant gloves, edges identified and controlled
- [ ] Names that hot work (brazing, soldering) is not in scope at this band and requires its own competency
- [ ] Names that rooftop work requires fall protection per OSHA 1926 Subpart M; confined-space entry requires OSHA 1910.146 permit, program, attendant, rescue plan; both not in this batch
- [ ] Locates the manufacturer's service literature for the household's actual equipment and demonstrates looking up one fact
- [ ] Names the rule that manufacturer's service literature is the authority for the specific equipment, not a general reference
- [ ] Demonstrates safe tool storage at end of session (sharp tools sheathed/cased, heavy tools returned, no tools in walkways or on equipment)

#### Standard references (confirm each is current and the household has confirmed locally where applicable)

- [ ] ANSI/ISEA Z308.1 (Workplace First Aid Kits)
- [ ] American Red Cross home/shop first-aid kit guidance
- [ ] OSHA 29 CFR 1910.147 (Lockout-Tagout)
- [ ] OSHA 29 CFR 1910.146 (Permit-Required Confined Spaces)
- [ ] OSHA 29 CFR 1910.137 and 1910.335 (Electrical PPE and Safe Practices)
- [ ] OSHA 29 CFR 1926 Subpart M (Fall Protection)
- [ ] OSHA 29 CFR 1910.23 (Walking-Working Surfaces, ladders)
- [ ] NFPA 70E (Electrical Safety in the Workplace; current edition)
- [ ] NFPA 70 (NEC; current edition per local AHJ)
- [ ] NFPA 54 (National Fuel Gas Code; current edition per local AHJ)
- [ ] NFPA 720 (CO Detection and Warning Equipment)
- [ ] EPA Section 608 of the Clean Air Act (refrigerant handling certification)
- [ ] ASHRAE Standard 34 (Refrigerant Designation and Safety Classification; current edition)
- [ ] ASHRAE Standard 62.1 and 62.2 (Ventilation for IAQ, commercial and residential)
- [ ] AHRI rating standards (current; SEER2, HSPF2, EER2, AFUE)
- [ ] UL 2034 (residential CO alarms) and UL 2075 (commercial CO alarms)
- [ ] Current CDC CO guidance for action levels and recognition
- [ ] Current CDC / NIOSH outdoor-worker heat-illness prevention guidance
- [ ] Current EPA and state asbestos rules for pre-1980 components
- [ ] Tetanus immunization per each household member's healthcare provider per current ACIP / CDC guidance
- [ ] Manufacturer service literature for the specific equipment
- [ ] Local AHJ adopted codes (NEC, NFPA 54, IMC, UMC, local mechanical/energy codes) — varies by jurisdiction
- [ ] Employer's written lockout-tagout program (for apprentice under a contractor or vocational program)

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in hvac_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### hc-001: Read an HVAC equipment nameplate

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `False`
- AI-mentor framing: AI tutor mentors end-to-end; no human supervision required for cover-closed nameplate reading
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Misreading the nameplate voltage and applying wrong meter range / PPE downstream (not direct hazard at this band; downstream error)
- [ ] Misreading the refrigerant type and missing A1/A2L/A3 safety class difference (not direct hazard at this band; downstream error in later refrigerant operation)
- [ ] Misreading the MCA / MOP (not direct hazard at this band; downstream error in any later electrical install)
- [ ] Reaching into a panel or enclosure to find a hidden nameplate (rule: cover stays on at this band; any nameplate not visible from outside is photographed by a qualified human with the disconnect open and verified dead per hc-021)

#### PPE required (confirm each item is correctly named; check or correct)

- [ ] Trade PPE per hs-001 (closed-toe shoes; trade's general defaults); no additional PPE required for nameplate reading from outside
- [ ] Eye protection optional but recommended in a dusty mechanical space

#### Supervision basis (confirm the AI-mentor framing is honest)

- [ ] Reading a nameplate visible from outside the enclosure involves no tool use, no opened enclosure, no live circuit contact, no moving parts, no chemical or refrigerant exposure
- [ ] AI tutor mentors end-to-end: learner photographs, AI confirms each field, learner builds nameplate card
- [ ] Trade-level supervision from hvac-root still applies in the sense that no enclosure is opened and no energized work is performed

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable and correct; check or correct)

- [ ] Locates the nameplate on a piece of household HVAC equipment without opening any enclosure
- [ ] Photographs the nameplate clearly enough that every printed field is legible
- [ ] Extracts every operative field onto a nameplate card: manufacturer; model; serial; manufacture date (decoded if encoded in serial); equipment type; voltage; frequency; phase; MCA; MOP; refrigerant type and factory charge (if applicable); rated capacity; efficiency rating; listing marks
- [ ] Submits the nameplate card and photograph to the AI tutor; AI tutor confirms each field or names discrepancy; learner reconciles
- [ ] Names which fields the nameplate did not supply
- [ ] Names what MCA and MOP fields mean in plain language; names that wiring itself is NEC-regulated work, not in this batch
- [ ] Names the ASHRAE 34 safety class of the refrigerant on the nameplate using the AI tutor's lookup; names that safety class affects later refrigerant operations (not in this batch)
- [ ] Reads three different nameplates correctly with complete card for each

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in hvac_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### hc-002: Identify the major components of a residential split-system AC or heat pump by sight

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `False`
- AI-mentor framing: AI tutor mentors end-to-end; photo-based identification with the unit cover closed
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Reaching toward a spinning condenser fan or blower in operation (rule: no body part in airflow path of running fan)
- [ ] Touching a hot suction or liquid line during operation (no touching during operation; visual ID only at this band)
- [ ] Touching the compressor or other hot components during or shortly after operation
- [ ] Opening the electrical disconnect or any enclosure to find a component (rule: cover stays on at this band)
- [ ] Sharp sheet-metal edges on the outdoor unit cabinet (cut-resistant gloves on if handling cabinet)
- [ ] Slip hazard from condensate or seasonal water around outdoor unit

#### PPE required (confirm each item is correctly named; check or correct)

- [ ] Trade PPE per hs-001
- [ ] Safety glasses for any close work near the outdoor unit
- [ ] Cut-resistant gloves if any handling of cabinet panels is anticipated; bare hands acceptable for arm's-length visual ID

#### Supervision basis (confirm the AI-mentor framing is honest)

- [ ] Visual identification with cover closed and no enclosure opening involves no tool use, no live circuit contact, no refrigerant contact, no opened combustion system, no rotating equipment contact
- [ ] AI tutor mentors end-to-end: learner photographs with unit cover closed, AI confirms each identification
- [ ] Trade-level supervision from hvac-root still applies in the sense that no enclosure is opened and no energized work is performed

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable and correct; check or correct)

- [ ] Names every visible component of the outdoor unit from outside the cabinet (cabinet, condenser coil, condenser fan, line set, service ports with caps, outdoor disconnect, electrical whip, access panels named but not opened)
- [ ] Names every visible component of the indoor unit (cabinet, supply and return duct connections, access panels named but not opened, condensate drain pan and primary line, secondary/emergency drain pan and float switch if present, filter slot or return-air filter grille, thermostat)
- [ ] Names the function of each component in one sentence
- [ ] Distinguishes the suction line from the liquid line (suction: larger, insulated; liquid: smaller, bare copper)
- [ ] Locates the outdoor disconnect and names that it is the device used in hc-021 to de-energize the outdoor unit; demonstrates pointing without operating
- [ ] Names that access panels are NOT opened at this band; opening requires hc-021 and a qualified human present
- [ ] Names that service ports on the line set are NOT touched at this band; service-port work requires 608-certified person physically present
- [ ] Photographs each component or component area and submits to AI tutor with name and function written; AI tutor confirms each identification
- [ ] Names the difference between a split-system AC and a split-system heat pump in one sentence
- [ ] Names what is and is not in this band

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in hvac_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### hc-021: Use a digital multimeter with formal lockout-tagout to verify the absence of voltage at a residential AC condenser disconnect (gold-standard apprentice node; ELECTRICAL HAZARD)

- Node type: `technique`
- Progression band: `apprentice`
- Supervision required: `True`
- AI-mentor framing: AI tutor mentors procedure walkthrough on paper and artifact review; AI does NOT stand in for the qualified human at the live moment
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

**THIS NODE REQUIRES THE MOST RIGOROUS REVIEW IN THE BATCH.** Reviewer must hold (or co-review with someone who holds) electrical credentials current in residential service work and current NFPA 70E familiarity.

#### Hazards (confirm each is named correctly and at the right scale; check or correct)

- [ ] ELECTROCUTION RISK: residential 240V/60Hz/1-phase at outdoor unit; at residential fault current, contact across heart can stop it; the whole purpose of this competency is to verify dead before further work
- [ ] ARC FLASH: short between conductors during energized work releases arc that can cause severe burns and concussive injury; NFPA 70E governs boundaries and PPE; default in trade is de-energize and verify dead before opening
- [ ] WRONG-DISCONNECT FAILURE: mis-identified or mis-operated disconnect leaves wrong circuit dead and intended one live; unit cabinet may have TWO power sources (line and low-voltage control); line disconnect handles only line side; control side verified separately
- [ ] METER FAILURE: DMM with depleted battery, blown fuse, broken probe lead, or wrong CAT rating can read zero on live conductor; live-dead-live (test-dead-test) per NFPA 70E catches this; all three readings must agree
- [ ] STORED ENERGY IN CAPACITORS: dual-run capacitor stores charge that persists after disconnect open; this competency does NOT include opening cabinet and contacting capacitor; verification at disconnect (line side) only; capacitor discharge is separate, not in this batch
- [ ] BACKFEED FROM CONTROL CIRCUIT OR SHARED NEUTRAL: in some misinstalled or older systems, opening line disconnect does not fully de-energize cabinet; verification at work point is the safeguard
- [ ] WET CONDITIONS: rain, standing water, or wet outdoor pad significantly increases shock risk; defer to dry conditions or qualified human decides on additional PPE per NFPA 70E
- [ ] SHARP SHEET-METAL EDGES on disconnect cover and unit cabinet if cover removed

#### PPE required (confirm each item is correctly named and rated; check or correct)

- [ ] Trade PPE per hs-001
- [ ] Safety glasses (ANSI Z87.1) required throughout the procedure
- [ ] Insulating gloves rated for voltage actually being verified (residential 240V: class 00 or higher per NFPA 70E and glove manufacturer); inspected per manufacturer and OSHA before use; qualified human present confirms rating and inspection
- [ ] Long sleeves and clothing rated appropriately per NFPA 70E for arc-flash incident energy at the disconnect (qualified human confirms PPE selection)
- [ ] No metal jewelry on hands, wrists, or neck during the procedure
- [ ] Multimeter (DMM) with CAT III at minimum rated for 600V or higher (CAT IV acceptable); intact test leads; current battery; current calibration where required by program; CAT II or unrated meters are NOT acceptable per NFPA 70E
- [ ] Lockout-tagout hardware: padlock fitting the disconnect's lockout provision; danger tag legible per OSHA 1910.145; key kept exclusively by person performing work for duration of lockout

#### Supervision basis (confirm the qualified-human-physically-present rule and the AI-mentor limit)

- [ ] ELECTRICAL HAZARD: qualified human PHYSICALLY PRESENT at the live-dead-live verification; qualified means licensed HVAC technician OR licensed electrician with current experience in residential electrical work
- [ ] Qualified human watches meter reading, watches probe placement, watches lockout-tagout sequence, in position to intervene physically if learner makes a mistake
- [ ] AI tutor mentors procedure walkthrough on paper and reviews artifact evidence; does NOT stand in for qualified human at the live moment
- [ ] Households without resident qualified person arrange paid professional supervision session, vocational-school program day, apprentice arrangement, or defer competency
- [ ] AI tutor and supervising adult on premises do NOT substitute for the qualified electrical-scope human at the live moment

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable and correct; check or correct)

- [ ] Reviews the nameplate card from hc-001 BEFORE starting; names expected voltage; confirms multimeter range covers it
- [ ] Reviews the component identification card from hc-002 BEFORE starting; identifies correct disconnect for the unit
- [ ] Inspects multimeter and leads BEFORE the live test (battery indicator OK, leads visually intact, fuse intact); qualified human confirms by inspection
- [ ] FIRST live test on known live source (120V receptacle or proving unit); reads expected voltage; announces reading aloud; qualified human confirms
- [ ] Operates disconnect to open position (or removes pull-out) correctly per disconnect type
- [ ] Applies padlock to lockout provision and attaches signed and dated tag; keeps key exclusively with self; qualified human confirms lock properly engaged and tag legible per OSHA 1910.145
- [ ] DEAD test at work point covering every pair of conductors that should be dead (residential 240V/1-phase: L1-ground, L2-ground, L1-L2); announces each reading aloud; qualified human confirms each probe placement and reading
- [ ] SECOND live test on same known live source; reads expected voltage; announces reading aloud; qualified human confirms reading and signs off that dead test is valid
- [ ] Photographs locked disconnect with tag in place; submits photo to AI tutor with written narration of every procedure step as performed
- [ ] Names rule that lockout is released ONLY by person who applied it AND ONLY after work is complete; demonstrates release sequence at end of session under qualified human's supervision
- [ ] Names what would invalidate the dead reading and require restarting (meter fails second live test; tag or lock disturbed; procedure deviates from OSHA 1910.147; wrong disconnect identified mid-procedure; backfeed suspected)
- [ ] Names that this competency covers ONLY line-voltage verification at disconnect; low-voltage control circuit verified separately; capacitor discharged separately; refrigerant work separate under EPA 608; gas-system work separate

#### Standard references (confirm each is current and the household / employer has the required programs in place)

- [ ] OSHA 29 CFR 1910.147 (Lockout-Tagout)
- [ ] OSHA 29 CFR 1910.145 (Signs and Tags)
- [ ] OSHA 29 CFR 1910.137 (Electrical PPE)
- [ ] OSHA 29 CFR 1910.335 (Electrical Safety-Related Work Practices)
- [ ] NFPA 70E (current edition)
- [ ] NFPA 70 / NEC (current edition per local AHJ)
- [ ] IEC 61010-1 / UL 61010-1 (CAT II / III / IV Categories)
- [ ] Household's or employer's written equipment-specific LOTO procedure per OSHA 1910.147
- [ ] Manufacturer service literature for specific multimeter, insulating gloves, lockout hardware, HVAC equipment
- [ ] Qualified human's professional license (licensed HVAC tech with electrical scope OR licensed electrician) per local jurisdiction; continuing-education currency in NFPA 70E

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in hvac_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

## Author-flagged uncertainties (named at the time of authoring)

The author of these nodes named the following points as places where they leaned conservative but could not claim independent verification. Reviewer confirms or corrects each.

### U1. Refrigerant safety-class transitions (A1 to A2L; AIM Act and EPA SNAP)

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 names R-410A as the dominant A1 residential refrigerant through the 2020s and R-454B and R-32 as A2L refrigerants now replacing R-410A in new residential equipment under the AIM Act and EPA SNAP transitions. The node defers per-refrigerant rules to ASHRAE 34, the equipment nameplate's listed refrigerant, the manufacturer's service literature, and the refrigerant's SDS. Reviewer confirms this transition framing is correct as of the review date and the deferral to standards is appropriate.

  Reviewer's correction:

  ```

  ```

### U2. Lockout-tagout written procedure

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hc-021 defers the equipment-specific written LOTO procedure to the household's or employer's written program per OSHA 29 CFR 1910.147. The node specifies that if no written procedure exists, the qualified human present produces one before work begins. Reviewer confirms this deferral is correct and the written-procedure requirement under OSHA is honored.

  Reviewer's correction:

  ```

  ```

### U3. Specific operating voltages

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 and hc-021 name 240V/60Hz/1-phase as typical residential outdoor-unit supply and 120V/60Hz/1-phase as typical air-handler supply in the US, with 24VAC typical for residential and light-commercial control circuits; commercial systems 208V/3-phase or 480V/3-phase. All expected voltages are deferred to the nameplate per hc-001. Reviewer confirms the typical residential voltages are correctly stated and the deferral to nameplate is appropriate.

  Reviewer's correction:

  ```

  ```

### U4. SEER / HSPF / AFUE rating standard changes (SEER → SEER2 etc.)

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hc-001 names SEER, SEER2, EER, EER2, HSPF, HSPF2, and AFUE as distinct ratings with distinct test conditions; the node defers per-rating ranges to the nameplate as printed and to the AHRI standards. The 2023 transition from SEER to SEER2 is named. Reviewer confirms the rating-standard names and the transition framing are correct as of the review date.

  Reviewer's correction:

  ```

  ```

### U5. Asbestos in pre-1980 systems

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 names duct mastic, boiler insulation, pipe lagging, gasket material, and some furnace components manufactured before 1980 as asbestos-suspect; defers visual identification as unreliable; defers to EPA and state asbestos rules; treats pre-1980 components as suspect until tested by a qualified inspector. Reviewer confirms the pre-1980 cut-off is the appropriate suspect-threshold and the deferral to qualified inspection is correct.

  Reviewer's correction:

  ```

  ```

### U6. CO action levels and CO alarm placement

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 names CO alarm activation as a stop-work event and defers action levels and recognition to current CDC guidance; defers alarm placement to current NFPA 720 and the local AHJ. The node does NOT name action-level ppm. Reviewer confirms the deferrals are correct and no specific ppm should be written into the node.

  Reviewer's correction:

  ```

  ```

### U7. Multimeter Category rating (CAT III vs CAT IV)

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hc-021 specifies CAT III rated for 600V or higher as the minimum for residential 240V live-dead-live verification; CAT IV acceptable; CAT II or unrated meters NOT acceptable per NFPA 70E. Defers to IEC 61010-1 / UL 61010-1 for Category definitions and to the qualified human present for confirmation. Reviewer confirms the CAT III at 600V minimum is correct for this measurement and that the prohibition on CAT II / unrated meters matches current NFPA 70E.

  Reviewer's correction:

  ```

  ```

### U8. Arc-flash boundaries on residential disconnects

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hc-021 names arc-flash hazard on residential 240V equipment as smaller than commercial but real; defers boundary calculation to NFPA 70E and the qualified human present. The default in the trade is to de-energize and verify dead before opening, removing the arc-flash hazard at the work point. Reviewer confirms this framing is correct for residential and that any non-residential application would require explicit boundary calculation.

  Reviewer's correction:

  ```

  ```

### U9. Refrigerant burn risk on cold lines

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 names frostbite from direct skin contact with escaping refrigerant; the high-pressure flash can reach below-freezing temperatures on contact. The node defers PPE selection to ASHRAE 34 and the refrigerant's SDS. hc-002 names that the suction line under operation runs cold but is not below freezing under normal operation. Reviewer confirms the frostbite-on-flash framing is correct and the normal-operation temperature statement matches typical residential systems.

  Reviewer's correction:

  ```

  ```

### U10. Sheet-metal edge cut frequency in HVAC

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 names sheet-metal cuts as "among the most frequent HVAC injuries per industry observation" and makes cut-resistant gloves the default for any sheet-metal handling. The node does NOT cite specific industry injury frequencies (no verified statistical source). Reviewer confirms the framing is accurate to professional observation and the cut-resistant-gloves default is the appropriate response.

  Reviewer's correction:

  ```

  ```

### U11. CO alarm service life

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 names "typically 5 to 10 years per the manufacturer" as the CO sensor service-life range and defers the actual number to the manufacturer's label. The node does NOT prescribe a specific number. Reviewer confirms the 5-to-10-year range is a fair characterization of current CO alarm manufacturer specifications and that the deferral to the manufacturer label is correct.

  Reviewer's correction:

  ```

  ```

### U12. Cut-resistant glove level (ANSI/ISEA 105 cut level A4)

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hs-001 names "ANSI/ISEA 105 cut level A4 or higher recommended for general sheet-metal handling" and defers the actual cut level to the household or employer program per the actual work; the node names the cut-rated requirement without prescribing a specific level. Reviewer confirms A4 is an appropriate recommendation for general HVAC sheet-metal work and the deferral to household / employer judgment is correct.

  Reviewer's correction:

  ```

  ```

### U13. Insulating-glove class for 240V

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hc-021 specifies "class 00 or higher per NFPA 70E" for residential 240V verification, with the qualified human present confirming the rating and inspection. Reviewer confirms class 00 is the appropriate minimum for 240V residential and that the deferral to qualified human confirmation is correct.

  Reviewer's correction:

  ```

  ```

### U14. EPA Section 608 certification types (Type I, II, III, Universal)

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  hvac-root and hs-001 name EPA Section 608 certification (Type I, II, III, or Universal) as required for hands-on refrigerant work and defer to EPA for the appropriate certification per the refrigerant being handled. The node does NOT enumerate which type covers which equipment. Reviewer confirms the deferral to EPA and the framing of the four certification types is correct.

  Reviewer's correction:

  ```

  ```

---

## After this review

Once every node above is set to `safety_review.reviewed = True` in `hvac_content.py` (with `reviewer` and `reviewed_on` recorded), the HVAC trade's first authoring batch is cleared for surfacing through the integration gate. Until then, the gate (per the `requires_human_safety_review` helper) refuses every node where the helper returns True and `safety_review.reviewed` is False.

**For `hc-021` specifically**, the integration must additionally confirm at the time of each learner's attempt that a qualified human (licensed HVAC technician or licensed electrician) is physically present at the live-dead-live verification. The AI tutor does NOT stand in for the qualified human at the live moment. This is a runtime gate above the content review gate, and is the responsibility of the activity-surface integration layer (see the TODO in `backend/app/services/node_content.py::requires_human_safety_review`).

**Subsequent batches** for this trade will add (in priority order) low-hazard hands-on competencies (filter changes, condensate-trap cleaning), the apprentice-band knowledge work for psychrometrics and refrigerant theory, the journeyman-band electrical and refrigerant troubleshooting competencies (each behind its own safety gate), gas-system and combustion competencies (NFPA 54 gate), rooftop and confined-space competencies (OSHA 1926 Subpart M and 1910.146 gates), and the qualified-band project nodes (a complete service call, a complete startup, a complete installation). Each batch will go through the same checklist process before surfacing.
