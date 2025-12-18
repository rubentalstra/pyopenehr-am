# Issue Codes

This document defines **stable Issue codes** used across the project for parser,
validation, and compiler diagnostics.

## Format

Codes are formatted as:

- `ADL###` — ADL2 parsing & syntax-level issues
- `ODN###` — ODIN parsing issues (optional prefix; you may also keep ODIN under
  ADL*)
- `AQL###` — AQL parsing & syntax-level issues
- `AOM###` — AOM2 semantic validity rules
- `BMM###` — BMM loading and RM conformance checks
- `OPT###` — OPT compilation and integrity
- `PATH###` — openEHR path parsing/resolution
- `CLI###` — CLI usage/IO errors (rare)

## Allocation ranges (recommended)

- ADL001–ADL199: parser/syntax/structure
- ODN100–ODN199: ODIN-specific parse/structure (if used)
- AQL100–AQL199: AQL parser/syntax
- AOM200–AOM499: AOM2 semantic validity
- BMM500–BMM699: BMM + RM validation
- OPT700–OPT899: OPT compilation + integrity
- PATH900–PATH999: path parsing/resolution
- CLI001–CLI199: CLI usage/IO errors (rare)

## Registry

| Code    | Severity | Category  | Summary                                           | Notes / Spec Link         |
| ------- | -------- | --------- | ------------------------------------------------- | ------------------------- |
| ADL001  | ERROR    | Parse     | Unexpected token / parse failure                  | ADL2 grammar              |
| ADL005  | ERROR    | IO        | Cannot read input file                            | Internal                  |
| ADL010  | ERROR    | Structure | Missing required ADL section                      | ADL2 structure            |
| ADL020  | WARN     | Structure | Deprecated/unknown section                        | ADL2 structure            |
| ADL030  | ERROR    | Structure | Invalid cADL interval / occurrences / cardinality | AOM2 constraints          |
| ODN100  | ERROR    | Parse     | ODIN parse failure                                | ODIN grammar              |
| ODN110  | WARN     | Structure | ODIN key duplication                              | ODIN rules                |
| AQL100  | ERROR    | Parse     | AQL parse failure / invalid query syntax          | AQL grammar               |
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
| AOM242  | ERROR    | Structure | Duplicate archetype id across ADL files           | Internal repository       |
| BMM500  | ERROR    | RM        | Unknown RM type referenced                        | BMM                       |
| BMM505  | ERROR    | IO        | Invalid BMM repository directory                  | Internal                  |
| BMM510  | ERROR    | RM        | Unknown RM attribute referenced                   | BMM                       |
| BMM520  | ERROR    | RM        | Multiplicity mismatch                             | BMM                       |
| BMM530  | WARN     | Structure | Unsupported / ignored BMM field                   | BMM loader (subset)       |
| BMM540  | ERROR    | Structure | Missing required BMM field                        | BMM loader (subset)       |
| BMM550  | ERROR    | Structure | Invalid BMM value shape/type                      | BMM loader (subset)       |
| OPT700  | ERROR    | Compile   | Cannot resolve archetype inclusion                | OPT2                      |
| OPT705  | ERROR    | Compile   | Dependency cycle detected                         | OPT2                      |
| OPT720  | ERROR    | Compile   | Slot filling failed / no matching archetype       | OPT2                      |
| OPT730  | ERROR    | Compile   | Specialisation flattening conflict                | OPT2                      |
| OPT750  | ERROR    | Integrity | Broken internal reference after compilation       | OPT2                      |
| PATH900 | ERROR    | Path      | Path parse failure                                | Path rules                |
| PATH910 | ERROR    | Path      | Path resolves to no nodes                         | Path resolver             |
| CLI010  | ERROR    | IO        | Cannot write output file                          | Internal                  |
| CLI011  | ERROR    | IO        | Invalid archetype repository directory            | Internal                  |

## Contributor checklist for new codes

- [ ] Add the code to this table before using it
- [ ] Add tests asserting the code appears
- [ ] Add a short spec URL comment near the rule implementation

## Automated check

The test suite includes a simple heuristic check that greps Python sources under
`openehr_am/` for code-like strings (e.g. `ADL001`, `AOM205`) and asserts they
are present in this document.

When you introduce a new Issue code in code, add it to the table above first.
