---
name: Testing standards
description: Standards for pytest tests
applyTo: "tests/**/*.py"
---
# Testing standards

- Use `pytest`.
- Prefer small, targeted tests (one behavior per test).
- Always include:
  - happy path
  - malformed input path
  - validation issue assertions (Issue codes + locations if available)
- Keep fixtures small; store larger samples in `tests/fixtures/`.
