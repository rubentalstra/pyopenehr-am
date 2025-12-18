# Issue Codes

This document defines **stable Issue codes** used across the project for parser,
validation, and compiler diagnostics.

## Why this exists

- Tooling users need **stable, machine-readable codes** for CI gating,
  analytics, and automated remediation.
- Contributors need a single place to avoid collisions and keep categories
  consistent.

## Format

Codes are formatted as:

- `ADL###` — ADL2 / ODIN-in-ADL parsing & syntax-level issues
- `AOM###` — AOM2 semantic model and validity rules
- `BMM###` — BMM schema loading and RM conformance checks
- `OPT###` — OPT2 compilation and operational template integrity
- `PATH###` — openEHR path parsing/resolution utilities
- `CLI###` — CLI usage/IO issues (rare; prefer standard exit codes)

### Severity

- `INFO` — informational (usually disabled by default)
- `WARN` — potentially problematic but not invalid
- `ERROR` — invalid artefact or failed compilation

## Allocation ranges (recommended)

- ADL001–ADL199: parser/syntax/structure
- AOM200–AOM499: AOM2 semantic validity
- BMM500–BMM699: BMM loader + RM validation
- OPT700–OPT899: OPT2 compilation + integrity
- PATH900–PATH999: path parsing/resolution

> You can change these ranges, but keep them consistent once published.

---

## Code Registry

> Add new codes here before using them in code.

| Code    | Severity | Category  | Summary                                     | Notes / Spec Link         |
| ------- | -------- | --------- | ------------------------------------------- | ------------------------- |
| ADL001  | ERROR    | Parse     | Unexpected token / parse failure            | (spec URL when relevant)  |
| ADL010  | ERROR    | Structure | Missing required ADL section                |                           |
| ADL020  | WARN     | Structure | Deprecated/unknown section                  |                           |
| AOM200  | ERROR    | Semantics | Terminology code referenced but not defined | AOM2 terminology validity |
| AOM210  | ERROR    | Semantics | Invalid node id format                      |                           |
| AOM230  | ERROR    | Semantics | Specialisation level mismatch               |                           |
| BMM500  | ERROR    | RM        | Unknown RM type referenced                  |                           |
| BMM510  | ERROR    | RM        | Unknown RM attribute referenced             |                           |
| OPT700  | ERROR    | Compile   | Cannot resolve archetype inclusion          |                           |
| OPT720  | ERROR    | Compile   | Slot filling failed / no matching archetype |                           |
| OPT750  | ERROR    | Integrity | Broken internal reference after compilation |                           |
| PATH900 | ERROR    | Path      | Path parse failure                          |                           |
| PATH910 | ERROR    | Path      | Path resolves to no nodes                   |                           |

---

## Contributor checklist for adding a new Issue code

- [ ] Add the code row to this table
- [ ] Ensure the code is unique and within the correct range
- [ ] Add/extend tests asserting the code appears
- [ ] If the rule comes from the spec, add a short spec URL in the “Notes / Spec
      Link” column
