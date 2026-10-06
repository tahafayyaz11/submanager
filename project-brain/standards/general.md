# Subsfolio — Engineering Standards

## 1. General Principles
- **Separation of Concerns**: Strict boundary between UI, API, Domain Services, and Database.
- **Minimal Complexity**: Avoid premature abstractions or unneeded infrastructure.
- **Safety First**: Never perform financial calculations in untrusted environments (e.g. LLM prompts).
- **Zero Hallucination**: Financial data originates purely from database queries.

## 2. Backend Standards (Python / FastAPI)
- **Typing & Linting**: Strict type annotations on all function signatures and returns.
- **Data Validation**: Use Pydantic v2 schemas for all request payloads and response bodies.
- **Error Handling**: Use standard FastAPI HTTPException with structured error details.
- **Security**: Authenticate and verify user ownership (`user_id`) on every data mutation and retrieval.
- **Database Access**: Use SQLAlchemy ORM with scoped sessions; never raw unparameterized SQL.

## 3. Frontend Standards (Next.js / TypeScript / React)
- **TypeScript**: Strict mode enabled, no implicit `any`.
- **Component Architecture**: Small, focused components; separation between UI components and data fetching.
- **Styling**: Tailwind CSS with consistent utility classes; accessible UI primitives via shadcn/ui.
- **State Management**: Predictable state, avoid prop-drilling.

## 4. Testing & Validation
- Unit and integration tests for critical business logic (e.g. billing calculations, renewal scheduling).
- Static validation must pass (linting, type checking, build) before code review.
