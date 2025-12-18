# AGENTS — pyopenehr-am (Python 3.14+)

These instructions apply to _all_ AI agents working in this repository.

## What we’re building

A **pure-Python** openEHR AM toolkit that other developers embed to build their
own legacy→openEHR migration logic.

This repo provides reusable primitives:

- Parse **ADL2** archetypes/templates and embedded **ODIN**
- Build an **AOM2** semantic object model
- Validate: syntax, AOM2 semantics, RM conformance via **BMM**
- Compile templates into **OPT2** (Operational Templates)
- (Later) validate instance data against OPT

Internal pipeline: **Parse → Build AOM → Validate → Compile OPT → (Optional)
Validate Instances**

## Target runtime (important)

- **Python 3.14+ only**.
- Avoid `from __future__ import annotations` because it opts out of 3.14’s
  default deferred-annotation semantics.
- If annotation introspection is required, use
  `annotationlib.get_annotations()`.

## Non-negotiables

- **Pure Python only**: no wrapping non-Python reference implementations, no
  JPype/JNI.
- **Diagnostics**: return structured `Issue` objects for all recoverable
  problems (no exceptions for invalid artefacts).
- **Spec provenance**: new rules must include a short `# Spec: <URL>` comment
  and a stable Issue code.

## Developer workflows (expected)

- Run tests: `pytest`
- Lint: `ruff check .` and `ruff format .` (generated code excluded)
- Type-check: `pyright` (or `mypy` if chosen)

## Generated parser code (ANTLR)

Policy:

- Grammar sources live in `grammars/`.
- Generated Python code lives in `openehr_am/_generated/` and is **committed**.
- A CI job runs the generator and fails if `git diff` is not clean.
- Never edit files in `openehr_am/_generated/` by hand.

## Output format for code changes

When implementing anything:

1. Brief plan
2. Files changed
3. Patch file-by-file
4. Tests added/updated + commands to run
