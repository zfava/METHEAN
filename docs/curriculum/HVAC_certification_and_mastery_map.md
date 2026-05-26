# HVAC certification and mastery map

Generated from `backend/app/content/hvac_content.py` (the `hvac-root.mastery_ladder` block, the `hcert-*` certification_prep nodes, and the `certification_alignment` metadata on the existing competencies). Do not edit this document directly to change what the trade teaches; edit the content file and regenerate. This document renders what is authored.

This map covers the HVAC trade's path from intro to master technician, expressed as:

- a **mastery ladder** with four progression rungs (helper, apprentice, journeyman, qualified),
- a **certification spine** with four real, externally administered credentials (EPA Section 608, state licensing, NATE, OSHA Outreach),
- **alignment references** showing which existing competency builds toward which credential domain at which rung.

## Framing

Mastery in this trade is **demonstrated competence PLUS a real portfolio of work AND readiness for the relevant external credentials**. Portfolio and credential are complementary, not alternatives:

- A learner with a portfolio but no credential cannot legally do regulated work (EPA Section 608 is legally required for any hands-on refrigerant work; state HVAC license is legally required for many scopes in many jurisdictions).
- A learner with a credential but no portfolio is not yet competent; the credential attests to passing an exam, not to having done the work.

METHEAN builds the portfolio and prepares the understanding. The credentials are taken through their official bodies, never administered by METHEAN.

## Credentials are NOT substitutable for safety gates

Authored explicitly in `hvac-root.mastery_ladder.credentials_NOT_substitutable_for` and locked in by the test suite:

1. **EPA Section 608 certification does NOT substitute for the supervision policy on hands-on refrigerant work.** A 608-certified learner still performs first hands-on refrigerant operations under a working 608-certified mentor per the trade's apprenticeship pedagogy.
2. **State HVAC license does NOT substitute for the specific safety competencies** (e.g. hc-021 live-dead-live verification). License-holders still perform live-dead-live verification on every service call as the competency teaches, because the verification is the safety habit.
3. **NATE certifications do NOT substitute for EPA Section 608**, do NOT substitute for state licensing, and do NOT change any supervision rule.
4. **OSHA 10 / 30 Outreach completion does NOT substitute for site-specific or task-specific safety training** required by particular OSHA standards (LOTO, fall protection, confined-space entry); those remain the employer's responsibility under OSHA's specific-training requirements.

## The mastery ladder

The trade's four rungs, with their authored content and certification placements.

### Rung 1: helper (emerging)

**What the learner does**: Assists a working mentor. Reads nameplates and component layouts. Walks the shop's safety with an adult on premises. Does not yet open enclosures, touch live electrical, handle refrigerant, or open gas systems. Begins study toward OSHA 10 orientation.

**Mentor models in use**:
- AI tutor end-to-end (knowledge work)
- Adult on premises (safety walkthrough, low-hazard hands-on)

**Authored competencies at this rung**:
- `hs-001` Safety walkthrough (helper, supervision_required True, mentor signoff required)
- `hc-001` Read an equipment nameplate (helper, AI-mentored end-to-end)
- `hc-002` Visual component identification (helper, AI-mentored end-to-end)

**Certifications appropriate at this rung**:
- `hcert-osha` **OSHA 10-Hour Outreach (General Industry or Construction)** — common employer entry prerequisite; reinforces the safety vocabulary used in hs-001 and prepares the learner for the next bands. Delivered by OSHA-authorized Outreach Training Program trainers, not METHEAN.

**Portfolio artifacts built here**:
- Nameplate cards (one per piece of household HVAC equipment, per hc-001)
- Component identification cards (outdoor unit and indoor air handler, per hc-002)
- Recorded safety walkthrough video (per hs-001)

### Rung 2: apprentice (developing)

**What the learner does**: Performs most steps with a mentor checking key cuts, joints, connections, and (for higher-hazard subsystems) with a **qualified human physically present**. Begins live-dead-live verification at the disconnect (hc-021) under a licensed electrician or licensed HVAC technician. Earns EPA Section 608 (study-only) as a precondition for any later hands-on refrigerant work. Earns OSHA 30 if taking on lead responsibility. Begins entry-level NATE certifications.

**Mentor models in use**:
- AI tutor (knowledge work, certification study, procedure walkthrough, artifact review)
- Adult on premises (low-hazard hands-on)
- **Qualified human physically present** (electrical verification per hc-021, and any other hazardous-subsystem work as it enters the band)

**Authored competencies at this rung**:
- `hc-021` DMM + LOTO live-dead-live verification at residential disconnect (apprentice, gold-standard; **ELECTRICAL HAZARD**; supervision_required True; qualified human physically present at the live moment; AI does NOT stand in)

**Certifications appropriate at this rung**:
- `hcert-epa608` **EPA Section 608 (Type I, Type II, or Universal)** — study-only credential the learner can earn before any hands-on refrigerant work; it is the legal precondition for that work in the United States. Exam taken through an EPA-approved certifying body, not METHEAN.
- `hcert-osha` **OSHA 30-Hour Outreach** — when the learner takes on lead or supervisory work. Delivered by OSHA-authorized trainers.
- `hcert-nate` **NATE entry-level certifications** (Ready to Work, HVAC Support Technician) — industry-recognized acknowledgment of basic readiness. Exam through NATE-approved testing partners.

**Portfolio artifacts built here**:
- Live-dead-live verification photographs and written narration with qualified-human countersignature (per hc-021)
- EPA Section 608 certification card (held by the learner; obtained from an EPA-approved certifying body)
- OSHA Outreach completion card if taken at this band

### Rung 3: journeyman (proficient)

**What the learner does**: Completes a competency independently to acceptable quality. Mentor available but not required step by step. For higher-hazard subsystems, the learner now holds the credentials that authorize the hands-on work (EPA 608 for refrigerant; state journeyman license per the AHJ for HVAC scope where licensing is required), and the qualified-human-present rule from the apprentice band shifts to the experienced-journeyman-available rule for routine live electrical work. The learner is now ready to sit the AHJ's journeyman exam (if not already taken at the close of the apprentice band) and to pursue NATE core / specialty certifications in their chosen subsystems.

**Mentor models in use**:
- AI tutor (continuing-education study, certification preparation, code lookup, artifact review)
- Working mentor available but not required step by step (for routine work)
- Qualified human present (for unusual hazards, first time on a new equipment family, or any work outside the learner's licensed scope)

**Authored competencies at this rung**: None yet in the current batch. Future batches will add: diagnostic frameworks, load calculations (Manual J), equipment selection (Manual S), duct design (Manual D), commercial controls, combustion analysis (knowledge level), complete maintenance and service calls.

**Certifications appropriate at this rung**:
- `hcert-licensing` **State journeyman HVAC license per the AHJ** — earned after completing the AHJ's apprenticeship hours requirement through a recognized apprenticeship and passing the AHJ's journeyman exam. The learner is now legally authorized to perform HVAC work within the scope the license names. Apprenticeship hours come from a state-approved program, not from METHEAN.
- `hcert-nate` **NATE Core plus one or more specialty certifications** (air conditioning, gas heating, heat pumps, light commercial refrigeration, etc.) — industry-recognized acknowledgment of competence in a chosen subsystem.

**Portfolio artifacts built here**:
- Complete service-call write-ups across the chosen specialty
- State journeyman HVAC license (obtained from the AHJ)
- NATE core and specialty certification cards (obtained from NATE)

### Rung 4: qualified (mastered)

**What the learner does**: Performs reliably under varied conditions across the chosen subsystems. Teaches helpers and apprentices through the helper-band steps of those subsystems. Holds the AHJ's master / contractor license where applicable, with the bonding, insurance, and continuing-education the AHJ requires. Pursues NATE senior-level certification where it advances the learner's chosen specialty. Maintains EPA 608 (no renewal currently required by EPA but the card is kept on the person for refrigerant work) and NFPA 70E currency. **Carries the qualified-human-present role for the next generation of learners.**

**Mentor models in use**:
- AI tutor (continuing-education, code-update tracking, master exam preparation, artifact review)
- Peer review (other masters / contractors)
- **Learner now MENTORS others** as the qualified human present for their hazardous-subsystem work

**Authored competencies at this rung**: None yet in the current batch. Future batches will add: advanced controls and building automation, commercial design, load and energy modeling, project management, business and contract law (master / contractor level), full design-and-install of a residential system, complete residential and light-commercial install, commercial refrigeration service, full combustion startup and tuning.

**Certifications appropriate at this rung**:
- `hcert-licensing` **State master / contractor HVAC license per the AHJ** — earned after the journeyman experience requirement the AHJ publishes, plus business / law exam in many states, plus bonding and insurance per the AHJ.
- `hcert-nate` **NATE Senior Efficiency Analyst (or other current NATE senior-level certifications)** per the chosen specialty — top-tier industry recognition.

**Portfolio artifacts built here**:
- State master / contractor HVAC license (obtained from the AHJ)
- NATE senior-level certification (obtained from NATE)
- A full project portfolio (residential install, commercial service, training-of-apprentice records)
- Continuing-education currency in NFPA 70E and the local AHJ's continuing-education requirements

### Mastery marker

The learner is qualified when:

1. Every authored competency in the chosen specialty has been demonstrated at the proficient or mastered band with portfolio artifacts;
2. The legally required credentials for the work the learner intends to do are held (EPA 608 for any refrigerant work; state journeyman or master license per the AHJ for the work the AHJ regulates);
3. The learner has either signed off a helper-band attempt for another learner OR completed a journeyman-band project entirely unsupervised, per the trades design's qualified-band signoff rule.

## The certification spine

### EPA Section 608 Technician Certification (`hcert-epa608`)

- **Credential body**: U.S. Environmental Protection Agency (EPA).
- **Legal status**: **legally required** under Section 608 of the Clean Air Act and 40 CFR Part 82 Subpart F.
- **Authorizing scope**: legal precondition in the United States to purchase regulated refrigerants in quantity and to handle refrigerant in any way that could release it to the atmosphere. Four types: Type I (small appliances), Type II (high- or very-high-pressure appliances; covers most residential and commercial split-system AC and heat-pump equipment), Type III (low-pressure chillers), Universal (all three).
- **Knowledge domains**: Core (regulations, ozone, recovery and recycling concepts, refrigerant safety, identification, leak-detection, record-keeping, venting prohibition); Type-specific domains as authored in `hcert-epa608.knowledge_domains_covered`.
- **Exam taken through**: an EPA-approved certifying body (the EPA Section 608 program page lists current approvals; historical examples include ESCO Institute, RSES, Mainstream Engineering, and others).
- **METHEAN's role**: AI tutor mentors end-to-end study; METHEAN does NOT administer or proctor the exam; no reproduced exam content.
- **Ladder placement**: late helper to early apprentice — study-only credential earned BEFORE any hands-on refrigerant work, because the certification is legally required for that work.
- **Aligned existing competencies**: hs-001 (refrigerant safety practices, A1/A2L/A3 classification, venting prohibition); hc-001 (refrigerant type and factory charge on the nameplate); hc-002 (service-port identification and the rule against opening them without 608).

### State HVAC apprenticeship and journeyman / master licensing path (`hcert-licensing`)

- **Credential body**: the Authority Having Jurisdiction (AHJ) for HVAC licensing in the learner's state, county, or municipality. No single federal HVAC license; learner identifies their AHJ.
- **Legal status**: **jurisdiction-specific** — required in many states; learner confirms with their AHJ.
- **Authorizing scope**: HVAC work as an employee (apprentice / journeyman) or as a contractor (master / contractor license) within the scope and geographic jurisdiction the license names.
- **Knowledge domains**: NEC (NFPA 70); NFPA 54 (National Fuel Gas Code); IMC or UMC per AHJ adoption; AHJ's local amendments; refrigeration theory; load calculations (Manual J); duct design (Manual D); equipment selection (Manual S); controls; combustion fundamentals; HVAC safety practices including NFPA 70E. Business and contract knowledge at the master / contractor level.
- **Exam taken through**: the AHJ or its authorized testing partner (commonly Prov Inc., PSI, or another state-approved testing service).
- **Supervised hours through**: a state-approved apprenticeship program or recognized employer-based apprenticeship. **METHEAN's practice sessions and portfolio work are NOT a substitute for registered apprenticeship hours.** The household confirms with the AHJ which programs are recognized for hours-credit.
- **METHEAN's role**: AI tutor mentors conceptual study end-to-end; the portfolio of demonstrated work is presented as supporting evidence; the AHJ's recognized hours come from a state-approved apprenticeship program; the exam is taken through the AHJ.
- **Ladder placement**: journeyman exam at the late apprentice to early journeyman band; master / contractor exam at the qualified band.
- **Aligned existing competencies**: hs-001 (general HVAC safety, NFPA 70E intro, OSHA familiarity, AHJ code awareness); hc-001 (MCA / MOP for circuit sizing per NEC, capacity for load matching per ACCA Manual S, efficiency ratings for energy-code compliance); hc-002 (split-system architecture, disconnect identification per NEC, IMC secondary-drain-pan requirements); hc-021 (NFPA 70E live-dead-live, NEC Article 440, multimeter Category Ratings per IEC/UL 61010-1).

### NATE (North American Technician Excellence) certifications (`hcert-nate`)

- **Credential body**: North American Technician Excellence (NATE), `https://natex.org`.
- **Legal status**: **optional** — industry-recognized, voluntary technician-certification program.
- **Authorizing scope**: NATE does NOT legally authorize work that a state license does not; NATE is NOT a substitute for state HVAC licensing where licensing is required, and NOT a substitute for EPA Section 608. NATE attests to demonstrated knowledge in a specific specialty area.
- **Knowledge domains**: per specialty's Knowledge Areas of Technician Expertise (KATE) published by NATE.
- **Exam taken through**: NATE-approved testing partners.
- **METHEAN's role**: AI tutor mentors end-to-end study; METHEAN does NOT administer the exam.
- **Ladder placement**: entry-level (Ready to Work, HVAC Support Technician) at late helper to apprentice; core / specialty at late apprentice to journeyman; senior-level at qualified.
- **Aligned existing competencies**: hs-001 (safety domain in every NATE specialty's KATE); hc-001 (nameplate fluency expected by every specialty); hc-002 (system architecture per AC / Heat Pump / Air Distribution KATEs); hc-021 (electrical-safety domain across all specialties).

### OSHA 10-Hour and 30-Hour Outreach Training (`hcert-osha`)

- **Credential body**: U.S. Occupational Safety and Health Administration (OSHA), through OSHA-authorized Outreach Training Program trainers.
- **Legal status**: **optional** — voluntary worker-orientation training programs. **NOT a license or certification in the legal sense**; does NOT authorize specific work; NOT a substitute for site-specific or task-specific OSHA-required training (LOTO, fall protection, confined-space entry, etc.). Many HVAC employers and apprenticeship sponsors require OSHA 10 for new technicians and OSHA 30 for supervisors.
- **Knowledge domains**: introduction to OSHA, general safety and health, recognition of common workplace hazards, PPE, basic OSHA 1910 (general industry) or OSHA 1926 (construction) introduction. The 30-hour version goes deeper with elective topics.
- **Exam taken through**: this is training, not an exam. Completion is attendance and in-course assessment per the authorized trainer. OSHA-issued Department of Labor completion cards are issued by the authorized trainer.
- **METHEAN's role**: AI tutor reinforces overlapping topics with hs-001 and hc-021; **METHEAN does NOT deliver the 10-Hour or 30-Hour course and does not issue the completion cards** (only OSHA-authorized trainers may).
- **Ladder placement**: OSHA 10 at helper to early apprentice; OSHA 30 at apprentice to journeyman.
- **Aligned existing competencies**: hs-001 (every domain of OSHA orientation); hc-021 (lockout-tagout per OSHA 1910.147; electrical safety practices per 1910.137 and 1910.335).

## Alignment matrix (existing competencies × certifications)

| Competency | EPA 608 | Licensing | NATE | OSHA 10/30 |
|---|---|---|---|---|
| `hs-001` Safety walkthrough | Core: refrigerant safety, A1/A2L/A3, venting prohibition | General HVAC safety, NFPA 70E intro, AHJ code awareness | Safety domain across every specialty's KATE | Every domain of OSHA orientation |
| `hc-001` Read nameplate | Core: refrigerant identification | MCA / MOP / capacity / efficiency for NEC, Manual S, energy code | Nameplate fluency across specialties | – |
| `hc-002` Visual component ID | Core: service-port awareness; Type II/III architecture | Split-system architecture, NEC disconnect, IMC drain pan | System architecture across AC / Heat Pump / Air Distribution KATEs | – |
| `hc-021` DMM + LOTO live-dead-live | Core: de-energization as precondition to refrigerant work | NFPA 70E live-dead-live; NEC Article 440; meter Category Ratings | Electrical-safety domain across every specialty | LOTO per 1910.147; electrical safety per 1910.137 and 1910.335 |

## Honesty and legal flags

1. **EPA Section 608 is a federal legal requirement** for hands-on refrigerant work in the United States, enforced by the EPA under Section 608 of the Clean Air Act and 40 CFR Part 82 Subpart F. Any future refrigerant-handling competency in this trade must require EPA Section 608 certification before the learner performs the work hands-on, with or without a mentor. Counsel review is appropriate before this content reaches learners, because the consequences of mis-stating the legal requirement are real (an unauthorized learner could face EPA enforcement; a household could face civil penalties).
2. **State HVAC licensing is state-regulated and varies widely**, including no-statewide-license states where municipal or county licensing may apply. The household identifies their AHJ. Any future competency that touches scope-limited work (gas piping, residential vs commercial, mechanical contracting) must include a clear gate on the learner's or supervising professional's licensure for the work being done. Counsel review is appropriate before the content reaches learners, because licensing rules change and misrepresentation can have legal consequences.
3. **No reproduced exam content** is in any certification_prep node. The validator enforces this by rejecting any field whose name suggests reproduced exam material (`exam_questions`, `exam_content`, `sample_questions`, `practice_exam_questions`, `exam_answer_key`, `reproduced_exam`). The reviewer confirms this when reviewing the nodes.
4. **Certification framing never lowers a supervision requirement.** The `hc-021` qualified-human-physically-present rule is locked in by tests and by the alignment metadata's `supervision_rung: qualified_human_physically_present` field; no credential held by the learner relaxes it. The `credentials_NOT_substitutable_for` clauses in the mastery ladder make this explicit.
5. **Review by a qualified HVAC professional and counsel is required before this content reaches learners.** Recommended profile: a licensed HVAC technician with current field experience (state license or journeyman / master credential per the local AHJ) for the technical claims; a licensed electrician (or HVAC technician with electrical scope) for the `hc-021` electrical content; counsel familiar with EPA Section 608 enforcement and state licensing rules for the legal claims; and a safety professional familiar with OSHA general-industry standards for the OSHA Outreach framing. None of the nodes' `safety_review.reviewed` fields are set to True; surfacing is blocked at the integration gate until they are.

## What is NOT in this map

Out of scope of this retrofit (will be added in later batches):

- The hands-on refrigerant competencies (gauge connection, recovery, recycling, charging, leak repair). Each requires EPA Section 608 certification (held by both the learner once earned AND the supervising mentor) and is its own safety gate.
- The brazing and silver-soldering competency. Fire watch, ventilation, regulator setup, hot-work gate.
- The gas-system competencies (NFPA 54). Gas-fitter licensing per AHJ.
- The combustion-startup-and-tuning competency. Calibrated combustion analyzer, manufacturer startup procedure.
- The rooftop competencies. OSHA 1926 Subpart M fall-protection gate.
- The confined-space competencies. OSHA 1910.146 permit-required confined-space gate.
- The capacitor-discharge competency. Its own safety gate.
- The electrical-panel-work competencies. NEC and licensed-electrician scope.
- Project nodes (a complete service call, a complete startup, a complete install). These follow once the prerequisite competencies are authored.

Each future batch will follow the same authoring discipline: safety competency first, helper competencies bottom-up, gold-standard apprentice / journeyman competencies, then projects. Each will get its own update to this map.
