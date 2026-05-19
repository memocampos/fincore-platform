# fincore-platform

A FastAPI-based fintech platform providing account management, fund transfers, transaction ledger, and audit logging.

## Features

- **Accounts** — create and manage financial accounts
- **Transfers** — initiate and validate fund transfers between accounts
- **Ledger** — append-only record of every debit and credit
- **Audit log** — immutable audit entry written atomically with every mutation
- **Authentication** — JWT-based auth on all endpoints
- **Money safety** — all amounts stored as integers (cents) to eliminate float errors

## Stack

- Python 3.11
- FastAPI + Uvicorn
- SQLAlchemy (async) + Alembic
- PostgreSQL

## Getting started

```bash
# Clone and set up the environment
git clone https://github.com/memocampos/fincore-platform.git
cd fincore-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and set FINCORE_DATABASE_URL and other required vars

# Run migrations
alembic upgrade head

# Start the development server
uvicorn main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## Project structure

```
src/
  api/        # FastAPI routers (one file per resource)
  core/       # Domain logic — no HTTP or DB dependencies
  models/     # SQLAlchemy ORM models and Alembic migrations
  services/   # External integrations (payment rails, notifications)
tests/
  unit/       # Pure logic tests, no DB or network
  integration/# Tests against a real Postgres instance
```

## Development

```bash
pytest                        # run all tests
pytest tests/unit/            # unit tests only
pytest -k "test_transfer"     # filter by name
ruff check src/               # lint
mypy src/                     # type check
```

## Claude Code

This repo is configured for Claude Code with path-specific rules and custom skills:

- `/review-endpoint` — security and schema checklist for API endpoints
- `/db-migrate` — scaffold and validate an Alembic migration

See `CLAUDE.md` for full guidance.
