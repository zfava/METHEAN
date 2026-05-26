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
            (
                "Locates the nameplate on a piece of household HVAC equipment without opening "
                "any enclosure"
            ),
            (
                "Photographs the nameplate clearly enough that every printed field is legible "
                "in the image"
            ),
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
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
}
