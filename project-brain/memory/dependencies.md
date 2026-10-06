# Subsfolio — Dependencies

## 1. Frontend Dependencies (Planned Phase 1)
- `next` (^14 or ^15) — React application framework
- `react`, `react-dom` — Core React libraries
- `typescript` — Static type safety
- `tailwindcss`, `postcss`, `autoprefixer` — Utility-first CSS styling
- `lucide-react` — UI icons
- `class-variance-authority`, `clsx`, `tailwind-merge` — Component styling utilities
- `recharts` — Dashboard analytics charts (Phase 4)

## 2. Backend Dependencies (Planned Phase 1)
- `fastapi` — Asynchronous web framework
- `uvicorn[standard]` — ASGI web server
- `pydantic` & `pydantic-settings` — Data validation and environment settings
- `sqlalchemy` — SQL toolkit and ORM
- `alembic` — Database migrations
- `psycopg2-binary` or `asyncpg` — PostgreSQL database driver
- `python-dotenv` — Environment configuration loader

## 3. Implementation Status
- Frontend dependencies installed and verified via `npm install` and Next.js production build (`next build`).
- Backend dependencies configured in `requirements.txt` & `pyproject.toml`, verified via `pytest`.
