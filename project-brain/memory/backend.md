# Subsfolio — Backend Architecture

## 1. Stack & Structure
- **Framework**: FastAPI (Python 3.11+)
- **Validation**: Pydantic v2
- **Data Access**: SQLAlchemy 2.0 (Async/Sync ORM)
- **Directory Layout (Target)**:
  - `app/main.py` — Application entrypoint & CORS middleware
  - `app/api/` — API routers (/subscriptions, /analytics, /ai, /notifications)
  - `app/core/` — Configuration, settings, security, dependencies
  - `app/models/` — SQLAlchemy database models
  - `app/schemas/` — Pydantic request & response models
  - `app/services/` — Business logic (calculations, reminders, AI extraction)
  - `app/db/` — Database connection session setup & Alembic migrations

## 2. Core Business Logic & Services
- `SubscriptionService`: CRUD operations scoped strictly by user identity. Soft-archives on delete.
- `UserService`: User creation with bcrypt hashing, credential authentication, and external Clerk SSO sync.
- `get_current_user` & `get_current_user_id`: Dependencies isolated in `core/deps.py` supporting `Authorization: Bearer <token>`, Clerk token inspection, and development fallback. Raises 401 Unauthorized outside development when unauthenticated.
- `AnalyticsService` (Planned Phase 4): Deterministic monthly/annual spending aggregation and category breakdown.
- `ReminderEngine` (Planned Phase 5): Scan upcoming renewals against preferences and dispatch reminders.
- `AIExtractorService` (Planned Phase 6): Parse unstructured text/receipts into validated Pydantic schemas.

## 3. Implementation Status
- Phase 1 Foundation implemented: FastAPI application structured into `core/`, `db/`, `models/`, `schemas/`, `services/`, and `api/v1/`.
- Phase 2 Subscription Management implemented:
  - SQLAlchemy `Subscription` model with check constraints, UUID primary key, Decimal/Numeric(10,2) price, and ARRAY(Integer) reminder days.
  - Pydantic v2 schemas: `SubscriptionCreate`, `SubscriptionUpdate`, `SubscriptionResponse`.
  - `SubscriptionService` with user-scoped create, get, list, update, and soft-archive methods.
  - REST endpoints mounted under `/api/v1/subscriptions` and root alias `/subscriptions`.
- Phase 3 Authentication & User Isolation implemented:
  - SQLAlchemy `User` model with String(128) ID (supporting both UUID and Clerk IDs), unique email, bcrypt hash, and timestamps.
  - Pydantic v2 schemas: `UserCreate`, `UserLogin`, `UserResponse`, `TokenResponse`.
  - Core security module `app/core/security.py` with bcrypt hashing and PyJWT token creation/decoding.
  - Endpoints `/api/v1/auth/signup`, `/api/v1/auth/login`, and `/api/v1/auth/me`.
  - Automated tests passing in Pytest: 19/19 passing (`test_health.py`, `test_subscriptions.py`, `test_auth.py`).

