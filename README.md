# WoW — Water on Way

**Water tanker delivery platform for Hyderabad** — connecting customers with purified water suppliers through a real-time logistics system.

## Current Status

| Component | Status |
|-----------|--------|
| Backend API (20 modules) | ✅ Implemented (not fully tested) |
| Frontend UI (33 pages) | ✅ Implemented (mock data — not API-connected) |
| Documentation (157 tasks, 139 stories) | ✅ Comprehensive |
| Rate Limiting | ❌ Planned (Phase 1) |
| Test Suite | ❌ Planned (Phase 1) — only health check exists |
| Frontend ↔ Backend Integration | ❌ Planned (Phases 2–5) |
| Production Deployment | ❌ Planned (Phase 7) |

**Current Phase: P0 — Audit & Foundation**

## Architecture

- **Backend**: Python 3.12 + FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL 15
- **Cache / Broker**: Redis 7
- **Background Jobs**: Celery + Celery Beat
- **Frontend**: Next.js 16 + TypeScript (single monorepo with 3 apps)
  - `/(customer)/app/` — Customer-facing PWA (mobile-first)
  - `/driver/` — Driver portal (mobile-first)
  - `/admin/` — Operations dashboard (17 pages)

See [SYSTEM_ARCHITECTURE.md](docs/03-architecture/SYSTEM_ARCHITECTURE.md) for full architecture documentation.

## Development Phases

```
P0  Audit & Foundation        ← CURRENT
P1  Core Platform & Security  (Auth hardening, rate limiting, test infra)
P2  Customer App              (Connect UI to real APIs)
P3  Driver App                (Connect UI to real APIs)
P4  Customer + Driver Integration
P5  Admin Dashboard           (Connect admin UI to real APIs)
P6  E2E Validation
P7  Production Readiness
```

See [docs/04-phases/](docs/04-phases/) for detailed phase documentation.

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.12+ (for local backend development without Docker)

### 1. Backend (Docker)

```bash
# Clone and start all services
cp backend/.env.example backend/.env
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed initial data (admin user, roles, permissions)
docker-compose exec backend python -m scripts.seed_data

# Verify backend is running
curl http://localhost:8000/health
```

### 2. Backend (Local — without Docker)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set DATABASE_URL to local Postgres, REDIS_URL to local Redis
uvicorn app.main:app --reload
```

### 3. Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000.

### API Documentation

Once the backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
WoW/
├── backend/                 FastAPI backend (modular monolith)
│   ├── app/
│   │   ├── core/            Config, DB, Auth, Errors, Middleware
│   │   ├── auth/            OTP + JWT authentication
│   │   ├── rbac/            Role-based access control
│   │   ├── users/           User management
│   │   ├── orders/          Order state machine
│   │   ├── deliveries/      Delivery tracking + driver assignment
│   │   ├── catalog/         Water purposes, quality, variants
│   │   ├── inventory/       Append-only ledger
│   │   ├── pricing/         Rules engine
│   │   ├── payments/        Razorpay integration
│   │   └── ...              20 domain modules total
│   ├── alembic/             Database migrations
│   ├── scripts/             Seed data, utilities
│   ├── tests/               Test suite
│   └── Dockerfile           Multi-stage (dev + prod)
├── frontend/                Next.js 16 monorepo
│   ├── app/
│   │   ├── admin/           17 admin dashboard pages
│   │   ├── (customer)/app/  Customer PWA (9 pages)
│   │   ├── driver/          Driver portal (3 pages)
│   │   └── login/           Auth page
│   ├── components/          Shared (WowLogo, MapView)
│   └── lib/                 Auth context, API client, utils
├── docs/                    Documentation
│   ├── 00-product/          PRD, Vision, Personas, Journeys
│   ├── 01-requirements/     SRS, FR, NFR, Business Rules
│   ├── 02-modules/          27 modules × (Tasks, User Stories, AC)
│   ├── 03-architecture/     System, API, DB, ERD, State Machines
│   ├── 04-phases/           Phase roadmap (P0–P7) + Traceability Matrix
│   ├── 05-security/         Rate limiting, Auth, RBAC
│   └── 06-migrations/       AquaSwift → WoW migration
├── docker-compose.yml       Postgres + Redis + Backend + Celery
├── AGENTS.md                AI agent governance
└── README.md                This file
```

## Documentation

| Directory | Contents |
|-----------|----------|
| [docs/00-product/](docs/00-product/) | PRD, Product Vision, User Personas, User Journeys |
| [docs/01-requirements/](docs/01-requirements/) | SRS (86KB), Functional Requirements, NFR, Business Rules |
| [docs/02-modules/](docs/02-modules/) | 27 modules with Tasks, User Stories, Acceptance Criteria |
| [docs/03-architecture/](docs/03-architecture/) | System Architecture, API (132 endpoints), Database, ERD |
| [docs/04-phases/](docs/04-phases/) | Phase roadmap (P0–P7), Traceability Matrix |
| [docs/05-security/](docs/05-security/) | Rate Limiting, Authentication, RBAC |
| [docs/06-migrations/](docs/06-migrations/) | AquaSwift → WoW naming migration |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Jobs | Celery + Celery Beat |
| Frontend | Next.js 16 + TypeScript |
| Maps | Leaflet + react-leaflet |
| Charts | Recharts |
| Icons | Lucide React |
| Auth | JWT (access + refresh tokens) |
| Payments | Razorpay |
| SMS | MSG91 |
| Push | Firebase Cloud Messaging |
| Container | Docker + Docker Compose |

## Agent Governance

See [AGENTS.md](AGENTS.md) for AI coding agent rules, conventions, and development workflow.

## Known Limitations

- **Frontend is mock-only** — no pages are connected to the backend API yet
- **No rate limiting** — all endpoints are unprotected (planned for Phase 1)
- **Only 1 test** — test infrastructure must be built in Phase 1
- **Demo auth bypass active** — must be reverted in Phase 1
- **No Alembic migrations run** — tables not yet created in DB
- **External services not integrated** — MSG91, Razorpay, FCM are stubbed

## License

Proprietary — All rights reserved.
