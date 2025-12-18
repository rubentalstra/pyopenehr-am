# AGENTS — openehr_am package

## Boundaries
- `adl/`, `odin/`, `antlr/`: syntax + parsing only (no semantic checks here)
- `aom/`: semantic data model (AOM2)
- `validation/`: all rule checks (syntax/semantic/RM/OPT)
- `bmm/`: RM schemas (BMM) and type repository
- `opt/`: compilation and operational template model
- `path/`: path parsing and resolution helpers

## Python 3.14+ conventions
- Prefer `@dataclass(slots=True)` for domain models.
- Use `frozen=True` where immutability makes sense.
- Do not use `from __future__ import annotations`.
- Use `annotationlib.get_annotations()` for introspection.
