---
context: fork
allowed-tools:
  - Read
  - Bash
  - Grep
---

# /review-endpoint

Reviews a new or modified API endpoint for security, schema correctness, and fincore conventions.

## Steps

1. Read the target router file provided by the user (or the most recently modified file under `src/api/`).
2. Check each endpoint for:
   - **Auth**: `get_current_user` dependency is present on every route.
   - **Input validation**: all path/query/body parameters have explicit types; no `Any` or bare `dict`.
   - **Money fields**: amounts are `int` (cents), not `float`. Field descriptions state the currency unit.
   - **Error codes**: 409 for business conflicts, 404 for not-found, never raw 500 from domain exceptions.
   - **Response model**: `response_model` is set and `response_model_exclude_none=True` is present.
   - **No direct DB access**: router only calls `src/core/` functions.
3. Run `ruff check <file>` and `mypy <file>` and include any findings.
4. Output a checklist: ✅ for passing items, ❌ with a one-line fix for failing items.
