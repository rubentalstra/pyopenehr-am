# Development

This project is **pure Python only** and targets **Python 3.14+ only**.

## Setup

```bash
pip install -e ".[dev]"
```

## Pre-commit (recommended)

Install the git hooks:

```bash
pre-commit install
```

Run the hooks across all files:

```bash
pre-commit run --all-files
```

By default, Ruff runs on each commit and `pytest` runs on `pre-push`.

## Tests

```bash
pytest
```

## Test layout

The test suite is grouped by subsystem to keep it navigable as the project
grows:

- `tests/adl/` — ADL parsing + syntax AST
- `tests/odin/` — ODIN parsing/transform/roundtrip
- `tests/antlr/` — ANTLR runtime glue (error listeners, spans)
- `tests/aom/` — AOM models + builder
- `tests/validation/` — validation layers (syntax/semantic) + Issue machinery
- `tests/cli/` — CLI rendering/UX
- `tests/meta/` — repo-level invariants (imports, issue-code registry,
  generated-code sanity)

Shared helpers and fixtures:

- `tests/fixture_loader.py`
- `tests/fixtures/`

Running a subset (examples):

```bash
pytest -q tests/validation
pytest -q tests/adl
```
