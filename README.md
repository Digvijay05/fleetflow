# FleetFlow

[![Build Status](https://img.shields.io/badge/build-passing-success)]() [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/) [![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

**Modular Fleet & Logistics Management System**

FleetFlow is a centralized, robust, and beautifully designed fleet and logistics management system. Built for speed, reliability, and scale, it digitizes the operational, compliance, and financial lifecycles of modern delivery fleets.

---

## 🌟 Key Features

*   **Role-Based Access Control (RBAC):** Distinct dashboards and capabilities for Administrators, Fleet Managers, Dispatchers, and Customers.
*   **Real-time Tracking:** Customers can track their shipments via a beautiful timeline interface with public or authenticated access paths.
*   **Vehicle & Driver Management:** Track vehicle statuses, maintenance logs, driver availability, and assignments.
*   **Trip Lifecycle Engine:** Robust state machine for trips (`Draft` → `Dispatched` → `In Transit` → `Out for Delivery` → `Delivered` → `Completed`).
*   **Expense & Financial Tracking:** Log trip-specific expenses and calculate revenue and profitability per shipment.
*   **Concurrency & Data Integrity:** Uses optimistic locking (`with_for_update`) to prevent race conditions during dispatching and trip state changes.
*   **Security & Hardening:** Global rate limiting, unified exception handling, JWT authentication, and strict foreign key constraints.

---

## 🏗️ Architecture

FleetFlow is built on a **Modular Monolith** pattern, ready to be split into microservices if needed:

*   **Frontend:** React 18, TypeScript, Vite, React Router v6, Tailwind CSS, Lucide Icons, and Axios for a blazing fast Single Page Application (SPA).
*   **Backend:** FastAPI, Python 3.12, SQLAlchemy 2.0 (Async), Pydantic V2, and Alembic.
*   **Database:** PostgreSQL with `asyncpg` for high-performance non-blocking data access.
*   **Deployment:** Fully dockerized with `docker-compose` for 1-click local setup.

---

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   (Optional) Node.js 20+ and Python 3.12+ for native development

### 1-Click Startup (Docker)

```bash
# Clone the repository
git clone https://github.com/your-username/fleetflow.git
cd fleetflow

# Build and start all services
docker compose up --build -d
```

The application will be available at:
*   **Frontend:** `http://localhost`
*   **Backend API Docs:** `http://localhost:8001/docs`

### Seed Data
The database is automatically provisioned. To log in and explore the app, use the following credentials:
*   **Admin/Fleet Manager:** `admin@fleetflow.com` / `admin123`
*   **Customer:** `customer@fleetflow.com` / `customer123`

*(Note: In a true production environment, seed data should be disabled and passwords changed.)*

---

## 🛡️ Production Hardening
This project includes production-ready safeguards:
1.  **Rate Limiting:** Global rate limit of 60 req/min, with strict 5 req/min on `/login`.
2.  **Concurrency Safeties:** Row-level locks (`SELECT ... FOR UPDATE`) are acquired before dispatching vehicles to prevent double-booking.
3.  **Frontend Resilience:** React Error Boundaries catch rendering errors and display a branded fallback UI without crashing the whole app.
4.  **Database Integrity:** `ondelete="RESTRICT"` and `CASCADE` ensure orphan records are prevented.

---

## 📁 Repository Structure

```text
fleetflow/
├── backend/                # Python FastAPI API
│   ├── app/
│   │   ├── api/            # Route controllers
│   │   ├── core/           # Config and Security context
│   │   ├── db/             # Session, Engine, Setup, Seeding
│   │   ├── models/         # SQLAlchemy 2.0 ORM Models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   └── services/       # Core business logic
│   ├── alembic/            # Database migrations
│   ├── scripts/            # CLI Utilities
│   ├── tests/              # Pytest Suite
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/               # React SPA
│   ├── src/
│   │   ├── api/            # Axios API client integrations
│   │   ├── components/     # Reusable UI components & ErrorBoundary
│   │   ├── pages/          # Full page views
│   │   └── utils/          # Helpers & formatters
│   ├── Dockerfile
│   ├── tailwind.config.js
│   └── package.json
├── docker-compose.yml      # Orchestration
└── README.md
```

---

## 💻 Development Setup (Native)

If you prefer to run services natively without Docker:

### Backend
```bash
cd backend
uv venv .venv
# Activate venv: source .venv/bin/activate (Linux/Mac) or .venv\Scripts\activate (Windows)
uv pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
