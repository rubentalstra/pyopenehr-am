---
name: Validation checks
description: How to implement new validation rules in a consistent way
applyTo: "openehr_am/validation/**/*.py"
---
# Validation checks

## Structure
- Implement checks as small functions: `def check_xxx(ctx) -> list[Issue]`
- Each check:
  - returns Issue objects only
  - never raises for invalid artefacts
  - uses stable Issue codes (tracked in `docs/issue-codes.md`)
- Add checks to a registry so `validate(level=...)` can run them by layer.

## Guidance
- Prefer deterministic ordering of issues.
- Use paths/node_ids to pinpoint errors when possible.
- Include a short `# Spec:` URL comment for each rule family.

## Template
Use `docs/validation-rule-template.md` when adding a new rule.
