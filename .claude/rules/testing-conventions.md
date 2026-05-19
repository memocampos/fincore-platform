---
paths:
  - "tests/**/*"
  - "**/*.test.py"
---

# Testing conventions

- Unit tests (`tests/unit/`) must not touch the database, network, or filesystem — mock at the service boundary.
- Integration tests (`tests/integration/`) use the `db_session` pytest fixture which provides a real Postgres connection inside a rolled-back transaction.
- Test function names follow `test_<action>_<expected_outcome>`, e.g. `test_transfer_insufficient_funds_raises`.
- One logical assertion per test. Use `pytest.raises` for exception cases rather than try/except.
- Financial edge cases to always cover: zero amount, negative amount, maximum integer overflow, mismatched currencies.
- Fixtures that create DB records live in `tests/conftest.py` and are function-scoped by default.
