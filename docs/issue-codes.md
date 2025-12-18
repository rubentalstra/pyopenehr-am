# Issue Codes

This document defines **stable Issue codes** used across the project for parser,
validation, and compiler diagnostics.

## Format

Codes are formatted as:

- `ADL###` — ADL2 parsing & syntax-level issues
- `ODN###` — ODIN parsing issues (optional prefix; you may also keep ODIN under
  ADL*)
- `AOM###` — AOM2 semantic validity rules
- `BMM###` — BMM loading and RM conformance checks
- `OPT###` — OPT compilation and integrity
- `PATH###` — openEHR path parsing/resolution
- `CLI###` — CLI usage/IO errors (rare)

## Allocation ranges (recommended)

- ADL001–ADL199: parser/syntax/structure
- ODN100–ODN199: ODIN-specific parse/structure (if used)
- AOM200–AOM499: AOM2 semantic validity
- BMM500–BMM699: BMM + RM validation
- OPT700–OPT899: OPT compilation + integrity
- PATH900–PATH999: path parsing/resolution
- CLI001–CLI199: CLI usage/IO errors (rare)

## Registry

| Code    | Severity | Category  | Summary                                           | Notes / Spec Link         |
| ------- | -------- | --------- | ------------------------------------------------- | ------------------------- |
| ADL001  | ERROR    | Parse     | Unexpected token / parse failure                  | ADL2 grammar              |
| ADL010  | ERROR    | Structure | Missing required ADL section                      | ADL2 structure            |
| ADL020  | WARN     | Structure | Deprecated/unknown section                        | ADL2 structure            |
| ADL030  | ERROR    | Structure | Invalid cADL interval / occurrences / cardinality | AOM2 constraints          |
| ODN100  | ERROR    | Parse     | ODIN parse failure                                | ODIN grammar              |
| ODN110  | WARN     | Structure | ODIN key duplication                              | ODIN rules                |
| AOM200  | ERROR    | Semantics | Terminology code referenced but not defined       | AOM2 terminology validity |
| AOM205  | ERROR    | Semantics | AOM build failed / unsupported artefact shape     | Internal builder          |
| AOM210  | ERROR    | Semantics | Invalid node id format                            | AOM2 node id rules        |
| AOM230  | ERROR    | Semantics | Specialisation level mismatch                     | AOM2 specialization       |
| AOM240  | ERROR    | Semantics | Duplicate node id / duplicate path                | AOM2 uniqueness           |
| AOM250  | ERROR    | Semantics | Occurrences/cardinality invalid                   | AOM2 constraints          |
| AOM260  | ERROR    | Semantics | Value set integrity failure                       | AOM2 terminology          |
| AOM270  | WARN     | Semantics | Language/original_language inconsistency          | AOM2 language             |
| AOM280  | ERROR    | Semantics | Template overlay/exclusion invalid                | Template rules            |
| AOM290  | WARN     | Semantics | Rules reference invalid path/code                 | GDL2/RULES subset         |
| BMM500  | ERROR    | RM        | Unknown RM type referenced                        | BMM                       |
| BMM510  | ERROR    | RM        | Unknown RM attribute referenced                   | BMM                       |
| BMM520  | ERROR    | RM        | Multiplicity mismatch                             | BMM                       |
| OPT700  | ERROR    | Compile   | Cannot resolve archetype inclusion                | OPT2                      |
| OPT705  | ERROR    | Compile   | Dependency cycle detected                         | OPT2                      |
| OPT720  | ERROR    | Compile   | Slot filling failed / no matching archetype       | OPT2                      |
| OPT730  | ERROR    | Compile   | Specialisation flattening conflict                | OPT2                      |
| OPT750  | ERROR    | Integrity | Broken internal reference after compilation       | OPT2                      |
| PATH900 | ERROR    | Path      | Path parse failure                                | Path rules                |
| PATH910 | ERROR    | Path      | Path resolves to no nodes                         | Path resolver             |

## Contributor checklist for new codes

- [ ] Add the code to this table before using it
- [ ] Add tests asserting the code appears
- [ ] Add a short spec URL comment near the rule implementation
