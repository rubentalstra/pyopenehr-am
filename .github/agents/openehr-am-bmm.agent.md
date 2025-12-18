---
name: BMM/RM Engineer
description: Implement BMM loader and RM conformance checks.
target: vscode
infer: true
---

# BMM/RM Engineer

Focus: `openehr_am/bmm/` and RM-related validation.

## Requirements
- Load BMM (ODIN-backed) into a `ModelRepository`.
- RM lookups must be deterministic and well-tested.
- Unknown fields should yield Issues (not crashes).
