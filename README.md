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
* TypeScript
* NestJS
* REST API
* Zod / class-validator
* JWT Authentication

### Database
* PostgreSQL
* Prisma ORM

## Setup Instructions

*(Coming Soon)*

## Folder Structure

```
fleetflow/
├── backend/                # NestJS API
│   ├── src/                # Source code
│   ├── tests/              # Test suite
│   └── config/             # Environment configurations
├── frontend/               # React SPA
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   └── pages/          # View logic
├── docs/                   # Engineering Planning Documents
│   ├── PRD.md              # Product Requirements Document
│   ├── TDD.md              # Technical Design Document
│   ├── CDB.md              # Creative Design Brief
│   ├── implementation-plan.md
│   └── phase-1-tasks.md
├── docker-compose.yml      # Local development cluster
└── README.md
```

## Development Workflow

1. Fork/Clone the repository.
2. Ensure Docker is running.
3. Start the services using `docker-compose up` (once available).

## License

MIT License
