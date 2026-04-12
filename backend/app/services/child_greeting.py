"""Child greeting and encouragement generators.

Generates warm, personalized, data-driven messages for the child's
daily dashboard. Never condescending. Always respectful.
"""

import random
from datetime import UTC, datetime, timedelta


def generate_greeting(
    first_name: str,
    current_streak: int,
    today_count: int,
    first_subject: str | None = None,
    recent_mastery: str | None = None,
) -> str:
    """Generate a personalized daily greeting.

    Rules:
    - Time-of-day aware
    - 1-2 sentences max
    - Respectful and warm, never condescending
    - Varies so it doesn't feel robotic
    """
    hour = datetime.now(UTC).hour

    if hour < 12:
        time_greeting = "Good morning"
    elif hour < 17:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"

    parts = [f"{time_greeting}, {first_name}."]

    # Streak context
    if current_streak >= 7:
        streak_msgs = [
            f"You're on a {current_streak}-day streak.",
            f"{current_streak} days in a row. Impressive.",
            f"Day {current_streak} of your streak. Keep it going.",
        ]
        parts.append(random.choice(streak_msgs))
    elif current_streak >= 3:
        parts.append(f"{current_streak}-day streak and counting.")
    elif current_streak == 0:
        welcome_msgs = [
            "Welcome back.",
            "Good to see you.",
            "Ready when you are.",
        ]
        parts.append(random.choice(welcome_msgs))

    # Today's workload (only if streak didn't add a line)
    if current_streak < 3:
        if today_count == 0:
            parts.append("Nothing scheduled today. Enjoy your free time.")
        elif today_count <= 2:
            parts.append(f"Light day today — just {today_count} activit{'y' if today_count == 1 else 'ies'}.")
        elif first_subject:
            parts.append(f"You have {today_count} activities today, starting with {first_subject}.")

    # Recent mastery
    if recent_mastery and len(parts) < 3:
        parts.append(f"You mastered {recent_mastery} recently.")

    return " ".join(parts)


def generate_encouragement(
    activities_completed_this_week: int,
    time_spent_this_week: int,
    mastery_ups_this_week: int,
    reviews_this_week: int,
    best_week_mastery: int,
    avg_session_minutes: float | None = None,
) -> str:
    """Generate a single line of data-driven encouragement.

    Rules:
    - Grounded in real data, never generic platitudes
    - Praises effort, strategy, persistence — not just correctness
    - Returns empty string if insufficient data
    """
    options = []

    if mastery_ups_this_week > 0:
        if best_week_mastery > 0 and mastery_ups_this_week >= best_week_mastery:
            options.append(f"You mastered {mastery_ups_this_week} new concepts this week. That's your best week this month.")
        else:
            options.append(f"You mastered {mastery_ups_this_week} new concept{'s' if mastery_ups_this_week > 1 else ''} this week.")

    if reviews_this_week >= 10:
        options.append(f"You've reviewed {reviews_this_week} topics this week. Your memory is getting stronger.")
    elif reviews_this_week >= 5:
        options.append(f"{reviews_this_week} review sessions this week. Consistent practice builds lasting knowledge.")

    if activities_completed_this_week >= 15:
        options.append(f"{activities_completed_this_week} activities completed this week. That's dedication.")

    if time_spent_this_week >= 120:
        hours = time_spent_this_week / 60
        options.append(f"You've put in {hours:.1f} hours of focused learning this week.")

    if avg_session_minutes and avg_session_minutes > 25:
        options.append("Your sessions have gotten longer. You're building focus.")

    if not options:
        return ""

    return random.choice(options)
