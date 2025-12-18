---
name: openEHR AM core library rules
description: Standards and architecture for openehr_am package modules
applyTo: "openehr_am/**/*.py"
---
# openEHR AM core library rules

## Style
- Python 3.11+
- Use `dataclasses` for domain objects (AST/AOM/BMM/OPT).
- Use `typing` everywhere; keep public APIs fully typed.
- Prefer pure functions and small classes.

## Layering (keep clean boundaries)
- Parsing layer:
  - ANTLR parse tree → minimal AST (syntax layer)
  - AST → AOM (semantic layer)
- Validation layer:
  - Syntax issues (parser)
  - AOM2 semantic checks
  - RM conformance via BMM
- OPT layer:
  - compile templates/archetypes into Operational Template structures

## Source locations
- Preserve `line/col` spans from parser tokens where possible.
- Attach source spans to AST and AOM nodes (even if optional).

## Rule provenance
When implementing a validation rule, include a short comment with the spec URL, e.g.:
`# Spec: https://specifications.openehr.org/releases/AM/Release-2.1.0/AOM2.html (Validity rules ...)`

Also ensure the rule’s Issue code is documented in `docs/issue-codes.md`.

## Minimal public API
Keep `openehr_am/__init__.py` small and stable:
- parse_* functions
- validate(level=...) function
- compile_opt function
Expose advanced internals under submodules but avoid breaking changes.
