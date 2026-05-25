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
    "ws-001": {
        "node_type": "safety",
        "trade": "woodworking",
        "competency_name": "Woodworking shop safety: hand tools and the workbench",
        "progression_band": "helper",
        "prerequisites": [],
        "safety_basis": {
            "hazards": [
                (
                    "Sharp edges: chisels, plane irons, marking knives, and saws are sharper "
                    "than they look; a sharp tool dropped point-down can pierce a shoe."
                ),
                ("Workpiece motion: a board that is not held still becomes a hazard the moment a tool engages it."),
                (
                    "Sawdust and shavings on the floor: shavings underfoot are slippery and "
                    "tools dropped into shavings can be hard to see."
                ),
                (
                    "Oily rags: rags soaked in linseed oil, boiled linseed oil, tung oil, or "
                    "danish oil can self-heat and ignite if balled up; they must be laid flat "
                    "outdoors to dry or stored in a sealed metal can with water."
                ),
                (
                    "Eye injury from chips, sawdust, or sharpening swarf, especially in overhead "
                    "work, in dry or pitchy stock, and at the grinder or stones."
                ),
                (
                    "Allergic or toxic reactions to specific woods (cocobolo, padauk, rosewoods, "
                    "yew, some other tropical hardwoods); an unfamiliar wood is identified before "
                    "it is cut."
                ),
                (
                    "Wrist-line cuts: putting a hand or any body part in the path the cutting edge "
                    "will travel through if it slips."
                ),
            ],
            "ppe_required": [
                (
                    "Closed-toe shoes (leather work shoes or boots preferred; no sandals or open "
                    "footwear; cloth sneakers offer little protection from a dropped chisel)"
                ),
                (
                    "Safety glasses for any sharpening, any overhead work, any work with dry or "
                    "pitchy stock, and any unfamiliar operation; default is to wear them"
                ),
                "Hair tied back if it would fall forward over the bench",
                "No loose sleeves, no scarves, and no jewelry near the cut path",
                (
                    "No gloves when using saws, chisels, planes, or marking knives; gloves reduce "
                    "tactile feedback and control"
                ),
            ],
            "supervision_required": True,
            "supervision_basis": (
                "The safety competency is itself supervised: an adult mentor walks the learner "
                "through every hazard and every piece of safety equipment in their actual shop "
                "and signs off only when the learner can name and locate each. There is no "
                "self-attestation on safety."
            ),
            "fresh_safety_signoff_within_days": None,
        },
        "tools_required": [
            {
                "name": "Fire extinguisher",
                "specification": (
                    "A:B:C rated multipurpose extinguisher within reach of the bench, inspection tag current"
                ),
                "alternatives": [],
            },
            {
                "name": "First aid kit",
                "specification": (
                    "A kit with adhesive bandages, gauze pads, medical tape, antiseptic wipes, "
                    "and tweezers; the household's choice of contents beyond this is up to the "
                    "household"
                ),
                "alternatives": [],
            },
            {
                "name": "Sealed metal can with lid for oily rags",
                "specification": "A metal can with a tight-fitting lid; or a way to lay rags flat outdoors to dry",
                "alternatives": ["A flat outdoor drying area away from combustibles"],
            },
            {
                "name": "Workbench with a holding device",
                "specification": "A flat bench with a vise, a holdfast, or bench dogs that can secure a board still",
                "alternatives": ["A saw bench with the learner's knee holding the work"],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Flat workbench at a height roughly level with the learner's relaxed wrist when standing",
            "ventilation": "Open air or normally ventilated shop; minimal for hand-tool work alone",
            "lighting": "Daylight or strong task lighting; the bench must not be in shadow",
            "power": "None required for hand-tool safety walkthrough",
            "containment": "Clear floor space around the bench; no tripping hazards",
        },
        "skill_description": (
            "The learner walks the shop with a mentor and learns where every safety element "
            "is, what every hazard looks like, and how the safe habits work. They learn the "
            "PPE rules and when each item is required; the safe carry of a sharp tool (handle "
            "led, edge controlled, edge away from self and others) and the safe pass of one "
            "(handle first); the oily-rag rule; the wrist-line rule that no body part is in the "
            "path the cutting edge will travel through if it slips; how to secure a board so it "
            "does not move under the tool; and where the fire extinguisher and first aid kit "
            "live. They learn that a sharp tool is safer than a dull one because it takes less "
            "force and gives more control."
        ),
        "demonstration_criteria": [
            "Names every PPE item on the list and explains when each is required and when each is forbidden",
            "Locates the A:B:C fire extinguisher within reach of the bench and names its rating",
            "Locates the first aid kit and names what is in it",
            (
                "Demonstrates the safe carry of a chisel: held by the handle, the cutting edge "
                "controlled, the edge angled away from the carrier's body and away from anyone "
                "else in the shop"
            ),
            "Demonstrates the safe pass of a chisel to another person: handle first, the receiver taking the handle before the giver lets go",
            "Demonstrates securing a board to the bench so it does not move when pushed by hand from any direction",
            (
                "Names and demonstrates the oily-rag rule: rags from linseed, boiled linseed, tung, "
                "or danish oil are laid flat outdoors to dry, or are stored in a sealed metal can; "
                "they are never balled up in a trash can"
            ),
            (
                "Names the wrist-line rule (no body part in the path the cutting edge will travel "
                "through if it slips) and shows it on a chisel held over a board"
            ),
            "Identifies an unfamiliar wood by stopping and asking before any cut",
            (
                "Demonstrates safe tool storage at the end of a session: chisels in their rack with "
                "edges protected, saws on their hanger or in a till, planes on their sides"
            ),
            "Names the sharp-tool-is-safer-than-dull rule and explains why",
        ],
        "common_errors": [
            {
                "error": "Carrying a chisel with the cutting edge leading or facing other people",
                "cause": "Habit of holding the chisel by the blade rather than by the handle",
                "remedy": (
                    "Always carry by the handle with the cutting edge controlled and angled "
                    "away from the body and from anyone else. When in doubt, slow down and "
                    "walk the tool the way you would walk an open knife."
                ),
            },
            {
                "error": "Leaving a sharp tool on the bench with the edge projecting over the bench edge",
                "cause": "The tool was set down in the middle of a task and the position was not checked",
                "remedy": (
                    "Always set sharp tools back from the bench edge with the cutting edge facing "
                    "away from where a hand could brush it; better, return them to their rack."
                ),
            },
            {
                "error": "Balling up an oily rag and dropping it in the trash",
                "cause": "Treating finish-soaked rags as ordinary trash",
                "remedy": (
                    "Lay the rag flat outdoors on a non-combustible surface until completely dry "
                    "and stiff, or store in a sealed metal can with water until disposed of by the "
                    "rules of the local waste service."
                ),
            },
            {
                "error": "Standing in shavings without sweeping",
                "cause": "Letting shavings accumulate underfoot during a long session",
                "remedy": "Sweep mid-session. A few minutes with a broom prevents both slips and lost tools.",
            },
            {
                "error": "Putting the off-hand in front of the chisel during a paring cut",
                "cause": "Reaching to steady the work with the hand that is downstream of the cutting edge",
                "remedy": (
                    "Both hands behind the cutting edge, or one hand on the chisel and the other "
                    "fully clear of the cut path. If the work needs steadying, the bench holds it, "
                    "not the off-hand."
                ),
            },
            {
                "error": "Skipping safety glasses at the sharpening stones",
                "cause": "Sharpening feels low-risk; the swarf is small",
                "remedy": (
                    "Swarf and stone dust travel toward the face on a forward stroke. Wear the "
                    "glasses every time the stones come out; make it habit."
                ),
            },
            {
                "error": "Letting a long sleeve or apron string drag across a sharpened plane iron on the bench",
                "cause": "The iron was set down off the plane and not noticed",
                "remedy": "Plane irons stay in the plane on the bench, or on a wooden block edge-down, never loose with the edge up.",
            },
        ],
        "artifact_expected": {
            "type": "video",
            "what_to_capture": (
                "A short walkthrough by the learner of their actual shop (under five minutes), "
                "pointing at and naming each item on the demonstration_criteria list, with the "
                "mentor offscreen or beside the learner"
            ),
            "what_the_evidence_shows": (
                "That the learner can identify, locate, and explain every safety element in the "
                "shop they will be working in, and can demonstrate the safe-carry, safe-pass, "
                "and securing habits without prompting"
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The mentor walks the learner through the shop, naming each hazard and each "
                "piece of safety equipment, demonstrating the safe carry of a chisel and the "
                "safe pass of one, securing a board to the bench, and laying out an oily rag "
                "to dry. The mentor names what is forbidden as well as what is required."
            ),
            "we_do": (
                "Mentor and learner walk the shop together. At each station the learner names "
                "the item and the mentor confirms or corrects. The learner takes a turn carrying "
                "and passing a chisel under the mentor's watch; the learner secures a board to "
                "the bench under the mentor's watch."
            ),
            "you_do_supervised": (
                "The learner walks the mentor through the shop, naming and locating each item "
                "without prompting. The mentor asks at least one follow-up question per item "
                "('why is the extinguisher in that spot?', 'what would you do if a rag fell into "
                "the trash already?'). The video is recorded at this stage."
            ),
            "you_do_unsupervised": (
                "Once signed off, the learner does the same walkthrough at the start of any "
                "session in a new or modified shop space; in any case the signoff is refreshed "
                "annually as the freshness check. There is no unsupervised work without a "
                "current ws-001 signoff."
            ),
        },
        "estimated_practice_sessions_to_signoff": 2,
        "session_length_minutes": 45,
        "signoff_validity_days": 365,
        "related_projects": [],
    },
    "wc-001": {
        "node_type": "technique",
        "trade": "woodworking",
        "competency_name": "Measure to a marked dimension with a tape measure and a pencil",
        "progression_band": "helper",
        "prerequisites": ["ws-001"],
        "safety_basis": {
            "hazards": [
                (
                    "The tape's spring return can snap the metal blade back into a finger if the "
                    "learner lets it run loose; a minor pinch, not a serious injury"
                ),
                (
                    "The end hook of a tape measure has intentional play (about 1/16 inch) to "
                    "compensate for the hook's thickness for inside vs outside measurements; a "
                    "learner who does not know this will get measurements that disagree between "
                    "pulled and pushed readings"
                ),
            ],
            "ppe_required": [
                "Shop PPE per ws-001 (closed-toe shoes, the shop's general rules); no additional PPE for measuring",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Measuring with tape and pencil involves no cutting tool. Trade-level supervision "
                "from woodworking-root still applies through the helper band, but the work itself "
                "is low-hazard and can be performed alongside a working mentor rather than under "
                "constant watch."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Tape measure",
                "specification": (
                    "12 to 25 foot tape with imperial graduations to 1/16 inch, hook end intact and not bent"
                ),
                "alternatives": [
                    "A wooden or metal rule with 1/16 inch graduations, for shorter measurements",
                ],
            },
            {
                "name": "Pencil",
                "specification": "A sharpened wood pencil (#2 or harder); a fine mechanical pencil also works",
                "alternatives": [],
            },
            {
                "name": "A verified second rule for checking",
                "specification": "A known-accurate rule the mentor keeps for verifying the learner's marks",
                "alternatives": [],
            },
        ],
        "materials_required": [
            {
                "name": "Practice stock, softwood",
                "quantity": "Three to five boards, 1x4 nominal, 12 to 24 inches long",
                "approximate_cost_usd": 8,
            },
        ],
        "workspace_requirements": {
            "surface": "Flat workbench at the learner's wrist height",
            "ventilation": "Open air or normally ventilated shop",
            "lighting": "Strong light on the tape so the small graduations are plainly visible",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner pulls the tape to the intended dimension, holding the body of the tape "
            "tight to the work and keeping the blade from twisting. They read the dimension to "
            "the nearest 1/16 inch and transfer it to the board with a short pencil tick. The "
            "tick is small and sharp, not a long line; precision matters more than visibility "
            "at this stage. The learner verifies the mark against a known-accurate rule before "
            "moving on. They learn that the hook end has play and that pulling against the hook "
            "and pushing against a stop can give slightly different readings until the technique "
            "is consistent."
        ),
        "demonstration_criteria": [
            (
                "Reads a marked dimension from a tape measure to the nearest 1/16 inch, agreeing "
                "with a verified second rule across five consecutive measurements"
            ),
            (
                "Pencil tick falls within 1/32 inch of the intended dimension, verified against "
                "the second rule across five consecutive marks"
            ),
            (
                "Tape is held tight against the work (no slack in the blade between the hook and "
                "the read point) for every measurement demonstrated"
            ),
            (
                "Hook end is engaged correctly for outside measurements (pulled tight against the "
                "edge) and the play is named when the mentor asks about it"
            ),
            "The learner can transfer the same dimension to three points along a board and have all three marks fall within 1/32 inch of each other",
        ],
        "common_errors": [
            {
                "error": "Tape blade is loose between the hook and the read point",
                "cause": "The learner is not holding the body of the tape tight to the work, or is not pulling the hook tight against the edge",
                "remedy": (
                    "Press the tape body firmly to the work. For outside measurements, give the "
                    "hook a small pull to engage it against the edge before reading."
                ),
            },
            {
                "error": "Readings disagree between two attempts on the same board",
                "cause": "Either the tape is twisting, or the hook is being treated differently between attempts (pulled one time, pushed the next)",
                "remedy": (
                    "Use the tape the same way each time. For repeated measurements, the same "
                    "edge of the board is the reference each time. For high precision, the learner "
                    "may eventually be taught to 'burn an inch' (read from the 1 inch mark instead "
                    "of the hook); that technique belongs to a later band."
                ),
            },
            {
                "error": "Reading to the nearest 1/8 instead of 1/16",
                "cause": "The 1/16 graduations are smaller and easier to skip past; the learner is reading the larger marks only",
                "remedy": (
                    "Slow down. Find the inch, then the half-inch, then the quarter, then the "
                    "eighth, then the sixteenth. Name the fraction aloud as the eye walks it down."
                ),
            },
            {
                "error": "Pencil tick is a long line rather than a precise point",
                "cause": "The pencil is dull, or the learner is making a visible mark rather than an accurate one",
                "remedy": (
                    "Keep the pencil sharp. A short tick at the exact dimension is more accurate "
                    "than a long line; when the line is needed for a cut, that line is drawn from "
                    "the tick with a square in wc-002, not from the tape."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "Three boards each marked at three points to the same dimension, with a tape "
                "measure or a verified rule laid alongside one mark of each board so the photo "
                "shows the mark against the rule"
            ),
            "what_the_evidence_shows": (
                "That each mark falls at the intended dimension to within 1/32 inch of the "
                "verified rule, and that repeated marks of the same dimension agree with each "
                "other to within 1/32 inch"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The mentor measures and marks a dimension on a board, narrating: pulling the "
                "tape tight, engaging the hook, walking the eye from inches down to sixteenths, "
                "naming the dimension aloud, and placing a sharp tick on the board. The mentor "
                "then checks the tick against a verified second rule and shows the agreement."
            ),
            "we_do": (
                "Mentor and learner alternate marks. The learner pulls and reads; the mentor "
                "watches the tape, names the reading from their side, and they compare. The "
                "mentor places a tick once, the learner places the next, and they verify both "
                "against the second rule."
            ),
            "you_do_supervised": (
                "The learner marks five dimensions on three boards. The mentor verifies each "
                "with the second rule. The learner is expected to catch their own errors before "
                "the mentor checks; the mentor's role is to confirm."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce ten consecutive accurate marks across two sessions, "
                "they may measure and mark unsupervised. The work is still inside a session a "
                "mentor is supervising at the trade level; the competency itself is unsupervised."
            ),
        },
        "estimated_practice_sessions_to_signoff": 3,
        "session_length_minutes": 20,
        "related_projects": [],
    },
    "wc-002": {
        "node_type": "technique",
        "trade": "woodworking",
        "competency_name": "Mark a line square to a reference edge with a try square and a marking knife",
        "progression_band": "helper",
        "prerequisites": ["ws-001", "wc-001"],
        "safety_basis": {
            "hazards": [
                (
                    "The marking knife is sharp and short: a slip cuts the off-hand or the hand "
                    "holding the square if it is in the knife's path"
                ),
                (
                    "The square's stock against the board: the off-hand pressing the square hard "
                    "can drag across the knife edge if the knife is lifted off the line"
                ),
                (
                    "The keep-side / waste-side convention: a line marked on the wrong side of "
                    "the intended cut wastes stock; not a hazard but a real error that compounds "
                    "in downstream work"
                ),
            ],
            "ppe_required": [
                "Shop PPE per ws-001",
                "Safety glasses optional but recommended for dry or pitchy stock at close range",
                "No gloves: the marking knife is a fine tool that requires tactile feedback",
            ],
            "supervision_required": True,
            "supervision_basis": (
                "The marking knife is the learner's first edged tool in the trade. Mentor on "
                "premises with sight of the off-hand throughout helper-band practice. Mentor "
                "steps back to apprentice-level supervision (on premises, attention divided) "
                "once the learner has demonstrated the technique on at least ten boards across "
                "at least two sessions without an off-hand-in-path moment."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Try square",
                "specification": (
                    "A try square or engineer's square of 6 to 12 inches, the stock and blade "
                    "verified square against a known reference; a combination square is an "
                    "acceptable substitute"
                ),
                "alternatives": [
                    "Combination square with the stock locked",
                    "Engineer's square (machinist's square) of 6 inches or larger",
                ],
            },
            {
                "name": "Marking knife",
                "specification": (
                    "A purpose-made marking knife with a beveled edge, or a chip-carving knife "
                    "kept sharp; a utility knife with a fresh blade is an acceptable substitute "
                    "but harder for a learner to control"
                ),
                "alternatives": [
                    "A sharpened pencil at the earliest stage; the learner moves to the knife once the technique with the square is reliable",
                ],
            },
            {
                "name": "Pencil",
                "specification": "Sharpened wood pencil for the visible line that follows the knife wall",
                "alternatives": [],
            },
            {
                "name": "A verified second square for checking",
                "specification": "A known-square reference the mentor keeps for checking the learner's marks",
                "alternatives": [],
            },
        ],
        "materials_required": [
            {
                "name": "Practice stock, softwood",
                "quantity": "Three to five boards, 1x4 nominal, 12 to 24 inches long, with one edge planed straight",
                "approximate_cost_usd": 10,
            },
        ],
        "workspace_requirements": {
            "surface": "Flat workbench with the board held still by a vise, holdfast, or hand pressure from the off-hand well clear of the knife path",
            "ventilation": "Open air or normally ventilated shop",
            "lighting": "Strong task light at a low angle so the knife wall is visible after marking",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner identifies the board's reference edge (the edge already known to be "
            "straight) and presses the stock of the try square against it. The blade extends "
            "across the board's face. The learner walks the knife along the blade with the "
            "bevel of the knife facing the waste side of the line and the flat of the knife "
            "against the square. The first pass is light, scoring the surface; the second pass "
            "deepens the line into a true knife wall. The pencil then follows the knife wall "
            "for visibility. The off-hand presses the square firmly to the reference edge and "
            "stays well clear of the knife path. The mark is on the keep side or the waste "
            "side as instructed; the convention is that the knife wall is on the keep side and "
            "the waste falls away from it."
        ),
        "demonstration_criteria": [
            (
                "The marked line is square to the reference edge within 1 degree, verified by a "
                "second known-square reference across the full width of the board"
            ),
            "The line goes fully across the board's face from edge to edge with no gaps or skips",
            (
                "The knife wall is a single continuous cut, not a series of misaligned short "
                "strokes; the pencil line follows it cleanly"
            ),
            "The line is on the keep side when the mentor specifies keep-side; on the waste side when the mentor specifies waste-side",
            "The off-hand was clear of the knife path throughout the demonstration; mentor confirms",
            (
                "The learner can produce three square lines across three boards from the same "
                "reference edge with all three lines passing the squareness check"
            ),
        ],
        "common_errors": [
            {
                "error": "Square's stock is not firmly against the reference edge",
                "cause": "The off-hand has loosened its grip on the square during the marking pass",
                "remedy": (
                    "Press the square hard with the off-hand throughout the cut. Some learners "
                    "find it helps to hook the thumb over the top of the stock and the fingers "
                    "around the underside of the board."
                ),
            },
            {
                "error": "Knife is held vertical (perpendicular to the board face) rather than with bevel toward the waste",
                "cause": "The learner is gripping the knife like a pencil and forcing it straight down",
                "remedy": (
                    "Tip the knife so the bevel faces the waste and the flat of the blade rides "
                    "against the square. The knife wall on the keep side will then be a clean "
                    "vertical face."
                ),
            },
            {
                "error": "The line is a series of short strokes that do not align",
                "cause": "The learner is lifting the knife and restarting along the way",
                "remedy": (
                    "One light pass first to establish the line, then a second pass deepening "
                    "it; the knife stays on the wood from edge to edge in each pass."
                ),
            },
            {
                "error": "Off-hand drifts in front of the knife path during the cut",
                "cause": "The learner reaches to steady the square or the board with the wrong hand",
                "remedy": (
                    "The off-hand stays on top of the square at the far end from the knife. If "
                    "the board needs more holding, secure it to the bench rather than holding it "
                    "with the off-hand at all."
                ),
            },
            {
                "error": "Line marked on the wrong side of the intended cut",
                "cause": "The keep-side / waste-side convention was not held in mind when the mark was made",
                "remedy": (
                    "Before marking, name aloud which side is keep and which is waste. Mark "
                    "the knife wall on the keep side; the cut will take the waste later."
                ),
            },
            {
                "error": "Square is referenced from the wrong edge or face of the board",
                "cause": "The reference edge was not identified and clearly named at the start",
                "remedy": (
                    "Mark the reference edge with a small triangle in pencil before any "
                    "marking begins. Every square mark on the board references from that edge."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "Three boards each marked with three square lines from the same reference edge, "
                "with a second known-square reference held against one line of each board so "
                "the photo shows the squareness"
            ),
            "what_the_evidence_shows": (
                "That each line is square to within 1 degree of the reference edge, that the "
                "line is continuous across the board, and that the keep-side / waste-side "
                "convention was held"
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The mentor marks a square line on a board, narrating: identifying the "
                "reference edge with a small triangle in pencil, placing the square stock "
                "against it, walking the knife along the blade with the bevel toward the "
                "waste, the light first pass and the deepening second pass, and finally "
                "running a pencil along the knife wall for visibility. The mentor then shows "
                "the line against a second square."
            ),
            "we_do": (
                "Mentor and learner alternate marks. The learner places the square; the mentor "
                "checks it is tight against the reference edge before the learner walks the "
                "knife. The mentor watches the off-hand throughout. After each line both "
                "verify it against the second square."
            ),
            "you_do_supervised": (
                "The learner marks three square lines across three boards from the same "
                "reference edge. Mentor watches the off-hand position, the knife angle, and "
                "the keep-side / waste-side convention. After each line, the learner verifies "
                "it against the second square and names aloud which side is keep and which is waste."
            ),
            "you_do_unsupervised": (
                "The learner is signed off for unsupervised square marking once they can "
                "produce ten consecutive square lines across at least two sessions without "
                "an off-hand-in-path moment and without a keep-side error, with the ws-001 "
                "safety signoff current within the last twelve months."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 30,
        "related_projects": [],
    },
    "wc-021": {
        "node_type": "technique",
        "trade": "woodworking",
        "competency_name": "Cross-cut to a line with a panel saw",
        "progression_band": "apprentice",
        "prerequisites": ["ws-001", "wc-001", "wc-002"],
        "safety_basis": {
            "hazards": [
                ("Sharp teeth: the saw's teeth are sharper than they look, especially a recently filed crosscut blade"),
                "Slip-into-the-finger: the saw can skip out of the kerf at the start of the cut",
                "Workpiece movement: a board not held still moves under the saw and walks the cut",
                "Eye injury from kerf dust on a dry, dusty board",
            ],
            "ppe_required": [
                "Eyes: safety glasses if the board is dry or pitchy, otherwise optional",
                "No loose sleeves or cuffs near the saw path",
                "Hair tied back if long enough to fall forward over the work",
                "No jewelry on the sawing hand",
                "No gloves: gloves reduce control of the saw and are forbidden for this technique",
            ],
            "supervision_required": True,
            "supervision_basis": (
                "Mentor on premises with sight of the cut; the mentor's role is to watch the "
                "off-hand position and the start of the kerf, the two places where a learner "
                "can hurt themselves. Mentor steps back once the learner has demonstrated "
                "start-and-finish on three boards."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Panel saw, crosscut filed",
                "specification": "20 to 26 inches long, 8 to 11 points per inch, recently sharpened",
                "alternatives": [
                    "A back saw of 14 inches or larger may substitute for stock under 4 inches wide",
                ],
            },
            {
                "name": "Bench with a vise or holdfast",
                "specification": (
                    "A flat surface that does not move under the cut, at a height where the "
                    "learner's elbow is roughly level with the cut"
                ),
                "alternatives": [
                    "A saw bench with the learner's knee holding the work",
                    "Two saw horses with a board across, the work clamped to the board",
                ],
            },
            {
                "name": "Pencil and a marking knife",
                "specification": "Marking knife sharp enough to leave a visible line in the wood; pencil for the waste-side mark",
                "alternatives": [],
            },
        ],
        "materials_required": [
            {
                "name": "Practice stock, softwood",
                "quantity": "Three to five boards, each 1x4 nominal, 12 to 24 inches long",
                "approximate_cost_usd": 8,
            },
            {
                "name": "Practice stock, hardwood (after softwood)",
                "quantity": "Two boards, each 1x4 nominal, 12 to 24 inches long",
                "approximate_cost_usd": 18,
            },
        ],
        "workspace_requirements": {
            "surface": "Flat workbench or saw bench at the learner's elbow height",
            "ventilation": "Open air or a normally ventilated shop; saw dust is minimal at hand-tool rates",
            "lighting": (
                "Daylight or strong task lighting positioned to throw a shadow on the marked "
                "line, so the line is plainly visible from the sawing side"
            ),
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner secures a board to the bench with the marked line just clear of the "
            "bench edge, the waste side of the line toward the floor or hanging off the bench. "
            "The sawing hand grips the saw with the index finger pointing down the spine of the "
            "handle. The off-hand thumb rests on the board, well away from the kerf, as a "
            "reference for the saw to start against. The first stroke is a backward pull to nick "
            "the corner of the board, beginning the kerf on the waste side of the marked line. "
            "The learner then takes long, full-length strokes with the weight of the saw doing "
            "the work, not downward pressure from the arm. The eye watches the line, not the "
            "saw. The cut is finished by easing pressure in the last inch so the offcut does "
            "not tear away from the board."
        ),
        "demonstration_criteria": [
            (
                "The kerf falls on the waste side of the marked line, no further than 1/32 inch "
                "from the line, across the full length of the cut"
            ),
            (
                "The cut face is square to the reference face of the board within roughly 1 "
                "degree, checked with a try square against the reference face"
            ),
            "The cut face is square to the edge of the board within roughly 1 degree, checked from the edge",
            "No tear-out at the exit corner: the offcut releases cleanly, not by snapping or splintering",
            "The learner can complete a crosscut on softwood in under 90 seconds for a 1x4, with relaxed shoulders",
            (
                "The learner can complete a crosscut on hardwood in under 3 minutes for a 1x4, "
                "with the same demonstration criteria as softwood"
            ),
        ],
        "common_errors": [
            {
                "error": "Kerf wanders off the line",
                "cause": "The learner is pushing down on the saw, forcing the teeth, or watching the saw instead of the line",
                "remedy": (
                    "Let the weight of the saw cut. Take longer strokes. Watch the line, not "
                    "the saw. If the kerf has already wandered, ease back to the line over the "
                    "next two strokes rather than yanking the saw back."
                ),
            },
            {
                "error": "Cut is not square to the reference face",
                "cause": "The saw is being held tilted, usually because the wrist is bent",
                "remedy": (
                    "Check the wrist is straight, the saw's plate vertical. Some learners "
                    "benefit from sighting along the saw's spine before each stroke until it "
                    "becomes habit."
                ),
            },
            {
                "error": "The saw skips out of the kerf at the start",
                "cause": "The first stroke was a push, not a pull, or the thumb-rest was not in place",
                "remedy": (
                    "Always start the cut with a backward pull stroke against the thumb-rest. "
                    "Once the kerf is established (about 1/8 inch deep), move the thumb away "
                    "and proceed with full strokes."
                ),
            },
            {
                "error": "The offcut tears away from the board at the exit",
                "cause": "The learner finished the cut with full pressure",
                "remedy": (
                    "Ease the pressure in the last inch of the cut. If supporting the offcut by "
                    "hand, do so without lifting it; let it fall straight down or to the side, "
                    "depending on grain."
                ),
            },
            {
                "error": "The board moves during the cut",
                "cause": "The board was not adequately secured, or the vise or holdfast was not tight",
                "remedy": "Re-secure before continuing. Check that the bench itself does not rack under the cut.",
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "Three completed crosscuts on three different boards, laid out flat with their "
                "mating offcuts beside them. Include a try square against one cut face and one "
                "cut edge for each board."
            ),
            "what_the_evidence_shows": (
                "The kerf placement relative to the marked line (still visible in pencil on the "
                "offcut side), the squareness checked by the try square, and the absence of "
                "exit tear-out."
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The mentor crosscuts a 1x4 in softwood, narrating each step: how the board is "
                "secured, where the off-hand thumb sits, the starting pull stroke, the long "
                "working strokes, the watching of the line, the easing at the exit. The mentor "
                "finishes by showing the cut against the try square and pointing to the side of "
                "the line the kerf fell on."
            ),
            "we_do": (
                "The mentor marks the line on a fresh board, secures it, and begins the cut "
                "with the starting pull stroke and the first three working strokes, then hands "
                "the saw to the learner without pausing the cut. The learner finishes. The "
                "mentor watches the off-hand thumb and the kerf line. The transition point is "
                "partway through the cut, not at the start: the learner is taking over an "
                "in-progress cut so they feel what the saw is already doing rather than "
                "starting cold."
            ),
            "you_do_supervised": (
                "The learner marks, secures, starts, and finishes a crosscut on softwood while "
                "the mentor watches from a position with sight of the kerf and the off-hand. "
                "The mentor intervenes only if the off-hand drifts into the saw path, if the "
                "saw is being forced, or if the board is moving. After the cut, the learner "
                "shows the result against the try square and names, out loud, which side of "
                "the line the kerf fell on. Repeat for three cuts on softwood and two cuts on "
                "hardwood across at least two separate sessions."
            ),
            "you_do_unsupervised": (
                "The learner is signed off for unsupervised crosscutting on softwood stock "
                "under 1 inch thick once the supervised demonstrations are complete, the "
                "artifact is in the portfolio, and the safety signoff (ws-001) is current "
                "within the last twelve months. Hardwood crosscutting and stock over 1 inch "
                "thick remain supervised until the journeyman band."
            ),
        },
        "estimated_practice_sessions_to_signoff": 6,
        "session_length_minutes": 30,
        "related_projects": [],
    },
}
