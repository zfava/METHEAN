"""HVAC trade content (intro to master technician, mastery path).

Three node shapes live here per docs/curriculum/METHEAN_trades_design.md:
the trade root (hvac-root), one safety competency (hs-001), and many
technique competencies (hc-NNN). Trades do not carry the five-philosophy
block; they carry a single apprenticeship pedagogy block. Safety is
gating: every hands-on competency prereqs the entry safety node hs-001.

The starting set authored here is bottom-up from safety. hc-021 (use a
digital multimeter with formal lockout-tagout to verify the absence of
voltage at a residential AC condenser disconnect) is the gold-standard
exemplar, authored at the apprentice band, after its helper-band
prerequisites hc-001 (read a nameplate) and hc-002 (identify components
by sight) and the trade safety competency hs-001.

Hazard posture: HVAC is a higher-hazard trade. The safety content is
authored thoroughly. The gold-standard apprentice node carries an
electrical hazard and is marked supervision_required:true and
safety_review.reviewed:false; it must be cleared by a licensed HVAC
technician or licensed electrician before surfacing. Refrigerant
handling (EPA Section 608), gas/combustion work, brazing, recovery and
recycling, rooftop work, and confined-space work are deliberately NOT
in this first batch and will each be authored behind their own safety
gates.

Mentorship framing: the AI tutor mentors knowledge competencies
(nameplate reading, component identification, code interpretation,
procedure walkthroughs, artifact review) end-to-end. For low-hazard
hands-on work an adult on premises (parent or other adult; no HVAC
credentials required for the walkthrough itself) supervises. For
higher-hazard hands-on work on an electrical, refrigerant, gas,
combustion, rooftop, or confined-space subsystem, a qualified human
named per subsystem (licensed electrician for line voltage;
EPA-608-certified person for refrigerant; licensed gas fitter for gas
piping per the AHJ; OSHA-defined competent person for fall protection)
is physically present at the work. The AI tutor does not stand in for
the human at the moment of the hazardous act.

Goal framing: this is a mastery path. The portfolio of demonstrated
work is the artifact. Certification (EPA-608, journeyman license,
NATE certification) is not the immediate gate; it is a later step the
learner may take when ready. The NodeType.certification_prep slot
stays open for trades whose end-state is a credential, but this trade
is mastery-first.

Regulated topics defer to recognized standards by name: OSHA 29 CFR
1910.147 (LOTO), 1910.146 (confined spaces), 1910.137 and 1910.335
(electrical safety practices), 1926 Subpart M (fall protection); NFPA
70E (electrical safety in the workplace); NFPA 70 (NEC); NFPA 54
(National Fuel Gas Code); EPA Section 608 (refrigerant); ASHRAE
Standard 34 (refrigerant classification); ASHRAE 62.1 / 62.2
(ventilation); AHRI equipment-rating standards; ANSI/ISEA Z308.1
(first aid); CDC carbon-monoxide guidance; CDC and EPA asbestos
guidance; manufacturer service literature for the specific equipment;
and the local AHJ adopted codes. No node invents a torque value, a
charge amount, a code citation, a CO action level, or a refrigerant
rule beyond what these standards supply.
"""

HVAC_CONTENT: dict[str, dict] = {
    "hvac-root": {
        "node_type": "root",
        "trade": "hvac",
        "trade_name": "HVAC (intro to master technician, mastery path)",
        "description": (
            "The HVAC trade taught from intro toward mastery: read an equipment "
            "nameplate, identify components by sight, change filters and clean "
            "condenser coils, verify the absence of voltage with formal "
            "lockout-tagout before any service, take static-pressure and "
            "temperature-rise readings, troubleshoot a no-cooling or no-heat call. "
            "Refrigerant handling (EPA-608 regulated), gas-system work, brazing, "
            "recovery and recycling, rooftop work, and confined-space work each "
            "enter behind their own safety gate, not authored in this first batch. "
            "The trade is foundational across the building's mechanical systems; "
            "every house has it, every commercial space has it, every learner who "
            "lives indoors benefits from understanding it. The path is mastery, "
            "demonstrated by a portfolio of real diagnostic and service work; "
            "certification (EPA-608, journeyman, NATE) is a later step the learner "
            "may take when ready, not the immediate gate."
        ),
        "default_supervision_policy": {
            "knowledge_work": (
                "AI tutor mentors end-to-end. Nameplate reading, component "
                "identification from photographs, code interpretation, procedure "
                "walkthroughs on paper, troubleshooting trees, artifact review of "
                "the learner's uploaded photos and videos. No human required. The "
                "knowledge competencies are where the AI tutor carries the bulk of "
                "the mentoring work."
            ),
            "low_hazard_hands_on_work": (
                "Adult on premises. A parent or other resident adult is in the room "
                "or on the property; the adult does not need HVAC credentials for "
                "this category. The AI tutor guides the learner step by step. "
                "Filter changes on a de-energized system, condensate trap cleaning, "
                "register and grille cleaning, exterior condenser cleaning with a "
                "soft brush (no chemicals, no fin combing) belong here. Not "
                "authored in this first batch."
            ),
            "higher_hazard_hands_on_work": (
                "Qualified human physically present at the work, where qualified is "
                "named per subsystem. For line-voltage electrical work: licensed "
                "electrician OR licensed HVAC technician with electrical scope "
                "(jurisdiction-dependent). For refrigerant work: a person holding "
                "the EPA-608 certification appropriate to the refrigerant being "
                "handled (Type I, II, III, or Universal). For gas-system work: "
                "licensed gas fitter or HVAC technician with gas scope per the "
                "local AHJ; gas piping work additionally per NFPA 54. For "
                "combustion startup and analysis: a person with the manufacturer's "
                "startup procedure and a calibrated combustion analyzer who has "
                "performed the operation. For rooftop work: an OSHA-defined "
                "competent person for fall protection per 29 CFR 1926.32 and "
                "Subpart M. For confined-space entry: a trained entrant and "
                "attendant per OSHA 29 CFR 1910.146 with the written program in "
                "place. The AI tutor mentors the procedure walkthrough, the "
                "artifact review, and the grading, but does NOT stand in for the "
                "qualified human at the moment of the hazardous act."
            ),
            "households_without_a_resident_qualified_mentor": (
                "Common in this trade. For the higher-hazard hands-on competencies, "
                "the household arranges: a paid professional supervision session "
                "(an HVAC technician or electrician hired for a defined block of "
                "time at a specific competency); a vocational-school program day "
                "or open-shop hours; an apprentice or shadow arrangement with a "
                "working contractor; or defers the hands-on competency until the "
                "learner reaches a community-college HVAC program where the "
                "qualified-human-present requirement is built into the program. "
                "The knowledge-work bands the AI tutor mentors are accessible "
                "throughout; the hands-on hazardous bands are gated until the "
                "qualified human is arranged."
            ),
            "all_bands": (
                "Power tools (drills, sheet-metal shears, brake) and any operation "
                "that opens an enclosure containing refrigerant, gas, or live "
                "conductors are supervised. The supervision band (helper, "
                "apprentice, journeyman) defines how close the supervision is, not "
                "whether it exists. No unsupervised hands-on work on hazardous "
                "subsystems below the qualified band."
            ),
        },
        "safety_node": "hs-001",
        "progression_bands": ["helper", "apprentice", "journeyman", "qualified"],
        "mastery_ladder": {
            "framing": (
                "Mastery in this trade is demonstrated competence PLUS a real portfolio of "
                "work AND readiness for the relevant external credentials. Portfolio and "
                "credential are complementary, not alternatives: a learner with a portfolio "
                "but no credential cannot legally do regulated work; a learner with a "
                "credential but no portfolio is not yet competent. The ladder below places "
                "each authored competency on its band and places each certification at the "
                "point in the ladder where a learner is genuinely ready for it. The ladder is "
                "the surface read by the planner and rendered in the per-trade map document "
                "(docs/curriculum/HVAC_certification_and_mastery_map.md)."
            ),
            "rungs": [
                {
                    "rung_name": "helper",
                    "mastery_level_alias": "emerging",
                    "what_the_learner_does": (
                        "Assists a working mentor. Reads nameplates and component layouts. "
                        "Walks the shop's safety with an adult on premises. Does not yet "
                        "open enclosures, touch live electrical, handle refrigerant, or open "
                        "gas systems. Begins study toward OSHA 10 orientation."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor end-to-end (knowledge work)",
                        "Adult on premises (safety walkthrough, low-hazard hands-on)",
                    ],
                    "knowledge_competencies": ["hc-001", "hc-002"],
                    "safety_competencies": ["hs-001"],
                    "low_hazard_hands_on_competencies": [
                        "filter change, condensate trap cleaning, exterior condenser cleaning (not yet authored; future batch)",
                    ],
                    "higher_hazard_hands_on_competencies": [],
                    "certifications_appropriate_here": [
                        {
                            "id": "hcert-osha",
                            "specific_credential": "OSHA 10-Hour Outreach (General Industry or Construction)",
                            "rationale": (
                                "Common employer entry prerequisite; reinforces the safety "
                                "vocabulary used in hs-001 and prepares the learner for the "
                                "next bands."
                            ),
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "Nameplate cards (one per piece of household HVAC equipment, per hc-001)",
                        "Component identification cards (outdoor unit and indoor air handler, per hc-002)",
                        "Recorded safety walkthrough video (per hs-001)",
                    ],
                },
                {
                    "rung_name": "apprentice",
                    "mastery_level_alias": "developing",
                    "what_the_learner_does": (
                        "Performs most steps with a mentor checking key cuts, joints, "
                        "connections, and (for higher-hazard subsystems) with a qualified "
                        "human physically present. Begins live-dead-live verification at the "
                        "disconnect (hc-021) under a licensed electrician or licensed HVAC "
                        "technician. Earns EPA Section 608 (study-only) as a precondition "
                        "for any later hands-on refrigerant work. Earns OSHA 30 if taking on "
                        "lead responsibility. Begins entry-level NATE certifications."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor (knowledge work, certification study, procedure walkthrough, artifact review)",
                        "Adult on premises (low-hazard hands-on)",
                        "Qualified human physically present (electrical verification per hc-021, and any other hazardous-subsystem work as it enters the band)",
                    ],
                    "knowledge_competencies": [
                        "advanced nameplate interpretation (capacity, latent vs sensible, derating); refrigeration cycle theory; psychrometrics; controls schematics (not yet authored; future batches)",
                    ],
                    "safety_competencies": ["hs-001 (current per the annual freshness check)"],
                    "low_hazard_hands_on_competencies": [
                        "static-pressure measurement, temperature-rise measurement, condensate-line clearing, capacitor-discharge with qualified human present (future batches)",
                    ],
                    "higher_hazard_hands_on_competencies": [
                        "hc-021 (DMM + LOTO live-dead-live verification at residential disconnect; qualified human physically present)",
                    ],
                    "certifications_appropriate_here": [
                        {
                            "id": "hcert-epa608",
                            "specific_credential": "EPA Section 608 Type I, Type II, or Universal (per the equipment the learner expects to work on; legally required before any hands-on refrigerant work)",
                            "rationale": (
                                "Study-only credential that the learner can earn before any "
                                "hands-on refrigerant work; it is the legal precondition for "
                                "that work in the United States."
                            ),
                        },
                        {
                            "id": "hcert-osha",
                            "specific_credential": "OSHA 30-Hour Outreach (when the learner takes on lead or supervisory work)",
                            "rationale": "Deeper version of OSHA 10 for workers with supervisory responsibility.",
                        },
                        {
                            "id": "hcert-nate",
                            "specific_credential": "NATE entry-level certifications (Ready to Work, HVAC Support Technician)",
                            "rationale": "Industry-recognized acknowledgment of basic readiness.",
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "Live-dead-live verification photographs and written narration with qualified-human countersignature (per hc-021)",
                        "EPA Section 608 certification card (held by the learner; obtained from an EPA-approved certifying body)",
                        "OSHA Outreach completion card if taken at this band",
                    ],
                },
                {
                    "rung_name": "journeyman",
                    "mastery_level_alias": "proficient",
                    "what_the_learner_does": (
                        "Completes a competency independently to acceptable quality. Mentor "
                        "available but not required step by step. For higher-hazard "
                        "subsystems, the learner now holds the credentials that authorize "
                        "the hands-on work (EPA 608 for refrigerant; state journeyman "
                        "license per the AHJ for HVAC scope where licensing is required), "
                        "and the qualified-human-present rule from the apprentice band "
                        "shifts to the experienced-journeyman-available rule for live "
                        "electrical work. The learner is now ready to sit the AHJ's "
                        "journeyman exam (if not already taken at the close of the "
                        "apprentice band) and to pursue NATE core / specialty "
                        "certifications in their chosen subsystems."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor (continuing-education study, certification preparation, code lookup, artifact review)",
                        "Working mentor available but not required step by step (for routine work)",
                        "Qualified human present (for unusual hazards, first time on a new equipment family, or any work outside the learner's licensed scope)",
                    ],
                    "knowledge_competencies": [
                        "diagnostic frameworks; load calculations (Manual J); equipment selection (Manual S); duct design (Manual D); commercial controls; combustion analysis (knowledge level) (future batches)",
                    ],
                    "safety_competencies": ["hs-001 (current per the annual freshness check)"],
                    "low_hazard_hands_on_competencies": [
                        "complete maintenance call (system check, filter, condensate, coil clean, voltage and amperage check); customer write-up (future batches)",
                    ],
                    "higher_hazard_hands_on_competencies": [
                        "refrigerant operations under EPA 608 with own certification; capacitor work; complete service call on a refrigeration fault; gas-system service under state gas license (future batches; each gated separately)",
                    ],
                    "certifications_appropriate_here": [
                        {
                            "id": "hcert-licensing",
                            "specific_credential": "State journeyman HVAC license per the AHJ",
                            "rationale": (
                                "Earned after completing the AHJ's apprenticeship hours "
                                "requirement through a recognized apprenticeship and "
                                "passing the AHJ's journeyman exam. The learner is now "
                                "legally authorized to perform HVAC work within the scope "
                                "the license names."
                            ),
                        },
                        {
                            "id": "hcert-nate",
                            "specific_credential": "NATE Core plus one or more specialty certifications (air conditioning, gas heating, heat pumps, light commercial refrigeration, etc.)",
                            "rationale": "Industry-recognized acknowledgment of competence in a chosen subsystem.",
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "Complete service-call write-ups across the chosen specialty",
                        "State journeyman HVAC license (obtained from the AHJ)",
                        "NATE core and specialty certification cards (obtained from NATE)",
                    ],
                },
                {
                    "rung_name": "qualified",
                    "mastery_level_alias": "mastered",
                    "what_the_learner_does": (
                        "Performs reliably under varied conditions across the chosen "
                        "subsystems. Teaches helpers and apprentices through the helper-band "
                        "steps of those subsystems. Holds the AHJ's master / contractor "
                        "license where applicable, with the bonding, insurance, and "
                        "continuing-education the AHJ requires. Pursues NATE senior-level "
                        "certification where it advances the learner's chosen specialty. "
                        "Maintains EPA 608 (no renewal currently required by EPA but the "
                        "card is kept on the person for refrigerant work) and NFPA 70E "
                        "currency. Carries the qualified-human-present role for the next "
                        "generation of learners."
                    ),
                    "mentor_models_in_use": [
                        "AI tutor (continuing-education, code-update tracking, master exam preparation, artifact review)",
                        "Peer review (other masters / contractors)",
                        "Learner now MENTORS others as the qualified human present for their hazardous-subsystem work",
                    ],
                    "knowledge_competencies": [
                        "advanced controls and building automation; commercial design; load and energy modeling; project management; business and contract law (master / contractor level) (future batches)",
                    ],
                    "safety_competencies": [
                        "hs-001 (current per the annual freshness check; learner now leads the walkthrough for helpers)"
                    ],
                    "low_hazard_hands_on_competencies": [
                        "full design-and-install of a residential system (future batch; a project node)",
                    ],
                    "higher_hazard_hands_on_competencies": [
                        "complete residential or light-commercial install; commercial refrigeration service; full combustion startup and tuning (future batches; each gated separately)",
                    ],
                    "certifications_appropriate_here": [
                        {
                            "id": "hcert-licensing",
                            "specific_credential": "State master / contractor HVAC license per the AHJ",
                            "rationale": (
                                "Earned after the journeyman experience requirement the AHJ "
                                "publishes, plus business / law exam in many states, plus "
                                "bonding and insurance per the AHJ."
                            ),
                        },
                        {
                            "id": "hcert-nate",
                            "specific_credential": "NATE Senior Efficiency Analyst (or other current NATE senior-level certifications) per the chosen specialty",
                            "rationale": "Top-tier industry recognition; signals mastery to employers, contractors, and customers.",
                        },
                    ],
                    "portfolio_artifacts_built_here": [
                        "State master / contractor HVAC license (obtained from the AHJ)",
                        "NATE senior-level certification (obtained from NATE)",
                        "A full project portfolio (residential install, commercial service, training-of-apprentice records)",
                        "Continuing-education currency in NFPA 70E and the local AHJ's continuing-education requirements",
                    ],
                },
            ],
            "mastery_marker": (
                "The learner is qualified when: (1) every authored competency in the chosen "
                "specialty has been demonstrated at the proficient or mastered band with "
                "portfolio artifacts; (2) the legally required credentials for the work the "
                "learner intends to do are held (EPA 608 for any refrigerant work; state "
                "journeyman or master license per the AHJ for the work the AHJ regulates); "
                "(3) the learner has either signed off a helper-band attempt for another "
                "learner OR completed a journeyman-band project entirely unsupervised, per "
                "the trades design's qualified-band signoff rule."
            ),
            "credentials_NOT_substitutable_for": [
                (
                    "EPA Section 608 certification does NOT substitute for the supervision "
                    "policy on hands-on refrigerant work; a 608-certified learner still "
                    "performs first hands-on refrigerant operations under a working "
                    "608-certified mentor per the trade's apprenticeship pedagogy."
                ),
                (
                    "State HVAC license does NOT substitute for the specific safety "
                    "competencies (e.g. hc-021 live-dead-live verification); license-holders "
                    "still perform live-dead-live verification on every service call as the "
                    "competency teaches, because the verification is the safety habit."
                ),
                (
                    "NATE certifications do NOT substitute for EPA Section 608, do NOT "
                    "substitute for state licensing, and do NOT change any supervision rule."
                ),
                (
                    "OSHA 10 / 30 Outreach completion does NOT substitute for site-specific "
                    "or task-specific safety training required by particular OSHA standards "
                    "(LOTO, fall protection, confined-space entry); those remain the "
                    "employer's responsibility under OSHA's specific-training requirements."
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
    "hs-001": {
        "node_type": "safety",
        "trade": "hvac",
        "competency_name": (
            "HVAC safety: electrical (line and low voltage), refrigerant handling and classification, "
            "combustion gases and CO, thermal (hot surfaces and refrigerant burns), falls and ladders, "
            "lifting and sheet-metal edges, confined spaces, asbestos awareness, and IAQ contaminants"
        ),
        "progression_band": "helper",
        "prerequisites": [],
        "safety_basis": {
            "hazards": [
                (
                    "Electrical shock and electrocution from line voltage (residential typically "
                    "240V/60Hz/1-phase at the outdoor unit and 120V/60Hz/1-phase at the air handler "
                    "in the US; commercial systems run 208V/3-phase or 480V/3-phase; the nameplate "
                    "is the authority per hc-001). At residential fault current, 240V across the "
                    "heart can stop it. The line-voltage hazard governs every service action that "
                    "opens an enclosure; the absence of voltage is verified before any contact with "
                    "the wiring per hc-021."
                ),
                (
                    "Electrical shock from stored energy in start and run capacitors. Capacitors "
                    "in HVAC equipment can hold a lethal charge for minutes to hours after the "
                    "system is de-energized; they are discharged with a resistor of the "
                    "manufacturer-specified value before any direct contact. Capacitor discharge "
                    "is its own competency, not authored in this first batch."
                ),
                (
                    "Arc flash from a short during energized work. Boundaries on residential "
                    "equipment are smaller than commercial but real; arc-rated PPE per NFPA 70E "
                    "applies to any work inside an energized enclosure. The default in this trade "
                    "is to de-energize and verify dead before opening."
                ),
                (
                    "Low-voltage control circuits (typically 24VAC in residential and light "
                    "commercial) carry shock risk that is lower than line voltage but real, and "
                    "can cause an involuntary reaction (jerk a hand into a fan blade or a sharp "
                    "edge). The control circuit is treated as live until verified dead."
                ),
                (
                    "Refrigerant exposure. Modern residential refrigerants are typically "
                    "ASHRAE 34 class A1 (non-flammable, low toxicity; R-410A is the dominant A1 "
                    "in residential through the 2020s) or class A2L (lower-flammability, low "
                    "toxicity; R-454B and R-32 are A2L refrigerants replacing R-410A in new "
                    "residential equipment under the AIM Act and EPA SNAP transitions). A2L "
                    "refrigerants have ignition risk in the right concentration and require "
                    "different leak-detection and ventilation practices than A1. The refrigerant "
                    "type on the nameplate governs; ASHRAE 34 supplies the safety class; the "
                    "manufacturer's service literature supplies the operational rules; the "
                    "refrigerant's Safety Data Sheet supplies PPE. Hands-on refrigerant work is "
                    "regulated by EPA Section 608 (Clean Air Act): a person without the "
                    "appropriate certification (Type I, II, III, or Universal) may not legally "
                    "open, charge, recover, or service systems containing refrigerant. Refrigerant "
                    "work is not authored in this first batch."
                ),
                (
                    "Frostbite from direct skin contact with escaping refrigerant. A high-pressure "
                    "refrigerant release can flash off and reach temperatures below freezing on "
                    "contact, causing severe burns to skin and eyes within seconds. PPE includes "
                    "leather gloves and safety glasses (or face shield, per the refrigerant and "
                    "the operation); refrigerant operations are conducted with the manufacturer's "
                    "and ASHRAE 34's PPE guidance for the specific class."
                ),
                (
                    "Thermal burns from hot surfaces. Furnace heat exchangers, vent pipes, and "
                    "draft inducer motors run hot enough to burn skin on contact during and shortly "
                    "after operation. Brazed joints during refrigerant work reach temperatures "
                    "that can ignite combustibles and cause serious burns; brazing is not authored "
                    "in this first batch and has its own gate."
                ),
                (
                    "Carbon monoxide (CO) poisoning from incomplete combustion of natural gas, "
                    "propane (LP), or fuel oil. CO is colorless and odorless; symptoms (headache, "
                    "dizziness, nausea) precede unconsciousness and death. A working CO alarm in "
                    "the home is required by code in most US jurisdictions; the alarm placement "
                    "follows current NFPA 720 and the local AHJ. Any CO alarm activation during "
                    "service is a stop-work event. CO action levels and recognition follow current "
                    "CDC guidance; the node does not name action-level ppm without a verified "
                    "current source."
                ),
                (
                    "Natural gas (NG) and propane (LP) leaks. The added odorant (mercaptan) gives "
                    "NG and LP a strong sulfur smell at small concentrations; any smell of gas is "
                    "a stop-work event, the area is ventilated, ignition sources (including "
                    "switches, phones, and the technician's vehicle key in the ignition) are not "
                    "operated in the area, and the gas utility's emergency line is called per the "
                    "utility's instructions. Gas-system work is regulated under NFPA 54 and the "
                    "local AHJ; it is not authored in this first batch."
                ),
                (
                    "Falls from ladders, rooftops, and elevated air-handler platforms. Rooftop "
                    "HVAC work is subject to OSHA 29 CFR 1926 Subpart M (fall protection); a "
                    "fall arrest system or guardrail per OSHA is required above the threshold "
                    "height. Ladder use follows OSHA 1910.23 (walking-working surfaces) and the "
                    "ladder manufacturer's duty rating. Rooftop and ladder competencies are not "
                    "authored in this first batch."
                ),
                (
                    "Lifting injuries. Compressors, condensers, air handlers, and packaged units "
                    "weigh from 50 lb (small residential air handler) to several hundred lb "
                    "(commercial packaged unit). Two-person lifts and mechanical assists (a hand "
                    "truck, a lift gate, a hoist) are the rule; one-person lifts of heavy "
                    "equipment cause back injuries. Lifting form follows current OSHA / NIOSH "
                    "lifting guidance."
                ),
                (
                    "Sheet-metal edge cuts. Sharp edges on ductwork, equipment enclosures, panels, "
                    "and drain pans cause hand and forearm cuts; per industry observation, "
                    "sheet-metal cuts are among the most frequent HVAC injuries. Cut-resistant "
                    "gloves are the default in this trade for any sheet-metal handling."
                ),
                (
                    "Eye injury from metal swarf (sheet-metal work), insulation fibers (fiberglass "
                    "duct liner, batt insulation in attics), and refrigerant or chemicals. Safety "
                    "glasses are the default in this trade for any work inside an enclosure; a "
                    "face shield for chemicals or refrigerant operations per the SDS."
                ),
                (
                    "Confined-space exposure. Crawl spaces, attics in summer, mechanical rooms "
                    "with poor ventilation, and packaged-unit interiors are confined or "
                    "potentially confined spaces. OSHA 29 CFR 1910.146 governs permit-required "
                    "confined space entry; the written program, attendant, gas testing, and "
                    "rescue plan are required. Confined-space work is not authored in this first "
                    "batch."
                ),
                (
                    "Asbestos in pre-1980 systems. Duct tape mastic, boiler insulation, pipe "
                    "lagging, gasket material, and some furnace components manufactured before "
                    "1980 may contain asbestos. Visual identification is unreliable. Disturbing "
                    "suspect material releases respirable fibers. EPA and state asbestos rules "
                    "govern; pre-1980 system components are treated as suspect until tested by a "
                    "qualified inspector. No cutting, scraping, or replacing of suspect material "
                    "in this batch."
                ),
                (
                    "Indoor air quality contaminants. Mold in coil pans and ducts, bacterial "
                    "growth in standing condensate, rodent and bird debris in attic equipment, "
                    "and accumulated dust in unmaintained systems can all cause respiratory "
                    "exposure during service. N95 (or higher per the contaminant) respirator is "
                    "the default for any work in a system with visible biological growth or "
                    "accumulated debris."
                ),
                (
                    "Pinch points and rotating equipment. Blower wheels, condenser fans, draft "
                    "inducers, and compressor pulleys (on older belt-drive equipment) all "
                    "present pinch and entanglement hazards. Power is verified off per hc-021 "
                    "before any contact with rotating equipment; loose clothing, jewelry, and "
                    "long hair are controlled before work begins."
                ),
                (
                    "Fire hazard during brazing, soldering, and any hot work. The work area is "
                    "cleared of combustibles, a fire watch is in place per the operation, and a "
                    "fire extinguisher rated for the hazards present (the household confirms the "
                    "appropriate rating with a local fire-safety authority; A:B:C is the "
                    "conservative default in the absence of a specific local recommendation) is "
                    "within reach. Hot work is not authored in this first batch."
                ),
            ],
            "ppe_required": [
                (
                    "Closed-toe leather work boots with non-slip soles; steel-toe or composite-toe "
                    "is required for any lifting of equipment or work where a dropped tool or "
                    "part is a hazard. No sneakers in the mechanical room or on a rooftop."
                ),
                (
                    "Safety glasses (ANSI Z87.1) as the shop-wide default any time an enclosure is "
                    "open, any time sheet metal is handled, and any time a refrigerant or chemical "
                    "operation is performed. A full face shield (in addition to safety glasses) "
                    "for refrigerant operations per the refrigerant's SDS and ASHRAE 34, for "
                    "battery work, and for any chemical operation per the SDS."
                ),
                (
                    "Cut-resistant gloves (ANSI/ISEA 105 cut level A4 or higher recommended for "
                    "general sheet-metal handling; the actual cut level is the household's or "
                    "employer's call per the actual work; this node names the cut-rated "
                    "requirement without prescribing a specific level)."
                ),
                (
                    "Insulating gloves rated for the voltage actually being worked are required "
                    "for any energized electrical work per NFPA 70E. The default in this trade is "
                    "to de-energize and verify dead before contact (per hc-021); energized work "
                    "requires the rated gloves AND the arc-rated PPE for the calculated incident "
                    "energy AND a documented energized-work justification per NFPA 70E. Energized "
                    "work is not in this batch."
                ),
                (
                    "Hearing protection (ANSI/ASA S3.19 rated earplugs or muffs) in any space with "
                    "running equipment loud enough to require raised voice to converse, per "
                    "current OSHA / NIOSH occupational noise exposure guidance."
                ),
                (
                    "Respiratory protection (N95 or higher per the contaminant, per current NIOSH "
                    "guidance and the local AHJ) for any work in dust, biological contamination, "
                    "fiberglass insulation in confined attics, or chemical operations per the SDS. "
                    "Respirator fit-testing applies if the household or employer's program "
                    "requires it; the node names the requirement without prescribing the test."
                ),
                (
                    "Fall protection per OSHA 29 CFR 1926 Subpart M for any work above the "
                    "OSHA-defined threshold. The personal fall arrest system (harness, lanyard, "
                    "anchor) is inspected before each use per the manufacturer and OSHA. Rooftop "
                    "and elevated work is not authored in this first batch; the requirement is "
                    "named here so it is in the safety walkthrough."
                ),
                (
                    "Long sleeves rolled down for any work near hot surfaces, brazing, or "
                    "biological contamination; hair tied back if long enough to fall into a fan "
                    "or onto a hot surface; no loose jewelry near rotating equipment or live "
                    "electrical."
                ),
                (
                    "Sun protection (brimmed hat, long sleeves, sunscreen per current public-health "
                    "guidance) for any outdoor or rooftop work in warm months; hydration per "
                    "current CDC / NIOSH outdoor-worker heat-illness guidance."
                ),
            ],
            "supervision_required": True,
            "supervision_basis": (
                "The safety competency is itself supervised: an adult on premises walks the "
                "learner through every hazard in the actual mechanical room, the actual "
                "equipment, and the actual tool kit, and signs off only when the learner can "
                "name and locate each. The supervising adult does not need HVAC credentials for "
                "the walkthrough itself; a parent or other resident adult counts. The AI tutor "
                "may guide what to look for and review the recorded walkthrough video. There is "
                "no self-attestation on safety. The mentor confirms the household's plans for "
                "tetanus immunization status (per each household member's healthcare provider), "
                "CO alarm presence and function (per current NFPA 720 and the local AHJ), fire "
                "extinguisher rating and placement (the household confirms the appropriate "
                "rating with a local fire-safety authority; A:B:C is the conservative default), "
                "first aid kit (per ANSI/ISEA Z308.1 or current American Red Cross guidance), "
                "and the household's understanding that higher-hazard hands-on work on "
                "electrical, refrigerant, gas, combustion, rooftop, or confined-space subsystems "
                "requires a qualified human physically present per the trade root's supervision "
                "policy."
            ),
            "fresh_safety_signoff_within_days": None,
        },
        "tools_required": [
            {
                "name": "First aid kit",
                "specification": (
                    "A kit that meets a recognized standard for first-aid contents: ANSI/ISEA "
                    "Z308.1 (Minimum Requirements for Workplace First Aid Kits and Supplies) or "
                    "current American Red Cross guidance for home/shop kits. The authoritative "
                    "contents list is the named standard, not this node. At minimum the kit will "
                    "contain items such as adhesive bandages, gauze pads, medical tape, "
                    "antiseptic wipes, and tweezers; the standard supplies the full list. The "
                    "kit accompanies the work area; on a service call, the kit is in the truck."
                ),
                "alternatives": [],
            },
            {
                "name": "Working CO alarm in the home or mechanical space",
                "specification": (
                    "A CO alarm meeting UL 2034 (residential) or UL 2075 (commercial) listed and "
                    "placed per current NFPA 720 and the local AHJ. The alarm's installation date "
                    "and replacement schedule are tracked per the manufacturer (CO sensors have a "
                    "limited service life, typically 5 to 10 years per the manufacturer; this "
                    "node does not prescribe a number, the manufacturer's label governs). Any CO "
                    "alarm activation during HVAC service is a stop-work event."
                ),
                "alternatives": [],
            },
            {
                "name": "Fire extinguisher",
                "specification": (
                    "An A:B:C rated multipurpose extinguisher within reach of the mechanical "
                    "room is the conservative default. The household confirms the appropriate "
                    "rating for their actual mechanical space with a local fire-safety authority "
                    "(local fire marshal or equivalent); inspection tag is kept current. For any "
                    "future hot-work competency (brazing, soldering), an extinguisher rated for "
                    "the hot-work hazards is within arm's reach of the work per the operation; "
                    "hot work is not in this batch."
                ),
                "alternatives": [],
            },
            {
                "name": "Working flashlight or headlamp",
                "specification": (
                    "Mechanical rooms, attics, and crawl spaces are commonly dark; a working "
                    "flashlight or headlamp is on the person before entry. A headlamp leaves "
                    "both hands free; preferred for HVAC service work."
                ),
                "alternatives": [],
            },
            {
                "name": "Cell phone or way to call for help",
                "specification": (
                    "A way to reach emergency services or the gas utility's emergency line "
                    "quickly. The household's standing instructions cover when to call for: "
                    "smell of gas (gas utility emergency line per the utility's instructions, "
                    "not from inside the building); CO alarm activation (evacuate, call emergency "
                    "services from outside); severe electrical shock; serious refrigerant "
                    "exposure to skin or eyes; serious burn; fall from height."
                ),
                "alternatives": [],
            },
            {
                "name": "Tetanus immunization status (household-level)",
                "specification": (
                    "Every household member working on HVAC equipment has a tetanus immunization "
                    "status current per their healthcare provider's recommendation. The node does "
                    "not write a booster interval; the household's healthcare provider sets it "
                    "per current ACIP / CDC guidance. Sheet-metal cuts and contact with old "
                    "equipment are the primary in-trade tetanus exposures."
                ),
                "alternatives": [],
            },
            {
                "name": "Tool storage for sharp and heavy tools",
                "specification": (
                    "Sharp tools (tin snips, utility knives, refrigeration knives) and heavy "
                    "tools (manifold gauges, hammers, hand trucks, recovery machines) have a "
                    "designated home in the truck or the shop and are returned to it at end of "
                    "session. Sharp edges are sheathed or returned to their case; tools are not "
                    "left in walkways or on top of equipment."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": (
                "Real mechanical space (utility closet, basement mechanical room, attic equipment "
                "platform, garage furnace location, exterior condenser pad) where the actual "
                "household equipment lives; the walkthrough is in the actual environment, not on "
                "paper or in a classroom"
            ),
            "ventilation": (
                "Adequate ventilation to detect fuel-gas odorants and to avoid CO accumulation; "
                "windows or doors open as appropriate for the walkthrough"
            ),
            "lighting": (
                "Daylight or strong task lighting; portable flashlight or headlamp available for "
                "dark areas (most mechanical rooms have at least one inadequately lit corner)"
            ),
            "power": "Energy off at the unit disconnect during any walkthrough that opens an enclosure",
            "containment": "Clear floor space around equipment; no tripping hazards; pets and small children excluded from the work area",
        },
        "skill_description": (
            "The learner walks the mechanical space and the tool kit with an adult on premises "
            "and learns where every safety element is, what every hazard looks like, and how the "
            "safe habits work. They learn the PPE rules and when each item is required and "
            "permitted; the rule that the absence of voltage is verified before any contact with "
            "wiring per hc-021; the rule that capacitors are treated as charged until discharged "
            "per the manufacturer; the rule that refrigerant operations are EPA Section 608 work "
            "and not in scope at the helper or apprentice band without a 608-certified human "
            "present; the rule that any smell of gas is a stop-work event and the gas utility's "
            "emergency line is called from outside the building; the rule that CO alarm "
            "activation is a stop-work event and the area is evacuated; the rule that pre-1980 "
            "system components are treated as asbestos-suspect; the lifting rule (two-person or "
            "mechanical assist for anything heavy); the sheet-metal-edge habit (cut-resistant "
            "gloves on, no bare hands on cut sheet metal); the rule that hot work (brazing, "
            "soldering) is not in scope at this band; the rule that rooftop and confined-space "
            "work is not in scope at this band. They learn where the first aid kit, the fire "
            "extinguisher, the CO alarm, the flashlight, the phone for help, the gas utility "
            "emergency number, and the manufacturer's service literature for the household's "
            "equipment live. They learn that the manufacturer's service literature is the "
            "authority for the specific equipment, not the AI tutor and not a general reference."
        ),
        "demonstration_criteria": [
            "Names every PPE item on the list and explains when each is required and when each is permitted",
            (
                "Locates the first aid kit and confirms it meets a recognized standard (ANSI/ISEA "
                "Z308.1 or current American Red Cross guidance)"
            ),
            (
                "Locates the fire extinguisher within reach of the mechanical space, names its "
                "rating, and confirms the rating is appropriate for what is actually in the space "
                "per the household's confirmation with a local fire-safety authority"
            ),
            (
                "Locates the CO alarm(s) covering the household's combustion equipment and "
                "confirms each is listed (UL 2034 for residential or UL 2075 for commercial), "
                "within the manufacturer's service-life window, and placed per current NFPA 720 "
                "and the local AHJ"
            ),
            (
                "Names the household's tetanus immunization status arrangement and confirms with "
                "the mentor that every working household member is current per their healthcare "
                "provider's recommendation"
            ),
            (
                "Names the rule that the absence of voltage is verified by a meter before any "
                "contact with wiring (the live-dead-live or test-dead-test sequence) per NFPA 70E "
                "and OSHA 1910.147, and points to where hc-021 lives in the helper-to-apprentice "
                "path"
            ),
            (
                "Names the rule that capacitors are treated as charged until discharged per the "
                "manufacturer, and that capacitor discharge is not in scope at this band without "
                "a qualified human present"
            ),
            (
                "Names the rule that refrigerant operations are EPA Section 608 work, that hands-"
                "on refrigerant work requires a 608-certified person physically present, and that "
                "refrigerant operations are not in scope at this band"
            ),
            (
                "Names the smell-of-gas stop-work rule and demonstrates the sequence: leave the "
                "area without operating any switch, phone, or ignition source in the area; call "
                "the gas utility's emergency line from outside the building per the utility's "
                "posted instructions; do not re-enter until cleared"
            ),
            (
                "Names the CO alarm activation rule and demonstrates the sequence: evacuate "
                "everyone from the building; call emergency services from outside; do not re-"
                "enter until cleared by emergency services or the gas utility"
            ),
            (
                "Names the asbestos suspect rule for pre-1980 system components and the stop-and-"
                "ask rule when encountering suspect material; names that disturbing suspect "
                "material is not in scope without a qualified inspector"
            ),
            (
                "Demonstrates safe lifting form on a real component or piece of equipment within "
                "the learner's safe carry weight, OR refuses to lift a heavier component and "
                "names that a two-person lift or mechanical assist is required (both are correct "
                "answers)"
            ),
            (
                "Demonstrates the safe handling of a piece of cut sheet metal with cut-resistant "
                "gloves on, edges identified and controlled, and the panel set down with the cut "
                "edge facing safely (not into a walkway)"
            ),
            (
                "Names the rule that hot work (brazing, soldering) is not in scope at this band "
                "and requires its own safety competency, ventilation, fire watch, and "
                "extinguisher rated for the operation"
            ),
            (
                "Names the rule that rooftop work requires fall protection per OSHA 29 CFR 1926 "
                "Subpart M and is not in scope at this band; that confined-space entry requires "
                "the OSHA 1910.146 permit, written program, attendant, and rescue plan and is "
                "not in scope at this band"
            ),
            (
                "Locates the manufacturer's service literature for the household's actual "
                "equipment (the printed manual, the manufacturer's online service portal, or a "
                "saved PDF on the household's reference device) and demonstrates looking up one "
                "fact (the unit's voltage and MOP, for example) in it"
            ),
            "Names the trade rule that the manufacturer's service literature is the authority for the specific equipment, not a general reference",
            (
                "Demonstrates safe tool storage at the end of a session: sharp tools sheathed or "
                "returned to their case, heavy tools returned to the truck or shop, no tools "
                "left in walkways or on top of equipment"
            ),
        ],
        "common_errors": [
            {
                "error": "Assuming a circuit is dead because the switch was thrown",
                "cause": "The learner trusted the switch position without verifying with a meter",
                "remedy": (
                    "The absence of voltage is verified by a meter, never assumed. The "
                    "live-dead-live sequence is the rule: verify the meter on a known-live source "
                    "first, verify dead at the work point, then re-verify the meter on the "
                    "known-live source. This is what hc-021 teaches; the safety walkthrough "
                    "establishes the rule in advance."
                ),
            },
            {
                "error": "Touching a capacitor terminal on a de-energized condenser",
                "cause": "The learner believed the circuit was safe because the disconnect was open",
                "remedy": (
                    "Capacitors hold a charge for minutes to hours after the system is "
                    "de-energized. They are discharged by a resistor of the manufacturer-specified "
                    "value before any direct contact. Capacitor discharge is its own competency, "
                    "not at this band without a qualified human present."
                ),
            },
            {
                "error": "Operating a light switch or phone in a room that smells of gas",
                "cause": "The learner did not recognize the smell or did not know the no-ignition rule",
                "remedy": (
                    "Any smell of gas: leave the area without operating any switch, phone, or "
                    "ignition source. Call the gas utility's emergency line from outside the "
                    "building per the utility's instructions. Do not re-enter until cleared."
                ),
            },
            {
                "error": "Ignoring a CO alarm activation as a false alarm",
                "cause": "The alarm had falsed before, or the learner did not understand the stakes",
                "remedy": (
                    "CO is colorless and odorless; the alarm is the only warning the household "
                    "has. Any activation is a stop-work event: evacuate the building, call "
                    "emergency services from outside, do not re-enter until cleared. A repeat "
                    "false alarm needs the alarm replaced or the source identified by a "
                    "qualified person, not silenced."
                ),
            },
            {
                "error": "Cutting suspect tape mastic or insulation on an older system",
                "cause": "The learner did not recognize the pre-1980 suspect-material rule",
                "remedy": (
                    "Pre-1980 system components are treated as asbestos-suspect until tested by a "
                    "qualified inspector. Stop, do not cut or disturb, name the suspect material "
                    "to the mentor, defer the work."
                ),
            },
            {
                "error": "Lifting a condenser alone because it 'looks light'",
                "cause": "The learner underestimated the weight",
                "remedy": (
                    "Compressors, condensers, and air handlers are dense and heavier than they "
                    "look. The default is a two-person lift or mechanical assist. If the lift "
                    "does not feel light from the first inch off the floor, set it back down and "
                    "ask for help."
                ),
            },
            {
                "error": "Handling cut sheet metal bare-handed",
                "cause": "The learner removed gloves for a finer task and did not put them back on",
                "remedy": (
                    "Cut-resistant gloves on for any handling of sheet metal that has been cut or "
                    "broken. The edges that look smooth are not. Sheet-metal cuts are among the "
                    "most common HVAC injuries."
                ),
            },
            {
                "error": "Opening a refrigerant service port to 'see if there is pressure'",
                "cause": "The learner was curious and did not recognize the EPA 608 regulation",
                "remedy": (
                    "Opening a refrigerant service port is EPA Section 608 regulated work. It is "
                    "not done by a person without the appropriate certification, and not done at "
                    "this band without a 608-certified person physically present and performing "
                    "the operation. The refrigerant gauges stay in the bag at this band."
                ),
            },
            {
                "error": "Standing on a chair to reach an attic air handler",
                "cause": "The learner skipped getting a ladder for what felt like a quick reach",
                "remedy": (
                    "A real ladder rated for the duty and the height, set up per the "
                    "manufacturer's instructions and OSHA 1910.23, is the rule. No chairs, no "
                    "buckets, no stacked stools. Rooftop and elevated work is gated separately."
                ),
            },
        ],
        "artifact_expected": {
            "type": "video",
            "what_to_capture": (
                "A short walkthrough by the learner of their actual mechanical space and tool kit "
                "(under ten minutes for HVAC, longer than the woodworking walkthrough because "
                "more is named), pointing at and naming each item on the demonstration_criteria "
                "list, with the supervising adult offscreen or beside the learner. The AI tutor "
                "reviews the walkthrough video for completeness and correctness against the "
                "demonstration_criteria list."
            ),
            "what_the_evidence_shows": (
                "That the learner can identify, locate, and explain every safety element in the "
                "mechanical space they will be working in, can demonstrate the stop-work rules "
                "for gas smell and CO alarm activation, can locate and look up a fact in the "
                "manufacturer's service literature for the household's equipment, and can name "
                "the bands at which each hazard-class operation enters scope"
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The supervising adult walks the learner through the mechanical space and the "
                "tool kit, naming each hazard and each piece of safety equipment, demonstrating "
                "the safe-carry and safe-pass habits, the lifting form on a real (within-weight) "
                "piece of equipment, the location of the disconnect for each piece of equipment, "
                "the location of the gas shutoff (for combustion equipment), the location of the "
                "CO alarm and its listing/manufacturer date, the location of the manufacturer's "
                "service literature, and the household's posted gas-utility emergency number. The "
                "adult names what is forbidden as well as what is required, and explicitly names "
                "the bands at which each higher-hazard operation enters scope and the qualified-"
                "human-present rule for those bands. The AI tutor provides the walkthrough script "
                "and the demonstration_criteria list so the adult and the learner know what to "
                "cover."
            ),
            "we_do": (
                "Supervising adult and learner walk the mechanical space together. At each "
                "station the learner names the item and the adult confirms or corrects. The "
                "learner takes a turn carrying and passing a sharp tool (a pair of tin snips, "
                "for example) under the adult's watch; the learner demonstrates a safe lift on "
                "a real (within-weight) piece of equipment; the learner walks through the "
                "smell-of-gas response sequence and the CO-alarm-activation response sequence in "
                "narration. The learner locates and reads one fact from the manufacturer's "
                "service literature for the household's equipment."
            ),
            "you_do_supervised": (
                "The learner walks the supervising adult through the mechanical space and the "
                "tool kit, naming and locating each item without prompting. The adult asks at "
                "least one follow-up question per item, drawn from the AI tutor's suggested "
                "questions ('what is the rating on the fire extinguisher and why?', 'where is "
                "the gas shutoff?', 'what is the rule on capacitor contact?'). The video is "
                "recorded at this stage and uploaded for the AI tutor's review against the "
                "demonstration_criteria list."
            ),
            "you_do_unsupervised": (
                "Once signed off (by the supervising adult, with the AI tutor's confirmation "
                "that the walkthrough video covers every demonstration criterion), the learner "
                "does the same walkthrough at the start of any session in a new or modified "
                "mechanical space, after any change to the equipment or the household's plans, "
                "and at any change of seasons when the equipment use changes (heating-season "
                "startup, cooling-season startup). In any case the signoff is refreshed annually "
                "as the freshness check. There is no unsupervised work on hazardous subsystems "
                "without a current hs-001 signoff AND the qualified-human-present arrangement "
                "for the specific subsystem per the trade root's supervision policy."
            ),
        },
        "estimated_practice_sessions_to_signoff": 3,
        "session_length_minutes": 60,
        "signoff_validity_days": 365,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Foundational safety competency. Underpins every credential the trade builds "
                "toward; underpins every higher-band competency. Metadata only; safety_basis "
                "and supervision_basis are unchanged."
            ),
            "certifications_supported": [
                {
                    "id": "hcert-osha",
                    "domains": [
                        "introduction to OSHA",
                        "PPE recognition and use",
                        "electrical hazard recognition",
                        "fall hazard recognition",
                        "hazard communication",
                        "struck-by and caught-in/between hazards",
                    ],
                    "notes": "The walkthrough explicitly names what OSHA 10 / 30 covers as employer-required orientation.",
                },
                {
                    "id": "hcert-epa608",
                    "domains": [
                        "refrigerant safety practices (Core domain)",
                        "refrigerant identification and class awareness (A1 / A2L / A3)",
                        "venting prohibition under the Clean Air Act",
                    ],
                    "notes": (
                        "hs-001 names the refrigerant classes per ASHRAE 34 and names that "
                        "hands-on refrigerant work is EPA 608 regulated. The Core domain "
                        "knowledge introduced here is built up in the hcert-epa608 study."
                    ),
                },
                {
                    "id": "hcert-licensing",
                    "domains": [
                        "general HVAC safety practice",
                        "NFPA 70E familiarity (introductory)",
                        "OSHA 1910 / 1926 familiarity (introductory)",
                        "AHJ adopted code awareness",
                    ],
                    "notes": "Foundational safety practice underpinning every AHJ exam.",
                },
                {
                    "id": "hcert-nate",
                    "domains": [
                        "safety domain present in every NATE specialty's Knowledge Areas of Technician Expertise",
                    ],
                    "notes": "NATE expects baseline safety knowledge regardless of specialty.",
                },
            ],
        },
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                "ANSI/ISEA Z308.1 (Minimum Requirements for Workplace First Aid Kits and Supplies)",
                "American Red Cross home/shop first-aid kit guidance",
                "OSHA 29 CFR 1910.147 (The Control of Hazardous Energy / Lockout-Tagout)",
                "OSHA 29 CFR 1910.146 (Permit-Required Confined Spaces)",
                "OSHA 29 CFR 1910.137 and 1910.335 (Electrical PPE and Safe Practices)",
                "OSHA 29 CFR 1926 Subpart M (Fall Protection)",
                "OSHA 29 CFR 1910.23 (Walking-Working Surfaces, including ladders)",
                "NFPA 70E (Standard for Electrical Safety in the Workplace; current edition)",
                "NFPA 70 (National Electrical Code / NEC; current edition adopted by the local AHJ)",
                "NFPA 54 (National Fuel Gas Code; current edition adopted by the local AHJ)",
                "NFPA 720 (Standard for the Installation of Carbon Monoxide Detection and Warning Equipment)",
                "EPA Section 608 of the Clean Air Act (refrigerant handling certification)",
                "ASHRAE Standard 34 (Designation and Safety Classification of Refrigerants; current edition)",
                "ASHRAE Standard 62.1 and 62.2 (Ventilation for Acceptable Indoor Air Quality, commercial and residential)",
                "AHRI rating standards for HVAC equipment (current edition, including SEER2, HSPF2, EER2, AFUE)",
                "UL 2034 (residential CO alarms) and UL 2075 (commercial CO alarms)",
                "Current CDC carbon-monoxide guidance for action levels and recognition",
                "Current CDC / NIOSH outdoor-worker heat-illness prevention guidance",
                "Current EPA and state asbestos rules for pre-1980 system components",
                "Tetanus immunization status per each household member's healthcare provider per current ACIP / CDC guidance",
                "Manufacturer service literature for the specific equipment in the household or shop",
                "The local AHJ adopted codes (NEC, NFPA 54, IMC, UMC, local mechanical and energy codes); these vary by jurisdiction and the household identifies their AHJ's current adopted editions",
                "The household's employer's written lockout-tagout program (for a learner working under a contractor or vocational program)",
            ],
        },
    },
    "hc-001": {
        "node_type": "technique",
        "trade": "hvac",
        "competency_name": (
            "Read an HVAC equipment nameplate to extract voltage, phase, MCA, MOP, refrigerant "
            "type and charge, capacity, efficiency rating, model and serial, and manufacture date"
        ),
        "progression_band": "helper",
        "prerequisites": ["hs-001"],
        "safety_basis": {
            "hazards": [
                (
                    "Misreading the nameplate voltage and trying to apply the wrong meter range "
                    "or the wrong PPE; not a direct hazard at this band because the work is "
                    "purely reading the printed plate, but a real downstream error if the wrong "
                    "number propagates to hc-021 or to any later electrical work"
                ),
                (
                    "Misreading the refrigerant type and missing the safety class difference "
                    "(A1 vs A2L vs A3); not a direct hazard at this band because no refrigerant "
                    "is opened, but a real downstream error if the wrong class propagates to a "
                    "later refrigerant operation (which is its own gate)"
                ),
                (
                    "Misreading the MCA (minimum circuit ampacity) or MOP (maximum overcurrent "
                    "protection) and concluding the wrong wire size or breaker size; not a "
                    "direct hazard at this band because the wiring is not changed, but the "
                    "wrong number compounds in any later electrical install (NEC-regulated, not "
                    "in this batch)"
                ),
                (
                    "Reaching into a panel or enclosure to find a hidden nameplate; the rule is "
                    "the cover stays on at this band, and any nameplate not visible from outside "
                    "the enclosure is photographed by a qualified human with the disconnect open "
                    "and verified dead per hc-021"
                ),
            ],
            "ppe_required": [
                (
                    "Trade PPE per hs-001 (closed-toe shoes, the trade's general defaults); no "
                    "additional PPE required for reading a nameplate visible from outside the "
                    "enclosure. Eye protection optional but recommended if working in a dusty "
                    "mechanical space."
                ),
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Reading a nameplate visible from outside the enclosure involves no tool use, no "
                "opened enclosure, no live circuit contact, no moving parts, and no chemical or "
                "refrigerant exposure. The AI tutor mentors this competency end-to-end: the "
                "learner photographs the nameplate, the AI confirms each extracted field, the "
                "learner builds a nameplate card. Trade-level supervision from hvac-root still "
                "applies through the helper band in the sense that no enclosure is opened and no "
                "energized work is performed; the reading itself is low-hazard and AI-mentorable."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "A real HVAC equipment nameplate visible from outside the enclosure",
                "specification": (
                    "The household's actual equipment (outdoor condenser unit, indoor air "
                    "handler, furnace cabinet, heat pump, mini-split outdoor unit, water heater, "
                    "boiler). The nameplate is typically on the side panel of the outdoor unit "
                    "or on the access door of indoor equipment, visible without opening any "
                    "enclosure. If the household's equipment has its nameplate inside the "
                    "enclosure only, this competency is deferred to a session with a qualified "
                    "human present per the trade root's supervision policy."
                ),
                "alternatives": [
                    "A clear photograph of the nameplate from a manufacturer's online service "
                    "literature, used as a learning aid until the real equipment is visited"
                ],
            },
            {
                "name": "A nameplate card or notebook page",
                "specification": (
                    "A sheet of paper or a notebook page where the learner writes down each "
                    "operative field from the nameplate. The card is the working reference for "
                    "every later step on that piece of equipment (parallel to the planting card "
                    "in gc-001 of the gardening trade)."
                ),
                "alternatives": [
                    "A structured digital form per the household's record-keeping practice; the "
                    "AI tutor can render the form"
                ],
            },
            {
                "name": "Camera (cell phone is sufficient) for the nameplate photograph",
                "specification": (
                    "A camera that produces an image clear enough to read every printed field. "
                    "The photo is uploaded to the AI tutor for confirmation of each extracted "
                    "field."
                ),
                "alternatives": [],
            },
            {
                "name": "Flashlight or headlamp",
                "specification": (
                    "Mechanical-space lighting is commonly poor; the nameplate often sits in "
                    "shadow. A flashlight is on the person for the visit."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Wherever the equipment is installed; the work is the visit itself",
            "ventilation": "Adequate per hs-001 for the space",
            "lighting": "Daylight, room lighting, or flashlight as needed for the nameplate location",
            "power": "Energy state immaterial for reading a nameplate visible from outside; no enclosure opened",
            "containment": "None required",
        },
        "skill_description": (
            "The learner visits a piece of HVAC equipment in the household and locates the "
            "nameplate without opening any enclosure. The nameplate is typically on the side or "
            "back panel of the outdoor unit and on the access panel or door of the indoor "
            "equipment. The learner photographs the nameplate clearly and reads each operative "
            "field onto a nameplate card. The fields read in order: manufacturer; model number; "
            "serial number; manufacture date (often encoded in the serial number per the "
            "manufacturer's scheme); equipment type (condensing unit, air handler, furnace, "
            "heat pump, etc.); voltage (typically printed as '208/230V' or '240V' for residential "
            "single-phase, '208V/3PH' or '460V/3PH' for commercial); frequency (60 Hz in the US); "
            "phase (1 or 3); MCA (minimum circuit ampacity, the smallest wire and conductor "
            "rating the equipment will accept per NEC); MOP (maximum overcurrent protection, "
            "the largest breaker or fuse the equipment will accept per NEC); refrigerant type "
            "(R-410A, R-454B, R-32, R-22 on older equipment, etc.) and factory charge (in "
            "ounces or pounds); rated capacity (in BTU/hr or tons for cooling equipment, in "
            "BTU/hr input and output for furnaces and boilers); efficiency rating (SEER2 or "
            "SEER for AC and heat pump cooling; HSPF2 or HSPF for heat pump heating; EER2 or "
            "EER for AC at a specific condition; AFUE for furnaces; thermal efficiency for "
            "commercial boilers); any listing or certification marks (UL, ETL, AHRI). The "
            "learner then submits the nameplate card and the photograph to the AI tutor for "
            "field-by-field confirmation. If any field is missing, illegible, or unfamiliar, "
            "the learner names it on the card and the AI tutor explains what the field "
            "typically represents and where the manufacturer's service literature defines it. "
            "The card is filed with the household's equipment records and travels with the "
            "learner for every later session on that equipment."
        ),
        "demonstration_criteria": [
            ("Locates the nameplate on a piece of household HVAC equipment without opening any enclosure"),
            ("Photographs the nameplate clearly enough that every printed field is legible in the image"),
            (
                "Extracts every operative field onto a nameplate card: manufacturer; model; "
                "serial; manufacture date (decoded if encoded in serial); equipment type; "
                "voltage; frequency; phase; MCA; MOP; refrigerant type and factory charge "
                "(if applicable); rated capacity; efficiency rating; listing marks"
            ),
            (
                "Submits the nameplate card and photograph to the AI tutor; the AI tutor "
                "confirms each field or names a discrepancy; the learner reconciles and "
                "resubmits"
            ),
            (
                "Names which fields the nameplate did not supply (some fields are not on every "
                "nameplate; the AI tutor confirms which are normal omissions and which would "
                "warrant looking up the manufacturer's service literature)"
            ),
            (
                "Names what the MCA and MOP fields mean in plain language: MCA is the smallest "
                "circuit the equipment will accept; MOP is the largest breaker the equipment "
                "will accept; both are required for sizing the dedicated branch circuit per NEC. "
                "The wiring itself is NEC-regulated work, not in this batch."
            ),
            (
                "Names the ASHRAE 34 safety class of the refrigerant on the nameplate (A1, A2L, "
                "A3, or other) using the AI tutor's lookup; names that the safety class affects "
                "later refrigerant operations (not in this batch) but does not affect the reading "
                "of the nameplate"
            ),
            (
                "Reads three different nameplates on three different pieces of equipment (or "
                "three different photographs if the household has only one piece of equipment) "
                "and submits a complete card for each"
            ),
        ],
        "common_errors": [
            {
                "error": "Reading the voltage as a single number when the plate shows a range",
                "cause": "Residential plates often print '208/230V' meaning the unit will operate on either; the learner picked one number",
                "remedy": (
                    "Record the plate as printed ('208/230V' or '230V', as the plate reads). The "
                    "unit's actual supply voltage is measured later; the plate range tells what "
                    "the unit will accept."
                ),
            },
            {
                "error": "Confusing MCA with MOP",
                "cause": "Both are amp ratings on the plate, often near each other",
                "remedy": (
                    "MCA (minimum circuit ampacity) is the smallest the circuit can be; MOP "
                    "(maximum overcurrent protection) is the largest the breaker can be. They "
                    "are named differently on the plate (sometimes 'Min. Circuit Ampacity' and "
                    "'Max. Fuse / HACR' or similar). The AI tutor confirms the labeling per the "
                    "specific manufacturer."
                ),
            },
            {
                "error": "Recording R-22 on an old plate without flagging it",
                "cause": "The learner read the printed type without recognizing the phase-out status",
                "remedy": (
                    "R-22 has been phased out for new equipment production in the US since 2010 "
                    "and for import / new manufacture per EPA. R-22 systems still exist and are "
                    "serviced under EPA Section 608 with recovered R-22 or approved drop-in "
                    "replacements. The nameplate field is recorded as printed; the AI tutor "
                    "confirms the phase-out status for the household's reference. Service on R-22 "
                    "is regulated work not in this batch."
                ),
            },
            {
                "error": "Opening an enclosure to find the nameplate",
                "cause": "The visible plate was missing or illegible and the learner reached inside",
                "remedy": (
                    "The cover stays on at this band. If the visible nameplate is missing or "
                    "illegible, the work is deferred to a session with a qualified human present "
                    "who opens the enclosure under lockout-tagout per hc-021 and photographs the "
                    "internal plate."
                ),
            },
            {
                "error": "Confusing tons with BTU/hr for cooling capacity",
                "cause": "Some plates state cooling capacity in tons and some in BTU/hr",
                "remedy": (
                    "1 ton of cooling = 12,000 BTU/hr. Residential equipment is commonly 1.5 to "
                    "5 tons (18,000 to 60,000 BTU/hr). Both are valid; record as the plate "
                    "reads and the AI tutor can convert if needed."
                ),
            },
            {
                "error": "Reading SEER instead of SEER2 (or vice versa)",
                "cause": "The rating standard shifted in 2023 and both ratings exist on equipment of different vintages",
                "remedy": (
                    "Read what the plate prints. SEER, SEER2, EER, EER2, HSPF, HSPF2, AFUE are "
                    "distinct ratings with distinct test conditions; the AI tutor explains the "
                    "shift and confirms which the plate is using by the printed label."
                ),
            },
            {
                "error": "Skipping the manufacture date because it is encoded in the serial number",
                "cause": "Many manufacturers encode the manufacture date in the first characters of the serial; the learner read the serial as opaque",
                "remedy": (
                    "Photograph the serial number clearly and submit to the AI tutor; the AI "
                    "tutor decodes the date per the manufacturer's published serial scheme, or "
                    "names that the scheme is not publicly documented and the household's "
                    "service literature or the manufacturer's customer service supplies the date."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "Three nameplate cards (one per piece of equipment), each accompanied by the "
                "clear photograph of the corresponding nameplate, with every operative field "
                "filled in on the card in the learner's handwriting (or typed in the household's "
                "record system)"
            ),
            "what_the_evidence_shows": (
                "That the learner extracted every operative field from each nameplate, that the "
                "AI tutor confirmed each field, and that any unfamiliar field was named on the "
                "card and resolved with the AI tutor's lookup against the manufacturer's "
                "service literature"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a sample nameplate photograph (provided "
                "by the AI), naming each field aloud (in chat or in voice), pointing out the "
                "typical layout (manufacturer top, model and serial mid-plate, electrical specs "
                "and refrigerant info usually grouped), and explaining what each field is for "
                "and where it will be used in later competencies. The AI explicitly names the "
                "ASHRAE 34 safety class of the sample refrigerant and the SEER / HSPF / AFUE "
                "rating context."
            ),
            "we_do": (
                "The AI tutor and the learner work through a second sample nameplate together. "
                "The learner names a field; the AI confirms or corrects; the next field is the "
                "AI's, then back to the learner. At the end the learner reads the whole "
                "nameplate card back."
            ),
            "you_do_supervised": (
                "The learner visits the household's actual equipment, photographs the nameplate, "
                "and reads it onto a card. The card and photograph are submitted to the AI tutor "
                "for field-by-field confirmation. The AI tutor names any discrepancy and the "
                "learner reconciles. The supervising adult is on premises only for the visit "
                "itself (because the learner is in the mechanical space); the AI mentors the "
                "actual reading."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce three accurate nameplate cards across at least "
                "two sessions, they may read nameplates unsupervised. The AI tutor remains "
                "available for field confirmation; this is not a supervision rule, it is a "
                "double-check rule that stays in place across bands."
            ),
        },
        "estimated_practice_sessions_to_signoff": 3,
        "session_length_minutes": 30,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency the AI tutor mentors end-to-end. Foundational across "
                "every credential the trade builds toward; the nameplate is the first thing "
                "looked at on every service call. Metadata only; safety_basis and "
                "supervision_basis are unchanged."
            ),
            "certifications_supported": [
                {
                    "id": "hcert-epa608",
                    "domains": [
                        "refrigerant identification (Core)",
                        "refrigerant type and factory charge",
                        "equipment type and capacity for sizing recovery / recycling",
                    ],
                    "notes": (
                        "Reading the nameplate's refrigerant type is foundational to all four "
                        "EPA 608 types (Core, I, II, III, Universal)."
                    ),
                },
                {
                    "id": "hcert-licensing",
                    "domains": [
                        "MCA and MOP for branch-circuit sizing per NEC",
                        "voltage and phase for service-disconnect sizing per NEC",
                        "tonnage and capacity for load matching per ACCA Manual S",
                        "AFUE / SEER2 / HSPF2 / EER2 for energy-code compliance",
                    ],
                    "notes": (
                        "Journeyman exam tests circuit-sizing math from nameplate values; "
                        "this competency builds the literacy."
                    ),
                },
                {
                    "id": "hcert-nate",
                    "domains": [
                        "equipment identification across the chosen specialty's KATE",
                        "rated-condition vs operating-condition distinction",
                    ],
                    "notes": "Every NATE specialty assumes nameplate fluency.",
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
    "hc-002": {
        "node_type": "technique",
        "trade": "hvac",
        "competency_name": (
            "Identify the major components of a residential split-system air conditioner or "
            "heat pump by sight, without opening any enclosure"
        ),
        "progression_band": "helper",
        "prerequisites": ["hs-001"],
        "safety_basis": {
            "hazards": [
                (
                    "Reaching toward a spinning condenser fan or blower in operation; the rule "
                    "is no body part enters the airflow path of a running fan; for visual ID the "
                    "learner stays clear of any operating equipment and works on de-energized "
                    "equipment when up close"
                ),
                (
                    "Touching a hot suction or liquid line during operation; the liquid line on "
                    "a running AC is typically warm to hot to the touch (over 100 F is common), "
                    "and the suction line can be cold enough to cause frostbite if a refrigerant "
                    "leak is escaping; the rule is no touching of line set during operation, only "
                    "visual identification at this band"
                ),
                (
                    "Touching the compressor or other hot components during or shortly after "
                    "operation; the compressor and head can run hot enough to burn skin"
                ),
                (
                    "Opening the electrical disconnect or any enclosure to find a component; the "
                    "rule is the cover stays on at this band; visual ID is performed with the "
                    "cover closed for energized equipment and with the cover closed (or open "
                    "under a qualified human's supervision per hc-021) for de-energized "
                    "equipment"
                ),
                (
                    "Sharp sheet-metal edges on the outdoor unit cabinet; cut-resistant gloves "
                    "on if any handling of the cabinet (touching, leaning against) is anticipated"
                ),
                (
                    "Slip hazard from condensate or seasonal water around the outdoor unit; the "
                    "learner observes the standing water and condensate path as part of the ID, "
                    "not as a hazard to step into"
                ),
            ],
            "ppe_required": [
                "Trade PPE per hs-001 (closed-toe shoes, the trade's general defaults)",
                "Safety glasses for any work close to the outdoor unit (insects, debris, weather)",
                (
                    "Cut-resistant gloves if any handling of the cabinet panels is anticipated; "
                    "bare hands acceptable for pure visual ID at arm's length"
                ),
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Visual identification with the cover closed and no enclosure opening involves no "
                "tool use, no live circuit contact, no refrigerant contact, no opened combustion "
                "system, and no rotating equipment contact. The AI tutor mentors this competency "
                "end-to-end: the learner photographs each component (with the unit cover closed "
                "for any energized equipment; the cover is opened only under hc-021 with a "
                "qualified human present, which is a different competency), and the AI confirms "
                "each identification. Trade-level supervision from hvac-root still applies in "
                "the sense that no enclosure is opened and no energized work is performed; the "
                "identification itself is low-hazard and AI-mentorable."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "A residential split-system air conditioner or heat pump",
                "specification": (
                    "The household's actual equipment, OR clear photographs of an outdoor "
                    "condenser unit and indoor air handler from manufacturer's service "
                    "literature. Visual ID is performed with the cover closed on energized "
                    "equipment; any cover-removed views are from manufacturer's documentation "
                    "or from a session with a qualified human present per hc-021. Mini-split "
                    "and packaged-unit photographs are acceptable substitutes if the household "
                    "does not have a split system."
                ),
                "alternatives": [],
            },
            {
                "name": "Camera (cell phone is sufficient)",
                "specification": (
                    "A camera that produces images clear enough to identify components in the "
                    "AI tutor's review. The learner photographs the unit and each external "
                    "component from a few angles."
                ),
                "alternatives": [],
            },
            {
                "name": "Component identification card or notebook",
                "specification": (
                    "A sheet or notebook page listing each named component with its function in "
                    "one sentence as the learner identifies it. The card travels with the "
                    "learner across later sessions on that equipment."
                ),
                "alternatives": [],
            },
            {
                "name": "Flashlight or headlamp",
                "specification": (
                    "Mechanical-space lighting is commonly poor; a flashlight is on the person for the visit"
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Wherever the equipment is installed (outdoor pad, basement, attic, utility closet, garage)",
            "ventilation": "Per hs-001 for the space",
            "lighting": "Daylight, room lighting, or flashlight as needed",
            "power": (
                "Energy state immaterial for cover-closed visual ID; for any cover-removed view, "
                "the disconnect is verified open under hc-021 by a qualified human (which is a "
                "different competency, not in scope for this node's unsupervised practice)"
            ),
            "containment": "None required",
        },
        "skill_description": (
            "The learner visits the household's outdoor condenser unit and indoor air handler "
            "(or furnace with cooling coil) and identifies each major component by sight with "
            "the unit covers closed. The learner photographs each component or component area "
            "and submits to the AI tutor with the component's name and function written on a "
            "card. The components, in order from outside in: outdoor condenser unit cabinet "
            "(the metal box on the pad); the condenser coil (the metal fins wrapped around the "
            "outside of the cabinet, visible through the cabinet grille); the condenser fan "
            "(the fan visible at the top or side of the cabinet, exhausting heated air); the "
            "line set entering the cabinet (two copper lines, the larger insulated suction line "
            "and the smaller bare liquid line; on a heat pump in heating mode the temperatures "
            "swap, but the size and insulation tell which line is which); the service ports "
            "(two small valves on the line set near the cabinet, with caps in place when not in "
            "use; refrigerant work happens here under EPA 608, not in this batch); the outdoor "
            "disconnect (a small electrical box mounted on the wall near the outdoor unit, "
            "between the building's electrical panel and the outdoor unit, containing the "
            "service-disconnect switch and overcurrent protection); the electrical whip (the "
            "flexible conduit from the disconnect to the cabinet, carrying the supply wiring); "
            "the cabinet access panels (the side or top panel the technician removes to access "
            "the contactor, capacitor, control board, and compressor, which are inside and not "
            "visible at this band). Indoor side: the air handler or furnace cabinet (the indoor "
            "metal box that contains the blower and the evaporator coil or burner); the supply "
            "and return duct connections (the rectangular sheet-metal openings on the cabinet); "
            "the evaporator coil access (a panel on the cabinet, behind which the coil sits; "
            "not opened at this band); the blower compartment (a panel on the cabinet, behind "
            "which the blower sits; not opened at this band); the condensate drain pan and "
            "primary condensate line (visible at the bottom of the cabinet or as a PVC pipe "
            "exiting the cabinet, usually with a P-trap and a termination at a floor drain or "
            "outside); the secondary or emergency drain pan and the float switch (on systems "
            "installed above living space; required by IMC in most jurisdictions); the indoor "
            "filter slot (often at the return-air side of the cabinet or in a separate filter "
            "grille in the return duct); the thermostat (on the wall in the living space, "
            "connected by low-voltage wiring back to the air handler or furnace control); the "
            "control board (inside the cabinet, not visible at this band). Each component is "
            "named with its function in one sentence on the card."
        ),
        "demonstration_criteria": [
            (
                "Names every visible component of the outdoor unit from outside the cabinet: "
                "cabinet, condenser coil (visible through the grille), condenser fan (visible at "
                "top or side), line set (insulated suction line and bare liquid line), service "
                "ports with caps in place, outdoor disconnect, electrical whip, access panels "
                "(named but not opened)"
            ),
            (
                "Names every visible component of the indoor unit from outside the cabinet: "
                "cabinet, supply and return duct connections, access panels for evaporator coil "
                "and blower (named but not opened), condensate drain pan and primary line, "
                "secondary or emergency drain pan and float switch (if present per the "
                "installation), filter slot or return-air filter grille, thermostat on the wall"
            ),
            (
                "Names the function of each component in one sentence: the condenser fan "
                "exhausts heated refrigerant gas to the outdoor air; the evaporator coil absorbs "
                "heat from the indoor air; the compressor (inside the outdoor unit, not visible "
                "at this band) pumps the refrigerant around the loop; etc."
            ),
            (
                "Distinguishes the suction line from the liquid line by inspection (the suction "
                "line is the larger of the two and is insulated; the liquid line is smaller and "
                "bare copper)"
            ),
            (
                "Locates the outdoor disconnect and names that it is the device used in hc-021 "
                "to de-energize the outdoor unit before any service; demonstrates pointing to "
                "the disconnect without operating it (operating the disconnect is part of "
                "hc-021, not this competency)"
            ),
            (
                "Names that the access panels (cabinet covers, blower compartment, evaporator "
                "coil access) are NOT opened at this band; opening them is part of a different "
                "competency that requires lockout-tagout per hc-021 and a qualified human "
                "present per the trade root's supervision policy"
            ),
            (
                "Names that the service ports on the line set are NOT touched at this band; "
                "any work at the service ports is EPA Section 608 refrigerant work and requires "
                "a 608-certified person physically present"
            ),
            (
                "Photographs each component or component area and submits to the AI tutor with "
                "the component name and function written on the card; the AI tutor confirms "
                "each identification or names a discrepancy; the learner reconciles"
            ),
            (
                "Names the difference between a split-system AC and a split-system heat pump in "
                "one sentence (a heat pump can run the refrigerant cycle in both directions, "
                "providing heating in winter and cooling in summer; an AC runs only in cooling "
                "mode)"
            ),
            (
                "Names what is and is not in this band: visible-from-outside identification is "
                "in band; opened-enclosure inspection, refrigerant work, electrical service work, "
                "and combustion-system work are each gated separately"
            ),
        ],
        "common_errors": [
            {
                "error": "Confusing the suction line and the liquid line",
                "cause": "The learner did not notice the insulation difference or the diameter difference",
                "remedy": (
                    "Suction line: larger diameter, insulated. Liquid line: smaller diameter, "
                    "bare copper. On a heat pump in heating mode the temperatures swap (the "
                    "suction line is now hot, the liquid line cool), but the size and insulation "
                    "of the lines themselves do not change. The AI tutor confirms in the photo."
                ),
            },
            {
                "error": "Trying to identify the compressor or contactor from the outside",
                "cause": "The learner expected the components named in the description to be visible",
                "remedy": (
                    "The compressor, contactor, capacitor, and control board sit inside the "
                    "outdoor cabinet, behind the access panels. They are not visible at this "
                    "band. The cover stays on; the AI tutor confirms which components are "
                    "external and which are internal."
                ),
            },
            {
                "error": "Opening the disconnect to look at the internals",
                "cause": "The learner reached to flip the disconnect or pull the pull-out",
                "remedy": (
                    "The disconnect is identified and pointed to, NOT operated. Operating the "
                    "disconnect (opening it, verifying the absence of voltage) is hc-021, which "
                    "requires a qualified human present at the live-dead-live verification. The "
                    "disconnect stays as found at this band."
                ),
            },
            {
                "error": "Touching a service port cap to see how it unscrews",
                "cause": "The learner was curious about the refrigerant service port",
                "remedy": (
                    "Service ports are NOT touched at this band. Removing a cap can release "
                    "refrigerant; opening the port is EPA Section 608 work and requires a 608-"
                    "certified person physically present. The cap stays on as found; the cap is "
                    "pointed to and named."
                ),
            },
            {
                "error": "Missing the secondary drain pan or float switch on an above-living-space air handler",
                "cause": "The pan and switch are visible but often not obvious if not looking for them",
                "remedy": (
                    "On any installation above living space (attic air handler, second-floor "
                    "closet), the IMC and most local codes require a secondary drain pan and a "
                    "float switch that interrupts the system on condensate overflow. The AI "
                    "tutor confirms in the photo and explains the function of the float switch."
                ),
            },
            {
                "error": "Reaching toward a running condenser fan",
                "cause": "The learner wanted to feel the airflow or see the fan blades better",
                "remedy": (
                    "No body part enters the airflow path of a running fan. The fan is observed "
                    "from outside the airflow; if a closer look is needed, the unit is "
                    "de-energized under hc-021 first by a qualified human."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "A series of photographs of the household's outdoor unit and indoor air handler "
                "(or furnace), with each named component visible and labeled in an accompanying "
                "card (handwritten or typed) that names the component and its function in one "
                "sentence. The cards and photographs are submitted to the AI tutor for "
                "field-by-field confirmation."
            ),
            "what_the_evidence_shows": (
                "That the learner identified each visible component correctly, distinguished "
                "the suction and liquid lines, located the disconnect without operating it, "
                "located the service ports without touching them, and named which components "
                "and operations are in band and which are gated for later"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The AI tutor walks the learner through a sample split-system photograph (the "
                "AI provides the image), naming each visible component aloud (in chat or in "
                "voice), pointing out the distinguishing features (insulated suction line, "
                "bare liquid line, capped service ports, etc.), and naming which components are "
                "internal and not visible at this band."
            ),
            "we_do": (
                "The AI tutor and the learner work through a second sample photograph together. "
                "The learner names a component; the AI confirms or corrects; the next component "
                "is the AI's, then back to the learner. At the end the learner reads the whole "
                "ID card back."
            ),
            "you_do_supervised": (
                "The learner visits the household's actual equipment, photographs each "
                "component, and writes the name and function of each on the card. The cards and "
                "photographs are submitted to the AI tutor for confirmation. The supervising "
                "adult is on premises only for the visit itself (because the learner is in the "
                "mechanical space or yard); the AI mentors the actual identification."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce accurate ID cards for the outdoor unit and the "
                "indoor unit (or furnace with cooling) across at least two sessions, they may "
                "identify components on new equipment unsupervised. The AI tutor remains "
                "available for component confirmation; this is not a supervision rule, it is a "
                "double-check rule that stays in place across bands."
            ),
        },
        "estimated_practice_sessions_to_signoff": 3,
        "session_length_minutes": 30,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "helper",
            "notes": (
                "Knowledge competency the AI tutor mentors end-to-end. Visual literacy of the "
                "split system is foundational across every credential. Metadata only; "
                "safety_basis and supervision_basis are unchanged."
            ),
            "certifications_supported": [
                {
                    "id": "hcert-epa608",
                    "domains": [
                        "service-port identification and the rule against opening them without 608 (Core)",
                        "high-pressure system component recognition (Type II)",
                        "low-pressure system component recognition (Type III, by contrast)",
                    ],
                    "notes": (
                        "Knowing which valves are service ports and which lines they sit on "
                        "is a Core EPA 608 domain. hc-002 enforces no-touch at this band."
                    ),
                },
                {
                    "id": "hcert-licensing",
                    "domains": [
                        "split-system architecture for service and install scope",
                        "disconnect location and identification per NEC",
                        "secondary drain pan and float switch per IMC for above-living-space installations",
                    ],
                    "notes": "Journeyman exam tests both code and system architecture knowledge.",
                },
                {
                    "id": "hcert-nate",
                    "domains": [
                        "system architecture per the AC, Heat Pump, and Air Distribution KATEs",
                    ],
                    "notes": "Foundational across multiple NATE specialties.",
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
    "hc-021": {
        "node_type": "technique",
        "trade": "hvac",
        "competency_name": (
            "Use a digital multimeter with formal lockout-tagout to verify the absence of voltage "
            "at a residential AC condenser disconnect before service (live-dead-live verification)"
        ),
        "progression_band": "apprentice",
        "prerequisites": ["hs-001", "hc-001", "hc-002"],
        "safety_basis": {
            "hazards": [
                (
                    "ELECTROCUTION RISK. Residential outdoor AC and heat pump units are typically "
                    "supplied at 240V/60Hz/1-phase in the US. At residential available fault "
                    "current, contact across the heart can stop it. The entire purpose of this "
                    "competency is to verify, with a meter, that the conductors at the work "
                    "point are dead before any further work. A learner who skips or mis-performs "
                    "this competency and then contacts a live conductor in a downstream task can "
                    "be killed."
                ),
                (
                    "ARC FLASH. A short between conductors during energized work releases an arc "
                    "that can cause severe burns and concussive injury. Arc-flash hazard on a "
                    "residential 240V disconnect is smaller than commercial but real. NFPA 70E "
                    "governs arc-flash boundaries and PPE selection; the default in this trade is "
                    "to de-energize and verify dead before opening any enclosure, which removes "
                    "the arc-flash hazard at the work point."
                ),
                (
                    "WRONG-DISCONNECT FAILURE. A mis-identified or mis-operated disconnect leaves "
                    "the wrong circuit dead and the intended one live. The unit cabinet may have "
                    "TWO sources of power (line-voltage supply AND low-voltage control from the "
                    "air handler); the line-voltage disconnect at the outdoor unit handles only "
                    "the line side. The control side is verified dead separately, typically by "
                    "switching the system off at the thermostat and verifying low voltage at the "
                    "contactor."
                ),
                (
                    "METER FAILURE. A digital multimeter with a depleted battery, a blown fuse, "
                    "a broken probe lead, or a wrong category rating can read zero on a live "
                    "conductor and mislead the user into thinking the circuit is dead. The "
                    "live-dead-live (or test-dead-test) sequence per NFPA 70E exists precisely "
                    "to catch this: verify the meter on a known live source FIRST, verify dead "
                    "at the work point, then re-verify the meter on the known live source. All "
                    "three readings must agree with the expected state. If the third reading "
                    "fails, the second reading is invalid."
                ),
                (
                    "STORED ENERGY IN CAPACITORS. The dual-run capacitor inside the outdoor unit "
                    "stores a charge that persists after the disconnect is opened. This "
                    "competency does NOT include opening the cabinet and contacting the "
                    "capacitor; the live-dead-live verification is performed at the disconnect "
                    "(line side), not at the capacitor (inside the cabinet). Capacitor discharge "
                    "is its own competency, gated separately, not in this batch."
                ),
                (
                    "BACKFEED FROM CONTROL CIRCUIT OR SHARED NEUTRAL. In some misinstalled or "
                    "older systems, opening the line disconnect does not fully de-energize the "
                    "cabinet because of a backfed control circuit, a shared neutral with another "
                    "circuit, or a generator transfer arrangement. The verification at the work "
                    "point is the safeguard; never assume the disconnect did its job."
                ),
                (
                    "WET CONDITIONS. Performing this verification in rain, standing water, or on "
                    "a wet outdoor pad significantly increases shock risk. The verification is "
                    "deferred to dry conditions; if the situation is urgent (storm-related "
                    "service), the qualified human present decides whether to proceed with "
                    "additional PPE per NFPA 70E or to defer."
                ),
                (
                    "SHARP SHEET-METAL EDGES on the disconnect cover and the unit cabinet if "
                    "the cover is removed; cut-resistant gloves on for any handling of the "
                    "cover."
                ),
            ],
            "ppe_required": [
                "Trade PPE per hs-001 (closed-toe shoes, the trade's general defaults)",
                "Safety glasses (ANSI Z87.1) required throughout the procedure",
                (
                    "Insulating gloves rated for the voltage actually being verified (residential "
                    "240V verification: class 00 or higher per NFPA 70E and the glove "
                    "manufacturer); inspected per the manufacturer and OSHA before use. The "
                    "qualified human present confirms the glove rating and the inspection."
                ),
                (
                    "Long sleeves and clothing rated appropriately per NFPA 70E for the "
                    "arc-flash incident energy at the disconnect (residential AC disconnect "
                    "incident energy is typically low but the calculation is per the system; "
                    "the qualified human present confirms PPE selection)"
                ),
                "No metal jewelry on hands, wrists, or neck during the procedure",
                (
                    "Multimeter (DMM) with CAT III at minimum rated for 600V or higher for the "
                    "240V residential measurement, with intact test leads, current battery, and "
                    "current calibration where the household or employer's program requires "
                    "calibration tracking. CAT IV is acceptable. CAT II or unrated meters are "
                    "NOT acceptable for this measurement per NFPA 70E."
                ),
                (
                    "Lockout-tagout hardware appropriate to the disconnect type: a padlock that "
                    "fits the disconnect's lockout provision, a danger tag legible per OSHA "
                    "1910.145, and the key kept exclusively by the person performing the work "
                    "for the duration of the lockout"
                ),
            ],
            "supervision_required": True,
            "supervision_basis": (
                "ELECTRICAL HAZARD. A qualified human is PHYSICALLY PRESENT at the live-dead-"
                "live verification, where qualified means a licensed HVAC technician OR a "
                "licensed electrician with current experience in residential electrical work. "
                "The qualified human watches the meter reading, watches the probe placement, "
                "watches the lockout-tagout sequence, and is in position to intervene physically "
                "if the learner makes a mistake. The AI tutor mentors the procedure walkthrough "
                "on paper and reviews the artifact evidence (photos of the LOTO setup, written "
                "procedure read-back) but does NOT stand in for the qualified human at the "
                "live moment. A learner working alone with only AI mentoring at the live moment "
                "is in mortal danger of electrocution if the procedure fails, the meter fails, "
                "or the wrong disconnect is operated. This is the one hard line in the trade's "
                "supervision policy. Households without a resident qualified person arrange a "
                "paid professional supervision session, a vocational-school program day, an "
                "apprentice arrangement with a working contractor, or defer the competency until "
                "the qualified human is arranged. The AI tutor and the supervising adult on "
                "premises do NOT substitute for the qualified electrical-scope human at the "
                "live moment."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Digital multimeter (DMM)",
                "specification": (
                    "CAT III rated for 600V or higher (CAT IV acceptable), with: a current "
                    "battery; test leads in good condition (no cracked insulation, no broken "
                    "shrouds, no exposed conductor); a current fuse on the current-measurement "
                    "range; calibration current per the household's or employer's program if "
                    "applicable. Fluke, Klein, Ideal, Amprobe, and other recognized industrial "
                    "brands at the named CAT rating are acceptable. Inexpensive automotive or "
                    "hobby meters typically lack the CAT rating and are NOT acceptable for this "
                    "measurement per NFPA 70E."
                ),
                "alternatives": [],
            },
            {
                "name": "A known live voltage source for the live-dead-live verification",
                "specification": (
                    "A standard 120V wall receptacle near the work area, OR a manufactured "
                    "proving unit (also called a voltage tester proving unit) that provides a "
                    "verifiable voltage. The known live source is used to verify the meter is "
                    "reading correctly BEFORE and AFTER the dead test at the work point. The "
                    "qualified human present confirms the live source is actually live before "
                    "the learner uses it."
                ),
                "alternatives": [],
            },
            {
                "name": "Lockout hardware (padlock)",
                "specification": (
                    "A padlock that fits the disconnect's lockout provision (most outdoor AC "
                    "disconnects have a hasp or provision for a padlock; pull-out disconnects "
                    "are 'locked' by removing the pull-out and storing it with the worker, "
                    "though a padlock through the body is still preferred where the disconnect "
                    "supports it). Color: red is conventional for personnel locks. The key is "
                    "kept exclusively by the person performing the work for the duration of the "
                    "lockout; no shared keys, no master overrides."
                ),
                "alternatives": [],
            },
            {
                "name": "Tagout tag",
                "specification": (
                    "A danger tag per OSHA 29 CFR 1910.145, signed and dated by the person "
                    "performing the work, naming the reason for the lockout and the date. The "
                    "tag is attached to the locked disconnect along with the lock; the tag is "
                    "NOT a substitute for the lock."
                ),
                "alternatives": [],
            },
            {
                "name": "The unit's nameplate card from hc-001",
                "specification": "Used to confirm the expected voltage (so the meter reads the expected value on the live test)",
                "alternatives": [],
            },
            {
                "name": "The unit's component-identification card from hc-002",
                "specification": "Used to confirm which disconnect serves which unit and where the work point is",
                "alternatives": [],
            },
            {
                "name": "Insulating gloves rated for the voltage",
                "specification": (
                    "Class 00 or higher per NFPA 70E for residential 240V verification, inspected "
                    "per the manufacturer and OSHA before use (visual inspection for cuts, "
                    "punctures, ozone cracking; air-roll test per the manufacturer where "
                    "applicable). The qualified human present confirms the glove rating and the "
                    "inspection."
                ),
                "alternatives": [],
            },
            {
                "name": "Safety glasses (ANSI Z87.1)",
                "specification": "Worn throughout the procedure",
                "alternatives": [],
            },
            {
                "name": "Camera (cell phone is sufficient) for the LOTO and procedure photographs",
                "specification": "Used to photograph the locked disconnect with the tag attached, for the artifact",
                "alternatives": [],
            },
            {
                "name": "The household's or employer's written lockout-tagout procedure",
                "specification": (
                    "OSHA 29 CFR 1910.147 requires a written, equipment-specific LOTO procedure "
                    "for service work. The household's or employer's procedure for the specific "
                    "equipment is read and followed; this node defers to that procedure for the "
                    "specific steps and confirms the procedure exists per OSHA. If no written "
                    "procedure exists for the equipment, the qualified human present produces "
                    "one before the work begins."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Dry outdoor pad or interior mechanical space at the disconnect's location",
            "ventilation": "Adequate; weather conditions dry (no rain, no standing water)",
            "lighting": "Adequate to clearly see the meter face, the test leads, the disconnect terminals, and the lockout hardware",
            "power": (
                "Power state is the work itself: the procedure begins with the system energized "
                "(to verify the live state), proceeds through disconnect operation and lockout, "
                "verifies dead at the work point, and re-verifies the meter on the known live "
                "source after the dead test. The disconnect is restored only after the lockout "
                "is released by the person who applied it and only after the work for which the "
                "lockout was applied is complete."
            ),
            "containment": "Clear floor space around the disconnect; pets and small children excluded from the work area",
        },
        "skill_description": (
            "The learner, with a qualified human (licensed electrician or licensed HVAC "
            "technician with electrical scope) physically present, performs the live-dead-live "
            "voltage verification at a residential outdoor AC condenser disconnect using a "
            "CAT III or higher rated digital multimeter and the lockout-tagout procedure per "
            "OSHA 29 CFR 1910.147 and NFPA 70E. The procedure: (1) review the nameplate from "
            "hc-001 to confirm the expected voltage; (2) review the component identification "
            "from hc-002 to confirm the correct disconnect for the unit; (3) put on insulating "
            "gloves and safety glasses; (4) inspect the multimeter and its leads; (5) verify "
            "the meter on a known live source (a nearby 120V receptacle or a proving unit), "
            "reading the expected voltage; this is the FIRST live test; (6) operate the "
            "disconnect to the open position (or remove the pull-out if it is a pull-out type); "
            "(7) apply the padlock to the lockout provision and the signed and dated tag, "
            "keeping the key exclusively with the person performing the work; (8) at the work "
            "point (typically the load-side terminals of the disconnect, or the line-voltage "
            "terminals inside the unit cabinet under the qualified human's supervision), verify "
            "voltage is now zero by testing every pair of conductors that should be dead (L1 "
            "to ground, L2 to ground, L1 to L2 for a 240V/1-phase circuit); this is the DEAD "
            "test; (9) re-verify the meter on the known live source from step 5, reading the "
            "expected voltage again; this is the SECOND live test, confirming the meter is "
            "still functioning correctly and the dead reading from step 8 is valid; (10) "
            "document the verification by photographing the locked disconnect with the tag in "
            "place; (11) the unit is now safe to open for downstream service work, which is its "
            "own competency. The learner narrates each step aloud as they perform it; the "
            "qualified human watches the meter readings, the probe placements, and the lockout "
            "sequence; the qualified human signs off on the verification before any downstream "
            "work begins. At the end of the service work, the lockout is released by the same "
            "person who applied it: tag removed, lock removed, disconnect operated to the "
            "closed position, system restored to operating state. The AI tutor reviews the "
            "written procedure, the LOTO photograph, and the learner's narrated walkthrough "
            "after the session; the AI does NOT replace the qualified human at the live "
            "moment."
        ),
        "demonstration_criteria": [
            (
                "Reviews the nameplate card from hc-001 BEFORE starting and names the expected "
                "voltage; confirms the multimeter range will cover the expected voltage"
            ),
            (
                "Reviews the component identification card from hc-002 BEFORE starting and "
                "identifies the correct disconnect for the unit"
            ),
            (
                "Inspects the multimeter and leads BEFORE the live test: battery indicator OK, "
                "leads visually intact, fuse intact (the qualified human confirms by inspection)"
            ),
            (
                "Performs the FIRST live test on the known live source (120V receptacle or "
                "proving unit), reads the expected voltage, and announces the reading aloud; "
                "the qualified human confirms the reading"
            ),
            (
                "Operates the disconnect to the open position (or removes the pull-out) "
                "correctly per the disconnect type"
            ),
            (
                "Applies the padlock to the lockout provision and attaches the signed and "
                "dated tag; keeps the key exclusively with the person performing the work; "
                "the qualified human confirms the lock is properly engaged and the tag is "
                "legible per OSHA 1910.145"
            ),
            (
                "Performs the DEAD test at the work point, testing every pair of conductors "
                "that should be dead (for residential 240V/1-phase: L1 to ground, L2 to ground, "
                "L1 to L2), announces each reading aloud; the qualified human confirms each "
                "probe placement and each reading"
            ),
            (
                "Performs the SECOND live test on the same known live source from the first "
                "live test, reads the expected voltage, and announces the reading aloud; the "
                "qualified human confirms the reading and signs off that the dead test from "
                "the previous step is valid"
            ),
            (
                "Photographs the locked disconnect with the tag in place and submits the photo "
                "to the AI tutor with a written narration of each step of the procedure as "
                "performed"
            ),
            (
                "Names the rule that the lockout is released ONLY by the person who applied it, "
                "and ONLY after the work for which the lockout was applied is complete; "
                "demonstrates the release sequence at the end of the practice session "
                "(restoring the disconnect to operating state) under the qualified human's "
                "supervision"
            ),
            (
                "Names what would invalidate the dead reading and require restarting the "
                "sequence: meter fails the second live test; tag or lock disturbed during the "
                "work; the procedure deviates from OSHA 1910.147 in any material way; the "
                "wrong disconnect is identified mid-procedure; a backfeed source is suspected"
            ),
            (
                "Names that this competency covers ONLY the line-voltage verification at the "
                "disconnect; the low-voltage control circuit is verified separately (off at the "
                "thermostat, dead at the contactor; not in this competency); the capacitor is "
                "discharged separately (a different competency); refrigerant work happens "
                "separately under EPA Section 608 with a 608-certified person present (a "
                "different competency); and gas-system work is separate (a different "
                "competency)"
            ),
        ],
        "common_errors": [
            {
                "error": "Skipping the first live test (testing the meter on the known live source before the dead test)",
                "cause": "The learner felt the procedure was familiar and went straight to the disconnect",
                "remedy": (
                    "The live-dead-live sequence is non-negotiable. Without the first live test, "
                    "a dead reading at the disconnect could mean (a) the disconnect is really "
                    "open OR (b) the meter is broken. The first live test rules out (b). The "
                    "qualified human present halts the procedure and requires the live test "
                    "before the dead test. This is what NFPA 70E mandates."
                ),
            },
            {
                "error": "Skipping the second live test (re-verifying the meter on the known live source AFTER the dead test)",
                "cause": "The learner read zero at the disconnect and assumed the meter was still good",
                "remedy": (
                    "The meter could have failed between the first live test and the dead test "
                    "(a blown fuse during the dead test is a classic failure mode). The second "
                    "live test confirms the meter is still functioning AND that the dead "
                    "reading is valid. The qualified human present requires the second live "
                    "test before the lockout is considered complete."
                ),
            },
            {
                "error": "Testing only L1 to L2 and skipping the conductor-to-ground readings",
                "cause": "The learner read the line-to-line voltage and called the circuit dead",
                "remedy": (
                    "Both conductors can be live to ground while reading zero line-to-line "
                    "(both at the same nonzero potential relative to ground, a real fault "
                    "condition). Every pair that should be dead is tested: L1 to ground, L2 to "
                    "ground, L1 to L2. All three must read zero."
                ),
            },
            {
                "error": "Using a CAT II or unrated meter for the 240V measurement",
                "cause": "The learner used the meter that was in the toolbag without checking the CAT rating",
                "remedy": (
                    "The CAT rating addresses the transient voltage the meter is designed to "
                    "survive. A CAT II meter on a CAT III circuit can explode in the user's "
                    "hand during a fault. CAT III at 600V minimum is the rule per NFPA 70E for "
                    "this measurement. The qualified human present confirms the CAT rating "
                    "before the procedure begins."
                ),
            },
            {
                "error": "Trusting the disconnect position without verifying",
                "cause": "The learner saw the disconnect in the open position and skipped the meter test",
                "remedy": (
                    "Position is not verification. The disconnect could be mechanically open "
                    "but electrically passing voltage (broken switch, miswire, backfeed). The "
                    "meter verification at the work point is the only safeguard. Every time."
                ),
            },
            {
                "error": "Leaving the key in the lock or giving it to someone else",
                "cause": "The learner walked away to get a tool and handed the key to the supervising adult",
                "remedy": (
                    "The key is kept EXCLUSIVELY with the person performing the work for the "
                    "duration of the lockout per OSHA 1910.147. No shared keys, no temporary "
                    "handoffs. If the learner must leave, the lock comes off and the procedure "
                    "is restarted on return."
                ),
            },
            {
                "error": "Performing the procedure in the rain or on a wet pad",
                "cause": "The learner did not weigh the weather against the work",
                "remedy": (
                    "Wet conditions significantly increase shock risk. The procedure is deferred "
                    "to dry conditions. If urgent, the qualified human present decides whether "
                    "additional PPE per NFPA 70E justifies proceeding; the default is to defer."
                ),
            },
            {
                "error": "Reaching for the capacitor terminals after the disconnect is verified dead",
                "cause": "The learner thought the cabinet was now fully safe",
                "remedy": (
                    "The capacitor stores a charge that persists after line voltage is removed. "
                    "Discharging the capacitor is a DIFFERENT competency, not part of this one. "
                    "After the line-voltage dead verification, the cabinet is safe to OPEN; "
                    "contact with internal components requires its own qualifications and "
                    "competencies."
                ),
            },
            {
                "error": "Operating the disconnect or removing the lock to test a downstream component before completing the work",
                "cause": "The learner felt the procedure was 'paused' and could be resumed",
                "remedy": (
                    "The lockout is in place for the duration of the work. If a downstream test "
                    "requires the system to be energized, the lock comes off in the OSHA-"
                    "compliant sequence (tools cleared, personnel cleared, lock removed, "
                    "disconnect restored), the test is performed energized, and a NEW LOTO "
                    "sequence is performed before any further work inside the cabinet. The "
                    "qualified human present manages this sequencing."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "A photograph showing: (1) the locked disconnect with the padlock engaged and "
                "the signed-and-dated tag attached; (2) the multimeter display reading the dead "
                "voltage at the work point (the photo can be of the meter on the leads, with the "
                "reading visible); (3) a separate photo of the meter reading the live voltage on "
                "the known live source, taken AFTER the dead test (the second live test). "
                "Submitted with a written narration of every step of the procedure as actually "
                "performed, including the announced readings at each test point. The qualified "
                "human present countersigns the narration."
            ),
            "what_the_evidence_shows": (
                "That the live-dead-live sequence was performed correctly per NFPA 70E, that "
                "the lockout was applied per OSHA 1910.147, that the dead test covered every "
                "conductor pair, and that the qualified human present confirmed each step. The "
                "AI tutor reviews the artifact for completeness against the demonstration "
                "criteria; the AI tutor does NOT countersign the live verification (only the "
                "qualified human can do that)."
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The qualified human (licensed electrician or HVAC technician with electrical "
                "scope) performs the full live-dead-live verification with formal LOTO on a "
                "real residential AC disconnect, narrating each step aloud and explaining why "
                "each step exists: the reason for the first live test (verify the meter), the "
                "reason for the LOTO before the dead test (defense in depth), the reason for "
                "every-pair-to-ground (catch both-live faults), the reason for the second live "
                "test (verify the meter still works after the dead test). The learner watches "
                "and the AI tutor (post-session, on the recorded narration) confirms the "
                "procedure walkthrough matches NFPA 70E and OSHA 1910.147."
            ),
            "we_do": (
                "The qualified human and the learner perform the procedure together on a second "
                "real disconnect. The learner takes the meter and announces each step; the "
                "qualified human watches every probe placement, confirms every reading, and "
                "applies the lock (or watches the learner apply it). At each transition (live "
                "test, disconnect open, LOTO applied, dead test, second live test, lockout "
                "released), the qualified human pauses and the learner narrates aloud what "
                "happens next and why."
            ),
            "you_do_supervised": (
                "The learner performs the full procedure on a third real disconnect with the "
                "qualified human physically present, watching the meter readings, the probe "
                "placements, and the LOTO sequence. The qualified human intervenes only if the "
                "learner is about to make a mistake that would invalidate the verification or "
                "create a hazard. After the procedure, the learner submits the LOTO photograph, "
                "the meter-reading photographs, and the written narration to the AI tutor; the "
                "AI tutor confirms the artifact covers every demonstration criterion. The "
                "qualified human countersigns the narration as having watched the live moment."
            ),
            "you_do_unsupervised": (
                "There is NO unsupervised band for this competency. Every live-dead-live "
                "verification on a real disconnect happens with a qualified human physically "
                "present. This is the rule that holds across the trade: the verification of the "
                "absence of voltage is a moment where a meter failure or a procedure failure "
                "can kill, and the qualified human is the safeguard against meter failure and "
                "procedure failure. The learner becomes journeyman in this competency by "
                "having performed the verification correctly on at least ten disconnects "
                "across at least five sessions, with at least two different qualified humans "
                "countersigning, and is then themselves the qualified-human-present for "
                "subsequent learners (which is itself a teaching-band competency, not in this "
                "first batch). The AI tutor continues to mentor the procedure walkthrough and "
                "review artifacts at every band."
            ),
        },
        "estimated_practice_sessions_to_signoff": 10,
        "session_length_minutes": 45,
        "signoff_validity_days": 365,
        "related_projects": [],
        "certification_alignment": {
            "ladder_rung": "apprentice",
            "supervision_rung": "qualified_human_physically_present",
            "notes": (
                "Apprentice-band gold standard. ELECTRICAL HAZARD. The qualified-human-"
                "physically-present rule is non-negotiable and unchanged by any credential the "
                "learner holds: the supervision rung stays at qualified-human-physically-"
                "present even when the learner themselves holds a state license, because this "
                "is the safety habit, not a credential gate. Adding the alignment metadata "
                "does not weaken any supervision rule; safety_basis and supervision_basis are "
                "unchanged."
            ),
            "certifications_supported": [
                {
                    "id": "hcert-osha",
                    "domains": [
                        "lockout-tagout per OSHA 29 CFR 1910.147",
                        "electrical safety practices per OSHA 29 CFR 1910.137 and 1910.335",
                        "PPE selection",
                    ],
                    "notes": "OSHA 10 / 30 covers LOTO and electrical safety as orientation; hc-021 is the demonstrated competency.",
                },
                {
                    "id": "hcert-licensing",
                    "domains": [
                        "electrical safety in the workplace per NFPA 70E",
                        "service disconnects per NEC Article 440 (HVAC) and 422 (appliances)",
                        "multimeter selection and use per IEC 61010-1 / UL 61010-1 Category Ratings",
                    ],
                    "notes": (
                        "Journeyman and master exams routinely test NFPA 70E concepts including "
                        "live-dead-live verification and the conditions for energized work. "
                        "hc-021 is the demonstrated competency for the live-dead-live habit."
                    ),
                },
                {
                    "id": "hcert-nate",
                    "domains": [
                        "electrical-safety domain across all NATE specialties' KATE",
                        "service-call electrical verification practice",
                    ],
                    "notes": "Every NATE specialty expects competent live-dead-live verification practice.",
                },
                {
                    "id": "hcert-epa608",
                    "domains": [
                        "system de-energization as the precondition for any refrigerant work (Core safety-practice domain)",
                    ],
                    "notes": (
                        "EPA 608 study touches the rule that refrigerant work happens on "
                        "de-energized systems; hc-021 is the demonstrated competency for the "
                        "de-energization step."
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
                "The household's or employer's written equipment-specific lockout-tagout procedure per OSHA 1910.147",
                "Manufacturer service literature for the specific multimeter, insulating gloves, lockout hardware, and HVAC equipment",
                "The qualified human's professional license (licensed HVAC technician with electrical scope OR licensed electrician) per the local jurisdiction; the qualified human's continuing-education currency in NFPA 70E",
            ],
        },
    },
    "hcert-epa608": {
        "node_type": "certification_prep",
        "trade": "hvac",
        "credential_name": "EPA Section 608 Technician Certification",
        "credential_body": "U.S. Environmental Protection Agency (EPA)",
        "credential_body_url": "https://www.epa.gov/section608",
        "authorizing_scope": (
            "Section 608 of the Clean Air Act requires that persons who maintain, service, "
            "repair, or dispose of appliances that contain regulated refrigerants be certified "
            "by an EPA-approved certifying body. The certification is the legal precondition in "
            "the United States to purchase regulated refrigerants in quantity and to handle "
            "refrigerant in any way that could release it to the atmosphere. Without it, a "
            "person may not legally open a refrigerant circuit, recover or recycle refrigerant, "
            "or service systems containing regulated refrigerant. The certification has four "
            "types issued by EPA-approved bodies: Type I (small appliances containing 5 lb or "
            "less of refrigerant); Type II (high- or very-high-pressure appliances except small "
            "appliances and motor vehicle air conditioning, which covers most residential and "
            "commercial split-system air conditioning and heat-pump equipment); Type III "
            "(low-pressure appliances, primarily chillers using low-pressure refrigerants); and "
            "Universal (all three types combined). The specific authorizing scope of each type, "
            "and the equipment covered, is defined by EPA at 40 CFR Part 82 Subpart F and at "
            "the EPA Section 608 program's published guidance."
        ),
        "knowledge_domains_covered": [
            (
                "Core: regulations and stratospheric ozone topics common to all four certification "
                "types; environmental basis of Section 608; recovery and recycling concepts at the "
                "introductory level; refrigerant safety practices; refrigerant identification and "
                "leak-detection concepts; record-keeping; venting prohibition under the Clean Air "
                "Act"
            ),
            (
                "Type I: small-appliance recovery techniques; passive vs. active recovery; "
                "system-dependent and self-contained recovery devices; safe handling of small "
                "appliances per EPA published guidance"
            ),
            (
                "Type II: high-pressure system service, recovery, and recycling; leak repair "
                "obligations under Section 608 for industrial process refrigeration, commercial "
                "refrigeration, and comfort cooling above thresholds published by EPA; "
                "evacuation and dehydration; oil change and filter procedures at the descriptive "
                "level; refrigerant transition guidance (R-410A to R-454B and R-32 under the AIM "
                "Act and the EPA SNAP program)"
            ),
            (
                "Type III: low-pressure appliance characteristics; rupture-disk and pressure-"
                "relief considerations; purge-unit operation at the descriptive level"
            ),
            ("Universal: the combined knowledge of all three types"),
        ],
        "eligibility": {
            "minimum_age": (
                "no federal age minimum set by EPA; testing programs may set their own age "
                "policies and the household confirms with the chosen testing program"
            ),
            "experience_requirements": (
                "none required by EPA for sitting the certification exam; some employers and "
                "vocational programs build the exam into a structured course"
            ),
            "prerequisites": [
                "none required by EPA; the learner takes the certification exam through an "
                "EPA-approved certifying body listed on the EPA Section 608 program page",
            ],
        },
        "exam_format_general": (
            "Multiple-choice examination administered by an EPA-approved certifying body. The "
            "Core section is taken once and is common to all four types. Each of Type I, II, "
            "and III is a separate section; passing all three plus Core grants Universal. Type "
            "I may be offered as an open-book mail-in exam through some approved bodies; Types "
            "II, III, and Universal are typically proctored. The current passing thresholds, "
            "section lengths, and any open-book / proctored designations are set and updated by "
            "EPA and the certifying body; the household and learner consult the EPA Section 608 "
            "program page and the chosen certifying body for current specifics."
        ),
        "legal_status": "legally_required",
        "prepares_understanding_only": True,
        "exam_taken_through": (
            "an EPA-approved certifying body (the EPA Section 608 program page lists the "
            "current approved certifying bodies; recognized examples have historically included "
            "ESCO Institute, RSES, Mainstream Engineering, and others; the household confirms "
            "current approval status on the EPA program page before paying for an exam). "
            "METHEAN does not administer or proctor the exam."
        ),
        "supervised_hours_through": None,
        "progression_band": "apprentice",
        "where_in_ladder": (
            "Late helper to early apprentice. Authored as a study-only credential the learner "
            "can earn before any hands-on refrigerant work, because the certification is "
            "legally required before any hands-on refrigerant work in the United States. "
            "Possession of EPA Section 608 certification is the precondition for the trade's "
            "refrigerant competencies (not yet authored in this batch); without it, hands-on "
            "refrigerant work is forbidden, with or without a mentor."
        ),
        "aligned_competencies": ["hs-001", "hc-001", "hc-002"],
        "study_resources_pointers": [
            (
                "The EPA Section 608 program page and EPA's published technician manual (the "
                "EPA manual is the authoritative reference)."
            ),
            (
                "Study guides published by EPA-approved certifying bodies (ESCO Institute, "
                "RSES, Mainstream Engineering, and others currently approved). The learner uses "
                "the study guide from the same body through which they will sit the exam."
            ),
            (
                "40 CFR Part 82 Subpart F (the federal regulation that Section 608 implements). "
                "The regulation itself is the authoritative legal text; the EPA program page is "
                "the user-facing summary."
            ),
        ],
        "mentor_model": (
            "AI tutor mentors end-to-end. This is study, not hands-on work. The AI tutor walks "
            "the learner through the published knowledge domains, quizzes against the official "
            "study guide's structure, and tracks readiness. METHEAN does not administer the "
            "exam; the learner sits the exam through an EPA-approved certifying body. Hands-on "
            "refrigerant work remains gated by the refrigerant competencies (not yet authored) "
            "which require a 608-certified person physically present even after the learner "
            "themselves earns the certification, per the apprenticeship pedagogy of supervised "
            "practice before independent practice."
        ),
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                "Section 608 of the Clean Air Act and 40 CFR Part 82 Subpart F (the federal regulation)",
                "The current EPA Section 608 program page and published technician manual",
                "The current list of EPA-approved certifying bodies (status changes; the household confirms current approval before paying for an exam)",
                "The AIM Act of 2020 and EPA SNAP program rulemaking, for the R-410A to A2L (R-454B, R-32) transition",
            ],
        },
    },
    "hcert-licensing": {
        "node_type": "certification_prep",
        "trade": "hvac",
        "credential_name": "State HVAC apprenticeship and journeyman / master licensing path",
        "credential_body": (
            "The Authority Having Jurisdiction (AHJ) for HVAC licensing in the learner's state, "
            "county, or municipality. In the United States, HVAC licensing is regulated at the "
            "state level (and in some states at the county or municipal level); there is no "
            "single federal HVAC license. The learner identifies their AHJ before pursuing "
            "this credential."
        ),
        "credential_body_url": None,
        "authorizing_scope": (
            "Licensing authorizes the holder to perform HVAC work as an employee (apprentice or "
            "journeyman) or as a contractor (master / contractor license), within the scope and "
            "the geographic jurisdiction the license names. Specific scopes (residential, "
            "commercial, refrigeration, gas-fitting, hydronics, mechanical contracting) vary by "
            "AHJ. In states with no statewide HVAC license, municipal or county licenses may "
            "still apply; in states with statewide licensing, the AHJ publishes the apprenticeship "
            "hours, the journeyman experience requirement, the master experience requirement, "
            "the bonding and insurance requirements for contractors, and the continuing-education "
            "requirements. The credential's authorizing scope is what the AHJ publishes, not what "
            "this node summarizes."
        ),
        "knowledge_domains_covered": [
            (
                "Core technical knowledge typically tested at the journeyman level: the NEC "
                "(NFPA 70) for HVAC-related electrical; the NFPA 54 National Fuel Gas Code "
                "where the license includes gas; the IMC (International Mechanical Code) or "
                "UMC (Uniform Mechanical Code) per the AHJ's adoption; the local jurisdiction's "
                "adopted codes and amendments; refrigeration theory; load calculations (Manual J "
                "or equivalent); duct design (Manual D or equivalent); equipment selection "
                "(Manual S or equivalent); controls; combustion fundamentals; HVAC safety "
                "practices including NFPA 70E"
            ),
            (
                "Business and contract knowledge typically tested at the master / contractor "
                "level: the state's contracting law; lien law; estimating; bonding and "
                "insurance; OSHA general industry and construction; tax and employment basics"
            ),
            (
                "The specific exam blueprint per the AHJ; the household and learner obtain the "
                "current blueprint from the AHJ before scheduling an exam"
            ),
        ],
        "eligibility": {
            "minimum_age": (
                "varies by AHJ; commonly 18 for journeyman and master; some states allow younger registered apprentices"
            ),
            "experience_requirements": (
                "apprenticeship hours and journeyman experience varies widely by AHJ; common "
                "ranges are several thousand hours for journeyman eligibility and additional "
                "years of journeyman experience for master eligibility, but the AHJ's current "
                "published requirements are authoritative and the learner confirms them"
            ),
            "prerequisites": [
                (
                    "registered apprenticeship through a state-approved apprenticeship sponsor "
                    "or an equivalent pathway the AHJ recognizes (employer-based, vocational "
                    "program, joint labor-management committee); the learner confirms recognized "
                    "pathways with the AHJ"
                ),
                (
                    "for master / contractor licensing additionally: passing the journeyman "
                    "exam OR documenting equivalent experience the AHJ accepts; insurance; "
                    "bonding; possibly a contractor's business exam"
                ),
            ],
        },
        "exam_format_general": (
            "Format varies by AHJ; commonly proctored multiple-choice for journeyman and master "
            "trade exams, plus a business and law exam for contractor licensing in many states. "
            "Some AHJs offer practical components. The exam blueprint, format, passing score, "
            "and any open-book provisions are published by the AHJ; the learner consults the "
            "AHJ for current specifics."
        ),
        "legal_status": "jurisdiction_specific",
        "prepares_understanding_only": True,
        "exam_taken_through": (
            "The AHJ or its authorized testing partner (commonly Prov Inc., PSI, or another "
            "state-approved testing service). METHEAN does not administer or proctor the exam."
        ),
        "supervised_hours_through": (
            "A state-approved apprenticeship program or recognized employer-based "
            "apprenticeship. METHEAN's practice sessions and portfolio work are NOT a "
            "substitute for registered apprenticeship hours; the household confirms with the "
            "AHJ which programs are recognized for hours-credit toward licensing eligibility."
        ),
        "progression_band": "journeyman",
        "where_in_ladder": (
            "Journeyman exam: at the late apprentice to early journeyman band, after the "
            "learner has completed the AHJ's hours requirement through a recognized "
            "apprenticeship and is ready to test. Master / contractor exam: at the qualified "
            "band, after several years of journeyman work plus the additional master "
            "eligibility the AHJ requires. The METHEAN trade prepares conceptual understanding "
            "and a portfolio that demonstrates competence; the hours and the exam are taken "
            "outside METHEAN."
        ),
        "aligned_competencies": ["hs-001", "hc-001", "hc-002", "hc-021"],
        "study_resources_pointers": [
            "The AHJ's published exam blueprint and approved reference list",
            ("The NEC (NFPA 70), NFPA 54, and the IMC or UMC (per AHJ adoption), the current adopted editions"),
            ("NFPA 70E and OSHA 29 CFR 1910 / 1926 (the relevant subparts for HVAC), as supporting safety references"),
            (
                "ACCA Manuals J, S, D (load, equipment selection, duct design); ASHRAE "
                "Handbooks (HVAC Systems and Equipment, Refrigeration, Fundamentals, "
                "Applications) at the depth the AHJ's exam expects"
            ),
            (
                "AHJ-recommended study courses (commonly offered by the apprenticeship sponsor, "
                "the state community-college system, or recognized commercial providers)"
            ),
        ],
        "mentor_model": (
            "AI tutor mentors the conceptual study end-to-end. The AI walks the learner "
            "through code structure, load and duct calculation methods, controls, and the "
            "AHJ's published exam blueprint. The portfolio of demonstrated work from METHEAN "
            "(competency artifacts, service-call write-ups, install documentation) is presented "
            "as supporting evidence of experience, but the AHJ's recognized hours come from a "
            "state-approved apprenticeship program, not from METHEAN. The hands-on competencies "
            "stay gated by the trade's existing supervision policy regardless of credential "
            "status; possession of a journeyman license does not by itself authorize "
            "unsupervised practice on hazardous subsystems until the learner has demonstrated "
            "the specific competencies at the qualified band."
        ),
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                "The learner's state (or county / municipality) HVAC licensing AHJ's currently published rules and exam blueprint",
                "NFPA 70 (NEC), NFPA 54 (National Fuel Gas Code), IMC or UMC per AHJ adoption",
                "NFPA 70E for electrical safety in the workplace",
                "OSHA 29 CFR 1910 (general industry) and 1926 (construction), the relevant subparts",
                "ACCA Manuals J / S / D and ASHRAE Handbooks for design domains the AHJ tests",
                "State approved apprenticeship program rules and any recognized alternate-pathway rules the AHJ publishes",
            ],
        },
    },
    "hcert-nate": {
        "node_type": "certification_prep",
        "trade": "hvac",
        "credential_name": "NATE (North American Technician Excellence) certifications",
        "credential_body": "North American Technician Excellence (NATE)",
        "credential_body_url": "https://natex.org",
        "authorizing_scope": (
            "NATE is an industry-recognized, voluntary technician-certification program. NATE "
            "certifications do not legally authorize work that a state license does not (they "
            "are not a substitute for state HVAC licensing where licensing is required, and "
            "they are not a substitute for EPA Section 608 for refrigerant handling). NATE "
            "attests to a technician's demonstrated knowledge in a specific specialty area, and "
            "is widely recognized by employers, contractors, and customers as a mark of "
            "professional competence. NATE offers entry-level (Ready to Work, HVAC Support "
            "Technician) and core / specialty / senior-level certifications across air "
            "conditioning, air distribution, gas heating, oil heating, heat pumps, light "
            "commercial refrigeration, commercial refrigeration, hydronics gas, hydronics oil, "
            "ground-source heat pumps, and others. The specific current certification offerings "
            "and exam blueprints are published on the NATE website."
        ),
        "knowledge_domains_covered": [
            (
                "Per specialty: the NATE Knowledge Areas of Technician Expertise (KATE) for "
                "that specialty, published by NATE on the natex.org website. KATEs vary by "
                "specialty and cover the technical knowledge a competent technician needs in "
                "that area (diagnostics, installation, service)."
            ),
            (
                "Across all specialties: refrigeration cycle theory, electrical fundamentals "
                "for HVAC, controls, safety, and code-aware service practice at the depth "
                "NATE's current published exam blueprint expects"
            ),
        ],
        "eligibility": {
            "minimum_age": "no NATE-published minimum; testing partners may set their own policies",
            "experience_requirements": (
                "NATE recommends but does not require specific experience for the core / "
                "specialty certifications; the senior-level certification has additional "
                "experience and credential prerequisites. The current eligibility per "
                "certification is on the NATE website."
            ),
            "prerequisites": [
                "Per certification: see the current NATE published eligibility on natex.org",
            ],
        },
        "exam_format_general": (
            "Proctored multiple-choice examinations administered by NATE-approved testing "
            "partners. Format, exam length, and passing scores are set by NATE and published "
            "on the NATE website. Some certifications require a Core exam plus a specialty "
            "exam."
        ),
        "legal_status": "optional",
        "prepares_understanding_only": True,
        "exam_taken_through": (
            "NATE-approved testing partners listed on the NATE website. METHEAN does not "
            "administer or proctor the exam."
        ),
        "supervised_hours_through": None,
        "progression_band": "journeyman",
        "where_in_ladder": (
            "Entry-level NATE certifications (Ready to Work, HVAC Support Technician) at the "
            "late helper to apprentice band as an industry-recognized acknowledgment of basic "
            "readiness. Core / specialty certifications at the late apprentice to journeyman "
            "band as the learner builds competence in a chosen subsystem (gas heating, heat "
            "pumps, light commercial refrigeration, etc.). Senior-level certifications at the "
            "qualified band, after several years of practice and the journeyman state license "
            "(where applicable). NATE complements the state license; it does not replace it."
        ),
        "aligned_competencies": ["hs-001", "hc-001", "hc-002", "hc-021"],
        "study_resources_pointers": [
            (
                "The NATE website's current published Knowledge Areas of Technician Expertise "
                "(KATE) for the chosen specialty"
            ),
            "NATE-recognized study materials and exam-prep courses listed on the NATE website",
            (
                "The technical references (manufacturer service literature, ACCA manuals, "
                "ASHRAE Handbooks) covering the specialty area's subject matter"
            ),
        ],
        "mentor_model": (
            "AI tutor mentors end-to-end study. The AI walks the learner through the published "
            "KATE for the chosen specialty, quizzes against the structure NATE publishes, and "
            "tracks readiness. METHEAN does not administer the exam; the learner sits the exam "
            "through a NATE-approved testing partner. NATE certification is complementary to "
            "state licensing and EPA Section 608; the safety and supervision gates on hands-on "
            "competencies are unchanged by possession of NATE certifications."
        ),
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                "The current NATE website (natex.org) for certification offerings, KATE, eligibility, exam format, and approved testing partners",
                "NATE's relationship to state licensing and EPA Section 608 (NATE is complementary, not a substitute)",
            ],
        },
    },
    "hcert-osha": {
        "node_type": "certification_prep",
        "trade": "hvac",
        "credential_name": "OSHA 10-Hour and 30-Hour Outreach Training (General Industry and Construction)",
        "credential_body": (
            "U.S. Occupational Safety and Health Administration (OSHA), through OSHA-authorized "
            "Outreach Training Program trainers"
        ),
        "credential_body_url": "https://www.osha.gov/training/outreach",
        "authorizing_scope": (
            "The OSHA 10-Hour and 30-Hour Outreach courses are voluntary worker-orientation "
            "training programs administered by OSHA-authorized trainers. They are not licenses "
            "or certifications in the legal sense, do not authorize the holder to perform any "
            "specific work, and are not a substitute for site-specific safety training or for "
            "employer training required by specific OSHA standards (lockout-tagout, fall "
            "protection, confined-space entry, etc.). They are widely required or recommended "
            "by employers, by general contractors on construction projects, and by some states "
            "or municipalities for entry to particular work sites, as evidence the worker has "
            "received baseline OSHA orientation. Many HVAC employers and apprenticeship "
            "sponsors require at least the OSHA 10 for new technicians and the OSHA 30 for "
            "supervisors or lead technicians."
        ),
        "knowledge_domains_covered": [
            (
                "OSHA 10-Hour General Industry / Construction: introduction to OSHA; general "
                "safety and health provisions; recognition of common workplace hazards "
                "including electrical, fall, struck-by, caught-in/between, fire, and chemical "
                "hazards; PPE; basic introduction to OSHA 1910 (general industry) or OSHA 1926 "
                "(construction) depending on which version is taken. HVAC technicians on "
                "construction projects commonly take the construction version (1926); HVAC "
                "technicians in service-only work commonly take the general industry version "
                "(1910). The exact topic list and time allocation is set by OSHA and the "
                "authorized trainer."
            ),
            (
                "OSHA 30-Hour General Industry / Construction: a deeper version of the same "
                "topics with additional depth and additional elective topics, intended for "
                "workers with supervisory responsibility. The exact topic list and time "
                "allocation is set by OSHA and the authorized trainer."
            ),
        ],
        "eligibility": {
            "minimum_age": "no OSHA-published minimum",
            "experience_requirements": "none",
            "prerequisites": [
                (
                    "registration with an OSHA-authorized Outreach Training Program trainer "
                    "(online or in-person); the OSHA Outreach Training Program page lists "
                    "authorized providers and the rules trainers must follow"
                ),
            ],
        },
        "exam_format_general": (
            "The 10-Hour and 30-Hour courses are training programs, not exams. Successful "
            "completion (attending the required hours, completing any in-course assessments "
            "per the authorized trainer's rules per OSHA) results in OSHA-issued Department of "
            "Labor completion cards. The exact in-course assessment format is set by the "
            "authorized trainer per OSHA's Outreach Training Program rules."
        ),
        "legal_status": "optional",
        "prepares_understanding_only": True,
        "exam_taken_through": (
            "An OSHA-authorized Outreach Training Program trainer. METHEAN does not deliver "
            "the 10-Hour or 30-Hour course and does not issue the completion cards; only "
            "OSHA-authorized trainers may do so per OSHA's Outreach Training Program rules. "
            "The learner enrolls with an authorized trainer (online or in-person) listed via "
            "the OSHA Outreach Training Program page."
        ),
        "supervised_hours_through": None,
        "progression_band": "helper",
        "where_in_ladder": (
            "Helper to early apprentice. Authored here because the OSHA 10 in particular is a "
            "common employer prerequisite for entry to HVAC work, and because the topics it "
            "covers (electrical hazard recognition, fall protection awareness, struck-by and "
            "caught-in/between, PPE, hazard communication) reinforce the safety walkthrough in "
            "hs-001 and prepare the learner for the safety vocabulary used across all higher "
            "bands. OSHA 30 typically arrives at the apprentice to journeyman band as the "
            "learner takes on more responsibility on a job site."
        ),
        "aligned_competencies": ["hs-001", "hc-021"],
        "study_resources_pointers": [
            "The OSHA Outreach Training Program page on osha.gov for current rules, authorized trainer lists, and any updates",
            "OSHA's published General Industry standards (29 CFR 1910) and Construction standards (29 CFR 1926), free on osha.gov",
            (
                "Training materials from OSHA-authorized Outreach Training Program trainers; "
                "the learner uses the materials from the same trainer through whom they will "
                "take the course"
            ),
        ],
        "mentor_model": (
            "AI tutor mentors the conceptual orientation and reinforces the topics that "
            "overlap with the HVAC trade's existing safety competency (hs-001) and the "
            "live-dead-live verification (hc-021). The actual 10-Hour or 30-Hour course is "
            "delivered by an OSHA-authorized trainer; the OSHA-issued completion card is the "
            "credential and comes from the trainer, not from METHEAN."
        ),
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                "OSHA Outreach Training Program page on osha.gov (the authoritative reference for current rules)",
                "OSHA 29 CFR 1910 (General Industry) and 29 CFR 1926 (Construction), the relevant subparts",
                "OSHA's published Outreach Training Program Guidelines and Procedures, which set the rules authorized trainers must follow",
            ],
        },
    },
}
