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
        "philosophy_specific": {},
    },

    "connections": {
        "prerequisite_skills_from_other_subjects": [],
        "feeds_into": [],
        "parallel_topics": [],
    },

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
