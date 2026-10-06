# Subsfolio — Architecture & System Design

## 1. System Design & Layers
Subsfolio strictly follows a 4-tier separation of concerns:
```
User Interface (Next.js)
        ↓
API Gateway & Controllers (FastAPI)
        ↓
Domain Services & Business Logic (Python)
        ↓
Data Layer (PostgreSQL + SQLAlchemy ORM) & External APIs (AI / Resend / Google)
```

## 2. Core Architectural Guardrails
1. **Deterministic Financial Math**: Monthly/yearly aggregations and renewal calculations are executed exclusively in backend service code, never guessed or calculated by LLMs.
2. **AI with Human-in-the-Loop**: AI-extracted subscriptions from receipts/emails are staged and require explicit user confirmation before insertion into the database.
3. **Data Ownership & Isolation**: Every subscription and resource is scoped strictly by `user_id`. Cross-user access is prohibited at the API and database query levels.
4. **Provider-Doc RAG vs Database Routing**: Structured queries query PostgreSQL; questions about provider cancellation/refund policies query the RAG vector store.
5. **No Premature Optimization / Simplicity First**:
   - Direct LLM calls prior to introducing LangGraph.
   - Built-in lightweight scheduler prior to Celery + Redis.
   - PostgreSQL + pgvector prior to dedicated vector databases.

## 3. Implementation Status
- System architecture designed.
- Codebase scaffolding pending for Next.js, FastAPI, and PostgreSQL.
