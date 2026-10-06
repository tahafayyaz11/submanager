# Recent Context

## Current Status
- Phase 2 Core Subscription Management Complete:
  - Database: SQLAlchemy `Subscription` model deployed to live Neon PostgreSQL via Alembic migration `27abfb355e8e_create_subscriptions_table.py`.
  - Schema & Types: Decimal + `Numeric(10,2)` price, 3-letter currency code, `ARRAY(Integer)` reminder days, check constraints.
  - Identity & Security: Temporary development user resolution isolated inside `get_current_user_id()`. Falls back to `DEV_USER_ID` strictly in development; raises 401 Unauthorized outside development.
  - Services & API: Full CRUD in `SubscriptionService` and FastAPI router `/api/v1/subscriptions` (and root `/subscriptions`).
  - Delete Behavior: Soft-archive (`status="archived"`) without hard delete.
  - Automated Tests: 13 of 13 Pytest tests passing (`test_health.py`, `test_subscriptions.py`).
  - Frontend UI: `/subscriptions` page, `SubscriptionForm`, `SubscriptionList`, typed client `lib/api.ts`.
  - Static & Production Verification: ESLint clean, TypeScript clean (`tsc --noEmit`), Next.js production build (`next build`) passing.
- Ready for Phase 3 (Authentication with Clerk / Supabase / Neon Auth).

