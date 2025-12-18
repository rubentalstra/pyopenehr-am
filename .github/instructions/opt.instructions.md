---
name: OPT compilation
description: Guidance for compiling templates/archetypes to OPT2 and validating integrity
applyTo: "openehr_am/opt/**/*.py,openehr_am/validation/opt/**/*.py"
---
# OPT compilation guidance

## Principles
- Compilation must be deterministic.
- Missing dependencies must emit Issues (not exceptions).

## Common issue codes
- Missing archetype/template dependency: `OPT700`
- Slot fill failure: `OPT720`
- Flattening conflicts: `OPT730`
- Integrity/broken refs: `OPT750`

## Output
- Provide deterministic JSON export (`to_dict()`).
- Avoid embedding parser internals in OPT output.
