---
name: openEHR AM core library rules
description: Standards and architecture for openehr_am package modules (Python 3.14+)
applyTo: "openehr_am/**/*.py"
---
# openEHR AM core library rules (Python 3.14+)

## Runtime baseline
- **Python 3.14+ only**.
- Avoid `from __future__ import annotations` (it opts out of 3.14’s default deferred annotations).
- Use `annotationlib.get_annotations()` if runtime introspection is required.

## Data modeling
- Prefer `@dataclass(slots=True)` for domain objects (AST/AOM/BMM/OPT).
- Use `frozen=True` for immutable models where practical.
- Keep models small and composable; avoid deep inheritance hierarchies.

## Typing
- All public APIs must be fully typed.
- Use modern syntax: `X | None`, `list[str]`, `dict[str, T]`.
- For aliases, prefer `type Name = ...` (PEP 695) when it improves readability.

## Boundaries
- Parsing: ANTLR parse-tree → syntax AST (no semantic validation)
- Semantic: syntax AST → AOM objects
- Validation: rules that emit Issues; do not raise for invalid user input
- Compilation: template + archetypes → OPT operational form

## Source locations
- Preserve line/col spans from tokens wherever possible.
- Attach spans to AST/AOM nodes; store them consistently (e.g., `span: SourceSpan | None`).

## Error handling
- Recoverable input errors → Issues.
- Programmer errors → exceptions (TypeError, ValueError, AssertionError).
- Never `eval` or execute any content parsed from ADL/ODIN.

## Public API discipline
Keep `openehr_am/__init__.py` minimal and stable:
- `parse_archetype`, `parse_template`
- `validate(...)`
- `load_bmm_repo(...)`
- `compile_opt(...)`
