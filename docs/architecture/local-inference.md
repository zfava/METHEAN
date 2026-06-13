# Local inference provider

## The independence principle

METHEAN is a parent-governed learning OS for a family's children. The
single most important property of that system is that the family stays
in control of it. Dependence on an external AI vendor is a standing risk
to that control: a vendor can change its prices, change its terms,
deprecate a model, refuse a use case, or simply go away, and every one
of those events would reach into a family's homeschool.

The local inference provider is the first and most important step toward
removing that dependence. It lets the tutor and the other conversational
roles run on an open-weight model on the family's own hardware, through
an OpenAI-compatible local endpoint (Ollama by default, but any
OpenAI-compatible server works). With it enabled and external keys
absent, the product runs with zero external AI API keys: the tutor still
answers, governance still applies, and nothing leaves the home.

## Where it sits

The provider slots into the existing governance gateway
(`backend/app/ai/gateway.py`) behind the exact same contract Claude and
OpenAI already implement. Each provider call is a function returning

```
{"content": str, "model": str, "input_tokens": int, "output_tokens": int}
```

and signals failure by raising an exception, which the gateway's
provider loop catches, logs, and steps past. The local provider
(`backend/app/ai/providers/local.py`) implements that contract over
httpx against `{LOCAL_AI_BASE_URL}/chat/completions`. It adds no new
heavyweight dependency: httpx is already present, so neither the ollama
SDK nor the openai SDK is pulled in.

Because the local provider returns through the same path as Claude, a
response from the local model is indistinguishable downstream from a
Claude response except in its provenance metadata. The gateway still
builds the prompt from role templates, still applies the philosophical
and governance constraints, still records the run, still returns output
as a recommendation rather than writing to state. There is no separate
code path and nothing that bypasses governance.

## Governance is unchanged

This is the load-bearing claim, so it is worth stating plainly: adding
the local provider changes nothing about governance, role checks, the
autonomy policy, or cost controls. The provider sits behind the same
interface as every other provider, so:

- the per-household AI role policy (off / standard / autonomous) is
  evaluated before any provider is chosen, local included;
- the prompt is assembled and constrained identically;
- the run is logged as an `AIRun` with the same shape, the same status
  transitions, and the same input/output capture;
- the response is returned as a recommendation through parent
  governance, never written to state directly.

The only observable difference between a Claude-answered run and a
local-answered run is provenance: the `provider` and `model_used`
fields on the `AIRun`. A test in `tests/test_local_provider.py` asserts
exactly this parity, comparing a local-answered tutor run against a
Claude-answered one and confirming the run shape is identical except for
those provenance fields.

## Provenance

Every AI run records which provider answered it. `AIRun` gained a
`provider` column (migration `063_ai_run_provider.py`) holding the named
provider (`anthropic`, `openai`, `local`, `native`, `mock`). This is the
audit trail a family relies on to prove their tutor ran locally:
`model_used` carries the model identifier, and `provider` carries the
brand. The column is nullable so historical runs predating it stay
readable.

## The tiered strategy

The chain is ordered to put independence first while keeping a
deterministic floor:

1. **LOCAL first (conversational roles).** The tutor, advisor, and other
   conversational roles run on the local open-weight model. These roles
   are well within the reach of a capable open model.
2. **External providers as optional enhancement.** Claude and OpenAI
   remain available and can sit behind local in the chain for families
   that want them, but they are no longer required.
3. **NATIVE floor for the architect.** The deterministic native
   generator continues to back the curriculum-shaped roles (the
   education architect, the curriculum mapper) until an L2 evaluation
   confirms local generation is good enough to take them over. Native is
   curriculum, not AI advice, and it is always reachable: the chain is
   guaranteed to include it so a request can never fall off the end.

Ordering is configurable through `PROVIDER_CHAIN`, a comma-separated
list parsed by `_get_provider_chain()`. When it is empty the default
ordering applies: LOCAL first (only when `LOCAL_AI_ENABLED`), then
Claude, OpenAI, the native floor, and mock. Existing deployments are
unaffected: with LOCAL disabled and no explicit chain, the result is
exactly the historical `Claude -> OpenAI -> native -> mock` order.

## Failure and fallback behavior

The local provider fails like any other provider, and it fails closed:

- **Unreachable / connection refused, timeout, non-2xx status, or
  malformed output** all raise `LocalProviderError`. The gateway loop
  catches it and falls through to the next configured provider, which
  may be the native floor. With external providers disabled the chain is
  `LOCAL -> NATIVE`, so an unreachable local endpoint degrades to the
  deterministic native generator and the request still completes. This
  is the independence proof: no external AI, no crash.
- **It never hangs.** Every call is bounded by `LOCAL_AI_TIMEOUT_SECONDS`,
  enforced on the httpx client. A slow endpoint aborts at the timeout and
  the chain moves on.
- **It never raises unhandled.** Transport and parse errors are converted
  to `LocalProviderError` inside the provider and handled by the loop.
- **It logs honestly and safely.** Failures are a sanctioned
  log-and-continue site under the repo failure policy: the provider emits
  a structlog warning carrying the failure kind only
  (`timeout`, `unreachable`, `http_status`, `malformed_response`,
  `transport`), never the prompt content, because the tutor stream
  carries child speech.

The capability probe `probe_local()` exists for detection rather than
serving: it returns `{reachable, model, latency_ms}` and never throws, so
the gateway and a later household-facing selector can tell whether local
inference is available without committing a real tutor turn.

## Cost

Local inference has zero marginal API cost, and the cost controls reflect
that honestly:

- A local run records its token usage (when the endpoint reports it) but
  is stored at `cost_usd = 0.0`.
- Local runs are excluded from the daily spend accounting
  (`get_daily_usage` filters them out), so they never push a household
  toward the daily cap.
- Local usage is recorded for transparency in the monthly usage ledger
  but does not consume the paid token budget.
- When LOCAL leads the chain (the free primary), the budget gate is
  skipped entirely, so a household at its spend cap can keep using its
  tutor on local hardware.

## Configuration

| Setting | Default | Meaning |
| --- | --- | --- |
| `LOCAL_AI_ENABLED` | `false` | Add the LOCAL provider to the chain. Off keeps behavior unchanged. |
| `LOCAL_AI_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible endpoint base. |
| `LOCAL_AI_MODEL` | `llama3.1:8b` | Open-weight model the endpoint serves. |
| `LOCAL_AI_TIMEOUT_SECONDS` | `30.0` | Hard per-call timeout. |
| `PROVIDER_CHAIN` | `` (empty) | Explicit comma-separated ordering; empty means the default. |

## Known follow-up

Production boot still requires `AI_API_KEY` (a cross-field guard in
`Settings`). A fully local, zero-external-key production deployment will
need that guard relaxed to accept `LOCAL_AI_ENABLED` as an alternative.
That is deliberately out of scope here, to avoid changing existing
production boot behavior, and is left for the prompt that wires the
household-facing selector.
