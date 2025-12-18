---
name: Validation framework and rules
description: Implementing validation checks with stable Issue codes and spec provenance
applyTo: "openehr_am/validation/**/*.py"
---
# Validation rules

## Layers
- syntax: produced during parsing; optionally re-run on text input
- semantic: AOM2 validity rules
- rm: BMM conformance checks
- opt: OPT compilation + integrity checks

## Rule requirements
Every new rule must:
- Emit stable Issue codes (documented in `docs/issue-codes.md`)
- Include a short `# Spec: <URL>` comment near the rule implementation
- Have tests asserting code + severity + (when possible) location

## Rule structure
Prefer small functions:
- `def check_xxx(ctx: ValidationContext) -> list[Issue]: ...`

## Registry
- Checks must be registered in a layer registry, executed in a deterministic order.

## Output stability
- Issue ordering must be deterministic:
  - sort by file, line, col, code, message
