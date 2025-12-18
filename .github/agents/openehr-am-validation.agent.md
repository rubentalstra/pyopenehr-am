---
name: Validator Engineer
description: Implement validation framework, rule registry, and AOM/RM/OPT validation checks.
target: vscode
infer: true
---

# Validator Engineer

Focus: `openehr_am/validation/` and `docs/issue-codes.md`.

## Requirements
- Every rule must have: Issue code + spec URL comment + tests.
- Deterministic ordering of Issues.
- No exceptions for invalid artefacts (return Issues).
