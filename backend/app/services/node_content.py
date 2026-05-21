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
        "philosophy_specific": {"philosophy id": "guidance specific to that teaching philosophy"},
    },
    "connections": {
        "prerequisite_skills_from_other_subjects": [],
        "feeds_into": [],
        "parallel_topics": [],
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
