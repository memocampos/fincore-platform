"""
fincore-platform — entry point for the FastAPI application.

Functionalities:
  - Account management    : create, retrieve, and list financial accounts (src/api/accounts.py)
  - Transfers             : initiate and validate fund transfers between accounts (src/api/transfers.py)
  - Transaction ledger    : append-only record of every debit/credit (src/core/ledger.py)
  - Audit logging         : immutable audit_log entry written atomically with every mutation (src/core/audit.py)
  - Authentication        : JWT-based auth enforced via get_current_user dependency (src/api/dependencies.py)
  - Money value object    : all amounts are integers (cents) via the Money type to prevent float errors (src/core/money.py)
  - ORM models            : SQLAlchemy models with UUID PKs and TimestampMixin (src/models/)
  - Alembic migrations    : reversible schema migrations; financial tables are append-only (alembic/)
  - External services     : payment rail and notification integrations isolated in src/services/
  - MCP servers           : Postgres, filesystem, and GitHub MCP servers configured in .mcp.json
  - Path-specific rules   : per-directory coding conventions loaded automatically via .claude/rules/
  - Custom skills         : /review-endpoint and /db-migrate slash commands in .claude/skills/
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB connection pool on startup; dispose on shutdown.
    # Engine is created lazily so tests can swap it before the app starts.
    from src.models.base import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="fincore-platform",
    version="0.1.0",
    # Disable the default /docs in production via the FINCORE_ENV env var.
    docs_url="/docs",
    lifespan=lifespan,
)

# Restrict origins in production via the FINCORE_ALLOWED_ORIGINS env var.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

# Each router owns exactly one resource; see src/api/CLAUDE.md for conventions.
from src.api.accounts import router as accounts_router
from src.api.transfers import router as transfers_router
from src.api.audit import router as audit_router

app.include_router(accounts_router)
app.include_router(transfers_router)
app.include_router(audit_router)


@app.get("/health", tags=["ops"])
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    # Use `uvicorn main:app --reload` during development instead of running this directly.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
