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
}
