# Contributing

Thanks for contributing to **pyopenehr-am**.

## Baseline constraints (non-negotiable)

- **Python 3.14+ only**.
- **Pure Python only** (no wrappers around Java/.NET implementations).
- Invalid user input must be handled with structured **Issue** objects (no
  exceptions for recoverable parse/validation failures).
- **Do not** add `from __future__ import annotations` (Python 3.14 has deferred
  annotations by default).

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Test layout (high level):

- `tests/adl/`, `tests/odin/`, `tests/antlr/`, `tests/aom/`,
  `tests/validation/`, `tests/cli/`, `tests/meta/`

Optional lint:

```bash
ruff check .
```

## Issue codes policy

Diagnostics use stable Issue codes registered in:

- `docs/issue-codes.md`

When adding a new validation rule or diagnostic:

- Allocate a new code in `docs/issue-codes.md` _before_ using it.
- Add tests that assert the code is emitted.

## Spec provenance policy

This project is standards-driven. New validation rules must include a short spec
reference comment of the form:

```python
# Spec: https://specifications.openehr.org/releases/.../<doc>.html
```

The pinned spec baseline is maintained in:

- `SPEC_BASELINE.md`

Spec baseline changes require a **minor version bump**.

## Generated code

Parser output under `openehr_am/_generated/` (ANTLR) is committed. Do not edit
generated files by hand.

## Style and scope

- Keep diffs small and focused.
- Prefer deterministic algorithms; treat ADL/ODIN/BMM input as untrusted.
- If you add public API, keep it small and stable.
