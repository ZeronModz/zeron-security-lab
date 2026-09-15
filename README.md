# Zeron Web Security Testing Suite

Advanced web security testing platform for authorized security testing of websites and APIs.

## Features

- **Web Testing** - Test website availability, HTTP/HTTPS behavior, redirects, security headers
- **API Testing** - Lightweight API client with authentication, assertions, and history
- **Browser Lab** - Authorized browser testing with JavaScript rendering
- **Cloudflare Testing** - Authorized Cloudflare protection testing on your own domains
- **CAPTCHA Testing** - reCAPTCHA integration testing with official test keys
- **Security Headers** - Check HSTS, CSP, X-Frame-Options and more
- **Response Inspection** - Status codes, headers, body, timing, redirect chains

## Architecture

```
bypass-testing/
├── android/              # Kotlin + Jetpack Compose Android app
│   └── app/src/main/
│       └── com/zeron/securitylab/
│           ├── ui/       # Screens, theme, navigation
│           ├── data/     # API client, repository, Room DB
│           └── util/     # Network utilities
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/v1/       # REST API routes
│   │   ├── core/         # Config, database, logging
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Web testing, API testing
│   │   ├── adapters/     # Cloudflare, CAPTCHA adapters
│   │   ├── security/     # Auth, validation, SSRF protection
│   │   └── middleware/    # Rate limiting, audit, security headers
│   └── tests/            # pytest test suite
├── scripts/              # Setup and dev scripts
├── .github/workflows/    # CI/CD pipelines
├── Dockerfile            # Container deployment
└── docker-compose.yml    # Local container setup
```

## Tech Stack

### Android
- Kotlin + Jetpack Compose
- Material 3 Design
- Navigation Compose
- Room Database
- Retrofit + OkHttp
- Kotlin Coroutines + Flow

### Backend
- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy + aiosqlite/asyncpg
- Pydantic v2
- httpx (async HTTP)
- structlog

### Deployment
- Railway (backend)
- GitHub Actions (CI/CD)
- Docker (containers)
- GitHub Container Registry

## Quick Start

### Backend (Termux)

```bash
cd bypass-testing
bash scripts/setup_termux.sh
bash scripts/dev.sh
```

Backend will be at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Backend (Docker)

```bash
docker compose up --build
```

### Android

Open `android/` in Android Studio and build.

Or via command line:
```bash
cd android
./gradlew assembleDebug
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/system/info` | System information |
| GET | `/api/v1/system/capabilities` | Available capabilities |
| POST | `/api/v1/web/fetch` | Test website |
| POST | `/api/v1/web/render` | Render page |
| POST | `/api/v1/web/screenshot` | Take screenshot |
| POST | `/api/v1/api/request` | Send API request |
| POST | `/api/v1/api/assert` | Assert response |
| GET | `/api/v1/targets` | List targets |
| POST | `/api/v1/targets` | Create target |
| DELETE | `/api/v1/targets/{id}` | Delete target |
| GET | `/api/v1/history` | Test history |
| GET | `/api/v1/cloudflare/health` | Cloudflare adapter health |
| POST | `/api/v1/cloudflare/test` | Test Cloudflare-protected URL |
| GET | `/api/v1/recaptcha/health` | CAPTCHA adapter health |
| POST | `/api/v1/recaptcha/test` | Test reCAPTCHA |

## Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL for production, SQLite for dev
- `API_KEY` - API authentication key
- `JWT_SECRET_KEY` - JWT token signing key
- `ALLOWED_TARGETS` - Comma-separated allowed target domains
- `BLOCKED_NETWORKS` - Blocked IP ranges (SSRF protection)

## Security

- **SSRF Protection** - Private IPs and localhost blocked by default
- **Rate Limiting** - Configurable per-IP rate limits
- **API Authentication** - API key or JWT token required
- **Security Headers** - X-Frame-Options, CSP, HSTS, etc.
- **Input Validation** - All inputs validated and sanitized
- **Audit Logging** - All requests logged with IDs

## Authorized Testing Only

This application is for testing websites and APIs you own or have explicit permission to test. Do not use against third-party websites without authorization.

## Third-Party Attributions

### CloudflareBypassForScraping
- Repository: https://github.com/sarperavci/CloudflareBypassForScraping
- License: MIT
- Copyright: Sarper AVCI
- Used via adapter layer for authorized testing

### GoogleRecaptchaBypass
- Repository: https://github.com/sarperavci/GoogleRecaptchaBypass
- License: MIT (inherited from upstream)
- Used via adapter layer with official test keys

## License

MIT License - see individual component licenses for details.
