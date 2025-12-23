# Documentation map

This repository is standards-driven. Use this map to navigate the docs and keep
changes aligned with the pinned spec baseline.

## Quick entry points

- **Project overview:** `README.md`
- **Continuation plan:** `CHECKLIST.md`
- **Spec baseline:** `SPEC_BASELINE.md` (release-specific URLs)
- **Resource index:** `openehr_am_resources.md`
- **Compatibility promises:** `docs/compatibility.md`
- **Architecture pipeline:** `docs/architecture.md`
- **Security posture:** `SECURITY.md`, `docs/security.md`

## Development references

1. `docs/dev/README.md` — environment setup, pre-commit, and running tests.
2. `docs/dev/parsers.md` — regenerating ANTLR parsers (use the pinned grammar
   commit).
3. `docs/dev/ci.md` — what CI runs (lint, type-check, tests, packaging).

## Validation and rules

- `docs/issue-codes.md` — canonical Issue codes.
- `docs/validation-rule-template.md` — how to add a rule (`# Spec:` URL required).
- `docs/validation_levels.md` — what each validation level guarantees.

## OPT and compilation

- `docs/opt_compilation.md` — OPT pipeline overview.
- `docs/quickstart.md` — CLI/API examples including `compile-opt`.

## Provenance and resources

- `openehr_am_resources.md` — curated spec/tool links.
- `resources/README.md` — provenance policy for fetched artefacts.
- `docs/MAINTENANCE_AUDIT.md` — archive log and current doc inventory.

## Reading order for new contributors (AI-friendly)

1. `SPEC_BASELINE.md` for the exact specs in scope.
2. `README.md` → `docs/quickstart.md` for usage.
3. `docs/architecture.md` for pipeline mental model.
4. `docs/validation_levels.md` + `docs/issue-codes.md` for diagnostics.
5. `docs/dev/parsers.md` + `openehr_am_resources.md` when touching grammars or
   external artefacts.

Keep URLs in docs/code comments aligned to `SPEC_BASELINE.md` (avoid `/latest/`
links in pinned references).
