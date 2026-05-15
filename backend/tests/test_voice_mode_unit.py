"""Unit tests for voice-mode brevity enforcement.

Covers the sentence-boundary truncator and the render_tutor_system
voice-mode directive. The full tutor endpoint path is exercised by
test_governance integration tests; this file isolates the two
deterministic helpers so they're testable without a DB.
"""

import pytest

from app.ai.gateway import PersonalizationContext
from app.ai.prompts import render_tutor_system
from app.services.sentence_truncate import truncate_to_sentences


# ── truncate_to_sentences ──────────────────────────────────────


def test_truncate_keeps_one_sentence():
    assert truncate_to_sentences("Hello there.", max_sentences=1) == "Hello there."


def test_truncate_keeps_two_sentences_drops_third():
    text = "Try multiplying first. Then add the remainder. Tell me what you got."
    out = truncate_to_sentences(text, max_sentences=2)
    assert "Try multiplying" in out
    assert "Then add" in out
    assert "Tell me" not in out


def test_truncate_handles_abbreviation_mr_smith():
    text = "Mr. Smith said hi. He waved back."
    out = truncate_to_sentences(text, max_sentences=1)
    # "Mr." must not be treated as a sentence boundary; the whole
    # "Mr. Smith said hi." is one sentence.
    assert out == "Mr. Smith said hi."


def test_truncate_handles_question_and_exclamation():
    text = "Great! What did you try first? Can you walk me through it?"
    out = truncate_to_sentences(text, max_sentences=2)
    assert out.startswith("Great!")
    assert "first?" in out
    assert "walk me" not in out


def test_truncate_empty_input_returns_empty():
    assert truncate_to_sentences("", max_sentences=2) == ""
    assert truncate_to_sentences("   ", max_sentences=2) == ""


def test_truncate_no_terminator_returns_input():
    out = truncate_to_sentences("hello there no period here", max_sentences=2)
    assert out == "hello there no period here"


def test_truncate_zero_max_returns_empty():
    assert truncate_to_sentences("Hi.", max_sentences=0) == ""


def test_truncate_known_limitation_terminal_etc_merges_next():
    """Documented limitation: when an abbreviation appears at the end
    of a sentence the simple splitter collapses it with the next
    sentence. "etc." is the most common case; tutor prompts almost
    never produce text like this, and full-NLP sentence segmentation
    is out of scope for v2."""
    text = "Add the units, tens, etc. Then check your work. Tell me."
    out = truncate_to_sentences(text, max_sentences=1)
    # The truncator merges "etc." with the following sentence; the
    # third sentence is still correctly excluded.
    assert "etc." in out
    assert "Tell me" not in out


# ── render_tutor_system voice_mode directive ───────────────────


def test_render_tutor_system_adds_brevity_when_voice_mode():
    ctx = PersonalizationContext(companion_name="Sage")
    rendered = render_tutor_system(ctx, voice_mode=True)
    assert "voice mode" in rendered.lower()
    assert "one or two sentences" in rendered.lower()


def test_render_tutor_system_omits_brevity_when_not_voice_mode():
    ctx = PersonalizationContext(companion_name="Sage")
    rendered = render_tutor_system(ctx, voice_mode=False)
    assert "voice mode" not in rendered.lower()


def test_render_tutor_system_voice_mode_preserves_rules():
    ctx = PersonalizationContext(companion_name="Sage")
    rendered = render_tutor_system(ctx, voice_mode=True)
    # The Socratic-tutor rules must remain regardless of voice mode.
    assert "NEVER give the answer directly" in rendered
    assert "OUTPUT FORMAT" in rendered


# Marker so the file picks up at least one test even if the rendering
# module changes shape; keeps CI signal from going silent.
def test_module_loads():
    assert truncate_to_sentences is not None
    assert render_tutor_system is not None


# Skip-on-missing-pytest-asyncio guard (not needed here; everything
# is sync). Placeholder for symmetry with neighboring files.
_ = pytest
