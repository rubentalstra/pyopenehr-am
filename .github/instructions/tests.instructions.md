---
name: Testing standards
description: pytest conventions, fixtures, corpus tests
applyTo: "tests/**/*.py"
---
# Testing standards

## General
- Use `pytest`.
- One behavior per test.
- Assert Issue codes and deterministic ordering.

## Fixtures
- Keep fixtures small and readable.
- Use `tests/fixtures/adl/` and `tests/fixtures/odin/` for artefact text.
- Add a corpus harness later under `tests/corpus/`.

## CLI tests
- Use Typer's testing utilities.
- Always test `--json` output is valid JSON and contains Issue objects.
