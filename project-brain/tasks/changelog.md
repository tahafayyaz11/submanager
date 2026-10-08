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

## [Unreleased] - Phase 3 Authentication & User Ownership Isolation

### Added
- **Data Model & Migrations**:
  - Defined SQLAlchemy 2.0 `User` model with String(128) ID (supporting both UUID and Clerk user IDs), unique indexed email, bcrypt hashed password (nullable for SSO/Clerk), full name, avatar URL, active status, and timestamps.
  - Generated and executed Alembic migration `5feaad396f25_create_users_table.py` against live Neon PostgreSQL database.
- **Core Security & Cryptography**:
  - `backend/app/core/security.py` with bcrypt salt generation & verification, and PyJWT token generation and claim decoding.
  - Configured JWT settings (`JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`) and Clerk environment bindings.
- **Service & API Endpoints**:
  - `UserService` in `backend/app/services/user.py` handling registration, credential authentication, duplicate email prevention, and external Clerk SSO sync.
  - Endpoints under `/api/v1/auth` and root `/auth` for `/signup`, `/login`, and `/me`.
  - Upgraded `get_current_user` and `get_current_user_id` dependencies in `backend/app/core/deps.py` enforcing Bearer JWT token validation with user ownership isolation across all subscription endpoints.
- **Frontend Authentication Architecture**:
  - `AuthProvider` and `useAuth` hook in `frontend/lib/auth-context.tsx` managing JWT tokens, user profiles, persistent storage, and automatic session restoration.
  - Top `Navbar` component with brand navigation, active user chip, and Sign Out action.
  - `/login` page with email/password form, show/hide password toggle, Clerk readiness badge, and 1-click Demo Account switchers (Alice vs Bob) for testing multi-user isolation.
  - `/signup` page with client-side validation, password match verification, and automatic redirect to dashboard.
  - Upgraded `/subscriptions` page displaying live tenant isolation status and authentic token propagation.
- **Testing & Verification**:
  - Automated tests in `backend/tests/test_auth.py` verifying signup, duplicate email prevention, login, invalid password rejection, `/me` profile retrieval, and cross-user tenant isolation (User A cannot view, edit, or archive User B's subscriptions).
  - All 19 pytest tests passing (100% pass rate).
  - Next.js production build (`npm run build`) passing with zero errors.

### Clerk Authentication Integration
- Linked Clerk application `app_3KNcbw5uhM7VcS1DfaCN6zllJc8` using Clerk CLI.
- Installed `@clerk/nextjs` (v6) and `@clerk/themes`.
- Wrapped Next.js App Router in `<ClerkProvider appearance={{ baseTheme: dark }}>`.
- Implemented `middleware.ts` with `clerkMiddleware()` and `createRouteMatcher`:
  - Protects non-public routes (`/subscriptions`, `/dashboard`, etc.) with `307 Redirect` to `/sign-in`.
  - Public routes permitted: `/`, `/sign-in(.*)`, `/sign-up(.*)`, `/login(.*)`, `/signup(.*)`.
- Implemented Clerk authentication routes: `/sign-in/[[...sign-in]]` and `/sign-up/[[...sign-up]]`.
- Added Clerk UI controls (`SignInButton`, `SignUpButton`, `UserButton`, `SignedIn`, `SignedOut`) in `Navbar` and hero sections with modal auth trigger mode.
- Passed `clerk doctor` verification with 100% green checkmarks.


