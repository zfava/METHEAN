"""Woodworking trade content (hand-tool first).

Three node shapes live here per docs/curriculum/METHEAN_trades_design.md:
the trade root (woodworking-root), one or more safety competencies
(ws-NNN), and many technique competencies (wc-NNN). Trades do not carry
the five-philosophy block; they carry a single apprenticeship pedagogy
block. Safety is gating: every hands-on competency prereqs the entry
safety node ws-001.

The starting set authored here is bottom-up from safety. wc-021
(cross-cut to a line with a panel saw) is the gold-standard exemplar,
authored at the apprentice band, after its helper-band prerequisites
wc-001 (measure) and wc-002 (mark a square line) and the trade safety
competency ws-001.
"""

WOODWORKING_CONTENT: dict[str, dict] = {
    "woodworking-root": {
        "node_type": "root",
        "trade": "woodworking",
        "trade_name": "Woodworking (hand-tool first)",
        "description": (
            "The woodworking trade taught hand-tool first: panel saw, marking gauge, "
            "try square, chisel, plane, brace and auger bits, coping saw, sharpening "
            "setup. Power tools enter later, behind their own safety gate. The trade "
            "is foundational: measure, mark, square, cut, fasten, finish. Every other "
            "physical trade reuses these competencies."
        ),
        "default_supervision_policy": {
            "hand_tool_work": (
                "Supervised through the helper band as a default; mentor on premises "
                "through the apprentice band; optional at journeyman with a current "
                "safety signoff."
            ),
            "power_tool_work": (
                "Supervised through journeyman without exception. Power-tool work is "
                "gated by its own safety competency, not authored in this first batch."
            ),
        },
        "safety_node": "ws-001",
        "progression_bands": ["helper", "apprentice", "journeyman", "qualified"],
    },
}
