"""Tests for email service and templates."""

from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from app.services.email_templates import (
    daily_summary_email,
    mastery_milestone_email,
    governance_alert_email,
    weekly_digest_email,
    compliance_warning_email,
)


@pytest.mark.asyncio
@patch("app.services.email.settings")
async def test_send_email_no_api_key(mock_settings):
    """No API key returns False gracefully."""
    mock_settings.RESEND_API_KEY = ""
    from app.services.email import send_email
    result = await send_email("test@test.com", "Subject", "<p>Body</p>")
    assert result is False


@pytest.mark.asyncio
@patch("app.services.email.settings")
@patch("app.services.email.httpx.AsyncClient")
async def test_send_email_success(mock_client_cls, mock_settings):
    """Successful email sends correct payload to Resend."""
    mock_settings.RESEND_API_KEY = "test-key"
    mock_settings.EMAIL_FROM = "METHEAN <test@methean.app>"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client_cls.return_value = mock_client

    from app.services.email import send_email
    result = await send_email("recipient@test.com", "Test Subject", "<p>Hello</p>")
    assert result is True
    mock_client.post.assert_called_once()
    call_args = mock_client.post.call_args
    assert call_args[1]["json"]["to"] == ["recipient@test.com"]
    assert call_args[1]["json"]["subject"] == "Test Subject"


def test_email_templates_return_html():
    """All templates return valid HTML strings."""
    templates = [
        daily_summary_email("Parent", [{"name": "Emma", "activity_count": 5, "total_minutes": 120}], 2, "Monday, Jan 1"),
        mastery_milestone_email("Parent", "Emma", "Long Division", "Math", "mastered"),
        governance_alert_email("Parent", "Assessment", "Content Filter", "Contains filtered topic"),
        weekly_digest_email("Parent", {"activities_completed": 20, "nodes_mastered": 5, "total_minutes": 600}, {"approved": 15, "rejected": 2}),
        compliance_warning_email("Parent", "Emma", "NY", "Below required instruction hours"),
    ]
    for html in templates:
        assert isinstance(html, str)
        assert "<html" in html.lower()
        assert "</html>" in html.lower()


def test_email_templates_include_brand():
    """All templates include METHEAN branding."""
    html = daily_summary_email("Test", [], 0, "Today")
    assert "METHEAN" in html

    html = mastery_milestone_email("Test", "Emma", "Fractions", "Math", "mastered")
    assert "METHEAN" in html

    html = weekly_digest_email("Test", {}, {})
    assert "METHEAN" in html
