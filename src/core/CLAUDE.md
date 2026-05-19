# Core Domain

Pure business logic. No FastAPI, no HTTP concerns, no external I/O.

- Functions accept and return domain objects (dataclasses or Pydantic models), not ORM instances.
- All mutations must be wrapped in a transaction and write to `audit_log` atomically.
- Raise domain exceptions (defined in `core/exceptions.py`) — never raise HTTP exceptions here.
- Money arithmetic uses the `Money` value object. Never add/subtract raw integers directly.
