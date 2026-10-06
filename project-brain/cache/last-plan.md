# Implementation Plan — Phase 2: Core Subscription Management

## 1. Task Classification
- **Type**: Domain Feature & CRUD Implementation
- **Phase**: Phase 2 — Core Subscription Management
- **Complexity**: Moderate
- **Objective**: Establish the core Subscription data model in PostgreSQL (Neon), Alembic migration, Pydantic schemas, Service/Repository layer, REST API endpoints, and a functional Next.js management UI.

## 2. Affected Modules
- `Database` (PostgreSQL / Neon schema & Alembic migration)
- `BackendAPI` (FastAPI endpoints, dependency injection)
- `SubscriptionModule` (Model, Schemas, Service layer)
- `FrontendApp` (Next.js `/subscriptions` route, CRUD components, API client)

## 3. Proposed Database Schema
Table: `subscriptions`
- `id`: UUID (Primary Key, default `uuid.uuid4`)
- `user_id`: VARCHAR(128) (Indexed, foreign-key ready for Phase 3 auth)
- `service_name`: VARCHAR(100) (NOT NULL)
- `plan_name`: VARCHAR(100) (NULLABLE)
- `price`: NUMERIC(10, 2) (NOT NULL, check constraint: `price >= 0`)
- `currency`: VARCHAR(3) (NOT NULL, default `'USD'`)
- `billing_cycle`: VARCHAR(20) (NOT NULL, values: `monthly`, `yearly`, `quarterly`, `weekly`)
- `purchase_date`: DATE (NULLABLE)
- `renewal_date`: DATE (NOT NULL, indexed)
- `category`: VARCHAR(50) (NOT NULL, default `'Other'`)
- `payment_method`: VARCHAR(50) (NULLABLE)
- `reminder_days_before`: JSON (NOT NULL, default `[7, 3, 1]`)
- `notes`: TEXT (NULLABLE)
- `status`: VARCHAR(20) (NOT NULL, default `'active'`, values: `active`, `cancelled`, `archived`, `paused`)
- `created_at`: TIMESTAMPTZ (NOT NULL, server_default `now()`)
- `updated_at`: TIMESTAMPTZ (NOT NULL, server_default `now()`, onupdate `now()`)

Indexes:
- `ix_subscriptions_user_id` on (`user_id`)
- `ix_subscriptions_renewal_date` on (`renewal_date`)
- `ix_subscriptions_status` on (`status`)

## 4. Proposed API Structure
Base Path: `/api/v1/subscriptions` (and root `/subscriptions` mounted)

- `POST /api/v1/subscriptions`
  - Status: 201 Created
  - Request: `SubscriptionCreate`
  - Response: `SubscriptionResponse`
- `GET /api/v1/subscriptions`
  - Status: 200 OK
  - Query params: `skip: int = 0`, `limit: int = 100`, `status: Optional[str] = None`
  - Response: `List[SubscriptionResponse]`
- `GET /api/v1/subscriptions/{id}`
  - Status: 200 OK (or 404 Not Found)
  - Response: `SubscriptionResponse`
- `PUT /api/v1/subscriptions/{id}`
  - Status: 200 OK (or 404 Not Found)
  - Request: `SubscriptionUpdate`
  - Response: `SubscriptionResponse`
- `DELETE /api/v1/subscriptions/{id}`
  - Status: 200 OK (or 204 No Content)
  - Query param: `hard_delete: bool = False` (default soft-archives by setting `status = 'archived'`)
  - Response: `SubscriptionResponse` or `{"message": "Subscription deleted successfully"}`

## 5. Proposed Backend Folder Changes
```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py         # Registers Subscription model for Alembic
│   │   └── subscription.py     # SQLAlchemy 2.0 Subscription model
│   ├── schemas/
│   │   ├── __init__.py         # Exports schemas
│   │   └── subscription.py     # Pydantic v2 schemas (Create, Update, Response)
│   ├── services/
│   │   ├── __init__.py
│   │   └── subscription.py     # SubscriptionService (CRUD, query filtering)
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py     # Includes subscriptions router
│   │       └── subscriptions.py# FastAPI router endpoints
│   └── core/
│       └── deps.py             # get_current_user_id dependency
├── alembic/
│   └── versions/
│       └── <hash>_create_subscriptions_table.py
└── tests/
    └── test_subscriptions.py   # Full CRUD pytest test suite
```

## 6. Proposed Frontend Changes
```
frontend/
├── app/
│   └── subscriptions/
│       └── page.tsx            # Subscriptions management page
├── components/
│   ├── SubscriptionForm.tsx    # Create & Edit modal/form
│   ├── SubscriptionList.tsx    # List/Table of subscriptions
│   └── DeleteDialog.tsx        # Delete/Archive confirmation dialog
└── lib/
    └── api.ts                  # Typed client fetch wrapper for /api/v1/subscriptions
```

## 7. user_id Strategy Before Authentication Exists
- Temporary development-only identity mechanism isolated strictly inside `backend/app/core/deps.py`:
  ```python
  from fastapi import Header, HTTPException, status
  from typing import Optional
  from app.core.config import settings

  def get_current_user_id(x_user_id: Optional[str] = Header(None)) -> str:
      """
      Temporary development-only user identity resolver.
      1. Reads explicit X-User-Id request header if provided.
      2. If missing and APP_ENV == 'development', falls back to settings.DEV_USER_ID.
      3. Outside development, never falls back: raises 401 Unauthorized if no identity provided.
      Will be replaced in Phase 3 with JWT validation (Clerk / Supabase) without touching domain or service layers.
      """
      if x_user_id and x_user_id.strip():
          return x_user_id.strip()

      if settings.APP_ENV == "development" and settings.DEV_USER_ID:
          return settings.DEV_USER_ID

      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Authentication required. Provide X-User-Id header during development."
      )
  ```
- Environment configuration:
  - Add `DEV_USER_ID=dev-user-0001` to `.env` and `.env.example`.
  - Add `DEV_USER_ID: Optional[str] = None` to `app.core.config.Settings`.
- Guardrails:
  - Zero hard-coded user IDs in Python code.
  - No silent fallback outside development (`APP_ENV != "development"` raises 401).
  - All database queries and mutations continue to strictly filter by `user_id == current_user_id`.
  - Clean drop-in replacement in Phase 3.

## 8. Migration Strategy
1. Register `Subscription` model on `Base.metadata`.
2. Generate migration via Alembic:
   `alembic revision --autogenerate -m "create_subscriptions_table"`
3. Inspect and verify the generated Python migration script.
4. Execute `alembic upgrade head` against live Neon PostgreSQL.
5. Verify schema directly on Neon via a ping query.

## 9. Testing Strategy
- **Database & Migration Tests**:
  - Run `alembic upgrade head`.
  - Validate table and columns in Neon PostgreSQL.
- **Backend API Tests** (`pytest backend/tests/test_subscriptions.py`):
  - `test_create_subscription`: Verify 201 Created and response attributes.
  - `test_get_subscriptions`: Verify list returns created subscriptions.
  - `test_get_subscription_by_id`: Verify 200 OK for valid ID.
  - `test_update_subscription`: Verify field changes persist (e.g. price, renewal date).
  - `test_delete_subscription`: Verify delete / soft-archive.
  - `test_validation_errors`: Verify negative price, missing name, or invalid cycle return HTTP 422.
  - `test_not_found`: Verify querying non-existent UUID returns HTTP 404.
- **Frontend Validation**:
  - `npx tsc --noEmit` (TypeScript check, zero errors).
  - `npm run lint` (ESLint check, zero warnings/errors).
  - Next.js build validation.
  - End-to-end form submission, listing, editing, and deleting against running backend.

## 10. Risks & Mitigation
- **Risk**: Price precision loss if floating point numbers are used.
  - **Mitigation**: Use Python `Decimal` in Pydantic and `Numeric(10, 2)` in SQLAlchemy/PostgreSQL.
- **Risk**: Timezone ambiguities on renewal dates.
  - **Mitigation**: Use Python `datetime.date` for `renewal_date` and `purchase_date` without time component, and timezone-aware `TIMESTAMPTZ` for audit timestamps.
- **Risk**: Stale Neon connection during migration.
  - **Mitigation**: Pool pre-ping configured; unpooled connection string available if needed for DDL.

## 11. Files That Will Be Created or Modified
- Backend:
  - `backend/app/models/subscription.py` (New)
  - `backend/app/models/__init__.py` (Modified)
  - `backend/app/schemas/subscription.py` (New)
  - `backend/app/schemas/__init__.py` (Modified)
  - `backend/app/core/deps.py` (New)
  - `backend/app/services/subscription.py` (New)
  - `backend/app/services/__init__.py` (Modified)
  - `backend/app/api/v1/subscriptions.py` (New)
  - `backend/app/api/v1/__init__.py` (Modified)
  - `backend/alembic/versions/*_create_subscriptions_table.py` (New)
  - `backend/tests/test_subscriptions.py` (New)
- Frontend:
  - `frontend/lib/api.ts` (New)
  - `frontend/components/SubscriptionForm.tsx` (New)
  - `frontend/components/SubscriptionList.tsx` (New)
  - `frontend/app/subscriptions/page.tsx` (New)
  - `frontend/app/page.tsx` (Modified to link to `/subscriptions`)
- Project Brain:
  - `project-brain/cache/last-plan.md` (Updated)
  - `project-brain/memory/database.md` (Updated)
  - `project-brain/memory/api.md` (Updated)
  - `project-brain/memory/backend.md` (Updated)
  - `project-brain/memory/frontend.md` (Updated)
  - `project-brain/graph/graph.json` (Updated)
  - `project-brain/tasks/completed.md` (Updated)
  - `project-brain/tasks/changelog.md` (Updated)

## 12. Implementation Order
1. Define SQLAlchemy model `backend/app/models/subscription.py` and register in `backend/app/models/__init__.py`.
2. Generate and apply Alembic migration (`alembic revision --autogenerate`, `alembic upgrade head`) to Neon PostgreSQL.
3. Define Pydantic validation schemas in `backend/app/schemas/subscription.py`.
4. Implement `get_current_user_id` dependency in `backend/app/core/deps.py`.
5. Implement `SubscriptionService` in `backend/app/services/subscription.py`.
6. Implement FastAPI endpoints in `backend/app/api/v1/subscriptions.py` and register in API router.
7. Write and run automated test suite in `backend/tests/test_subscriptions.py`.
8. Create frontend API client and components: `lib/api.ts`, `SubscriptionForm.tsx`, `SubscriptionList.tsx`, and `app/subscriptions/page.tsx`.
9. Run static validation (TypeScript `tsc`, ESLint `lint`, Next.js build).
10. Verify end-to-end runtime operations.
11. Update Project Brain memory, graph, tasks, and cache.
