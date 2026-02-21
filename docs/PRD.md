# FleetFlow: Modular Fleet & Logistics Management System

**Product Requirements Document (PRD)**

---

## 1. Executive Summary

### Product Vision

FleetFlow is a modular, rule-based fleet and logistics management system designed to digitize and optimize the operational, compliance, and financial lifecycle of delivery fleets. It replaces manual logbooks and fragmented spreadsheets with a centralized digital command center.

### Problem Statement

Fleet operators currently face:

* Manual tracking of vehicles and drivers
* Lack of real-time visibility into fleet availability
* Inefficient dispatch workflows
* Poor maintenance planning
* Inconsistent compliance monitoring
* Inaccurate cost and ROI calculations per vehicle

These issues lead to:

* Increased downtime
* Regulatory risk
* Fuel inefficiencies
* Financial opacity
* Reduced asset lifespan

### Solution Overview

FleetFlow provides:

* Centralized asset registry
* Rule-based dispatch validation
* Real-time vehicle and driver state management
* Automated maintenance state transitions
* Compliance enforcement (license expiry blocks)
* Operational cost tracking per vehicle
* Financial analytics with exportable reports

### Expected Impact

* 15–25% increase in fleet utilization
* 20% reduction in unplanned downtime
* 100% automated compliance enforcement
* Accurate cost-per-km visibility
* Data-driven asset replacement decisions

---

## 2. Goals & Success Metrics

| Goal                        | KPI                                 | Target                    |
| --------------------------- | ----------------------------------- | ------------------------- |
| Increase fleet efficiency   | Fleet Utilization Rate              | ≥ 85%                     |
| Reduce downtime             | Maintenance Downtime Reduction      | ≥ 20%                     |
| Enforce compliance          | License Compliance Enforcement Rate | 100%                      |
| Optimize operational cost   | Cost per km reduction               | ≥ 10%                     |
| Improve capital performance | ROI per Vehicle                     | Positive within 12 months |

### KPI Definitions

* **Fleet Utilization Rate**
  [
  \frac{\text{Vehicles On Trip}}{\text{Total Active Vehicles}} \times 100
  ]

* **Fuel Efficiency**
  [
  \text{Fuel Efficiency} = \frac{\text{Distance (km)}}{\text{Fuel (L)}}
  ]

* **Vehicle ROI**
  [
  \frac{\text{Revenue - (Maintenance + Fuel)}}{\text{Acquisition Cost}}
  ]

---

## 3. Target Users & Personas

### 3.1 Fleet Managers

**Responsibilities:**

* Asset lifecycle management
* Maintenance oversight
* Vehicle availability tracking
* Strategic decision-making

**System Interactions:**

* Manage Vehicle Registry
* Log Maintenance
* View Analytics Dashboard
* Toggle vehicle service status

---

### 3.2 Dispatchers

**Responsibilities:**

* Create and manage trips
* Assign vehicles and drivers
* Validate cargo load limits

**System Interactions:**

* Access Dispatch Page
* View available vehicles
* Assign drivers
* Track trip lifecycle

---

### 3.3 Safety Officers

**Responsibilities:**

* Monitor driver compliance
* Track license expiry
* Enforce driver suspension

**System Interactions:**

* View Driver Profiles
* Update driver status
* Monitor compliance dashboard

---

### 3.4 Financial Analysts

**Responsibilities:**

* Audit expenses
* Track fuel costs
* Calculate ROI
* Generate reports

**System Interactions:**

* View analytics reports
* Export CSV/PDF
* Monitor cost per vehicle

---

## 4. Functional Requirements (Page-by-Page)

---

## Page 1: Login & Authentication

### Features

* Email & Password login
* Forgot Password (email reset link)
* Role-Based Access Control (RBAC)

### Roles

* Fleet Manager
* Dispatcher
* Safety Officer
* Financial Analyst

### Requirements

* Secure hashed passwords
* Session-based authentication
* Role-restricted page access
* Unauthorized access returns HTTP 403

---

## Page 2: Command Center Dashboard

### KPIs Displayed

* Active Fleet (vehicles "On Trip")
* Maintenance Alerts ("In Shop")
* Utilization Rate (%)
* Pending Cargo (unassigned trips)

### Filters

* Vehicle Type
* Status
* Region

### UI Requirements

* Status pills (Available / On Trip / In Shop / Retired)
* Real-time updates
* Data refresh every 5 seconds

---

## Page 3: Vehicle Registry (Asset Management)

### CRUD Operations

* Create vehicle
* Edit vehicle
* Soft-delete (Retired toggle)

### Fields

| Field            | Type    | Constraint                              |
| ---------------- | ------- | --------------------------------------- |
| id               | UUID    | Primary Key                             |
| name             | String  | Required                                |
| model            | String  | Required                                |
| license_plate    | String  | Unique, Required                        |
| max_capacity_kg  | Decimal | Required                                |
| odometer_km      | Decimal | Required                                |
| acquisition_cost | Decimal | Required                                |
| status           | Enum    | Available / On Trip / In Shop / Retired |

### Logic

* If Retired → Hidden from dispatch pool
* License plate must be unique

---

## Page 4: Trip Dispatcher & Management

### Trip Creation Form

Fields:

* Origin
* Destination
* Cargo Weight
* Vehicle
* Driver
* Estimated Distance
* Revenue

### Validation Rules

* `CargoWeight <= Vehicle.MaxCapacity`
* Vehicle.Status = Available
* Driver.Status = On Duty
* Driver.License not expired

If validation fails → prevent dispatch

### Trip Lifecycle

* Draft
* Dispatched
* Completed
* Cancelled

### State Transitions

| Action   | Result                       |
| -------- | ---------------------------- |
| Dispatch | Vehicle & Driver → On Trip   |
| Complete | Vehicle & Driver → Available |
| Cancel   | No state change              |

---

## Page 5: Maintenance & Service Logs

### Features

* Add maintenance entry
* Preventative / Reactive type
* Cost entry

### Logic

* Adding service log:

  * Vehicle.Status → In Shop
  * Remove from dispatch pool

* Mark service completed:

  * Vehicle.Status → Available

### Fields

* Vehicle ID (FK)
* Service Type
* Description
* Cost
* Date
* Odometer

---

## Page 6: Completed Trip, Expense & Fuel Logging

### Fuel Log Fields

* Vehicle ID
* Trip ID
* Fuel Liters
* Fuel Cost
* Date

### Calculation

Total Operational Cost per Vehicle:

[
\text{Fuel Cost} + \text{Maintenance Cost}
]

Auto-recalculated after each new entry.

---

## Page 7: Driver Performance & Safety Profiles

### Fields

| Field                | Description                    |
| -------------------- | ------------------------------ |
| License Expiry Date  | Required                       |
| Status               | On Duty / Off Duty / Suspended |
| Trip Completion Rate | Auto-calculated                |
| Safety Score         | Configurable metric            |

### Rules

* If License expired:

  * Driver automatically suspended
  * Cannot assign to new trip

* Suspended drivers:

  * Removed from dispatch pool

---

## Page 8: Operational Analytics & Financial Reports

### Metrics

* Fleet Utilization
* Fuel Efficiency (km/L)
* Cost per km
* Vehicle ROI

### Export Options

* CSV
* PDF
* Monthly payroll report
* Audit report

### Reporting Filters

* Date range
* Vehicle
* Driver
* Region

---

## 5. System Logic & Workflow

### 1. Vehicle Intake

* Manager adds vehicle
* Status = Available
* Added to dispatch pool

### 2. Driver Compliance Verification

* Add driver
* System validates:

  * License expiry
  * Category compatibility

If expired → Status = Suspended

---

### 3. Dispatch Logic Validation

Before dispatch:

* Vehicle.Status == Available
* Driver.Status == On Duty
* CargoWeight <= MaxCapacity
* Driver license valid

If all pass:

* Vehicle.Status → On Trip
* Driver.Status → On Trip

---

### 4. Trip Completion

On completion:

* Update final odometer
* Vehicle.Status → Available
* Driver.Status → On Duty
* Trigger analytics recalculation

---

### 5. Maintenance Override

When service log added:

* Vehicle.Status → In Shop
* Hidden from dispatch

On service completion:

* Vehicle.Status → Available

---

### 6. Analytics Recalculation

Triggers:

* Trip completion
* Fuel log addition
* Maintenance cost entry

System recalculates:

* Cost per km
* ROI
* Utilization metrics

---

## 6. Non-Functional Requirements

### Performance

* Dashboard load time < 2 seconds
* Real-time state updates < 1 second latency

### Scalability

* Support 10,000+ vehicles
* Horizontal scaling for backend

### Data Integrity

* ACID compliance
* Foreign key enforcement
* Transactional updates for state transitions

### Security

* Encrypted passwords (bcrypt)
* JWT/session-based auth
* Role-based authorization
* Audit logs for critical actions

### Availability

* 99.9% uptime target

---

## 7. Technical Architecture Overview

### Frontend

* Modular component-based UI
* Dynamic data tables
* Status indicators
* Real-time state refresh
* Role-based rendering

---

### Backend

* RESTful API
* Real-time availability engine
* Business rule enforcement layer
* Transaction-safe state transitions

---

### Database

Relational database (PostgreSQL recommended)

### Core Entities

* Vehicles
* Drivers
* Trips
* MaintenanceLogs
* Expenses
* Users

---

### High-Level ER Model

* One Vehicle → Many Trips
* One Driver → Many Trips
* One Vehicle → Many MaintenanceLogs
* One Trip → Many Expenses
* Users linked to Roles

---

## 8. Data Model Definitions

---

### Vehicles

* id (PK)
* license_plate (Unique)
* max_capacity_kg
* odometer_km
* status
* acquisition_cost

---

### Drivers

* id (PK)
* name
* license_number
* license_expiry
* status
* safety_score

---

### Trips

* id (PK)
* vehicle_id (FK → Vehicles.id)
* driver_id (FK → Drivers.id)
* cargo_weight
* status
* revenue
* distance_km
* start_time
* end_time

Constraints:

* cargo_weight <= vehicle.max_capacity_kg

---

### MaintenanceLogs

* id (PK)
* vehicle_id (FK)
* type
* description
* cost
* date
* odometer_km
* status

---

### Expenses

* id (PK)
* vehicle_id (FK)
* trip_id (FK)
* fuel_liters
* fuel_cost
* date

---

### Users (RBAC)

* id (PK)
* email (Unique)
* password_hash
* role (Enum)

---

## 9. Assumptions & Constraints

* Internet connectivity required
* Vehicles do not have real-time GPS in MVP
* Manual odometer entry required
* Revenue entered manually per trip
* Compliance rules configurable

Constraints:

* No telematics integration in Phase 1
* Single organization per deployment
* No multi-tenant architecture initially

---

## 10. Future Enhancements

* GPS integration
* Real-time telematics
* Predictive maintenance (ML-based)
* AI route optimization
* Automated fuel anomaly detection
* Multi-tenant SaaS support
* Mobile driver application
* IoT sensor integration

---

**End of Document**
