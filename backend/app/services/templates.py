"""Starter learning map templates.

3 templates defined in code. Each is a read-only reference;
POST /v1/learning-maps/from-template/{template_id} deep-copies
into a household's map with new UUIDs.
"""

from dataclasses import dataclass, field


@dataclass
class TemplateNode:
    ref: str  # internal reference key for edge wiring
    node_type: str
    title: str
    description: str = ""
    estimated_minutes: int | None = None
    sort_order: int = 0


@dataclass
class TemplateEdge:
    from_ref: str
    to_ref: str
    relation: str = "prerequisite"


@dataclass
class Template:
    template_id: str
    name: str
    description: str
    subject_name: str
    subject_color: str
    nodes: list[TemplateNode] = field(default_factory=list)
    edges: list[TemplateEdge] = field(default_factory=list)


# ── Template 1: K-2 Foundations ──

K2_FOUNDATIONS = Template(
    template_id="k2-foundations",
    name="K-2 Foundations",
    description="Core literacy and numeracy skills for kindergarten through 2nd grade",
    subject_name="K-2 Foundations",
    subject_color="#4CAF50",
    nodes=[
        # Literacy domain
        TemplateNode("lit-root", "root", "Literacy", "Reading and writing fundamentals", sort_order=0),
        TemplateNode("letter-rec", "milestone", "Letter Recognition", "Identify all 26 letters", 30, 1),
        TemplateNode("phonics-basic", "concept", "Basic Phonics", "Letter-sound correspondence", 25, 2),
        TemplateNode("sight-words", "skill", "Sight Words", "100 most common words", 20, 3),
        TemplateNode("simple-read", "skill", "Simple Reading", "Read simple sentences", 30, 4),
        # Numeracy domain
        TemplateNode("num-root", "root", "Numeracy", "Number sense and basic math", sort_order=10),
        TemplateNode("counting", "milestone", "Counting to 100", "Count objects to 100", 20, 11),
        TemplateNode("addition", "concept", "Addition", "Single-digit addition", 25, 12),
        TemplateNode("subtraction", "concept", "Subtraction", "Single-digit subtraction", 25, 13),
        TemplateNode("word-problems", "skill", "Word Problems", "Simple story problems", 30, 14),
    ],
    edges=[
        # Literacy chain
        TemplateEdge("lit-root", "letter-rec"),
        TemplateEdge("letter-rec", "phonics-basic"),
        TemplateEdge("phonics-basic", "sight-words"),
        TemplateEdge("sight-words", "simple-read"),
        # Numeracy chain
        TemplateEdge("num-root", "counting"),
        TemplateEdge("counting", "addition"),
        TemplateEdge("counting", "subtraction"),
        TemplateEdge("addition", "word-problems"),
        TemplateEdge("subtraction", "word-problems"),
    ],
)

# ── Template 2: Elementary Core ──

ELEMENTARY_CORE = Template(
    template_id="elementary-core",
    name="Elementary Core",
    description="3rd-5th grade core curriculum: math, language arts, and science",
    subject_name="Elementary Core",
    subject_color="#2196F3",
    nodes=[
        # Math
        TemplateNode("math-root", "root", "Mathematics", "3rd-5th grade math", sort_order=0),
        TemplateNode("multiplication", "milestone", "Multiplication", "Multiplication facts and concepts", 30, 1),
        TemplateNode("division", "concept", "Division", "Division as inverse of multiplication", 30, 2),
        TemplateNode("fractions", "concept", "Fractions", "Fraction concepts and operations", 35, 3),
        TemplateNode("decimals", "skill", "Decimals", "Decimal notation and operations", 30, 4),
        # Language Arts
        TemplateNode("ela-root", "root", "Language Arts", "Reading comprehension and writing", sort_order=10),
        TemplateNode("paragraphs", "milestone", "Paragraph Writing", "Topic sentence, body, conclusion", 30, 11),
        TemplateNode("essay-intro", "concept", "Essay Structure", "Five-paragraph essay basics", 35, 12),
        TemplateNode("grammar", "skill", "Grammar & Mechanics", "Parts of speech, punctuation", 25, 13),
        # Science
        TemplateNode("sci-root", "root", "Science", "Elementary science foundations", sort_order=20),
        TemplateNode("sci-method", "milestone", "Scientific Method", "Observation, hypothesis, experiment", 30, 21),
        TemplateNode("life-sci", "concept", "Life Science", "Plants, animals, ecosystems", 35, 22),
        TemplateNode("earth-sci", "concept", "Earth Science", "Weather, rocks, water cycle", 35, 23),
    ],
    edges=[
        TemplateEdge("math-root", "multiplication"),
        TemplateEdge("multiplication", "division"),
        TemplateEdge("division", "fractions"),
        TemplateEdge("fractions", "decimals"),
        TemplateEdge("ela-root", "paragraphs"),
        TemplateEdge("paragraphs", "essay-intro"),
        TemplateEdge("paragraphs", "grammar"),
        TemplateEdge("sci-root", "sci-method"),
        TemplateEdge("sci-method", "life-sci"),
        TemplateEdge("sci-method", "earth-sci"),
    ],
)

# ── Template 3: Classical Logic ──

CLASSICAL_LOGIC = Template(
    template_id="classical-logic",
    name="Classical Logic Stage",
    description="Logic-stage curriculum (grades 5-8): formal reasoning, rhetoric foundations, and Latin roots",
    subject_name="Classical Logic",
    subject_color="#9C27B0",
    nodes=[
        # Logic
        TemplateNode("logic-root", "root", "Formal Logic", "Introduction to logical reasoning", sort_order=0),
        TemplateNode("propositions", "milestone", "Propositions", "Statements, truth values, negation", 30, 1),
        TemplateNode("syllogisms", "concept", "Syllogisms", "Major premise, minor premise, conclusion", 35, 2),
        TemplateNode("fallacies", "concept", "Logical Fallacies", "Common informal fallacies", 30, 3),
        TemplateNode("argument", "skill", "Argument Construction", "Build and evaluate arguments", 40, 4),
        # Rhetoric
        TemplateNode("rhet-root", "root", "Rhetoric Foundations", "Art of persuasion basics", sort_order=10),
        TemplateNode("ethos", "concept", "Ethos", "Credibility and character appeals", 25, 11),
        TemplateNode("pathos", "concept", "Pathos", "Emotional appeals", 25, 12),
        TemplateNode("logos", "concept", "Logos", "Logical appeals", 25, 13),
        TemplateNode("persuasive", "skill", "Persuasive Writing", "Combine appeals in writing", 40, 14),
    ],
    edges=[
        TemplateEdge("logic-root", "propositions"),
        TemplateEdge("propositions", "syllogisms"),
        TemplateEdge("syllogisms", "fallacies"),
        TemplateEdge("fallacies", "argument"),
        TemplateEdge("rhet-root", "ethos"),
        TemplateEdge("rhet-root", "pathos"),
        TemplateEdge("rhet-root", "logos"),
        TemplateEdge("ethos", "persuasive"),
        TemplateEdge("pathos", "persuasive"),
        TemplateEdge("logos", "persuasive"),
        # Cross-domain: logic strengthens rhetoric
        TemplateEdge("syllogisms", "logos"),
    ],
)


# ── Template 4: Welding Fundamentals ──

WELDING_FUNDAMENTALS = Template(
    template_id="welding-fundamentals",
    name="Welding Fundamentals",
    description="MIG, TIG, and stick welding from safety through certification prep.",
    subject_name="Welding",
    subject_color="#D84315",
    nodes=[
        TemplateNode("weld-safety", "safety", "Shop Safety & PPE", "Welding hazards, PPE, fire prevention, ventilation, burn treatment.", 60, 0),
        TemplateNode("weld-metals", "knowledge", "Metal Identification", "Mild steel, stainless, aluminum. Material properties, filler selection.", 45, 1),
        TemplateNode("weld-positions", "knowledge", "Welding Positions & Joint Types", "Flat, horizontal, vertical, overhead. Butt, lap, T-joint, corner.", 45, 2),
        TemplateNode("weld-mig-setup", "technique", "MIG Welder Setup", "Wire feed speed, voltage, gas flow. Contact tip, nozzle maintenance.", 60, 3),
        TemplateNode("weld-mig-flat", "technique", "MIG Flat Position", "Bead runs on flat plate. Travel speed, work angle, push vs drag.", 90, 4),
        TemplateNode("weld-mig-horiz", "technique", "MIG Horizontal & Vertical", "Horizontal fillet welds. Vertical up technique. Puddle control.", 90, 5),
        TemplateNode("weld-stick-setup", "technique", "Stick (SMAW) Setup", "Polarity, electrode selection (6010, 7018), arc length, amperage.", 60, 6),
        TemplateNode("weld-stick-flat", "technique", "Stick Flat Position", "Flat bead runs with 6013 and 7018. Rod angle, restart technique.", 90, 7),
        TemplateNode("weld-tig-intro", "technique", "TIG (GTAW) Introduction", "Machine setup, tungsten selection, gas cup, filler rod on mild steel.", 90, 8),
        TemplateNode("weld-inspection", "knowledge", "Weld Inspection & Testing", "Visual inspection. Undercut, porosity, lack of fusion. Bend test.", 45, 9),
        TemplateNode("weld-project1", "project", "Project: Flat Table Bracket", "Fabricate steel bracket using MIG. Cut, fit, tack, weld, grind.", 120, 10),
        TemplateNode("weld-project2", "project", "Project: Multi-Joint Weldment", "Structure with butt, lap, T-joints. Multiple positions. Inspection.", 180, 11),
        TemplateNode("weld-cert-prep", "certification_prep", "AWS Certification Prep", "AWS D1.1 code basics. Qualification test format. Practice plates.", 120, 12),
    ],
    edges=[
        TemplateEdge("weld-safety", "weld-mig-setup"), TemplateEdge("weld-safety", "weld-stick-setup"),
        TemplateEdge("weld-safety", "weld-tig-intro"), TemplateEdge("weld-metals", "weld-mig-setup"),
        TemplateEdge("weld-positions", "weld-mig-flat"), TemplateEdge("weld-mig-setup", "weld-mig-flat"),
        TemplateEdge("weld-mig-flat", "weld-mig-horiz"), TemplateEdge("weld-stick-setup", "weld-stick-flat"),
        TemplateEdge("weld-mig-horiz", "weld-project1"), TemplateEdge("weld-stick-flat", "weld-project2"),
        TemplateEdge("weld-tig-intro", "weld-project2"), TemplateEdge("weld-inspection", "weld-cert-prep"),
        TemplateEdge("weld-project2", "weld-cert-prep"),
    ],
)


# ── Template 5: Electrical Fundamentals ──

ELECTRICAL_FUNDAMENTALS = Template(
    template_id="electrical-fundamentals",
    name="Electrical Fundamentals",
    description="Residential electrical from Ohm's law through circuit installation.",
    subject_name="Electrical",
    subject_color="#FFA000",
    nodes=[
        TemplateNode("elec-safety", "safety", "Electrical Safety & Lockout/Tagout", "Shock hazards, GFCI, lockout/tagout, meter safety, arc flash.", 60, 0),
        TemplateNode("elec-ohms", "knowledge", "Ohm's Law & Basic Circuits", "Voltage, current, resistance. Series and parallel. P=IV.", 45, 1),
        TemplateNode("elec-tools", "technique", "Meter Usage & Wire Skills", "Multimeter operation. Wire stripping, termination, splicing.", 60, 2),
        TemplateNode("elec-nec", "knowledge", "NEC Code Basics", "Wire sizing (AWG), breaker ratings, box fill, grounding.", 60, 3),
        TemplateNode("elec-outlets", "technique", "Outlet & Switch Installation", "Single-pole, 3-way switch, duplex outlet, GFCI outlet.", 90, 4),
        TemplateNode("elec-circuits", "technique", "Residential Circuit Design", "Branch circuit layout, load calculation, panel scheduling.", 90, 5),
        TemplateNode("elec-rough", "technique", "Rough-In Wiring", "Running Romex, drilling studs, securing cable, box mounting.", 120, 6),
        TemplateNode("elec-project1", "project", "Project: Wire a Room", "Complete rough-in and finish for a bedroom. Inspect and test.", 180, 7),
        TemplateNode("elec-240v", "knowledge", "240V Circuits & Subpanels", "Double-pole breakers, 10/3 wire, dryer/range connections.", 60, 8),
        TemplateNode("elec-project2", "project", "Project: Subpanel Installation", "Install subpanel in garage. Run feeder, land circuits, test.", 180, 9),
        TemplateNode("elec-cert", "certification_prep", "Journeyman Exam Prep", "NEC code review, practice calculations, sample exam questions.", 120, 10),
    ],
    edges=[
        TemplateEdge("elec-safety", "elec-tools"), TemplateEdge("elec-safety", "elec-outlets"),
        TemplateEdge("elec-safety", "elec-rough"), TemplateEdge("elec-ohms", "elec-tools"),
        TemplateEdge("elec-ohms", "elec-nec"), TemplateEdge("elec-nec", "elec-circuits"),
        TemplateEdge("elec-tools", "elec-outlets"), TemplateEdge("elec-outlets", "elec-rough"),
        TemplateEdge("elec-circuits", "elec-rough"), TemplateEdge("elec-rough", "elec-project1"),
        TemplateEdge("elec-nec", "elec-240v"), TemplateEdge("elec-240v", "elec-project2"),
        TemplateEdge("elec-project1", "elec-project2"), TemplateEdge("elec-project2", "elec-cert"),
    ],
)


# ── Template 6: Automotive Fundamentals ──

AUTOMOTIVE_FUNDAMENTALS = Template(
    template_id="automotive-fundamentals",
    name="Automotive Fundamentals",
    description="Vehicle systems from basic maintenance through diagnostics.",
    subject_name="Automotive",
    subject_color="#37474F",
    nodes=[
        TemplateNode("auto-safety", "safety", "Shop Safety & Tool ID", "Jack stand safety, chemical handling, fire extinguisher, eye protection.", 45, 0),
        TemplateNode("auto-systems", "knowledge", "Vehicle Systems Overview", "Engine, transmission, brakes, suspension, electrical, cooling.", 60, 1),
        TemplateNode("auto-oil", "technique", "Oil Change & Fluid Checks", "Oil drain, filter replacement, fluid level checks.", 45, 2),
        TemplateNode("auto-tires", "technique", "Tires, Rotation & Brake Inspection", "Tire pressure, tread depth, rotation, visual brake inspection.", 60, 3),
        TemplateNode("auto-brakes", "technique", "Brake Pad & Rotor Replacement", "Caliper removal, pad replacement, rotor inspection, bleeding.", 120, 4),
        TemplateNode("auto-electrical", "knowledge", "Automotive Electrical Basics", "Battery testing, charging system, starting circuit, fuse diagnosis.", 60, 5),
        TemplateNode("auto-obd", "technique", "OBD-II Diagnostics", "Scanner operation, DTC reading, freeze frame, live data.", 60, 6),
        TemplateNode("auto-engine", "knowledge", "Engine Fundamentals", "Four-stroke cycle, timing, compression, fuel delivery, ignition.", 90, 7),
        TemplateNode("auto-project1", "project", "Project: Full Brake Service", "Complete front and rear: pads, rotors, calipers, bleeding, test.", 180, 8),
        TemplateNode("auto-project2", "project", "Project: Diagnose & Fix", "Use OBD-II and manual diagnostics to find and repair a real issue.", 240, 9),
        TemplateNode("auto-cert", "certification_prep", "ASE Student Certification Prep", "ASE A-series practice tests. Study guide review.", 120, 10),
    ],
    edges=[
        TemplateEdge("auto-safety", "auto-oil"), TemplateEdge("auto-safety", "auto-tires"),
        TemplateEdge("auto-safety", "auto-brakes"), TemplateEdge("auto-systems", "auto-electrical"),
        TemplateEdge("auto-systems", "auto-engine"), TemplateEdge("auto-oil", "auto-tires"),
        TemplateEdge("auto-tires", "auto-brakes"), TemplateEdge("auto-electrical", "auto-obd"),
        TemplateEdge("auto-brakes", "auto-project1"), TemplateEdge("auto-obd", "auto-project2"),
        TemplateEdge("auto-engine", "auto-project2"), TemplateEdge("auto-project1", "auto-cert"),
        TemplateEdge("auto-project2", "auto-cert"),
    ],
)


# ── Template 7: Woodworking Fundamentals ──

WOODWORKING_FUNDAMENTALS = Template(
    template_id="woodworking-fundamentals",
    name="Woodworking Fundamentals",
    description="Hand and power tool skills from basic joinery through furniture.",
    subject_name="Woodworking",
    subject_color="#5D4037",
    nodes=[
        TemplateNode("wood-safety", "safety", "Shop Safety & Hand Tool ID", "Tool safety, sharp tool handling, dust protection, clamp usage.", 45, 0),
        TemplateNode("wood-measure", "technique", "Measuring, Marking & Layout", "Tape measure, combination square, marking gauge, knife lines.", 45, 1),
        TemplateNode("wood-handsaw", "technique", "Hand Sawing", "Crosscut, rip cut, coping saw. Saw selection, sharpening basics.", 60, 2),
        TemplateNode("wood-planes", "technique", "Planes & Chisels", "Block plane, smoothing plane, chisel technique. Water stones.", 60, 3),
        TemplateNode("wood-joinery1", "technique", "Basic Joinery: Butt, Dado, Rabbet", "Butt joint, dado with router/saw, rabbet joint.", 90, 4),
        TemplateNode("wood-power", "safety", "Power Tool Safety", "Circular saw, drill press, router, sander. Guards, push sticks.", 60, 5),
        TemplateNode("wood-joinery2", "technique", "Intermediate Joinery: M&T, Dovetail", "Hand-cut mortise and tenon. Half-blind dovetails.", 120, 6),
        TemplateNode("wood-finishing", "technique", "Finishing: Sand, Stain, Seal", "Sanding progression, stain application, polyurethane/oil finish.", 60, 7),
        TemplateNode("wood-project1", "project", "Project: Cutting Board", "Edge-grain cutting board. Ripping, gluing, planing, food-safe finish.", 120, 8),
        TemplateNode("wood-project2", "project", "Project: Small Table or Shelf", "Design, cut list, joinery, assembly, finishing.", 240, 9),
        TemplateNode("wood-project3", "project", "Project: Furniture Piece", "Bookshelf, workbench, or cabinet. Complex joinery, hardware.", 360, 10),
    ],
    edges=[
        TemplateEdge("wood-safety", "wood-measure"), TemplateEdge("wood-safety", "wood-handsaw"),
        TemplateEdge("wood-safety", "wood-planes"), TemplateEdge("wood-measure", "wood-joinery1"),
        TemplateEdge("wood-handsaw", "wood-joinery1"), TemplateEdge("wood-planes", "wood-joinery1"),
        TemplateEdge("wood-safety", "wood-power"), TemplateEdge("wood-power", "wood-joinery2"),
        TemplateEdge("wood-joinery1", "wood-joinery2"), TemplateEdge("wood-joinery1", "wood-finishing"),
        TemplateEdge("wood-joinery1", "wood-project1"), TemplateEdge("wood-finishing", "wood-project1"),
        TemplateEdge("wood-joinery2", "wood-project2"), TemplateEdge("wood-project1", "wood-project2"),
        TemplateEdge("wood-project2", "wood-project3"),
    ],
)


# Registry
TEMPLATES: dict[str, Template] = {
    t.template_id: t
    for t in [
        K2_FOUNDATIONS, ELEMENTARY_CORE, CLASSICAL_LOGIC,
        WELDING_FUNDAMENTALS, ELECTRICAL_FUNDAMENTALS,
        AUTOMOTIVE_FUNDAMENTALS, WOODWORKING_FUNDAMENTALS,
    ]
}
