# Models & Migrations

SQLAlchemy ORM models and Alembic migrations.

- Every model must have `created_at` and `updated_at` columns (use the `TimestampMixin`).
- Primary keys are UUIDs, not auto-increment integers.
- Financial tables (`accounts`, `transactions`) are append-only — no `UPDATE` or `DELETE` in migrations.
- After changing a model, generate a migration with `/db-migrate` rather than writing one by hand.
- Migration files must not contain `drop_table` or `drop_column` for financial tables without a lead engineer review.
