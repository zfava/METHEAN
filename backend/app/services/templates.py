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

# Registry
TEMPLATES: dict[str, Template] = {
    t.template_id: t
    for t in [K2_FOUNDATIONS, ELEMENTARY_CORE, CLASSICAL_LOGIC]
}
