"""State compliance engine for US homeschool requirements.

Contains requirements for all 50 US states plus DC
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

# IMPORTANT: This data is provided for informational purposes only and should
# not be construed as legal advice. Homeschool laws change frequently. Parents
# should verify current requirements with their state's Department of Education
# and consider consulting HSLDA (hslda.org/legal) or a qualified attorney.
# Data last verified: 2026-04-06

STATE_REQUIREMENTS: dict[str, dict] = {
    # ── Alabama ───────────────────────────────────────
    "AL": {
        "code": "AL", "name": "Alabama", "strictness": "low",
        "notification": {"required": True, "to_whom": "Local school district superintendent", "when": "One-time upon beginning (church school option)"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test", "evaluation by certified teacher"]},
        "record_retention_years": None,
        "special_notes": "Three options: church/umbrella school (most popular, minimal requirements), private school, or private tutor (requires AL certified teacher). Church schools operate as ministry of a church — no mandated subjects or hours. CHOOSE Act ESA available ($2,000/student starting 2025-2026). Must keep attendance records. Assessment required annually under all options.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Alaska ────────────────────────────────────────
    "AK": {
        "code": "AK", "name": "Alaska", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Under the homeschool statute (independent option), no notice, subjects, testing, or reporting required. Alternative options: correspondence study program (~$2,700 allotment but requires testing/teacher contact), private tutor (requires AK teaching certificate), or private school (180 days, testing grades 4, 6, 8).",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Arizona ───────────────────────────────────────
    "AZ": {
        "code": "AZ", "name": "Arizona", "strictness": "low",
        "notification": {"required": True, "to_whom": "County school superintendent", "when": "Within 30 days of starting (one-time affidavit)"},
        "required_subjects": {"all": ["reading", "grammar", "mathematics", "social studies", "science"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Affidavit of intent filed once. No curriculum approval, testing, or teacher qualification required. HSLDA classifies as 'no notice' despite the one-time affidavit. Empowerment Scholarship Account (ESA) available.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Arkansas ──────────────────────────────────────
    "AR": {
        "code": "AR", "name": "Arkansas", "strictness": "low",
        "notification": {"required": True, "to_whom": "Local school district superintendent", "when": "By August 15 (or December 15 for spring start)"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "No mandated subjects or testing (Act 832 of 2015 repealed all testing). Must sign waiver of state liability. LEARNS Act universal ESA available (~$6,864/student). Late filing after Aug 15 triggers 5-school-day waiting period. Forms available June 1.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── California ────────────────────────────────────
    "CA": {
        "code": "CA", "name": "California", "strictness": "low",
        "notification": {"required": True, "to_whom": "County superintendent", "when": "Between October 1 and October 15 annually (PSA option)"},
        "required_subjects": {
            "1-6": ["English", "mathematics", "social sciences", "science", "health", "PE", "fine arts"],
            "7-12": ["English", "mathematics", "social sciences", "science", "health", "PE", "fine arts", "career education"],
        },
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "PSA (Private School Affidavit) option: file Oct 1-15, no hour/day requirements, no testing. The 3-hour daily minimum and 175-day requirement apply only to the separate private tutor option (requires CA-credentialed teacher). Parent must be 'capable of teaching.' Keep attendance register.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Colorado ──────────────────────────────────────
    "CO": {
        "code": "CO", "name": "Colorado", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district", "when": "14 days before starting, via certified mail"},
        "required_subjects": {"all": ["reading", "writing", "speaking", "mathematics", "history", "civics", "US Constitution", "literature", "science"]},
        "instruction_hours": {"1-5": {"annual": 968}, "6-12": {"annual": 1056}},
        "instruction_days": 172,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test", "evaluation by qualified person", "evaluation by certified teacher"]},
        "record_retention_years": None,
        "special_notes": "172 days at minimum 4 hours/day. Evaluation required in grades 3, 5, 7, 9, 11. Test results kept by parent — not submitted unless requested. Notification required each year.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Connecticut ───────────────────────────────────
    "CT": {
        "code": "CT", "name": "Connecticut", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["reading", "writing", "spelling", "English grammar", "geography", "arithmetic", "US history", "citizenship"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "No statutory notification required. The CT Board of Education 'Suggested Procedure' recommends filing NOI and annual portfolio review, but this is voluntary policy, NOT law. School officials may claim it is required — it is not. Required subjects must be covered over K-12, not necessarily every year.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Delaware ──────────────────────────────────────
    "DE": {
        "code": "DE", "name": "Delaware", "strictness": "low",
        "notification": {"required": True, "to_whom": "Delaware Department of Education", "when": "One-time upon initially opening homeschool"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Two annual reports only: enrollment by September 30 and end-of-year attendance by July 31 to DE DOE. No mandated subjects, hours, or testing. Single-family or multi-family homeschool options. HSLDA classifies as 'no notice, low regulation.'",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── District of Columbia ──────────────────────────
    "DC": {
        "code": "DC", "name": "District of Columbia", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "DC Office of the State Superintendent of Education (OSSE)", "when": "15 business days before starting; continuation by August 15 annually"},
        "required_subjects": {"all": ["language arts", "mathematics", "science", "social studies", "art", "music", "health", "PE"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Parent must have high school diploma or equivalent (waiver available from OSSE). Must provide 'thorough and regular instruction of sufficient duration.' Notify OSSE 15 days before discontinuing. Only one homeschool option exists in DC.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Florida ───────────────────────────────────────
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
            "options": [
                "evaluation by certified teacher",
                "standardized test",
                "state student assessment",
                "evaluation by psychologist holding valid active license",
                "other method mutually agreed upon with superintendent",
            ],
        },
        "record_retention_years": 2,
        "special_notes": "Maintain portfolio of records and materials (preserved for 2 years). Annual evaluation required — five options available. No mandated subjects. Terminate by filing written notice with superintendent. Log of texts and sample work sheets recommended.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Georgia ───────────────────────────────────────
    "GA": {
        "code": "GA", "name": "Georgia", "strictness": "low",
        "notification": {"required": True, "to_whom": "Georgia Department of Education", "when": "By September 1 or within 30 days of starting"},
        "required_subjects": {"all": ["reading", "language arts", "mathematics", "social studies", "science"]},
        "instruction_hours": {"all": {"annual": None, "daily_min": 4.5}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test every 3 years (beginning at end of 3rd grade)"]},
        "record_retention_years": 3,
        "special_notes": "Declaration of intent filed with GA DOE (changed from local superintendent in 2013). 4.5-hour minimum school day. Annual written progress report kept for 3 years. Standardized testing every 3 years starting at end of grade 3. Monthly attendance reports to superintendent NO LONGER required (eliminated 2013). Note: HSLDA classifies Georgia as low regulation. METHEAN rates it moderate due to monthly attendance reporting and triennial testing.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Hawaii ────────────────────────────────────────
    "HI": {
        "code": "HI", "name": "Hawaii", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Principal of child's zoned public school", "when": "Before beginning homeschool"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": [
                "standardized achievement test (grades 3, 5, 8, 10)",
                "written evaluation by parent with work samples",
                "participation in Hawaii Statewide Testing Program",
            ],
        },
        "record_retention_years": None,
        "special_notes": "No mandated subjects, but curriculum must be 'structured, cumulative, and sequential, based on educational objectives and the needs of the child.' Annual progress report to local principal required. Must keep record of planned curriculum with start/end dates.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Idaho ─────────────────────────────────────────
    "ID": {
        "code": "ID", "name": "Idaho", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["language arts", "mathematics", "social studies", "science"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "No notification, testing, or reporting required. Must provide instruction comparable to public schools in listed subjects.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Illinois ──────────────────────────────────────
    "IL": {
        "code": "IL", "name": "Illinois", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["language arts", "mathematics", "biological and physical sciences", "social sciences", "fine arts", "health", "PE"]},
        "instruction_hours": {},
        "instruction_days": 176,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "No registration or notification required. Must teach in English. 176-day requirement derived from IL public school law — HSLDA does not confirm this applies to homeschools. No testing or reporting.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Indiana ───────────────────────────────────────
    "IN": {
        "code": "IN", "name": "Indiana", "strictness": "low",
        "notification": {"required": True, "to_whom": "Indiana Department of Education", "when": "Enrollment report by first day of school year"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "HSLDA classifies as 'no notice required.' The DOE online enrollment form is voluntary, not legally required. Must provide instruction equivalent to public school (180 days). Keep attendance records. No mandated subjects or testing.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Iowa ──────────────────────────────────────────
    "IA": {
        "code": "IA", "name": "Iowa", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Five options. Independent Private Instruction (IPI): no notice, no subjects, no testing, no reporting — but cannot access dual enrollment or public school programs. Competent Private Instruction (CPI) Options 3-5: require Form A filing and annual assessment, but provide dual enrollment and extracurricular access. Choose IPI for maximum freedom or CPI for public school access.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Kansas ────────────────────────────────────────
    "KS": {
        "code": "KS", "name": "Kansas", "strictness": "low",
        "notification": {"required": True, "to_whom": "State Board of Education", "when": "One-time registration when starting"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": 186,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Operates as non-accredited private school. One-time registration only (not annual). No mandated subjects or testing. Teacher must be 'competent' (undefined in statute — no degree or certification required). Instruction must be 'planned and scheduled.' Always refer to your homeschool as a 'private school' when dealing with officials.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Kentucky ──────────────────────────────────────
    "KY": {
        "code": "KY", "name": "Kentucky", "strictness": "low",
        "notification": {"required": True, "to_whom": "Local board of education", "when": "Within first two weeks of school year, annually"},
        "required_subjects": {"all": ["reading", "writing", "spelling", "grammar", "history", "mathematics", "science", "civics"]},
        "instruction_hours": {"all": {"annual": 1062}},
        "instruction_days": 170,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Operates under private school statute (no homeschool-specific law). Must maintain attendance and scholarship reports (report cards) on same schedule as local public schools (every 6-9 weeks). Must teach in English. 1,062 hours over 170 days. Records only requestable if evidence of non-compliance.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # ── Louisiana ─────────────────────────────────────
    "LA": {
        "code": "LA", "name": "Louisiana", "strictness": "low",
        "notification": {"required": True, "to_whom": "Board of Elementary and Secondary Education (BESE)", "when": "Within 15 days of starting; renewal by October 1 annually"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": [
                "LEAP test passing score",
                "standardized test at/above grade level or showing one grade level progress",
                "certified teacher evaluation",
            ],
        },
        "record_retention_years": None,
        "special_notes": "Two options: Home Study (BESE approval, annual renewal with curriculum outline and work samples) or Private School (notification within 10 days, annual attendance report). Home Study curriculum must be 'equal to public school quality' but no specific subject list mandated. 180 days required for both options.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Maine -------------------------------------------------
    "ME": {
        "code": "ME", "name": "Maine", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Local school superintendent", "when": "Within 10 days of starting (one-time); annual letter by September 1"},
        "required_subjects": {"all": ["English and language arts", "mathematics", "science and technology", "social studies", "PE and health", "library skills", "fine arts"]},
        "instruction_hours": {},
        "instruction_days": 175,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": [
                "standardized achievement test",
                "local school-developed test",
                "certified teacher review letter",
                "support group with certified teacher review",
                "advisory board review",
            ],
        },
        "record_retention_years": None,
        "special_notes": "Assessment due by September 1 annually. Alternative: REPS (Recognized Equivalent Private School) option. Maine studies required in one grade between 6-12. Computer proficiency required in one grade between 7-12.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Maryland -----------------------------------------------
    "MD": {
        "code": "MD", "name": "Maryland", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Local superintendent", "when": "15 days before starting; annual verification to continue"},
        "required_subjects": {"all": ["math", "English", "social studies", "science", "art", "music", "health", "PE"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Four options: independent (portfolio), church umbrella, church-exempt school umbrella, or nonpublic school umbrella. Portfolio reviewed by superintendent up to 3 times/year. Must provide 'regular, thorough instruction of sufficient duration.' No teacher qualifications required.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Massachusetts ------------------------------------------
    "MA": {
        "code": "MA", "name": "Massachusetts", "strictness": "high",
        "notification": {"required": True, "to_whom": "Local school committee or superintendent", "when": "Annually; prior approval required before starting"},
        "required_subjects": {"all": ["reading", "writing", "English grammar", "geography", "arithmetic", "drawing", "music", "US history and Constitution", "citizenship", "health", "PE"]},
        "instruction_hours": {"K-6": {"annual": 900}, "7-12": {"annual": 990}},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": [
                "standardized test (if agreed upon with superintendent)",
                "progress reports with dated work samples",
                "other mutually agreed evaluation method",
            ],
        },
        "record_retention_years": None,
        "special_notes": "One of the strictest states. Requires PRIOR APPROVAL from school committee/superintendent before homeschooling can begin. Education plan must be submitted annually. Superintendent may consider parent competency. Framework established by Care and Protection of Charles (1987) court decision.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Michigan -----------------------------------------------
    "MI": {
        "code": "MI", "name": "Michigan", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["reading", "spelling", "mathematics", "science", "history", "civics", "literature", "writing", "English grammar"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "No notification, testing, or reporting required. Must teach required subjects.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Minnesota ----------------------------------------------
    "MN": {
        "code": "MN", "name": "Minnesota", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Local school district superintendent", "when": "By October 1 annually, or within 15 days of withdrawal from public school"},
        "required_subjects": {"all": ["reading", "writing", "literature", "fine arts", "math", "science", "history", "geography", "economics", "government and citizenship", "health", "PE"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": ["nationally normed standardized achievement test"],
        },
        "record_retention_years": None,
        "special_notes": "Annual standardized testing required (waived if accredited by HBEAA). If composite score below 30th percentile, child must be evaluated for learning disabilities. Non-parent instructors must hold MN teaching license. Immunization requirements apply.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Mississippi ---------------------------------------------
    "MS": {
        "code": "MS", "name": "Mississippi", "strictness": "low",
        "notification": {"required": True, "to_whom": "Local school attendance officer", "when": "By September 15 annually (Certificate of Enrollment)"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Certificate of Enrollment filed annually with simple description of education type. No mandated subjects, hours, days, or testing. One of the least regulated states. Public school activity access not guaranteed — varies by district.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Missouri -----------------------------------------------
    "MO": {
        "code": "MO", "name": "Missouri", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["reading", "language arts", "math", "social studies", "science"]},
        "instruction_hours": {"all": {"annual": 1000}},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "1,000 hours total required (600 in core subjects, 400 of those 600 at home location). Must maintain plan book, work samples, and evaluations — but records are NEVER submitted to anyone. Requirements cease at age 16; all requirements end at 17. No notification required.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Montana ------------------------------------------------
    "MT": {
        "code": "MT", "name": "Montana", "strictness": "low",
        "notification": {"required": True, "to_whom": "County superintendent of schools", "when": "Annually at beginning of school fiscal year (July 1)"},
        "required_subjects": {"all": ["reading/English language arts", "mathematics", "social studies", "science", "health", "arts", "career education"]},
        "instruction_hours": {"1-3": {"annual": 720}, "4-12": {"annual": 1080}},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Annual notification to county superintendent. Attendance records must be available on request. No testing required. No immunization requirements (HB 778, effective 2025). Homeschoolers may participate in public school extracurricular activities.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- North Carolina -----------------------------------------
    "NC": {
        "code": "NC", "name": "North Carolina", "strictness": "low",
        "notification": {"required": True, "to_whom": "Division of Non-Public Education", "when": "One-time filing when starting (not annual)"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["nationally standardized test"]},
        "record_retention_years": None,
        "special_notes": "One-time notification only (not annual). Annual standardized test required. Maintain attendance and immunization records. Parent must have high school diploma or equivalent.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- North Dakota -------------------------------------------
    "ND": {
        "code": "ND", "name": "North Dakota", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Local public school district superintendent", "when": "At least 14 days before starting; annually via certified mail"},
        "required_subjects": {"all": ["English language arts", "mathematics", "social studies", "science", "health"]},
        "instruction_hours": {"all": {"annual": None, "daily_min": 4}},
        "instruction_days": 175,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": ["standardized achievement test in grades 4, 6, 8, 10 (administered by ND certified teacher)"],
        },
        "record_retention_years": None,
        "special_notes": "Parent must have HS diploma or GED (if not, monitoring by certified teacher for first 2 years). Test opt-out available for philosophical/moral/religious objection or if parent holds bachelor's degree or teaching license. If composite below 30th percentile, remediation plan required. Statement of Intent filed via certified mail.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Nebraska -----------------------------------------------
    "NE": {
        "code": "NE", "name": "Nebraska", "strictness": "low",
        "notification": {"required": True, "to_whom": "Nebraska Department of Education", "when": "Annually by July 15"},
        "required_subjects": {"all": ["language arts", "mathematics", "science", "social studies", "health"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Operates as exempt school (private school electing not to meet accreditation). 2024 reform eliminated powers to demand achievement tests, parent competency tests, or home inspections. Statement of Election and Assurances form filed annually.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Nevada -------------------------------------------------
    "NV": {
        "code": "NV", "name": "Nevada", "strictness": "low",
        "notification": {"required": True, "to_whom": "Local school district superintendent", "when": "Before starting; via certified mail (one-time unless name/address changes)"},
        "required_subjects": {"all": ["English/language arts", "mathematics", "science", "social studies"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "One-time NOI (no annual re-filing unless name/address changes). Must include educational plan showing required subjects. Filed via certified mail, return receipt requested. Retain superintendent's acknowledgment letter as proof of compliance.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- New Hampshire ------------------------------------------
    "NH": {
        "code": "NH", "name": "New Hampshire", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Participating agency (Commissioner of Ed, superintendent, or nonpublic school principal)", "when": "Within 5 days of commencing"},
        "required_subjects": {"all": ["science", "mathematics", "language", "government", "history", "health", "reading", "writing", "spelling", "NH and US constitutions", "art", "music"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": [
                "certified teacher evaluation with portfolio review",
                "nationally normed standardized test",
                "other portfolio-based assessment",
            ],
        },
        "record_retention_years": 2,
        "special_notes": "Annual evaluation required but results kept by parent, NOT submitted. Portfolio required by law (reading log + work samples, retained 2 years). No minimum test score threshold (eliminated by HB 1663). Participating agency can be nonpublic school principal.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- New Jersey ---------------------------------------------
    "NJ": {
        "code": "NJ", "name": "New Jersey", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "No notification, subjects, hours, testing, or record-keeping required by law. Must provide 'equivalent instruction' (broadly interpreted by courts). School districts may demand notice — this is NOT required by law. One of the least regulated states.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- New Mexico ---------------------------------------------
    "NM": {
        "code": "NM", "name": "New Mexico", "strictness": "low",
        "notification": {"required": True, "to_whom": "New Mexico Public Education Department", "when": "Within 30 days of starting; annually by August 1"},
        "required_subjects": {"all": ["reading", "language arts", "mathematics", "social studies", "science"]},
        "instruction_hours": {},
        "instruction_days": 180,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Parent must have high school diploma or GED. Immunization requirements apply (waivers available). No testing or academic record-keeping required by statute. Annual notification to PED.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- New York -----------------------------------------------
    "NY": {
        "code": "NY", "name": "New York", "strictness": "high",
        "notification": {"required": True, "to_whom": "Local school district superintendent", "when": "By July 1 or within 14 days of starting"},
        "ihip_required": True,
        "required_subjects": {
            "1-6": ["arithmetic", "reading", "spelling", "writing", "English", "geography", "US history", "science", "health", "music", "visual arts", "PE", "patriotism", "citizenship"],
            "7-8": ["arithmetic", "reading", "spelling", "writing", "English", "geography", "US history", "science", "health", "music", "visual arts", "PE", "career education"],
            "9-12": ["English (4yr)", "social studies (4yr)", "mathematics (3yr)", "science (3yr)", "art/music", "health", "PE"],
        },
        "instruction_hours": {"1-6": {"annual": 900}, "7-12": {"annual": 990}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": True,
        "quarterly_report_contents": ["hours completed", "subjects covered", "grade-level assessment"],
        "annual_assessment": {
            "required": True,
            "options": ["standardized test (above 33rd percentile or one year growth)", "written narrative by certified teacher"],
        },
        "record_retention_years": None,
        "special_notes": "IHIP (Individualized Home Instruction Plan) must be filed by August 15 for each child each year. Quarterly reports due to district. Most detailed requirements in the US. HSLDA hours are grades 1-6 (900) and 7-12 (990).",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Ohio ---------------------------------------------------
    "OH": {
        "code": "OH", "name": "Ohio", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district superintendent", "when": "By August 30 or within 5 days of starting"},
        "required_subjects": {"all": ["English language arts", "mathematics", "science", "history", "government", "social studies"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test", "written narrative", "portfolio review by certified teacher"]},
        "record_retention_years": None,
        "special_notes": "New Ohio law significantly streamlined requirements. No hours, no assessment required. Notification must include outline of curriculum. Previous 900-hour and testing requirements have been eliminated.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Oklahoma -----------------------------------------------
    "OK": {
        "code": "OK", "name": "Oklahoma", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": 180,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "No notice, subjects, testing, or record-keeping required. Courts suggest education should be 'equivalent or comparable' to public school. 180 instruction days. HSLDA recommends keeping records for 2 years as protective measure.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Oregon -------------------------------------------------
    "OR": {
        "code": "OR", "name": "Oregon", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "Local Education Service District (ESD)", "when": "Within 10 days of starting (one-time filing)"},
        "required_subjects": {},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": ["standardized test in grades 3, 5, 8, 10 (by August 15)"],
        },
        "record_retention_years": None,
        "special_notes": "One-time notification (not annual). If composite below 15th percentile, re-test within one year. If second test lower, ESD may place education under certified teacher (selected and paid by parent). Special needs children evaluated per IEP. No parent qualifications required.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Pennsylvania -------------------------------------------
    "PA": {
        "code": "PA", "name": "Pennsylvania", "strictness": "high",
        "notification": {"required": True, "to_whom": "School district superintendent", "when": "By August 1"},
        "required_subjects": {
            "K-6": ["English", "arithmetic", "geography", "history", "civics", "safety", "health", "PE", "music", "art"],
            "7-12": ["English", "mathematics", "science", "social studies", "health", "PE", "music", "art"],
        },
        "instruction_hours": {"K-6": {"annual": 900}, "7-12": {"annual": 990}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": ["standardized test (3rd, 5th, 8th grade)", "portfolio review by certified evaluator"],
        },
        "record_retention_years": None,
        "special_notes": "Affidavit and objectives must be filed. Portfolio reviewed by evaluator at year end. Elementary (K-6): 900 hours. Secondary (7-12): 990 hours.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Rhode Island -------------------------------------------
    "RI": {
        "code": "RI", "name": "Rhode Island", "strictness": "high",
        "notification": {"required": True, "to_whom": "Local school committee", "when": "Before beginning homeschool"},
        "required_subjects": {"all": ["reading", "writing", "geography", "arithmetic", "health and PE", "US history", "Rhode Island history", "civics"]},
        "instruction_hours": {},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Must maintain attendance register (available to school committee at year end). No state-level assessment requirement, but local school committees may adopt additional requirements through local policies. 180 days same as public school. No parent qualifications required.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- South Carolina -----------------------------------------
    "SC": {
        "code": "SC", "name": "South Carolina", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district", "when": "Annually"},
        "required_subjects": {
            "all": ["reading", "writing", "mathematics", "social studies", "science"],
            "7-12": ["reading", "writing", "mathematics", "social studies", "science", "composition", "literature"],
        },
        "instruction_hours": {"all": {"annual": None, "daily_min": 4.5}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "HSLDA classifies as low regulation. 4.5-hour minimum school day. Three program structure options (Option 1 with school district, Option 2 with SCAIHS association, Option 3 with accountability association). Semiannual progress reports may be required under Option 1.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- South Dakota -------------------------------------------
    "SD": {
        "code": "SD", "name": "South Dakota", "strictness": "low",
        "notification": {"required": True, "to_whom": "SD Department of Education or local school district", "when": "Within 30 days of beginning"},
        "required_subjects": {"all": ["language arts", "math"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "SB 177 (2021) eliminated standardized testing requirement. Only language arts and math explicitly required. Must lead to mastery of English language. File new notification if moving districts.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Tennessee ----------------------------------------------
    "TN": {
        "code": "TN", "name": "Tennessee", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "LEA director of schools", "when": "Before start of school year"},
        "required_subjects": {},
        "instruction_hours": {"all": {"annual": None, "daily_min": 4}},
        "instruction_days": 180,
        "attendance_tracking": True,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test (grades 5, 7, 9)"]},
        "record_retention_years": None,
        "special_notes": "Data represents Option 1 (Independent Homeschooling). Options 2 and 3 (church-related and Category III schools) have fewer requirements. Parent must have HS diploma or GED for Option 1. Attendance records and test results filed with LEA.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Texas --------------------------------------------------
    "TX": {
        "code": "TX", "name": "Texas", "strictness": "none",
        "notification": {"required": False},
        "required_subjects": {"all": ["reading", "spelling", "grammar", "mathematics", "citizenship"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Texas has minimal requirements. Curriculum must be bona fide (visual-based) and include the five listed subjects. No notification, testing, or reporting required.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Utah ---------------------------------------------------
    "UT": {
        "code": "UT", "name": "Utah", "strictness": "low",
        "notification": {"required": True, "to_whom": "School district", "when": "At least 30 days before starting (one-time affidavit)"},
        "required_subjects": {"all": ["language arts", "mathematics", "science", "social studies", "arts", "health", "computing"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "HSLDA classifies as low regulation (notification required). As of 2025 law update, no specific subjects required. Affidavit to school district. No testing or evaluation required.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Virginia -----------------------------------------------
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
            "options": ["standardized test (above 23rd percentile / 4th stanine)", "evaluation showing adequate progress"],
        },
        "record_retention_years": None,
        "special_notes": "Standard home instruction option (Option 1). Parent must have baccalaureate degree OR provide approved curriculum OR be assessed capable. Annual assessment results due by August 1. Four total homeschool options exist (religious exemption is separate).",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Vermont ------------------------------------------------
    "VT": {
        "code": "VT", "name": "Vermont", "strictness": "high",
        "notification": {"required": True, "to_whom": "Vermont Secretary of Education / Agency of Education", "when": "At least 10 business days before starting; annually"},
        "required_subjects": {
            "K-6": ["reading", "writing", "mathematics", "citizenship and history", "fine arts", "PE", "health"],
            "7-12": ["reading and writing", "literature", "mathematics", "natural science", "citizenship and history"],
        },
        "instruction_hours": {},
        "instruction_days": 175,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": [
                "standardized test",
                "certified teacher review",
                "parent report with portfolio",
                "online academy grades",
                "evidence of passing GED",
            ],
        },
        "record_retention_years": None,
        "special_notes": "Post-July 2023 changes: no longer submit course of study with enrollment notice; assessment results kept by parent, NOT submitted to state. Different subjects for under-13 vs 13+. No parent qualifications required. Enrollment notice must include attestation of 175 days.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Washington ---------------------------------------------
    "WA": {
        "code": "WA", "name": "Washington", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "School district superintendent", "when": "By September 15 or within 2 weeks of starting"},
        "required_subjects": {"all": ["reading", "writing", "spelling", "mathematics", "science", "social studies", "history", "health", "PE", "occupational education", "art", "music"]},
        "instruction_hours": {"all": {"annual": 1000}},
        "instruction_days": 180,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": True, "options": ["standardized test", "evaluation by certified teacher"]},
        "record_retention_years": None,
        "special_notes": "180 days OR 1,000 hours/year (either satisfies). Parent must be supervised by certified teacher (1 hr/wk) OR have 45 college quarter credits OR complete approved parent qualifying course. This parent qualification requirement is critical.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- West Virginia ------------------------------------------
    "WV": {
        "code": "WV", "name": "West Virginia", "strictness": "moderate",
        "notification": {"required": True, "to_whom": "County school board or superintendent", "when": "One-time Notice of Intent (Option 2, most popular)"},
        "required_subjects": {"all": ["reading", "language", "mathematics", "science", "social studies"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {
            "required": True,
            "options": [
                "standardized achievement test (23rd percentile or improvement over prior year)",
                "public school testing program",
                "certified teacher portfolio review",
                "alternative assessment with superintendent approval",
            ],
        },
        "record_retention_years": 3,
        "special_notes": "Three options: school board approval (Option 1, 180 days), Notice of Intent (Option 2, most popular, one-time filing), or Learning Pod (Option 3). Parent must have HS diploma or equivalent. Assessment results submitted at grades 3, 5, 8, 11 by June 30 only. Hope Scholarship ESA available (separate legal category).",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Wisconsin ----------------------------------------------
    "WI": {
        "code": "WI", "name": "Wisconsin", "strictness": "low",
        "notification": {"required": True, "to_whom": "Department of Public Instruction", "when": "By October 15"},
        "required_subjects": {"all": ["reading", "language arts", "mathematics", "social studies", "science", "health"]},
        "instruction_hours": {"all": {"annual": 875}},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "PI-1206 form filed annually. No curriculum approval or testing required. 875 hours/year.",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
    },
    # -- Wyoming ------------------------------------------------
    "WY": {
        "code": "WY", "name": "Wyoming", "strictness": "low",
        "notification": {"required": True, "to_whom": "Local school board", "when": "Annually with curriculum description"},
        "required_subjects": {"all": ["reading", "writing", "mathematics", "civics", "history", "literature", "science"]},
        "instruction_hours": {},
        "instruction_days": None,
        "attendance_tracking": False,
        "quarterly_reports": False,
        "annual_assessment": {"required": False},
        "record_retention_years": None,
        "special_notes": "Homeschool Freedom Act (HB 46, effective July 2025) eliminated all notification and curriculum submission requirements. 12th state with no government requirements. Must provide sequentially progressive curriculum in listed subjects. Optional free PAWS testing available (notify district by November 1).",
        "last_verified": "2026-04-06", "source": "HSLDA + state DOE",
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
