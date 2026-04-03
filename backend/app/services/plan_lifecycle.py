"""Plan and Activity lifecycle state machines.

Defines valid state transitions and enforces them. Every status change
must go through validate_transition() to ensure only legal moves happen.
"""

from app.models.enums import ActivityStatus, PlanStatus

# Plan lifecycle: (current_status, action) -> new_status
PLAN_TRANSITIONS: dict[tuple[str, str], str] = {
    ("draft", "submit"): "proposed",
    ("proposed", "approve"): "approved",
    ("proposed", "reject"): "draft",
    ("approved", "activate"): "active",
    ("active", "complete"): "completed",
    ("active", "archive"): "archived",
    ("draft", "archive"): "archived",
    ("completed", "archive"): "archived",
}

# Activity lifecycle: (current_status, action) -> new_status
ACTIVITY_TRANSITIONS: dict[tuple[str, str], str] = {
    ("scheduled", "approve"): "scheduled",
    ("scheduled", "start"): "in_progress",
    ("scheduled", "cancel"): "cancelled",
    ("scheduled", "reject"): "cancelled",
    ("in_progress", "complete"): "completed",
    ("in_progress", "skip"): "skipped",
    ("in_progress", "cancel"): "cancelled",
}


def validate_transition(
    current: str,
    action: str,
    transitions: dict[tuple[str, str], str],
) -> str:
    """Return the new status for a valid transition, or raise ValueError.

    Args:
        current: The current status value (e.g. "draft", "scheduled").
        action: The action being taken (e.g. "submit", "approve").
        transitions: The transition table to check against.

    Returns:
        The new status string.

    Raises:
        ValueError: If the transition is not allowed.
    """
    # Normalize enum values
    if hasattr(current, "value"):
        current = current.value

    key = (current, action)
    if key not in transitions:
        allowed = [
            act for (st, act) in transitions if st == current
        ]
        if allowed:
            raise ValueError(
                f"Cannot '{action}' a plan/activity in '{current}' status. "
                f"Allowed actions: {', '.join(allowed)}"
            )
        raise ValueError(
            f"No transitions available from '{current}' status."
        )

    return transitions[key]
