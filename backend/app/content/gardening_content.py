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
    "gs-001": {
        "node_type": "safety",
        "trade": "agriculture",
        "competency_name": "Garden safety: sun and heat, soil-borne hazards, hand-tool injuries, allergens and toxic plants, water hazards, and lifting",
        "progression_band": "helper",
        "prerequisites": [],
        "safety_basis": {
            "hazards": [
                (
                    "Sun and heat exposure: outdoor garden work in warm months carries real risk "
                    "of sunburn, dehydration, heat exhaustion, and heat stroke. The household "
                    "follows current CDC / NIOSH outdoor-worker heat-illness guidance for "
                    "hydration, rest in shade, and watching for early symptoms."
                ),
                (
                    "Soil-borne wounds and tetanus risk: a puncture or laceration in soil can "
                    "introduce tetanus and other soil bacteria. The household ensures every "
                    "member's tetanus immunization status is current per their healthcare "
                    "provider's recommendation; the node does not name a specific interval."
                ),
                (
                    "Sharp hand-tool injuries: pruners, hori-hori knives, sharpened trowels, "
                    "scissors, and harvest knives are all sharp enough to cut a hand. A hori-hori "
                    "in particular has both a serrated and a straight edge; both can injure."
                ),
                (
                    "Allergens and toxic plants: poison ivy, poison oak, and poison sumac cause "
                    "contact dermatitis from urushiol; other regional plants (depending on the "
                    "household's location) can also cause contact or systemic reactions. The "
                    "household uses the state cooperative extension service to learn the specific "
                    "toxic plants in their region; the node does not enumerate."
                ),
                (
                    "Stinging insects: bees, wasps, hornets, and yellow jackets nest in and around "
                    "gardens, especially in summer. For any household member with a known sting "
                    "allergy, the household's anaphylaxis-management plan governs and the mentor "
                    "knows where the epinephrine is."
                ),
                (
                    "Tick exposure (region-dependent): in many regions ticks carry Lyme disease, "
                    "Rocky Mountain spotted fever, or other vector-borne illnesses. The household "
                    "follows current CDC tick-prevention and tick-check guidance for their region."
                ),
                (
                    "Lifting strain: full bags of soil, compost, mulch, and harvest crates can "
                    "exceed a learner's safe carry weight. Bend at the knees not the back; carry "
                    "loads close to the body; ask for help with anything that does not feel light."
                ),
                (
                    "Water-borne hazards: standing water in barrels, ponds, and large containers "
                    "is a drowning hazard for young children. Rain barrels and water features are "
                    "covered or fenced per the household's safety arrangement."
                ),
                (
                    "Slips and falls: wet soil, hoses laid across paths, and uneven ground are "
                    "tripping hazards. Hoses are coiled or laid against an edge when not in use; "
                    "tools are not left on the ground in path lines."
                ),
            ],
            "ppe_required": [
                (
                    "Closed-toe shoes or boots: leather garden boots preferred; no sandals or "
                    "bare feet in the garden. A sharp tool dropped point-down is the easiest "
                    "soil-borne injury in the trade."
                ),
                (
                    "Sun-rated clothing or sunscreen: a brimmed sun hat, long sleeves rated for "
                    "sun protection, OR a broad-spectrum sunscreen at the SPF and reapplication "
                    "interval recommended by the household's healthcare provider or current CDC / "
                    "Skin Cancer Foundation public guidance. The node does not specify an SPF "
                    "number; the household chooses per their skin and the day's UV index."
                ),
                (
                    "Garden gloves: leather or coated cloth gloves are allowed AND recommended "
                    "for most garden work to reduce thorn punctures, hand abrasions, and soil "
                    "contact with broken skin. This is the opposite of the woodworking shop's "
                    "no-gloves-on-edged-tools rule because the dominant hazards differ: in the "
                    "garden the puncture and the allergen win, in the shop the loss of feel wins. "
                    "Gloves come off for fine tasks where touch is needed (handling small seed, "
                    "transplanting fragile seedlings) and the mentor names when each is correct."
                ),
                (
                    "Long pants and long sleeves for tick-active regions and seasons, per current "
                    "CDC tick-prevention guidance for the household's region."
                ),
                (
                    "Eye protection (safety glasses): required for any cutting work overhead "
                    "(small-tree pruning at apprentice band and above), for any string-trimmer "
                    "or mower work (gated separately, not in this batch), and for any work where "
                    "soil or compost is being moved in wind. Optional for low-risk ground tasks."
                ),
                (
                    "Hair tied back if long enough to fall forward when bending over a planting "
                    "row or when working with stinging or thorny plants."
                ),
            ],
            "supervision_required": True,
            "supervision_basis": (
                "The safety competency is itself supervised: an adult mentor walks the learner "
                "through every hazard in the actual garden and the actual tool shed and signs off "
                "only when the learner can name and locate each. There is no self-attestation on "
                "safety. The mentor also confirms the household's plans for tetanus status, "
                "anaphylaxis (if applicable), water-feature safety, and chemical storage in their "
                "particular situation."
            ),
            "fresh_safety_signoff_within_days": None,
        },
        "tools_required": [
            {
                "name": "First aid kit",
                "specification": (
                    "A kit that meets a recognized standard for first-aid contents: ANSI/ISEA "
                    "Z308.1 (Minimum Requirements for Workplace First Aid Kits and Supplies) or "
                    "current American Red Cross guidance for home/garden kits. The authoritative "
                    "contents list is the named standard, not this node. At minimum the kit will "
                    "contain items such as adhesive bandages, gauze pads, medical tape, antiseptic "
                    "wipes, and tweezers (the last especially for tick removal in regions where "
                    "ticks are active); the standard supplies the full list."
                ),
                "alternatives": [],
            },
            {
                "name": "Drinking water",
                "specification": (
                    "A clean drinking-water source within easy reach of the garden, refilled at the "
                    "start of every session. Quantity per session is the household's call per "
                    "current CDC outdoor-worker hydration guidance; the node does not specify a "
                    "fluid ounce target. In hot weather, the rule is drink before thirsty."
                ),
                "alternatives": [],
            },
            {
                "name": "Shade or shaded rest area",
                "specification": (
                    "A real shaded place within sight of the garden where the learner can sit out "
                    "of direct sun. A tree, a porch, a tarp on a frame, or the inside of the house "
                    "all qualify. In hot weather the learner takes scheduled breaks in shade."
                ),
                "alternatives": [],
            },
            {
                "name": "Sun hat",
                "specification": "A brimmed hat that shades the face, ears, and back of the neck",
                "alternatives": ["Long-sleeved sun-protective clothing plus sunscreen per the household's guidance"],
            },
            {
                "name": "Cell phone or way to call for help",
                "specification": (
                    "A way to reach emergency services or another adult quickly if needed; the "
                    "household's standing instructions on when to call cover sting reactions, "
                    "deep puncture wounds, heat-illness symptoms, and any injury the mentor cannot "
                    "treat at the first aid kit."
                ),
                "alternatives": [],
            },
            {
                "name": "Tetanus immunization status (household-level)",
                "specification": (
                    "Every household member working in the garden has a tetanus immunization "
                    "status current per their healthcare provider's recommendation. This is a "
                    "household precondition, not a tool the learner carries; it is checked by the "
                    "mentor before the safety signoff and re-checked annually."
                ),
                "alternatives": [],
            },
            {
                "name": "Tool shed or storage area for sharp tools",
                "specification": (
                    "Sharp tools (pruners, hori-hori, harvest knives, sharpened trowels) live in "
                    "the shed or on a designated rack out of reach of small children and never "
                    "on the ground in path lines. Each has a known home and is returned to it at "
                    "the end of the session."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Real outdoor garden with prepared and unprepared areas the mentor can walk the learner through",
            "ventilation": "Open air",
            "lighting": "Daylight; sessions scheduled to avoid peak sun where heat is a concern",
            "power": "None required for the safety walkthrough",
            "containment": "None required; gates closed if pets or small children might enter",
        },
        "skill_description": (
            "The learner walks the garden and the tool shed with a mentor and learns where every "
            "safety element is, what every hazard looks like, and how the safe habits work. They "
            "learn the PPE rules and when each item is required; the sun-and-heat habits "
            "(hat, water, shade breaks, drink before thirsty); the soil-borne wound habit (every "
            "scratch washed at the spigot before the session ends, tetanus status known to the "
            "mentor); the safe carry of a hori-hori, pruners, or harvest knife (blade closed or "
            "sheathed, edge controlled, handed handle-first); the rule that no body part is in "
            "the path the cutting edge will travel through if it slips; the regional toxic-plant "
            "rule (identify the named plants for their region per the state cooperative "
            "extension, before working bare-armed near unfamiliar leaves); the stinging-insect "
            "rule and the household's anaphylaxis plan if it applies; the tick rule for their "
            "region; the lifting rule; and where the first aid kit, the drinking water, and the "
            "phone for help live. They learn that a sharp garden tool is safer than a dull one "
            "(it takes less force, gives more control, makes a cleaner cut on the plant)."
        ),
        "demonstration_criteria": [
            "Names every PPE item on the list and explains when each is required and when each is optional",
            (
                "Locates the first aid kit and confirms it meets a recognized standard (ANSI/ISEA "
                "Z308.1 or current American Red Cross guidance), and points to the tweezers "
                "specifically if the household is in a tick-active region"
            ),
            (
                "Locates the drinking water and shade area and names the household's rule for hot-day "
                "breaks (or names that the household defers to current CDC / NIOSH outdoor-worker "
                "heat-illness guidance for the day's conditions)"
            ),
            (
                "Names the household's tetanus immunization status arrangement and confirms with the "
                "mentor that every working household member is current per their healthcare "
                "provider's recommendation"
            ),
            (
                "Demonstrates the safe carry of a hori-hori or pruners: blade closed or sheathed, "
                "edge controlled, the carrier walking with the tool angled away from their body and "
                "away from anyone else in the garden"
            ),
            (
                "Demonstrates the safe pass of a sharp garden tool to another person: handle first, "
                "the receiver taking the handle before the giver lets go"
            ),
            (
                "Names the wrist-line rule (no body part in the path the cutting edge will travel "
                "through if it slips) and shows it on a hori-hori or trowel held over a planting "
                "hole"
            ),
            (
                "Names the regional toxic plants the household has identified using the state "
                "cooperative extension service, and demonstrates the stop-and-ask rule on any "
                "unfamiliar plant before bare-armed contact"
            ),
            (
                "Names the household's anaphylaxis plan if applicable (where the epinephrine is, "
                "when to use it, when to call emergency services) per the household's healthcare "
                "provider's instructions; if no household member has a known sting allergy, names "
                "the general first-response rule for an apparent severe reaction (call emergency "
                "services)"
            ),
            (
                "Names the tick rule for the region per current CDC tick-prevention guidance "
                "(cover skin in tick season, perform a tick check after the session, use the "
                "tweezers from the first aid kit to remove a tick with steady straight pull and "
                "save the tick if illness develops); in regions where ticks are not a concern, "
                "names that no tick rule applies and the mentor confirms"
            ),
            (
                "Demonstrates safe lifting form on a real bag of soil or compost (or refuses to "
                "lift it because it is too heavy and asks for help; both are correct answers)"
            ),
            (
                "Demonstrates safe tool storage at the end of a session: sharp tools returned to "
                "their shed or rack, hoses coiled, no tools left in path lines"
            ),
            "Names the sharp-tool-is-safer-than-dull rule and explains why",
            "Demonstrates washing any scratch or cut at the spigot before the end of the session, and names when a wound exceeds first-aid-kit scope and the mentor or household healthcare contact must be called",
        ],
        "common_errors": [
            {
                "error": "Working bareheaded in the noon sun without water",
                "cause": "The learner did not check the day's conditions or skipped the hat and water at the start of the session",
                "remedy": (
                    "Every session starts with the hat, the water, and a look at the day's heat. "
                    "In hot weather the mentor schedules the work for morning or evening and "
                    "names the rest-break schedule before any tool comes out."
                ),
            },
            {
                "error": "Walking with a hori-hori or pruners in hand, blade open and exposed",
                "cause": "Habit of carrying the tool the same way it is used",
                "remedy": (
                    "Pruners close; hori-hori in its sheath or with the blade controlled and "
                    "angled away. When in doubt, slow down and walk the tool the way you would "
                    "walk an open knife."
                ),
            },
            {
                "error": "Bare hands and forearms pushing through unfamiliar leaves",
                "cause": "The learner did not stop to identify a plant before contact",
                "remedy": (
                    "Stop at any unfamiliar plant. Identify it (from the household's reference of "
                    "regional toxic plants, or by asking the mentor) before bare-armed contact. "
                    "If in doubt, work gloved or do not work this area at all."
                ),
            },
            {
                "error": "Leaving a scratch unwashed at the end of the session",
                "cause": "The scratch was small and noticed only after the work",
                "remedy": (
                    "Every scratch and cut is washed at the spigot or sink before the end of the "
                    "session. Soil-borne wound habit is one of the trade's foundations."
                ),
            },
            {
                "error": "Lifting a full bag of soil from the back rather than the legs",
                "cause": "The learner reached down with straight legs and bent at the waist",
                "remedy": (
                    "Bend at the knees, hug the bag close to the body, push up with the legs. "
                    "If the bag is too heavy to lift this way, it is too heavy to lift alone; "
                    "ask for help."
                ),
            },
            {
                "error": "Tools left on the ground across a path",
                "cause": "The learner set the tool down where they finished, not where it belongs",
                "remedy": (
                    "Tools are returned to the shed or to a designated rack at the end of the "
                    "session; mid-session, tools rest on a known surface (the wheelbarrow, the "
                    "tool tray) not in path lines."
                ),
            },
            {
                "error": "Skipping a tick check after a session in tick-active terrain",
                "cause": "Tick exposure is invisible at the time and the learner forgot",
                "remedy": (
                    "End-of-session tick check is a household habit in tick-active regions. The "
                    "mentor confirms the rule with the learner before the safety signoff; the "
                    "household sets the rule per current CDC guidance."
                ),
            },
            {
                "error": "Working near a beehive or hornet's nest without naming it first",
                "cause": "The nest was noticed and not pointed out to the mentor",
                "remedy": (
                    "Any stinging-insect nest is named to the mentor before work begins in that "
                    "area; the mentor decides whether to relocate the work, the time of day, or "
                    "the nest itself. For any household member with a known sting allergy, the "
                    "anaphylaxis plan governs."
                ),
            },
        ],
        "artifact_expected": {
            "type": "video",
            "what_to_capture": (
                "A short walkthrough by the learner of their actual garden and tool shed (under "
                "five minutes), pointing at and naming each item on the demonstration_criteria "
                "list, with the mentor offscreen or beside the learner"
            ),
            "what_the_evidence_shows": (
                "That the learner can identify, locate, and explain every safety element in the "
                "garden and shed they will be working in, and can demonstrate the safe-carry, "
                "safe-pass, lifting, and toxic-plant stop-and-ask habits without prompting"
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The mentor walks the learner through the garden and the tool shed, naming each "
                "hazard and each piece of safety equipment, demonstrating the safe carry of a "
                "hori-hori and the safe pass of pruners, modeling the hat-and-water habit before "
                "any work, the safe lift on a real bag of soil, and the end-of-session wound "
                "wash. The mentor names what is forbidden as well as what is required, and "
                "explicitly names the household's plans for tetanus, anaphylaxis (if applicable), "
                "water-feature safety, and chemical storage."
            ),
            "we_do": (
                "Mentor and learner walk the garden and shed together. At each station the "
                "learner names the item and the mentor confirms or corrects. The learner takes a "
                "turn carrying and passing a hori-hori under the mentor's watch; the learner "
                "demonstrates a safe lift on a real bag of soil; the learner washes a small "
                "(simulated) scratch at the spigot."
            ),
            "you_do_supervised": (
                "The learner walks the mentor through the garden and the shed, naming and "
                "locating each item without prompting. The mentor asks at least one follow-up "
                "question per item ('what would you do if you found a tick on your leg after "
                "this session?', 'why is the water cooler in that spot?', 'what is the rule on "
                "an unfamiliar plant?'). The video is recorded at this stage."
            ),
            "you_do_unsupervised": (
                "Once signed off, the learner does the same walkthrough at the start of any "
                "session in a new or modified garden, and after any change to PPE, tool storage, "
                "or the household's plans (tetanus, anaphylaxis, water features, chemicals). In "
                "any case the signoff is refreshed annually as the freshness check. There is no "
                "unsupervised work without a current gs-001 signoff."
            ),
        },
        "estimated_practice_sessions_to_signoff": 2,
        "session_length_minutes": 45,
        "signoff_validity_days": 365,
        "related_projects": [],
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [
                (
                    "ANSI/ISEA Z308.1 (Minimum Requirements for Workplace First Aid Kits and "
                    "Supplies). The standard itself supplies the authoritative contents list; "
                    "this node defers to it."
                ),
                (
                    "American Red Cross home/garden first-aid kit guidance as an alternate "
                    "recognized standard; the household chooses one and follows it."
                ),
                (
                    "Current CDC / NIOSH outdoor-worker heat-illness prevention guidance, "
                    "including hydration, rest in shade, and recognition of early heat-illness "
                    "symptoms. The household reads the current guidance for their conditions; "
                    "this node does not name a specific water volume or break interval."
                ),
                (
                    "Current CDC tick-prevention and tick-removal guidance for tick-active regions. "
                    "The household identifies whether their region is tick-active per the CDC's "
                    "regional information."
                ),
                (
                    "Tetanus immunization status per each household member's healthcare provider's "
                    "recommendation. This node does not write a tetanus booster interval; the "
                    "household's healthcare provider sets it per current ACIP / CDC guidance."
                ),
                (
                    "Each state's cooperative extension service for the regional list of toxic "
                    "plants (poison ivy / oak / sumac, regional toxics) and for regional pest, "
                    "disease, and soil information. The household identifies their state's "
                    "extension service and uses it as the regional safety reference."
                ),
                (
                    "Each household member with a known sting or other anaphylaxis allergy has an "
                    "individual anaphylaxis-management plan from their healthcare provider; this "
                    "node defers to that plan and to current emergency-medical guidance for "
                    "severe allergic reactions."
                ),
                (
                    "Sun-exposure protection (broad-spectrum SPF, brimmed hat, UV-rated clothing) "
                    "per current public-health guidance (CDC / Skin Cancer Foundation). The "
                    "household chooses the SPF and reapplication interval per their conditions; "
                    "this node does not specify a number."
                ),
            ],
        },
    },
    "gc-001": {
        "node_type": "technique",
        "trade": "agriculture",
        "competency_name": "Read a seed packet for spacing, depth, sun, water, days-to-maturity, and direct-sow vs. transplant",
        "progression_band": "helper",
        "prerequisites": ["gs-001"],
        "safety_basis": {
            "hazards": [
                (
                    "Misreading the depth instruction can lead to a learner planting seed too "
                    "deep (it does not germinate) or too shallow (it dries out before germination); "
                    "not a safety hazard but a real wasted-work error that compounds across a season"
                ),
                (
                    "Misreading direct-sow vs. start-indoors-and-transplant can have a learner "
                    "sowing a tomato seed outdoors in cold soil where it will rot, or starting "
                    "indoors a carrot whose taproot dislikes transplanting; not a safety hazard "
                    "but a real wasted-season error"
                ),
                (
                    "Seed treatment warnings on the packet (some commercial seed is treated with "
                    "fungicide or insecticide and is labeled with handling and disposal cautions): "
                    "the learner reads the warning and applies it. The node does not enumerate "
                    "the chemicals; the packet's label and the EPA-registered information govern."
                ),
                (
                    "Seed storage: opened seed packets stored damp or warm lose viability. Not a "
                    "safety hazard but the practice is part of the doing."
                ),
            ],
            "ppe_required": [
                "Garden PPE per gs-001 (closed-toe shoes, garden gloves if handling treated seed); no additional PPE for reading the packet itself",
            ],
            "supervision_required": False,
            "supervision_basis": (
                "Reading a packet involves no cutting tool, no body load, and no exposure. "
                "Trade-level supervision from gardening-root still applies through the helper "
                "band, but the reading itself is low-hazard and can be performed alongside a "
                "working mentor rather than under constant watch. The mentor confirms the "
                "learner's extracted numbers before any sowing happens."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "A real seed packet from the household's actual seed for the season",
                "specification": (
                    "A commercially printed seed packet from a recognized seed company, in date "
                    "(the packet's printed date is within the seed company's stated viability "
                    "window for the crop). A homemade or repackaged seed envelope is acceptable "
                    "only if it has been labeled with the same fields as a commercial packet."
                ),
                "alternatives": [
                    "A clearly written household record card carrying the same fields, if the seed "
                    "is the household's own saved seed and the record is current."
                ],
            },
            {
                "name": "A planting card or notebook",
                "specification": (
                    "A sheet of paper or a notebook page where the learner writes down each "
                    "operative number from the packet before any tool is touched. The planting "
                    "card travels with the learner to the bed and is the reference during the "
                    "actual sowing."
                ),
                "alternatives": [],
            },
            {
                "name": "Pencil or pen",
                "specification": "A real writing instrument; this is a written-record task",
                "alternatives": [],
            },
            {
                "name": "A reference of the household's last frost and first frost dates",
                "specification": (
                    "The local last-frost and first-frost dates for the household's location, from "
                    "the state cooperative extension service or another local source. These are "
                    "the dates the packet's 'start indoors X weeks before last frost' or 'direct "
                    "sow after danger of frost has passed' instructions are anchored to. The node "
                    "does not name dates; the household supplies them per their location."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [],
        "workspace_requirements": {
            "surface": "Any flat surface where the packet and the planting card can be laid out together",
            "ventilation": "Open air or indoors",
            "lighting": "Strong enough light to read fine print on the packet",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner takes a real seed packet and works through it field by field, writing "
            "each operative number onto a planting card. The fields read in order: the crop "
            "name and variety; whether the seed is to be direct-sown or started indoors; if "
            "indoors, how many weeks before the household's last frost; if direct-sown, what "
            "soil condition (after last frost, when soil reaches a stated temperature, etc.); "
            "planting depth (typically a fraction of an inch); spacing between seeds in the row "
            "and between rows; thinning instructions (sow more, thin to X inches apart); sun "
            "exposure (full sun, partial sun, shade); water needs; days to maturity (and whether "
            "DTM is counted from sowing or from transplant; for direct-sown crops this is from "
            "sowing, for transplanted crops it is from transplant out, and the packet usually "
            "says); any seed treatment warning. The planting card is then shown to the mentor "
            "for a check before any sowing or transplant happens. The learner names which "
            "fields the packet did not supply, and which the household must add from local "
            "knowledge (last frost date, first frost date, soil temperature in the row at the "
            "time of sowing)."
        ),
        "demonstration_criteria": [
            (
                "Extracts every operative field from a real packet onto a planting card: crop "
                "and variety, direct-sow vs. start-indoors, weeks-before-last-frost (if indoors) "
                "or soil condition (if direct-sow), depth, in-row spacing, between-row spacing, "
                "thinning, sun, water, days-to-maturity"
            ),
            (
                "Names which DTM counting convention applies to the crop (from sowing for direct-"
                "sown crops, from transplant for transplanted crops) and points to where the "
                "packet says so, or names that the packet did not say and the household defers to "
                "the seed company's website or the cooperative extension service"
            ),
            (
                "Names the household's last frost and first frost dates from a local source and "
                "explains how the packet's calendar instructions anchor to them"
            ),
            (
                "Names any seed treatment warning on the packet and the handling rule that follows "
                "(gloves on, no eating, packet stored away from food); if the packet has no "
                "treatment warning, names that and confirms with the mentor"
            ),
            (
                "Names the storage rule for any leftover seed: cool, dry, dark, in a labeled "
                "envelope or jar, with the open date written on the label"
            ),
            (
                "Reads three different packets for three different crops onto three planting "
                "cards correctly, with the mentor verifying each card before any sowing"
            ),
        ],
        "common_errors": [
            {
                "error": "Skipping fields the packet supplies and guessing at the bed",
                "cause": "The learner glanced at the packet and went straight to the soil",
                "remedy": (
                    "Read every field onto the card before any sowing. The card is the working "
                    "reference; the packet stays clean in the shed. The mentor verifies the card "
                    "before any sowing begins."
                ),
            },
            {
                "error": "Confusing direct-sow with start-indoors",
                "cause": "The packet's icons or wording were not clearly read",
                "remedy": (
                    "Find the words on the packet, not the icons. 'Direct sow,' 'sow outdoors,' "
                    "'after last frost,' 'sow indoors X weeks before last frost.' If unclear, the "
                    "seed company's website usually has the full instruction sheet for that variety."
                ),
            },
            {
                "error": "Reading depth in inches when the packet states a fraction",
                "cause": "The fraction was misread (1/4 inch read as 1 inch, or 1/8 inch read as 1 inch)",
                "remedy": (
                    "Slow down on fractions. Most seed plants at 1/8 to 1/2 inch deep; anything "
                    "stated in whole inches is unusual and worth a second look at the packet."
                ),
            },
            {
                "error": "Skipping the days-to-maturity counting convention",
                "cause": "The learner read DTM but did not check from-sowing vs. from-transplant",
                "remedy": (
                    "Direct-sown crops count DTM from sowing; transplanted crops count DTM from "
                    "transplant out, not from indoor start. The packet usually says; if not, the "
                    "seed company's website does. Knowing this affects when the harvest is expected."
                ),
            },
            {
                "error": "Ignoring a seed treatment warning",
                "cause": "The warning was small text near the bottom of the packet",
                "remedy": (
                    "Treated seed is labeled. The handling rule on the packet governs: gloves on, "
                    "no eating, packet stored away from food and out of reach of small children, "
                    "leftover treated seed disposed of per the packet's instructions or the local "
                    "waste service's rules."
                ),
            },
            {
                "error": "Storing the opened packet on the windowsill",
                "cause": "The packet was left where it was last used",
                "remedy": (
                    "Cool, dry, dark, sealed in a labeled envelope or jar. Sun and heat shorten "
                    "viability. Write the open date on the packet so next year's reader knows."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "Three planting cards (one per crop), each laid alongside its corresponding seed "
                "packet, with every operative field filled in on the card in the learner's "
                "handwriting"
            ),
            "what_the_evidence_shows": (
                "That the learner extracted every operative number from each packet onto the "
                "planting card, including the DTM counting convention, the seed treatment status, "
                "and the anchoring to the household's last frost date if applicable"
            ),
        },
        "mentor_signoff_required": False,
        "pedagogy": {
            "i_do": (
                "The mentor takes a real packet and reads it onto a planting card aloud, field by "
                "field, naming what is on the packet and what the household has to add from "
                "local knowledge (last frost date). The mentor explicitly names the DTM "
                "convention and any seed treatment warning. The card is then read aloud as a "
                "summary."
            ),
            "we_do": (
                "Mentor and learner alternate fields on a second packet. The learner reads a "
                "field aloud and writes it; the mentor confirms or corrects; the next field is "
                "the mentor's, then back to the learner. At the end both read the card aloud "
                "together."
            ),
            "you_do_supervised": (
                "The learner reads three real packets onto three planting cards independently. "
                "The mentor checks each card after completion. The learner names any field the "
                "packet did not supply and any field that depended on local knowledge."
            ),
            "you_do_unsupervised": (
                "Once the learner can produce three accurate planting cards across at least two "
                "sessions, they may read packets unsupervised. The mentor still verifies the "
                "card before any sowing or transplant; this is not a supervision rule, it is a "
                "double-check rule that stays in place across bands."
            ),
        },
        "estimated_practice_sessions_to_signoff": 3,
        "session_length_minutes": 20,
        "related_projects": [],
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
}
