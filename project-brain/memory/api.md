# Subsfolio — API Specification

## 1. Protocol & Conventions
- RESTful HTTP API with JSON payloads.
- Authentication: Bearer token header (`Authorization: Bearer <token>`).
  - Supports local Subsfolio JWT tokens (email/password).
  - Supports Clerk session JWT tokens with claims validation and automatic user auto-provisioning into PostgreSQL.
- User scoping: All protected routes enforce `get_current_user_id()` derived strictly from validated tokens. No client-supplied user IDs accepted.

## 2. Planned API Endpoints

### Authentication (Phase 3)
- `POST /api/v1/auth/signup` — Register new user account (returns JWT token and User profile)
- `POST /api/v1/auth/login` — Authenticate user credentials (returns JWT token and User profile)
- `GET /api/v1/auth/me` — Retrieve profile of currently authenticated user (`Authorization: Bearer <token>`)
- Root alias `/auth` mounted for direct access.

### Subscriptions (Phase 2 & 3)
- `POST /api/v1/subscriptions` — Create subscription (scoped strictly to `get_current_user_id()`)
- `GET /api/v1/subscriptions` — List subscriptions for user (supports `status` query filter)
- `GET /api/v1/subscriptions/{id}` — Get single subscription by ID (scoped to user, 404 for other tenants)
- `PUT /api/v1/subscriptions/{id}` & `PATCH /api/v1/subscriptions/{id}` — Update subscription fields
- `DELETE /api/v1/subscriptions/{id}` — Soft-archive subscription (sets `status='archived'`, no hard delete)
- Root alias `/subscriptions` mounted for direct access.

### Analytics (Future Phase 4)
- `GET /api/v1/analytics/overview` — Monthly & annual spending totals, counts
- `GET /api/v1/analytics/categories` — Spending aggregated by category

### AI Services (Future Phase 6 & 7)
- `POST /api/v1/ai/extract` — Extract subscription details from text/receipt
- `POST /api/v1/ai/chat` — Natural-language query interface with database tools

## 3. Implementation Status
- `GET /health` (root health check) — Implemented & active.
- `GET /api/v1/health` (versioned health check) — Implemented & active.
- `GET /api/v1/health/detailed` (database diagnostic health check) — Implemented & active.
- Subscription CRUD endpoints (`POST`, `GET`, `PUT`, `DELETE` archive) fully implemented and covered by automated tests.
- Phase 3 Authentication endpoints (`POST /auth/signup`, `POST /auth/login`, `GET /auth/me`) fully implemented with bcrypt, JWT token signing, and complete tenant isolation coverage.

