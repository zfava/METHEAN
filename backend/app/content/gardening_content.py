"""Gardening / horticulture trade content (food-garden first).

Three node shapes live here per docs/curriculum/METHEAN_trades_design.md:
the trade root (gardening-root), one safety competency (gs-001), and
many technique competencies (gc-NNN). Trades do not carry the
five-philosophy block; they carry a single apprenticeship pedagogy
block. Safety is gating: every hands-on competency prereqs the entry
safety node gs-001.

The starting set authored here is bottom-up from safety. gc-021
(transplant a tray of seedlings to a prepared bed) is the gold-standard
exemplar, authored at the apprentice band, after its helper-band
prerequisites gc-001 (read a seed packet) and gc-002 (use a trowel to
dig a planting hole) and the trade safety competency gs-001.

Hazard posture: gardening is lower-hazard than woodworking, but real
hazards remain (sun and heat exposure, soil-borne wounds and tetanus
risk, sharp hand tools, allergens, lifting strain). Regulated topics
defer to recognized standards by name (CDC, ANSI/ISEA Z308.1, state
cooperative extension, EPA, the household's healthcare provider). No
node invents a tetanus interval, an SPF number, a regional toxic-plant
list, or a pesticide label.
"""

GARDENING_CONTENT: dict[str, dict] = {
    "gardening-root": {
        "node_type": "root",
        "trade": "agriculture",
        "trade_name": "Gardening and horticulture (food-garden first)",
        "description": (
            "The gardening trade taught food-garden first: read a seed packet, dig a "
            "planting hole, prepare a bed, sow and transplant, water, mulch, weed, "
            "scout for pests, harvest, save seed. Ornamental work and orchard work "
            "follow once the food-garden bands are in. The trade is seasonal and "
            "year-long: practice runs across spring sowing, summer tending, autumn "
            "harvest and storage, and winter planning. Foundational competencies "
            "carry over to small-fruit, herb, and ornamental gardens."
        ),
        "default_supervision_policy": {
            "hand_tool_work": (
                "Supervised through the helper band as a default; mentor on premises "
                "through the apprentice band for any work with a sharp hand tool; "
                "optional at journeyman with a current safety signoff."
            ),
            "power_tool_work": (
                "Supervised through journeyman without exception. String trimmers, "
                "mowers, tillers, and chainsaws are each gated by their own safety "
                "competency, not authored in this first batch."
            ),
            "ladder_work": (
                "Supervised through journeyman without exception. Orchard pruning "
                "from a ladder is gated by its own safety competency, not authored "
                "in this first batch."
            ),
            "chemical_application": (
                "Pesticide and herbicide application is supervised by an adult who "
                "has read the product label and any state requirements; pesticide "
                "application is not authored in the helper or apprentice bands. The "
                "household defers to the EPA label and the state's cooperative "
                "extension for application practice."
            ),
        },
        "safety_node": "gs-001",
        "progression_bands": ["helper", "apprentice", "journeyman", "qualified"],
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
}
