# Subsfolio — API Specification

## 1. Protocol & Conventions
- RESTful HTTP API with JSON payloads.
- Authentication: Bearer token header (`Authorization: Bearer <token>`).
- User scoping: All protected routes enforce `current_user.id`.

## 2. Planned API Endpoints

### Subscriptions
- `POST /api/v1/subscriptions` — Create subscription (scoped to `get_current_user_id()`)
- `GET /api/v1/subscriptions` — List subscriptions for user (supports `status` query filter)
- `GET /api/v1/subscriptions/{id}` — Get single subscription by ID (scoped to user)
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

