# Play Store Data Safety Questionnaire

## Data Collected

| Data Type | Collected | Shared | Purpose |
|-----------|-----------|--------|---------|
| Email address | Yes | No | Account creation and login |
| Name | Yes | No | Display name for parent account |
| Child first name | Yes | No | Personalization within the family |
| Usage analytics | Yes | No | App improvement, feature usage |
| Crash diagnostics | Yes | No | Bug fixing and stability |

## Security Practices

- **Data encrypted in transit**: Yes (HTTPS/TLS)
- **Data encrypted at rest**: Yes (PostgreSQL encryption, S3 encryption)
- **Data deletion**: Users can request deletion via Settings > Account > Delete Account, or by emailing privacy@methean.app
- **Independent security review**: Not yet (planned)

## Data NOT Collected
- Location data
- Financial information (Stripe handles payment directly)
- Contact lists
- Device identifiers (beyond push notification tokens)
- Browsing history
- Search history

## Third-Party SDKs
- **Stripe** (payment processing only, no data shared)
- **Firebase Cloud Messaging** (push notification delivery only)
- **Resend** (transactional email delivery only)

## Children's Privacy (COPPA)
- Child accounts are created and managed by parents
- Children's data is scoped to the family household
- No advertising or tracking of children
- AI interactions with children are logged and parent-inspectable
- Parents can delete all child data at any time
