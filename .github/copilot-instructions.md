# Copilot Instructions — pyopenehr-am (Python 3.14+, Pure Python)

These instructions apply to **all Copilot Chat requests** in this repository.

## North star
Build a **standards-driven**, **pure-Python** toolkit for openEHR artefacts (ADL2/AOM2/ODIN/BMM/OPT2) that other teams can embed.

## Target runtime
- Python **3.14+ only**. No compatibility shims for older Python.
- Default semantics in 3.14 include **deferred evaluation of annotations**; do not opt out by adding `from __future__ import annotations`.
- Use `annotationlib.get_annotations()` if you need runtime access to evaluated annotations.

## Hard constraints
- Pure Python only (no wrappers around existing Java/.NET implementations).
- All invalid input must be handled gracefully by returning `Issue` objects.
- Keep public API small and stable; avoid leaking internal parse-tree objects.

## Architecture
Treat the library like a compiler:
**Parse → Build AOM → Validate → Compile OPT → (Optional) Validate Instances**

### Layer responsibilities
- Parsing (`adl/`, `odin/`): text → syntax AST with source spans.
- Semantic building (`aom/`): syntax AST → semantic AOM model.
- Validation (`validation/`): rule checks (syntax/semantic/RM/OPT) returning Issues.
- RM schemas (`bmm/`): load BMM and expose type/class/property lookup.
- Compilation (`opt/`): template + archetype set → OPT operational form.
- Paths (`path/`): parse/normalize/resolve openEHR paths.

## Diagnostics (non-negotiable)
Use `Issue` objects with:
- `code` (stable, documented in `docs/issue-codes.md`)
- `severity` (INFO/WARN/ERROR)
- best-effort location (`file`, `line`, `col`, optional end span)
- optional `path`, `node_id`

Exceptions are for programmer errors or irrecoverable I/O only.

## Validation rules
- Every new rule needs:
  1) an Issue code in `docs/issue-codes.md`
  2) a `# Spec:` URL comment (short, no big quotes)
  3) tests asserting the code is emitted

## ANTLR generated code
- Generated parser output under `openehr_am/_generated/` is committed.
- Never edit generated code by hand.
- If grammars change, rerun the generator script and commit the new output.

## How to respond when asked to implement code
Always provide:
1) Plan (brief)
2) Files to add/modify
3) Patch file-by-file
4) Tests + commands to run
5) Notes on spec provenance and Issue codes (if applicable)

Keep diffs small and incremental.
