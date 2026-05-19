---
context: fork
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
---

# /db-migrate

Scaffolds an Alembic migration from the current model diff and validates it against fincore rules.

## Steps

1. Run `alembic revision --autogenerate -m "<message from user>"` to generate the migration file.
2. Read the generated file in `alembic/versions/`.
3. Validate:
   - `downgrade()` is not a no-op — it must reverse every operation in `upgrade()`.
   - No `drop_table` or `drop_column` on financial tables (`accounts`, `transactions`, `audit_log`). If found, stop and warn the user that a lead review is required.
   - All new columns on existing tables have a `server_default` or are nullable (required for zero-downtime deploys).
   - Index and constraint names follow the `ix_<table>_<col>` / `uq_<table>_<col>` convention.
4. If validation passes, print the migration path and a summary of changes.
5. If validation fails, list each violation with a suggested fix and do not leave the file in place.
