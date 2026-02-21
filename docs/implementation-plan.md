# implementation-plan.md

## 1. Overview

**Project Summary**
FleetFlow is a centralized, modular, rule-based fleet and logistics management system designed to digitize operational, compliance, and financial lifecycles of delivery fleets.

**Development Strategy**
The development strategy utilizes a modular, milestone-based approach focusing on vertical slices. Frontend and backend development will proceed in parallel, decoupled via clear API contracts defined in the TDD. 

**Assumptions**
* Single organization deployment (no multi-tenancy in MVP).
* Web-based UI only.
* Internet connectivity is persistently available for operations.
* Infrastructure will use Dockerized containers for isolated testing and deployment.

---

## 2. Phase Breakdown

### Phase 0 – Project Setup & Architecture Foundation

#### Phase Overview
* **Goals:** Establish repositories, CI/CD pipelines, environment configurations, and base architectural scaffolding.
* **Deliverables:** Empty runnable frontend and backend services, database connected, linting/formatting enforced.
* **Dependencies:** None.

#### Backend Scope
* **APIs:** Health check endpoint (`GET /health`).
* **Database Tables:** None.
* **Business Rules:** Standardize formatting and logging.
* **State Logic:** N/A.
* **Validation Rules:** N/A.
* **Migrations:** Initial baseline schema setup.

#### Frontend Scope
* **Pages/components:** Scaffold React/TypeScript app.
* **State Management:** Setup Redux Toolkit and React Router.
* **Forms:** N/A.
* **Tables:** N/A.
* **UI validation:** N/A.
* **Role-based visibility:** N/A.

#### Exit Criteria
* Both services run locally via `docker-compose up`.
* CI pipeline passes on pushed code (linting, build).
* Integration validation with basic health check.

---

### Phase 1 – Core Infrastructure & Authentication

#### Phase Overview
* **Goals:** Implement Identity & Access Management (IAM) and Role-Based Access Control (RBAC).
* **Deliverables:** Secure login system, JWT generation, and protected routes based on roles (Fleet Manager, Dispatcher, Safety Officer, Financial Analyst).
* **Dependencies:** Phase 0.

#### Backend Scope
* **APIs:** `POST /login`, `POST /logout`.
* **Database Tables:** `users`, `roles`.
* **Business Rules:** Password hashing (bcrypt), JWT expiration (1 hour).
* **State Logic:** User authentication state.
* **Validation Rules:** Request body validation via Pydantic.
* **Migrations:** Create users and roles tables via Alembic, seed roles and super-admin user.

#### Frontend Scope
* **Pages/components:** Login UI, Layout framework (Sidebar, Header).
* **State Management:** Auth state (token storage).
* **Forms:** Login form.
* **Tables:** N/A.
* **UI validation:** Email format, password presence.
* **Role-based visibility:** Protected route wrappers checking JWT roles.

#### Exit Criteria
* Users can authenticate successfully.
* API test coverage confirms unauthorized access returns 401/403.
* UI completion of login flow.

---

### Phase 2 – Vehicle & Driver Management

#### Phase Overview
* **Goals:** Build the core asset and personnel registry.
* **Deliverables:** Vehicle and Driver management modules enabling users to populate the system.
* **Dependencies:** Phase 1.

#### Backend Scope
* **APIs:** CRUD operations for `/vehicles` and `/drivers`.
* **Database Tables:** `vehicles`, `drivers`.
* **Business Rules:** License plate uniqueness, license expiry validation.
* **State Logic:** Available (vehicle), On Duty (driver).
* **Validation Rules:** Valid capacity limits, valid dates.
* **Migrations:** Add `vehicles` and `drivers` schemas.

#### Frontend Scope
* **Pages/components:** Vehicle Registry, Driver Profiles.
* **State Management:** Registry lists mapped to tables.
* **Forms:** Add/Edit Vehicle, Add/Edit Driver.
* **Tables:** Vehicle list, Driver list.
* **UI validation:** Required fields, numeric bounds.
* **Role-based visibility:** Read/Write restrictions based on Manager/Safety roles.

#### Exit Criteria
* Full CRUD operations work for Vehicles and Drivers.
* State toggles correctly update database status.
* Integration validation linking UI to backend storage safely.

---

### Phase 3 – Trip Management & Dispatch Logic

#### Phase Overview
* **Goals:** Implement the core workflow engine for dispatching trips.
* **Deliverables:** Trip dispatcher module with complex validation and state tracking.
* **Dependencies:** Phase 2.

#### Backend Scope
* **APIs:** `POST /trips`, `PATCH /trips/{id}/status`, `GET /trips`.
* **Database Tables:** `trips`.
* **Business Rules:** Capacity constraint (`cargo_weight <= vehicle.max_capacity_kg`).
* **State Logic:** Draft → Dispatched → Completed. Modifies Vehicle and Driver status.
* **Validation Rules:** Prevent dispatch if Vehicle/Driver is unavailable or if capacity is exceeded.
* **Migrations:** Add `trips` table with foreign keys.

#### Frontend Scope
* **Pages/components:** Trip Dispatcher & Management.
* **State Management:** Dynamic vehicle/driver availability.
* **Forms:** Trip creation form.
* **Tables:** Active/Historical trips tracking.
* **UI validation:** Cross-field validation (cargo vs capacity).
* **Role-based visibility:** Dispatcher capabilities.

#### Exit Criteria
* Trips progress through full lifecycle.
* Vehicle and driver states transition correctly upon trip dispatch and completion.
* Backend prevents invalid assignments.

---

### Phase 4 – Maintenance & Expense Modules

#### Phase Overview
* **Goals:** Enable tracking of vehicle-specific maintenance and trip-specific fuel logs.
* **Deliverables:** Maintenance logging interface and expense aggregator.
* **Dependencies:** Phase 2, Phase 3.

#### Backend Scope
* **APIs:** CRUD for `/maintenance_logs` and `/expenses`.
* **Database Tables:** `maintenance_logs`, `expenses`.
* **Business Rules:** Maintenance sets vehicle out of dispatch pool.
* **State Logic:** Maintenance additions change Vehicle to `In Shop`.
* **Validation Rules:** Validate cost and dates.
* **Migrations:** Add `maintenance_logs` and `expenses` tables.

#### Frontend Scope
* **Pages/components:** Maintenance Logs, Expense/Fuel Logging.
* **State Management:** Expense and log tracking.
* **Forms:** Insert log, Insert expense.
* **Tables:** Service records, Fuel records.
* **UI validation:** Linked resources exist.
* **Role-based visibility:** Fleet Manager limits.

#### Exit Criteria
* Maintenance logs trigger correct vehicle state transitions.
* API test coverage on logic overrides.
* UI reflects maintenance overrides cleanly.

---

### Phase 5 – Analytics & Reporting

#### Phase Overview
* **Goals:** Render operational metrics and financial observability.
* **Deliverables:** Command Center Dashboard and static reports.
* **Dependencies:** Phases 1-4.

#### Backend Scope
* **APIs:** `GET /analytics/dashboard`, `GET /analytics/reports`.
* **Database Tables:** Materialized views (optional) for speed.
* **Business Rules:** Calculate Fuel Efficiency, Cost per km, and ROI.
* **State Logic:** Recalculations triggered on trip/expense/maintenance updates.
* **Validation Rules:** Valid date bounds for reports.
* **Migrations:** Analytical views indexing.

#### Frontend Scope
* **Pages/components:** Command Center Dashboard, Analytics Page.
* **State Management:** Read-only metric fetching.
* **Forms:** Data filters (date range, specific asset filters).
* **Tables:** Breakdown metrics.
* **UI validation:** Export actions.
* **Role-based visibility:** Visible strictly to Managers/Analysts.

#### Exit Criteria
* Dashboard accurately reflects database states.
* ROI and metrics match predefined formulas.
* UI correctly renders visual charts.

---

### Phase 6 – Hardening, Optimization & Deployment

#### Phase Overview
* **Goals:** Prepare system for production traffic and finalize CI/CD.
* **Deliverables:** Production candidate release, load testing results, security audits.
* **Dependencies:** Phases 1-5.

#### Backend Scope
* **APIs:** Hardened endpoints with rate-limiting.
* **Database Tables:** Indexes optimized.
* **Business Rules:** Secure connections enforced.
* **State Logic:** Validated edge cases.
* **Validation Rules:** Strict payload sanitization.
* **Migrations:** Applied to staging db.

#### Frontend Scope
* **Pages/components:** Error boundaries, 404 views.
* **State Management:** Optimized rendering.
* **Forms:** Double submission blocks.
* **Tables:** Virtualized list rendering.
* **UI validation:** Accessibility enhancements.
* **Role-based visibility:** Rigorously tested.

#### Exit Criteria
* Functional verification passes all test suites.
* High API test coverage (> 85%).
* Integration deployment on staging runs without errors.

---

## 3. Timeline Estimation

* **Phase 0:** Week 1
* **Phase 1:** Week 2
* **Phase 2:** Week 3
* **Phase 3:** Weeks 4 - 5
* **Phase 4:** Week 6
* **Phase 5:** Week 7
* **Phase 6:** Week 8
* **Total Estimated Timeline:** 8 Weeks

---

## 4. Risk Areas

* **Concurrency Conflicts:** Two dispatchers assigning the same vehicle simultaneously. Requires DB row-level locking or serializable isolation.
* **State Inconsistencies:** Process crash between marking trip 'completed' and freeing the driver. Requires strict atomic transactions.
* **Data Integrity Risks:** Dangling references if entities are not soft-deleted. Requires constraints preventing hard deletions of active assets.
* **Reporting Complexity:** Large datasets joining trips, vehicles, expenses rendering slowly. Requires caching or materialized views as database size grows.

---

## 5. Deployment Milestones

* **Dev Ready:** End of Week 3 (Phases 0-2 complete; Core, IAM, Asset creation).
* **Staging Ready:** End of Week 5 (Phases 3-4 complete; Full operational logic deployed).
* **Production Candidate:** End of Week 8 (Analytics, optimizations, fully verified logic deployed).
