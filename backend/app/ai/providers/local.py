"""Local inference provider (OpenAI-compatible endpoint).

This is the first step toward independence from external AI vendors: a
provider that runs an open-weight model on the family's own hardware
through an OpenAI-compatible local server (Ollama by default, but any
OpenAI-compatible endpoint works). It slots into the gateway chain
behind the exact same contract the built-in Claude and OpenAI calls
use, so governance, role checks, and cost controls apply unchanged. A
local response is indistinguishable downstream from a Claude response
except in its provenance metadata.

Contract (mirrors ``app.ai.gateway._call_claude`` / ``_call_openai``):

    async def call_local(system_prompt, user_prompt, max_tokens, ...)
        -> {"content": str, "model": str,
            "input_tokens": int, "output_tokens": int}

On any transport, timeout, HTTP, or parse failure ``call_local`` raises
``LocalProviderError`` (a plain Exception). The gateway loop catches it
like any other provider error and falls through to the next configured
provider (which may be the deterministic native floor), so the request
never hangs and never escapes as an unhandled error. We use httpx
directly (already a dependency) rather than pulling in the ollama or
openai SDKs.
"""

import time

import httpx
import structlog

from app.core.config import settings

slog = structlog.get_logger()


class LocalProviderError(Exception):
    """The local inference endpoint failed or returned malformed output.

    Raised on connection refusal, timeout, non-2xx status, or a
    response that does not parse into the expected OpenAI-compatible
    shape. The gateway treats this exactly like a Claude or OpenAI
    provider error: log a warning with the failure kind and fall
    through to the next provider in the chain.
    """


def _classify(exc: Exception) -> str:
    """Map a failure to a coarse kind for structured logging.

    Never includes prompt content or response bodies: provider error
    strings can echo request content and the tutor carries child
    speech. Only the failure category is logged.
    """
    if isinstance(exc, httpx.TimeoutException):
        return "timeout"
    if isinstance(exc, httpx.ConnectError):
        return "unreachable"
    if isinstance(exc, httpx.HTTPStatusError):
        return "http_status"
    if isinstance(exc, (KeyError, ValueError, TypeError)):
        return "malformed_response"
    if isinstance(exc, httpx.HTTPError):
        return "transport"
    return "unknown"


def _chat_completions_url(base_url: str) -> str:
    """Build the chat-completions URL from an OpenAI-compatible base."""
    return base_url.rstrip("/") + "/chat/completions"


async def call_local(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    *,
    model: str | None = None,
    base_url: str | None = None,
    timeout: float | None = None,
) -> dict:
    """Call the local OpenAI-compatible endpoint for a completion.

    Returns a dict shaped exactly like the gateway's other provider
    calls: ``content``, ``model``, ``input_tokens``, ``output_tokens``.
    Token counts come from the endpoint's ``usage`` block when present
    and default to 0 otherwise (local usage is recorded but never
    billed). Raises ``LocalProviderError`` on any failure so the
    gateway chain falls through.
    """
    base = base_url or settings.LOCAL_AI_BASE_URL
    use_model = model or settings.LOCAL_AI_MODEL
    use_timeout = timeout if timeout is not None else settings.LOCAL_AI_TIMEOUT_SECONDS
    payload = {
        "model": use_model,
        "max_tokens": max_tokens,
        "temperature": settings.AI_TEMPERATURE,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=use_timeout) as client:
            response = await client.post(_chat_completions_url(base), json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        # Sanctioned log-and-continue site (repo failure policy): warn
        # with the failure kind only, never the prompt, then signal the
        # gateway to fall through.
        slog.warning("local_provider_call_failed", failure_kind=_classify(exc))
        raise LocalProviderError(f"local provider {_classify(exc)}") from exc

    try:
        choice = data["choices"][0]
        content = choice["message"]["content"]
        if content is None:
            raise ValueError("empty content")
        usage = data.get("usage") or {}
        return {
            "content": content,
            "model": data.get("model") or use_model,
            "input_tokens": int(usage.get("prompt_tokens", 0) or 0),
            "output_tokens": int(usage.get("completion_tokens", 0) or 0),
        }
    except Exception as exc:
        slog.warning("local_provider_call_failed", failure_kind="malformed_response")
        raise LocalProviderError("local provider malformed_response") from exc


async def probe_local(
    *,
    base_url: str | None = None,
    model: str | None = None,
    timeout: float | None = None,
) -> dict:
    """Probe the local endpoint for capability detection.

    Returns ``{"reachable": bool, "model": str | None, "latency_ms":
    float | None}`` and never raises. Used by the gateway and a later
    prompt's household-facing selector to detect whether local
    inference is available without committing a real tutor turn. On
    success ``model`` is the model the endpoint reports (falling back
    to the configured model name) and ``latency_ms`` is the round-trip
    time of the probe. On any failure ``reachable`` is False and the
    other fields are None.
    """
    base = base_url or settings.LOCAL_AI_BASE_URL
    use_model = model or settings.LOCAL_AI_MODEL
    use_timeout = timeout if timeout is not None else settings.LOCAL_AI_TIMEOUT_SECONDS
    payload = {
        "model": use_model,
        "max_tokens": 1,
        "messages": [{"role": "user", "content": "ping"}],
    }

    start = time.monotonic()
    try:
        async with httpx.AsyncClient(timeout=use_timeout) as client:
            response = await client.post(_chat_completions_url(base), json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        slog.warning("local_provider_probe_failed", failure_kind=_classify(exc))
        return {"reachable": False, "model": None, "latency_ms": None}

    latency_ms = round((time.monotonic() - start) * 1000, 1)
    reported_model = use_model
    if isinstance(data, dict) and data.get("model"):
        reported_model = data["model"]
    return {"reachable": True, "model": reported_model, "latency_ms": latency_ms}
