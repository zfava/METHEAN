"""Grading scale abstraction.

Maps internal MasteryLevel strings (not_started, emerging, developing,
proficient, mastered) to external representations (letter grades, four
point GPA, percentage bands, pass/fail, competency descriptors).

The mapping is intentionally declarative so callers can supply custom
household-specific scales without code changes.
"""

from collections.abc import Sequence

DEFAULT_GRADING_SCALES: dict[str, dict[str, object]] = {
    "letter": {
        "mastered": "A",
        "proficient": "B",
        "developing": "C",
        "emerging": "D",
        "not_started": "F",
    },
    "four_point": {
        "mastered": 4.0,
        "proficient": 3.0,
        "developing": 2.0,
        "emerging": 1.0,
        "not_started": 0.0,
    },
    "percentage": {
        "mastered": "93-100%",
        "proficient": "83-92%",
        "developing": "73-82%",
        "emerging": "63-72%",
        "not_started": "0-62%",
    },
    "pass_fail": {
        "mastered": "Pass",
        "proficient": "Pass",
        "developing": "Pass",
        "emerging": "Fail",
        "not_started": "Fail",
    },
    "competency": {
        "mastered": "Exceeds Standard",
        "proficient": "Meets Standard",
        "developing": "Approaching Standard",
        "emerging": "Below Standard",
        "not_started": "Not Assessed",
    },
}


def get_grade(
    mastery_level: str,
    scale_name: str,
    custom_scales: dict | None = None,
) -> str | float:
    """Translate a mastery level through the named scale.

    Custom scales are consulted first when provided; otherwise the
    built-in DEFAULT_GRADING_SCALES table is used. If the scale is
    unknown or the mastery level is not mapped, the raw mastery level
    string is returned so callers can surface the original value rather
    than a silent blank.
    """
    scales = custom_scales if custom_scales else DEFAULT_GRADING_SCALES
    scale = scales.get(scale_name, DEFAULT_GRADING_SCALES.get(scale_name, {}))
    return scale.get(mastery_level, mastery_level)


def compute_gpa(mastery_levels: Sequence[str], credit_hours: Sequence[float]) -> float:
    """Credit-weighted GPA on the four-point scale.

    Returns 0.0 for empty inputs or when total credit hours is zero so
    the function is safe to call on in-progress transcripts. Unknown
    mastery levels contribute 0.0 points, not an exception, to match
    the forgiving behavior of get_grade.
    """
    if not mastery_levels or not credit_hours or sum(credit_hours) == 0:
        return 0.0
    four_point = DEFAULT_GRADING_SCALES["four_point"]
    total_points = sum(float(four_point.get(m, 0.0)) * c for m, c in zip(mastery_levels, credit_hours))
    return round(total_points / sum(credit_hours), 2)
