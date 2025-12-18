# Copilot Instructions — openEHR AM Toolkit (Pure Python)

These instructions apply to **all Copilot Chat requests** in this repository.

## What this repo is
A **pure-Python** SDK that other developers can embed to build legacy → openEHR migration tooling. This repo provides the reusable primitives:
- Parse **ADL2** (archetypes/templates) and embedded **ODIN**
- Build **AOM2** semantic models
- Validate (syntax + AOM2 semantic validity + RM conformance via **BMM** schemas)
- Compile templates/archetypes to **OPT2** (Operational Template)
- (Later) validate instance data (composition JSON/object) against OPT

## Hard constraints (must follow)
- **Pure Python only.** No Java/.NET wrappers, no JPype/JNI, no calling external “reference implementations”.
- **Standards-driven.** When implementing a rule/structure, add a short comment with the relevant spec URL.
- Keep the public API **small, stable, and typed**.
- Prefer **incremental, reviewable diffs** and always include tests.

## Internal architecture (compiler pipeline)
Implement the package like a compiler:
**Parse → Build AOM → Validate → Compile OPT → (Optional) Validate Instances**

- “Compile OPT” means compiling a template + archetypes into an Operational Template representation for runtime validation.
- “Validate Instances” means validating the output data produced by migration code (userland) against an OPT.

## Repository structure (expected)
- `openehr_am/odin/` — ODIN parsing + AST
- `openehr_am/adl/` — ADL2 parsing + AST (cADL + RULES parsing)
- `openehr_am/aom/` — AOM2 dataclasses (semantic object model)
- `openehr_am/bmm/` — BMM loader + ModelRepository (RM schemas)
- `openehr_am/validation/` — layered validators + check registry
- `openehr_am/opt/` — OPT2 model + compiler
- `openehr_am/path/` — openEHR path parsing + resolution helpers
- `openehr_am/_generated/` — generated parser code (DO NOT edit by hand)

## Diagnostics (non-negotiable)
All recoverable problems must be returned as `Issue` objects (not exceptions), including:
- stable `code` (e.g., `ADL001`, `AOM014`, `BMM003`, `OPT010`)
- `severity` (`INFO|WARN|ERROR`)
- best-effort `file`, `line`, `col`
- optional `path` and `node_id`

Exceptions are only for programmer errors or unrecoverable I/O.

## Issue codes and rule provenance
- Maintain the canonical list of codes in `docs/issue-codes.md`.
- Every new validation rule must:
  1) choose or add an Issue code in that file, and
  2) include a short `# Spec:` comment pointing to the relevant openEHR spec URL.

## How to respond when generating code
When the user asks to “implement X”, respond with:
1) **Plan (brief)**: what changes and why
2) **Files**: list files to add/modify
3) **Patch**: code file-by-file
4) **How to test**: commands to run (`pytest`, etc.)

Avoid huge rewrites; keep diffs small and composable.
