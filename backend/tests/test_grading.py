"""Tests for the grading scale abstraction layer."""

from app.services.grading import DEFAULT_GRADING_SCALES, compute_gpa, get_grade


def test_letter_grade_mastered():
    assert get_grade("mastered", "letter") == "A"


def test_letter_grade_not_started():
    assert get_grade("not_started", "letter") == "F"


def test_four_point_proficient():
    assert get_grade("proficient", "four_point") == 3.0


def test_pass_fail_developing_passes():
    assert get_grade("developing", "pass_fail") == "Pass"


def test_pass_fail_emerging_fails():
    assert get_grade("emerging", "pass_fail") == "Fail"


def test_competency_mapping():
    assert get_grade("mastered", "competency") == "Exceeds Standard"


def test_custom_scale_override():
    custom = {"custom": {"mastered": "Expert"}}
    assert get_grade("mastered", "custom", custom) == "Expert"


def test_unknown_scale_returns_raw():
    assert get_grade("mastered", "nonexistent") == "mastered"


def test_gpa_computation():
    """Credit-weighted GPA: (4.0*3 + 3.0*3 + 2.0*4) / 10 = 2.9."""
    result = compute_gpa(["mastered", "proficient", "developing"], [3.0, 3.0, 4.0])
    expected = (4.0 * 3.0 + 3.0 * 3.0 + 2.0 * 4.0) / (3.0 + 3.0 + 4.0)
    assert result == round(expected, 2)
    assert result == 2.9


def test_gpa_empty_returns_zero():
    assert compute_gpa([], []) == 0.0


def test_gpa_zero_credits_returns_zero():
    assert compute_gpa(["mastered"], [0.0]) == 0.0


def test_default_scales_cover_all_mastery_levels():
    """Every built-in scale should map every mastery level."""
    levels = {"not_started", "emerging", "developing", "proficient", "mastered"}
    for name, scale in DEFAULT_GRADING_SCALES.items():
        assert set(scale.keys()) >= levels, f"{name} missing: {levels - set(scale.keys())}"
