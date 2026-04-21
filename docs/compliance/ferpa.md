# FERPA Compliance Posture

Draft for legal review. Last updated: 2026-04-17.

## Scope

FERPA applies to educational agencies and institutions that receive federal funding. METHEAN is a consumer tool operated directly by parents; it is not an educational institution and does not receive federal funds.

However, if METHEAN is used in a school-service context (e.g., a charter school, umbrella program, or homeschool co-op that receives federal funding and designates METHEAN as a tool), the platform would operate as a "school official" under FERPA, with a "legitimate educational interest" in the student records it processes.

This document describes METHEAN's technical posture for FERPA compliance in either context.

## Education Records

METHEAN stores the following data that qualifies as "education records" under FERPA (records directly related to a student that are maintained by an educational agency or a party acting on its behalf):

| Record Type | Model | Description |
|---|---|---|
| Mastery records | ChildNodeState | Per-node mastery level (not_started through mastered) |
| Assessment records | Assessment | Formal evaluation results |
| Attempt transcripts | Attempt | Student responses to educational activities |
| Portfolio entries | PortfolioEntry | Work samples and artifacts |
| Progress snapshots | WeeklySnapshot | Weekly aggregated activity metrics |
| Attendance records | (computed) | Instruction hours by subject, derived from activity duration |
| Transcripts | (generated) | PDF academic transcripts generated from mastery and curriculum data |
| Annual curricula | AnnualCurriculum | Year-level scope and sequence with week-by-week plans |
| Reading logs | ReadingLogEntry | Books read, pages, time spent |
| Compliance reports | (generated) | State-specific compliance check results |

## Directory Information

METHEAN does not collect or publish directory information. There are no public profiles, no student directories, and no way for users outside a household to discover or view any student data.

## Rights Under FERPA

### Right to Inspect (34 CFR 99.10)

Parents can inspect all education records through the platform interface. A complete machine-readable export is available via `POST /api/v1/household/export` (ZIP file containing JSON).

Generated documents (IHIP, quarterly reports, attendance records, transcripts) are available as PDF downloads through the `/documents/` API endpoints.

### Right to Amend (34 CFR 99.20)

Parents can edit student profiles, preferences, and annotations directly through the platform. Assessment results can be annotated with parent notes. If a parent believes a record is inaccurate, they can modify it in-app or contact support.

### Right to Control Disclosure (34 CFR 99.30)

METHEAN does not disclose education records to any third party without parental consent, with the following exceptions:

1. **AI providers** (Anthropic, OpenAI): Student-generated content is sent for educational evaluation. No identifying information (name, DOB) is included. See [processors.md](processors.md).
2. **Email provider** (Resend): Notification content may include student first names in parent-addressed emails. No education records are sent.
3. **Hosting provider**: All data is stored on the hosting platform's infrastructure.

No data is shared with other educational institutions, government agencies, or law enforcement unless required by law and communicated to the parent.

### Records of Disclosure

The `audit_logs` table records all system actions, including any data access events. The `governance_events` table records all governance decisions (approvals, rejections, modifications). Together these provide a disclosure audit trail.

**Verification**:
```bash
grep -n "AuditLog\|GovernanceEvent" backend/app/models/governance.py backend/app/models/operational.py
```

## Technical Controls Supporting FERPA

1. **Access control**: Only authenticated household members can view student data. Role-based permissions (owner, co_parent, observer) control write access.
2. **Tenant isolation**: PostgreSQL Row-Level Security on all 49 household-scoped tables. Cross-household data access is impossible at the database level.
3. **Audit trail**: Immutable audit_logs and governance_events tables record all significant actions.
4. **Data minimization in AI calls**: AI prompts contain educational content and pseudonymous context (mastery level, learning style), not identifying information.

## What Is Not Yet Implemented

- **Formal data processing agreement (DPA) template**: For school-service deployments, a DPA between the school and METHEAN (as the processor) is needed. Template not yet drafted.
- **Student records transfer**: No mechanism to transfer education records to another institution upon request. This would be needed for school-service deployments.
- **Annual FERPA notification**: If used in a school context, the school must issue annual FERPA notifications to parents. METHEAN does not automate this.
