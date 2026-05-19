---
paths:
  - "src/api/**/*"
---

# API conventions

- Router files are named after the resource in plural snake_case: `accounts.py`, `transfers.py`.
- Use `APIRouter(prefix="/v1/<resource>", tags=["<Resource>"])` at the top of every router.
- All path parameters that represent financial resource IDs must be typed `uuid.UUID`.
- Paginated list endpoints accept `limit: int = Query(50, le=200)` and `cursor: str | None = None`.
- Never expose internal model IDs or database row counts in responses.
- Add `response_model_exclude_none=True` to every endpoint decorator to keep responses clean.
