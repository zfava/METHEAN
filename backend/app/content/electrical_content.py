"""Residential and low-voltage electrical trade content (mastery path).

Mirrors the conventions established in hvac_content.py. The trade root
(el-root) carries the four-tier supervision policy, the mastery ladder,
and the credentials-NOT-substitutable-for lock. Safety is gating:
els-001 is a prerequisite of every hands-on electrical competency.
elc-021 (de-energize, lock out / tag out, perform live-dead-live
verification on a residential circuit) is the apprentice-band
gold-standard exemplar; ELECTRICAL HAZARD; supervision_required True;
mentor_signoff_required True; safety_review.reviewed False;
licensed-electrician-physically-present at the live moment is the one
hard line in the trade's supervision policy.

Hazard posture: HIGHEST hazard authored to date in this product.
Electrical is line-voltage lethal. Every node carries
safety_review.reviewed False by default. Clearance requires a
licensed electrician for the technical and elc-021 content, and
counsel familiar with state electrical-licensing regulations for the
certification claims. No node is cleared by authoring.

Mentorship framing: the AI tutor mentors knowledge competencies (code
interpretation, component and diagram identification, circuit theory,
load calculation, service anatomy, grounding and bonding theory,
meter literacy, procedure walkthroughs, artifact review) end-to-end.
For low-hazard hands-on work on de-energized and verified-dead
circuits, an adult on premises supervises. For energized or
near-energized work, and ANY work where re-energization or backfeed
is possible, a licensed electrician is physically present at the
work; the AI tutor does NOT stand in for the licensed human at the
energized moment.

Goal framing: this is a mastery path. The portfolio of demonstrated
work is the artifact. Certification (NEC and NFPA 70E familiarity,
state apprentice / journeyman / master license, OSHA 10 / 30
Outreach) is a complementary step the learner takes through the
official bodies; possession of a credential never lowers a supervision
requirement.

Regulated topics defer to recognized standards by name: NFPA 70 (NEC;
current edition adopted by the local AHJ); NFPA 70E (Standard for
Electrical Safety in the Workplace; current edition); OSHA 29 CFR
1910.147 (LOTO), 1910.137 (Electrical PPE), 1910.335 (Electrical
Safe Work Practices), 1910.145 (Signs and Tags), 1910.146 (Confined
Spaces), 1926 Subpart M (Fall Protection); ANSI/ISEA Z308.1 (First
Aid); IEC 61010-1 / UL 61010-1 (Multimeter CAT Ratings); the local
AHJ adopted codes and any AHJ-specific amendments; the manufacturer's
service literature for the specific equipment; the employer's written
LOTO program for any apprenticeship under a working employer. No node
invents a code citation, a torque value, an ampacity figure, an
NFPA 70E boundary calculation, or any AHJ-specific rule beyond what
these standards supply.
"""

ELECTRICAL_CONTENT: dict[str, dict] = {
    "el-root": {
        "node_type": "root",
        "trade": "electrical",
        "trade_name": "Residential and low-voltage electrical (intro to master electrician, mastery path)",
        "description": (
            "The electrical trade taught from intro toward mastery, scoped at the foundation "
            "to residential and low-voltage / limited-energy work. The foundation covers: "
            "reading equipment nameplates and rating labels; identifying components and "
            "circuit elements from diagrams and with covers closed; Ohm's law and basic "
            "circuit theory; series and parallel circuits; basic load calculation; reading "
            "wiring diagrams and schematics; the anatomy of a residential electrical "
            "service; conductor sizing and ampacity basics; grounding and bonding theory; "
            "meter and tool literacy including the meaning of multimeter Category (CAT) "
            "ratings; and the apprentice-band gold standard, de-energize / LOTO / "
            "live-dead-live verification on a residential circuit with a licensed "
            "electrician physically present. The foundation explicitly stops at the load "
            "side of the main disconnect: service-entrance work, panel-bus work, meter "
            "work, generator and solar PV interconnection, conduit and cable installation, "
            "termination of conductors, receptacle / switch / fixture / breaker "
            "replacement, GFCI / AFCI device installation, three-phase work, commercial "
            "and industrial work, and any voltage above 600V each enter behind their own "
            "safety gate in later batches. The trade is taught toward demonstrated "
            "competence and a real portfolio of work; the relevant credentials (NEC and "
            "NFPA 70E familiarity, state apprentice / journeyman / master license, OSHA "
            "10 / 30 Outreach) are taken through their official bodies."
        ),
        "default_supervision_policy": {
            "tier_1_knowledge_work": (
                "AI tutor mentors end-to-end. Code interpretation (NEC, NFPA 70E, the AHJ's "
                "adopted codes), component and diagram identification, circuit theory, "
                "load calculation, service anatomy, grounding and bonding theory, "
                "procedure walkthroughs on paper, troubleshooting trees, and artifact "
                "review of the learner's uploaded photos and written procedures belong "
                "here. No human required. The knowledge competencies are where the AI "
                "tutor carries the bulk of the mentoring work."
            ),
            "tier_2_low_hazard_hands_on_de_energized_and_verified_dead_only": (
                "Adult on premises. A parent or other resident adult is in the room or on "
                "the property; the adult does not need electrical credentials for this "
                "tier. The AI tutor guides the learner step by step. Cover-closed "
                "observation, meter familiarization on a known-dead circuit (with the "
                "branch breaker physically locked off and verified dead by a licensed "
                "electrician beforehand), and visual identification work belong here. NO "
                "competencies of this tier are authored in this first batch; they enter "
                "in future batches behind their own gates."
            ),
            "tier_3_energized_or_near_energized_work_or_any_work_where_re_energization_or_backfeed_is_possible": (
                "LICENSED ELECTRICIAN physically present at the work, where licensed means "
                "a state-licensed electrician (apprentice working under a journeyman, OR a "
                "journeyman, OR a master) per the AHJ for the work being performed. The "
                "licensed electrician watches the meter readings, the probe placements, "
                "the lockout-tagout sequence, and is in position to intervene physically "
                "if the learner makes a mistake. The AI tutor mentors the procedure "
                "walkthrough on paper and reviews the artifact evidence (photos of the "
                "LOTO setup, written procedure read-back) but does NOT stand in for the "
                "licensed electrician at the energized moment. elc-021 is the canonical "
                "competency at this tier; all later energized competencies follow the "
                "same supervision rule."
            ),
            "tier_4_regulated_credentialed_milestones": (
                "Deferred to the official bodies and the state AHJ. NEC and NFPA 70E "
                "familiarity is built through the AI-mentored study of the codes; the "
                "codes themselves are obtained through NFPA. State apprentice / "
                "journeyman / master licensing is taken through the AHJ; the required "
                "supervised hours are logged through a state-approved apprenticeship "
                "program, not METHEAN. OSHA 10 / 30 Outreach is delivered by "
                "OSHA-authorized Outreach Training Program trainers. NFPA 70E "
                "electrical-safe-work-practices training is delivered through "
                "recognized providers (employer programs, the electrical training "
                "ALLIANCE for IBEW members, equivalent independent programs). METHEAN "
                "does not administer or proctor any of these."
            ),
            "households_without_a_resident_licensed_electrician": (
                "Common in this trade. For the tier-3 energized competencies, the "
                "household arranges: a paid professional supervision session (a licensed "
                "electrician hired for a defined block of time at a specific competency); "
                "a vocational-school program day or open-shop hours; an apprentice or "
                "shadow arrangement with a working contractor; or defers the energized "
                "competency until the licensed electrician is arranged. The tier-1 "
                "knowledge work the AI mentors is accessible throughout; the tier-3 "
                "energized work is gated until the qualified human is arranged."
            ),
            "all_bands": (
                "Power tools (drills, saws, conduit benders, breakers) and any operation "
                "that opens an enclosure containing live conductors are supervised. The "
                "supervision tier (1, 2, 3) defines how close the supervision is, not "
                "whether it exists. No unsupervised hands-on work on energized subsystems "
                "below the qualified band. Possession of a credential by the learner "
                "(NEC familiarity, state license, NFPA 70E training, OSHA Outreach) "
                "NEVER lowers the supervision tier per the "
                "credentials_NOT_substitutable_for lock in mastery_ladder."
            ),
        },
        "safety_node": "els-001",
        "progression_bands": ["helper", "apprentice", "journeyman", "qualified"],
        "mastery_ladder": {
            "framing": (
                "Mastery in this trade is demonstrated competence PLUS a real portfolio of "
                "work AND readiness for the relevant external credentials. Portfolio and "
                "credential are complementary, not alternatives: a learner with a "
                "portfolio but no credential cannot legally perform regulated electrical "
                "work in most jurisdictions; a learner with a credential but no portfolio "
                "is not yet competent. The ladder below places each authored competency on "
                "its band and places each certification at the point in the ladder where "
                "a learner is genuinely ready for it. The ladder is the surface read by "
                "the planner and rendered in the per-trade map document "
                "(docs/curriculum/electrical_certification_and_mastery_map.md)."
            ),
            "rungs": [
                {
                    "rung_name": "helper",
                    "mastery_level_alias": "emerging",
                    "what_the_learner_does": (
                        "Builds the conceptual foundation an elite apprentice masters "
                        "before any energized work: reads nameplates, identifies "
                        "components from diagrams, learns Ohm's law and basic circuit "
                        "theory, learns series and parallel circuits and basic load "
                        "calculation, learns to read wiring diagrams and schematics, "
                        "learns the anatomy of a residential electrical service, learns "
                        "conductor sizing and ampacity basics by reference to the NEC, "
                        "learns grounding and bonding theory, and learns meter and tool "
                        "literacy including the meaning of multimeter CAT ratings. "
                        "Walks the shop and the household's electrical service with an "
                        "adult on premises. Begins study toward OSHA 10 orientation."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor end-to-end (knowledge work)",
                        "Adult on premises (safety walkthrough)",
                    ],
                    "knowledge_competencies": [
                        "elc-001 (nameplate / rating label)",
                        "elc-002 (component identification from diagrams and with covers closed)",
                        "elc-003 (Ohm's law and basic circuit theory)",
                        "elc-004 (series and parallel circuits; basic load calculation)",
                        "elc-005 (reading wiring diagrams and schematics)",
                        "elc-006 (anatomy of a residential electrical service)",
                        "elc-007 (conductor sizing and ampacity basics)",
                        "elc-008 (grounding and bonding theory)",
                        "elc-009 (meter and tool literacy, including CAT ratings)",
                    ],
                    "safety_competencies": ["els-001"],
                    "low_hazard_hands_on_competencies": [
                        "future batches: meter familiarization on a known-dead circuit with the breaker locked off by a licensed electrician (tier-2 work)",
                    ],
                    "higher_hazard_hands_on_competencies": [],
                    "certifications_appropriate_here": [
                        {
                            "id": "elcert-safety",
                            "specific_credential": "OSHA 10-Hour Outreach (General Industry or Construction)",
                            "rationale": (
                                "Common employer entry prerequisite; reinforces the safety "
                                "vocabulary used in els-001 and prepares the learner for "
                                "the apprentice band."
                            ),
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "Nameplate cards across the household's actual equipment (per elc-001)",
                        "Annotated diagrams and component identification sheets (per elc-002, elc-005)",
                        "Worked Ohm's law / circuit calculations (per elc-003, elc-004, elc-007)",
                        "Annotated diagram of the household's residential service (per elc-006)",
                        "Worked grounding-and-bonding diagrams (per elc-008)",
                        "Multimeter inspection card with CAT rating documented (per elc-009)",
                        "Recorded safety walkthrough video (per els-001)",
                    ],
                },
                {
                    "rung_name": "apprentice",
                    "mastery_level_alias": "developing",
                    "what_the_learner_does": (
                        "Performs the apprentice-band gold standard: de-energize a "
                        "residential branch circuit at the panel, apply formal "
                        "lockout-tagout per OSHA 29 CFR 1910.147, perform the "
                        "live-dead-live verification per NFPA 70E, all with a LICENSED "
                        "ELECTRICIAN physically present at the live moment. Begins "
                        "intensive NEC and NFPA 70E study toward the journeyman exam. "
                        "Earns OSHA 30 if taking on lead responsibility. Begins logged "
                        "apprenticeship hours through a state-approved apprenticeship "
                        "program (NOT through METHEAN)."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor (knowledge work, certification study, procedure walkthrough, artifact review)",
                        "Adult on premises (low-hazard tier-2 hands-on)",
                        "LICENSED ELECTRICIAN physically present (every tier-3 energized act)",
                    ],
                    "knowledge_competencies": [
                        "advanced NEC topics: branch-circuit ratings and load calculations, GFCI/AFCI requirements per AHJ-adopted edition, AFCI vs GFCI distinctions, dwelling-unit receptacle and lighting requirements; NFPA 70E topics: arc-flash boundary calculation methodology, shock approach boundaries, energized-work permit documentation (future batches; each tier-1 knowledge)",
                    ],
                    "safety_competencies": ["els-001 (current per the annual freshness check)"],
                    "low_hazard_hands_on_competencies": [
                        "future batches: receptacle / switch / fixture replacement on a verified-dead circuit, with the breaker locked off and the circuit verified dead per elc-021 each time (tier-2 after verification)",
                    ],
                    "higher_hazard_hands_on_competencies": [
                        "elc-021 (de-energize / LOTO / live-dead-live verification at a residential branch circuit; LICENSED ELECTRICIAN physically present)",
                    ],
                    "certifications_appropriate_here": [
                        {
                            "id": "elcert-safety",
                            "specific_credential": "OSHA 30-Hour Outreach (when the learner takes on lead or supervisory work)",
                            "rationale": "Deeper version of OSHA 10 for workers with supervisory responsibility.",
                        },
                        {
                            "id": "elcert-nec",
                            "specific_credential": "Working familiarity with NEC (NFPA 70) and NFPA 70E (study only; the codes themselves are obtained through NFPA, the AHJ's adopted edition governs)",
                            "rationale": (
                                "The apprentice-band reader is expected to navigate the "
                                "NEC by article and section, locate the AHJ's adopted "
                                "edition, and apply NFPA 70E's live-dead-live and PPE "
                                "guidance to every tier-3 act."
                            ),
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "Live-dead-live verification photographs and written narration with licensed-electrician countersignature (per elc-021)",
                        "OSHA Outreach completion card if taken at this band",
                        "Logged hours toward state apprenticeship requirement, recorded by the state-approved apprenticeship program (NOT by METHEAN)",
                    ],
                },
                {
                    "rung_name": "journeyman",
                    "mastery_level_alias": "proficient",
                    "what_the_learner_does": (
                        "Completes a competency independently to acceptable quality. "
                        "Mentor available but not required step by step for tier-1 and "
                        "tier-2 work. For tier-3 energized work, the supervision rule "
                        "from the apprentice band stays in place: a LICENSED "
                        "ELECTRICIAN is physically present at every live-dead-live "
                        "verification per elc-021, because the verification is the "
                        "safety habit, not a credential gate. The learner now holds the "
                        "state journeyman license per the AHJ (where licensing is "
                        "required), and is legally authorized to perform electrical "
                        "work within the scope the license names. The learner pursues "
                        "specialty study (low-voltage / limited-energy, fire alarm, "
                        "communications, residential generator / solar interconnection) "
                        "as the next focus."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor (continuing-education study, certification preparation, code-update tracking, artifact review)",
                        "Working mentor available but not required step by step (for tier-1 and tier-2 work)",
                        "Licensed electrician physically present (every tier-3 live-dead-live verification, by safety-habit rule)",
                    ],
                    "knowledge_competencies": [
                        "advanced diagnostic frameworks; commercial NEC topics; arc-flash hazard analysis on commercial 480V; controls; fire-alarm and communication-system fundamentals (future batches; each gated separately)",
                    ],
                    "safety_competencies": ["els-001 (current per the annual freshness check)"],
                    "low_hazard_hands_on_competencies": [
                        "complete tier-2 service work (de-energized receptacle, switch, fixture, breaker work after verification) (future batches; each gated separately)",
                    ],
                    "higher_hazard_hands_on_competencies": [
                        "service-entrance work; panel-bus work; meter work; generator and solar PV interconnection; conduit and cable installation; full energized troubleshooting under licensed-electrician-present (future batches; each tier-3, each gated separately)",
                    ],
                    "certifications_appropriate_here": [
                        {
                            "id": "elcert-licensing",
                            "specific_credential": "State journeyman electrician license per the AHJ (in jurisdictions that license; in low-voltage-specific states, the low-voltage / limited-energy journeyman license per the AHJ)",
                            "rationale": (
                                "Earned after completing the AHJ's apprenticeship hours "
                                "requirement through a recognized apprenticeship and "
                                "passing the AHJ's journeyman exam. The learner is now "
                                "legally authorized to perform electrical work within "
                                "the scope the license names."
                            ),
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "Complete service-call write-ups across the chosen specialty",
                        "State journeyman electrician license (obtained from the AHJ)",
                        "Logged journeyman experience hours toward master eligibility (where applicable)",
                    ],
                },
                {
                    "rung_name": "qualified",
                    "mastery_level_alias": "mastered",
                    "what_the_learner_does": (
                        "Performs reliably under varied conditions across the chosen "
                        "specialty (residential, low-voltage / limited-energy, fire alarm, "
                        "communications, etc.). Teaches helpers and apprentices through "
                        "the helper-band steps. Holds the AHJ's master / contractor "
                        "license where applicable, with the bonding, insurance, and "
                        "continuing-education the AHJ requires. Maintains NFPA 70E "
                        "currency. Carries the licensed-electrician-physically-present "
                        "role for the next generation of learners performing tier-3 "
                        "work."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor (continuing-education, code-update tracking, master exam preparation, artifact review)",
                        "Peer review (other masters / contractors)",
                        "Learner now MENTORS others as the licensed electrician physically present for their tier-3 work",
                    ],
                    "knowledge_competencies": [
                        "advanced controls and building automation; commercial design; lighting and energy modeling; project management; business and contract law (master / contractor level) (future batches)",
                    ],
                    "safety_competencies": ["els-001 (current per the annual freshness check; learner now leads the walkthrough for helpers)"],
                    "low_hazard_hands_on_competencies": [
                        "full design-and-install of a residential branch-circuit addition (future batch; a project node)",
                    ],
                    "higher_hazard_hands_on_competencies": [
                        "complete residential or light-commercial install; service-entrance and panel work; generator and solar interconnection; full energized troubleshooting (future batches; each gated separately, each tier-3)",
                    ],
                    "certifications_appropriate_here": [
                        {
                            "id": "elcert-licensing",
                            "specific_credential": "State master electrician license per the AHJ (or master limited-energy where applicable); contractor licensing additionally per the AHJ's contractor rules",
                            "rationale": (
                                "Earned after the journeyman experience requirement the "
                                "AHJ publishes, plus business / law exam in many states, "
                                "plus bonding and insurance per the AHJ."
                            ),
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "State master electrician license (obtained from the AHJ)",
                        "Contractor license and bonding / insurance documentation where applicable (obtained from the AHJ)",
                        "A full project portfolio (residential install, low-voltage system install, training-of-apprentice records)",
                        "Continuing-education currency in NFPA 70E and the local AHJ's continuing-education requirements",
                    ],
                },
            ],
            "mastery_marker": (
                "The learner is qualified when: (1) every authored competency in the "
                "chosen residential or low-voltage specialty has been demonstrated at "
                "the proficient or mastered band with portfolio artifacts; (2) the "
                "legally required credentials for the work the learner intends to do "
                "are held (state journeyman or master license per the AHJ for the work "
                "the AHJ regulates); (3) the learner has either signed off a "
                "helper-band attempt for another learner OR completed a "
                "journeyman-band project entirely unsupervised at tier-1 and tier-2, "
                "with every tier-3 energized step still performed under licensed-"
                "electrician-present (energized work is NEVER unsupervised below the "
                "qualified band, and even at the qualified band, the licensed-"
                "electrician-physically-present rule applies on every elc-021 act as "
                "the safety habit)."
            ),
            "credentials_NOT_substitutable_for": [
                (
                    "Knowledge of the NEC (NFPA 70) and NFPA 70E does NOT substitute "
                    "for any supervision rule in this trade. A learner with deep code "
                    "knowledge still performs live-dead-live verification on every "
                    "energized job per elc-021 because the verification is the safety "
                    "habit, not a credential gate."
                ),
                (
                    "A state apprentice / journeyman / master electrician license does "
                    "NOT substitute for any specific safety competency authored in "
                    "this trade. License-holders still perform live-dead-live "
                    "verification on every service call as elc-021 teaches, every "
                    "time, regardless of how many years they have been licensed."
                ),
                (
                    "OSHA 10 / 30 Outreach completion does NOT substitute for "
                    "site-specific or task-specific safety training required by "
                    "particular OSHA standards (LOTO per 1910.147, fall protection per "
                    "1926 Subpart M, confined-space entry per 1910.146). Those remain "
                    "the employer's responsibility under OSHA's specific-training "
                    "requirements."
                ),
                (
                    "NFPA 70E electrical-safe-work-practices training does NOT "
                    "substitute for the supervision policy or for any safety "
                    "competency authored in this trade. NFPA 70E defines the "
                    "safe-work-practices the trade follows; training does not "
                    "authorize a learner to bypass the supervision tier required for "
                    "the work."
                ),
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "els-001": {
        "node_type": "safety",
        "trade": "electrical",
        "competency_name": (
            "Electrical shop and site safety: line-voltage and low-voltage shock hazards, "
            "arc flash, stored energy, backfeed sources, multiwire branch circuits, the "
            "neutral conductor, GFCI / AFCI protection, lockout-tagout, multimeter Category "
            "ratings, PPE, working space and clearance, fire and CO from electrical sources, "
            "and the scope boundaries of the foundation"
        ),
        "progression_band": "helper",
        "prerequisites": [],
        "safety_basis": {
            "hazards": [
                (
                    "Electrocution from line voltage. Residential branch circuits are typically "
                    "120V/60Hz/1-phase or 240V/60Hz/1-phase in the US; the nameplate per "
                    "elc-001 and the panel labeling are the authorities for the specific "
                    "circuit. Across the heart at residential fault current, line voltage can "
                    "stop the heart. The default in this trade is to de-energize, lock out, "
                    "and verify dead before any contact with a conductor; elc-021 is the "
                    "competency that teaches the verification."
                ),
                (
                    "Shock from low-voltage and control circuits. Doorbell, thermostat, "
                    "communication, and limited-energy systems run at 24VAC or lower in most "
                    "residential applications; shock risk is lower than line voltage but real, "
                    "and the involuntary-reaction risk (jerking a hand into a sharp edge or a "
                    "fan blade) is not lower. The control side of any equipment is treated as "
                    "live until verified dead."
                ),
                (
                    "Arc flash from a short during energized work. Arc-flash hazard on "
                    "residential 120V and 240V is smaller than commercial 480V but real, with "
                    "real burn and concussive-injury risk. NFPA 70E provides the boundary "
                    "calculation methodology and the arc-rated PPE requirements; the default "
                    "in this trade is to de-energize and verify dead before opening, which "
                    "removes the arc-flash hazard at the work point."
                ),
                (
                    "Stored energy in capacitors. Capacitors in HVAC equipment, motor "
                    "starters, light ballasts (older), and some electronic equipment can hold "
                    "lethal charge for minutes to hours after the system is de-energized. "
                    "Capacitor discharge is its own competency, not authored in this batch; "
                    "the rule at this band is no capacitor contact without a licensed "
                    "electrician present and the manufacturer's discharge procedure in hand."
                ),
                (
                    "Backfeed from a generator. A residential standby or portable generator "
                    "connected without a transfer switch or interlock per the AHJ-adopted NEC "
                    "and NFPA 70 can backfeed power onto a circuit the utility has "
                    "de-energized. This is a documented failure mode that has killed line "
                    "workers and homeowners. Any premises with a generator is treated as a "
                    "backfeed source until the transfer arrangement is verified by a licensed "
                    "electrician."
                ),
                (
                    "Backfeed from solar PV. A residential solar PV inverter connected without "
                    "proper anti-islanding (rapid-shutdown per the AHJ-adopted NEC for "
                    "rooftop arrays, supply-side or load-side interconnection per the AHJ) "
                    "can backfeed power onto a circuit the utility or the main breaker has "
                    "de-energized. Any premises with solar PV is treated as a backfeed source "
                    "until the interconnection and rapid-shutdown arrangement is verified by "
                    "a licensed electrician."
                ),
                (
                    "Multiwire branch circuit (MWBC) shared-neutral hazard. An MWBC shares a "
                    "single neutral conductor between two hot legs of opposite phases; "
                    "opening the neutral on an energized MWBC can place the full line-to-line "
                    "voltage across whatever load was connected to the smaller leg, and can "
                    "produce a voltage on the supposedly-neutral wire that will shock a "
                    "person who touches it. MWBC identification and the rule against opening "
                    "the neutral on an energized circuit are covered in the apprentice band "
                    "alongside elc-021; at this safety band the rule is the learner does NOT "
                    "open any neutral on any circuit without a licensed electrician present."
                ),
                (
                    "Neutral-to-ground bond fault. The neutral and the ground are bonded "
                    "together only at the main service equipment per the AHJ-adopted NEC; "
                    "downstream of the main, they must remain separate. A fault that places "
                    "the neutral and ground at different potentials at a downstream point can "
                    "energize metal that is normally at ground potential. This is the reason "
                    "verification at the work point is mandatory in elc-021."
                ),
                (
                    "Thermal burns from hot conductors and heated components. Overloaded "
                    "conductors, undersized breakers run at peak load, and damaged splices "
                    "can heat to combustion temperatures. Visual inspection alone is "
                    "unreliable; a damaged splice may not look damaged. Discoloration of "
                    "conductor insulation, scorch marks at terminations, and warm cover "
                    "plates are stop-work signals."
                ),
                (
                    "Fire from arcing faults, overloaded circuits, damaged insulation, and "
                    "improper terminations. AFCI (arc-fault circuit interrupter) protection "
                    "is required by the AHJ-adopted NEC on most dwelling-unit branch circuits "
                    "in current editions, specifically to detect the arcing-fault failure "
                    "mode. Damaged extension cords, undersized cords, and improperly stapled "
                    "or terminated nonmetallic-sheathed cable are common arc-fault initiators."
                ),
                (
                    "Carbon monoxide from electrical sources is rare directly but secondary "
                    "to electrical failure in some installations (a failed thermostat that "
                    "fires a furnace incorrectly, a generator running indoors). A working CO "
                    "alarm in the household is required by code in most US jurisdictions per "
                    "the AHJ-adopted NFPA 720; the rule for an active CO alarm during "
                    "electrical work is stop work and evacuate."
                ),
                (
                    "Sheet-metal and conductor-end cuts. Stripped conductor ends and cut "
                    "sheathing have sharp edges; junction box and panel edges are often "
                    "sharp; cut-resistant gloves are the default for any conductor handling "
                    "and any panel work."
                ),
                (
                    "Eye injury from metal swarf (cutting cable, drilling boxes), insulation "
                    "fragments, arc flash, and solvent splash. Safety glasses are the default "
                    "in this trade for any work inside an enclosure; face shield per NFPA 70E "
                    "for any energized work."
                ),
                (
                    "Falls from ladders and elevated work. Reaching panels mounted high, "
                    "fixtures in stairwells, and any attic or crawl-space work all involve "
                    "ladder or elevated risk. OSHA 29 CFR 1910.23 (ladders) and 1926 Subpart "
                    "M (fall protection) govern; elevated work is not authored in this "
                    "batch."
                ),
                (
                    "Confined-space exposure. Crawl spaces, attics in summer, panel rooms "
                    "with poor ventilation are confined or potentially confined spaces. OSHA "
                    "29 CFR 1910.146 governs permit-required confined-space entry; "
                    "confined-space work is not authored in this batch."
                ),
                (
                    "Wrong-circuit and wrong-disconnect failure. A learner who misidentifies "
                    "the breaker or disconnect for the circuit being worked, or who trusts a "
                    "panel label that is wrong (panel labels are commonly wrong in older or "
                    "remodeled homes), can de-energize the wrong circuit and walk into a live "
                    "one. The verification at the work point (elc-021) is the safeguard; the "
                    "rule at this band is verify, never assume."
                ),
                (
                    "Wrong meter Category (CAT) rating. A multimeter at insufficient CAT "
                    "rating for the circuit can read zero on a live circuit, can fail "
                    "internally during the measurement, or can explode in the user's hand "
                    "during a fault. CAT III at 600V minimum is the residential standard per "
                    "NFPA 70E for 240V branch-circuit verification; IEC 61010-1 / UL 61010-1 "
                    "define the Categories. This is one of the documented causes of "
                    "electrocution and burn injuries in working electricians."
                ),
                (
                    "Working space and clearance. NEC working-space and headroom requirements "
                    "(per the AHJ-adopted edition) exist precisely so that a person working "
                    "on or near energized equipment has room to step back if the work goes "
                    "wrong. Working in cramped quarters around a panel violates the code and "
                    "removes the escape path. The rule is no work begins where the working "
                    "space is below the AHJ-adopted minimum."
                ),
                (
                    "Wet conditions. Working on or near electrical equipment in rain, "
                    "standing water, or on a wet pad significantly increases shock risk. The "
                    "default is to defer; if the situation is urgent, the licensed "
                    "electrician present decides whether additional PPE per NFPA 70E "
                    "justifies proceeding."
                ),
                (
                    "Scope boundary. The foundation explicitly stops at the load side of the "
                    "main disconnect. Service-entrance work (line side of the main, meter "
                    "work, the utility supply) is regulated more strictly than branch-circuit "
                    "work, may require utility involvement, and is NOT in scope at the "
                    "foundation. Any work on the supply side is deferred to the licensed "
                    "electrician with the appropriate scope and the AHJ-permitted "
                    "arrangement."
                ),
            ],
            "ppe_required": [
                (
                    "Closed-toe leather work boots with non-slip soles. No sneakers in the "
                    "panel room, on a service-entrance work site, or near energized "
                    "equipment. Electrical-rated (EH-rated) soles preferred for any tier-3 "
                    "energized work."
                ),
                (
                    "Safety glasses (ANSI Z87.1) as the shop-wide default any time an "
                    "enclosure is open, any time conductor ends are being cut or stripped, "
                    "any time work near energized equipment is performed. A full face shield "
                    "(in addition to safety glasses) for any energized work per NFPA 70E for "
                    "the calculated arc-flash incident energy at the work point."
                ),
                (
                    "Insulating gloves rated for the voltage actually being worked are "
                    "required for any energized electrical work per NFPA 70E. Class 00 "
                    "(rated 500V) minimum for 240V residential branch-circuit verification; "
                    "the licensed electrician present confirms the class and the inspection "
                    "(visual for cuts and ozone cracking; air-roll test per the manufacturer "
                    "where applicable) before each use."
                ),
                (
                    "Leather protectors over insulating gloves for any work where the "
                    "insulating glove can be punctured or cut (handling sharp tools, "
                    "reaching into panels with sharp edges); per NFPA 70E."
                ),
                (
                    "Arc-rated clothing per NFPA 70E for the calculated arc-flash incident "
                    "energy at the work point. The licensed electrician present confirms the "
                    "PPE category. The default in this trade is to de-energize and verify "
                    "dead before opening, removing the arc-flash hazard at the work point; "
                    "energized work is not in this first batch."
                ),
                (
                    "Cut-resistant gloves (ANSI/ISEA 105 cut level A4 or higher recommended) "
                    "for any conductor handling, any cable stripping, and any panel work "
                    "after voltage is verified dead per elc-021; not for energized work, "
                    "where insulating gloves take precedence. The household or employer "
                    "program names the actual cut level."
                ),
                (
                    "Hearing protection (ANSI/ASA S3.19) in any space with running equipment "
                    "loud enough to require raised voice; per current OSHA / NIOSH "
                    "occupational noise-exposure guidance."
                ),
                (
                    "No metal jewelry on hands, wrists, or neck for any work near energized "
                    "equipment. No watches with metal bands, no rings, no chains, no metal "
                    "earrings near the work point."
                ),
                (
                    "Long sleeves rolled down near energized equipment, hot conductors, or "
                    "any operation where falling sparks or molten metal is possible. Hair "
                    "tied back if long enough to fall into the work."
                ),
                (
                    "Multimeter at CAT III for 600V minimum (CAT IV acceptable; CAT II or "
                    "unrated meters NOT acceptable per NFPA 70E) for any residential 240V "
                    "verification, with intact test leads, current battery, current fuse, "
                    "and current calibration where the household or employer program "
                    "requires calibration tracking. The licensed electrician present "
                    "confirms the CAT rating before any tier-3 verification begins."
                ),
                (
                    "Fall protection per OSHA 29 CFR 1926 Subpart M for any work above the "
                    "OSHA-defined threshold. The personal fall arrest system (harness, "
                    "lanyard, anchor) is inspected before each use per the manufacturer and "
                    "OSHA. Elevated work is not authored in this first batch; the "
                    "requirement is named here so it is in the safety walkthrough."
                ),
                (
                    "Insulated tools (rated 1000V or higher per IEC 60900 / ASTM F1505) for "
                    "any work near energized equipment per NFPA 70E. The licensed electrician "
                    "present confirms tool rating before any tier-3 work begins."
                ),
            ],
            "supervision_required": True,
            "supervision_basis": (
                "The safety competency is itself supervised: an adult on premises walks the "
                "learner through every hazard in the actual electrical equipment and the "
                "actual tool kit, and signs off only when the learner can name and locate "
                "each. The supervising adult does not need electrical credentials for the "
                "walkthrough itself; a parent or other resident adult counts. The AI tutor "
                "may guide what to look for and review the recorded walkthrough video. "
                "There is no self-attestation on safety. The mentor confirms the "
                "household's plans for: working CO alarm presence and function per current "
                "NFPA 720 and the AHJ; fire extinguisher rating and placement per local "
                "fire-safety authority confirmation; first aid kit per ANSI/ISEA Z308.1 or "
                "current American Red Cross guidance; tetanus immunization status per each "
                "household member's healthcare provider; the location of the main "
                "disconnect; the labeling state of the panel (panel labels are commonly "
                "wrong in older or remodeled homes and must be verified at the work point); "
                "any backfeed sources on the property (generator, solar PV); and the "
                "household's understanding that any tier-3 energized work requires a "
                "licensed electrician physically present per the trade root's "
                "default_supervision_policy."
            ),
            "fresh_safety_signoff_within_days": None,
        },
        "tools_required": [
            {
                "name": "First aid kit",
                "specification": (
                    "A kit that meets a recognized standard for first-aid contents: ANSI/ISEA "
                    "Z308.1 (Minimum Requirements for Workplace First Aid Kits and Supplies) or "
                    "current American Red Cross guidance. The authoritative contents list is "
                    "the named standard. The kit accompanies the work area; on a service call "
                    "the kit is in the truck."
                ),
                "alternatives": [],
            },
            {
                "name": "Working CO alarm",
                "specification": (
                    "A CO alarm listed (UL 2034 residential or UL 2075 commercial) and placed "
                    "per current NFPA 720 and the local AHJ. Installation date and "
                    "manufacturer service life tracked. Any CO alarm activation during "
                    "electrical service is a stop-work event."
                ),
                "alternatives": [],
            },
            {
                "name": "Fire extinguisher",
                "specification": (
                    "An A:B:C rated multipurpose extinguisher within reach of the work area "
                    "is the conservative default. The household confirms the appropriate "
                    "rating with a local fire-safety authority. For electrical fires, only a "
                    "rating that includes Class C is appropriate; do not use a Class A-only "
                    "(water) extinguisher on energized electrical equipment."
                ),
                "alternatives": [],
            },
            {
                "name": "Working flashlight or headlamp",
                "specification": (
                    "Panels, crawl spaces, attics, and behind-equipment areas are commonly "
                    "dark. A headlamp leaves both hands free; preferred for electrical work."
                ),
                "alternatives": [],
            },
            {
                "name": "Cell phone or way to call for help",
                "specification": (
                    "A way to reach emergency services quickly. The household's standing "
                    "instructions cover when to call for: severe electrical shock; arc-flash "
                    "burn; serious fall; fire from an electrical source; CO alarm activation."
                ),
                "alternatives": [],
            },
            {
                "name": "The household's adopted-edition NEC and a current NFPA 70E reference",
                "specification": (
                    "The current NEC edition adopted by the local AHJ, and current NFPA 70E "
                    "(both obtained through NFPA or recognized publishers; the household "
                    "identifies their AHJ's current adopted edition). The codes themselves "
                    "are the authority for any specific rule; this node names that authority "
                    "without reproducing code text."
                ),
                "alternatives": [],
            },
            {
                "name": "The household's panel-labeling state and main-disconnect location",
                "specification": (
                    "The main disconnect is located, labeled, and clear (working space and "
                    "headroom per the AHJ-adopted NEC). The panel labeling is verified by "
                    "the licensed electrician on a service visit; the labels are not "
                    "trusted at the work point. Panel labels in older or remodeled homes "
                    "are commonly wrong; the verification at the work point (elc-021) is "
                    "the safeguard."
                ),
                "alternatives": [],
            },
            {
                "name": "Tetanus immunization status (household-level)",
                "specification": (
                    "Every household member working in or near electrical panels and junction "
                    "boxes has a tetanus immunization status current per their healthcare "
                    "provider's recommendation. Sharp panel edges and cut conductor ends are "
                    "the primary in-trade tetanus exposures."
                ),
                "alternatives": [],
            },
            {
                "name": "Tool storage for sharp and insulated tools",
                "specification": (
                    "Sharp tools (wire strippers / cutters, utility knives, conduit "
                    "reamers), insulated tools (rated screwdrivers, pliers, nut drivers), "
                    "and insulating gloves have a designated home in the truck or the shop "
                    "and are returned to it at end of session. Insulated tools are "
                    "inspected for insulation damage before each use per NFPA 70E."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": (
                "Real residential electrical service (main panel location, subpanels if "
                "present, branch circuits in the actual rooms), the household's actual "
                "equipment, and the household's tool kit. The walkthrough is in the actual "
                "environment, not on paper or in a classroom."
            ),
            "ventilation": "Adequate to detect any thermal or burning smell from electrical equipment",
            "lighting": (
                "Daylight or strong task lighting; portable flashlight or headlamp "
                "available for panel interiors and dark corners"
            ),
            "power": (
                "Energy state immaterial for the cover-closed walkthrough at this safety "
                "band; for any cover-removed view of the panel or any junction box, the "
                "disconnect is verified open under elc-021 by a licensed electrician "
                "(which is a different competency, not in scope for this node's "
                "unsupervised practice)"
            ),
            "containment": "Clear floor space around panels; pets and small children excluded from the work area",
        },
        "skill_description": (
            "The learner walks the actual residential electrical service and the actual "
            "tool kit with an adult on premises, and learns where every safety element "
            "lives, what every hazard looks like, and how the safe habits work. They "
            "learn the PPE rules and when each item is required; the rule that the absence "
            "of voltage is verified by a meter before any contact with wiring per elc-021; "
            "the rule that capacitors are treated as charged until discharged per the "
            "manufacturer and never contacted at this band; the rule that backfeed sources "
            "(generators, solar PV) on the property are treated as live until the transfer "
            "arrangement is verified by a licensed electrician; the rule that the neutral "
            "is treated as a current-carrying conductor and not opened on an energized "
            "circuit; the rule that panel labels are not trusted at the work point and are "
            "verified by the licensed electrician; the rule that working-space and "
            "headroom around any panel must meet the AHJ-adopted NEC minimum before work "
            "begins; the rule that wet conditions defer any tier-3 work; the rule that hot "
            "work (where any) is gated separately; the rule that elevated and "
            "confined-space work is gated separately; the rule that the foundation stops "
            "at the load side of the main disconnect; the rule that any work above 600V is "
            "outside the foundation entirely. They learn where the first aid kit, the CO "
            "alarm, the fire extinguisher, the flashlight, the phone for help, and the "
            "household's NEC and NFPA 70E references live. They learn that the "
            "manufacturer's service literature and the AHJ's adopted codes are the "
            "authorities for the specific equipment and the specific work, not the AI "
            "tutor and not a general reference."
        ),
        "demonstration_criteria": [
            "Names every PPE item on the list and explains when each is required and when each is permitted",
            (
                "Locates the first aid kit and confirms it meets a recognized standard "
                "(ANSI/ISEA Z308.1 or current American Red Cross guidance)"
            ),
            (
                "Locates the fire extinguisher within reach of the work area, names its "
                "rating, and confirms the rating includes Class C for electrical fires per "
                "household confirmation with local fire-safety authority"
            ),
            (
                "Locates the CO alarm(s) covering the household's combustion equipment and "
                "confirms each is listed (UL 2034 or UL 2075), within the manufacturer's "
                "service-life window, and placed per current NFPA 720 and the local AHJ"
            ),
            (
                "Locates the main disconnect, names that it is the device used to "
                "de-energize the entire household electrical service, and confirms working "
                "space and headroom per the AHJ-adopted NEC minimum at the panel"
            ),
            (
                "Names any backfeed sources on the property (generator, solar PV) and "
                "confirms that the transfer or interconnection arrangement was installed "
                "by a licensed electrician and verified by the AHJ"
            ),
            (
                "Names the household's tetanus immunization status arrangement and "
                "confirms with the mentor that every working household member is current "
                "per their healthcare provider's recommendation"
            ),
            (
                "Names the rule that the absence of voltage is verified by a meter before "
                "any contact with wiring per NFPA 70E (the live-dead-live sequence) and "
                "OSHA 29 CFR 1910.147, and points to where elc-021 lives in the "
                "helper-to-apprentice path"
            ),
            (
                "Names the rule that capacitors are treated as charged until discharged "
                "per the manufacturer, and that capacitor contact is NOT in scope at this "
                "band without a licensed electrician present and the manufacturer's "
                "discharge procedure in hand"
            ),
            (
                "Names the rule that the neutral is a current-carrying conductor and is "
                "never opened on an energized circuit, and names the MWBC shared-neutral "
                "case as the specific failure mode"
            ),
            (
                "Names the rule that panel labels in older or remodeled homes are commonly "
                "wrong and are verified at the work point, not trusted from the label"
            ),
            (
                "Names the wrong-CAT-rating multimeter failure mode and identifies the "
                "household's multimeter's CAT rating; confirms CAT III at 600V minimum is "
                "available for any tier-3 work"
            ),
            (
                "Names the rule that wet conditions defer any tier-3 energized work; names "
                "the no-ignition-source rule for any work that might produce arc or spark"
            ),
            (
                "Names the rule that hot work, elevated work, and confined-space work are "
                "each gated separately and not in scope at this band"
            ),
            (
                "Names the scope boundary: the foundation stops at the load side of the "
                "main disconnect; service-entrance work is out of scope; any voltage above "
                "600V is out of scope; three-phase work is out of scope at the foundation"
            ),
            (
                "Locates the household's NEC (AHJ-adopted edition) and NFPA 70E references "
                "and demonstrates looking up one general topic (e.g. NEC Article 250 for "
                "grounding and bonding) in each; names the rule that the AHJ-adopted "
                "edition governs"
            ),
            (
                "Names the trade rule that the manufacturer's service literature and the "
                "AHJ's adopted codes are the authorities for specific work, not a general "
                "reference and not the AI tutor"
            ),
            (
                "Demonstrates safe tool storage at the end of a session: sharp tools "
                "sheathed or cased, insulated tools inspected and returned, insulating "
                "gloves inspected and stored per the manufacturer, no tools in walkways"
            ),
        ],
        "common_errors": [
            {
                "error": "Assuming a circuit is dead because the breaker was thrown",
                "cause": "The learner trusted the breaker position or the panel label without verifying with a meter",
                "remedy": (
                    "The absence of voltage is verified by a meter, never assumed. The "
                    "live-dead-live sequence is the rule: verify the meter on a known-live "
                    "source first, verify dead at the work point, then re-verify the meter "
                    "on the known-live source. This is what elc-021 teaches; the safety "
                    "walkthrough establishes the rule in advance. Panel labels are not "
                    "trusted at the work point."
                ),
            },
            {
                "error": "Opening the neutral on an energized multiwire branch circuit",
                "cause": "The learner did not recognize the MWBC and treated the neutral as not-current-carrying",
                "remedy": (
                    "The neutral is a current-carrying conductor whenever the circuit is "
                    "energized. On an MWBC, opening the neutral places the full line-to-line "
                    "voltage across the loads, and produces a voltage on the formerly-"
                    "neutral wire. The rule is the neutral is verified dead at the work "
                    "point and is never opened on an energized circuit. MWBC identification "
                    "is part of elc-021 with the licensed electrician present."
                ),
            },
            {
                "error": "Working near a generator transfer switch or solar inverter without verifying the backfeed isolation",
                "cause": "The learner assumed the main disconnect at the panel cuts everything",
                "remedy": (
                    "Generators and solar PV inverters can backfeed power onto circuits "
                    "the main disconnect cannot reach. Any backfeed source on the property "
                    "is verified isolated by the licensed electrician before any work "
                    "downstream; the AHJ-required transfer switch or interlock is the "
                    "protective device. The work at the panel is not begun until the "
                    "backfeed isolation is confirmed."
                ),
            },
            {
                "error": "Using a CAT II or unrated meter for a 120V or 240V residential measurement",
                "cause": "The learner used the meter that was in the toolbag without checking the CAT rating",
                "remedy": (
                    "The CAT rating addresses the transient voltage the meter is designed "
                    "to survive. A CAT II meter on a CAT III circuit can read zero on a "
                    "live conductor, can fail internally during the measurement, or can "
                    "explode in the user's hand during a fault. CAT III at 600V minimum is "
                    "the rule per NFPA 70E for this measurement. The licensed electrician "
                    "present confirms the CAT rating before any tier-3 work begins."
                ),
            },
            {
                "error": "Trusting a panel label that says BREAKER 12 controls the work circuit",
                "cause": "The learner read the label and threw the breaker; the label was wrong from a remodel",
                "remedy": (
                    "Panel labels in older or remodeled homes are commonly wrong. The "
                    "verification at the work point (live-dead-live per elc-021) catches "
                    "the wrong-circuit failure mode. Every elc-021 act verifies dead at the "
                    "work point regardless of what the label said. The label is corrected "
                    "after the work point is verified."
                ),
            },
            {
                "error": "Working on or near a panel in a wet basement after a flood",
                "cause": "The learner saw water on the floor and proceeded anyway",
                "remedy": (
                    "Wet conditions significantly increase shock risk. The work is deferred "
                    "to dry conditions; if the situation is urgent (a real outage from a "
                    "real flood), the licensed electrician present decides whether to "
                    "proceed with additional PPE per NFPA 70E or to call the utility. The "
                    "default is to defer."
                ),
            },
            {
                "error": "Reaching into a panel with metal jewelry on the hands or wrists",
                "cause": "The learner forgot a watch, ring, or bracelet",
                "remedy": (
                    "Metal jewelry on the hands, wrists, or neck near energized equipment "
                    "is a documented cause of severe burn injuries. Jewelry comes off "
                    "before any work near a panel or any energized equipment. The "
                    "supervising adult confirms before the work begins."
                ),
            },
            {
                "error": "Standing on a chair to reach an overhead light fixture",
                "cause": "The learner skipped getting a ladder for what felt like a quick reach",
                "remedy": (
                    "A real ladder rated for the duty and the height, set up per the "
                    "manufacturer's instructions and OSHA 1910.23, is the rule. No chairs, "
                    "no buckets, no stacked stools. Elevated work is gated separately at "
                    "later bands."
                ),
            },
            {
                "error": "Opening a junction box to 'see what's inside' on an old circuit",
                "cause": "The learner was curious about how the existing wiring was run",
                "remedy": (
                    "Opening any junction box exposes conductors that may be live, may "
                    "include shared neutrals from an MWBC, may be old aluminum or "
                    "knob-and-tube wiring with specific hazards, and is tier-3 work. "
                    "Opening is deferred to a session with a licensed electrician present "
                    "performing the verification per elc-021."
                ),
            },
            {
                "error": "Touching the panel bus or any conductor on the line side of the main disconnect",
                "cause": "The learner thought the main disconnect cut all power",
                "remedy": (
                    "The line side of the main disconnect (the conductors from the meter to "
                    "the main breaker, the meter itself, and the supply from the utility) "
                    "remains energized even when the main is open. Service-entrance work is "
                    "regulated more strictly than branch-circuit work, may require utility "
                    "involvement, and is OUT OF SCOPE at the foundation. The learner does "
                    "NOT touch the line side at this band."
                ),
            },
        ],
        "artifact_expected": {
            "type": "video",
            "what_to_capture": (
                "A short walkthrough by the learner of the household's actual electrical "
                "service and the tool kit (under ten minutes), pointing at and naming each "
                "item on the demonstration_criteria list, with the supervising adult "
                "offscreen or beside the learner. The AI tutor reviews the walkthrough "
                "video for completeness and correctness against the demonstration_criteria "
                "list."
            ),
            "what_the_evidence_shows": (
                "That the learner can identify, locate, and explain every safety element "
                "in the electrical service they will be working in, can demonstrate the "
                "stop-work rules for wet conditions and CO alarm activation, can locate "
                "and look up a topic in the AHJ-adopted NEC and NFPA 70E, and can name "
                "the bands at which each hazard-class operation enters scope and the "
                "licensed-electrician-present rule for those bands"
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The supervising adult walks the learner through the actual residential "
                "electrical service and the tool kit, naming each hazard and each piece of "
                "safety equipment, demonstrating the safe-carry and safe-pass habits, "
                "demonstrating tool inspection (insulated screwdriver insulation, insulating "
                "glove visual check), demonstrating the location of the main disconnect "
                "and any subpanels, demonstrating the location of any backfeed sources "
                "(generator, solar PV) on the property and the AHJ-permitted transfer "
                "arrangement, demonstrating the location of the household's NEC and NFPA "
                "70E references and looking up one topic in each. The adult names what is "
                "forbidden as well as what is required, and explicitly names the bands at "
                "which each higher-hazard operation enters scope and the licensed-"
                "electrician-physically-present rule for tier-3 work. The AI tutor "
                "provides the walkthrough script and the demonstration_criteria list so "
                "the adult and the learner know what to cover."
            ),
            "we_do": (
                "Supervising adult and learner walk the service together. At each station "
                "the learner names the item and the adult confirms or corrects. The "
                "learner takes a turn inspecting an insulated tool, locating the main "
                "disconnect, and looking up a topic (e.g. NEC Article 250 grounding) in "
                "the household's adopted-edition NEC. The learner walks through the "
                "wrong-CAT-rating failure-mode story in narration, and walks through the "
                "MWBC shared-neutral hazard in narration."
            ),
            "you_do_supervised": (
                "The learner walks the supervising adult through the electrical service "
                "and the tool kit, naming and locating each item without prompting. The "
                "adult asks at least one follow-up question per item, drawn from the AI "
                "tutor's suggested questions ('what is the rule on the panel labels?', "
                "'where is the gas shutoff in case of fire?', 'what is the rule on the "
                "neutral?'). The video is recorded at this stage and uploaded for the AI "
                "tutor's review against the demonstration_criteria list."
            ),
            "you_do_unsupervised": (
                "Once signed off (by the supervising adult, with the AI tutor's "
                "confirmation that the walkthrough video covers every demonstration "
                "criterion), the learner does the same walkthrough at the start of any "
                "session in a new or modified electrical service, after any change to the "
                "equipment or the household's plans (new generator installation, solar PV "
                "installation, breaker replacement, panel replacement), and at any change "
                "of seasons when the load profile changes. In any case the signoff is "
                "refreshed annually as the freshness check. There is no unsupervised work "
                "on hazardous subsystems below the qualified band; even at the qualified "
                "band, every tier-3 energized act follows the licensed-electrician-"
                "physically-present rule on elc-021 as the safety habit."
            ),
        },
        "estimated_practice_sessions_to_signoff": 3,
        "session_length_minutes": 60,
        "signoff_validity_days": 365,
        "related_projects": [],
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                "ANSI/ISEA Z308.1 (Workplace First Aid Kits)",
                "American Red Cross home/shop first-aid kit guidance",
                "OSHA 29 CFR 1910.147 (The Control of Hazardous Energy / Lockout-Tagout)",
                "OSHA 29 CFR 1910.146 (Permit-Required Confined Spaces)",
                "OSHA 29 CFR 1910.137 (Electrical Protective Equipment)",
                "OSHA 29 CFR 1910.335 (Electrical Safety-Related Work Practices)",
                "OSHA 29 CFR 1910.145 (Specifications for Accident Prevention Signs and Tags)",
                "OSHA 29 CFR 1910.23 (Walking-Working Surfaces, including ladders)",
                "OSHA 29 CFR 1926 Subpart M (Fall Protection)",
                "NFPA 70 (NEC; current edition adopted by the local AHJ)",
                "NFPA 70E (Standard for Electrical Safety in the Workplace; current edition)",
                "NFPA 720 (CO Detection and Warning Equipment)",
                "IEC 61010-1 and UL 61010-1 (Multimeter Category Ratings: CAT II / III / IV)",
                "IEC 60900 and ASTM F1505 (Insulated and Insulating Hand Tools)",
                "UL 2034 (residential CO alarms) and UL 2075 (commercial CO alarms)",
                "Tetanus immunization status per each household member's healthcare provider per current ACIP / CDC guidance",
                "The local AHJ adopted codes (NEC, IECC, IRC, IBC, local amendments) — vary by jurisdiction; the household identifies their AHJ's current adopted editions",
                "The household's employer's written lockout-tagout program (for an apprentice working under a contractor or vocational program)",
                "Manufacturer service literature for the specific equipment",
            ],
        },
    },
    "elc-001": {
        "node_type": "technique",
        "trade": "electrical",
        "competency_name": (
            "Read and interpret an electrical nameplate / rating label to extract voltage, "
            "current, power, frequency, phase, listing marks, AIC rating, and any "
            "circuit-protection specifications"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001"],
        "safety_basis": {
            "hazards": [
                (
                    "Misreading the voltage rating and applying the wrong meter range or the "
                    "wrong PPE downstream. Not a direct hazard at this band because the "
                    "reading is done with the cover closed, but a real downstream error if "
                    "the wrong number propagates to elc-021 or to any later energized work."
                ),
                (
                    "Misreading the current draw or full-load ampacity and concluding the "
                    "wrong conductor size or breaker size downstream. Not a direct hazard at "
                    "this band because no wiring is changed, but the wrong number compounds "
                    "in any later install (NEC Article 240, 310 — AHJ-adopted edition "
                    "governs)."
                ),
                (
                    "Misreading the AIC (ampere interrupting capacity) on a breaker or fuse "
                    "rating and concluding the device can safely interrupt the available "
                    "fault current at that location. The AIC is a critical safety rating; "
                    "a breaker with insufficient AIC for the available fault current can "
                    "explode during a short. This is not a direct hazard at the reading band "
                    "but is a critical downstream input for any breaker selection or panel "
                    "work in later batches."
                ),
                (
                    "Reaching into a panel or enclosure to find a hidden rating label. The "
                    "rule is the cover stays on at this band; any label not visible from "
                    "outside is photographed by a licensed electrician with the disconnect "
                    "open and verified dead per elc-021."
                ),
            ],
            "ppe_required": [
                (
                    "Trade PPE per els-001 (closed-toe shoes, the trade's general defaults); "
                    "no additional PPE required for reading a label visible from outside the "
                    "enclosure. Eye protection optional but recommended in a dusty mechanical "
                    "space."
                ),
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Reading a rating label visible from outside the enclosure involves no tool "
                "use, no opened enclosure, no live circuit contact, no moving parts, and no "
                "chemical or refrigerant exposure. The AI tutor mentors this competency "
                "end-to-end: the learner photographs the label, the AI confirms each "
                "extracted field, the learner builds a nameplate card. Trade-level "
                "supervision from el-root still applies in the sense that no enclosure is "
                "opened and no energized work is performed; the reading itself is "
                "low-hazard and AI-mentorable."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "A real electrical nameplate or rating label visible from outside the enclosure",
                "specification": (
                    "The household's actual equipment (the main panel's manufacturer label, "
                    "any subpanel labels, a breaker's amp / AIC marking, a receptacle's "
                    "amp / volt marking, a fixture's wattage / volt rating, an appliance's "
                    "nameplate, a transformer's rating label, a low-voltage adapter's input "
                    "and output ratings). The label is typically on the side or front of the "
                    "enclosure, on the breaker face, on the receptacle face, on the fixture "
                    "label, on the appliance back, or molded into the device housing. If the "
                    "household's equipment has its rating only inside an enclosure that "
                    "requires opening, the work is deferred to a session with a licensed "
                    "electrician present per the trade root's supervision policy."
                ),
                "alternatives": [
                    "A clear photograph of a rating label from the manufacturer's published "
                    "service literature, used as a learning aid",
                ],
            },
            {
                "name": "A nameplate card or notebook page",
                "specification": (
                    "A sheet of paper or a notebook page where the learner writes down each "
                    "operative field from the label. The card is the working reference for "
                    "every later step on that piece of equipment."
                ),
                "alternatives": [
                    "A structured digital form per the household's record-keeping practice; "
                    "the AI tutor can render the form",
                ],
            },
            {
                "name": "Camera (cell phone is sufficient)",
                "specification": (
                    "A camera that produces an image clear enough to read every printed "
                    "field. The photo is uploaded to the AI tutor for confirmation of each "
                    "extracted field."
                ),
                "alternatives": [],
            },
            {
                "name": "Flashlight or headlamp",
                "specification": (
                    "Panel labels and equipment labels are commonly in shadow or behind "
                    "equipment. A flashlight is on the person for the visit."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Wherever the equipment is installed; the work is the visit itself",
            "ventilation": "Adequate per els-001",
            "lighting": "Daylight, room lighting, or flashlight as needed",
            "power": (
                "Energy state immaterial for reading a label visible from outside the "
                "enclosure; no enclosure opened at this band"
            ),
            "containment": "None required",
        },
        "skill_description": (
            "The learner visits a piece of electrical equipment in the household and "
            "locates the rating label without opening any enclosure. The label is typically "
            "on the side or front of the enclosure, on a breaker face, on a receptacle "
            "face, on a fixture label, or on an appliance nameplate. The learner "
            "photographs the label clearly and reads each operative field onto a nameplate "
            "card. The fields read across the kinds of equipment in scope: panel and "
            "subpanel labels (manufacturer, model, series, voltage rating, current rating "
            "in amps, AIC short-circuit rating, listing marks UL/ETL/CSA, neutral and "
            "ground busbar configuration, date code if present); breaker labels (amp "
            "rating, voltage rating, AIC, single- or two-pole, GFCI or AFCI marking if "
            "present, manufacturer and series); receptacle labels (amp rating typically 15A "
            "or 20A, voltage typically 125V or 250V, NEMA configuration, GFCI or AFCI "
            "marking, listing); fixture labels (input voltage, wattage, replacement-lamp "
            "type and wattage, listing, damp- or wet-location rating); appliance nameplates "
            "(voltage, full-load amps, watts or kilowatts, frequency, phase, "
            "manufacturer/model/serial, listing); transformer labels (primary and "
            "secondary voltage, kVA rating, primary and secondary current); low-voltage "
            "adapter labels (input voltage and frequency, output voltage and current, "
            "polarity marking). The learner then submits the nameplate card and the "
            "photograph to the AI tutor for field-by-field confirmation. If any field is "
            "missing, illegible, or unfamiliar, the learner names it on the card and the "
            "AI tutor explains what the field typically represents and where the "
            "manufacturer's service literature or the AHJ-adopted code defines it. The "
            "card is filed with the household's equipment records and travels with the "
            "learner for every later session on that equipment."
        ),
        "demonstration_criteria": [
            (
                "Locates a rating label on each of: a panel, a breaker, a receptacle, a "
                "fixture, an appliance, and (where applicable) a low-voltage adapter, "
                "without opening any enclosure"
            ),
            (
                "Photographs each label clearly enough that every printed field is legible "
                "in the image"
            ),
            (
                "Extracts every operative field onto a nameplate card: voltage rating, "
                "current rating (amps), wattage or kilowatts (where present), frequency, "
                "phase, AIC (where present), manufacturer / model / series / serial, "
                "listing marks (UL / ETL / CSA), location rating (dry / damp / wet, where "
                "present), GFCI / AFCI marking (where present)"
            ),
            (
                "Submits each card and photograph to the AI tutor; AI tutor confirms each "
                "field or names a discrepancy; learner reconciles"
            ),
            (
                "Names which fields the label did not supply (some fields are not on every "
                "label; the AI tutor confirms which are normal omissions and which would "
                "warrant looking up the manufacturer's service literature)"
            ),
            (
                "Names what the AIC field on a breaker means in plain language: the "
                "maximum short-circuit current the breaker is rated to safely interrupt; "
                "names that a breaker installed in a system where the available fault "
                "current exceeds the breaker's AIC is a documented cause of explosion "
                "during a fault, and that AIC selection is licensed-electrician work per "
                "the AHJ"
            ),
            (
                "Names the listing-mark requirement: equipment intended for installation in "
                "the electrical system carries a listing mark from a recognized testing "
                "laboratory (UL, ETL, CSA, others recognized by OSHA as Nationally "
                "Recognized Testing Laboratories); unlisted equipment is not used per the "
                "AHJ-adopted NEC"
            ),
            (
                "Reads three different rating labels across three different equipment types "
                "(at minimum one panel or breaker, one receptacle, one fixture or "
                "appliance) and submits a complete card for each"
            ),
        ],
        "common_errors": [
            {
                "error": "Reading the voltage as a single number when the label shows a range",
                "cause": "Some labels print '120/240V' meaning the unit will operate on either; the learner picked one number",
                "remedy": (
                    "Record the label as printed. The actual supply voltage is measured "
                    "later under elc-021; the label range tells what the equipment will "
                    "accept."
                ),
            },
            {
                "error": "Confusing amp rating with AIC",
                "cause": "Both are amp values on a breaker label and may sit near each other",
                "remedy": (
                    "Amp rating is the continuous-load current the breaker will pass before "
                    "tripping (typically 15A, 20A, 30A, etc. on residential branch "
                    "breakers). AIC (or 'Interrupting Rating' or 'kAIC') is the maximum "
                    "short-circuit current the breaker can safely interrupt (typically 10kA "
                    "or higher; the AHJ-adopted NEC governs minimum required AIC for "
                    "available fault current). They are labeled differently; the AI tutor "
                    "confirms the labeling per the specific manufacturer."
                ),
            },
            {
                "error": "Opening an enclosure to find a label",
                "cause": "The visible label was missing or illegible and the learner reached inside",
                "remedy": (
                    "The cover stays on at this band. If the visible label is missing or "
                    "illegible, the work is deferred to a session with a licensed "
                    "electrician present who opens the enclosure under elc-021 and "
                    "photographs the internal label."
                ),
            },
            {
                "error": "Skipping the listing mark and the location rating on a fixture",
                "cause": "The learner read voltage and wattage and moved on",
                "remedy": (
                    "The listing mark is the safety-certification check; the location "
                    "rating tells whether the fixture is approved for dry, damp, or wet "
                    "installation. A fixture in a bathroom or outdoors that is rated for "
                    "dry-only is an AHJ violation and a safety hazard. Read every printed "
                    "field."
                ),
            },
            {
                "error": "Treating a low-voltage adapter rating as the device's primary rating",
                "cause": "The learner read the small print on a wall wart and reported it as the appliance's rating",
                "remedy": (
                    "Low-voltage adapters have an input rating (typically 120VAC, 60Hz, in "
                    "the US) and an output rating (the DC or low-voltage AC that powers the "
                    "device). The adapter's output rating is the input to the downstream "
                    "device. Read both and write both on the card."
                ),
            },
            {
                "error": "Confusing 'amps' with 'amp-hours' on a battery-backed system",
                "cause": "The learner saw 'Ah' and recorded it as amps",
                "remedy": (
                    "Amps (A) is current; amp-hours (Ah) is battery capacity. They are not "
                    "interchangeable. The AI tutor confirms the unit on the photo."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "A series of nameplate cards (one per piece of equipment), each accompanied "
                "by the clear photograph of the corresponding rating label, with every "
                "operative field filled in on the card in the learner's handwriting (or "
                "typed in the household's record system). At minimum: one panel or "
                "breaker, one receptacle, and one fixture or appliance."
            ),
            "what_the_evidence_shows": (
                "That the learner extracted every operative field from each label, that "
                "the AI tutor confirmed each field, and that any unfamiliar field was "
                "named on the card and resolved with the AI tutor's lookup against the "
                "manufacturer's service literature"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a sample rating-label photograph "
                "(provided by the AI), naming each field aloud, pointing out the typical "
                "layout (manufacturer top, model and series next, electrical specs grouped, "
                "listing marks bottom), and explaining what each field is for and where it "
                "will be used in later competencies. The AI explicitly names the AIC field "
                "and the listing-mark requirement."
            ),
            "we_do": (
                "The AI tutor and the learner work through a second sample label together. "
                "The learner names a field; the AI confirms or corrects; the next field is "
                "the AI's, then back to the learner. At the end the learner reads the "
                "whole card back."
            ),
            "you_do_supervised": (
                "The learner visits the household's actual equipment, photographs each "
                "rating label, and reads it onto a card. The card and photograph are "
                "submitted to the AI tutor for field-by-field confirmation. The AI tutor "
                "names any discrepancy and the learner reconciles. The supervising adult "
                "is on premises only for the visit itself (because the learner is in the "
                "mechanical space); the AI mentors the actual reading."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce three accurate nameplate cards across at "
                "least two sessions, they may read labels unsupervised. The AI tutor "
                "remains available for field confirmation; this is not a supervision rule, "
                "it is a double-check rule that stays in place across bands."
            ),
        },
        "estimated_practice_sessions_to_signoff": 3,
        "session_length_minutes": 30,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency the AI tutor mentors end-to-end. Foundational across "
                "every credential the trade builds toward; the rating label is the first "
                "thing read on every service call."
            ),
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "AIC selection per the AHJ-adopted NEC's interrupting-rating "
                        "requirements",
                        "voltage and current ratings used in load calculations per NEC",
                        "listing requirement per NEC for equipment used in the system",
                    ],
                    "notes": (
                        "The journeyman exam tests reading and applying nameplate values "
                        "into load calculations and AIC selection."
                    ),
                },
                {
                    "id": "elcert-licensing",
                    "domains": [
                        "nameplate literacy across the residential equipment scope of the "
                        "state license",
                    ],
                    "notes": "Foundational across every state licensing exam.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-002": {
        "node_type": "technique",
        "trade": "electrical",
        "competency_name": (
            "Identify residential electrical components from diagrams and with covers closed: "
            "service entrance, panel, branch-circuit devices, grounding electrode system, "
            "and low-voltage components"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001"],
        "safety_basis": {
            "hazards": [
                (
                    "Reaching toward an energized busbar or breaker terminal while "
                    "'identifying' inside a panel. The rule is the cover stays on at this "
                    "band; identification is performed visually from outside the enclosure, "
                    "from diagrams, and from photographs the licensed electrician has taken "
                    "with the panel verified dead per elc-021."
                ),
                (
                    "Touching a receptacle, switch, fixture base, or junction box cover "
                    "with bare hands while the circuit is energized. Identification at this "
                    "band is visual only with cover closed; bare-hand contact is acceptable "
                    "for cover identification only when the cover is intact and unbroken "
                    "and the device is undamaged."
                ),
                (
                    "Operating a breaker, disconnect, or switch as part of identification. "
                    "The rule is no operation at this band; identification is identification "
                    "only. Operating any device is part of elc-021 with the licensed "
                    "electrician present."
                ),
                (
                    "Misidentifying a component on a diagram and propagating the error to a "
                    "later step. Not a direct hazard at this band, but a real downstream "
                    "error if the wrong component identity is used in elc-021 or later."
                ),
                (
                    "Misreading a schematic symbol and confusing series for parallel, or "
                    "confusing the equipment grounding conductor for a current-carrying "
                    "neutral. Not a direct hazard at this band but a foundational "
                    "literacy error that compounds in elc-005 (schematic reading) and "
                    "every downstream competency."
                ),
                (
                    "Slip or trip hazards in panel rooms, basements, and behind appliances "
                    "where the equipment lives. Tools and equipment in walkways are real "
                    "hazards; the rule is no tools on the floor in path lines."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001 (closed-toe shoes, the trade's general defaults)",
                "Safety glasses for any close inspection inside a panel room or attic",
                (
                    "Bare hands acceptable for identifying intact covers, intact receptacle "
                    "faces, and intact switch faces; cut-resistant gloves on if any "
                    "handling of damaged or sharp covers is anticipated"
                ),
                "No metal jewelry on hands or wrists near panels or distribution equipment",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Visual identification with the cover closed and no enclosure opening "
                "involves no tool use, no live circuit contact, no disconnect operation, "
                "and no rotating equipment contact. The AI tutor mentors this competency "
                "end-to-end: the learner photographs each component (with the enclosure "
                "cover closed; the cover is opened only under elc-021 with a licensed "
                "electrician present, which is a different competency), and the AI "
                "confirms each identification. Trade-level supervision from el-root still "
                "applies in the sense that no enclosure is opened and no energized work "
                "is performed."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "The household's actual residential electrical service",
                "specification": (
                    "The household's main panel (cover closed), any subpanels (cover "
                    "closed), branch-circuit devices (receptacles, switches, fixtures, "
                    "junction-box covers, all intact and cover-closed), grounding "
                    "electrode system (where visible: ground rod, water-pipe bond if "
                    "accessible), and any low-voltage components (doorbell transformer, "
                    "thermostat at the wall, security panel, smoke / CO alarms). "
                    "Identification is from outside the enclosure only."
                ),
                "alternatives": [
                    "Clear photographs of a residential service from manufacturer or "
                    "published-textbook documentation, used as a learning aid when the "
                    "household's equipment is not accessible",
                ],
            },
            {
                "name": "A residential one-line diagram (or a sample residential diagram from a recognized publisher)",
                "specification": (
                    "A one-line diagram or schematic of a residential electrical service "
                    "the learner can study. The AI tutor provides sample diagrams matched "
                    "to the household's actual service configuration where possible."
                ),
                "alternatives": [
                    "A reproducible sample diagram from a recognized educational publisher",
                ],
            },
            {
                "name": "A residential schematic-symbol reference",
                "specification": (
                    "A standard reference of the electrical schematic symbols used on "
                    "residential one-line and wiring diagrams (switch, receptacle, "
                    "fixture, ground, ungrounded / hot conductor, grounded / neutral "
                    "conductor, equipment grounding conductor, breaker, fuse, motor, "
                    "transformer, GFCI, AFCI, smoke detector). The AI tutor provides the "
                    "reference."
                ),
                "alternatives": [],
            },
            {
                "name": "Camera (cell phone is sufficient)",
                "specification": (
                    "A camera that produces images clear enough to identify components in "
                    "the AI tutor's review."
                ),
                "alternatives": [],
            },
            {
                "name": "Component identification card or notebook",
                "specification": (
                    "A sheet or notebook page listing each named component with its "
                    "function in one sentence as the learner identifies it. The card "
                    "travels with the learner across later sessions on that equipment."
                ),
                "alternatives": [],
            },
            {
                "name": "Flashlight or headlamp",
                "specification": "Panel rooms, basements, and attics are commonly dark; a flashlight is on the person",
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Wherever the equipment is installed; the work is the visit itself",
            "ventilation": "Per els-001 for the space",
            "lighting": "Daylight, room lighting, or flashlight as needed",
            "power": (
                "Energy state immaterial for cover-closed visual ID; for any "
                "cover-removed view, the disconnect is verified open under elc-021 by a "
                "licensed electrician (a different competency)"
            ),
            "containment": "None required",
        },
        "skill_description": (
            "The learner visits the household's residential electrical service and "
            "identifies each major component by sight with all enclosure covers closed, "
            "and identifies the corresponding component on a one-line diagram or "
            "schematic. The learner photographs each component and writes its name and "
            "function in one sentence on an ID card. The components, in order from the "
            "utility inward: weatherhead or service lateral (the entrance point of the "
            "supply conductors); meter (the utility's metering enclosure); main "
            "disconnect (the breaker or switch that de-energizes the entire service); "
            "main panel (the enclosure containing the main disconnect on combination "
            "panels, and the branch-circuit breakers); subpanels if any (downstream "
            "panels fed from the main, with their own neutral and ground busbars "
            "isolated per the AHJ-adopted NEC); branch-circuit breakers (the "
            "individual-circuit overcurrent devices); the neutral busbar and the ground "
            "busbar inside the panel (covers closed; identified from manufacturer "
            "diagrams and from the panel's published one-line layout); the "
            "neutral-to-ground bond (located at the main service equipment ONLY per the "
            "AHJ-adopted NEC); branch-circuit cables exiting the panel (NM, MC, AC, "
            "conduit-and-wire as applicable; identified by the visible sheathing or "
            "raceway); junction boxes along the circuit (covers closed; identified by "
            "the visible box and cover); receptacles (standard duplex, GFCI, AFCI, "
            "tamper-resistant where required by the AHJ-adopted NEC); switches (single-"
            "pole, three-way, four-way, dimmer); fixtures (ceiling, wall, fluorescent, "
            "LED); the grounding electrode system (ground rod or rods, water-pipe bond "
            "if accessible, intersystem bonding termination if present); low-voltage "
            "components (doorbell transformer typically mounted on the panel exterior or "
            "in the basement; thermostat at the wall; smoke and CO alarms; security and "
            "communication panels). On the schematic / one-line side, the learner "
            "matches each physical component to its standard symbol and names the "
            "convention (ungrounded conductor is hot; grounded conductor is neutral; "
            "equipment grounding conductor is the bare or green wire; the bond between "
            "neutral and ground exists at the main service equipment only)."
        ),
        "demonstration_criteria": [
            (
                "Names every visible exterior component of the residential service from "
                "outside the enclosure: weatherhead or service-lateral entry, meter, "
                "main disconnect location, main-panel exterior, any subpanel exterior, "
                "grounding electrode system (where visible)"
            ),
            (
                "Names every visible branch-circuit and low-voltage component from "
                "outside the enclosure: receptacles (standard, GFCI by face marking, "
                "AFCI by face marking, tamper-resistant by face marking), switches "
                "(single-pole, three-way by appearance), fixtures (by mounting and "
                "lamp type), junction-box covers, doorbell transformer, thermostat, "
                "smoke and CO alarms"
            ),
            (
                "Matches each physical component identified above to its standard "
                "symbol on a residential one-line diagram or schematic; the AI tutor "
                "confirms each match"
            ),
            (
                "Names the conventions: ungrounded conductor (hot) is typically black "
                "or red insulation; grounded conductor (neutral) is white insulation; "
                "equipment grounding conductor is bare or green; identifies these on a "
                "diagram and (where the household has accessible visible conductors at "
                "a fixture or device after the licensed electrician has verified dead) "
                "on the real wiring"
            ),
            (
                "Names that the neutral-to-ground bond exists at the main service "
                "equipment ONLY per the AHJ-adopted NEC, and that subpanels must have "
                "their neutral and ground busbars isolated; demonstrates locating where "
                "the bond would be in a one-line diagram"
            ),
            (
                "Names that all access panels and covers are NOT opened at this band; "
                "opening any cover is part of elc-021 with the licensed electrician "
                "physically present"
            ),
            (
                "Names that switches, breakers, and disconnects are NOT operated at "
                "this band; operating any device is part of elc-021"
            ),
            (
                "Photographs each component and matches each to the diagram; submits "
                "the ID card and photographs to the AI tutor; AI tutor confirms each "
                "identification"
            ),
            (
                "Names the standard cable types likely in the household's service "
                "(NM-B nonmetallic-sheathed cable for residential branch circuits, "
                "MC armored cable in some installations, conduit-and-wire in service "
                "or feeder runs); identifies the visible cable type at the panel exit "
                "without contacting the cable"
            ),
        ],
        "common_errors": [
            {
                "error": "Trying to identify breaker busbar or neutral busbar by opening the panel cover",
                "cause": "The learner expected the components named in the description to be visible inside",
                "remedy": (
                    "The cover stays on at this band. Internal panel components are "
                    "identified from manufacturer diagrams, from the panel's published "
                    "one-line layout, and from photographs the licensed electrician took "
                    "during a prior verified-dead session per elc-021."
                ),
            },
            {
                "error": "Operating a breaker as part of 'identifying' which circuit it controls",
                "cause": "The learner thought turning the breaker would help identify the circuit",
                "remedy": (
                    "Operating a breaker is elc-021 work, not elc-002 work. Identifying "
                    "the circuit a breaker controls is part of the apprentice band with "
                    "the licensed electrician present, who performs the live-dead-live "
                    "verification at the work point. Trust no panel label at the work "
                    "point regardless."
                ),
            },
            {
                "error": "Misidentifying the equipment grounding conductor on a diagram",
                "cause": "The learner read the schematic symbol for ground as if it were a neutral",
                "remedy": (
                    "The equipment grounding conductor symbol is distinct from the "
                    "neutral symbol; the AI tutor confirms on the diagram. The learner "
                    "memorizes the standard symbol set; it is the basis of elc-005 "
                    "schematic reading."
                ),
            },
            {
                "error": "Treating the neutral as 'safe to touch' on a diagram exercise",
                "cause": "The learner thought neutral being at ground potential meant safe contact",
                "remedy": (
                    "Even on a paper exercise, the rule is the same as on real equipment: "
                    "the neutral is a current-carrying conductor whenever the circuit is "
                    "energized, and is not contacted hands-on without verification per "
                    "elc-021. The rule is the safety habit; it is practiced in the "
                    "diagram exercise."
                ),
            },
            {
                "error": "Confusing a subpanel's neutral and ground busbars",
                "cause": "The learner did not know subpanels must have neutral and ground isolated",
                "remedy": (
                    "Per the AHJ-adopted NEC, the neutral-to-ground bond exists at the "
                    "main service equipment only; subpanels have a separate ground "
                    "busbar bonded to the enclosure and a separate neutral busbar "
                    "ISOLATED from the enclosure. The AI tutor confirms on the diagram "
                    "and explains the failure mode if the bond is duplicated at a "
                    "subpanel (parallel return paths via grounding conductors, potential "
                    "shock on metal equipment)."
                ),
            },
            {
                "error": "Treating a 'GFCI receptacle' face as if it protected the entire circuit",
                "cause": "The learner did not know a GFCI receptacle has LINE and LOAD terminals",
                "remedy": (
                    "A GFCI receptacle protects itself and any downstream receptacles "
                    "wired to its LOAD terminals; receptacles wired ahead of it (on the "
                    "LINE side) are NOT protected. The AHJ-adopted NEC governs which "
                    "circuits require GFCI protection. The learner will revisit this at "
                    "apprentice band; at this band the rule is identification by face "
                    "marking only."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "A series of photographs of the household's electrical service and "
                "branch-circuit components, each accompanied by a card naming the "
                "component, its function in one sentence, and the matching standard "
                "schematic symbol. At minimum: the main panel exterior, the meter, two "
                "branch-circuit components of different kinds (receptacle, switch, "
                "fixture, or junction-box cover), and one low-voltage component "
                "(doorbell, thermostat, smoke / CO alarm). The cards and photographs "
                "are submitted to the AI tutor for field-by-field confirmation."
            ),
            "what_the_evidence_shows": (
                "That the learner identified each visible component correctly, matched "
                "each to its standard schematic symbol, distinguished hot / neutral / "
                "ground conventions, and named which components and operations are in "
                "band and which are gated for later"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a sample residential one-line "
                "diagram and the corresponding photographs (provided by the AI), "
                "naming each component aloud, pointing out the distinguishing features "
                "(GFCI vs standard receptacle by face marking, three-way switch by "
                "toggle and screw count, etc.), and naming which components are "
                "external and which are internal."
            ),
            "we_do": (
                "The AI tutor and the learner work through a second sample together. "
                "The learner names a component; the AI confirms or corrects; the next "
                "component is the AI's, then back to the learner. At the end the "
                "learner reads the whole ID card back."
            ),
            "you_do_supervised": (
                "The learner visits the household's actual service, photographs each "
                "component, writes the name and function on the card, and matches each "
                "to the schematic symbol on the reference. Submits to the AI tutor for "
                "confirmation. The supervising adult is on premises only for the visit "
                "itself; the AI mentors the actual identification."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce accurate ID cards across the household's "
                "service and the schematic-symbol match across at least two sessions, "
                "they may identify components on new services unsupervised. The AI "
                "tutor remains available for component confirmation; this is not a "
                "supervision rule, it is a double-check rule that stays in place across "
                "bands."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 45,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency the AI tutor mentors end-to-end. Visual literacy "
                "of the residential service and schematic-symbol fluency are "
                "foundational across every credential."
            ),
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "the residential one-line as the basis of the NEC's Chapter 2 "
                        "wiring and protection requirements",
                        "service-equipment vs subpanel neutral-to-ground bond rules per "
                        "the AHJ-adopted NEC",
                        "GFCI / AFCI required locations per the AHJ-adopted NEC",
                    ],
                    "notes": (
                        "The journeyman exam tests reading and applying the residential "
                        "one-line and the symbol set."
                    ),
                },
                {
                    "id": "elcert-licensing",
                    "domains": [
                        "component identification across the residential scope of the "
                        "state license",
                    ],
                    "notes": "Foundational across every state licensing exam.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-003": {
        "node_type": "knowledge",
        "trade": "electrical",
        "competency_name": (
            "Ohm's law and basic DC and AC-resistive circuit theory: voltage, current, "
            "resistance, and power"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001"],
        "safety_basis": {
            "hazards": [
                (
                    "Misapplying Ohm's law and concluding the wrong current draw for a "
                    "stated voltage and resistance, or the wrong load wattage for a "
                    "stated current and voltage. Not a direct hazard at this band (pure "
                    "paper work), but a real downstream error if the wrong calculation "
                    "propagates into elc-004 load calculation, elc-007 ampacity, or any "
                    "later install."
                ),
                (
                    "Treating Ohm's law as the only equation needed for AC circuits. "
                    "Ohm's law (V = I R) applies to purely resistive AC loads (heaters, "
                    "incandescent bulbs); inductive loads (motors, transformers, "
                    "fluorescent ballasts, LED drivers with non-unity power factor) "
                    "introduce reactance and a power factor below 1, where apparent "
                    "power (V x I in volt-amps) differs from real power (in watts). Not "
                    "a direct hazard at this band but a foundational distinction; the "
                    "AI tutor introduces real / reactive / apparent power and power "
                    "factor at this band and the AHJ-adopted NEC's load-calculation "
                    "rules govern downstream."
                ),
                (
                    "Mistaking voltage for the cause of injury. Voltage is the driving "
                    "force; CURRENT through the body is what causes injury or death. A "
                    "few hundred milliamps across the heart at 60 Hz can fibrillate. The "
                    "rule the learner takes from elc-003 into elc-021 is that any "
                    "voltage capable of pushing dangerous current through the body's "
                    "resistance is dangerous, and residential 120V at hand-to-hand "
                    "contact CAN push that current."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001; no additional PPE required for paper work",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Pure conceptual work with paper, calculator, and the AI tutor's "
                "interactive problem set. No real equipment, no live circuits, no tool "
                "use. AI tutor mentors end-to-end: the learner solves problems, the AI "
                "confirms answers, names misconceptions, and re-quizzes where needed."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Pencil, paper, and a calculator",
                "specification": "A real calculator (handheld or phone) capable of basic arithmetic, division, and a square root function",
                "alternatives": [],
            },
            {
                "name": "A reference card for Ohm's law and the power equations",
                "specification": (
                    "A card or printout showing V = I R, P = V I, P = I^2 R, P = V^2 / R, "
                    "and the Ohm's-law triangle / power-rose. The AI tutor provides one."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Any flat surface (desk or table); the work is paper and arithmetic",
            "ventilation": "Indoor or outdoor; not relevant",
            "lighting": "Adequate to read calculator and paper",
            "power": "None required (handheld calculator); a phone calculator works",
            "containment": "None required",
        },
        "skill_description": (
            "The learner builds a working command of the fundamental electrical "
            "relationships. Voltage (V, volts) is the potential difference that drives "
            "current through a conductor; current (I, amperes) is the rate of charge "
            "flow; resistance (R, ohms) is the opposition to current flow; power (P, "
            "watts) is the rate at which electrical energy is converted to heat, light, "
            "motion, or other forms. Ohm's law states V = I R; equivalently I = V / R "
            "and R = V / I. Power has three forms derived from Ohm's law: P = V I (the "
            "general form for purely resistive circuits), P = I^2 R (useful when the "
            "current and resistance are known), P = V^2 / R (useful when the voltage and "
            "resistance are known). The learner solves problems of all six rearrangements "
            "(V from I and R; I from V and R; R from V and I; P from V and I; P from I "
            "and R; P from V and R). The learner names the units: volts, amperes, ohms, "
            "watts, milliamperes, kilowatts, kilo-ohms. The learner names that current "
            "(not voltage) is what causes injury in the human body, and that 120V "
            "residential is fully capable of pushing fatal current at hand-to-hand "
            "contact through normal skin resistance, particularly when the skin is wet "
            "or broken. The learner is introduced to the distinction between purely "
            "resistive AC loads (where Ohm's law applies directly) and inductive AC "
            "loads (motors, transformers, fluorescent ballasts, switched-mode LED "
            "drivers and power supplies, where reactance enters and the power factor is "
            "below 1); apparent power in volt-amps (S = V I), real power in watts (P = "
            "V I cos(theta) where theta is the phase angle), and power factor (PF = "
            "cos(theta) = P / S) are named at the introductory level, with deeper "
            "treatment reserved for the apprentice band."
        ),
        "demonstration_criteria": [
            (
                "Given any two of V, I, R, computes the third using Ohm's law correctly "
                "across at least ten problems spanning DC and AC-resistive cases"
            ),
            (
                "Given any combination of two of V, I, R, computes power P correctly "
                "using the appropriate form (V I, I^2 R, or V^2 / R) across at least "
                "five problems"
            ),
            (
                "Uses correct units in every answer (volts, amperes, ohms, watts) and "
                "uses sensible engineering prefixes (milliamperes for small currents, "
                "kilowatts for large loads, kilo-ohms for high resistances)"
            ),
            (
                "Names that current (not voltage) is what causes injury in the human "
                "body, and explains in one sentence why this matters for the trade's "
                "safety habits"
            ),
            (
                "Names the distinction between purely resistive AC loads and inductive "
                "AC loads at the introductory level; names that apparent power (volt-"
                "amps) and real power (watts) are not the same for inductive loads, "
                "and that the power factor is the ratio of real to apparent power"
            ),
            (
                "Solves three short word problems involving real residential equipment "
                "(a 120V hair dryer at 1500W: what is the current draw?; a 240V "
                "electric range at 40A: what is the wattage at unity power factor?; a "
                "9V battery driving a 100-ohm resistor: what is the current?)"
            ),
            (
                "Catches at least one unreasonable answer in a set by sanity-checking "
                "against expected residential values (a 120V lamp drawing 100A is "
                "wrong; a kitchen receptacle on a 15A circuit can support no more than "
                "1800W at unity PF)"
            ),
        ],
        "common_errors": [
            {
                "error": "Computing power as V x R or I x R instead of V x I",
                "cause": "The learner mixed up the variables in the power equation",
                "remedy": (
                    "Power is V x I in the general form. The other two forms (I^2 R "
                    "and V^2 / R) are derived by substituting Ohm's law into V x I. "
                    "The reference card carries all three forms; the AI tutor confirms "
                    "the substitution."
                ),
            },
            {
                "error": "Forgetting the units, or using inconsistent units (mixing milliamperes with amperes in the same calculation)",
                "cause": "The learner did the arithmetic without tracking units",
                "remedy": (
                    "Every answer carries its unit. When using a sub-unit (milliampere, "
                    "kilo-ohm), convert to the base unit before applying Ohm's law, OR "
                    "use the matched sub-unit consistently (V = milliamperes x "
                    "kilo-ohms is dimensionally correct for V in volts because the "
                    "milli and kilo cancel). The AI tutor names the convention."
                ),
            },
            {
                "error": "Assuming Ohm's law applies to a motor or LED driver",
                "cause": "The learner read the device's voltage and current rating and applied V = I R as if there were a single fixed R",
                "remedy": (
                    "Motors, transformers, fluorescent ballasts, and switched-mode LED "
                    "drivers and power supplies do NOT present a fixed resistance; "
                    "their current draw at a given voltage depends on the load they "
                    "are driving and on reactance / power-factor effects. For these "
                    "loads, the device's NAMEPLATE current at the rated voltage is "
                    "the authoritative value (per elc-001), not Ohm's law applied to "
                    "a calculated resistance."
                ),
            },
            {
                "error": "Treating voltage as the cause of injury",
                "cause": "The learner heard 'high voltage' and conflated voltage with danger",
                "remedy": (
                    "Voltage is the driving force; CURRENT through the body is what "
                    "injures and kills. Across the heart, a few hundred milliamperes "
                    "at 60 Hz can fibrillate. 120V household voltage is fully capable "
                    "of pushing that current through normal skin resistance, "
                    "especially when wet or broken. This is the safety habit elc-003 "
                    "carries into elc-021."
                ),
            },
            {
                "error": "Confusing apparent power (VA) with real power (W) for inductive loads",
                "cause": "The learner multiplied volts and amps and called it watts",
                "remedy": (
                    "For a purely resistive load (heater, incandescent bulb), apparent "
                    "power (V x I in VA) equals real power (W). For an inductive load "
                    "(motor, transformer, fluorescent ballast, switched-mode supply), "
                    "real power is V x I x cos(theta) where theta is the phase angle, "
                    "and cos(theta) = power factor. Apparent power exceeds real power. "
                    "This affects load calculations at the apprentice band; at this "
                    "band the rule is name the distinction and reach for the nameplate."
                ),
            },
            {
                "error": "Forgetting that resistance varies with temperature",
                "cause": "The learner used a cold-resistance value at operating temperature",
                "remedy": (
                    "Conductor resistance rises with temperature; an incandescent "
                    "filament has a much higher resistance hot than cold. For "
                    "introductory problems, the AI tutor names the temperature at "
                    "which a resistance value is taken; for downstream conductor-"
                    "sizing work (elc-007), the AHJ-adopted NEC tables provide the "
                    "correct temperature-rated values."
                ),
            },
        ],
        "artifact_expected": {
            "type": "document",
            "what_to_capture": (
                "A worked problem set: at least 10 Ohm's law problems and 5 power "
                "problems, each with units, with the learner's work shown and the AI "
                "tutor's confirmation of each answer; plus three real-residential-"
                "equipment word problems worked end-to-end"
            ),
            "what_the_evidence_shows": (
                "That the learner can apply V = I R and P = V I (and derivatives) "
                "across the full set of rearrangements with correct units, and can "
                "sanity-check answers against expected residential values"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through Ohm's law and the power "
                "equation with worked examples: starting with simple DC (a 9V battery "
                "driving a 100-ohm resistor), then resistive AC (a 120V incandescent "
                "bulb at 60W), then a residential example (a 1500W hair dryer on a "
                "120V circuit). Names the units, the rearrangements, and the sanity-"
                "check habit."
            ),
            "we_do": (
                "The AI tutor and the learner alternate problems. The AI poses; the "
                "learner solves and names the units; the AI confirms or corrects. The "
                "AI introduces the apparent / real / power-factor distinction once "
                "Ohm's law is solid for resistive cases."
            ),
            "you_do_supervised": (
                "The learner solves a 10-problem Ohm's law set and a 5-problem power "
                "set independently, then submits to the AI tutor. The AI tutor "
                "confirms each answer; on any miss, the AI names the misconception "
                "and re-quizzes a similar problem."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce a complete and correct problem set "
                "across at least two sessions, they may continue to work problems "
                "unsupervised. The AI tutor remains available for confirmation and "
                "for the apprentice-band deeper treatment of AC theory."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 30,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency the AI tutor mentors end-to-end. Ohm's law and "
                "the power equation are the foundation of every load calculation, "
                "every conductor-sizing decision, and every troubleshooting framework "
                "in the trade."
            ),
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "load calculation (NEC Article 220) rests on Ohm's law and the "
                        "power equation",
                        "ampacity selection (NEC Article 310) uses the power and "
                        "current relationship",
                    ],
                    "notes": "Every NEC chapter touching loads and conductors assumes Ohm's-law fluency.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": [
                        "Ohm's law and basic circuit theory at the journeyman-exam depth",
                    ],
                    "notes": "Universal across every state licensing exam at the journeyman and master level.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-004": {
        "node_type": "knowledge",
        "trade": "electrical",
        "competency_name": (
            "Series and parallel circuits and basic residential load calculation"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001", "elc-003"],
        "safety_basis": {
            "hazards": [
                (
                    "Misapplying series rules to a parallel circuit (or vice versa) and "
                    "concluding the wrong current draw. Not a direct hazard at this band "
                    "(paper work), but a real downstream error if the wrong calculation "
                    "propagates into elc-007 ampacity or any later install."
                ),
                (
                    "Underestimating the load on a circuit by computing only the "
                    "nameplate-rated draw at unity power factor and missing inrush, "
                    "starting current, or non-unity power factor. Branch-circuit "
                    "breakers must hold the continuous load below the AHJ-adopted NEC's "
                    "80% continuous-load rule for non-100%-rated breakers. The "
                    "AHJ-adopted NEC's load-calculation rules (Article 220) govern."
                ),
                (
                    "Confusing voltage drop on a long branch with the supply voltage. A "
                    "long branch carrying significant current can drop several volts "
                    "from the panel to the load; the load sees less than nameplate "
                    "voltage and may overheat or run poorly. Voltage drop is treated "
                    "at this band as a concept; the AHJ-adopted NEC's voltage-drop "
                    "guidance applies in any install."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001; no additional PPE required for paper work",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Pure conceptual work with paper, calculator, and the AI tutor's "
                "interactive problem set. No real equipment, no live circuits. AI "
                "tutor mentors end-to-end."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Pencil, paper, and a calculator",
                "specification": "A real calculator capable of basic arithmetic and reciprocal operations",
                "alternatives": [],
            },
            {
                "name": "A reference card for the series and parallel circuit rules",
                "specification": (
                    "A card or printout showing the series rules (I same, V adds, R "
                    "adds), the parallel rules (V same, I adds, 1/R_total = sum of "
                    "1/R_i), and the 80% continuous-load rule for branch-circuit "
                    "breakers. The AI tutor provides one."
                ),
                "alternatives": [],
            },
            {
                "name": "Sample residential branch-circuit load lists",
                "specification": (
                    "Worked sample lists showing the kinds of loads typically on a "
                    "kitchen small-appliance branch, a bathroom branch, a general-"
                    "purpose room branch, a 240V dedicated branch (range, dryer, "
                    "electric water heater, etc.), provided by the AI tutor"
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Any flat surface (desk or table)",
            "ventilation": "Indoor or outdoor; not relevant",
            "lighting": "Adequate to read calculator and paper",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner extends Ohm's law and the power equation from a single "
            "resistor to networks of two or more loads. In a series circuit (loads "
            "wired end-to-end), the same current flows through every load; the "
            "voltage divides across the loads in proportion to their resistance; the "
            "total resistance is the sum of the individual resistances; if one load "
            "opens (e.g. a bulb burns out), the whole string goes dark. In a "
            "parallel circuit (loads wired across the same voltage), every load sees "
            "the full supply voltage; the total current is the sum of the individual "
            "currents; the total (equivalent) resistance is found by 1/R_total = "
            "1/R_1 + 1/R_2 + ... and is always less than the smallest individual "
            "resistance; if one load opens, the others continue. Residential branch "
            "circuits wire loads in PARALLEL (every receptacle on a branch sees 120V "
            "regardless of what else is plugged in); series wiring of household loads "
            "is uncommon and is mostly seen historically in old Christmas-light "
            "strings. The learner solves problems of both kinds. The learner then "
            "applies the series and parallel rules to a basic residential load "
            "calculation: list the loads on a branch (each in watts at the rated "
            "voltage), convert each to amperes at the branch voltage, sum the amps "
            "(since the loads are in parallel), and compare to the branch breaker's "
            "amp rating. The AHJ-adopted NEC governs the formal load-calculation "
            "rules (Article 220 in current editions); this band introduces the "
            "concept and the rules of thumb (the 80% continuous-load rule, the "
            "diversity / demand factors named at the introductory level), with "
            "deeper treatment reserved for the apprentice band."
        ),
        "demonstration_criteria": [
            (
                "Given a series circuit of two or three resistors and a supply "
                "voltage, computes total resistance, current, and voltage across "
                "each resistor correctly across at least three problems"
            ),
            (
                "Given a parallel circuit of two or three resistors and a supply "
                "voltage, computes total (equivalent) resistance, total current, and "
                "current through each branch correctly across at least three problems"
            ),
            (
                "Names that residential branch circuits wire receptacles, switches, "
                "and fixtures in PARALLEL (every device sees full supply voltage), "
                "and explains in one sentence why series wiring is uncommon (one "
                "open and everything stops)"
            ),
            (
                "Given a list of loads on a residential branch (e.g. a kitchen small-"
                "appliance branch: a 1500W toaster, a 1000W microwave, a 500W "
                "coffee maker), computes the total current draw at 120V and "
                "compares to a 20A breaker (the kitchen small-appliance standard per "
                "the AHJ-adopted NEC in many editions); names whether the load fits "
                "under the 80% continuous-load rule for a non-100%-rated breaker"
            ),
            (
                "Names voltage drop as a concept: a long branch carrying significant "
                "current drops voltage from the panel to the load; the load sees less "
                "than nameplate voltage. Names that the AHJ-adopted NEC publishes "
                "voltage-drop guidance for branch circuits and feeders, and that the "
                "actual voltage-drop calculation is part of the apprentice band's "
                "install work."
            ),
            (
                "Catches at least one unreasonable answer per problem set by sanity-"
                "check against expected residential values (a 120V branch with five "
                "1500W loads totals 7500W = 62A, which a 20A breaker cannot hold; the "
                "answer requires either fewer loads or a 240V dedicated circuit)"
            ),
        ],
        "common_errors": [
            {
                "error": "Adding parallel resistances directly (R_total = R_1 + R_2) instead of using the reciprocal formula",
                "cause": "The learner confused the series rule with the parallel rule",
                "remedy": (
                    "For parallel: 1/R_total = 1/R_1 + 1/R_2 + ... and then take the "
                    "reciprocal. For two equal resistors in parallel, R_total is half "
                    "of one (a useful sanity check). The AI tutor walks through the "
                    "reciprocal step explicitly."
                ),
            },
            {
                "error": "Computing total power as I_total x V (correct) but using R_total wrong in a derived form",
                "cause": "The learner used the parallel R_total in V^2 / R correctly but then added series resistances on a parallel problem",
                "remedy": (
                    "Solve for the equivalent resistance first, name which rule "
                    "applies (series adds, parallel reciprocal), then apply Ohm's "
                    "law. The AI tutor walks through both methods (sum the branch "
                    "currents vs use V^2 / R_total) and confirms they agree."
                ),
            },
            {
                "error": "Treating every receptacle on a branch as if it has its own breaker",
                "cause": "The learner did not internalize the parallel wiring of residential branches",
                "remedy": (
                    "One branch breaker protects every receptacle, switch, and "
                    "fixture wired in parallel on that branch. The breaker's amp "
                    "rating is the total current the branch can carry; the loads on "
                    "the branch share that ampacity. The AHJ-adopted NEC governs the "
                    "rules for what loads can share a branch."
                ),
            },
            {
                "error": "Forgetting the 80% continuous-load rule",
                "cause": "The learner sized the load at 100% of the breaker rating",
                "remedy": (
                    "For a non-100%-rated breaker (the residential default), a "
                    "continuous load (3 hours or more) is sized at 80% of the "
                    "breaker rating. A 20A breaker carries a continuous load of 16A "
                    "maximum. The AHJ-adopted NEC defines continuous load and the "
                    "specific exceptions; the rule of thumb is the standard starting "
                    "point at this band."
                ),
            },
            {
                "error": "Confusing volts and volt-amperes on a load list",
                "cause": "The learner treated VA as if it were V",
                "remedy": (
                    "Volts (V) is the voltage; volt-amperes (VA) is the apparent "
                    "power. They are unrelated units. The learner converts loads to "
                    "amps by dividing the load's wattage (or VA for inductive loads "
                    "with a published VA rating) by the branch voltage. The AI tutor "
                    "names this on every load-list problem."
                ),
            },
        ],
        "artifact_expected": {
            "type": "document",
            "what_to_capture": (
                "A worked problem set: three series problems, three parallel problems, "
                "and two basic residential load-calculation problems (one kitchen "
                "small-appliance branch, one 240V dedicated branch), each with "
                "answers in correct units and the 80%-rule check"
            ),
            "what_the_evidence_shows": (
                "That the learner can apply series and parallel rules correctly and "
                "can size a basic residential load against a branch breaker at the "
                "introductory level, with the 80% continuous-load rule applied where "
                "applicable"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a series example, then a "
                "parallel example, then a load-list example. Names the rules, the "
                "units, and the parallel-wiring fact for residential branches. "
                "Introduces the 80% continuous-load rule with a worked example."
            ),
            "we_do": (
                "The AI tutor and the learner alternate problems across the three "
                "kinds. The AI poses; the learner solves; the AI confirms or names "
                "the misconception."
            ),
            "you_do_supervised": (
                "The learner solves a complete problem set independently and submits "
                "to the AI tutor. The AI tutor confirms each answer; on any miss, "
                "the AI re-quizzes a similar problem."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce a complete and correct problem set "
                "across at least two sessions, they may continue unsupervised. The "
                "AI tutor remains available for the apprentice-band deeper treatment "
                "of NEC Article 220 load-calculation methods and voltage-drop "
                "calculation."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 30,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": "Knowledge competency. Foundational for NEC load-calculation work.",
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "NEC Article 220 (load calculations) rests on series/parallel "
                        "rules and the 80% continuous-load rule",
                        "branch-circuit sizing per the AHJ-adopted NEC",
                    ],
                    "notes": "Heavily tested on the journeyman exam.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": [
                        "circuit theory at journeyman depth; load-calculation methods",
                    ],
                    "notes": "Universal across every state licensing exam.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-005": {
        "node_type": "knowledge",
        "trade": "electrical",
        "competency_name": (
            "Read residential wiring diagrams and schematics: one-line diagrams, "
            "device-level wiring diagrams, and the standard symbol set"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001", "elc-002"],
        "safety_basis": {
            "hazards": [
                (
                    "Misreading a wiring diagram and concluding the wrong terminal is "
                    "LINE or LOAD on a device. Not a direct hazard at this band (paper "
                    "work), but a real downstream error in elc-021 and any later "
                    "install where the LINE / LOAD distinction governs whether "
                    "downstream protection is provided."
                ),
                (
                    "Mistaking the equipment grounding conductor symbol for the "
                    "neutral. Not a direct hazard at this band, but a foundational "
                    "literacy error that would result in dangerous wiring downstream."
                ),
                (
                    "Treating a diagram as authoritative when the AHJ-adopted NEC "
                    "edition (or local amendment) has changed the rule. Diagrams in "
                    "older textbooks or older manufacturer literature may not reflect "
                    "current code; the AHJ-adopted edition governs."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001; no additional PPE required for paper work",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Pure paper / on-screen diagram reading with the AI tutor. No real "
                "circuits, no live work. AI tutor mentors end-to-end."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "A standard residential schematic-symbol reference",
                "specification": (
                    "A reference of the standard symbols used on residential one-line "
                    "diagrams, schematics, and wiring diagrams (switch single-pole / "
                    "three-way / four-way / dimmer; receptacle standard / GFCI / AFCI / "
                    "tamper-resistant; fixture incandescent / fluorescent / LED; "
                    "breaker single-pole / two-pole; fuse; ground; ungrounded / hot "
                    "conductor; grounded / neutral conductor; equipment grounding "
                    "conductor; junction box; smoke / CO alarm with interconnect; "
                    "doorbell transformer). The AI tutor provides one."
                ),
                "alternatives": [],
            },
            {
                "name": "A library of sample residential wiring diagrams",
                "specification": (
                    "Sample diagrams for common residential circuits: a switched "
                    "receptacle, a single switched fixture, a three-way switched "
                    "fixture, a four-way switched fixture (where present), a GFCI "
                    "receptacle protecting downstream outlets (LINE and LOAD wiring), "
                    "an AFCI breaker with a branch circuit, interconnected smoke / CO "
                    "alarms, a doorbell with transformer and chime. Provided by the "
                    "AI tutor."
                ),
                "alternatives": [],
            },
            {
                "name": "Pencil and paper for tracing current paths",
                "specification": "Standard pencil and paper; the learner traces and annotates",
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Any flat surface (desk or table)",
            "ventilation": "Indoor or outdoor; not relevant",
            "lighting": "Adequate to read diagrams clearly",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner builds fluency in reading the three main kinds of electrical "
            "drawing used in residential work. A ONE-LINE (single-line) DIAGRAM shows "
            "the overall topology of the service: the utility supply, the meter, the "
            "main disconnect, the main panel, any subpanels, and the major branches, "
            "each represented as a single line and a standard symbol. A WIRING DIAGRAM "
            "shows the actual conductors and terminals at the device level, drawn as "
            "the conductors would actually be connected: the LINE-side wiring of a "
            "GFCI receptacle vs the LOAD-side wiring; the common, traveler, and load "
            "conductors of a three-way switched fixture; the interconnect terminal on "
            "a smoke/CO alarm. A SCHEMATIC shows the circuit's electrical function "
            "with standard symbols, often abstracted from the physical layout (mostly "
            "used in equipment-internal documentation rather than residential install "
            "drawings). The learner reads each of these for common residential "
            "circuits: a switched fixture from a single switch (a 'hot, neutral, "
            "ground' supply at the switch box, a switch leg up to the fixture, the "
            "neutral and ground traveling with); a three-way switched fixture (the "
            "common terminal of each switch, the two travelers between switches, the "
            "fixture's hot from one switch's common and neutral from the source); a "
            "GFCI receptacle's LINE and LOAD terminals and what each protects; an "
            "AFCI breaker protecting a branch from arcing faults per the AHJ-adopted "
            "NEC's required locations; a multiwire branch circuit (MWBC) with two "
            "hots from opposite phases sharing a single neutral; smoke and CO alarms "
            "with the interconnect terminal so all alarms sound when one detects. The "
            "learner traces current paths on each diagram by pencil, annotating "
            "ungrounded / grounded / equipment-grounding conductors and naming where "
            "the protection (breaker, GFCI, AFCI) lies. The learner names the "
            "convention for residential color coding (black or red insulation for hot; "
            "white for neutral; bare or green for equipment ground; the AHJ-adopted "
            "NEC governs specific cases including re-identification of conductors)."
        ),
        "demonstration_criteria": [
            (
                "Names every symbol on the standard residential reference card without "
                "prompting"
            ),
            (
                "Reads and annotates a single switched fixture diagram, naming the "
                "supply, the switch leg, the neutral, and the ground"
            ),
            (
                "Reads and annotates a three-way switched fixture diagram, naming the "
                "common terminal of each switch, the two travelers, and the load "
                "wiring; correctly traces the current path with the switch in each "
                "position"
            ),
            (
                "Reads and annotates a GFCI receptacle diagram, identifying the LINE "
                "and LOAD terminals and naming which receptacles downstream are "
                "protected and which (wired ahead of the LINE side) are NOT protected"
            ),
            (
                "Reads and annotates an AFCI breaker diagram and names that AFCI "
                "protects against arcing faults along the branch wiring, per the "
                "AHJ-adopted NEC's required locations"
            ),
            (
                "Reads and annotates a multiwire branch circuit (MWBC) diagram, "
                "naming the two hots from opposite phases, the shared neutral, and "
                "the rule that opening the neutral on an energized MWBC produces "
                "dangerous voltages (the safety habit elc-005 carries into elc-021)"
            ),
            (
                "Reads and annotates an interconnected smoke / CO alarm diagram, "
                "naming the interconnect terminal and explaining in one sentence "
                "why interconnect matters (when one alarm detects, all alarms sound)"
            ),
            (
                "Names the residential color-coding convention and the rule that the "
                "AHJ-adopted NEC governs re-identification of conductors (some "
                "circuits use a white conductor as a switch leg with re-"
                "identification by tape or paint)"
            ),
        ],
        "common_errors": [
            {
                "error": "Confusing the LINE and LOAD terminals on a GFCI receptacle",
                "cause": "The learner read the diagram without naming which side is the supply and which is the protected output",
                "remedy": (
                    "LINE = supply from the panel; LOAD = downstream receptacles to "
                    "be protected. Wiring the supply to LOAD terminals leaves the "
                    "GFCI inoperative and the downstream receptacles unprotected. The "
                    "AI tutor walks through both wiring methods (LINE-only and LINE-"
                    "plus-LOAD) and names the consequence of each error."
                ),
            },
            {
                "error": "Treating the white conductor as always neutral",
                "cause": "The learner read the color-coding rule without the re-identification exception",
                "remedy": (
                    "In some switch-leg configurations the AHJ-adopted NEC permits a "
                    "white conductor to be used as a hot when re-identified with "
                    "black tape, paint, or other permanent marking. The learner "
                    "names the rule and the rule that re-identification must be "
                    "present; the AHJ-adopted edition governs current requirements."
                ),
            },
            {
                "error": "Reading a three-way switch as if it had a single ON / OFF position",
                "cause": "The learner did not internalize the common-and-two-travelers configuration",
                "remedy": (
                    "A three-way switch has a common terminal and two travelers; "
                    "either traveler connects to the common as the toggle moves. The "
                    "AI tutor traces both positions and shows the current path for "
                    "each."
                ),
            },
            {
                "error": "Treating the equipment grounding conductor as if it carries current under normal operation",
                "cause": "The learner confused the equipment grounding conductor with the neutral",
                "remedy": (
                    "Under normal operation the equipment grounding conductor "
                    "carries NO current; it is a safety bond that carries fault "
                    "current to ground only when an insulation failure puts hot on "
                    "metal that should be at ground potential. The neutral carries "
                    "the return current during normal operation. These are different "
                    "conductors with different jobs."
                ),
            },
            {
                "error": "Trusting an older textbook diagram as if it reflected current code",
                "cause": "The learner did not check the publication date of the reference",
                "remedy": (
                    "AHJ-adopted NEC requirements evolve every 3-year cycle. The "
                    "diagram is correct conceptually but specific code-required "
                    "locations of GFCI, AFCI, tamper-resistant, and similar features "
                    "may differ from the diagram's edition. The learner names the "
                    "rule and defers code-specific requirements to the AHJ-adopted "
                    "edition."
                ),
            },
        ],
        "artifact_expected": {
            "type": "document",
            "what_to_capture": (
                "A worked diagram-reading set: annotated copies of at least six "
                "residential wiring diagrams (single switched fixture, three-way "
                "switched fixture, GFCI receptacle with LINE and LOAD, AFCI branch, "
                "MWBC, interconnected smoke/CO), with the learner's annotations of "
                "hot / neutral / ground, switch positions, and protection locations"
            ),
            "what_the_evidence_shows": (
                "That the learner reads the standard residential symbol set and the "
                "three diagram types (one-line, wiring, schematic), and can trace "
                "current paths and name protection on common residential circuits"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through the symbol reference and one "
                "diagram of each kind (one-line, wiring, schematic), naming every "
                "symbol and tracing the current path on each."
            ),
            "we_do": (
                "The AI tutor and the learner alternate diagrams. The AI poses a "
                "diagram with annotations missing; the learner fills them in; the AI "
                "confirms or corrects. The MWBC diagram and the GFCI LINE / LOAD "
                "diagram each get extra walkthrough time."
            ),
            "you_do_supervised": (
                "The learner annotates six diagrams independently and submits to the "
                "AI tutor. The AI tutor confirms each annotation; on any miss, the AI "
                "re-quizzes a similar diagram."
            ),
            "you_do_unsupervised": (
                "Once the learner can annotate the six standard diagrams correctly "
                "across two sessions, they may continue with additional kinds of "
                "diagrams (sub-feeder layouts, generator transfer arrangements, "
                "solar interconnections) at the apprentice band."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 45,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": "Knowledge competency. Diagram-reading fluency is universal across credentials.",
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "diagram interpretation of residential circuits per the NEC",
                        "MWBC and shared-neutral rules per the AHJ-adopted NEC",
                        "GFCI / AFCI required locations per the AHJ-adopted NEC",
                    ],
                    "notes": "Heavily tested on the journeyman exam.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": ["diagram fluency across the state licensing exam scope"],
                    "notes": "Universal across every state licensing exam.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-006": {
        "node_type": "knowledge",
        "trade": "electrical",
        "competency_name": (
            "Anatomy of a residential electrical service: service entrance, meter, "
            "main disconnect, panel, branch circuits, overcurrent protection, and "
            "the foundation's scope boundary"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001", "elc-002"],
        "safety_basis": {
            "hazards": [
                (
                    "Misidentifying the line side vs the load side of the main "
                    "disconnect. The line side (the conductors from the meter to the "
                    "main breaker, the meter itself, and the supply from the utility) "
                    "is energized even when the main disconnect is open. Service-"
                    "entrance work is regulated more strictly than branch-circuit "
                    "work and is NOT in scope at the foundation. This is the most "
                    "important boundary in this competency."
                ),
                (
                    "Confusing the role of the main disconnect with the role of a "
                    "branch breaker. The main disconnect de-energizes everything "
                    "downstream (every branch); a branch breaker de-energizes only "
                    "its branch. Both are protective devices but at different "
                    "scopes."
                ),
                (
                    "Trusting a panel label that says BREAKER N controls a specific "
                    "circuit. Panel labels in older or remodeled homes are commonly "
                    "wrong; the verification at the work point under elc-021 is the "
                    "safeguard."
                ),
                (
                    "Treating a subpanel as if its neutral is bonded to ground at the "
                    "subpanel. The AHJ-adopted NEC bonds neutral to ground at the "
                    "main service equipment only; subpanels must have neutral "
                    "isolated from ground. Misunderstanding this is a real downstream "
                    "wiring error."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001 if the learner visits the actual service; no additional PPE required for diagram-and-photo work",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Conceptual work with the AI tutor, on diagrams, photographs (taken "
                "with covers closed), and the household's actual service viewed from "
                "outside the enclosures. No enclosure opening at this band; no live "
                "work."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "A diagram of a residential electrical service from the utility through the main panel",
                "specification": (
                    "A one-line diagram showing utility supply (overhead service drop "
                    "or underground service lateral), the service-entrance conductors, "
                    "the meter base, the main disconnect (a separate switch in some "
                    "installations or a main breaker in combination panels), the "
                    "main panel with branch breakers and neutral / ground busbars, "
                    "any subpanels with their feeders, the grounding electrode system "
                    "(ground rod, water-pipe bond, intersystem bonding termination), "
                    "and the typical branch circuits exiting the panel. The AI tutor "
                    "provides one."
                ),
                "alternatives": [
                    "Clear photographs of the household's actual service taken with "
                    "covers closed (the utility drop, the meter base, the main panel "
                    "exterior, any subpanel exterior)",
                ],
            },
            {
                "name": "The household's actual residential service viewed from outside enclosures",
                "specification": (
                    "The actual installation, walked through with the supervising "
                    "adult on premises (per els-001); the learner identifies each "
                    "component on the diagram against the real installation. No "
                    "enclosure opened."
                ),
                "alternatives": [],
            },
            {
                "name": "Notebook for annotated diagrams and the household's service inventory",
                "specification": "Pencil, paper, and a way to file the work",
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Any flat surface for diagram work; the household's actual service for the walk-through",
            "ventilation": "Per els-001 for the walk-through",
            "lighting": "Per els-001",
            "power": "None for the diagram work; energy state immaterial for cover-closed walk-through",
            "containment": "None required",
        },
        "skill_description": (
            "The learner builds a complete mental map of the residential electrical "
            "service from the utility supply through every branch circuit. The "
            "service begins at the utility's connection: an OVERHEAD SERVICE DROP "
            "(the conductors from the utility pole to the weatherhead at the house) "
            "or an UNDERGROUND SERVICE LATERAL (the conductors from a utility "
            "padmount transformer or pad to the meter base). The conductors enter "
            "the METER BASE (the utility's metering enclosure; this is the utility's "
            "property up to the load-side terminals). From the meter the conductors "
            "go to the MAIN DISCONNECT, which in many residential installations is "
            "the MAIN BREAKER inside the MAIN PANEL (a 'combination service "
            "equipment'); in some installations it is a separate main disconnect "
            "ahead of the panel. The main disconnect de-energizes everything "
            "downstream when opened; the LINE SIDE of the main disconnect remains "
            "energized from the utility (this is the SCOPE BOUNDARY of the "
            "foundation; service-entrance work is not in scope). From the main, "
            "TWO HOT BUSBARS (in residential single-phase 120/240V service, two "
            "120V legs of opposite phases) supply the branch BREAKERS that protect "
            "each branch circuit. A NEUTRAL BUSBAR (bonded to the panel enclosure "
            "and to ground at the main service equipment ONLY per the AHJ-adopted "
            "NEC) carries the return current. The GROUNDING ELECTRODE CONDUCTOR "
            "(GEC) connects the panel's neutral / ground busbar to the GROUNDING "
            "ELECTRODE SYSTEM (typically one or two ground rods, a water-pipe bond "
            "to the metallic water supply if present, possibly a concrete-encased "
            "electrode 'Ufer' if part of the slab, and an intersystem bonding "
            "termination for telephone, cable, and similar systems per the AHJ-"
            "adopted NEC). SUBPANELS, where present, are fed from the main by a "
            "four-wire FEEDER (two hots, a neutral, and an equipment grounding "
            "conductor); the subpanel has its OWN ground bus bonded to its "
            "enclosure but its neutral bus ISOLATED from the enclosure (the AHJ-"
            "adopted NEC governs). Each BRANCH CIRCUIT leaves the panel through a "
            "BRANCH BREAKER (the overcurrent protective device), runs in a CABLE "
            "(NM-B nonmetallic-sheathed cable for residential, MC armored where "
            "permitted, conduit-and-wire in some installations), and serves the "
            "RECEPTACLES, SWITCHES, and FIXTURES on the circuit. The OVERCURRENT "
            "PROTECTION at each branch is sized per the AHJ-adopted NEC's Article "
            "240 to protect the conductors against thermal damage from overload "
            "and short circuit; specific sizing follows the conductor's AMPACITY "
            "per Article 310 (the next competency, elc-007). The learner walks "
            "their household's actual service (covers closed) and identifies each "
            "of these components on the diagram and on the real installation."
        ),
        "demonstration_criteria": [
            (
                "Names every major component of a residential electrical service "
                "from the utility supply through a branch circuit, in order, with "
                "the function of each in one sentence"
            ),
            (
                "Identifies in the household's actual installation: the utility "
                "drop or lateral entry; the meter base; the main disconnect "
                "location; the main panel; any subpanels; the visible grounding "
                "electrode (ground rod, water-pipe bond if accessible)"
            ),
            (
                "Names the LINE / LOAD distinction at the main disconnect and "
                "names that the line side is the foundation's SCOPE BOUNDARY: "
                "service-entrance work is NOT in scope at the foundation"
            ),
            (
                "Names the neutral-to-ground bond rule: bonded at the main "
                "service equipment ONLY per the AHJ-adopted NEC; subpanels have "
                "neutral isolated from ground"
            ),
            (
                "Names the grounding electrode system components likely in the "
                "household: ground rod(s), water-pipe bond, concrete-encased "
                "electrode if present, intersystem bonding termination if present"
            ),
            (
                "Names that each branch circuit is protected by an overcurrent "
                "device (breaker or fuse) sized per the AHJ-adopted NEC to protect "
                "the conductors and the equipment; names that AHJ-adopted Article "
                "240 governs overcurrent protection and Article 310 governs "
                "conductor ampacity"
            ),
            (
                "Names that residential single-phase service is typically 120/240V "
                "split-phase: two 120V hot legs of opposite phases sharing a "
                "neutral; either hot to neutral gives 120V (general branches), "
                "hot-to-hot gives 240V (range, dryer, electric water heater, "
                "central AC dedicated branches)"
            ),
            (
                "Annotates a one-line diagram of a representative residential "
                "service, labeling every component named above"
            ),
        ],
        "common_errors": [
            {
                "error": "Treating the meter as 'where the power starts inside the house'",
                "cause": "The learner did not internalize that the meter is the utility's metering enclosure, and that the conductors from the meter to the main disconnect are still service-entrance conductors",
                "remedy": (
                    "The service-entrance conductors and the meter itself are part "
                    "of the SERVICE (the line side of the main disconnect); the "
                    "premises wiring begins at the load side of the main "
                    "disconnect. The AHJ-adopted NEC Article 100 names the "
                    "definitions. The line side is OUT OF SCOPE at the "
                    "foundation."
                ),
            },
            {
                "error": "Wiring a subpanel's neutral bonded to its enclosure",
                "cause": "The learner read the bond rule for the main and applied it everywhere",
                "remedy": (
                    "The neutral-to-ground bond exists at the main service "
                    "equipment ONLY. At a subpanel, the neutral bus is ISOLATED "
                    "from the enclosure; the ground bus is bonded to the "
                    "enclosure. Duplicate bonds at subpanels create parallel "
                    "return paths via the equipment grounding conductors, can "
                    "cause neutral current on the equipment grounding system, "
                    "and can energize metal equipment under fault. The AHJ-"
                    "adopted NEC governs."
                ),
            },
            {
                "error": "Confusing 120V general branches with 240V dedicated branches",
                "cause": "The learner did not internalize that residential is 120/240V split-phase",
                "remedy": (
                    "Either 120V hot leg to neutral is a 120V general branch "
                    "(receptacles, lights, small appliances). Both hot legs "
                    "together (hot-to-hot) is 240V for dedicated branches "
                    "(electric range, dryer, water heater, central AC). The "
                    "panel uses two-pole breakers (one in each phase position) "
                    "for 240V branches and single-pole breakers for 120V "
                    "branches."
                ),
            },
            {
                "error": "Treating overcurrent protection as if it protected the load",
                "cause": "The learner thought the breaker's amp rating was 'for the load'",
                "remedy": (
                    "Overcurrent protection per the AHJ-adopted NEC Article 240 "
                    "protects the CONDUCTORS (and the equipment) against thermal "
                    "damage from overload and short circuit. The load may be "
                    "sized smaller than the breaker; what cannot happen is the "
                    "conductor sized smaller than the breaker. Conductor sizing "
                    "(elc-007) is what the breaker is protecting."
                ),
            },
            {
                "error": "Trusting a panel label as authoritative",
                "cause": "The learner did not internalize the rule that labels are commonly wrong in older or remodeled homes",
                "remedy": (
                    "Labels are a starting point, not a final answer. Every "
                    "elc-021 act verifies dead at the work point regardless of "
                    "label. Labels are corrected during a verified-dead session "
                    "by the licensed electrician."
                ),
            },
        ],
        "artifact_expected": {
            "type": "document",
            "what_to_capture": (
                "An annotated one-line diagram of the household's actual "
                "residential service, with every major component named and "
                "labeled (utility supply, meter, main disconnect, main panel, "
                "subpanels if any, neutral / ground busbars, grounding electrode "
                "system, representative branches at 120V and 240V), accompanied "
                "by cover-closed photographs of each component on the diagram"
            ),
            "what_the_evidence_shows": (
                "That the learner has a complete mental and visual map of the "
                "household's actual residential service, can name the scope "
                "boundary at the main disconnect, can name the neutral-to-"
                "ground bond rule, and can name the role of the grounding "
                "electrode system and the overcurrent protection"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a representative "
                "residential service one-line diagram, naming every component "
                "in order from utility supply inward, and explains the LINE / "
                "LOAD scope boundary, the neutral-to-ground bond rule, and the "
                "120/240V split-phase convention."
            ),
            "we_do": (
                "The AI tutor and the learner walk through a second sample "
                "service together. The learner names a component; the AI "
                "confirms or corrects. Then the learner walks the household's "
                "actual service with the supervising adult on premises, "
                "identifying each component on the real installation against "
                "the diagram."
            ),
            "you_do_supervised": (
                "The learner annotates a one-line diagram of the household's "
                "actual service, naming every component, and submits to the "
                "AI tutor. The AI tutor confirms each annotation and the "
                "scope-boundary call. The supervising adult is on premises for "
                "the walk-through; the AI mentors the diagram work."
            ),
            "you_do_unsupervised": (
                "Once the learner can annotate the household's service "
                "correctly and walk through it identifying every component, "
                "they may study additional residential service configurations "
                "(generator transfer arrangements, solar interconnections, "
                "200A vs 100A vs 400A services, subpanel arrangements) at the "
                "apprentice band."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 45,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": "Knowledge competency. Service-anatomy fluency underpins every later install and service competency.",
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "NEC Article 100 definitions (service, service-entrance, "
                        "service equipment, branch circuit, feeder, etc.)",
                        "NEC Article 230 services and service-entrance "
                        "requirements",
                        "NEC Article 250 grounding and bonding",
                        "NEC Article 240 overcurrent protection",
                        "NEC Article 408 panelboards and switchboards",
                    ],
                    "notes": "These chapters are foundational on every journeyman and master exam.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": ["service anatomy across the state licensing exam scope"],
                    "notes": "Universal foundational knowledge.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-007": {
        "node_type": "knowledge",
        "trade": "electrical",
        "competency_name": (
            "Conductor sizing and ampacity basics for residential branch circuits "
            "and feeders (concepts and AHJ-adopted NEC reference)"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001", "elc-003", "elc-004"],
        "safety_basis": {
            "hazards": [
                (
                    "Undersizing a conductor for a given load is one of the historic "
                    "causes of residential electrical fires. A conductor carrying "
                    "more current than its ampacity heats; the insulation fails; "
                    "the conductor arcs or melts; fire follows. Conductor sizing is "
                    "a load-bearing knowledge competency precisely because the "
                    "downstream installation depends on it being correct."
                ),
                (
                    "Treating ampacity as a single fixed number rather than as a "
                    "table look-up adjusted for installation conditions. The AHJ-"
                    "adopted NEC's ampacity tables (Article 310 in current editions) "
                    "apply at a specific ambient temperature and a specific "
                    "conductor count in the raceway; deviations from those "
                    "conditions require AHJ-adopted correction factors. The wrong "
                    "ampacity from missing the correction is a real downstream "
                    "error."
                ),
                (
                    "Mismatching the conductor's insulation temperature rating with "
                    "the termination's temperature rating. The AHJ-adopted NEC's "
                    "termination temperature rule (often called the 60/75/90 rule) "
                    "limits the ampacity used in sizing to the LOWER of the "
                    "conductor's insulation rating and the termination device's "
                    "rating. This is one of the most-missed rules at the journeyman "
                    "level; the AI tutor names it explicitly at the helper band."
                ),
                (
                    "Using a copper-only table for aluminum conductors (or vice "
                    "versa). Aluminum has different ampacity at the same size than "
                    "copper; the AHJ-adopted NEC publishes separate tables. Mixing "
                    "is a real downstream error."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001; no additional PPE for paper work",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Conceptual work with paper, the AHJ-adopted NEC ampacity tables "
                "(referenced by article and table number, not reproduced), and the "
                "AI tutor. No real conductors handled, no live work."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "The household's AHJ-adopted-edition NEC for reference",
                "specification": (
                    "The current NEC adopted by the local AHJ. The actual table "
                    "values, the correction factors, and the termination-temperature "
                    "rule are read from the code itself; this node does NOT "
                    "reproduce code text or table values. The learner consults the "
                    "AHJ-adopted edition for each problem."
                ),
                "alternatives": [],
            },
            {
                "name": "Pencil, paper, and a calculator",
                "specification": "Standard arithmetic plus multiplication for correction-factor application",
                "alternatives": [],
            },
            {
                "name": "Sample problem set provided by the AI tutor",
                "specification": (
                    "Worked sample problems matched to the AHJ-adopted edition's "
                    "ampacity tables; the learner solves with the code in hand"
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Any flat surface (desk or table)",
            "ventilation": "Indoor or outdoor; not relevant",
            "lighting": "Adequate to read the code and the calculator",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner learns the conceptual basis of conductor sizing and the "
            "structure of the AHJ-adopted NEC's ampacity tables, WITHOUT memorizing "
            "specific numbers (which change by edition). The conceptual basis: a "
            "conductor's ampacity is the maximum continuous current it can carry "
            "without exceeding the insulation's temperature rating at the rated "
            "ambient conditions and conductor count. The AHJ-adopted NEC's Article "
            "310 publishes the ampacity tables. The values in the table are at a "
            "specific ambient temperature (often 30 degrees C / 86 degrees F) and "
            "for a specific number of current-carrying conductors in a raceway "
            "(historically three or fewer); ambient temperatures above the table's "
            "base and conductor counts above the table's base require correction "
            "factors (also published in Article 310). Insulation temperature rating "
            "matters: a conductor rated for 90 degrees C insulation can carry more "
            "current than the same conductor with 60 degrees C insulation in the "
            "same ambient, because the conductor itself is the same but the "
            "insulation tolerates more heat. The AHJ-adopted NEC's termination-"
            "temperature rule limits the actual ampacity used in sizing to the "
            "LOWER of the conductor's insulation rating and the termination "
            "device's rating; residential terminations are commonly rated 60 or 75 "
            "degrees C, and using a 90 degrees C ampacity at a 60 degrees C "
            "termination is a code violation that produces undersized terminations. "
            "Copper and aluminum have different ampacities at the same gauge; "
            "aluminum tables are separate from copper tables. The learner reads "
            "the relevant tables in the AHJ-adopted edition, names which table "
            "applies to which conductor material and insulation rating, applies "
            "correction factors for ambient temperature and conductor count, and "
            "applies the termination-temperature rule. The learner does NOT "
            "memorize specific table numbers (they change per edition); the "
            "learner DOES build the habit of looking up the answer in the code in "
            "hand."
        ),
        "demonstration_criteria": [
            (
                "Names that conductor ampacity is set by the AHJ-adopted NEC's "
                "Article 310 ampacity tables; locates the relevant tables in the "
                "household's adopted edition; the AI tutor confirms the locator "
                "is correct"
            ),
            (
                "Names the structure of an ampacity table: rows are conductor sizes "
                "(AWG or kcmil), columns are insulation temperature ratings (60 "
                "degrees C, 75 degrees C, 90 degrees C), values are amperes at the "
                "table's base ambient temperature"
            ),
            (
                "Names the termination-temperature rule (the 60/75/90 rule): the "
                "ampacity actually used for sizing is the LOWER of the conductor's "
                "insulation rating and the termination device's rating; in many "
                "residential installations the termination dictates the 75 degrees "
                "C or even 60 degrees C column"
            ),
            (
                "Names that ambient temperatures above the table's base and "
                "conductor counts above the table's base require correction "
                "factors, also published in Article 310"
            ),
            (
                "Names that copper and aluminum have separate ampacity tables, and "
                "names that aluminum at the same gauge carries less current than "
                "copper"
            ),
            (
                "Solves three guided ampacity-look-up problems in the AHJ-adopted "
                "edition: a 14 AWG copper THHN/THWN conductor in a residential "
                "raceway at standard ambient; a 12 AWG copper THHN/THWN in the "
                "same; a #8 AWG copper THHN/THWN feeding a typical residential "
                "240V branch (the AI tutor confirms the table-look-up technique, "
                "not the specific value, which the AHJ-adopted edition provides)"
            ),
            (
                "Names the rule that the overcurrent device (the breaker per "
                "Article 240) must protect the CONDUCTOR'S ampacity; you do not "
                "use a breaker larger than the conductor can safely carry; "
                "permitted exceptions per the AHJ-adopted NEC are named without "
                "reproduction"
            ),
            (
                "Catches at least one unreasonable answer: a 14 AWG copper "
                "conductor wired to a 30A breaker (the breaker exceeds the "
                "conductor's ampacity) is the kind of error the conductor-sizing "
                "rules exist to prevent"
            ),
        ],
        "common_errors": [
            {
                "error": "Memorizing 15A = 14 AWG, 20A = 12 AWG, 30A = 10 AWG as if these were the answer",
                "cause": "The learner picked up rules of thumb without the AHJ-adopted NEC's actual table and correction factors",
                "remedy": (
                    "The rules of thumb are starting points, not answers. The "
                    "AHJ-adopted edition's tables and correction factors are the "
                    "authority. Many installations use higher ratings (because of "
                    "the 75 or 90 degrees C column with appropriate terminations); "
                    "many require lower ratings (because of derating for ambient or "
                    "conductor count). The habit is to look up, not memorize."
                ),
            },
            {
                "error": "Using the 90 degrees C column for sizing at a 75 degrees C termination",
                "cause": "The learner saw a higher ampacity in the 90 degrees C column and used it",
                "remedy": (
                    "The termination-temperature rule limits the ampacity to the "
                    "termination's rating. Using the 90 degrees C column at a 75 "
                    "degrees C termination overheats the termination and is a "
                    "code violation. Most residential terminations are 60 or 75 "
                    "degrees C; verify before sizing."
                ),
            },
            {
                "error": "Forgetting to apply ambient-temperature correction in a hot attic",
                "cause": "The learner used the base table value for a conductor that runs through a 120 degrees F attic",
                "remedy": (
                    "Ambient temperatures above the table's base require the "
                    "AHJ-adopted NEC's correction factor (also in Article 310). "
                    "Attics in summer commonly exceed the base; the correction "
                    "factor reduces the ampacity. Apply it before sizing."
                ),
            },
            {
                "error": "Forgetting to apply conductor-count adjustment in a bundled cable run",
                "cause": "The learner ran six current-carrying conductors in one conduit and used the unadjusted ampacity",
                "remedy": (
                    "Conductor counts above the table's base require the "
                    "adjustment factor. More than three current-carrying "
                    "conductors in a raceway requires adjustment per the AHJ-"
                    "adopted NEC."
                ),
            },
            {
                "error": "Mixing copper and aluminum ampacity values",
                "cause": "The learner read a copper-table value and applied it to an aluminum conductor",
                "remedy": (
                    "Copper and aluminum are different conductor materials with "
                    "different conductivities; the AHJ-adopted NEC publishes "
                    "separate tables. Aluminum at the same gauge carries less "
                    "current than copper; do not mix tables."
                ),
            },
        ],
        "artifact_expected": {
            "type": "document",
            "what_to_capture": (
                "A worked problem set of conductor-sizing look-ups using the "
                "household's AHJ-adopted NEC: at least three branch-circuit sizing "
                "problems and one feeder sizing problem, with the table reference "
                "(article and table number from the adopted edition), the column "
                "used (60 / 75 / 90 degrees C), any correction factors applied "
                "(ambient, conductor count), and the resulting ampacity and "
                "breaker selection; the AI tutor confirms the method and the "
                "code reference"
            ),
            "what_the_evidence_shows": (
                "That the learner can navigate the AHJ-adopted NEC's ampacity "
                "tables, apply the termination-temperature rule and the "
                "correction factors, and arrive at a defensible conductor and "
                "breaker selection for a residential branch or feeder"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through one worked problem with "
                "the AHJ-adopted edition open: a residential 20A branch on 12 AWG "
                "copper THHN/THWN at standard ambient with a 75 degrees C "
                "termination. Names the table, the column, and the resulting "
                "ampacity. Names the termination-temperature rule explicitly."
            ),
            "we_do": (
                "The AI tutor and the learner work a second problem together with "
                "a non-standard condition (a hot attic ambient). The learner reads "
                "the correction factor from the AHJ-adopted edition; the AI tutor "
                "confirms the method. They work a third problem with a non-"
                "standard conductor count (a six-conductor raceway)."
            ),
            "you_do_supervised": (
                "The learner solves a three-problem set in the AHJ-adopted "
                "edition. The AI tutor confirms each method and the code "
                "reference."
            ),
            "you_do_unsupervised": (
                "Once the learner can navigate the ampacity tables independently "
                "and apply the termination and correction rules, they may "
                "continue to deeper Article-310 work (Type SE service-entrance "
                "cable, conductors in conduit underground, parallel conductors) "
                "at the apprentice band. The AI tutor remains available for "
                "code-reference confirmation."
            ),
        },
        "estimated_practice_sessions_to_signoff": 5,
        "session_length_minutes": 45,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency. Conductor sizing and ampacity is one of the "
                "most-tested topics on every journeyman and master exam."
            ),
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "NEC Article 310 ampacity",
                        "NEC Article 240 overcurrent protection",
                        "termination-temperature rule (NEC 110.14(C))",
                        "ambient and conductor-count correction factors per Article 310",
                    ],
                    "notes": "Universally tested at journeyman and master levels.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": ["conductor sizing across the state licensing exam scope"],
                    "notes": "Foundational on every state exam.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-008": {
        "node_type": "knowledge",
        "trade": "electrical",
        "competency_name": (
            "Grounding and bonding theory for a residential electrical system "
            "(concepts and AHJ-adopted NEC reference; NOT a license to perform "
            "energized grounding work alone)"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001", "elc-006"],
        "safety_basis": {
            "hazards": [
                (
                    "Confusing GROUNDING with BONDING. The two are distinct: grounding "
                    "connects the system to earth; bonding connects metal parts that "
                    "could otherwise be at different potentials. Both are required; "
                    "they serve different safety functions. Confusion between them is "
                    "the most-documented residential electrical knowledge gap and the "
                    "reason this competency exists at the helper band."
                ),
                (
                    "Bonding neutral to ground at a subpanel (instead of at the main "
                    "service equipment only). This creates parallel return paths via "
                    "the equipment grounding conductor under normal operation, can "
                    "energize metal equipment under fault, and can cause shock or "
                    "fire. The AHJ-adopted NEC bonds at the main service equipment "
                    "ONLY (Article 250 in current editions)."
                ),
                (
                    "Treating the equipment grounding conductor as if it carries "
                    "current under normal operation. The EGC is a SAFETY BOND that "
                    "carries current ONLY during a fault (when insulation failure "
                    "places a hot conductor in contact with metal that should be at "
                    "ground potential). Designing or wiring as if the EGC normally "
                    "carries current is wrong and dangerous."
                ),
                (
                    "Believing that 'a ground rod is enough.' Ground rods alone "
                    "typically have high resistance to earth (often hundreds of "
                    "ohms); they cannot safely clear a fault by themselves. The "
                    "fault-clearing safety function depends on the LOW-IMPEDANCE PATH "
                    "back to the source (utility neutral) through the equipment "
                    "grounding conductor and the main bonding jumper. The ground rod's "
                    "role is to bond the system to earth potential, not to be a "
                    "fault path. The AHJ-adopted NEC's separate fault-current path "
                    "and grounding-electrode requirements both exist for distinct "
                    "reasons."
                ),
                (
                    "Performing energized grounding work without a licensed "
                    "electrician present. Grounding theory at this band is "
                    "CONCEPTUAL ONLY; the AHJ-adopted NEC's grounding-electrode "
                    "system, main bonding jumper, equipment grounding conductor, and "
                    "intersystem bonding work are all licensed-electrician work "
                    "regulated by the AHJ. Knowledge of the theory does NOT "
                    "authorize hands-on grounding work."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001; no additional PPE for paper work",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Conceptual work with the AHJ-adopted NEC Article 250 in hand and "
                "the AI tutor. No hands-on grounding work at this band. Knowledge "
                "of grounding and bonding theory does NOT authorize hands-on "
                "grounding work; that work is licensed-electrician work and is not "
                "in scope at the foundation. The AI tutor names this rule "
                "throughout the competency."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "The household's AHJ-adopted-edition NEC, Article 250",
                "specification": (
                    "The current NEC adopted by the local AHJ; Article 250 governs "
                    "grounding and bonding. The article structure (general; system "
                    "grounding; grounding electrode system; main bonding jumper; "
                    "equipment grounding; equipment grounding conductors; bonding) "
                    "is the reference for this competency. The node does NOT "
                    "reproduce code text."
                ),
                "alternatives": [],
            },
            {
                "name": "A residential grounding-and-bonding diagram",
                "specification": (
                    "A diagram showing the grounding electrode system (ground "
                    "rod(s), water-pipe bond if accessible, concrete-encased "
                    "electrode if present, intersystem bonding termination), the "
                    "grounding electrode conductor (GEC) from the panel to the "
                    "electrodes, the main bonding jumper at the main service "
                    "equipment bonding neutral to ground ONCE, the equipment "
                    "grounding conductors running with every branch circuit, and "
                    "the bonded metal water pipe and gas pipe (where required by "
                    "the AHJ-adopted NEC). The AI tutor provides one."
                ),
                "alternatives": [],
            },
            {
                "name": "Pencil, paper, and a notebook",
                "specification": "Standard; the learner annotates the diagram and writes worked explanations",
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Any flat surface (desk or table)",
            "ventilation": "Indoor or outdoor; not relevant",
            "lighting": "Adequate to read the code and the diagram",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner builds a sound conceptual understanding of grounding and "
            "bonding, the two distinct (and complementary) safety mechanisms in a "
            "residential electrical system. GROUNDING refers to the connection of "
            "the electrical system to earth: the GROUNDING ELECTRODE SYSTEM (one "
            "or more ground rods, a water-pipe bond to the metallic water service "
            "if present, a concrete-encased 'Ufer' electrode if part of the slab, "
            "an intersystem bonding termination for telephone / cable / similar "
            "systems) is connected to the panel's neutral / ground bus by the "
            "GROUNDING ELECTRODE CONDUCTOR (GEC). The grounding electrode system "
            "stabilizes the system voltage with respect to earth; it does NOT "
            "primarily provide a fault-clearing path. BONDING refers to the "
            "deliberate connection of metal parts so that they share the same "
            "electrical potential and cannot energize relative to each other "
            "under fault. The MAIN BONDING JUMPER bonds the neutral to ground "
            "ONCE at the main service equipment (and only there, per the AHJ-"
            "adopted NEC); the EQUIPMENT GROUNDING CONDUCTOR (EGC) bonds every "
            "branch circuit's metal raceway and equipment back to the panel; "
            "metal water and gas piping is bonded where the AHJ-adopted NEC "
            "requires; intersystem bonding terminates the bonding of telephone, "
            "cable, antenna, and similar systems at the service. The "
            "FAULT-CLEARING PATH is the LOW-IMPEDANCE PATH a fault current "
            "follows when a hot conductor contacts metal that should be at "
            "ground potential: through the EGC back to the panel, through the "
            "main bonding jumper to the neutral, and through the neutral back "
            "to the utility transformer. The breaker operates only when the "
            "fault current is high enough to trip it, which requires a "
            "LOW-IMPEDANCE PATH. The ground rod is too high in resistance to "
            "carry fault current safely; if the only path were ground rod to "
            "earth, the breaker would NOT trip and metal equipment would stay "
            "energized at lethal voltage. This is the most-misunderstood part "
            "of residential electrical theory and the reason elc-008 exists at "
            "the helper band. The learner annotates the diagram, names every "
            "component, and writes one paragraph explaining the difference "
            "between grounding and bonding, in plain language, with the "
            "fault-clearing path as the centerpiece. Knowledge of this theory "
            "does NOT authorize hands-on grounding work; the AHJ-adopted NEC's "
            "grounding-and-bonding requirements are licensed-electrician work."
        ),
        "demonstration_criteria": [
            (
                "Names the distinction between GROUNDING (connection to earth) and "
                "BONDING (connection between metal parts to keep them at the same "
                "potential); explains in one paragraph why both are required and "
                "how they serve different safety functions"
            ),
            (
                "Names the components of the grounding electrode system likely in "
                "the household: ground rod(s), water-pipe bond if the metallic "
                "water service is present, concrete-encased electrode if present, "
                "intersystem bonding termination"
            ),
            (
                "Names the grounding electrode conductor (GEC) and its role: "
                "connects the panel's neutral / ground bus to the grounding "
                "electrode system"
            ),
            (
                "Names the main bonding jumper and its role: bonds neutral to "
                "ground ONCE at the main service equipment; this is the only "
                "place in the system where neutral and ground are bonded together"
            ),
            (
                "Names the equipment grounding conductor (EGC) and its role: the "
                "low-impedance path from every metal raceway and metal equipment "
                "back to the panel, used to clear a fault"
            ),
            (
                "Names the fault-clearing path explicitly: hot contacts metal that "
                "should be at ground potential -> fault current flows through the "
                "EGC back to the panel -> through the main bonding jumper to the "
                "neutral -> through the neutral back to the utility transformer "
                "-> the resulting high fault current trips the breaker"
            ),
            (
                "Names that the ground rod's role is to bond the system to earth "
                "potential, NOT to be the fault-clearing path; the ground rod's "
                "resistance to earth is typically too high to clear a fault by "
                "itself"
            ),
            (
                "Names the rule that bonding neutral to ground at a subpanel is a "
                "code violation per the AHJ-adopted NEC, and names the failure "
                "modes (parallel return paths on EGC, energized metal equipment "
                "under fault)"
            ),
            (
                "Names that hands-on grounding work is licensed-electrician work "
                "and is not in scope at the foundation; this knowledge competency "
                "does NOT authorize the learner to perform grounding work"
            ),
            (
                "Annotates a residential grounding-and-bonding diagram with every "
                "component named correctly; submits to the AI tutor for "
                "confirmation"
            ),
        ],
        "common_errors": [
            {
                "error": "Calling 'a ground rod' the safety mechanism that protects from shock",
                "cause": "The learner did not internalize that the EGC and the bonding system, not the ground rod, are what clear faults",
                "remedy": (
                    "The ground rod stabilizes the system to earth potential. The "
                    "EGC (and the main bonding jumper, and the neutral back to the "
                    "transformer) are the low-impedance fault path that allows the "
                    "breaker to trip. Without the EGC, the breaker would not trip "
                    "on a fault even with a ground rod present. The AI tutor walks "
                    "the fault-clearing path explicitly."
                ),
            },
            {
                "error": "Bonding neutral to ground at a subpanel",
                "cause": "The learner did not internalize the once-only bonding rule",
                "remedy": (
                    "The neutral-to-ground bond exists at the main service "
                    "equipment ONLY. At a subpanel, the neutral and ground are "
                    "isolated: the neutral bus floats relative to the enclosure; "
                    "the ground bus is bonded to the enclosure. Duplicating the "
                    "bond at the subpanel creates parallel return paths through "
                    "the EGC and can energize metal equipment under fault."
                ),
            },
            {
                "error": "Treating the EGC as if it carries current normally",
                "cause": "The learner confused the EGC with the neutral",
                "remedy": (
                    "Under normal operation the EGC carries NO current; the "
                    "neutral carries the return current. The EGC carries current "
                    "ONLY during a fault. Designing or wiring as if the EGC "
                    "normally carries current is wrong; if you see current on "
                    "the EGC under normal operation, something is misconfigured."
                ),
            },
            {
                "error": "Bonding metal water piping but skipping intersystem bonding",
                "cause": "The learner did not study the AHJ-adopted NEC's intersystem-bonding requirement",
                "remedy": (
                    "The AHJ-adopted NEC requires intersystem bonding termination "
                    "at the service to bond telephone, cable, antenna, and "
                    "similar systems to the grounding electrode system. The "
                    "purpose is to keep all utility entrances at the same "
                    "potential during a transient (lightning surge, line fault). "
                    "Skipping it leaves potential-difference vulnerabilities."
                ),
            },
            {
                "error": "Thinking the EGC is optional on residential branches",
                "cause": "The learner saw old two-wire installations and concluded the EGC was optional",
                "remedy": (
                    "Modern residential branch circuits per the AHJ-adopted NEC "
                    "include an EGC (the bare or green conductor in NM-B cable; "
                    "the equipment-grounding conductor in a separate raceway "
                    "system). Old two-wire installations (no EGC) are legacy and "
                    "are addressed by the AHJ-adopted NEC's specific exceptions "
                    "(GFCI protection in some cases). New work follows the "
                    "current code; legacy work is treated specifically per the "
                    "AHJ."
                ),
            },
        ],
        "artifact_expected": {
            "type": "document",
            "what_to_capture": (
                "An annotated grounding-and-bonding diagram of a typical "
                "residential service with the household's actual configuration "
                "noted (which grounding electrodes are present: ground rod, "
                "water-pipe bond, Ufer, intersystem bonding), with the GEC, "
                "main bonding jumper, EGC, and bonded metal systems all labeled; "
                "plus a one-paragraph written explanation of the difference "
                "between grounding and bonding and the fault-clearing path. "
                "Submitted to the AI tutor for confirmation."
            ),
            "what_the_evidence_shows": (
                "That the learner has internalized the distinction between "
                "grounding and bonding, can name every component of the system, "
                "can trace the fault-clearing path, and can name the licensed-"
                "electrician scope boundary on hands-on work"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a residential grounding-"
                "and-bonding diagram, naming every component and tracing the "
                "fault-clearing path explicitly. Names the once-only bonding "
                "rule and the role of the ground rod (stabilize to earth; not a "
                "fault path)."
            ),
            "we_do": (
                "The AI tutor and the learner annotate a sample diagram "
                "together. The learner names a component; the AI confirms or "
                "corrects. The AI poses the question 'what happens during a "
                "ground fault if the EGC is missing?' and walks the learner "
                "through the answer."
            ),
            "you_do_supervised": (
                "The learner annotates a diagram of the household's own "
                "service grounding-and-bonding, names every component, and "
                "writes the one-paragraph explanation. Submits to the AI tutor "
                "for confirmation."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce a correct annotated diagram and "
                "explanation across at least two sessions, they may continue to "
                "the apprentice band's deeper Article-250 work (sizing the GEC, "
                "sizing the EGC for different branch capacities, parallel "
                "feeders, separately derived systems). Hands-on grounding work "
                "remains licensed-electrician work and is not in scope at any "
                "point in the foundation."
            ),
        },
        "estimated_practice_sessions_to_signoff": 5,
        "session_length_minutes": 45,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency. Grounding and bonding is the most "
                "safety-critical conceptual area in residential electrical "
                "theory and is heavily tested on every journeyman and master "
                "exam."
            ),
            "certifications_supported": [
                {
                    "id": "elcert-nec",
                    "domains": [
                        "NEC Article 250 grounding and bonding (every part)",
                        "fault-clearing path concept (NFPA 70E and NEC),",
                        "intersystem bonding (NEC 250.94)",
                    ],
                    "notes": "Article 250 is one of the most-tested NEC chapters on every journeyman and master exam.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": [
                        "grounding and bonding at journeyman and master depth",
                    ],
                    "notes": "Universal foundational knowledge.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-009": {
        "node_type": "technique",
        "trade": "electrical",
        "competency_name": (
            "Meter and tool literacy: multimeter Category (CAT) ratings, insulated "
            "and insulating tools, glove inspection, and tool selection for the "
            "work; NO live measurement at this band"
        ),
        "progression_band": "helper",
        "prerequisites": ["els-001", "elc-003"],
        "safety_basis": {
            "hazards": [
                (
                    "Using a multimeter with insufficient Category (CAT) rating on a "
                    "live circuit. A CAT II meter on a CAT III circuit can read zero "
                    "on a live conductor, can fail internally during a measurement, "
                    "OR can explode in the user's hand during a fault transient. "
                    "The CAT rating is the meter's design strength against transient "
                    "voltages on the circuit being measured. CAT III at 600V minimum "
                    "is the residential standard per NFPA 70E for 240V branch-"
                    "circuit verification; CAT IV is acceptable; CAT II or unrated "
                    "meters are NOT acceptable per NFPA 70E. This is the most-"
                    "documented multimeter-related cause of injury in working "
                    "electricians."
                ),
                (
                    "Using a multimeter with cracked, abraded, or otherwise damaged "
                    "test leads. A damaged lead can short to the user's hand or to "
                    "the work surface, causing shock or arc flash. Lead inspection "
                    "is part of the pre-measurement routine per NFPA 70E."
                ),
                (
                    "Using insulating gloves that have not been inspected (visual "
                    "for cuts, punctures, ozone cracking; air-roll test per the "
                    "manufacturer where applicable). Insulating gloves degrade with "
                    "age, oil exposure, and UV; an undetected pinhole on a "
                    "supposedly 1000V-rated glove can allow lethal current through "
                    "the user. NFPA 70E and the glove manufacturer govern inspection."
                ),
                (
                    "Using non-insulated screwdrivers or pliers near energized "
                    "equipment. A standard screwdriver shaft is a conductor; a "
                    "slip can short hot to ground or to another phase, causing arc "
                    "flash. Insulated tools rated for the voltage (IEC 60900 / ASTM "
                    "F1505) are the standard for any work near energized equipment "
                    "per NFPA 70E."
                ),
                (
                    "Performing any live measurement at this band. elc-009 is "
                    "meter and tool LITERACY: identification, inspection, and "
                    "selection. NO live measurement is part of elc-009; live "
                    "measurement is part of elc-021 with the licensed electrician "
                    "physically present."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001 (closed-toe shoes, the trade's general defaults)",
                "Safety glasses for any work handling tools or meters; no live measurement at this band",
                (
                    "Insulating gloves for INSPECTION practice only at this band "
                    "(the learner inspects an insulating glove with the licensed "
                    "electrician's coaching, but does not USE the gloves on a live "
                    "circuit until elc-021)"
                ),
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Meter and tool literacy involves handling instruments and tools "
                "on a workbench, no live circuit contact, no enclosure opening, "
                "no operation of disconnects. The AI tutor mentors end-to-end: "
                "the learner photographs the household's actual multimeter (or a "
                "sample), names each control and the CAT rating, inspects test "
                "leads, inspects insulated tools, and quizzes against the AI "
                "tutor on selection scenarios. No live measurement is in scope "
                "at this band; live measurement is elc-021 with a licensed "
                "electrician physically present."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "A real multimeter (DMM) the household owns or can obtain",
                "specification": (
                    "A digital multimeter the learner can hold, inspect, and "
                    "photograph. The meter's CAT rating is on the meter face or in "
                    "the manual. If the household's meter is CAT II or unrated, "
                    "the AI tutor identifies it as INADEQUATE for any later live "
                    "measurement per NFPA 70E; the household upgrades to CAT III "
                    "at 600V minimum (Fluke, Klein, Ideal, Amprobe, and other "
                    "recognized industrial brands at the named CAT rating are "
                    "acceptable; inexpensive automotive or hobby meters typically "
                    "lack the CAT rating and are not acceptable for residential "
                    "240V work)."
                ),
                "alternatives": [
                    "Manufacturer photos and manuals of a CAT III 600V residential-"
                    "scope meter, used as a learning aid if the household's meter "
                    "is being upgraded",
                ],
            },
            {
                "name": "Standard test leads with manufacturer's CAT marking",
                "specification": (
                    "Test leads matched to the meter's CAT rating; leads are "
                    "inspected for cracked insulation, broken shrouds, exposed "
                    "conductor, and intact probe tips and connectors. Damaged "
                    "leads are removed from service."
                ),
                "alternatives": [],
            },
            {
                "name": "A representative set of insulated and insulating tools",
                "specification": (
                    "Insulated screwdrivers, pliers, and nut drivers rated 1000V "
                    "per IEC 60900 / ASTM F1505 (the learner identifies the "
                    "rating mark on the tool); insulating gloves (Class 00 "
                    "rated 500V minimum for residential 240V per NFPA 70E) with "
                    "their leather protectors; a glove inspection kit (visual "
                    "and air-roll test per the manufacturer)"
                ),
                "alternatives": [
                    "Photos and specifications from manufacturers of recognized "
                    "insulated tools, used as a learning aid if the household "
                    "does not yet have a full set",
                ],
            },
            {
                "name": "The multimeter and tool manufacturer manuals",
                "specification": "The manuals shipped with the equipment; the AI tutor walks the learner through the relevant pages",
                "alternatives": [],
            },
            {
                "name": "Notebook for meter and tool cards",
                "specification": "Pencil and paper to record CAT ratings, calibration dates, inspection results, and replacement schedules",
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "A workbench or clean table; the work is bench-based, no live circuits",
            "ventilation": "Indoor or outdoor; not relevant",
            "lighting": "Strong enough to read the meter face markings clearly",
            "power": "None (multimeter own battery)",
            "containment": "None required",
        },
        "skill_description": (
            "The learner builds fluency in identifying, inspecting, and selecting "
            "the meters and tools used in residential electrical work, with no "
            "live measurement at this band. MULTIMETER: the learner identifies "
            "the meter's Category (CAT) rating (CAT II / III / IV) and voltage "
            "rating on the meter face or in the manual; names what each Category "
            "is designed to survive (CAT II for receptacles and appliances at "
            "the end of branch circuits; CAT III for distribution panels, "
            "feeders, and short branch circuits with significant transient "
            "exposure; CAT IV for utility connection points and outdoor service "
            "entrances); names that CAT III at 600V is the residential "
            "standard per NFPA 70E for 240V branch-circuit verification, CAT IV "
            "acceptable, CAT II or unrated NOT acceptable. The learner reads "
            "the meter's range selector and identifies AC voltage, DC voltage, "
            "AC current (if the meter has a clamp), DC current, resistance, "
            "continuity, diode, and (where present) capacitance and frequency "
            "ranges; names the auto-ranging vs manual-ranging distinction. "
            "The learner identifies the test-lead connectors (COM, V/Ohm, A, "
            "mA/uA) and the standard color coding (black to COM, red to V/Ohm "
            "or A as appropriate). The learner inspects the test leads visually "
            "(cracked insulation, broken shrouds, exposed conductor); damaged "
            "leads are removed from service. TEST-LEAD PROBES: the learner "
            "names finger-guard probes (the safety guard between the user's "
            "finger and the probe tip per IEC 61010-031) and identifies them "
            "on the household's leads. METER FUSES: the learner identifies the "
            "current-circuit fuse on the meter and names that a blown fuse "
            "removes current-measurement capability and that operating a meter "
            "with a wrong fuse (or no fuse) is a fault-survival failure. "
            "INSULATED TOOLS: the learner identifies the IEC 60900 / ASTM "
            "F1505 marking on insulated screwdrivers, pliers, and nut drivers; "
            "the household's insulated tools should be rated 1000V (the "
            "residential standard for any work near energized equipment per "
            "NFPA 70E). The learner inspects the tool insulation for cuts, "
            "punctures, gouges, melted spots, or exposed metal. INSULATING "
            "GLOVES: the learner identifies the glove's rating (Class 00 "
            "rated 500V is the minimum for residential 240V; higher classes "
            "are acceptable), the inspection date, and the leather protectors. "
            "The learner inspects the glove visually (cuts, punctures, ozone "
            "cracking) and performs the manufacturer's air-roll test where "
            "applicable, with the licensed electrician's coaching the first "
            "time. Gloves that fail any test are removed from service. The "
            "learner explicitly NEVER uses any of these tools or the "
            "multimeter on a live circuit at this band; live measurement is "
            "elc-021 with a licensed electrician physically present."
        ),
        "demonstration_criteria": [
            (
                "Identifies the household multimeter's Category (CAT) rating "
                "and voltage rating from the meter face or manual; names "
                "whether the rating is adequate (CAT III at 600V minimum) for "
                "later 240V residential measurement per NFPA 70E"
            ),
            (
                "Names what each CAT Category is designed to survive (CAT II / "
                "III / IV) and gives one example application of each"
            ),
            (
                "Identifies every range on the meter's selector (AC volts, DC "
                "volts, AC current if present, DC current, resistance, "
                "continuity, diode, capacitance and frequency if present) and "
                "explains in one sentence what each measures"
            ),
            (
                "Identifies the test-lead connectors (COM, V/Ohm, A, mA/uA) "
                "and the standard color coding"
            ),
            (
                "Inspects the test leads visually and reports any damage; "
                "names the rule that damaged leads are removed from service"
            ),
            (
                "Identifies finger-guard probes per IEC 61010-031 on the "
                "household's leads (or names that the leads do not have them "
                "and that finger-guard leads are the standard per NFPA 70E)"
            ),
            (
                "Identifies the meter's current-circuit fuse and names that a "
                "blown fuse removes current-measurement capability; names the "
                "rule that the correct manufacturer fuse is replaced, never a "
                "substitute"
            ),
            (
                "Identifies the IEC 60900 / ASTM F1505 marking on the "
                "household's insulated screwdrivers, pliers, and nut drivers; "
                "names that 1000V-rated is the residential standard per NFPA "
                "70E"
            ),
            (
                "Inspects an insulated tool visually and reports any damage; "
                "names the rule that damaged insulation removes the tool from "
                "energized-work service"
            ),
            (
                "Identifies the household's insulating glove rating (Class 00 "
                "minimum for residential 240V) and inspection date; performs "
                "the manufacturer's air-roll test with the licensed "
                "electrician's coaching"
            ),
            (
                "Names that NO LIVE MEASUREMENT is performed at this band; "
                "live measurement is elc-021 with a licensed electrician "
                "physically present"
            ),
            (
                "Builds a meter-and-tool card for the household's equipment: "
                "meter CAT rating, calibration date if applicable, test-lead "
                "inspection date, insulated tool inventory with ratings, "
                "insulating glove rating and last inspection date"
            ),
        ],
        "common_errors": [
            {
                "error": "Confusing a CAT III 600V rating with a meter rated for 600V general use",
                "cause": "The learner read 600V on the meter and assumed it was just the voltage limit",
                "remedy": (
                    "The Category rating (CAT II / III / IV) is the meter's "
                    "transient-survival design rating, NOT the voltage range. A "
                    "CAT II 1000V meter is rated for 1000V on its working range "
                    "but is designed to survive only CAT II transients; using it "
                    "on a CAT III circuit risks meter failure. Both the Category "
                    "AND the voltage matter. Read both on the meter face."
                ),
            },
            {
                "error": "Using a hobby or automotive meter on a 240V residential circuit",
                "cause": "The learner used the meter in the toolbox without checking the rating",
                "remedy": (
                    "Inexpensive hobby and automotive meters typically lack a CAT "
                    "rating or are CAT II only. They are not acceptable for "
                    "residential 240V work per NFPA 70E. The household upgrades "
                    "to CAT III at 600V minimum before any live measurement is "
                    "performed (elc-021)."
                ),
            },
            {
                "error": "Replacing a blown meter fuse with whatever fits the holder",
                "cause": "The learner did not understand the role of the meter fuse",
                "remedy": (
                    "The meter's current-circuit fuse is a fault-survival "
                    "device. It must be the manufacturer's specified part (often "
                    "a high-rupture-capacity HRC fuse with specific voltage and "
                    "amperage ratings). A substitute fuse can fail to interrupt "
                    "a fault, allowing the fault energy into the user's hand. "
                    "Always the manufacturer's part."
                ),
            },
            {
                "error": "Treating insulating gloves as 'in date forever once bought'",
                "cause": "The learner did not understand that insulating gloves degrade",
                "remedy": (
                    "Insulating gloves degrade with age, oil exposure, ozone, and "
                    "UV. They have a manufacturer-recommended periodic test "
                    "interval (commonly 6 months for in-service gloves; the "
                    "manufacturer and NFPA 70E govern). Gloves are tested before "
                    "each use (visual and air-roll) and periodically by an "
                    "accredited lab per the manufacturer."
                ),
            },
            {
                "error": "Using insulating gloves WITHOUT leather protectors",
                "cause": "The learner found the protectors uncomfortable and removed them",
                "remedy": (
                    "Leather protectors are part of the rated assembly per NFPA "
                    "70E for any work where the insulating glove can be cut or "
                    "punctured. Removing them voids the rated assembly. The "
                    "licensed electrician confirms the protectors are in use on "
                    "every tier-3 act."
                ),
            },
            {
                "error": "Performing live measurement at this band 'just to check'",
                "cause": "The learner forgot the scope boundary",
                "remedy": (
                    "elc-009 is meter and tool LITERACY: identification, "
                    "inspection, and selection. NO LIVE MEASUREMENT is part of "
                    "this band. Live measurement is elc-021 with a licensed "
                    "electrician physically present. The supervising adult on "
                    "premises confirms no live measurement is attempted during "
                    "elc-009 practice."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "A meter-and-tool card for the household's equipment: a "
                "photograph of the household's multimeter showing the CAT "
                "rating clearly; a photograph of the test leads showing the "
                "manufacturer's CAT marking and the finger guards (or naming "
                "the absence of finger guards); photographs of the household's "
                "insulated tools showing the IEC 60900 / ASTM F1505 marking; "
                "a photograph of the insulating gloves showing the rating and "
                "the leather protectors. The card carries each item's "
                "specifications, inspection date, and any deficiencies "
                "identified for upgrade. The AI tutor confirms each "
                "identification and any required upgrade."
            ),
            "what_the_evidence_shows": (
                "That the learner can identify, inspect, and select every "
                "meter and tool needed for elc-021 and beyond, and that the "
                "household's equipment is either adequate to NFPA 70E for "
                "residential work or has been identified for upgrade"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a sample CAT III "
                "multimeter and its manual, naming the CAT rating, the "
                "voltage rating, the range selector, the test-lead "
                "connectors, the finger-guard probes, and the current-"
                "circuit fuse. Then through insulated tools, naming the IEC "
                "60900 / ASTM F1505 marking. Then through insulating gloves, "
                "naming the class and the inspection procedure."
            ),
            "we_do": (
                "The AI tutor and the learner work through the household's "
                "actual equipment together. The learner photographs and "
                "names each item; the AI confirms or corrects. If any "
                "household equipment is inadequate (e.g. a CAT II meter), "
                "the AI flags the upgrade and explains the failure mode."
            ),
            "you_do_supervised": (
                "The learner builds the full meter-and-tool card for the "
                "household, photographing and recording every item. Submits "
                "to the AI tutor for confirmation. The supervising adult on "
                "premises is present only because the learner is in the "
                "household's electrical work area; no live measurement is "
                "attempted."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce a complete meter-and-tool card "
                "across at least two sessions, they may inspect new "
                "equipment unsupervised. The AI tutor remains available for "
                "rating confirmation. Live measurement (elc-021) requires "
                "the licensed electrician physically present regardless of "
                "how fluent the learner becomes at this competency."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 45,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency the AI tutor mentors end-to-end. Meter "
                "and tool literacy is required by NFPA 70E and is the "
                "precondition for the gold-standard elc-021."
            ),
            "certifications_supported": [
                {
                    "id": "elcert-safety",
                    "domains": [
                        "NFPA 70E electrical safe work practices (meter "
                        "selection, insulated tool selection, glove inspection)",
                        "OSHA 29 CFR 1910.137 electrical PPE",
                    ],
                    "notes": (
                        "NFPA 70E training builds directly on this competency; "
                        "the meter and tool habits are universal in trade "
                        "practice."
                    ),
                },
                {
                    "id": "elcert-nec",
                    "domains": [
                        "test instrument requirements per NFPA 70E (referenced "
                        "by the NEC's safe-work-practice context)",
                    ],
                    "notes": "Tested implicitly in journeyman exam scenarios involving live work.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": ["meter and tool literacy at journeyman depth"],
                    "notes": "Universal foundational knowledge.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "elc-021": {
        "node_type": "technique",
        "trade": "electrical",
        "competency_name": (
            "De-energize, lock out / tag out, and perform live-dead-live "
            "verification on a residential branch circuit (apprentice-band "
            "gold standard; ELECTRICAL HAZARD; licensed electrician "
            "physically present at the live moment)"
        ),
        "progression_band": "apprentice",
        "prerequisites": [
            "els-001",
            "elc-001",
            "elc-002",
            "elc-006",
            "elc-007",
            "elc-008",
            "elc-009",
        ],
        "safety_basis": {
            "hazards": [
                (
                    "ELECTROCUTION RISK. Residential branch circuits are typically "
                    "120V/60Hz/1-phase or 240V/60Hz/1-phase in the US; the nameplate "
                    "per elc-001 and the panel labeling are the authorities for the "
                    "specific circuit. Across the heart at residential fault current, "
                    "line voltage can stop the heart. The entire purpose of this "
                    "competency is to verify, with a meter, that the conductors at "
                    "the work point are dead before any further work. A learner who "
                    "skips or mis-performs this competency and then contacts a live "
                    "conductor in a downstream task can be killed."
                ),
                (
                    "ARC FLASH. A short between conductors during energized work "
                    "releases an arc that can cause severe burns and concussive "
                    "injury. Arc-flash hazard on residential 120V and 240V is "
                    "smaller than commercial 480V but real. NFPA 70E governs "
                    "arc-flash boundaries and PPE selection; the default in this "
                    "trade is to de-energize and verify dead before opening any "
                    "enclosure, which removes the arc-flash hazard at the work "
                    "point."
                ),
                (
                    "WRONG-CIRCUIT or WRONG-DISCONNECT FAILURE. A mis-identified or "
                    "mis-operated breaker leaves the wrong circuit dead and the "
                    "intended one live. Panel labels in older or remodeled homes "
                    "are commonly wrong; the verification at the work point is the "
                    "safeguard. The licensed electrician confirms the circuit at "
                    "the work point regardless of the label."
                ),
                (
                    "METER FAILURE. A digital multimeter with a depleted battery, "
                    "a blown fuse, a broken probe lead, or a wrong CAT rating can "
                    "read zero on a live conductor and mislead the user into "
                    "thinking the circuit is dead. The live-dead-live (or "
                    "test-dead-test) sequence per NFPA 70E exists precisely to "
                    "catch this: verify the meter on a known live source FIRST, "
                    "verify dead at the work point, then re-verify the meter on "
                    "the known live source. All three readings must agree with "
                    "the expected state. If the third reading fails, the second "
                    "reading is invalid and the procedure is restarted."
                ),
                (
                    "BACKFEED from a generator or solar PV. Residential standby and "
                    "portable generators connected without a transfer switch or "
                    "interlock per the AHJ-adopted NEC, and residential solar PV "
                    "inverters without proper anti-islanding, can backfeed power "
                    "onto a circuit that the panel main breaker has de-energized. "
                    "Any backfeed source on the property is verified isolated by "
                    "the licensed electrician before any work downstream."
                ),
                (
                    "MULTIWIRE BRANCH CIRCUIT (MWBC) SHARED-NEUTRAL HAZARD. An MWBC "
                    "shares a single neutral conductor between two hot legs of "
                    "opposite phases; opening the neutral on an energized MWBC "
                    "places the full line-to-line voltage across the loads, and "
                    "produces a voltage on the formerly-neutral wire that will "
                    "shock a person who touches it. MWBC identification at the "
                    "panel and the rule against opening the neutral on an "
                    "energized circuit are part of this competency."
                ),
                (
                    "NEUTRAL-TO-GROUND BOND FAULT. The neutral and the ground are "
                    "bonded only at the main service equipment per the AHJ-adopted "
                    "NEC; downstream of the main they must remain separate. A "
                    "fault that places the neutral and ground at different "
                    "potentials at a downstream point can energize metal that is "
                    "normally at ground potential, and the live-dead-live "
                    "verification at the work point may not catch it unless every "
                    "pair of conductors that should be dead is tested."
                ),
                (
                    "STORED ENERGY IN CAPACITORS. Capacitors in motor starters, "
                    "ballasts, switched-mode supplies, and some equipment can "
                    "hold lethal charge for minutes to hours after de-energization. "
                    "Capacitor contact is NOT part of this competency; it is a "
                    "separate competency gated separately."
                ),
                (
                    "WET CONDITIONS. Performing this verification in rain, "
                    "standing water, or on a wet floor significantly increases "
                    "shock risk. The verification is deferred to dry conditions; "
                    "if the situation is urgent, the licensed electrician present "
                    "decides whether to proceed with additional PPE per NFPA 70E "
                    "or to defer."
                ),
                (
                    "SHARP SHEET-METAL EDGES on the panel cover, breaker openings, "
                    "and conductor ends if the cover is removed; cut-resistant "
                    "gloves on for any handling of the cover."
                ),
            ],
            "ppe_required": [
                "Trade PPE per els-001 (closed-toe shoes, the trade's general defaults)",
                "Safety glasses (ANSI Z87.1) required throughout the procedure",
                (
                    "Insulating gloves rated for the voltage actually being "
                    "verified (residential 120V or 240V: Class 00 rated 500V "
                    "minimum per NFPA 70E and the glove manufacturer); inspected "
                    "per the manufacturer and OSHA before use. The licensed "
                    "electrician present confirms the glove rating and the "
                    "inspection."
                ),
                "Leather protectors over insulating gloves per NFPA 70E",
                (
                    "Long sleeves and arc-rated clothing per NFPA 70E for the "
                    "calculated arc-flash incident energy at the work point; the "
                    "licensed electrician present confirms PPE category"
                ),
                "No metal jewelry on hands, wrists, or neck during the procedure",
                (
                    "Multimeter (DMM) with CAT III at minimum rated for 600V or "
                    "higher (CAT IV acceptable), with intact test leads, current "
                    "battery, current fuse, and finger-guard probes per IEC "
                    "61010-031. CAT II or unrated meters are NOT acceptable per "
                    "NFPA 70E."
                ),
                (
                    "Insulated tools (rated 1000V per IEC 60900 / ASTM F1505) for "
                    "any work near energized equipment; the licensed electrician "
                    "confirms"
                ),
                (
                    "Lockout-tagout hardware appropriate to the breaker type: a "
                    "breaker lockout device that fits the breaker handle, a "
                    "padlock that fits the lockout device, a danger tag legible "
                    "per OSHA 1910.145, and the key kept exclusively by the "
                    "person performing the work for the duration of the lockout"
                ),
            ],
            "supervision_required": True,
            "supervision_basis": (
                "ELECTRICAL HAZARD. A licensed electrician (or equivalent "
                "journeyman/master per the AHJ) is PHYSICALLY PRESENT at the "
                "live-dead-live verification. The licensed electrician watches "
                "the meter reading, watches the probe placement, watches the "
                "lockout-tagout sequence, and is in position to intervene "
                "physically if the learner makes a mistake. The AI tutor "
                "mentors the procedure walkthrough on paper and reviews the "
                "artifact evidence (photos of the LOTO setup, written procedure "
                "read-back) but does NOT stand in for the licensed electrician "
                "at the live moment. A learner working alone with only AI "
                "mentoring at the live moment is in mortal danger of "
                "electrocution if the procedure fails, the meter fails, the "
                "wrong meter CAT rating is in hand, the probes slip, the wrong "
                "circuit or disconnect is identified, or a backfeed source is "
                "present (generator, solar PV inverter, MWBC shared neutral, "
                "neutral-to-ground bond fault). This is the one hard line in "
                "the trade's supervision policy. Households without a resident "
                "licensed electrician arrange a paid professional supervision "
                "session, a vocational-school program day, an apprentice "
                "arrangement with a working contractor, or defer the "
                "competency until the qualified human is arranged. The AI "
                "tutor and the supervising adult on premises do NOT substitute "
                "for the licensed electrician at the live moment."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Digital multimeter (DMM) at CAT III for 600V minimum",
                "specification": (
                    "CAT III rated for 600V or higher (CAT IV acceptable); intact "
                    "test leads with finger-guard probes per IEC 61010-031; "
                    "current battery; current fuse on the current-measurement "
                    "range; calibration current per the household's or "
                    "employer's program if applicable. CAT II or unrated meters "
                    "are NOT acceptable per NFPA 70E for residential 240V "
                    "verification."
                ),
                "alternatives": [],
            },
            {
                "name": "A known live voltage source for the live-dead-live verification",
                "specification": (
                    "A standard 120V receptacle near the work area whose live "
                    "status has been confirmed by the licensed electrician, OR "
                    "a manufactured proving unit (also called a voltage tester "
                    "proving unit) that provides a verifiable voltage. The live "
                    "source is used to verify the meter is reading correctly "
                    "BEFORE and AFTER the dead test at the work point. The "
                    "licensed electrician confirms the live source is actually "
                    "live before the learner uses it."
                ),
                "alternatives": [],
            },
            {
                "name": "Breaker lockout device and padlock",
                "specification": (
                    "A device that fits the specific breaker style on the "
                    "household's panel (a single-pole breaker lockout, a "
                    "two-pole breaker lockout for 240V branches, a panel-"
                    "specific lockout for some panel types). A padlock that "
                    "fits the lockout device; key kept exclusively by the "
                    "person performing the work for the duration of the "
                    "lockout."
                ),
                "alternatives": [],
            },
            {
                "name": "Tagout tag",
                "specification": (
                    "A danger tag per OSHA 29 CFR 1910.145, signed and dated by "
                    "the person performing the work, naming the reason for the "
                    "lockout and the date. The tag is attached to the locked "
                    "breaker along with the lock; the tag is NOT a substitute "
                    "for the lock."
                ),
                "alternatives": [],
            },
            {
                "name": "The nameplate cards from elc-001 and the component identification from elc-002",
                "specification": "Used to confirm the expected voltage and identify the correct breaker for the work circuit",
                "alternatives": [],
            },
            {
                "name": "Insulating gloves rated for the voltage",
                "specification": (
                    "Class 00 (rated 500V) or higher per NFPA 70E for residential "
                    "120V or 240V verification, inspected per the manufacturer "
                    "and OSHA before use, with leather protectors. The licensed "
                    "electrician confirms the rating and inspection."
                ),
                "alternatives": [],
            },
            {
                "name": "Safety glasses (ANSI Z87.1)",
                "specification": "Worn throughout the procedure",
                "alternatives": [],
            },
            {
                "name": "Insulated tools rated 1000V per IEC 60900 / ASTM F1505",
                "specification": "For any work near energized equipment during the verification",
                "alternatives": [],
            },
            {
                "name": "Camera (cell phone is sufficient) for the LOTO and procedure photographs",
                "specification": "Used to photograph the locked breaker with the tag attached, for the artifact",
                "alternatives": [],
            },
            {
                "name": "The household's or employer's written lockout-tagout procedure",
                "specification": (
                    "OSHA 29 CFR 1910.147 requires a written, equipment-specific "
                    "LOTO procedure for service work. The household's or "
                    "employer's procedure for the specific panel and circuit is "
                    "read and followed; this node defers to that procedure for "
                    "the specific steps and confirms the procedure exists per "
                    "OSHA. If no written procedure exists for the equipment, "
                    "the licensed electrician present produces one before the "
                    "work begins."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Dry workspace at the panel and at the work point",
            "ventilation": "Adequate; weather conditions dry (no rain, no standing water)",
            "lighting": "Adequate to clearly see the meter face, the test leads, the breaker terminals, and the lockout hardware; portable headlamp commonly required at the panel",
            "power": (
                "Power state is the work itself: the procedure begins with the "
                "circuit energized (to verify the live state), proceeds through "
                "breaker operation and lockout, verifies dead at the work point, "
                "and re-verifies the meter on the known live source after the "
                "dead test. The breaker is restored only after the lockout is "
                "released by the person who applied it and only after the work "
                "for which the lockout was applied is complete."
            ),
            "containment": "Clear floor space at the panel and at the work point; pets and small children excluded from the work area; working space and headroom per the AHJ-adopted NEC at the panel",
        },
        "skill_description": (
            "The learner, with a licensed electrician (or equivalent journeyman / "
            "master per the AHJ) PHYSICALLY PRESENT, performs the live-dead-live "
            "voltage verification on a residential branch circuit using a CAT "
            "III or higher rated digital multimeter and the lockout-tagout "
            "procedure per OSHA 29 CFR 1910.147 and NFPA 70E. The procedure: "
            "(1) review the nameplate from elc-001 and component identification "
            "from elc-002 to confirm the expected voltage and identify the "
            "correct branch and breaker; (2) confirm no active backfeed sources "
            "on the property (generator off and isolated; solar PV inverter "
            "off / no sun / rapid-shutdown engaged per the AHJ-adopted NEC); "
            "(3) put on insulating gloves with leather protectors and safety "
            "glasses; (4) inspect the multimeter, its leads, the lockout "
            "hardware, and the panel working space (headroom and clearance per "
            "the AHJ-adopted NEC); (5) verify the meter on a known live source "
            "(a nearby 120V receptacle confirmed live by the licensed "
            "electrician, or a proving unit), reading the expected voltage; "
            "this is the FIRST live test; (6) operate the branch breaker to "
            "the OFF position; (7) apply the breaker lockout device, the "
            "padlock, and the signed and dated tag, keeping the key "
            "exclusively with the person performing the work; (8) at the work "
            "point (typically a junction box, a receptacle, a switch, or a "
            "fixture base on the circuit), verify voltage is now zero by "
            "testing every pair of conductors that should be dead: for a 120V "
            "branch, test hot-to-neutral, hot-to-ground, and neutral-to-"
            "ground; for a 240V branch, test L1-to-ground, L2-to-ground, "
            "L1-to-L2, L1-to-neutral, and L2-to-neutral; for any MWBC, "
            "additionally test each hot-to-neutral and explicitly confirm "
            "with the licensed electrician that the neutral is NOT shared "
            "with another energized hot; (9) re-verify the meter on the known "
            "live source from step 5, reading the expected voltage; this is "
            "the SECOND live test, confirming the meter is still functioning "
            "correctly and the dead reading from step 8 is valid; (10) "
            "document the verification by photographing the locked breaker "
            "with the tag in place. The circuit is now safe to open for "
            "downstream service work, which is its own competency. The "
            "learner narrates each step aloud as they perform it; the "
            "licensed electrician watches the meter readings, the probe "
            "placements, and the lockout sequence; the licensed electrician "
            "signs off on the verification before any downstream work begins. "
            "At the end of the service work, the lockout is released by the "
            "same person who applied it: tag removed, lock removed, breaker "
            "operated to the ON position, system restored to operating state. "
            "The AI tutor reviews the written procedure, the LOTO photograph, "
            "and the learner's narrated walkthrough after the session; the "
            "AI does NOT replace the licensed electrician at the live moment."
        ),
        "demonstration_criteria": [
            (
                "Reviews the nameplate card from elc-001 and the component "
                "identification from elc-002 BEFORE starting; names the expected "
                "voltage and identifies the correct branch and breaker"
            ),
            (
                "Confirms no active backfeed sources on the property: generator "
                "off and isolated by the transfer switch or interlock per the "
                "AHJ-adopted NEC; solar PV inverter off / no sun / rapid-shutdown "
                "engaged where required by the AHJ-adopted NEC; the licensed "
                "electrician confirms the backfeed isolation"
            ),
            (
                "Inspects the multimeter and leads BEFORE the live test: battery "
                "indicator OK, leads visually intact and finger-guarded, fuse "
                "intact, CAT III at 600V minimum confirmed on the meter face; "
                "the licensed electrician confirms"
            ),
            (
                "Inspects the insulating gloves (visual and air-roll test per "
                "the manufacturer) BEFORE wearing; the licensed electrician "
                "confirms the inspection"
            ),
            (
                "Confirms the panel working space and headroom per the AHJ-"
                "adopted NEC before opening the panel cover; if working space "
                "is inadequate, the work is deferred"
            ),
            (
                "Performs the FIRST live test on the known live source (120V "
                "receptacle confirmed live by the licensed electrician, or a "
                "proving unit), reads the expected voltage, and announces the "
                "reading aloud; the licensed electrician confirms"
            ),
            (
                "Operates the branch breaker to the OFF position correctly per "
                "the panel type"
            ),
            (
                "Applies the breaker lockout device, the padlock, and the "
                "signed and dated tag; keeps the key exclusively with the "
                "person performing the work; the licensed electrician confirms "
                "the lock is properly engaged and the tag is legible per OSHA "
                "1910.145"
            ),
            (
                "Performs the DEAD test at the work point, testing every pair "
                "of conductors that should be dead. For a 120V branch: hot-to-"
                "neutral, hot-to-ground, neutral-to-ground. For a 240V branch: "
                "L1-to-ground, L2-to-ground, L1-to-L2, L1-to-neutral, L2-to-"
                "neutral. For any MWBC: each hot-to-neutral plus explicit "
                "confirmation that the neutral is not shared with another "
                "energized hot. Announces each reading aloud; the licensed "
                "electrician confirms each probe placement and each reading"
            ),
            (
                "Performs the SECOND live test on the same known live source "
                "from the first live test, reads the expected voltage, and "
                "announces the reading aloud; the licensed electrician "
                "confirms the reading and signs off that the dead test from "
                "the previous step is valid"
            ),
            (
                "Photographs the locked breaker with the tag in place and "
                "submits the photo to the AI tutor with a written narration "
                "of every procedure step as performed, countersigned by the "
                "licensed electrician"
            ),
            (
                "Names the rule that the lockout is released ONLY by the "
                "person who applied it, and ONLY after the work for which the "
                "lockout was applied is complete; demonstrates the release "
                "sequence at the end of the practice session (restoring the "
                "breaker to ON) under the licensed electrician's supervision"
            ),
            (
                "Names what would invalidate the dead reading and require "
                "restarting the sequence: meter fails the second live test; "
                "tag or lock disturbed during the work; procedure deviates "
                "from OSHA 1910.147 in any material way; the wrong breaker "
                "is identified mid-procedure; a backfeed source is suspected"
            ),
            (
                "Names that this competency covers ONLY line-voltage "
                "verification at the work point on a residential branch; "
                "low-voltage control circuits are verified separately; the "
                "capacitor discharge competency is separate; service-"
                "entrance work is OUT OF SCOPE at the foundation entirely"
            ),
        ],
        "common_errors": [
            {
                "error": "Skipping the first live test",
                "cause": "The learner felt the procedure was familiar and went straight to the breaker",
                "remedy": (
                    "The live-dead-live sequence is non-negotiable. Without the "
                    "first live test, a dead reading at the work point could "
                    "mean (a) the circuit is really dead OR (b) the meter is "
                    "broken. The first live test rules out (b). The licensed "
                    "electrician halts the procedure and requires the live "
                    "test before the dead test. This is what NFPA 70E mandates."
                ),
            },
            {
                "error": "Skipping the second live test",
                "cause": "The learner read zero at the work point and assumed the meter was still good",
                "remedy": (
                    "The meter could have failed between the first live test "
                    "and the dead test (a blown fuse during a current attempt "
                    "is a classic failure mode). The second live test confirms "
                    "the meter is still functioning AND that the dead reading "
                    "is valid. The licensed electrician requires the second "
                    "live test before the lockout is considered complete."
                ),
            },
            {
                "error": "Testing only hot-to-neutral on a 240V branch",
                "cause": "The learner ran one test and called it done",
                "remedy": (
                    "On a 240V branch, every pair that should be dead must be "
                    "tested: L1-to-ground, L2-to-ground, L1-to-L2, L1-to-"
                    "neutral, L2-to-neutral. Each pair represents a different "
                    "fault possibility. All must read zero."
                ),
            },
            {
                "error": "Trusting a panel label that says BREAKER 12 controls the work circuit",
                "cause": "The learner read the label and threw the breaker; the label was wrong from a remodel",
                "remedy": (
                    "Panel labels in older or remodeled homes are commonly "
                    "wrong. The verification at the work point catches the "
                    "wrong-circuit failure mode. Every elc-021 act verifies "
                    "dead at the work point regardless of label. The label is "
                    "corrected after the verification."
                ),
            },
            {
                "error": "Using a CAT II or unrated meter for the 240V measurement",
                "cause": "The learner used the meter that was in the toolbag without checking the CAT rating",
                "remedy": (
                    "The CAT rating addresses the transient voltage the meter "
                    "is designed to survive. A CAT II meter on a CAT III "
                    "circuit can explode in the user's hand during a fault. "
                    "CAT III at 600V minimum is the rule per NFPA 70E for "
                    "residential 240V measurement. The licensed electrician "
                    "confirms the CAT rating before the procedure begins."
                ),
            },
            {
                "error": "Trusting the breaker position without verifying",
                "cause": "The learner saw the breaker in the OFF position and skipped the meter test",
                "remedy": (
                    "Position is not verification. The breaker could be "
                    "mechanically off but electrically passing voltage (broken "
                    "switch, miswire, backfeed). The meter verification at the "
                    "work point is the only safeguard. Every time."
                ),
            },
            {
                "error": "Leaving the key in the lock or giving it to someone else",
                "cause": "The learner walked away to get a tool and handed the key to the supervising adult",
                "remedy": (
                    "The key is kept EXCLUSIVELY with the person performing "
                    "the work for the duration of the lockout per OSHA "
                    "1910.147. No shared keys, no temporary handoffs. If the "
                    "learner must leave, the lock comes off and the procedure "
                    "is restarted on return."
                ),
            },
            {
                "error": "Performing the procedure in a wet basement after a flood",
                "cause": "The learner saw water on the floor and proceeded anyway",
                "remedy": (
                    "Wet conditions significantly increase shock risk. The "
                    "procedure is deferred to dry conditions. If urgent (a "
                    "real outage from a real flood), the licensed electrician "
                    "decides whether to proceed with additional PPE per NFPA "
                    "70E or to call the utility. The default is to defer."
                ),
            },
            {
                "error": "Opening a junction box on an MWBC without verifying the neutral",
                "cause": "The learner did not recognize the MWBC and assumed neutral was always safe",
                "remedy": (
                    "On an MWBC, opening the neutral on an energized circuit "
                    "produces dangerous voltages. The neutral on every MWBC is "
                    "verified dead at the work point before any contact. The "
                    "licensed electrician identifies the MWBC at the panel and "
                    "walks the verification at the work point."
                ),
            },
            {
                "error": "Reaching for a capacitor or device with stored energy after the disconnect is verified dead",
                "cause": "The learner thought the work point was now fully safe",
                "remedy": (
                    "Some equipment (motor starters, ballasts, switched-mode "
                    "supplies) holds stored charge after de-energization. "
                    "Capacitor contact is a SEPARATE competency, not part of "
                    "elc-021. After the line-voltage dead verification, the "
                    "work point is safe to OPEN; contact with internal "
                    "components requires its own qualifications and "
                    "competencies."
                ),
            },
            {
                "error": "Removing the lock to test a downstream component before completing the work",
                "cause": "The learner felt the procedure was 'paused' and could be resumed",
                "remedy": (
                    "The lockout is in place for the duration of the work. If "
                    "a downstream test requires the system to be energized, "
                    "the lock comes off in the OSHA-compliant sequence (tools "
                    "cleared, personnel cleared, lock removed, breaker "
                    "restored), the test is performed energized, and a NEW "
                    "LOTO sequence is performed before any further work. The "
                    "licensed electrician manages this sequencing."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "A photograph showing: (1) the locked breaker with the padlock "
                "engaged through the breaker lockout device and the signed-"
                "and-dated tag attached; (2) the multimeter display reading the "
                "dead voltage at the work point (the photo can be of the meter "
                "on the leads, with the reading visible) for at least one of "
                "the conductor pairs tested; (3) a separate photo of the meter "
                "reading the live voltage on the known live source, taken "
                "AFTER the dead test (the second live test). Submitted with a "
                "written narration of every step of the procedure as actually "
                "performed, including the announced readings at each test "
                "point. The licensed electrician COUNTERSIGNS the narration."
            ),
            "what_the_evidence_shows": (
                "That the live-dead-live sequence was performed correctly per "
                "NFPA 70E, that the lockout was applied per OSHA 1910.147, "
                "that the dead test covered every conductor pair, and that "
                "the licensed electrician physically present confirmed each "
                "step. The AI tutor reviews the artifact for completeness "
                "against the demonstration criteria; the AI tutor does NOT "
                "countersign the live verification (only the licensed "
                "electrician can do that)."
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The licensed electrician performs the full live-dead-live "
                "verification with formal LOTO on a real residential branch "
                "circuit, narrating each step aloud and explaining why each "
                "step exists: the reason for the first live test (verify the "
                "meter), the reason for the LOTO before the dead test "
                "(defense in depth), the reason for every-pair-to-ground (catch "
                "both-live faults), the reason for the second live test "
                "(verify the meter still works after the dead test), the "
                "reason for the MWBC-specific neutral check (catch the "
                "shared-neutral hazard). The learner watches and the AI tutor "
                "(post-session, on the recorded narration) confirms the "
                "procedure walkthrough matches NFPA 70E and OSHA 1910.147."
            ),
            "we_do": (
                "The licensed electrician and the learner perform the "
                "procedure together on a second real branch. The learner "
                "takes the meter and announces each step; the licensed "
                "electrician watches every probe placement, confirms every "
                "reading, and applies the lock (or watches the learner apply "
                "it). At each transition (live test, breaker off, LOTO "
                "applied, dead test, second live test, lockout released), the "
                "licensed electrician pauses and the learner narrates aloud "
                "what happens next and why."
            ),
            "you_do_supervised": (
                "The learner performs the full procedure on a third real "
                "branch with the licensed electrician physically present, "
                "watching the meter readings, the probe placements, and the "
                "LOTO sequence. The licensed electrician intervenes only if "
                "the learner is about to make a mistake that would "
                "invalidate the verification or create a hazard. After the "
                "procedure, the learner submits the LOTO photograph, the "
                "meter-reading photographs, and the written narration to the "
                "AI tutor; the AI tutor confirms the artifact covers every "
                "demonstration criterion. The licensed electrician countersigns "
                "the narration as having watched the live moment."
            ),
            "you_do_unsupervised": (
                "There is NO unsupervised band for this competency. Every "
                "live-dead-live verification on a real circuit happens with a "
                "licensed electrician physically present. This is the rule "
                "that holds across the trade: the verification of the "
                "absence of voltage is a moment where a meter failure or a "
                "procedure failure can kill, and the licensed electrician is "
                "the safeguard against meter failure and procedure failure. "
                "The learner becomes journeyman-level proficient in this "
                "competency by having performed the verification correctly on "
                "at least ten branches across at least five sessions, with "
                "at least two different licensed electricians countersigning, "
                "and the rule then becomes that the licensed-electrician-"
                "physically-present is the safety habit on every elc-021 act "
                "regardless of the learner's own licensure (per the "
                "credentials_NOT_substitutable_for clause in el-root's "
                "mastery_ladder). The AI tutor continues to mentor the "
                "procedure walkthrough and review artifacts at every band."
            ),
        },
        "estimated_practice_sessions_to_signoff": 10,
        "session_length_minutes": 45,
        "signoff_validity_days": 365,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "apprentice",
            "supervision_rung": "licensed_electrician_physically_present",
            "notes": (
                "Apprentice-band gold standard. ELECTRICAL HAZARD. The "
                "licensed-electrician-physically-present rule is non-negotiable "
                "and unchanged by any credential the learner holds: the "
                "supervision rung stays at licensed-electrician-physically-"
                "present even when the learner themselves holds a state "
                "license, because this is the safety habit, not a credential "
                "gate. Adding the alignment metadata does not weaken any "
                "supervision rule; safety_basis and supervision_basis are the "
                "load-bearing rules."
            ),
            "certifications_supported": [
                {
                    "id": "elcert-safety",
                    "domains": [
                        "lockout-tagout per OSHA 29 CFR 1910.147",
                        "electrical safety practices per OSHA 29 CFR 1910.137 and 1910.335",
                        "NFPA 70E live-dead-live verification",
                        "NFPA 70E PPE selection (insulating gloves, insulated tools, arc-rated clothing)",
                    ],
                    "notes": (
                        "OSHA 10 / 30 covers LOTO and electrical safety as "
                        "orientation; NFPA 70E training covers the verification "
                        "procedure in depth; elc-021 is the demonstrated "
                        "competency."
                    ),
                },
                {
                    "id": "elcert-nec",
                    "domains": [
                        "NEC service-equipment and branch-circuit identification",
                        "NEC working space and headroom at panels",
                        "NEC equipment grounding conductor and bonding (the verification at the work point reads the EGC's role)",
                    ],
                    "notes": "Every NEC chapter touching service work assumes live-dead-live competence.",
                },
                {
                    "id": "elcert-licensing",
                    "domains": [
                        "NFPA 70E live-dead-live procedure and PPE at journeyman "
                        "and master depth",
                        "AHJ-adopted code application during service work",
                    ],
                    "notes": (
                        "The state journeyman and master exams test the "
                        "live-dead-live discipline and the PPE selection "
                        "directly."
                    ),
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                "OSHA 29 CFR 1910.147 (The Control of Hazardous Energy / Lockout-Tagout)",
                "OSHA 29 CFR 1910.145 (Specifications for Accident Prevention Signs and Tags)",
                "OSHA 29 CFR 1910.137 (Electrical Protective Equipment)",
                "OSHA 29 CFR 1910.335 (Electrical Safety-Related Work Practices)",
                "NFPA 70E (Standard for Electrical Safety in the Workplace; current edition)",
                "NFPA 70 (NEC; current edition adopted by the local AHJ)",
                "IEC 61010-1 / UL 61010-1 (test and measurement equipment Category Ratings: CAT II / III / IV)",
                "IEC 61010-031 (handheld probe finger-guard requirements)",
                "IEC 60900 / ASTM F1505 (Insulated and Insulating Hand Tools)",
                "The household's or employer's written equipment-specific lockout-tagout procedure per OSHA 1910.147",
                "Manufacturer service literature for the specific multimeter, insulating gloves, lockout hardware, and panel equipment",
                "The licensed electrician's professional license per the local AHJ and current NFPA 70E familiarity",
            ],
        },
    },
}
