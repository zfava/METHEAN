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
}
