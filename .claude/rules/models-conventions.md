---
paths:
  - "src/models/**/*"
  - "alembic/versions/**/*"
---

# Models & migrations conventions

- ORM models inherit from `Base` and `TimestampMixin` (both in `src/models/base.py`).
- Column names use snake_case. Boolean columns are prefixed `is_` or `has_`.
- All foreign keys must have an explicit `ondelete` policy (`CASCADE` or `RESTRICT`).
- Index names follow `ix_<table>_<column(s)>`. Unique constraint names follow `uq_<table>_<column(s)>`.
- Alembic migration messages use imperative mood: `add user_id to transactions`, not `added` or `adding`.
- Every migration must be reversible: the `downgrade()` function must undo `upgrade()` completely.
