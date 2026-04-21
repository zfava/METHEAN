# State Privacy Law Posture

METHEAN's posture toward state-level consumer privacy laws. This covers data privacy legislation, not homeschool compliance requirements (those are in the compliance engine at `app/services/compliance_engine.py`).

Last updated: 2026-04-17

## Applicable State Laws

| State | Law | Key Requirement | METHEAN Posture |
|---|---|---|---|
| California | CPRA (California Privacy Rights Act) | Right to know, delete, correct, limit use of sensitive data. Applies to businesses meeting revenue/data thresholds. | METHEAN is below CPRA thresholds today. Technical controls (export, deletion cascade, no data sale) align with CPRA requirements. No CPRA-specific opt-out mechanism yet. |
| Colorado | CPA (Colorado Privacy Act) | Consent for sensitive data, right to opt out of profiling. | METHEAN does not profile for advertising. Educational profiling is the core service. Parental consent is implicit via account creation. |
| Connecticut | CTDPA | Similar to CPA. Data protection assessments for high-risk processing. | No formal data protection assessment completed. Educational profiling of minors may qualify as high-risk processing. |
| Utah | UCPA (Utah Consumer Privacy Act) | Narrower than CPRA. Right to delete, right to data portability. | Export and deletion capabilities satisfy portability and deletion rights. |
| Virginia | VCDPA (Virginia Consumer Data Protection Act) | Consent for sensitive data processing (children's data is sensitive). | Parental consent via account creation. No separate opt-in mechanism for child data processing. |
| Texas | TDPSA (Texas Data Privacy and Security Act) | Similar to VCDPA. Effective July 2024. | Same posture as Virginia. |
| Montana | MCDPA | Similar scope, effective October 2024. | Same posture as Virginia. |
| Oregon | OCPA | Effective July 2024, broad scope. | Same posture as Virginia. |
| New York | SHIELD Act | Reasonable security measures for private information. | RLS, encryption in transit, access controls, audit logging satisfy "reasonable security" standard. |

## METHEAN's General Posture

1. **Data minimization**: We collect only data necessary for the educational service. See [data-inventory.md](data-inventory.md).
2. **Purpose limitation**: Data is used exclusively for educational service delivery, compliance reporting, and parent dashboards. No secondary uses.
3. **No data sale**: METHEAN does not sell personal data to any party. This is a blanket commitment, not state-specific.
4. **Right to delete**: Implemented via CASCADE deletion across all household-scoped tables.
5. **Right to export**: Implemented via `POST /api/v1/household/export`.
6. **Right to correct**: Parents can edit all child data directly in the platform.
7. **Security**: PostgreSQL RLS, TLS, JWT auth, CSRF protection, structured audit logging.

## What Is Not Yet Implemented

- **CPRA-specific "Do Not Sell" link**: Not needed at current scale but will be required if METHEAN meets CPRA thresholds.
- **Data protection impact assessment (DPIA)**: Required by CTDPA and GDPR (if expanding to EU). Not completed.
- **Minor-specific consent mechanism**: Several states require heightened consent for processing minors' data. The current implicit-consent-via-parent-account model may need a formal consent flow.
- **Universal opt-out signal recognition**: CPRA requires honoring Global Privacy Control (GPC) browser signals. Not implemented.
