# FleetFlow: Modular Fleet & Logistics Management System

## Technical Design Document (TDD)

---

## 1. System Overview

FleetFlow is a centralized, rule-driven fleet lifecycle management platform designed to digitize vehicle operations, enforce dispatch compliance, and provide financial observability across assets.

Reference Functional Specification: 

### Architectural Style

**Modular Monolith (Microservices-Ready)**

* Single deployable backend
* Strict module boundaries
* Clear domain separation
* Service layer isolation
* Event-driven internal communication
* Future extraction capability into services (Trips, Analytics, Maintenance)

### Core Design Principles

* Domain-driven modular separation
* Explicit state machines
* Strong relational integrity
* Transaction-safe dispatch logic
* RBAC-enforced access boundaries
* Deterministic recalculation engine
* Observability-first logging

---

## 2. Architecture Diagram (Textual Description)

### Layered Architecture

```
Client Layer (Frontend - SPA)
        ↓
API Layer (REST Controllers)
        ↓
Business Logic Layer (Domain Services)
        ↓
Persistence Layer (ORM + Relational DB)
        ↓
Analytics Layer (Aggregation Engine + Reporting)
```

---

### Client Layer

* SPA Web App
* Role-based UI rendering
* State-managed tables
* Dashboard KPIs
* Form-driven workflows

---

### API Layer

* REST controllers
* Input validation
* Authentication middleware
* RBAC enforcement
* DTO serialization

---

### Business Logic Layer

* Domain services
* State machine validators
* Assignment engine
* Compliance checker
* Cost calculation engine

---

### Persistence Layer

* Relational database
* ORM abstraction
* Transaction manager
* Optimistic locking
* Indexed queries

---

### Reporting / Analytics Layer

* Read-optimized queries
* Aggregation pipelines
* KPI materialized views
* Export generation (CSV/PDF)

---

### Data Flow

1. User submits action (e.g., Create Trip).
2. API validates schema.
3. RBAC middleware verifies role.
4. Business layer checks:

   * Vehicle availability
   * Driver compliance
   * Cargo weight
5. Transaction executes:

   * Insert trip
   * Update vehicle state
   * Update driver state
6. Analytics recalculation triggered.
7. Response returned.

---

## 3. Technology Stack

### Frontend

| Component        | Selection             |
| ---------------- | --------------------- |
| Framework        | React (TypeScript)    |
| State Management | Redux Toolkit         |
| Routing          | React Router          |
| UI Library       | MUI / Tailwind        |
| Form Validation  | React Hook Form + Zod |

---

### Backend

| Component  | Selection             |
| ---------- | --------------------- |
| Language   | TypeScript            |
| Framework  | NestJS                |
| API Style  | REST                  |
| Validation | Zod / class-validator |
| Auth       | JWT                   |

---

### Database

| Component      | Selection      |
| -------------- | -------------- |
| Type           | PostgreSQL     |
| ORM            | Prisma         |
| Migration Tool | Prisma Migrate |

---

### Infrastructure

| Layer         | Assumption                 |
| ------------- | -------------------------- |
| Hosting       | Dockerized Deployment      |
| Environment   | Dev / Staging / Production |
| Reverse Proxy | NGINX                      |
| CI/CD         | GitHub Actions             |
| Secrets       | Environment Variables      |

---

## 4. Module-Level Design

---

### 4.1 Authentication & RBAC

#### Responsibilities

* User login/logout
* JWT issuance
* Role enforcement
* Permission mapping

#### Key Services

* AuthService
* TokenService
* RoleGuard

#### Key APIs

* POST /login
* POST /logout

#### Dependencies

* users table
* roles table

---

### 4.2 Vehicle Management

#### Responsibilities

* Asset registry
* Status lifecycle
* Capacity validation

#### Key Services

* VehicleService
* VehicleStateMachine

#### APIs

* GET /vehicles
* POST /vehicles
* PATCH /vehicles/{id}
* DELETE /vehicles/{id}

#### State Transitions

Available → On Trip
Available → In Shop
Available → Retired
On Trip → Available
In Shop → Available

---

### 4.3 Driver Management

#### Responsibilities

* Compliance enforcement
* Status lifecycle
* Assignment blocking

#### Services

* DriverService
* ComplianceService

#### APIs

* CRUD /drivers
* GET /drivers/{id}/compliance

#### States

On Duty
Off Duty
Suspended

---

### 4.4 Trip Management

#### Responsibilities

* Trip creation
* Dispatch validation
* Lifecycle tracking
* Assignment locking

#### APIs

* POST /trips
* PATCH /trips/{id}/status
* GET /trips

#### State Flow

Draft → Dispatched → Completed
Draft → Cancelled

---

### 4.5 Maintenance Module

#### Responsibilities

* Service logs
* Auto vehicle state update
* Cost tracking

#### APIs

* POST /maintenance
* GET /maintenance

#### Auto-Logic

On creation:
Vehicle → In Shop

---

### 4.6 Expense & Fuel Logging

#### Responsibilities

* Fuel entry
* Expense association
* Cost calculation

---

### 4.7 Analytics Engine

#### Responsibilities

* Fuel efficiency
* ROI
* Cost per km
* Utilization rate

---

### 4.8 Reporting & Export

* CSV generation
* PDF export
* Monthly summary aggregation

---

## 5. Business Rules & State Machine Logic

---

### Vehicle States

| From      | To        | Trigger            |
| --------- | --------- | ------------------ |
| Available | On Trip   | Trip dispatched    |
| On Trip   | Available | Trip completed     |
| Available | In Shop   | Maintenance log    |
| In Shop   | Available | Maintenance closed |
| Available | Retired   | Manual action      |

Blocking:

* Cannot assign if In Shop
* Cannot assign if Retired

---

### Driver States

| From      | To        | Trigger        |
| --------- | --------- | -------------- |
| Off Duty  | On Duty   | Manual toggle  |
| On Duty   | Suspended | Violation      |
| Suspended | Off Duty  | Review cleared |

Blocking:

* Cannot dispatch if Suspended
* Cannot dispatch if license expired

---

### Trip States

| From       | To         |
| ---------- | ---------- |
| Draft      | Dispatched |
| Dispatched | Completed  |
| Draft      | Cancelled  |

Validation:

* CargoWeight ≤ MaxCapacity
* Driver On Duty
* Vehicle Available

---

## 6. API Design

---

### Authentication

#### POST /login

Request:

```json
{
  "email": "manager@fleetflow.com",
  "password": "password123"
}
```

Response:

```json
{
  "accessToken": "jwt-token",
  "role": "MANAGER"
}
```

Validation Error:

```json
{
  "error": "Invalid credentials"
}
```

---

### Vehicles

#### POST /vehicles

```json
{
  "name": "Van-05",
  "model": "Transit 250",
  "licensePlate": "GJ01AB1234",
  "maxCapacityKg": 500,
  "odometerKm": 12000,
  "acquisitionCost": 35000.00
}
```

Response:

```json
{
  "id": 1,
  "status": "Available"
}
```

---

### Trips

#### POST /trips

```json
{
  "vehicleId": 1,
  "driverId": 4,
  "cargoWeightKg": 450,
  "origin": "Warehouse A",
  "destination": "City B"
}
```

Validation Error:

```json
{
  "error": "Cargo exceeds vehicle capacity"
}
```

---

### Analytics

GET /analytics/dashboard

Response:

```json
{
  "activeFleet": 12,
  "maintenanceAlerts": 3,
  "utilizationRate": 0.74
}
```

---

## 7. Database Design

---

### users

| Field         | Type    | Constraints |
| ------------- | ------- | ----------- |
| id            | UUID    | PK          |
| email         | VARCHAR | UNIQUE      |
| password_hash | VARCHAR | NOT NULL    |
| role_id       | UUID    | FK roles    |

---

### roles

| id | UUID | PK |
| name | VARCHAR | UNIQUE (Fleet Manager, Dispatcher, Safety Officer, Financial Analyst) |

---

### vehicles

| id | UUID | PK |
| name | VARCHAR | |
| model | VARCHAR | NOT NULL |
| license_plate | VARCHAR | UNIQUE |
| max_capacity_kg | INT | NOT NULL |
| odometer_km | INT | |
| acquisition_cost | DECIMAL | NOT NULL |
| status | ENUM | INDEX |

---

### drivers

| id | UUID | PK |
| name | VARCHAR | |
| license_number | VARCHAR | UNIQUE |
| license_expiry | DATE | INDEX |
| safety_score | DECIMAL | |
| status | ENUM | INDEX |

---

### trips

| id | UUID | PK |
| vehicle_id | UUID | FK vehicles |
| driver_id | UUID | FK drivers |
| cargo_weight | INT | |
| revenue | DECIMAL | |
| distance_km | DECIMAL | |
| status | ENUM | INDEX |
| start_time | TIMESTAMP | |
| end_time | TIMESTAMP | |

---

### expenses

| id | UUID | PK |
| vehicle_id | UUID | FK vehicles |
| trip_id | UUID | FK trips |
| fuel_liters | DECIMAL | |
| fuel_cost | DECIMAL | |
| date | DATE | |

---

### maintenance_logs

| id | UUID | PK |
| vehicle_id | UUID | FK vehicles |
| type | ENUM | |
| description | TEXT | |
| cost | DECIMAL | |
| date | DATE | |
| odometer_km | INT | |
| status | ENUM | (Open / Completed) |

---

## 8. Calculation Logic

### Fuel Efficiency

```
fuel_efficiency = total_km / total_liters
```

### Total Operational Cost

```
fuel_cost + maintenance_cost
```

### Vehicle ROI

```
(revenue − (maintenance + fuel)) / acquisition_cost
```

### Recalculation Triggers

* Trip completion
* Fuel log entry
* Maintenance entry
* Revenue update

---

## 9. Concurrency & Consistency Strategy

* DB transactions for trip dispatch
* Row-level locking on vehicles
* Unique constraint preventing active trip overlap
* Driver overlapping prevented via:

  * WHERE driver_id AND status='Dispatched'
* Serializable isolation for dispatch operation

---

## 10. Security Design

* Password hashing: bcrypt (12 rounds)
* JWT expiration: 1 hour
* RBAC middleware enforcement
* Input validation on all endpoints
* Audit log table for:

  * State transitions
  * Assignment actions
  * Login attempts

---

## 11. Performance Considerations

* Index on:

  * vehicle.status
  * driver.status
  * trips.status
  * trips.vehicle_id
* Pagination on list endpoints
* Materialized views for analytics
* Query batching

---

## 12. Logging & Monitoring

### Structured Logs

* JSON format
* Request ID
* User ID
* Module name

### Metrics

* Active trips
* Dispatch latency
* Failed dispatch attempts
* API response time

Monitoring via:

* Prometheus
* Grafana dashboards

---

## 13. Deployment Strategy

### Environments

* Dev: Local Docker
* Staging: Cloud container
* Production: Scaled container cluster

### CI/CD

* Lint
* Unit tests
* Build Docker image
* Run migrations
* Deploy

### Migrations

* Versioned
* Zero-downtime strategy
* Backward-compatible schema changes

---

## 14. Assumptions & Technical Constraints

* Single organization tenancy (multi-tenant extension possible)
* Web-based access only
* No IoT telematics integration (future scope)
* Manual odometer updates
* PDF generation server-side
* Real-time updates via polling (WebSockets optional)

---

**End of Technical Design Document**
