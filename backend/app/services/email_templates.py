"""Email templates for METHEAN notifications.

All templates return complete HTML with inline CSS.
METHEAN palette: navy #0F1B2D, gold #C6A24E, cream #F5F1E8.
"""


def _base(title: str, body: str) -> str:
    """Wrap content in the base email layout."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title></head>
<body style="margin:0;padding:0;background:#F5F1E8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F1E8;padding:24px 16px;">
<tr><td align="center">
<table width="100%" style="max-width:560px;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
<!-- Header -->
<tr><td style="background:#0F1B2D;padding:20px 24px;">
<span style="color:#C6A24E;font-size:18px;font-weight:700;letter-spacing:0.5px;">METHEAN</span>
</td></tr>
<!-- Body -->
<tr><td style="padding:28px 24px;">
{body}
</td></tr>
<!-- Footer -->
<tr><td style="padding:16px 24px;border-top:1px solid rgba(0,0,0,0.06);">
<p style="margin:0;font-size:11px;color:#9A9A9A;text-align:center;">
METHEAN &mdash; AI advises, you govern.<br>
<a href="https://methean.app/settings" style="color:#4A6FA5;text-decoration:none;">Notification preferences</a>
</p>
</td></tr>
</table>
</td></tr></table>
</body></html>"""


def daily_summary_email(
    parent_name: str,
    children_data: list[dict],
    pending_reviews: int,
    date_str: str,
) -> str:
    """Morning email: today's plan per child + pending reviews."""
    children_html = ""
    for child in children_data:
        name = child.get("name", "Your child")
        count = child.get("activity_count", 0)
        minutes = child.get("total_minutes", 0)
        children_html += f"""
        <div style="background:#FAFAF8;border-radius:8px;padding:12px 16px;margin-bottom:8px;">
            <strong style="color:#1A1A1A;font-size:14px;">{name}</strong>
            <span style="color:#6B6B6B;font-size:12px;margin-left:8px;">
                {count} activities &middot; {minutes} min planned
            </span>
        </div>"""

    pending_html = ""
    if pending_reviews > 0:
        pending_html = f"""
        <div style="background:rgba(184,134,11,0.08);border-left:3px solid #B8860B;border-radius:0 8px 8px 0;padding:12px 16px;margin-top:16px;">
            <strong style="color:#B8860B;font-size:13px;">{pending_reviews} activities need your review</strong>
            <br><a href="https://methean.app/governance/queue" style="color:#4A6FA5;font-size:12px;text-decoration:none;">Review now &rarr;</a>
        </div>"""

    body = f"""
    <p style="margin:0 0 4px;font-size:16px;font-weight:600;color:#1A1A1A;">Good morning, {parent_name}</p>
    <p style="margin:0 0 16px;font-size:13px;color:#6B6B6B;">Here's what's planned for {date_str}.</p>
    {children_html}
    {pending_html}
    <div style="margin-top:20px;text-align:center;">
        <a href="https://methean.app/dashboard" style="display:inline-block;background:#4A6FA5;color:white;padding:10px 24px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;">Open Dashboard</a>
    </div>"""
    return _base(f"Today's Plan — {date_str}", body)


def mastery_milestone_email(
    parent_name: str,
    child_name: str,
    node_title: str,
    subject: str,
    new_level: str,
) -> str:
    """Celebration: child mastered a concept."""
    level_label = new_level.replace("_", " ").title()
    emoji = "🎯" if new_level == "mastered" else "📈"

    body = f"""
    <div style="text-align:center;margin-bottom:20px;">
        <span style="font-size:36px;">{emoji}</span>
    </div>
    <p style="margin:0 0 4px;font-size:18px;font-weight:600;color:#1A1A1A;text-align:center;">{child_name} reached {level_label}!</p>
    <p style="margin:0 0 20px;font-size:13px;color:#6B6B6B;text-align:center;">
        <strong>{node_title}</strong> in {subject}
    </p>
    <div style="background:rgba(45,106,79,0.08);border-radius:8px;padding:16px;text-align:center;">
        <p style="margin:0;font-size:13px;color:#2D6A4F;">
            This milestone was earned through {child_name}'s own work, evaluated by your governance rules.
        </p>
    </div>
    <div style="margin-top:20px;text-align:center;">
        <a href="https://methean.app/maps" style="display:inline-block;background:#2D6A4F;color:white;padding:10px 24px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;">View Progress</a>
    </div>"""
    return _base(f"{child_name} mastered {node_title}!", body)


def governance_alert_email(
    parent_name: str,
    activity_title: str,
    rule_name: str,
    reason: str,
) -> str:
    """A governance rule blocked or flagged something."""
    body = f"""
    <p style="margin:0 0 12px;font-size:15px;font-weight:600;color:#1A1A1A;">Governance Alert</p>
    <div style="background:rgba(184,134,11,0.08);border-left:3px solid #8B7355;border-radius:0 8px 8px 0;padding:14px 16px;">
        <p style="margin:0 0 8px;font-size:13px;color:#1A1A1A;">
            <strong>{activity_title}</strong> was flagged by your governance rule <em>{rule_name}</em>.
        </p>
        <p style="margin:0;font-size:12px;color:#6B6B6B;">{reason}</p>
    </div>
    <div style="margin-top:20px;text-align:center;">
        <a href="https://methean.app/governance/queue" style="display:inline-block;background:#C6A24E;color:white;padding:10px 24px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;">Review Activity</a>
    </div>"""
    return _base("Governance Alert — Action Required", body)


def weekly_digest_email(
    parent_name: str,
    week_stats: dict,
    governance_summary: dict,
) -> str:
    """End-of-week summary."""
    completed = week_stats.get("activities_completed", 0)
    mastered = week_stats.get("nodes_mastered", 0)
    minutes = week_stats.get("total_minutes", 0)
    approved = governance_summary.get("approved", 0)
    rejected = governance_summary.get("rejected", 0)

    body = f"""
    <p style="margin:0 0 4px;font-size:16px;font-weight:600;color:#1A1A1A;">Week in review</p>
    <p style="margin:0 0 16px;font-size:13px;color:#6B6B6B;">Here's how this week went, {parent_name}.</p>
    <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
        <td style="background:#FAFAF8;border-radius:8px;padding:16px;text-align:center;width:33%;">
            <div style="font-size:22px;font-weight:700;color:#1A1A1A;">{completed}</div>
            <div style="font-size:11px;color:#9A9A9A;">activities</div>
        </td>
        <td style="width:8px;"></td>
        <td style="background:#FAFAF8;border-radius:8px;padding:16px;text-align:center;width:33%;">
            <div style="font-size:22px;font-weight:700;color:#2D6A4F;">{mastered}</div>
            <div style="font-size:11px;color:#9A9A9A;">mastered</div>
        </td>
        <td style="width:8px;"></td>
        <td style="background:#FAFAF8;border-radius:8px;padding:16px;text-align:center;width:33%;">
            <div style="font-size:22px;font-weight:700;color:#4A6FA5;">{minutes}m</div>
            <div style="font-size:11px;color:#9A9A9A;">learning time</div>
        </td>
    </tr></table>
    <div style="margin-top:16px;background:#FAFAF8;border-radius:8px;padding:12px 16px;">
        <span style="font-size:12px;color:#6B6B6B;">Governance: {approved} approved, {rejected} rejected</span>
    </div>
    <div style="margin-top:20px;text-align:center;">
        <a href="https://methean.app/dashboard" style="display:inline-block;background:#4A6FA5;color:white;padding:10px 24px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;">View Full Report</a>
    </div>"""
    return _base("Your weekly learning digest", body)


def compliance_warning_email(
    parent_name: str,
    child_name: str,
    state: str,
    issue: str,
) -> str:
    """Compliance hours shortfall or approaching deadline."""
    body = f"""
    <p style="margin:0 0 12px;font-size:15px;font-weight:600;color:#1A1A1A;">Compliance Notice</p>
    <div style="background:rgba(166,61,64,0.08);border-left:3px solid #A63D40;border-radius:0 8px 8px 0;padding:14px 16px;">
        <p style="margin:0 0 8px;font-size:13px;color:#1A1A1A;">
            <strong>{child_name}</strong> &mdash; {state} compliance
        </p>
        <p style="margin:0;font-size:12px;color:#6B6B6B;">{issue}</p>
    </div>
    <div style="margin-top:20px;text-align:center;">
        <a href="https://methean.app/compliance" style="display:inline-block;background:#A63D40;color:white;padding:10px 24px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;">Check Compliance</a>
    </div>"""
    return _base(f"Compliance warning — {child_name}", body)
