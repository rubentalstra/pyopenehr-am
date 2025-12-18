---
name: CLI behavior
description: Rules for the CLI entrypoints and command structure
applyTo: "openehr_am/cli/**/*.py"
---
# CLI behavior

- CLI must be stable and script-friendly.
- Commands:
  - `lint` (syntax)
  - `validate` (semantic + optional RM)
  - `compile-opt` (template compilation)
- Output:
  - human-readable by default
  - `--json` option for machine-readable Issue output
- Exit codes:
  - 0: success (no errors)
  - 1: errors present
  - 2: usage/IO error
