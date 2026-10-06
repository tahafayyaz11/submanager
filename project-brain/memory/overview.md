# Subsfolio — Project Overview

## 1. Project Summary
Subsfolio is an AI-powered subscription intelligence, management, analytics, and renewal-tracking SaaS platform. It acts as an intelligent financial assistant specifically designed for recurring subscriptions.

## 2. Core Vision & Goals
- Centralized tracking of recurring subscriptions and renewal dates.
- Advance renewal alerts to prevent unwanted recurring charges.
- Precise deterministic calculations for monthly and annual spending.
- AI-assisted subscription extraction from emails, receipts, and invoices (with human confirmation).
- Natural language query assistant grounded in database figures and verified provider policies.
- Identifying overlapping/duplicate subscriptions.

## 3. Technology Stack
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS, shadcn/ui.
- **Backend**: Python, FastAPI, Pydantic, SQLAlchemy, Alembic.
- **Database**: PostgreSQL (pgvector for future RAG).
- **Authentication**: Clerk or Supabase Auth (TBD during Phase 3).
- **Background Jobs**: Simple backend scheduler initially (Celery + Redis later).
- **Notifications**: Resend (email first).
- **AI Integrations**: OpenAI API / Gemini API (direct SDK initially; LangGraph for complex agent orchestration later).

## 4. Current Status
- **Current Phase**: Phase 1 — Project Foundation
- **Implementation Status**:
  - `project-brain`: Initialized
  - `frontend`: Scaffold pending (Phase 1)
  - `backend`: Scaffold pending (Phase 1)
  - `database`: Configuration pending (Phase 1)
