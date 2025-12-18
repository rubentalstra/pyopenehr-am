---
name: BMM and RM conformance
description: Rules for loading BMM schemas and validating RM references
applyTo: "openehr_am/bmm/**/*.py,openehr_am/validation/rm/**/*.py"
---
# BMM / RM rules

## Loader principles
- BMM is persisted in ODIN; use the ODIN AST as an intermediate representation.
- Loader must tolerate unknown/unimplemented fields:
  - emit Issues for unsupported features instead of crashing.

## Repository
- Provide a `ModelRepository` that supports:
  - class lookup by name
  - property lookup by (class, property)
  - type reference resolution (subset initially)

## Conformance checks
- Unknown RM type → `BMM500`
- Unknown RM attribute → `BMM510`
- Multiplicity mismatch → `BMM520` (basic)
