# Electrical certification and mastery map

Generated from `backend/app/content/electrical_content.py` (the `el-root.mastery_ladder` block, the `elcert-*` certification_prep nodes, and the `certification_alignment` metadata on each competency). Do not edit this document directly to change what the trade teaches; edit the content file and regenerate.

This map covers the electrical trade's path from intro to master electrician, expressed as:

- a **mastery ladder** with four progression rungs (helper, apprentice, journeyman, qualified),
- a **certification spine** with three real, externally administered credential paths (NFPA standards, state licensing, OSHA / NFPA 70E adjacent training),
- **alignment references** showing which existing competency builds toward which credential domain at which rung.

## Framing

Mastery in this trade is **demonstrated competence PLUS a real portfolio of work AND readiness for the relevant external credentials**. Portfolio and credential are complementary, not alternatives:

- A learner with a portfolio but no credential cannot legally perform regulated electrical work in most jurisdictions (state licensing governs).
- A learner with a credential but no portfolio is not yet competent.

METHEAN builds the portfolio and prepares the understanding. The credentials are taken through their official bodies, never administered by METHEAN. Hands-on apprenticeship hours are logged through state-approved apprenticeship programs (the electrical training ALLIANCE for IBEW / NECA, state non-union programs, or recognized employer-based pathways), NOT through METHEAN.

## Credentials are NOT substitutable for safety gates

Authored explicitly in `el-root.mastery_ladder.credentials_NOT_substitutable_for` and locked in by the test suite:

1. **Knowledge of the NEC (NFPA 70) and NFPA 70E does NOT substitute for any supervision rule.** A learner with deep code knowledge still performs live-dead-live verification on every energized job per elc-021, because the verification is the safety habit, not a credential gate.
2. **A state apprentice / journeyman / master electrician license does NOT substitute for any specific safety competency.** License-holders still perform live-dead-live verification on every service call as elc-021 teaches, every time, regardless of how many years they have been licensed.
3. **OSHA 10 / 30 Outreach completion does NOT substitute for site-specific or task-specific safety training** required by particular OSHA standards (LOTO per 1910.147, fall protection per 1926 Subpart M, confined-space entry per 1910.146).
4. **NFPA 70E electrical-safe-work-practices training does NOT substitute for the supervision policy or for any safety competency authored in this trade.** NFPA 70E defines the safe-work-practices the trade follows; training does not authorize a learner to bypass the supervision tier required for the work.

## The four-tier supervision policy (authored on el-root)

1. **Tier 1 — Knowledge work**: AI tutor mentors end-to-end. Code interpretation, component identification, circuit theory, load calculation, service anatomy, grounding/bonding theory, procedure walkthroughs, troubleshooting trees, artifact review. No human required.
2. **Tier 2 — Low-hazard hands-on, de-energized and verified-dead ONLY**: adult on premises (parent counts; no electrical credentials needed for this tier). NO competencies of this tier are authored in this first batch; they enter in future batches.
3. **Tier 3 — Energized or near-energized work, OR any work where re-energization or backfeed is possible**: **LICENSED ELECTRICIAN physically present at the work**. The AI tutor mentors the procedure walkthrough and reviews artifacts, but does NOT stand in for the licensed human at the energized moment. `elc-021` is the canonical competency at this tier.
4. **Tier 4 — Regulated / credentialed milestones**: deferred to NFPA, OSHA, and the state AHJ. METHEAN does not administer.

## The mastery ladder

### Rung 1: helper (emerging)

**What the learner does**: Builds the conceptual foundation an elite apprentice masters before any energized work. Reads nameplates, identifies components from diagrams, learns Ohm's law and basic circuit theory, series and parallel circuits with load calculation, reads wiring diagrams and schematics, learns the anatomy of a residential electrical service, learns conductor sizing and ampacity basics by reference to the AHJ-adopted NEC, learns grounding and bonding theory, and learns meter and tool literacy including the meaning of multimeter CAT ratings. Walks the actual household service and tool kit with an adult on premises. Begins study toward OSHA 10 orientation.

**Mentor models**: AI tutor end-to-end (knowledge work); adult on premises (safety walkthrough).

**Competencies at this rung**: `hs-001`-equivalent (els-001), `elc-001`, `elc-002`, `elc-003`, `elc-004`, `elc-005`, `elc-006`, `elc-007`, `elc-008`, `elc-009`.

**Certifications appropriate here**:

- `elcert-safety`: **OSHA 10-Hour Outreach (General Industry or Construction)** — common employer entry prerequisite; reinforces the safety vocabulary used in els-001 and prepares for the apprentice band.

**Portfolio artifacts built here**:

- Nameplate cards across the household's actual equipment (per elc-001)
- Annotated diagrams and component ID sheets (per elc-002, elc-005)
- Worked Ohm's law / circuit calculations (per elc-003, elc-004, elc-007)
- Annotated diagram of the household's residential service (per elc-006)
- Worked grounding-and-bonding diagrams (per elc-008)
- Meter-and-tool card with CAT rating documented (per elc-009)
- Recorded safety walkthrough video (per els-001)

### Rung 2: apprentice (developing)

**What the learner does**: Performs the apprentice-band gold standard — de-energize a residential branch circuit at the panel, apply formal LOTO per OSHA 29 CFR 1910.147, perform live-dead-live verification per NFPA 70E, all with a **LICENSED ELECTRICIAN physically present** at the live moment. Begins intensive NEC and NFPA 70E study toward the journeyman exam. Earns OSHA 30 if taking lead responsibility. Begins logged apprenticeship hours through a state-approved apprenticeship program (NOT through METHEAN).

**Mentor models**: AI tutor (knowledge, certification study, procedure walkthrough, artifact review); adult on premises (low-hazard tier-2 hands-on); LICENSED ELECTRICIAN physically present (every tier-3 energized act).

**Competencies at this rung**: `elc-021` (de-energize / LOTO / live-dead-live verification on a residential branch; **ELECTRICAL HAZARD**; supervision_required True; AI does NOT stand in at the live moment).

**Certifications appropriate here**:

- `elcert-safety`: **OSHA 30-Hour Outreach** when taking lead responsibility.
- `elcert-nec`: **Working familiarity with NEC and NFPA 70E** — study-only; codes obtained through NFPA; AHJ-adopted edition governs.

**Portfolio artifacts built here**:

- Live-dead-live verification photographs and written narration with licensed-electrician countersignature (per elc-021)
- OSHA Outreach completion card if taken at this band
- Logged hours toward state apprenticeship requirement, recorded by the state-approved apprenticeship program (NOT by METHEAN)

### Rung 3: journeyman (proficient)

**What the learner does**: Completes a competency independently to acceptable quality for tier-1 and tier-2 work. For tier-3 energized work, the supervision rule stays in place: a LICENSED ELECTRICIAN is physically present at every live-dead-live verification per elc-021, because the verification is the safety habit, not a credential gate. The learner holds the state journeyman license per the AHJ (where licensing is required) and is legally authorized to perform electrical work within the scope the license names. Pursues specialty study (low-voltage / limited-energy, fire alarm, communications, residential generator / solar interconnection).

**Mentor models**: AI tutor (continuing education, code-update tracking); working mentor available not required step-by-step; licensed electrician physically present for every tier-3 act.

**Competencies at this rung**: future batches will add advanced diagnostic frameworks, commercial NEC topics, arc-flash on commercial 480V, controls, fire-alarm and communication systems, service-entrance and panel work, generator and solar PV interconnection, conduit and cable installation, full energized troubleshooting.

**Certifications appropriate here**:

- `elcert-licensing`: **State journeyman electrician license per the AHJ** — earned after the AHJ's apprenticeship hours requirement and the journeyman exam. In low-voltage-specific states, the **low-voltage / limited-energy journeyman license** per the AHJ.

**Portfolio artifacts built here**:

- Complete service-call write-ups across the chosen specialty
- State journeyman electrician license (obtained from the AHJ)
- Logged journeyman experience hours toward master eligibility

### Rung 4: qualified (mastered)

**What the learner does**: Performs reliably under varied conditions across the chosen specialty. Teaches helpers and apprentices through the helper-band steps. Holds the AHJ's master / contractor license where applicable, with bonding, insurance, and continuing education. Maintains NFPA 70E currency. **Carries the licensed-electrician-physically-present role for the next generation of learners performing tier-3 work.**

**Mentor models**: AI tutor (continuing education, master exam preparation); peer review; learner now MENTORS others as the licensed electrician physically present for their tier-3 work.

**Competencies at this rung**: future batches will add commercial design, lighting / energy modeling, project management, business and contract law, full design-and-install, full energized troubleshooting.

**Certifications appropriate here**:

- `elcert-licensing`: **State master electrician license per the AHJ** (or master limited-energy where applicable); **contractor licensing** additionally per the AHJ's contractor rules.

**Portfolio artifacts built here**:

- State master electrician license (obtained from the AHJ)
- Contractor license and bonding / insurance documentation where applicable
- Full project portfolio (residential install, low-voltage system install, training-of-apprentice records)
- Continuing-education currency in NFPA 70E and the AHJ's continuing-education requirements

### Mastery marker

The learner is qualified when:

1. Every authored competency in the chosen residential or low-voltage specialty has been demonstrated at the proficient or mastered band with portfolio artifacts;
2. The legally required credentials for the work the learner intends to do are held (state journeyman or master license per the AHJ);
3. The learner has either signed off a helper-band attempt for another learner OR completed a journeyman-band project entirely unsupervised at tier-1 and tier-2, with every tier-3 energized step still performed under licensed-electrician-present (energized work is NEVER unsupervised below the qualified band, and even at the qualified band, the licensed-electrician-physically-present rule applies on every elc-021 act as the safety habit).

## The certification spine

### `elcert-nec`: Working familiarity with the NEC (NFPA 70) and NFPA 70E

- **Credential body**: National Fire Protection Association (NFPA), `https://www.nfpa.org`.
- **Legal status**: jurisdiction_specific (AHJ adopts editions, sometimes with amendments).
- **Authorizing scope**: The NEC and NFPA 70E are standards, not credentials in the legal sense. Familiarity with them is the foundation of every state electrical license and every employer-required safety program.
- **Knowledge domains**: NEC structure (Articles 100, 200-285 wiring and protection, 300-398 wiring methods, 400-490 equipment, residential-focus Articles 210, 220, 230, 240, 250, 310, 314, 330/334, 404, 406, 408, 410, 422, 430, 440, 460, 690, 702); NFPA 70E structure (Articles 110 general practices, 120 LOTO, 130 working on or near live parts, arc-flash). No code text reproduced.
- **Exam taken through**: NFPA-approved training providers for code-update seminars and continuing-education credit; the AHJ for the journeyman exam where code familiarity is tested. METHEAN does not administer.
- **METHEAN's role**: AI tutor mentors end-to-end study against the AHJ-adopted edition; METHEAN does not issue completion certificates.
- **Ladder placement**: apprentice band intensifying through journeyman.

### `elcert-licensing`: State electrician licensing path

- **Credential body**: The Authority Having Jurisdiction (AHJ) for electrical licensing in the learner's state, county, or municipality. No single federal electrician license.
- **Legal status**: **jurisdiction_specific**, required in many states.
- **Authorizing scope**: Authorizes the holder to perform electrical work as apprentice, journeyman, or master/contractor within the scope and jurisdiction the license names. General electrical (residential and commercial); residential-only in some states; **low-voltage / limited-energy** as a distinct license in many states (data, fire alarm, security, audio/video, communications).
- **Knowledge domains**: NEC at AHJ-adopted depth; AHJ local amendments; conductor sizing and ampacity (Article 310 + correction factors); overcurrent (Article 240); grounding and bonding (Article 250); branch and feeder calculations (Articles 215, 220); residential wiring methods (Articles 330, 334); detailed application of Articles 210, 240, 250, 310, 314, 406, 408, 410, 422, 430, 440, 690, 702; NFPA 70E safe work practices. Master/contractor adds business and contract law per AHJ. Low-voltage adds NEC Articles 725, 760, 770, 800.
- **Eligibility (commonly, varies by AHJ)**: ~8,000 hours / 4 years for journeyman; additional years for master; insurance and bonding for contractor.
- **Exam taken through**: AHJ or authorized testing partner (PSI, Prov Inc., etc.). METHEAN does not administer.
- **Supervised hours through**: state-approved apprenticeship program — the electrical training ALLIANCE (IBEW / NECA), state non-union sponsors, or AHJ-recognized employer-based apprenticeship. **METHEAN's practice sessions and portfolio work are NOT a substitute for registered apprenticeship hours.**
- **METHEAN's role**: AI tutor mentors conceptual study end-to-end; portfolio of demonstrated work (including elc-021 narrations) presented as supporting evidence; AHJ's recognized hours come from the state-approved apprenticeship program.
- **Ladder placement**: journeyman exam at late apprentice / early journeyman; master / contractor at qualified.

### `elcert-safety`: OSHA 10 / 30 Outreach + NFPA 70E training (adjacent credentials)

- **Credential body**: OSHA-authorized Outreach Training Program trainers (for OSHA 10 / 30); NFPA-approved or employer-program / electrical training ALLIANCE / recognized independent providers (for NFPA 70E training). METHEAN does not deliver.
- **Legal status**: **optional**. The OSHA Outreach courses are voluntary worker-orientation training programs; they are NOT licenses in the legal sense and NOT a substitute for site-specific or task-specific OSHA-required training. NFPA 70E is a standard; training in it is recognized by employers and the trade widely.
- **Knowledge domains**: OSHA 10 / 30 — introduction to OSHA, common workplace hazards, PPE, basic 1910 or 1926 introduction. NFPA 70E — live-dead-live per Article 130, arc-flash boundaries and PPE per Article 130 and Annex C, LOTO per Article 120, insulating PPE and tools per Article 130 and Annex H, energized-work permit per Article 130.
- **Exam taken through**: OSHA-authorized Outreach trainers (OSHA-issued DOL completion cards); NFPA-approved or employer / electrical training ALLIANCE / recognized independent providers for NFPA 70E. METHEAN does not deliver.
- **METHEAN's role**: AI tutor mentors conceptual orientation overlapping with els-001, elc-009, elc-021.
- **Ladder placement**: OSHA 10 and entry-level NFPA 70E at helper / early apprentice; OSHA 30 and deeper NFPA 70E at apprentice / journeyman.

## Alignment matrix (existing competencies × certifications)

| Competency | NEC / NFPA 70E (elcert-nec) | Licensing (elcert-licensing) | OSHA / NFPA 70E training (elcert-safety) |
|---|---|---|---|
| `els-001` Safety walkthrough | NEC Article 100, 250 introductory; NFPA 70E general practices | General HVAC safety, NFPA 70E intro, AHJ code awareness | Every domain of OSHA orientation |
| `elc-001` Read nameplate | AIC per AHJ; voltage / current for Article 220 load calc; listing per NEC | Nameplate literacy across state licensing exam scope | — |
| `elc-002` Component ID | One-line basis for NEC Chapter 2; service-vs-subpanel bond rules; GFCI / AFCI locations | Component ID across state licensing scope | — |
| `elc-003` Ohm's law | Foundation for Article 220 load calculation and Article 310 ampacity | Ohm's law at journeyman depth | — |
| `elc-004` Series, parallel, load calc | Article 220 load calculations; 80% continuous-load rule; branch sizing | Circuit theory at journeyman depth | — |
| `elc-005` Wiring diagrams | Diagram interpretation; MWBC shared-neutral; GFCI / AFCI per AHJ | Diagram fluency across state licensing scope | — |
| `elc-006` Residential service anatomy | Articles 100, 230, 250, 240, 408 service-equipment topics | Service anatomy across state licensing scope | — |
| `elc-007` Conductor sizing and ampacity | Article 310 ampacity, Article 240 overcurrent, 110.14(C) termination-temperature rule | Conductor sizing across state licensing scope | — |
| `elc-008` Grounding and bonding theory | Article 250 (every part); fault-clearing path concept | Grounding and bonding at journeyman and master depth | — |
| `elc-009` Meter and tool literacy (CAT) | Test instrument requirements via NFPA 70E referenced by NEC safe-work context | Meter and tool literacy at journeyman depth | NFPA 70E meter selection; insulated tool selection; glove inspection; OSHA 1910.137 |
| `elc-021` LOTO live-dead-live | NEC service-equipment ID; NEC working space at panels; EGC and bonding role | NFPA 70E live-dead-live and PPE at journeyman / master depth; AHJ code application | LOTO per OSHA 1910.147; electrical safety per 1910.137 / 1910.335; NFPA 70E live-dead-live and PPE; arc-rated clothing |

## Honesty and legal flags

1. **State electrician licensing is jurisdiction-specific.** Licensing rules change. Any future competency that touches scope-limited work (high voltage, three-phase, service entrance, gas-related electrical, photovoltaic interconnection) must include clear gates on the learner's or supervising professional's licensure. **Counsel review is appropriate before this content reaches learners**, because the consequences of mis-stating a licensing rule are real (an unauthorized learner could face AHJ enforcement; a household could face civil penalties).
2. **No reproduced code or exam content** is in any node. The validator enforces this by rejecting any field whose name suggests reproduced exam material (`exam_questions`, `exam_content`, `sample_questions`, `practice_exam_questions`, `exam_answer_key`, `reproduced_exam`). The reviewer confirms this on every node.
3. **Certification framing never lowers a supervision requirement.** The `elc-021` licensed-electrician-physically-present rule is locked in by tests and by the alignment metadata's `supervision_rung: licensed_electrician_physically_present` field; no credential held by the learner relaxes it. The `credentials_NOT_substitutable_for` clauses in the mastery ladder make this explicit.
4. **Review by a licensed electrician AND counsel is required before this content reaches learners.** Recommended profile:
   - A licensed electrician with current field experience (state license per the local AHJ) for the technical claims.
   - For `elc-021` specifically: a licensed electrician current in NFPA 70E AND a safety professional familiar with OSHA 1910.147.
   - **Counsel familiar with state electrical licensing rules** for the `elcert-licensing` claims.

## What is NOT in this map (deferred for future batches behind their own safety gates)

- All energized service-entrance work (line side of the main disconnect). Service work is regulated more strictly than branch-circuit work and is out of scope at the foundation.
- All termination of conductors (wire stripping, lugging, splicing). De-energized tier-2 competencies after live-dead-live verification.
- Receptacle, switch, fixture, and breaker replacement on a verified-dead circuit (de-energized tier-2 work in future batches).
- GFCI / AFCI device installation and testing.
- Conduit bending, cable pulling, junction-box installation.
- Generator, transfer switch, and solar PV interconnection work.
- Three-phase, commercial, industrial, and any voltage above 600V.
- Capacitor discharge.
- Permits and inspections (deferred until install / service competencies authored).
- Project nodes (a complete branch addition, a complete service install, a low-voltage system install). These follow once the prerequisite competencies are authored.

Each future batch follows the same authoring discipline: safety competency review first, helper competencies bottom-up, gold-standard apprentice / journeyman competencies, then projects. Each gets its own update to this map.
