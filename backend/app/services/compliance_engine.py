"""State compliance engine for US homeschool requirements.

Contains requirements for the 20 most-populated homeschool states
and functions to check compliance, generate documents, and track hours.
"""

import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode, Subject
from app.models.governance import Activity, Attempt
from app.models.identity import Child
from app.models.state import ChildNodeState
from app.models.enums import MasteryLevel, AttemptStatus


# ══════════════════════════════════════════════════
# State Requirements Database
# ══════════════════════════════════════════════════

STATE_REQUIREMENTS: dict[str, dict] = {
    "TX": {
        "code": "TX", "name": "Texas", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {
            "all": ["reading", "spelling", "grammar", "mathematics", "citizenship"],
        },
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "Texas has minimal requirements. Curriculum must be bona fide and include the five listed subjects. No notification, testing, or reporting required.",
    },
    "CA": {
        "code": "CA", "name": "California", "strictness": "low",
        "notification": {"required": True, "to_whom": "County superintendent", "when": "By October 1 or within 30 days of starting"},
        "required_subjects": {
            "1-6": ["English", "mathematics", "social sciences", "science", "health", "PE", "fine arts"],
            "7-12": ["English", "mathematics", "social sciences", "science", "health", "PE", "fine arts", "career education"],
        },
        "instruction_hours": {"all": {"annual": None, "daily_min": 3}},
        "instruction_days": 175,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "Private school affidavit (PSA) filed annually. Parent must be 'capable of teaching.'",
    },
    "FL": {
        "code": "FL", "name": "Florida", "strictness": "low",
        "notification": {"required": True, "to_whom": "County school superintendent", "when": "Within 30 days of starting"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": ["standardized test", "evaluation by certified teacher", "other approved method"],
        },
        "special_notes": "Maintain portfolio of records and materials. Annual evaluation required.",
    },
    "NY": {
        "code": "NY", "name": "New York", "strictness": "high",
        "notification": {"required": True, "to_whom": "Local school district superintendent", "when": "By July 1 or within 14 days of starting"},
        "ihip_required": True,
        "required_subjects": {
            "K-6": ["arithmetic", "reading", "spelling", "writing", "English", "geography", "US history", "science", "health", "music", "visual arts", "PE", "patriotism", "citizenship"],
            "7-8": ["arithmetic", "reading", "spelling", "writing", "English", "geography", "US history", "science", "health", "music", "visual arts", "PE", "career education"],
            "9-12": ["English (4yr)", "social studies (4yr)", "mathematics (3yr)", "science (3yr)", "art/music", "health", "PE"],
        },
        "instruction_hours": {"K-6": {"annual": 900}, "7-12": {"annual": 990}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": True,
        "quarterly_report_contents": ["hours completed", "subjects covered", "grade-level assessment"],
        "annual_assessment": {
            "required": True,
            "options": ["standardized test (above 33rd percentile)", "written narrative by certified teacher"],
        },
        "special_notes": "IHIP must be filed for each child each year. Most detailed requirements in the US.",
    },
    "PA": {
        "code": "PA", "name": "Pennsylvania", "strictness": "high",
        "notification": {"required": True, "to_whom": "School district superintendent", "when": "By August 1"},
        "required_subjects": {
            "K-6": ["English", "arithmetic", "geography", "history", "civics", "safety", "health", "PE", "music", "art"],
            "7-12": ["English", "mathematics", "science", "social studies", "health", "PE", "music", "art"],
        },
        "instruction_hours": {"all": {"annual": 900, "daily_min": None}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": ["standardized test (3rd, 5th, 8th grade)", "portfolio review by certified evaluator"],
        },
        "special_notes": "Affidavit and objectives must be filed. Portfolio reviewed by evaluator at year end.",
    },
    "VA": {
        "code": "VA", "name": "Virginia", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School board/superintendent", "when": "By August 15"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": ["standardized test (above 23rd percentile)", "evaluation showing adequate progress"],
        },
        "special_notes": "Parent must have baccalaureate degree OR provide approved curriculum OR be assessed capable.",
    },
    "NC": {
        "code": "NC", "name": "North Carolina", "strictness": "low",
        "notification": {"required": True, "to_whom": "Division of Non-Public Education", "when": "Within 30 days of starting"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["nationally standardized test"]},
        "special_notes": "Maintain attendance and disease immunization records.",
    },
    "OH": {
        "code": "OH", "name": "Ohio", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district superintendent", "when": "Annually"},
        "required_subjects": {
            "all": ["language arts", "geography", "US/Ohio history", "government", "mathematics", "science", "health", "PE", "fine arts", "first aid"],
        },
        "instruction_hours": {"all": {"annual": 900}},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test", "written narrative", "portfolio review"]},
        "special_notes": "Notification must include outline of curriculum.",
    },
    "GA": {
        "code": "GA", "name": "Georgia", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Local superintendent", "when": "By September 1 or within 30 days"},
        "required_subjects": {"all": ["reading", "language arts", "mathematics", "social studies", "science"]},
        "instruction_hours": {"all": {"annual": None, "daily_min": 4.5}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test every 3 years"]},
        "special_notes": "Monthly attendance reports to superintendent. Annual progress report.",
    },
    "IL": {
        "code": "IL", "name": "Illinois", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["language arts", "mathematics", "biological and physical sciences", "social sciences", "fine arts", "health", "PE"]},
        "instruction_hours": {"all": {"annual": None, "daily_min": 5}},
        "instruction_days": 176,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "No registration or notification required. Must teach in English.",
    },
    "IN": {
        "code": "IN", "name": "Indiana", "strictness": "none",
        "notification": {"required": True, "to_whom": "Indiana DOE", "when": "By first day of school year"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "Enrollment report required. Must provide instruction equivalent to public school.",
    },
    "AZ": {
        "code": "AZ", "name": "Arizona", "strictness": "none",
        "notification": {"required": True, "to_whom": "County school superintendent", "when": "Within 30 days"},
        "required_subjects": {"all": ["reading", "grammar", "mathematics", "social studies", "science"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "Affidavit of intent. No curriculum approval, testing, or teacher qualification.",
    },
    "CO": {
        "code": "CO", "name": "Colorado", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district", "when": "14 days before starting"},
        "required_subjects": {"all": ["reading", "writing", "speaking", "mathematics", "history", "civics", "literature", "science"]},
        "instruction_hours": {"1-5": {"annual": 968}, "6-12": {"annual": 1056}},
        "instruction_days": 172,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test", "evaluation by qualified person"]},
        "special_notes": "Evaluation in grades 3, 5, 7, 9, 11.",
    },
    "SC": {
        "code": "SC", "name": "South Carolina", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district", "when": "Annually"},
        "required_subjects": {"all": ["reading", "writing", "mathematics", "social studies", "science", "composition"]},
        "instruction_hours": {"all": {"annual": None, "daily_min": 4.5}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "Maintain records of instruction. Three options for program structure.",
    },
    "TN": {
        "code": "TN", "name": "Tennessee", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "LEA director of schools", "when": "By August 1"},
        "required_subjects": {},
        "instruction_hours": {"1-8": {"annual": None, "daily_min": 4}, "9-12": {"annual": None, "daily_min": 4}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test (grades 5, 7, 9)"]},
        "special_notes": "Attendance records and test results filed with LEA.",
    },
    "UT": {
        "code": "UT", "name": "Utah", "strictness": "none",
        "notification": {"required": True, "to_whom": "School district", "when": "At least 30 days before starting"},
        "required_subjects": {"all": ["language arts", "mathematics", "science", "social studies", "arts", "health", "computing"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "Affidavit to school district. No testing or evaluation.",
    },
    "WA": {
        "code": "WA", "name": "Washington", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district superintendent", "when": "By September 15 or within 2 weeks of starting"},
        "required_subjects": {"all": ["reading", "writing", "spelling", "mathematics", "science", "social studies", "history", "health", "PE", "occupational education", "art", "music"]},
        "instruction_hours": {"all": {"annual": 1000}},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test", "evaluation by certified teacher"]},
        "special_notes": "Parent must be supervised by certified teacher OR have 45 college credits OR complete approved course.",
    },
    "WI": {
        "code": "WI", "name": "Wisconsin", "strictness": "low",
        "notification": {"required": True, "to_whom": "Department of Public Instruction", "when": "By October 15"},
        "required_subjects": {"all": ["reading", "language arts", "mathematics", "social studies", "science", "health"]},
        "instruction_hours": {"all": {"annual": 875}},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "PI-1206 form filed annually. No curriculum approval or testing.",
    },
    "MI": {
        "code": "MI", "name": "Michigan", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["reading", "spelling", "mathematics", "science", "history", "civics", "literature", "writing", "English grammar"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "No notification, testing, or reporting. Must teach required subjects.",
    },
    "ID": {
        "code": "ID", "name": "Idaho", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["language arts", "mathematics", "social studies", "science"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "special_notes": "No notification required. Must provide instruction comparable to public schools.",
    },
}


async def get_hours_breakdown(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    start_date: date | None = None,
    end_date: date | None = None,
) -> dict:
    """Aggregate hours by subject from ChildNodeState and attempts."""
    states_result = await db.execute(
        select(ChildNodeState).where(
            ChildNodeState.child_id == child_id,
            ChildNodeState.household_id == household_id,
        )
    )
    states = states_result.scalars().all()

    total_minutes = sum(s.time_spent_minutes or 0 for s in states)

    # Group by subject via node -> map -> subject
    node_ids = [s.node_id for s in states if s.time_spent_minutes]
    by_subject: dict[str, float] = {}

    if node_ids:
        nodes_result = await db.execute(select(LearningNode).where(LearningNode.id.in_(node_ids)))
        nodes = {n.id: n for n in nodes_result.scalars().all()}

        map_ids = list({n.learning_map_id for n in nodes.values()})
        maps = {}
        if map_ids:
            maps_result = await db.execute(select(LearningMap).where(LearningMap.id.in_(map_ids)))
            maps = {m.id: m for m in maps_result.scalars().all()}

        subj_cache: dict[uuid.UUID, str] = {}
        for m in maps.values():
            s_result = await db.execute(select(Subject.name).where(Subject.id == m.subject_id))
            name = s_result.scalar_one_or_none()
            subj_cache[m.id] = name or "General"

        for state in states:
            if not state.time_spent_minutes:
                continue
            node = nodes.get(state.node_id)
            if node:
                subj_name = subj_cache.get(node.learning_map_id, "General")
            else:
                subj_name = "General"
            by_subject[subj_name] = by_subject.get(subj_name, 0) + state.time_spent_minutes / 60

    return {
        "total_hours": round(total_minutes / 60, 1),
        "by_subject": {k: round(v, 1) for k, v in sorted(by_subject.items())},
    }


async def check_compliance(
    db: AsyncSession,
    household_id: uuid.UUID,
    child_id: uuid.UUID,
    state_code: str,
) -> dict:
    """Run a full compliance check against state requirements."""
    reqs = STATE_REQUIREMENTS.get(state_code.upper())
    if not reqs:
        return {"state": state_code, "error": f"State '{state_code}' not found in database"}

    child_result = await db.execute(select(Child).where(Child.id == child_id))
    child = child_result.scalar_one_or_none()
    if not child:
        return {"error": "Child not found"}

    hours = await get_hours_breakdown(db, household_id, child_id)
    checks = []
    met_count = 0
    total_checks = 0

    # Notification check
    if reqs.get("notification", {}).get("required"):
        total_checks += 1
        checks.append({
            "requirement": "Notification filed",
            "status": "unknown",
            "action": f"File with {reqs['notification'].get('to_whom', 'your school district')} {reqs['notification'].get('when', '')}",
        })

    # Hours check
    for grade_range, hrs_req in reqs.get("instruction_hours", {}).items():
        annual = hrs_req.get("annual")
        if annual:
            total_checks += 1
            current = hours["total_hours"]
            remaining = max(0, annual - current)
            today = date.today()
            weeks_left = max(1, (date(today.year, 6, 30) - today).days / 7)
            status = "met" if current >= annual else ("at_risk" if remaining / weeks_left > 20 else "on_track")
            if status == "met":
                met_count += 1
            checks.append({
                "requirement": f"{annual} annual hours ({grade_range})",
                "status": status,
                "evidence": f"{current:.0f} hours logged, {remaining:.0f} remaining",
            })

    # Days check
    if reqs.get("instruction_days"):
        total_checks += 1
        checks.append({
            "requirement": f"{reqs['instruction_days']} instruction days",
            "status": "unknown",
            "action": "Track via attendance record",
        })

    # Subject checks
    subjects_required = set()
    for grade_range, subjects in reqs.get("required_subjects", {}).items():
        subjects_required.update(subjects)

    logged_subjects = set(hours["by_subject"].keys())
    for subj in sorted(subjects_required):
        total_checks += 1
        # Fuzzy match: check if any logged subject contains the required subject name
        matched = any(subj.lower() in ls.lower() or ls.lower() in subj.lower() for ls in logged_subjects)
        if matched:
            met_count += 1
            checks.append({"requirement": f"{subj} instruction", "status": "met", "evidence": "Subject enrolled"})
        else:
            checks.append({"requirement": f"{subj} instruction", "status": "not_met", "action": f"Add {subj} to curriculum"})

    # Assessment check
    if reqs.get("annual_assessment", {}).get("required"):
        total_checks += 1
        options = reqs["annual_assessment"].get("options", [])
        checks.append({
            "requirement": "Annual assessment",
            "status": "unknown",
            "action": f"Options: {', '.join(options)}" if options else "Complete annual assessment",
        })

    # Quarterly reports
    if reqs.get("quarterly_reports"):
        total_checks += 1
        checks.append({
            "requirement": "Quarterly reports",
            "status": "unknown",
            "action": "Generate quarterly progress reports",
        })

    score = round(met_count / total_checks * 100) if total_checks > 0 else 100

    return {
        "state": reqs["name"],
        "state_code": state_code.upper(),
        "strictness": reqs.get("strictness", "unknown"),
        "compliant": score == 100,
        "score": score,
        "checks": checks,
        "total_hours": hours["total_hours"],
        "hours_by_subject": hours["by_subject"],
        "special_notes": reqs.get("special_notes", ""),
    }
