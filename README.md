# AquaSwift

**Water tanker delivery platform for Hyderabad** — connecting customers with purified water suppliers through a real-time logistics system.

## Architecture

- **Backend**: Python 3.11 + FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL 15
- **Cache / Broker**: Redis 7
- **Background Jobs**: Celery + Celery Beat
- **Frontend**: Next.js 16 + TypeScript + Tailwind CSS (single monorepo with 3 apps)
  - `/admin` — Operations dashboard (15 pages)
  - `/app` — Customer-facing PWA (mobile-first)
  - `/driver` — Driver portal (mobile-first)

See `docs/03-architecture/SYSTEM_ARCHITECTURE.md` for full architecture documentation.

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for local backend development without Docker)

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

### 2. Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000 — login with `admin@aquaswift.in` / `admin123`.

### API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
aquaswift/
├── backend/                 # FastAPI backend (modular monolith)
│   ├── app/
│   │   ├── core/            # Config, DB, Auth, Errors, Middleware
│   │   ├── auth/            # OTP + JWT authentication
│   │   ├── users/           # User management + RBAC
│   │   ├── orders/          # Order state machine (7 statuses)
│   │   ├── deliveries/      # Delivery tracking + driver assignment
│   │   ├── catalog/         # Water purposes, quality, variants
│   │   ├── inventory/       # Append-only ledger, source balances
│   │   ├── pricing/         # Rules engine (volume/distance/dynamic)
│   │   ├── payments/        # Razorpay integration + webhooks
│   │   ├── ...              # 18 domain modules total
│   │   └── main.py          # App factory + router registration
│   ├── alembic/             # Database migrations
│   ├── scripts/             # Seed data, utilities
│   ├── tests/               # Test suite
│   └── Dockerfile           # Multi-stage (dev + prod)
├── frontend/                # Next.js 16 monorepo
│   ├── app/
│   │   ├── admin/           # 15 admin dashboard pages
│   │   ├── (customer)/app/  # Customer PWA (3 pages)
│   │   ├── driver/          # Driver portal (3 pages)
│   │   └── login/           # Auth page
│   └── lib/
│       ├── api.ts           # Typed API client (67 endpoints)
│       ├── auth.tsx          # JWT + cookie auth context
│       └── utils.ts          # Formatting helpers
├── docs/                    # Architecture & requirements docs
├── docker-compose.yml       # Postgres + Redis + Backend + Celery
└── README.md
```

## Documentation

All project documentation lives in `docs/`:

| Directory | Contents |
|-----------|----------|
| `docs/00-product/` | Product Requirements Document (PRD), Product Vision |
| `docs/01-requirements/` | SRS, Business Rules, Traceability Matrix |
| `docs/02-modules/` | Per-module user stories, tasks, acceptance criteria |
| `docs/03-architecture/` | System architecture, database, API, integrations |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Jobs | Celery + Celery Beat |
| Frontend | Next.js 16 + TypeScript |
| Styling | Tailwind CSS |
| State | TanStack Query (React Query) |
| Charts | Recharts |
| Icons | Lucide React |
| Auth | JWT (access + refresh tokens) |
| Payments | Razorpay |
| Container | Docker + Docker Compose |

## License

Proprietary — All rights reserved.
