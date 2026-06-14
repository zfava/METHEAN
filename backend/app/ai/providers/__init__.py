"""AI provider implementations that plug into the governance gateway.

Providers in this package implement the same lightweight contract the
gateway's built-in Claude and OpenAI calls use: an async completion
function returning a dict with ``content``, ``model``, ``input_tokens``
and ``output_tokens``, and a plain Exception raised on any transport or
parse failure so the gateway chain falls through to the next provider.

The local provider lives here. Claude, OpenAI, native and mock remain
inline in ``app.ai.gateway`` for now; new providers should land in this
package.
"""

from app.ai.providers.local import (
    LocalProviderError,
    call_local,
    probe_local,
)

__all__ = ["LocalProviderError", "call_local", "probe_local"]
