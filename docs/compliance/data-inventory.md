# METHEAN Data Inventory

Complete inventory of personal data collected, stored, and processed. Every field listed here appears in a SQLAlchemy model in `backend/app/models/`.

Last verified: 2026-04-17

## Parent (User) Data

| Field | Model | Source | Purpose | Retention | Deleteable | Exportable |
|---|---|---|---|---|---|---|
| email | User | Parent (registration) | Authentication, notifications | Until account deletion | Yes (cascade) | Yes |
| password_hash | User | Parent (registration) | Authentication | Until account deletion | Yes (cascade) | No (hashed, not exportable) |
| display_name | User | Parent (registration) | Personalization, reports | Until account deletion | Yes (cascade) | Yes |
| email_verified | User | System | Email validation status | Until account deletion | Yes (cascade) | No |
| notification_preferences | User | Parent (settings) | Email/push notification control | Until account deletion | Yes (cascade) | Yes |
| role | User | System | Access control (owner, co_parent, observer) | Until account deletion | Yes (cascade) | Yes |
| ip_address | AuditLog | System (request) | Security audit trail | Until account deletion | Yes (anonymized) | No |

## Child Data

| Field | Model | Source | Purpose | Retention | Deleteable | Exportable |
|---|---|---|---|---|---|---|
| first_name | Child | Parent | Personalization, reports, compliance documents | Until account deletion | Yes (cascade) | Yes |
| last_name | Child | Parent | Reports, compliance documents | Until account deletion | Yes (cascade) | Yes |
| date_of_birth | Child | Parent | Grade/age calculation, compliance, temporal rule triggers | Until account deletion | Yes (cascade) | Yes |
| grade_level | Child | Parent | Curriculum planning, compliance | Until account deletion | Yes (cascade) | Yes |
| is_active | Child | System | Soft-delete flag | Until account deletion | Yes (cascade) | Yes |

## Child Preferences and Learning Profile

| Field | Model | Source | Purpose | Retention | Deleteable | Exportable |
|---|---|---|---|---|---|---|
| learning_style | ChildPreferences | Parent | AI tutoring personalization | Until account deletion | Yes (cascade) | Yes |
| interests | ChildPreferences | Parent | Content enrichment, engagement | Until account deletion | Yes (cascade) | Yes |
| subject_levels | ChildPreferences | Parent | Curriculum planning | Until account deletion | Yes (cascade) | Yes |
| strengths | ChildPreferences | Parent | AI advisor context | Until account deletion | Yes (cascade) | Yes |
| areas_for_growth | ChildPreferences | Parent | AI advisor context | Until account deletion | Yes (cascade) | Yes |
| parent_notes | ChildPreferences | Parent | Free-text observations about child | Until account deletion | Yes (cascade) | Yes |

## Child-Generated Educational Content

| Field | Model | Source | Purpose | Retention | Deleteable | Exportable |
|---|---|---|---|---|---|---|
| attempt responses | Attempt | Child (via tutor) | Mastery evaluation, FSRS scheduling | Until account deletion | Yes (cascade) | Yes |
| attempt score | Attempt | System (evaluator AI) | Mastery tracking | Until account deletion | Yes (cascade) | Yes |
| activity_feedback | ActivityFeedback | Parent | Session quality notes | Until account deletion | Yes (cascade) | Yes |
| reading_log entries | ReadingLogEntry | Parent/Child | Reading habit tracking, compliance hours | Until account deletion | Yes (cascade) | Yes |
| portfolio entries | PortfolioEntry | Parent | Work samples, compliance evidence | Until account deletion | Yes (cascade) | Yes |
| assessment results | Assessment | Parent/System | Formal evaluation records | Until account deletion | Yes (cascade) | Yes |

## Intelligence and Analytics Data (Parent-Only Visibility)

| Field | Model | Source | Purpose | Retention | Deleteable | Exportable |
|---|---|---|---|---|---|---|
| engagement_patterns | LearnerIntelligence | System (computed) | Learning style analysis | Until account deletion | Yes (cascade) | Yes |
| pace_trends | LearnerIntelligence | System (computed) | Progress tracking | Until account deletion | Yes (cascade) | Yes |
| parent_observations | LearnerIntelligence | Parent | Qualitative notes on child's learning | Until account deletion | Yes (cascade) | Yes |
| calibration_profile | CalibrationProfile | System (computed) | Evaluator accuracy tracking | Until account deletion | Yes (cascade) | No (internal) |
| style_vector | LearnerStyleVector | System (computed) | Learning style dimensions | Until account deletion | Yes (cascade) | Yes |
| wellbeing_anomalies | WellbeingAnomaly | System (detected) | Parent-only wellbeing alerts | Until account deletion | Yes (cascade) | No (parent-only) |
| family_insights | FamilyInsight | System (detected) | Cross-child pattern analysis | Until account deletion | Yes (cascade) | No (parent-only) |

## Household Data

| Field | Model | Source | Purpose | Retention | Deleteable | Exportable |
|---|---|---|---|---|---|---|
| household name | Household | Parent | Organization, reports | Until account deletion | Yes (root) | Yes |
| philosophical_profile | Household | Parent | Curriculum approach (classical, CM, Montessori) | Until account deletion | Yes (root) | Yes |
| home_state | Household | Parent | Compliance requirement selection | Until account deletion | Yes (root) | Yes |
| stripe_customer_id | Household | System (Stripe) | Billing | Until account deletion | Yes (root) | No |
| stripe_subscription_id | Household | System (Stripe) | Subscription management | Until account deletion | Yes (root) | No |
| timezone | Household | Parent | Scheduling, notification timing | Until account deletion | Yes (root) | Yes |

## Data NOT Collected

METHEAN does not collect:
- Social Security numbers
- Physical addresses (beyond state for compliance)
- Phone numbers
- Biometric data
- Location data
- Browser fingerprints
- Third-party tracking cookies
- Behavioral advertising profiles
- Photos or videos of children (unless parent uploads to portfolio)

## Verification

```bash
# Verify every PII field listed above exists in models
grep -rnE "(first_name|last_name|email|date_of_birth|display_name|password_hash)" backend/app/models/identity.py

# Verify CASCADE deletion chain
grep -c "ondelete.*CASCADE" backend/app/models/*.py

# Verify export service covers child data
grep -n "Child\|child" backend/app/services/data_export.py
```
