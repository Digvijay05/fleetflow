# phase-1-tasks.md

## Phase 1 Scope
Core Infrastructure & Authentication

---

## 1. Phase Objective
Establish the foundational authentication, database setup, and authorization layers of FleetFlow. Produce a secure, deployment-ready backend with a Postgres database, a functional REST API, and a React frontend shell that enforces Role-Based Access Control (RBAC) across protected routes.

---

## 2. Backend Tasks (Detailed & Atomic)

* **Project Scaffolding**
  * **Description:** Initialize backend repository (Python/FastAPI), configure Ruff and pytest. Setup `pyproject.toml` via `uv`.
  * **Expected Output:** Bootstrapped backend service with local dev server running.
  * **Dependencies:** None

* **Environment Configuration**
  * **Description:** Set up `.env` architecture and a configuration validation module (pydantic-settings) for expected variable types (`DATABASE_URL`, `JWT_SECRET`).
  * **Expected Output:** Environment typed schema mapping.
  * **Dependencies:** Project Scaffolding

* **Database Setup**
  * **Description:** Configure PostgreSQL via local Docker-compose, initialize SQLAlchemy async engine and connect backend.
  * **Expected Output:** Active local relational database connecting logging output to backend.
  * **Dependencies:** Environment Configuration

* **Role Model Creation**
  * **Description:** Write SQLAlchemy ORM schema to construct the `roles` table. 
  * **Expected Output:** ORM schema for roles definition.
  * **Dependencies:** Database Setup

* **User Model Creation**
  * **Description:** Write SQLAlchemy ORM schema to construct the `users` table linked to the `roles` table. Include email, password_hash, and role_id.
  * **Expected Output:** ORM schema for users definition.
  * **Dependencies:** Role Model Creation

* **Initial Migrations**
  * **Description:** Generate Alembic auto-migrations and execute the structural schema upward migration inside the database.
  * **Expected Output:** Live database structural reflection.
  * **Dependencies:** User Model Creation

* **Seed Data**
  * **Description:** Build seed scripts automating insertion of 4 system roles and 1 super-admin testing account.
  * **Expected Output:** Easily re-loadable testing environment state.
  * **Dependencies:** Initial Migrations

* **Password Hashing**
  * **Description:** Utilize `bcrypt` (via passlib) to inject automated salt and hashing cycles intercepting password additions.
  * **Expected Output:** Secure payload transformation helper.
  * **Dependencies:** Project Scaffolding

* **JWT/Session Setup**
  * **Description:** Incorporate PyJWT service enforcing 1-hour expirations containing `user_id` and `role` claims.
  * **Expected Output:** Encrypted string generation helper.
  * **Dependencies:** Environment Configuration

* **Input Validation**
  * **Description:** Architect Pydantic V2 schemas on endpoints preventing malformed traffic processing.
  * **Expected Output:** Standardized 422 Unprocessable Entity error outputs on malformed payload injections.
  * **Dependencies:** Project Scaffolding

* **Login Endpoint**
  * **Description:** Expose `POST /api/v1/auth/login` connecting validation, hashing, database verification, and JWT issuance into an endpoint pipeline.
  * **Expected Output:** Active returning controller logic.
  * **Dependencies:** Input Validation, JWT/Session Setup, Seed Data, Password Hashing

* **RBAC Middleware**
  * **Description:** Implement FastAPI `Depends()` guards, unpack JWT assertions, match current role against route-required credentials, pass or block processing.
  * **Expected Output:** Protected router logic yielding 403 blocks.
  * **Dependencies:** Login Endpoint

* **Basic Logging**
  * **Description:** Inject structured logger configuration.
  * **Expected Output:** Emits organized, timestamped request tracing.
  * **Dependencies:** Project Scaffolding

---

## 3. Frontend Tasks (Detailed & Atomic)

* **Project Scaffolding**
  * **Description:** Initialize frontend repository (React/TypeScript), add Vite or Next.js, set strict Typescript, Prettier, and ESLint configurations.
  * **Expected Output:** Clean template app compiling via `npm run dev` to localhost.
  * **Dependencies:** None

* **Layout System**
  * **Description:** Build the high-level wireframe shell incorporating sidebar, top-navigation bar, and page content canvas. 
  * **Expected Output:** Reusable, responsive application wrapper.
  * **Dependencies:** Project Scaffolding

* **Login Page**
  * **Description:** Map CD variables representing identity visuals to a login panel component capturing email context strings and secret password inputs.
  * **Expected Output:** Visual login gateway view.
  * **Dependencies:** Layout System

* **Form Validation**
  * **Description:** Couple React Hook Form logic and Zod client-schema to prevent submit events failing data cleanliness checks.
  * **Expected Output:** Red-highlighting and inline warnings appearing over fields prior to API transport.
  * **Dependencies:** Login Page

* **API Integration**
  * **Description:** Abstract remote interaction wrapper logic via Axios. Call `POST /api/v1/auth/login` payload logic block.
  * **Expected Output:** Triggering XHR/Fetch external routing events.
  * **Dependencies:** Form Validation

* **Token Storage**
  * **Description:** Capture network response strings and dictate storage (e.g. mapping into `localStorage` or automated HTTP-only cookies).
  * **Expected Output:** JWT persisted effectively through tab regeneration.
  * **Dependencies:** API Integration

* **Auth State Management**
  * **Description:** Launch global memory context (Context API / Redux) broadcasting live truth holding `isLoggedIn` and active user limits.
  * **Expected Output:** Variable accessibility globally to all components.
  * **Dependencies:** Token Storage

* **Role-Based Routing**
  * **Description:** Wrap core application react-router branches parsing global memory Auth States dictating allowable DOM printing.
  * **Expected Output:** Invisible, unreachable component rendering mapped tightly to roles.
  * **Dependencies:** Auth State Management

* **Logout Flow**
  * **Description:** Clear token storage limits and navigate memory to disconnected state upon user toggle.
  * **Expected Output:** Resetted local cache yielding boot sequence to Login.
  * **Dependencies:** Auth State Management

* **Error Handling UI**
  * **Description:** Construct Toast feedback elements interpreting and displaying 4xx and 5xx network rejection codes clearly to user strings.
  * **Expected Output:** Legible UI interaction failure messaging.
  * **Dependencies:** API Integration

---

## 4. Integration Tasks

* **Connect frontend login to backend:** Confirm CORS alignment allowing XHR requests traversing port domains successfully sending valid/invalid payloads to backend schema.
* **Test RBAC:** Confirm backend explicit blocks correctly synchronize mapping into frontend 403 rejection overlays.
* **Validate protected routes:** Bypass attempts directly inputting dashboard URL paths assert correct hard redirects to base login domains.
* **API error mapping:** Confirm backend explicit validation rejections trigger exactly synchronized human readable Toast UI outputs.

---

## 5. Definition of Done (Phase 1)

* Users can log in successfully interacting with verified DB models.
* Roles enforced persistently through backend logic structures protecting payload interactions, and frontend rendering logic hiding unauthorized panes.
* Unauthorized access blocked yielding 401s and 403s respectively.
* Clean code structure verified identically mapped cleanly via linters and static analysis.
* Basic documentation written describing initialization sequences and local docker instantiation.