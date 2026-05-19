# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`fincore-platform` is a Python 3.11 fintech platform. Virtual environment is at `.venv/`.

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Commands

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/unit/test_accounts.py

# Run tests matching a name pattern
pytest -k "test_transfer"

# Lint
ruff check src/
ruff format src/

# Type check
mypy src/

# Run the API server locally
uvicorn src.api.main:app --reload
```

## Architecture

```
src/
  api/        # FastAPI routers and request/response schemas
  core/       # Domain logic: accounts, transactions, ledger
  models/     # SQLAlchemy ORM models and Alembic migrations
  services/   # External integrations (payment rails, notifications)
tests/
  unit/       # Pure logic tests, no DB or network
  integration/# Tests against a real DB (use pytest-docker fixture)
```

### Key invariants

- All money values are stored as integers (cents / minor currency units). Never use `float`.
- Every state-changing operation must write an immutable audit entry to the `audit_log` table before returning.
- `src/core/` must not import from `src/api/` or `src/services/`. Dependency direction: `api → core ← services`.

## Path-specific rules

Additional conventions load automatically when you edit files in specific directories — see `.claude/rules/`.

## Custom skills

Project slash commands are in `.claude/skills/`. Available:
- `/review-endpoint` — security and schema review for a new API endpoint
- `/db-migrate` — scaffold an Alembic migration from a model diff
