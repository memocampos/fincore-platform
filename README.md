# fincore-platform

A FastAPI-based fintech platform providing account management, fund transfers, transaction ledger, and audit logging.

## Features

- **Accounts** — create and manage financial accounts per user
- **Transfers** — atomic fund transfers with `SELECT FOR UPDATE` to prevent race conditions
- **Ledger** — append-only debit/credit transaction pairs linked by a shared `reference_id`
- **Audit log** — immutable entry written in the same transaction as every mutation
- **Authentication** — JWT-based auth enforced on all endpoints via a shared dependency
- **Money safety** — all amounts are integers (cents); the `Money` type enforces this at the boundary

## Stack

- Python 3.11
- FastAPI + Uvicorn
- SQLAlchemy (async) + Alembic
- PostgreSQL

## Getting started

```bash
git clone https://github.com/memocampos/fincore-platform.git
cd fincore-platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set the required environment variables:

| Variable | Description |
|---|---|
| `FINCORE_DATABASE_URL` | Async Postgres URL, e.g. `postgresql+asyncpg://user:pass@localhost/fincore` |
| `FINCORE_JWT_SECRET` | Secret key used to sign and verify JWT tokens |

```bash
alembic upgrade head       # apply migrations
uvicorn main:app --reload  # start dev server
```

API docs: `http://localhost:8000/docs`

## API

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/accounts` | Create a new account |
| `GET` | `/v1/accounts` | List the caller's accounts |
| `GET` | `/v1/accounts/{id}` | Get a single account |
| `POST` | `/v1/transfers` | Initiate a transfer between two accounts |
| `GET` | `/v1/audit` | List audit log entries (filterable by `resource_id`) |
| `GET` | `/health` | Liveness check (no auth required) |

All monetary amounts in requests and responses are integers representing minor currency units (cents).

## Project structure

```
src/
  api/          # FastAPI routers and Pydantic schemas (one file per resource)
  core/         # Domain logic: Money type, ledger transfer, audit writer, exceptions
  models/       # SQLAlchemy ORM models (Account, Transaction, AuditLog)
  services/     # External adapter interfaces: PaymentRailClient, NotificationService
tests/
  unit/         # Pure logic tests — no DB or network
  integration/  # Tests against a real Postgres instance via pytest fixture
```

## Development

```bash
pytest                      # all tests
pytest tests/unit/          # unit tests only
pytest -k "test_transfer"   # filter by name
ruff check src/             # lint
mypy src/                   # type check
```

## Claude Code

This repo includes path-specific rules and custom slash commands:

- `/review-endpoint` — security and schema checklist for new API endpoints
- `/db-migrate` — scaffold and validate an Alembic migration from a model diff

See `CLAUDE.md` for full guidance.
