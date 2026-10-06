# Subsfolio — Reusable Patterns & Conventions

## 1. Mathematical Truth Pattern
- Financial formulas (monthly normalized expense, annual projections) MUST reside in backend Python utility/service functions.
- Billing frequency normalization rules:
  - Monthly: `price`
  - Yearly: `price / 12`
  - Quarterly: `price / 3`
  - Weekly: `price * 52 / 12`
- LLMs are never permitted to compute totals or averages directly from prompts.

## 2. AI Ingestion & Confirmation Pattern
- Never commit AI-extracted data directly to the database.
- AI returns structured Pydantic schema -> frontend displays confirmation review card -> user edits/verifies -> user submits to standard CRUD endpoint.

## 3. Strict User Isolation Pattern
- Every database query for subscriptions, categories, or notifications must filter by `user_id = current_user.id`.
- Handlers extract user identity from validated JWT/session middleware.

## 4. Query Routing Pattern
- Questions regarding user spending, upcoming bills, or active subscriptions -> Route to Backend SQL/Tool functions.
- Questions regarding provider terms, cancellation methods, or refund rules -> Route to RAG provider knowledge base.
