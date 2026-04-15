"""Tests for email service and templates."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.email_templates import (
    compliance_warning_email,
    daily_summary_email,
    governance_alert_email,
    mastery_milestone_email,
    weekly_digest_email,
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
        daily_summary_email(
            "Parent", [{"name": "Emma", "activity_count": 5, "total_minutes": 120}], 2, "Monday, Jan 1"
        ),
        mastery_milestone_email("Parent", "Emma", "Long Division", "Math", "mastered"),
        governance_alert_email("Parent", "Assessment", "Content Filter", "Contains filtered topic"),
        weekly_digest_email(
            "Parent",
            {"activities_completed": 20, "nodes_mastered": 5, "total_minutes": 600},
            {"approved": 15, "rejected": 2},
        ),
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


def test_welcome_email_template():
    """Welcome email contains name and getting started steps."""
    from app.services.email_templates import welcome_email

    html = welcome_email("Zack")
    assert "Zack" in html
    assert "METHEAN" in html
    assert "philosophy" in html.lower()
    assert "<html" in html.lower()


def test_password_reset_email_template():
    """Password reset email contains the reset link."""
    from app.services.email_templates import password_reset_email

    url = "https://methean.app/auth/reset?token=abc123"
    html = password_reset_email(url)
    assert url in html
    assert "expires" in html.lower()
    assert "METHEAN" in html


@pytest.mark.asyncio
@patch("app.services.email.settings")
@patch("app.services.email.httpx.AsyncClient")
async def test_send_email_handles_api_error(mock_client_cls, mock_settings):
    """Email returns False on Resend API error, doesn't crash."""
    mock_settings.RESEND_API_KEY = "test-key"
    mock_settings.EMAIL_FROM = "METHEAN <test@methean.app>"

    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client_cls.return_value = mock_client

    from app.services.email import send_email

    result = await send_email("bad@test.com", "Subject", "<p>Body</p>")
    assert result is False


@pytest.mark.asyncio
@patch("app.services.email.settings")
@patch("app.services.email.httpx.AsyncClient")
async def test_send_email_handles_timeout(mock_client_cls, mock_settings):
    """Email returns False on timeout, doesn't crash."""
    import httpx as real_httpx

    mock_settings.RESEND_API_KEY = "test-key"
    mock_settings.EMAIL_FROM = "METHEAN <test@methean.app>"

    mock_client = AsyncMock()
    mock_client.post.side_effect = real_httpx.TimeoutException("timeout")
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client_cls.return_value = mock_client

    from app.services.email import send_email

    result = await send_email("timeout@test.com", "Subject", "<p>Body</p>")
    assert result is False
