# Subsfolio — Database Architecture & Schema

## 1. Engine & Migrations
- **Engine**: PostgreSQL
- **Migration Tool**: Alembic
- **Extensions**: `pgvector` (planned for Phase 9 RAG)

## 2. Planned Tables & Models
- `users`: User identity and credentials/OAuth mapping.
- `subscriptions`:
  - `id` (UUID / Integer, Primary Key)
  - `user_id` (Foreign Key -> users.id, indexed)
  - `service_name` (String, required)
  - `plan_name` (String, optional)
  - `price` (Numeric / Float, required)
  - `currency` (String, default USD/PKR)
  - `billing_cycle` (Enum: monthly, yearly, quarterly, weekly)
  - `renewal_date` (Date, indexed)
  - `category` (String / Enum)
  - `payment_method` (String, optional)
  - `reminder_days_before` (Integer / Array, default [7, 3, 1])
  - `is_active` (Boolean, default True)
  - `notes` (Text, optional)
  - `created_at`, `updated_at` (Timestamps)
- `notifications`: History of dispatched renewal notices.
- `ai_requests`: Observability log for tokens, latency, cost.
- `rag_documents` & `rag_chunks`: Knowledge base for cancellation/refund policies (pgvector).

## 3. Implementation Status
- Engine (`app.db.session.engine`), `SessionLocal`, `Base` (`app.db.base.Base`), and `get_db` dependency initialized.
- Live Neon PostgreSQL integration linked: Project `subsfolio` (`royal-star-77346519`), branch `production`.
- Live database connectivity verified passing (`database_connected: true`).
- Alembic migrations initialized and executed:
  - Revision `27abfb355e8e_create_subscriptions_table.py` deployed to Neon PostgreSQL.
  - Revision `5feaad396f25_create_users_table.py` deployed to Neon PostgreSQL:
    - Table `users` created with columns: `id` (VARCHAR 128 PK, UUID/Clerk ID compatible), `email` (VARCHAR 255 UNIQUE, indexed), `hashed_password` (VARCHAR 255, nullable for SSO/Clerk), `full_name`, `avatar_url`, `is_active`, `created_at`, `updated_at`.
  - Table `subscriptions` active with constraints:
    - `ck_subscription_positive_price` (`price >= 0`)
    - `ck_subscription_billing_cycle` (`monthly`, `yearly`, `quarterly`, `weekly`)
    - `ck_subscription_status` (`active`, `cancelled`, `archived`, `paused`)
    - Indexes on `user_id`, `renewal_date`, and `status`.
    - Column types: `Decimal` / `NUMERIC(10,2)` for price, `VARCHAR(3)` currency, `ARRAY(Integer)` for `reminder_days_before`.
- Health check ping, subscription CRUD, and auth user isolation verified passing against live database.

