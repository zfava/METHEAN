"""Guard: no silent exception swallows in backend/app, ever again.

The June audit found dozens of ``except Exception: pass`` blocks hiding
real failures. The repo-wide eradication converted every one to a
structured log, a narrowed type, or a re-raise (see
docs/architecture-decisions.md, "Failure handling policy: loud by
default, silent never"). These tests walk the application AST so the
count can never silently grow back:

1. Zero broad handlers (bare ``except:``, ``except Exception``,
   ``except BaseException``, or a tuple containing either) whose body
   is a single ``pass``.
2. Every broad handler's body contains at least one logging call or a
   ``raise``.

Exemption mechanism: a genuinely justified permanent swallow carries
``# swallow-exempt: <reason>`` on the ``except`` line. The tests
recognize exemptions, surface them in the failure output so review
sees them, and fail any exemption whose reason is empty. There are
currently no exemptions; keep it that way unless a reason survives
review.
"""

import ast
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"

LOG_METHOD_NAMES = frozenset({"debug", "info", "warning", "error", "exception", "critical"})

EXEMPT_MARKER = "# swallow-exempt:"


def _catches_broad(handler: ast.ExceptHandler) -> bool:
    t = handler.type
    if t is None:
        return True
    if isinstance(t, ast.Name) and t.id in ("Exception", "BaseException"):
        return True
    if isinstance(t, ast.Tuple):
        return any(isinstance(e, ast.Name) and e.id in ("Exception", "BaseException") for e in t.elts)
    return False


def _body_has_log_or_raise(handler: ast.ExceptHandler) -> bool:
    for node in ast.walk(ast.Module(body=handler.body, type_ignores=[])):
        if isinstance(node, ast.Raise):
            return True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in LOG_METHOD_NAMES:
            return True
    return False


def _exemption(source_lines: list[str], handler: ast.ExceptHandler) -> str | None:
    """The exemption reason on the handler's except line, or None."""
    line = source_lines[handler.lineno - 1]
    if EXEMPT_MARKER in line:
        return line.split(EXEMPT_MARKER, 1)[1].strip()
    return None


def _broad_handlers():
    for path in sorted(APP_DIR.rglob("*.py")):
        source = path.read_text()
        lines = source.splitlines()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Try):
                continue
            for handler in node.handlers:
                if _catches_broad(handler):
                    rel = path.relative_to(APP_DIR.parent).as_posix()
                    yield rel, lines, handler


def test_zero_bare_pass_swallows():
    """No broad handler may swallow into a bare ``pass``."""
    offenders = []
    exemptions = []
    for rel, lines, handler in _broad_handlers():
        if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
            reason = _exemption(lines, handler)
            if reason:
                exemptions.append(f"{rel}:{handler.lineno} ({reason})")
            else:
                offenders.append(f"{rel}:{handler.lineno}")
    assert offenders == [], (
        "Broad except handlers with a bare pass swallow failures silently. "
        "Log with context, narrow the type, or re-raise (see "
        "docs/architecture-decisions.md). Either fix or, only with a reason "
        f"that survives review, mark '{EXEMPT_MARKER} <reason>'. "
        f"Offenders: {offenders}. Current exemptions: {exemptions}"
    )


def test_every_broad_handler_logs_or_raises():
    """Every broad handler must make the failure visible: a logging
    call or a raise somewhere in its body."""
    offenders = []
    exemptions = []
    for rel, lines, handler in _broad_handlers():
        if _body_has_log_or_raise(handler):
            continue
        reason = _exemption(lines, handler)
        if reason:
            exemptions.append(f"{rel}:{handler.lineno} ({reason})")
        else:
            offenders.append(f"{rel}:{handler.lineno}")
    assert offenders == [], (
        "Broad except handlers that neither log nor raise hide failures. "
        f"Offenders: {offenders}. Current exemptions: {exemptions}"
    )


def test_exemptions_carry_reasons():
    """An exemption marker without a reason is itself a failure: the
    mechanism exists for documented judgment calls, not for muting."""
    empty = []
    for rel, lines, handler in _broad_handlers():
        line = lines[handler.lineno - 1]
        if EXEMPT_MARKER in line and not line.split(EXEMPT_MARKER, 1)[1].strip():
            empty.append(f"{rel}:{handler.lineno}")
    assert empty == [], f"swallow-exempt markers without a reason: {empty}"


def test_exemption_count_is_zero():
    """The eradication landed with zero exemptions. If this number must
    move, the reason belongs in the ADR and in code review, and this
    assertion is updated in the same commit."""
    count = 0
    for rel, lines, handler in _broad_handlers():
        if _exemption(lines, handler) is not None:
            count += 1
    assert count == 0, f"expected zero swallow exemptions, found {count}"
