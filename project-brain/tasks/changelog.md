# Project Changelog

## [Unreleased] - Phase 1 Foundation

### Initialized
- Project Brain repository memory structure (`memory/`, `graph/`, `standards/`, `reviews/`, `tasks/`, `cache/`).
- Documented Subsfolio product vision, technical stack, architecture guardrails, and roadmap.

### Added - Phase 1 Foundation
- Scaffolding for FastAPI backend (`core`, `db`, `models`, `schemas`, `services`, `api/v1`).
- Implemented `GET /health` and `GET /api/v1/health` with database ping diagnostics.
- Configured SQLAlchemy 2.0 ORM engine, sessionmaker, and Alembic migrations.
- Configured CORS middleware between Next.js (port 3000) and FastAPI (port 8000).
- Scaffolding for Next.js 14 frontend with React 18, TypeScript, Tailwind CSS, and shadcn/ui readiness (`components.json`, `lib/utils.ts`).
- Created full-stack verification page in `frontend/app/page.tsx` testing the Browser → Next.js → FastAPI → PostgreSQL connection pipeline.
- Added root environment templates (`.env.example`, `.env`), comprehensive `.gitignore`, and detailed `README.md`.
- Automated test suite `tests/test_health.py` passing with 100% test success.
- Configured `.eslintrc.json`, installed ESLint toolchain, and resolved hook dependency warnings for zero-warning static analysis.
- Completed runtime verification of Phase 1 foundation (Next.js server, FastAPI server, health endpoints, CORS, database ping).
- Integrated Neon serverless PostgreSQL: linked project `subsfolio` (`royal-star-77346519`), branch `production`.
- Installed Neon agent skills (`.agents/skills/neon*`) and configured Neon MCP server for IDE agents.
- Configured root `neon.ts`, installed `@neon/config` & `@neon/env`, and deployed configuration.
- Verified live PostgreSQL database connectivity passing (`database_connected: true`).

## [Unreleased] - Phase 2 Core Subscription Management

### Added
- **Data Model & Migrations**:
  - Defined SQLAlchemy 2.0 `Subscription` model with PostgreSQL `UUID` primary key, `String(128)` user indexing, `Decimal`/`Numeric(10,2)` price, 3-letter currency, `ARRAY(Integer)` reminder days, and check constraints (`price >= 0`, valid billing cycle, valid status).
  - Generated and executed Alembic migration `27abfb355e8e_create_subscriptions_table.py` against live Neon PostgreSQL database.
- **Pydantic Schemas**:
  - `SubscriptionCreate`, `SubscriptionUpdate`, and `SubscriptionResponse` with Decimal precision validation, 3-letter uppercase ISO currency regex validation, and reminder day array normalization.
- **Isolated User Identity Resolver**:
  - `get_current_user_id` in `backend/app/core/deps.py`: accepts `X-User-Id` header, falls back to `settings.DEV_USER_ID` strictly when `APP_ENV == "development"`, and enforces 401 Unauthorized outside development with zero silent fallbacks to a shared production user.
- **Service & API Endpoints**:
  - `SubscriptionService` in `backend/app/services/subscription.py` with strict user-scoping for `create`, `get_by_id`, `get_multi`, `update`, and `archive`.
  - Soft-archive deletion logic (`status="archived"`) without hard delete.
  - Endpoints under `/api/v1/subscriptions` and root alias `/subscriptions` for `POST`, `GET`, `PUT`, `PATCH`, `DELETE`.
- **Automated Test Suite**:
  - Pytest suite `tests/test_subscriptions.py` testing creation, listing, detail retrieval, updates, soft-archiving, validation errors, 404 handling, cross-user data isolation, and production 401 security guardrail. 13 of 13 tests passing.
- **Frontend Management UI**:
  - Next.js `/subscriptions` route with subscription cards/list, status filtering (`active`, `archived`, `all`), and live dev user switching.
  - `SubscriptionForm` modal dialog with comprehensive field inputs and client-side validation.
  - `SubscriptionList` component with intuitive status chips, price/cycle formatting, and edit/archive actions.
  - Typed client `lib/api.ts` wrapping all REST endpoints with error handling.
  - Navigation link added from home dashboard to `/subscriptions`.
  - Zero ESLint errors, zero TypeScript errors (`tsc --noEmit`), and production build passing (`next build`).


