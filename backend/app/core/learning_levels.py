"""Learning level definitions and subject catalog for METHEAN.

Five learning levels replace grade bands. They are per-subject, per-child, parent-defined.
A child can be 'advanced' in math and 'foundational' in Latin simultaneously.
"""

LEARNING_LEVELS = {
    "foundational": {
        "label": "Foundational",
        "description": "Building core concepts. No prerequisites assumed.",
        "ai_instruction": "Introduce concepts from scratch. Use concrete examples, manipulatives, sensory engagement. Short lessons (10-20 min). Heavy repetition. Celebrate small wins.",
        "sort_order": 1,
    },
    "developing": {
        "label": "Developing",
        "description": "Working through fundamentals. Some foundation in place.",
        "ai_instruction": "Build on existing knowledge. Introduce connections between concepts. Lessons 15-30 min. Begin requiring independent practice. Scaffold toward autonomy.",
        "sort_order": 2,
    },
    "intermediate": {
        "label": "Intermediate",
        "description": "Solid foundation. Ready for deeper exploration.",
        "ai_instruction": "Challenge with multi-step problems and cross-subject connections. Lessons 25-45 min. Expect independent work. Introduce primary sources and real-world applications.",
        "sort_order": 3,
    },
    "advanced": {
        "label": "Advanced",
        "description": "Strong mastery of fundamentals. Ready for complex work.",
        "ai_instruction": "Push toward original thinking, analysis, synthesis. Lessons 30-60 min. Seminar-style discussion. Research projects. Self-directed study with guidance.",
        "sort_order": 4,
    },
    "mastery": {
        "label": "Mastery",
        "description": "Deep expertise. Self-directed, teaching others, original work.",
        "ai_instruction": "Facilitate independent research and creation. The student leads; you advise. Support thesis-level work, mentorship, portfolio development.",
        "sort_order": 5,
    },
}

VALID_LEVELS = set(LEARNING_LEVELS.keys())

SUBJECT_CATALOG = {
    "academic": [
        {"id": "phonics_reading", "name": "Phonics & Reading", "description": "Letter sounds through reading fluency", "category": "language"},
        {"id": "literature", "name": "Literature", "description": "Classic literature, great books, mythology", "category": "language"},
        {"id": "writing_grammar", "name": "Writing & Grammar", "description": "Composition, grammar, rhetoric", "category": "language"},
        {"id": "mathematics", "name": "Mathematics", "description": "Number sense through advanced mathematics", "category": "stem"},
        {"id": "science", "name": "Science", "description": "Natural sciences, experiments, scientific method", "category": "stem"},
        {"id": "history", "name": "History", "description": "Ancient through modern, primary sources", "category": "humanities"},
        {"id": "latin", "name": "Latin", "description": "Grammar, vocabulary, translation", "category": "language"},
        {"id": "logic", "name": "Logic", "description": "Formal logic, syllogisms, critical thinking", "category": "humanities"},
        {"id": "nature_study", "name": "Nature Study", "description": "Observation, journaling, ecology", "category": "stem"},
        {"id": "music_art", "name": "Music & Art", "description": "Music theory, instruments, visual arts", "category": "arts"},
        {"id": "geography", "name": "Geography", "description": "Physical and human geography", "category": "humanities"},
        {"id": "foreign_language", "name": "Foreign Language", "description": "Modern language study", "category": "language"},
        {"id": "bible_theology", "name": "Bible & Theology", "description": "Scripture study, doctrine, church history", "category": "humanities"},
        {"id": "health_pe", "name": "Health & PE", "description": "Physical education, health, nutrition", "category": "life"},
        {"id": "computer_science", "name": "Computer Science", "description": "Programming, computational thinking", "category": "stem"},
        {"id": "rhetoric", "name": "Rhetoric & Composition", "description": "Persuasive writing, public speaking", "category": "language"},
        {"id": "government_economics", "name": "Government & Economics", "description": "Civics, political science, finance", "category": "humanities"},
    ],
    "vocational": [
        {"id": "woodworking", "name": "Woodworking", "description": "Hand tools, joinery, furniture construction", "category": "trades"},
        {"id": "electrical", "name": "Electrical Fundamentals", "description": "Circuits, wiring, NEC code basics", "category": "trades"},
        {"id": "welding", "name": "Welding", "description": "MIG, TIG, stick welding fundamentals", "category": "trades"},
        {"id": "automotive", "name": "Automotive", "description": "Engine systems, diagnostics, maintenance", "category": "trades"},
        {"id": "plumbing", "name": "Plumbing", "description": "Pipe fitting, fixtures, water systems", "category": "trades"},
        {"id": "hvac", "name": "HVAC", "description": "Heating, ventilation, air conditioning", "category": "trades"},
        {"id": "cooking_nutrition", "name": "Cooking & Nutrition", "description": "Culinary arts, meal planning, food safety", "category": "life"},
        {"id": "agriculture", "name": "Agriculture", "description": "Animal husbandry, crop management, soil science", "category": "life"},
        {"id": "sewing_textiles", "name": "Sewing & Textiles", "description": "Pattern reading, machine operation", "category": "life"},
        {"id": "small_engine", "name": "Small Engine Repair", "description": "Lawn equipment, generators, motors", "category": "trades"},
        {"id": "construction", "name": "Construction", "description": "Framing, roofing, drywall, finishing", "category": "trades"},
        {"id": "first_aid", "name": "First Aid / EMT", "description": "Emergency medicine, CPR, trauma response", "category": "life"},
        {"id": "entrepreneurship", "name": "Entrepreneurship", "description": "Business planning, accounting, marketing", "category": "life"},
    ],
}


def get_all_subjects(household_settings=None):
    """Return the complete subject catalog including household custom subjects."""
    result = []
    for category in SUBJECT_CATALOG.values():
        result.extend(category)
    if household_settings:
        result.extend(household_settings.get("custom_subjects", []))
    return result


def get_level_for_subject(preferences, subject_name):
    """Get a child's learning level for a subject. Default: developing."""
    if not preferences or not getattr(preferences, "subject_levels", None):
        return "developing"
    levels = preferences.subject_levels or {}
    key = subject_name.lower().replace(" ", "_").replace("&", "and")
    if key in levels:
        return levels[key]
    for k, v in levels.items():
        if k.lower() in subject_name.lower() or subject_name.lower() in k.lower():
            return v
    return "developing"


def get_daily_minutes_for_child(child, calendar=None):
    """Daily target: child preference > calendar default > 120."""
    if hasattr(child, "preferences") and child.preferences and child.preferences.daily_duration_minutes:
        return child.preferences.daily_duration_minutes
    if calendar:
        return calendar.get("daily_target_minutes", {}).get("default", 120)
    return 120


def build_level_context(preferences, subjects):
    """Build a learning level summary for AI prompts."""
    lines = []
    for subj in subjects:
        name = subj if isinstance(subj, str) else subj.get("name", "")
        level = get_level_for_subject(preferences, name)
        level_info = LEARNING_LEVELS.get(level, LEARNING_LEVELS["developing"])
        lines.append(f"- {name}: {level_info['label']} — {level_info['ai_instruction']}")
    return "\n".join(lines)
