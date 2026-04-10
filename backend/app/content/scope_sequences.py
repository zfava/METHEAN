"""Scope and sequence framework for METHEAN."""

SCOPE_SEQUENCES = {}


def get_scope_sequence(subject_id: str, level: str) -> list[dict]:
    return SCOPE_SEQUENCES.get(subject_id, {}).get(level, [])


def get_next_topics(subject_id: str, level: str, completed_refs: list[str], count: int = 5) -> list[dict]:
    scope = get_scope_sequence(subject_id, level)
    completed = set(completed_refs)
    result = []
    for topic in scope:
        if topic["ref"] in completed:
            continue
        if all(p in completed for p in topic.get("prerequisites", [])):
            result.append(topic)
            if len(result) >= count:
                break
    return result


def get_all_subject_ids() -> list[str]:
    return list(SCOPE_SEQUENCES.keys())


SCOPE_SEQUENCES["mathematics"] = {
    "foundational": [
        {
            "ref": "math_f_01",
            "title": "Counting to 20",
            "description": "Count objects to 20 with one-to-one correspondence. Recognize and write numerals 0 through 20. Count forward and backward from any number within 20.",
            "prerequisites": [],
            "estimated_weeks": 2,
            "key_concepts": ["one-to-one correspondence", "numeral recognition", "counting sequence", "cardinality"],
            "assessment_indicators": ["Counts 20 objects accurately", "Writes numerals 0-20", "Counts backward from 20"],
            "classical_alignment": "Grammar stage: memorization of number sequence",
            "charlotte_mason_alignment": "Living math: counting real objects in nature and daily life",
            "standard_alignment": "K.CC.1-5",
        },
    ],
    "developing": [],
    "intermediate": [],
    "advanced": [],
    "mastery": [],
}
