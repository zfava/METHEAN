# Software Bill of Materials

Generated: 2026-04-15

## Backend Dependencies (Python 3.12)

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| fastapi | 0.115.6 | MIT | Web framework |
| uvicorn | 0.34.0 | BSD-3 | ASGI server |
| gunicorn | 23.0.0 | MIT | Process manager |
| uvloop | 0.21.0 | MIT/Apache-2.0 | Event loop |
| sqlalchemy | 2.0.36 | MIT | ORM |
| asyncpg | 0.30.0 | Apache-2.0 | PostgreSQL driver |
| alembic | 1.14.1 | MIT | Migrations |
| pydantic | 2.10.4 | MIT | Validation |
| pydantic-settings | 2.7.1 | MIT | Config |
| redis | 5.2.1 | MIT | Cache client |
| celery | 5.4.0 | BSD-3 | Task queue |
| pyjwt | 2.10.1 | MIT | JWT tokens |
| bcrypt | 4.2.1 | Apache-2.0 | Password hashing |
| anthropic | 0.42.0 | MIT | Claude API |
| openai | 1.59.3 | Apache-2.0 | OpenAI fallback |
| fsrs | 6.3.1 | MIT | Spaced repetition |
| boto3 | 1.36.2 | Apache-2.0 | S3 storage |
| httpx | 0.28.1 | BSD-3 | HTTP client |
| reportlab | 4.2.5 | BSD | PDF generation |
| structlog | 24.4.0 | Apache-2.0/MIT | Logging |
| sentry-sdk | 2.0.0 | MIT | Error tracking |
| prometheus-client | 0.21.1 | Apache-2.0 | Metrics |
| prometheus-fastapi-instrumentator | 7.0.0 | ISC | Auto-metrics |
| stripe | 8.0.0 | MIT | Billing |
| pytest | 8.3.4 | MIT | Testing |
| pytest-asyncio | 0.25.0 | Apache-2.0 | Async tests |
| locust | 2.29.0 | MIT | Load testing |

## Frontend Dependencies (Node 20)

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| next | 15.1.x | MIT | React framework |
| react | 19.0.x | MIT | UI library |
| react-dom | 19.0.x | MIT | DOM rendering |
| tailwindcss | 4.0.x | MIT | CSS framework |
| typescript | 5.7.x | Apache-2.0 | Type system |
| @capacitor/core | 6.0.x | MIT | Native bridge |
| @capacitor/haptics | 6.0.x | MIT | Haptic feedback |
| @capacitor/push-notifications | 6.0.x | MIT | Push notifications |
| @capacitor/status-bar | 6.0.x | MIT | Status bar control |
| @capacitor/keyboard | 6.0.x | MIT | Keyboard handling |
| @capacitor/network | 6.0.x | MIT | Network status |
| @capacitor/share | 6.0.x | MIT | Native share |
| @capacitor/splash-screen | 6.0.x | MIT | Splash screen |
| @capawesome/capacitor-badge | 6.0.x | MIT | App badge |
| capacitor-native-biometric | 4.2.x | MIT | Biometric auth |
| @playwright/test | 1.59.x | Apache-2.0 | E2E tests |

## Infrastructure

| Component | Version | License |
|-----------|---------|---------|
| PostgreSQL | 16 | PostgreSQL License |
| Redis | 7 | BSD-3 |
| MinIO | latest | AGPL-3.0 / Commercial |
| Docker | 24+ | Apache-2.0 |
