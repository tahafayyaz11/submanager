# Subsfolio

AI-powered subscription intelligence, management, analytics, and renewal-tracking platform.

---

## Technical Stack (Phase 1 Foundation)
- **Frontend**: Next.js 14+ (App Router), React, TypeScript, Tailwind CSS, shadcn/ui ready.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic.
- **Database**: PostgreSQL.

---

## Directory Structure
```
submanager/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/v1/          # Route handlers (Health, etc.)
│   │   ├── core/            # App settings and environment config
│   │   ├── db/              # SQLAlchemy session & Base
│   │   ├── models/          # ORM data models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic services
│   │   └── main.py          # FastAPI entrypoint & middleware
│   ├── alembic/             # Database migrations
│   ├── tests/               # Test suites
│   ├── requirements.txt     # Python dependencies
│   └── pyproject.toml
├── frontend/                 # Next.js Application
│   ├── app/                 # Next.js App Router (pages & layouts)
│   ├── components/ui/       # UI components (shadcn/ui compatible)
│   ├── lib/                 # Shared utilities
│   └── package.json
├── project-brain/            # Architecture memory, graph & pipeline
├── .env.example              # Environment variables template
└── README.md
```

---

## Getting Started

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- PostgreSQL 14+ (running locally or remotely)

### 2. Environment Configuration
Copy `.env.example` to `.env` in the root directory:
```bash
cp .env.example .env
```
Ensure `DATABASE_URL` points to your PostgreSQL instance.

### 3. Backend Setup
Navigate to the backend directory, install dependencies, and run:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Verify the backend health check:
- `http://localhost:8000/health` -> `{"status": "ok"}`
- Interactive API Docs: `http://localhost:8000/docs`

Run tests:
```bash
pytest
```

### 4. Database Migrations (Alembic)
Apply migrations:
```bash
cd backend
alembic upgrade head
```

### 5. Frontend Setup
Navigate to the frontend directory, install dependencies, and run:
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the application and test live connectivity to the backend.
