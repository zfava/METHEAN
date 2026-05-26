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
    "gc-002": {
        "node_type": "technique",
        "trade": "agriculture",
        "competency_name": "Use a trowel or hori-hori knife to dig a planting hole at correct depth and width",
        "progression_band": "helper",
        "prerequisites": ["gs-001"],
        "safety_basis": {
            "hazards": [
                (
                    "Sharp tool: a hori-hori has both a serrated edge and a straight edge; a "
                    "sharpened trowel has a sharpened front edge. A slip can cut the off-hand "
                    "or the leg if the tool path is not controlled."
                ),
                (
                    "Off-hand-in-path: the off-hand steadies the soil or the plant, and a "
                    "learner can put a finger directly under the trowel's tip on a downward "
                    "stroke if the wrist-line rule is not held"
                ),
                (
                    "Kneeling strain and knee injury on hard or stony ground: the learner is "
                    "typically kneeling for ten to thirty minutes per session; without a kneeling "
                    "pad on hard ground the knee bursa can become inflamed"
                ),
                (
                    "Back strain from bending repeatedly at the waist: leaning over to dig from "
                    "a standing position rather than kneeling can strain the lower back over a "
                    "long session"
                ),
                (
                    "Soil contact: a hand cut while digging makes immediate contact with soil "
                    "bacteria; the wound-wash and tetanus-status habits from gs-001 govern"
                ),
                (
                    "Buried hazards (root, rock, glass, or wire in old garden soil): the trowel "
                    "can strike or be deflected by a buried object; the learner stops on any "
                    "unexpected resistance and looks before pushing"
                ),
            ],
            "ppe_required": [
                "Garden PPE per gs-001 (closed-toe shoes, hat, water, sun protection)",
                "Garden gloves on for general digging; off for the moment of fine placement",
                "A kneeling pad on any ground harder than soft loam, or a low garden stool",
                "Eye protection optional but recommended when working in dry, windy conditions where soil or compost might blow into the face",
            ],
            "supervision_required": True,
            "supervision_basis": (
                "The hori-hori (or sharpened trowel) is the learner's first sharp garden tool in "
                "the trade. Mentor on premises with sight of the off-hand and the tool path "
                "throughout helper-band practice. Mentor steps back to apprentice-level "
                "supervision (on premises, attention divided) once the learner has demonstrated "
                "the technique on at least ten holes across at least two sessions without an "
                "off-hand-in-path moment and with correct kneeling form."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Hand trowel or hori-hori knife",
                "specification": (
                    "A hand trowel with a sound handle and a clean (not rusted-through) blade, OR "
                    "a hori-hori knife with a sheath. The hori-hori is the more versatile tool "
                    "but is sharper and demands more control. Either is acceptable; the mentor "
                    "chooses which the learner starts on based on the learner's age and grip."
                ),
                "alternatives": [
                    "A garden dibber for seed-depth holes that do not need width",
                ],
            },
            {
                "name": "Kneeling pad or low garden stool",
                "specification": "A foam pad or stool that lets the learner kneel or sit close to the ground without knee or back strain",
                "alternatives": [],
            },
            {
                "name": "A garden bucket or wheelbarrow for displaced soil",
                "specification": "A clean container to set excavated soil into so it can be returned to the hole around the plant",
                "alternatives": ["A clean tarp laid alongside the hole"],
            },
            {
                "name": "Soil amendment (if the planting card calls for it)",
                "specification": (
                    "Compost, aged manure, or a named soil amendment per the planting card or the "
                    "mentor's instruction. The mentor chooses the amendment per the crop and the "
                    "soil; the node does not name a specific amendment."
                ),
                "alternatives": [],
            },
            {
                "name": "A planting card from gc-001 if planting follows the digging",
                "specification": "The card carries the depth and width the hole must reach",
                "alternatives": [],
            },
        ],
        "materials_required": [
            {
                "name": "A real bed of prepared garden soil",
                "quantity": "Enough bed for ten practice holes plus a small margin",
                "approximate_cost_usd": None,
            },
        ],
        "workspace_requirements": {
            "surface": "Prepared garden soil at the learner's kneeling height, with the bed already cleared of large weeds and surface debris",
            "ventilation": "Open air",
            "lighting": "Daylight",
            "power": "None",
            "containment": "None required; the bucket or tarp catches the displaced soil",
        },
        "skill_description": (
            "The learner kneels on the pad facing the spot for the hole, with the bucket or "
            "tarp on the side of their dominant hand. They hold the trowel or hori-hori with "
            "the dominant hand and the off-hand stays away from the tool path, on the soil "
            "well behind the trowel's tip. The first stroke drives the trowel into the soil "
            "to the depth the planting card or the mentor specifies (typically two to three "
            "times the depth of the seed for a sown hole, or the height of the root ball for "
            "a transplant hole). A second and third stroke widen the hole by lifting soil out "
            "and into the bucket. The width of the hole at the bottom is at least the width "
            "of the root ball plus a small margin (typically an inch larger all around for a "
            "seedling); the hole is roughly cylindrical, not conical, so the roots have room "
            "to spread when the plant is set in. The learner checks the depth with the trowel "
            "or by holding the plant beside the hole to compare. If the planting card calls "
            "for soil amendment, a handful is mixed into the bottom of the hole and the loose "
            "soil to the side. The off-hand stays clear throughout; the trowel returns to the "
            "bucket or rests beside the hole between strokes, never on the path the learner "
            "will move through next."
        ),
        "demonstration_criteria": [
            (
                "The finished hole reaches the depth specified by the planting card or the "
                "mentor, within roughly 1/2 inch, verified by holding the trowel or the plant "
                "beside the hole"
            ),
            (
                "The finished hole is at least the width of the intended root ball plus roughly "
                "1 inch all around at the bottom; the bottom is roughly flat, not pointed"
            ),
            (
                "The displaced soil is in the bucket or on the tarp, not scattered across the "
                "bed where the next plant will go"
            ),
            ("The off-hand was clear of the trowel path throughout the demonstration; the mentor confirms"),
            "The learner is kneeling on a pad (or seated on a stool) with the back roughly straight, not bent over from a standing position",
            (
                "The trowel was set down on a known surface (the bucket, the tarp, beside the "
                "hole on the soil-tarp side) between strokes, never in the path the learner moves "
                "through"
            ),
            (
                "On any buried hazard struck during the dig (root, rock, glass, wire), the "
                "learner stopped, named the object, and asked the mentor before continuing"
            ),
            (
                "The learner can dig three holes for three different specifications (seed depth, "
                "small transplant, larger transplant) on softer ground in a single session"
            ),
        ],
        "common_errors": [
            {
                "error": "The hole is conical, narrowing at the bottom",
                "cause": "The learner pushed the trowel straight down repeatedly without lifting soil out to widen the bottom",
                "remedy": (
                    "After the first plunge, the next strokes lift soil out by rocking the trowel "
                    "back and pulling soil up and into the bucket. The bottom should be roughly "
                    "as wide as the top."
                ),
            },
            {
                "error": "The hole is shallower than the planting card specifies",
                "cause": "The learner measured by eye and stopped too soon",
                "remedy": (
                    "Hold the trowel into the hole and check the depth against the planting card "
                    "before declaring the hole done. For transplants, hold the plant in its "
                    "container beside the hole and compare; the soil level on the plant should "
                    "match the soil level at the top of the hole."
                ),
            },
            {
                "error": "Off-hand drifts in front of the trowel during a deepening stroke",
                "cause": "The learner reached to steady soil or pull a small root with the wrong hand",
                "remedy": (
                    "Off-hand stays behind the trowel's tip, on soil well clear of the path. If "
                    "soil or roots need to be moved by hand, the trowel is set down first."
                ),
            },
            {
                "error": "Bending at the waist from a standing position to dig",
                "cause": "The learner did not set up the kneeling pad and the bucket before starting",
                "remedy": (
                    "Set up the kneeling pad or stool first, the bucket on the dominant side. "
                    "Long sessions of bending at the waist hurt the back; the trade's habits "
                    "include the setup as part of the work."
                ),
            },
            {
                "error": "Striking a rock or root and forcing the trowel through",
                "cause": "The learner felt resistance and pushed harder",
                "remedy": (
                    "Stop on unexpected resistance. Look. If it is a small root, cut it cleanly "
                    "with a hori-hori, do not break it with the trowel. If it is a rock, work "
                    "around it or lever it out with the trowel's tip and the leverage of the "
                    "handle. If it is glass, wire, or anything sharp, stop and tell the mentor."
                ),
            },
            {
                "error": "Leaving the trowel in the path or on the soil where the learner will move next",
                "cause": "The trowel was set down where it was last used, not where it belongs",
                "remedy": (
                    "Trowel goes into the bucket, on the tarp, or beside the bucket between "
                    "strokes. At end of session it goes back to the shed. A trowel in a path "
                    "line is a foot puncture waiting to happen."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "Three finished planting holes side by side, with the trowel laid into one for "
                "scale, the bucket of displaced soil beside, and the kneeling pad in frame. If a "
                "planting card is in use, lay it visible beside the holes."
            ),
            "what_the_evidence_shows": (
                "That each hole reaches the specified depth and width, that the soil is "
                "contained in the bucket, and that the setup (pad, bucket, planting card) is in "
                "place"
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The mentor sets up the pad, the bucket, and the trowel, then digs one hole "
                "narrating each step: the depth and width the card calls for, the wrist-line "
                "rule, the soil into the bucket, the check of depth, the trowel set down on the "
                "bucket between strokes. The mentor finishes by setting the plant or a "
                "stand-in into the hole to show the fit."
            ),
            "we_do": (
                "Mentor and learner alternate strokes on a fresh hole. The learner takes a "
                "stroke, the mentor takes the next. The mentor watches the off-hand throughout. "
                "After each pair of strokes both check the depth and width together. The "
                "learner finishes the hole with the last few strokes alone, the mentor watching."
            ),
            "you_do_supervised": (
                "The learner digs three holes for three different specifications under the "
                "mentor's watch. The mentor's role is to watch the off-hand position, the "
                "kneeling form, and the depth-and-width check. After each hole the learner names "
                "aloud the depth and width achieved and shows it against the card."
            ),
            "you_do_unsupervised": (
                "The learner is signed off for unsupervised hole-digging on prepared garden soil "
                "for known crops once they can dig ten holes across two sessions without an "
                "off-hand-in-path moment, with the gs-001 safety signoff current within the last "
                "twelve months. The mentor is still on premises through the apprentice band. "
                "Working unsupervised on unknown ground, breaking new beds, or digging deep "
                "(over 8 inches) remains supervised through the journeyman band."
            ),
        },
        "estimated_practice_sessions_to_signoff": 4,
        "session_length_minutes": 30,
        "related_projects": [],
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
    "gc-021": {
        "node_type": "technique",
        "trade": "agriculture",
        "competency_name": "Transplant a tray of started seedlings to a prepared garden bed at correct spacing",
        "progression_band": "apprentice",
        "prerequisites": ["gs-001", "gc-001", "gc-002"],
        "safety_basis": {
            "hazards": [
                (
                    "Sharp tool: a trowel or hori-hori is in use for every hole; the hazards from "
                    "gc-002 carry forward (off-hand-in-path, slip into the leg or hand)"
                ),
                (
                    "Sun and heat exposure: transplanting is typically done at the season's "
                    "warmest moments and the learner is outdoors for an hour or more; the "
                    "sun-and-water habit from gs-001 governs"
                ),
                (
                    "Stooping and kneeling for an extended session: a tray of twelve to fifty "
                    "seedlings transplanted in one session compounds back and knee strain"
                ),
                (
                    "Damage to the seedling: rough handling of the root ball, planting at the "
                    "wrong depth for the crop, or planting on a hot afternoon when the seedling "
                    "wilts before recovering can kill a young plant. Not a safety hazard for the "
                    "learner but a real wasted-work error if the work is not done correctly."
                ),
                (
                    "Transplant shock: even correct transplanting causes some shock; the learner "
                    "learns to recognize normal shock (wilting on day one, recovering by day three) "
                    "from abnormal shock (collapse, root rot, sun scald)"
                ),
                (
                    "Soil contact in cuts: any small hand cut during the session is in immediate "
                    "contact with soil; the wound-wash and tetanus-status habits from gs-001 govern"
                ),
            ],
            "ppe_required": [
                "Garden PPE per gs-001 (closed-toe shoes, hat, water, sun protection)",
                "Garden gloves on for soil handling; OFF for the moment of root-ball release and seedling placement, where touch matters",
                "Kneeling pad or low stool",
                "Eye protection optional; recommended in dry, windy conditions",
            ],
            "supervision_required": True,
            "supervision_basis": (
                "Transplanting is the apprentice band's first multi-step technique that combines "
                "a sharp tool, a living organism, and a real bed. Mentor on premises with sight "
                "of the work for the first three transplants of each new crop. Mentor steps back "
                "to apprentice-level supervision (on premises, attention divided) once the "
                "learner has demonstrated correct depth, spacing, root-ball handling, and "
                "watering-in on three transplants of the crop. Mentor returns to direct watch "
                "for any new crop the learner has not transplanted before, because the planting "
                "depth and root-ball handling rules differ across crop families."
            ),
            "fresh_safety_signoff_within_days": 365,
        },
        "tools_required": [
            {
                "name": "Hand trowel or hori-hori knife",
                "specification": "Per gc-002; in sound condition with a sheath for the hori-hori",
                "alternatives": [],
            },
            {
                "name": "A tray of hardened-off seedlings of one or more known crops",
                "specification": (
                    "Seedlings started by the household or purchased from a nursery, hardened off "
                    "for the household's stated duration (commonly 7 to 10 days of progressive "
                    "outdoor exposure, but the exact duration is a teaching tolerance; the mentor "
                    "confirms the seedlings are ready). Each cell shows a healthy root mass when "
                    "the plug is gently lifted: pale, branching roots filling the cell without "
                    "becoming a tight spiral (root-bound)."
                ),
                "alternatives": [],
            },
            {
                "name": "A prepared garden bed",
                "specification": (
                    "A bed cleared of weeds, loosened to a depth at least equal to the planned "
                    "planting depth, raked roughly level, and at a soil temperature suitable for "
                    "the crop per the planting card or the seed company's instructions. Bed "
                    "preparation is its own competency (not authored in this first batch); the "
                    "bed is prepared by the mentor for the first transplants."
                ),
                "alternatives": [],
            },
            {
                "name": "Planting cards from gc-001 for the crops in the tray",
                "specification": "Each card carries the in-row spacing, between-row spacing, planting depth, sun, and water for its crop",
                "alternatives": [],
            },
            {
                "name": "A measuring tape or a marked stick for spacing",
                "specification": (
                    "A real tape graduated to the inch, or a stick the mentor has marked with "
                    "the household's standard spacings. Eyeballed spacing is acceptable only "
                    "after the learner has demonstrated correct measured spacing for the crop"
                ),
                "alternatives": ["A row marker or planting board with the household's standard spacings"],
            },
            {
                "name": "Watering can or hose with a gentle rose or breaker",
                "specification": (
                    "A watering can with a rose, OR a hose with a watering breaker that produces "
                    "a gentle shower, not a jet. The watering-in flow must not blast the seedling "
                    "or wash soil away from the root ball."
                ),
                "alternatives": [],
            },
            {
                "name": "Mulch (if the household's practice includes mulching after transplant)",
                "specification": (
                    "A clean straw, shredded leaf, or other named mulch per the household's "
                    "practice. The mentor chooses the mulch; the node does not name a material."
                ),
                "alternatives": [],
            },
        ],
        "materials_required": [
            {
                "name": "A tray of hardened-off seedlings",
                "quantity": "12 to 50 cells, depending on the crop and the bed",
                "approximate_cost_usd": None,
            },
            {
                "name": "Water at the bed",
                "quantity": "Enough to water in every transplant immediately after planting",
                "approximate_cost_usd": None,
            },
        ],
        "workspace_requirements": {
            "surface": "Prepared garden bed at ground level, with kneeling pad alongside",
            "ventilation": "Open air",
            "lighting": "Daylight; transplanting is best done in cool conditions (evening, morning, or an overcast day) to reduce transplant shock",
            "power": "None",
            "containment": "None required",
        },
        "skill_description": (
            "The learner lays out the planting cards and the spacing stick alongside the bed, "
            "and marks each plant's position with a small finger-press or a tick before any "
            "hole is dug. The in-row spacing comes from the card; the between-row spacing comes "
            "from the card; the layout is rectangular or a deliberate staggered pattern that "
            "the mentor names. For each transplant: the learner digs the hole to the depth and "
            "width specified for the crop (per gc-002); they lift the cell from the tray by "
            "gently squeezing the bottom of the cell with their thumb to release the plug, "
            "supporting the plant by the leaves and the root ball, not by the stem (the stem "
            "is the most easily damaged structure on a young plant); they set the plug into "
            "the hole, attending to the planting depth rule for that crop. Tomatoes and "
            "tomato-family crops are planted deeper than they grew in the cell (the stem grows "
            "roots when buried); brassicas, lettuces, and most herbs are planted at the soil "
            "line of the original cell (no deeper); alliums (onions, leeks) are planted shallow "
            "with the tip of the bulblet just at or above the soil line; the planting card or "
            "the mentor names the rule per crop. The learner backfills loose soil around the "
            "root ball, firms gently with the fingertips (not the palm, which would compact too "
            "much) to remove air pockets, and waters in immediately with a gentle flow at the "
            "base of the plant until the soil settles and water visibly pools and drains. The "
            "learner returns to the next mark and repeats. After the tray is set, the learner "
            "mulches if the household's practice includes mulching and waters once more lightly "
            "across the row."
        ),
        "demonstration_criteria": [
            (
                "Every transplant in the row is at the in-row spacing the planting card "
                "specifies, within roughly 1 inch, measured by tape or marked stick"
            ),
            ("Every row is at the between-row spacing the planting card specifies, within roughly 1 inch"),
            (
                "Every transplant is at the correct planting depth for its crop: tomato-family "
                "deeper than the cell soil line; brassicas, lettuces, and most herbs at the cell "
                "soil line; alliums shallow with the tip just at or above the soil line; the "
                "learner names which rule applies to each crop and the mentor confirms"
            ),
            (
                "Every root ball is intact at the moment of placement: the plug came out of the "
                "cell without fracturing, the roots are pale and branching, no major root mass "
                "left in the cell"
            ),
            (
                "Every transplant is held by the leaves and the root ball, never by the stem, "
                "during transfer from the cell to the hole; the mentor confirms by watching "
                "the hand position"
            ),
            (
                "Every transplant is firmed gently by fingertip, not compacted by palm; the soil "
                "around the root ball is in full contact with the root ball, no visible air gaps"
            ),
            (
                "Every transplant is watered in immediately after planting, with a gentle flow at "
                "the base, until water visibly pools and drains; the learner does not blast the "
                "seedling with a jet of water"
            ),
            ("The off-hand was clear of the trowel path throughout each hole; the mentor confirms"),
            (
                "The learner completes a row of six to twelve transplants in a single session "
                "without leaving any plant out of the soil for more than the time it takes to dig "
                "its hole (roots exposed to sun and air for prolonged periods dry out)"
            ),
            (
                "On the next session (24 to 72 hours later), the learner observes the transplants "
                "and names which look healthy (perked up, leaves firm), which are in normal "
                "transplant shock (slight wilt, recovering), and any that need attention (severe "
                "wilt, collapse, sun scald, signs of pest damage)"
            ),
        ],
        "common_errors": [
            {
                "error": "Pulling the seedling out of the cell by the stem",
                "cause": "The cell did not release easily and the learner tugged",
                "remedy": (
                    "Squeeze the bottom of the cell gently with the thumb to push the plug up; "
                    "if it still does not release, slide a thin tool around the inside edge of "
                    "the cell. The plant comes out into the hand by the root ball, not by the "
                    "stem."
                ),
            },
            {
                "error": "Planting a tomato at the cell's soil line (the same depth it grew in the tray)",
                "cause": "The learner used the general at-the-soil-line rule from brassicas or lettuces",
                "remedy": (
                    "Tomatoes and tomato-family plants (tomatoes, tomatillos, ground cherries) "
                    "are planted deeper, with one or two sets of lower leaves pinched off and the "
                    "bare stem buried. They grow roots from the buried stem. The planting card or "
                    "the mentor names this for the crop."
                ),
            },
            {
                "error": "Planting an onion or leek bulblet too deep",
                "cause": "The learner over-corrected from the tomato rule",
                "remedy": (
                    "Alliums are planted shallow with the tip of the bulblet at or just above the "
                    "soil line. The bulb forms above ground or at the surface; planting deep "
                    "produces poor bulbs."
                ),
            },
            {
                "error": "Spacing eyeballed without the stick or tape",
                "cause": "The learner skipped the layout step",
                "remedy": (
                    "Mark every plant's position with a finger-press or a tick before digging "
                    "any hole. Walk the row with the tape or the marked stick. Eyeballed "
                    "spacing is for a learner who has internalized the spacing through years of "
                    "the crop; the apprentice band still measures."
                ),
            },
            {
                "error": "Watering with a jet that washes soil away from the root ball",
                "cause": "The learner used a hose without a breaker or a watering can without a rose",
                "remedy": (
                    "Use a rose on the can or a breaker on the hose. The water flows gently at "
                    "the base of the plant; the soil settles around the root ball; the plant is "
                    "not flattened."
                ),
            },
            {
                "error": "Transplanting in the heat of a sunny midday",
                "cause": "The session was scheduled by convenience, not by the day's heat",
                "remedy": (
                    "Transplant in the evening, the early morning, or on an overcast day. The "
                    "seedling has hours of cool, shaded soil contact before it must face the "
                    "next noon. Hot-day transplanting can be done if necessary with extra water "
                    "and a temporary shade, but the cool-time rule is the default."
                ),
            },
            {
                "error": "Leaving seedlings out of the soil while digging the next hole",
                "cause": "The learner pulled out two cells at once or set a cell down to dig",
                "remedy": (
                    "One at a time: pull the cell, plant it, then move to the next. If multiple "
                    "cells are out of the tray, keep them in the shade of the tray itself with "
                    "their roots covered."
                ),
            },
            {
                "error": "Firming the soil with the palm hard enough to compact it",
                "cause": "The learner pressed down on the planted seedling to be sure it was set",
                "remedy": (
                    "Fingertips, not palm. The soil is in contact with the root ball, no air "
                    "gaps, but is not compressed into a hardpan. The watering-in finishes the "
                    "settling."
                ),
            },
            {
                "error": "Skipping the next-session check",
                "cause": "The transplants looked fine at the end of the session",
                "remedy": (
                    "Walk the row 24 to 72 hours later. Normal transplant shock (slight wilt, "
                    "recovery in two or three days) is expected; severe wilt, collapse, sun "
                    "scald, or pest damage needs attention now, not later."
                ),
            },
        ],
        "artifact_expected": {
            "type": "photo",
            "what_to_capture": (
                "Two photos: (1) the completed row immediately after watering-in, with the "
                "spacing tape or marked stick laid alongside one section of the row so the "
                "spacing is visible; (2) the same row 24 to 72 hours later, showing the "
                "transplants standing or in normal transplant shock. Include the planting card "
                "in the frame of photo 1."
            ),
            "what_the_evidence_shows": (
                "Spacing within roughly 1 inch of the card specification; correct depth for the "
                "crops planted; root balls set in firm contact with soil; the next-session check "
                "showing the row stable and recovering"
            ),
        },
        "mentor_signoff_required": True,
        "pedagogy": {
            "i_do": (
                "The mentor lays out the planting cards, the spacing stick, the tray, and the "
                "watering can. The mentor transplants the first three seedlings narrating each "
                "step: the mark, the hole per gc-002, the gentle release of the plug, the depth "
                "rule for the crop, the placement, the firming, the watering-in. The mentor "
                "explicitly names the depth rule for the crop and points to the planting card."
            ),
            "we_do": (
                "Mentor and learner alternate transplants in the next section of the row. The "
                "learner takes a transplant; the mentor watches the hand position on the plug, "
                "the depth, the firming, the watering-in. The mentor names what was correct and "
                "what could be smoother before the learner takes the next one."
            ),
            "you_do_supervised": (
                "The learner completes a row of six to twelve transplants under the mentor's "
                "watch. The mentor watches the planting depth, the root-ball handling, the "
                "spacing, and the watering-in technique. After the row, the learner names which "
                "depth rule applied to which crop and shows the spacing against the card. The "
                "next-session check (24 to 72 hours later) is also under the mentor's watch."
            ),
            "you_do_unsupervised": (
                "The learner is signed off for unsupervised transplanting of crops they have "
                "transplanted before (the depth rule for that crop is known and demonstrated) "
                "once they can complete three rows across two sessions with no off-hand-in-path "
                "moment, correct spacing within 1 inch, correct depth per crop, and a successful "
                "next-session check, with the gs-001 safety signoff current within the last "
                "twelve months. The mentor returns to direct watch for any new crop family the "
                "learner has not transplanted before; the depth rule must be demonstrated for "
                "each new crop family before unsupervised work resumes on that family."
            ),
        },
        "estimated_practice_sessions_to_signoff": 6,
        "session_length_minutes": 60,
        "related_projects": [],
        "safety_review": {
            "reviewed": False,
            "reviewer": None,
            "reviewed_on": None,
            "standard_refs": [],
        },
    },
}
