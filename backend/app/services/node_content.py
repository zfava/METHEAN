"""Node content schema and validation.

Defines the structured content JSONB schema for LearningNode.content.
This tells the AI tutor how to teach, the evaluator how to assess,
and the parent what resources to gather.
"""

# Expected structure for LearningNode.content JSONB
NODE_CONTENT_SCHEMA = {
    "learning_objectives": ["list of specific, measurable objectives"],
    "teaching_guidance": {
        "introduction": "How to introduce this concept",
        "practice_activities": ["activity types that build this skill"],
        "common_misconceptions": ["what students get wrong and how to address it"],
        "scaffolding_sequence": ["step-by-step from simple to complex"],
        "socratic_questions": ["key questions to ask rather than tell"],
        "real_world_connections": ["how this concept connects to life"],
    },
    "assessment_criteria": {
        "mastery_indicators": ["observable behaviors demonstrating mastery"],
        "proficiency_indicators": ["understanding but not fluency"],
        "developing_indicators": ["grasping with support"],
        "assessment_methods": ["oral narration", "written work", "demonstration", "project"],
        "sample_assessment_prompts": ["specific questions or tasks"],
    },
    "resource_guidance": {
        "required": ["what's needed (never brand names, always types)"],
        "recommended": ["nice to have"],
    },
    "connections": {
        "prerequisite_skills_from_other_subjects": [],
        "feeds_into": [],
        "parallel_topics": [],
    },
    # philosophy_specific holds one variant per pedagogical philosophy.
    # Each philosophy has its OWN native shape (below); the shapes are
    # intentionally different. A variant may also be a plain string,
    # which is a legacy, un-upgraded form: valid, not an error. This
    # block is the source of truth for the five native shapes. The
    # classical copywork field is optional: it is omitted for oral or
    # pre-print skills that have no authentic copywork.
    "philosophy_specific": {
        "traditional": {
            "introduction": "What the skill is and what today covers",
            "gradual_release": {
                "i_do": "Teacher models the skill explicitly",
                "we_do": "Teacher and child practice together",
                "you_do": "Child practices independently",
            },
            "guided_practice": ["practice done with support"],
            "independent_practice": ["practice done alone"],
            "mastery_check": ["observable checks the child can do the skill"],
            "spiral_review": ["earlier skills revisited to confirm retention"],
        },
        "classical": {
            "narrative_introduction": "An introduction framed as a story or idea",
            "memory_work": {
                "chants": ["sequences chanted to commit to memory"],
                "recitations": ["passages or rhymes recited from memory"],
            },
            "copywork": ["optional: text or numerals copied neatly by hand; omit for oral or pre-print skills"],
            "recitation_routine": "How prior memory work is reviewed cumulatively",
            "history_integration": "How the skill ties to the chronological spine",
            "read_aloud_suggestions": ["well-written texts to read aloud"],
        },
        "charlotte_mason": {
            "lesson_length_minutes": 0,
            "living_book_suggestions": ["beautiful, real books, never workbooks"],
            "short_lesson_flow": "The calm flow of a single short lesson",
            "narration_prompt": "A prompt inviting the child to tell back",
            "real_world_objects": ["real objects the lesson uses"],
            "nature_connection": "How the skill connects to nature study",
            "habit_focus": "The habit of mind this lesson cultivates",
        },
        "montessori": {
            "prepared_materials": ["concrete materials, ordered concrete to abstract"],
            "presentation": {
                "three_period_lesson": "Naming, recognition, recall",
                "steps": ["the ordered steps of the presentation"],
            },
            "control_of_error": "How the material reveals an error to the child",
            "abstraction_pathway": "The path from concrete material to abstraction",
            "extensions": ["further work that deepens the concept"],
            "observation_focus": "What the adult watches for instead of grading",
        },
        "unschooling": {
            "invitations": ["materials left out to invite, never assign"],
            "real_world_contexts": ["where the skill already lives in real life"],
            "conversation_starters": ["genuine questions that spark curiosity"],
            "resource_bank": ["resources kept available, not assigned"],
            "parent_role": "How the parent supports without turning it into a lesson",
            "observation_documentation": "How learning is noticed over time, not tested",
        },
    },
    "practice_items": [
        {
            "type": "problem type label",
            "difficulty": "int 1 to 3",
            "prompt": "the practice question",
            "expected_type": "number | text | multiple_choice | true_false",
            "correct_answer": "optional expected answer",
            "hints": ["optional progressive hints"],
            "explanation": "optional worked explanation",
            "options": ["optional choices for multiple_choice"],
        }
    ],
    "assessment_items": [
        {
            "prompt": "the assessment question",
            "type": "number | multiple_choice | true_false | open_response",
            "target_concept": "optional concept the item assesses",
            "rubric": "optional scoring guidance",
        }
    ],
    "media": [
        {
            "id": "stable identifier",
            "kind": "image | number_line | diagram | figure",
            "src": "optional asset URL or path",
            "alt": "required text alternative",
            "caption": "optional visible caption",
            "params": {"kind-specific, e.g. number_line": "min, max, ticks, highlight"},
        }
    ],
    "passages": [
        {
            "id": "stable identifier",
            "title": "optional passage title",
            "text": "the reading passage text",
            "level": "optional reading level label",
            "decodable_focus": ["optional phonics patterns the passage targets"],
            "questions": ["optional comprehension questions"],
        }
    ],
    "widgets": [
        {
            "id": "instance id, unique within the node",
            "widget": "widget type, e.g. counting_objects or number_line",
            "params": {"widget-specific configuration": "..."},
            "prompt": "optional instruction shown above the widget",
            "target": "optional expected value used by the widget for success feedback",
        }
    ],
    "accommodations": {
        "dyslexia": "",
        "adhd": "",
        "gifted": "",
        "visual_learner": "",
        "kinesthetic_learner": "",
        "auditory_learner": "",
    },
    "time_estimates": {
        "first_exposure": 30,
        "practice_session": 20,
        "review_session": 10,
        "estimated_sessions_to_mastery": 5,
    },
}


def is_enriched(content: dict | None) -> bool:
    """Check if a node's content has been enriched (not empty/minimal)."""
    if not content:
        return False
    return bool(content.get("learning_objectives")) and bool(content.get("teaching_guidance"))


def validate_content(content: dict) -> list[str]:
    """Return list of missing required fields."""
    issues = []
    if not content.get("learning_objectives"):
        issues.append("learning_objectives missing")
    if not content.get("teaching_guidance"):
        issues.append("teaching_guidance missing")
    if not content.get("assessment_criteria"):
        issues.append("assessment_criteria missing")
    return issues


def validate_media(content: dict) -> list[str]:
    """Return non-fatal warnings about media and passage blocks.

    This never raises and never rejects content. Legacy nodes without
    media or passages produce no warnings. Flags media blocks missing
    the required alt text, passages missing text, and duplicate media
    or passage ids.
    """
    warnings: list[str] = []

    seen_media_ids: set[str] = set()
    for i, block in enumerate(content.get("media", []) or []):
        if not block.get("alt"):
            warnings.append(f"media[{i}] missing alt text")
        block_id = block.get("id")
        if block_id is not None:
            if block_id in seen_media_ids:
                warnings.append(f"duplicate media id: {block_id}")
            seen_media_ids.add(block_id)

    seen_passage_ids: set[str] = set()
    for i, passage in enumerate(content.get("passages", []) or []):
        if not passage.get("text"):
            warnings.append(f"passage[{i}] missing text")
        passage_id = passage.get("id")
        if passage_id is not None:
            if passage_id in seen_passage_ids:
                warnings.append(f"duplicate passage id: {passage_id}")
            seen_passage_ids.add(passage_id)

    return warnings


def validate_widgets(content: dict) -> list[str]:
    """Return non-fatal warnings about interactive widget blocks.

    This never raises and never rejects content. Legacy nodes without
    widgets produce no warnings. Flags widgets missing an id or widget
    type, duplicate instance ids, and params that are present but not
    a dict. The set of widget types is intentionally open: the
    frontend widget registry is the source of truth for renderable
    types, and unknown types degrade gracefully there.
    """
    warnings: list[str] = []

    seen_ids: set[str] = set()
    for i, widget in enumerate(content.get("widgets", []) or []):
        widget_id = widget.get("id")
        if not widget_id:
            warnings.append(f"widget[{i}] missing id")
        elif widget_id in seen_ids:
            warnings.append(f"duplicate widget id: {widget_id}")
        else:
            seen_ids.add(widget_id)

        if not widget.get("widget"):
            warnings.append(f"widget[{i}] missing widget type")

        params = widget.get("params")
        if params is not None and not isinstance(params, dict):
            warnings.append(f"widget[{i}] params is not a dict")

    return warnings


# Lesson, sequence, and assessment keys that must never appear in an
# unschooling philosophy variant: their presence contradicts the
# philosophy, which has no lessons, no fixed sequence, and no tests.
_UNSCHOOLING_FORBIDDEN_KEYS: frozenset[str] = frozenset(
    {
        "gradual_release",
        "i_do",
        "we_do",
        "you_do",
        "guided_practice",
        "independent_practice",
        "mastery_check",
        "spiral_review",
        "scaffolding",
        "assessment",
        "lesson",
        "sequence",
    }
)


def validate_philosophy(content: dict) -> list[str]:
    """Return warnings and hard-fail errors for philosophy_specific.

    Mirrors validate_content and validate_media: it returns a list of
    strings and never raises. Entries prefixed "warning:" are advisory;
    entries prefixed "error:" are hard failures the authoring pipeline
    must not ship.

    - A plain-string variant is a legacy, un-upgraded form. It is
      valid, but flagged with a warning so it can be upgraded to its
      native per-philosophy shape.
    - An unschooling variant must never carry a lesson, sequence, or
      assessment key. That contradicts the philosophy, so it is a hard
      failure that protects the philosophy's integrity.

    Field completeness is not enforced here: the per-philosophy shapes
    are advisory, so an optional field (the classical copywork field,
    for example, is omitted for oral or pre-print skills) is never
    treated as missing.
    """
    issues: list[str] = []

    philosophy_specific = content.get("philosophy_specific", {})
    if not isinstance(philosophy_specific, dict):
        return issues

    for philosophy, variant in philosophy_specific.items():
        if isinstance(variant, str):
            issues.append(f"warning: philosophy_specific[{philosophy}] is a legacy string variant")
            continue
        if philosophy == "unschooling" and isinstance(variant, dict):
            forbidden = sorted(_UNSCHOOLING_FORBIDDEN_KEYS.intersection(variant.keys()))
            if forbidden:
                issues.append(
                    "error: unschooling variant must not contain lesson, sequence, or "
                    f"assessment keys (found: {', '.join(forbidden)})"
                )

    return issues
