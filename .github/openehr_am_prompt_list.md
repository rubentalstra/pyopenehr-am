# Prompt List — Build `pyopenehr-am` (Pure Python, Typer + Rich CLI)

Copy/paste these prompts into your VS Code agent (or Copilot Chat) **in order**.
Each prompt is designed to produce **reviewable diffs** with tests.

> CLI choice: **Typer** (type-hint driven, Click-based) + **Rich** for formatted
> output.

---

## Phase 0 — Bootstrap

### 0.1 Repo scaffold + tooling

Create the initial project scaffold for a pure-Python package named
`openehr_am`. Add `pyproject.toml` with Python 3.12+, dependencies for `pytest`
and `ruff`, and a Typer-based CLI entrypoint placeholder (`openehr-am --help`).
Create `openehr_am/__init__.py`. Add one trivial test to confirm imports work.
Provide file-by-file patches and test commands.

### 0.2 Diagnostics foundation

Implement the diagnostics model: `Severity` enum, `Issue` dataclass (code,
severity, message, file, line, col, end_line, end_col, path, node_id), plus
`.to_dict()` and `.pretty()` methods. Add `IssueCollector`. Add tests asserting
serialization and formatting.

### 0.3 Issue codes + docs integration

Add `docs/issue-codes.md` and wire a small helper in code that validates Issue
codes match the pattern (e.g., `ADL###`, `AOM###`, etc.). Add tests.

---

## Phase 1 — Parsing (ODIN first)

### 1.1 ANTLR integration plan + generation scripts + "generated code" policy

Add a documented approach for integrating ANTLR grammars and **adopt this
policy**:

- **Commit generated ANTLR Python code** to the repo under
  `openehr_am/_generated/` (so `pip install` does not require Java/ANTLR).
- Provide a generator script `scripts/generate_parsers.py` (or `.sh`) that
  regenerates code into `openehr_am/_generated/`.
- Add a CI job that runs the generator and **fails if `git diff` is non-empty**
  (ensures generated code stays in sync).
- Add clear docs in `docs/dev/parsers.md` explaining how to regenerate parsers
  and the "do not edit generated files" rule.

Scaffold folders for:

- `grammars/` (or a pinned submodule) for grammar sources
- `openehr_am/_generated/` for generated output

Don’t implement full generation yet if it’s too heavy; start with the structure,
scripts, and CI check placeholders.

### 1.2 ODIN AST model

Implement a minimal ODIN AST model in `openehr_am/odin/ast.py` (nodes for
primitive, list, object, keyed-list). Include optional source span fields. Add
unit tests constructing these nodes.

### 1.3 ODIN parser wrapper (stub first)

Create `openehr_am/odin/parser.py` with a
`parse_odin(text, *, filename=None) -(node, issues)` API that currently returns
a structured `Issue` explaining ODIN parsing is not wired yet. Add tests that
ensure it returns an Issue list, not an exception.

### 1.4 ODIN parser wired to generated ANTLR (real implementation)

Integrate the ANTLR runtime and the generated ODIN parser classes (assume they
exist under `openehr_am/_generated/odin/`). Implement `parse_odin` to return an
ODIN AST and parser Issues with line/col info. Add tests for:

- primitives
- nested objects
- malformed input (Issue code `ADL001` or `ODIN001`—pick one, document in
  `docs/issue-codes.md`)

---

## Phase 2 — ADL2 parse to AST (minimal)

### 2.1 ADL AST model

Create `openehr_am/adl/ast.py` with a minimal ADL AST that captures:
archetype/template id, language, description/terminology ODIN blocks as ODIN AST
nodes, and the definition section as a placeholder object. Include source spans.

### 2.2 ADL2 parser wrapper (header + ODIN sections)

Implement `openehr_am/adl/parser.py` with
`parse_adl(text, *, filename=None) -(adl_ast, issues)`. For now, parse only:

- archetype/template header identifiers
- language/description/terminology sections (ODIN blocks) Leave cADL definition
  parsing as TODO but don’t crash. Add tests with a minimal valid ADL snippet.

---

## Phase 3 — AOM2 model + first semantic validator

### 3.1 AOM2 core dataclasses (MVP)

Implement minimal AOM2 dataclasses in `openehr_am/aom/model.py` sufficient to
represent:

- `Archetype` / `Template`
- Terminology tables (term_defs, constraint_defs, value_sets)
- A minimal definition tree placeholder Keep it small and typed. Add tests.

### 3.2 AST → AOM builder (terminology first)

Implement `openehr_am/aom/builder.py` converting ADL AST → AOM objects for
header + terminology only. Preserve source locations where possible. Add tests
ensuring terminology codes are imported correctly.

### 3.3 Semantic validation: terminology references (first real AOM rule)

Add a semantic validator check: “every referenced `atNNNN`/`acNNNN` must be
defined”. Add Issue codes (e.g., `AOM200`) to `docs/issue-codes.md`. Add tests
where a definition references an undefined code and asserts `AOM200`.

---

## Phase 4 — Paths + RM conformance foundations

### 4.1 Path parser (MVP)

Implement `openehr_am/path/parser.py` with a basic openEHR path parser (enough
for bracketed node IDs like `/items[at0001]`). Add tests for parsing and error
Issue codes `PATH900`.

### 4.2 BMM loader (skeleton)

Create `openehr_am/bmm/` models and a loader stub that will load `.bmm` files
using the ODIN AST. Return structured Issues for unsupported features. Add tests
for graceful behavior.

### 4.3 RM conformance validator (MVP)

Implement minimal RM conformance checks:

- unknown RM type name
- unknown RM attribute name Use a tiny test BMM fixture in `tests/fixtures/` to
  validate behavior. Add Issue codes `BMM500`/`BMM510` with tests.

---

## Phase 5 — OPT2 compilation MVP

### 5.1 Archetype repository

Implement `ArchetypeRepository` that loads `.adl` files from a directory, parses
them, validates syntax, and indexes by archetype id. Add tests with 2
archetypes.

### 5.2 OPT2 model (minimal)

Add `openehr_am/opt/model.py` with minimal structures to represent an
operational template and flattened constraint tree (placeholder allowed). Add
JSON export. Add tests for JSON export determinism.

### 5.3 OPT compiler (MVP)

Implement `compile_opt(template, archetype_repo, rm_repo)` that:

- resolves included archetypes
- produces a minimal OPT structure Add tests for missing archetype resolution
  (Issue code `OPT700`).

---

## Phase 6 — Developer experience (Typer + Rich CLI)

### 6.1 CLI v0 using Typer

Implement the CLI using **Typer** + **Rich**. Commands: `lint`, `validate`,
`compile-opt`. Add shared options like `--json` and `--rm`. Ensure exit codes: 0
success, 1 validation errors, 2 usage/IO errors. Use Rich for human output
(tables/colors), and output strict JSON when `--json` is set (no Rich
formatting). Add CLI tests.

### 6.2 Docs + examples

Add `docs/quickstart.md` with an example of parsing + validating + compiling an
OPT and showing Issues (both human and JSON output). Keep it minimal and
runnable.

---

## Phase 7 — Optional (High value for migration builders)

### 7.1 Instance validation vs OPT

Add an experimental module `openehr_am/instance/validate.py` that can validate a
simplified composition JSON/object against your OPT constraints. Start with a
tiny supported subset (e.g., presence/required fields and primitive ranges). Add
tests and clearly document limitations.

---

## Notes

- **ANTLR generated code policy:** Commit generated code in
  `openehr_am/_generated/` and enforce regeneration via CI (`git diff` must be
  clean).
- **Rich output policy:** Human output uses Rich; `--json` outputs strict JSON
  only.
