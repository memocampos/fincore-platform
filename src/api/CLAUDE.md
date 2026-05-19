# API Layer

Routers live here. Each router owns one resource (e.g. `accounts.py`, `transfers.py`).

- Request/response models use Pydantic v2. Define them in the same file as the router unless shared.
- Routers call `src/core/` functions only — no direct DB queries here.
- All endpoints require authentication via the `get_current_user` dependency.
- Return `422` for validation errors (Pydantic handles this automatically), `409` for business rule conflicts, `404` for missing resources.
- Monetary amounts in JSON are always integers (cents). Document the currency unit in the field description.
