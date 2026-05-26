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
}
