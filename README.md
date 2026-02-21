# FleetFlow

Modular Fleet & Logistics Management System

## Overview

FleetFlow is a centralized, modular, rule-based fleet and logistics management system designed to digitize operational, compliance, and financial lifecycles of delivery fleets.

## Architecture Summary

FleetFlow uses a Modular Monolith (Microservices-Ready) architectural style:
* Single deployable backend
* Strict module boundaries
* Clear domain separation
* Service layer isolation
* Event-driven internal communication

## Tech Stack

### Frontend
* React (TypeScript)
* Redux Toolkit
* React Router
* MUI / Tailwind
* React Hook Form + Zod

### Backend
* Python 3.12+
* FastAPI (ASGI)
* SQLAlchemy 2.0 (Async)
* Pydantic V2
* JWT Authentication (PyJWT)
* Alembic (Migrations)

### Database
* PostgreSQL (asyncpg driver)

### Infrastructure
* Docker
* Uvicorn / Gunicorn
* GitHub Actions CI/CD

## Setup Instructions

### Backend
```bash
cd backend
uv venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
uv pip install -e ".[dev]"
cp .env.example .env        # Edit with your values
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Folder Structure

```
fleetflow/
├── backend/                # Python / FastAPI API
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── api/            # Route definitions (controllers)
│   │   ├── core/           # Config, security utilities
│   │   ├── db/             # DB engine, sessions, seed
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic DTOs
│   │   ├── services/       # Business logic layer
│   │   └── utils/          # Shared helpers
│   ├── alembic/            # DB migrations
│   ├── tests/              # Pytest test suite
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/               # React SPA
│   └── src/
│       ├── components/
│       └── pages/
├── docs/                   # Engineering documentation
│   ├── PRD.md
│   ├── TDD.md
│   ├── CDB.md
│   ├── implementation-plan.md
│   └── phase-1-tasks.md
└── README.md
```

## Development Workflow

1. Fork/Clone the repository
2. Start PostgreSQL (via Docker or local install)
3. Set up Python environment and install deps
4. Run `alembic upgrade head` to apply migrations
5. Run `python -m app.db.seed` to seed initial data
6. Start the backend with `uvicorn app.main:app --reload`

## License

MIT License
