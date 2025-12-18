# Prompt List — Build `pyopenehr-am` (Pure Python **3.14**, Typer + Rich CLI)

This is an **expanded, task-by-task** prompt sequence you can feed to your VS
Code agent (or Copilot Chat). It is designed to build the full codebase
incrementally with **reviewable diffs** and **tests per task**.

> Policies baked in:
>
> - **Target runtime:** Python **3.14+ only** (no backports required).
> - **Typer + Rich** for human CLI output; `--json` prints strict JSON only.
> - **Commit generated ANTLR Python code** under `openehr_am/_generated/`, and
>   enforce regeneration via CI (`git diff` must be clean).
> - Prefer **small PR-sized increments** with tests.

> Python 3.14 note (typing/annotations):
>
> - Do **not** use `from __future__ import annotations` (deprecated); rely on
>   Python 3.14’s deferred annotations.
> - If any code needs runtime introspection of annotations, use
>   `annotationlib.get_annotations()` rather than reading `__annotations__`
>   directly.

---

## How to use agents for this prompt list (VS Code Copilot)

### Do agents switch automatically?

- **No** — you normally **choose an agent from the agent picker** in the Chat
  view, and the conversation runs with that agent’s configuration.
- You _can_ switch agents manually at any time by selecting a different agent in
  the picker.
- VS Code custom agents can also define **handoffs** so you can jump from one
  agent to another with a single click (useful for moving from planning →
  implementation → review).

References:

- VS Code custom agents:
  https://code.visualstudio.com/docs/copilot/customization/custom-agents
- Copilot Chat basics / agent picker:
  https://code.visualstudio.com/docs/copilot/chat/copilot-chat

### Recommended agent per phase

Use **openEHR AM Builder** as your default “orchestrator” and switch to
specialists for focused phases:

| Phase | What you’re doing                                                   | Recommended agent                                                             |
| ----- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 0–2   | Repo bootstrap, CI, diagnostics, conventions                        | **openEHR AM Builder** (or **Release Engineer** for packaging/CI-heavy tasks) |
| 3–7   | ANTLR wiring + ODIN/ADL parsing + cADL + rules parsing              | **Parser Engineer**                                                           |
| 8–11  | AOM model + semantic validation framework + path parsing/resolution | **Validator Engineer** (and **Parser Engineer** if grammar work needed)       |
| 12    | BMM loader + RM repository + RM conformance checks                  | **BMM/RM Engineer**                                                           |
| 13–14 | Archetype repo + OPT model + compilation + OPT integrity            | **OPT Compiler Engineer**                                                     |
| 16    | Typer + Rich CLI and CLI tests                                      | **CLI/UX Engineer**                                                           |
| 17–20 | Docs, corpus tests, release readiness                               | **openEHR AM Builder** (and **Release Engineer** for packaging/release)       |

Tip: if you keep one chat thread per major phase (parsing / validation / BMM /
OPT / CLI), context stays cleaner and results are more consistent.

---

## Phase 0 — Repo bootstrap and standards baseline

### 0.1 Repo scaffold + packaging basics [x]

Create the initial project scaffold for a pure-Python package named `openehr_am`
targeting **Python 3.14+ only**. Add `pyproject.toml` (PEP 621) with
`requires-python = ">=3.14"`, and dependencies for `pytest`, `ruff`, `typer`,
and `rich`. Create `openehr_am/__init__.py`. Add `openehr_am/cli/` package with
`app.py` exposing a Typer app and `main.py` entrypoint. Add one trivial test to
confirm imports work. Provide file-by-file patches and test commands.

### 0.2 Add README + project docs skeleton [x]

Add `README.md` (concise), plus `docs/` folder with `docs/architecture.md` and
`docs/dev/`. Ensure docs mention “Python 3.14+ only”, “pure Python only”, and
the compiler pipeline architecture. Add “Development” instructions:
`pip install -e ".[dev]"` and `pytest`.

### 0.3 Pin spec baseline file [x]

Add `SPEC_BASELINE.md` that pins the exact openEHR spec URLs you target (ADL2,
AOM2, ODIN, BMM, OPT2) and the chosen release versions. Add a note: “Spec
baseline changes require a minor version bump.”

### 0.4 Add repo hygiene files [x]

Add `.gitignore`, `.editorconfig`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`.
Keep `CONTRIBUTING.md` aligned with the Issue-code and “Spec provenance” policy,
and note “Python 3.14+ only”.

### 0.5 Add ruff config and formatting policy [x]

Configure `ruff` in `pyproject.toml` with sane defaults. Ensure lint/format
excludes `openehr_am/_generated/`. Add a “lint” instruction to README.

### 0.6 Add typing checker (Python 3.14) [x]

Configure **pyright** (recommended) or **mypy** for Python 3.14. Ensure CI runs
it. Prefer modern typing features (PEP 695 `type` aliases where helpful), but
keep it readable.

### 0.7 Add versioning [x]

Add `openehr_am/__about__.py` (or similar) holding `__version__`. Expose
`__version__` in `openehr_am/__init__.py`. Add a test that checks `__version__`
exists.

### 0.8 Enforce “no future annotations” policy [x]

Add a simple lint/test guard that prevents `from __future__ import annotations`
anywhere in `openehr_am/` (since Python 3.14+ is the baseline). Add a test that
scans for it and fails if found.

---

## Phase 1 — CI and “generated parser code” discipline

### 1.1 CI: lint + tests + typing [x]

Add GitHub Actions workflow(s) to run: ruff, tests, and type checking on
push/PR. Keep CI fast and deterministic. Ensure it runs with Python 3.14.

### 1.2 ANTLR policy scaffolding (commit generated code + CI drift check) [x]

Create:

- `grammars/` folder (or doc a pinned git submodule strategy)
- `openehr_am/_generated/` folder with `README.md` stating “generated; do not
  edit”
- `scripts/generate_parsers.py` placeholder (Python 3.14)
- CI job: run generator and fail if `git diff` is non-empty. Add
  `docs/dev/parsers.md` documenting regeneration steps and the policy.

### 1.3 Optional: pre-commit hooks [x]

Add `pre-commit` config (recommended) to run ruff + tests locally. Document
usage.

---

## Phase 2 — Diagnostics and stable Issue codes (foundation)

### 2.1 Implement `Issue` model and Severity enum [x]

Implement `Severity` enum and `Issue` dataclass: code, severity, message, file,
line, col, end_line, end_col, path, node_id, plus `.to_dict()` and `.pretty()`
methods. Add tests for formatting and JSON-serializable dict output.

### 2.2 Issue code validation helper [x]

Implement `validate_issue_code(code: str) -bool` enforcing prefixes/ranges. Add
tests. Align with `docs/issue-codes.md`.

### 2.3 IssueCollector + deterministic ordering [x]

Implement `IssueCollector` that preserves deterministic ordering and supports
`.extend(...)`, `.has_errors()`, `.to_json()`. Add tests.

### 2.4 Rich rendering helpers (for CLI) [x]

Add `openehr_am/cli/render.py` that renders Issues using Rich tables (group by
file, sort by line/col). Add tests that JSON mode never outputs Rich markup.

---

## Phase 3 — ANTLR runtime wiring and error capture

### 3.1 Add ANTLR runtime dependency and wrappers [x]

Add `antlr4-python3-runtime` dependency and create `openehr_am/antlr/runtime.py`
that:

- constructs lexer/parser
- attaches error listeners that collect Issues with line/col Add tests that the
  error listener converts a fake syntax error into Issues.

### 3.2 Add generation script that supports ODIN + ADL [x]

Implement `scripts/generate_parsers.py` to generate Python code into
`openehr_am/_generated/` from grammars. Document requirements (Java, ANTLR jar)
only for contributors.

### 3.3 Add “generated code drift” unit test (optional) [x]

Add an optional local test that fails if generated outputs are missing or
clearly out of date (lightweight sanity check). CI remains the primary enforcer.

---

## Phase 4 — ODIN parsing (complete)

### 4.1 ODIN AST dataclasses (use slots where sensible) [x]

Implement ODIN AST nodes in `openehr_am/odin/ast.py`: primitives, object, list,
keyed list. Prefer `@dataclass(slots=True, frozen=True)` unless mutation is
required. Include optional source spans. Add tests.

### 4.2 ODIN parse API (stable surface) [x]

Implement
`parse_odin(text, *, filename=None) -tuple[OdinNode | None, list[Issue]]` in
`openehr_am/odin/parser.py`. It must never crash on invalid input; it returns
Issues. Add tests for malformed input.

### 4.3 ODIN parse-tree → AST visitor [x]

Implement visitor/transformer from ANTLR parse tree to ODIN AST. Handle strings,
numbers, booleans, lists, objects, keyed lists. Add tests for each.

### 4.4 ODIN serializer (MVP) [x]

Implement `to_odin(node) -str` for debugging and round-trip tests. Add
round-trip tests.

---

## Phase 5 — ADL2 parsing (incremental)

### 5.1 ADL AST skeleton [x]

Implement `openehr_am/adl/ast.py` capturing: artefact kind, artefact id,
language/original_language, description + terminology ODIN AST, definition
placeholder, rules placeholder. Include source spans and tests.

### 5.2 ADL parser: header + ODIN sections [x]

Implement `parse_adl(text, filename=None) -(AdlAst|None, issues)` that parses
header id and ODIN blocks (language/description/terminology). Leave
definition/rules as TODO but don’t crash. Add tests with minimal archetype and
template samples.

### 5.3 Add ADL fixtures folder [x]

Create `tests/fixtures/adl/` with tiny valid/invalid ADL snippets used by tests.
Add a fixture loader helper.

---

## Phase 6 — cADL definition parsing (constraint syntax)

### 6.1 Define a cADL AST (syntax layer) [x]

Create `openehr_am/adl/cadl_ast.py` with syntax-level nodes: object nodes
(rm_type_name, node_id), attributes with children, occurrences/cardinality,
primitive constraints. Add tests.

### 6.2 Parse cADL blocks into cADL AST (MVP) [x]

Extend ADL parsing to parse a minimal supported subset of `definition` into cADL
AST. Add tests.

### 6.3 Expand primitive constraints support [x]

Add ranges/intervals, regex/string constraints, enumerations. Add tests.

### 6.4 Parse occurrences/cardinality [x]

Implement occurrences/cardinality parsing and validation in AST form. Add tests.

---

## Phase 7 — RULES / expression parsing (parse-only first)

### 7.1 Rules section capture (syntax only) [x]

Extend ADL parser to capture `rules` section with source locations. Don’t
implement evaluation. Add tests.

### 7.2 Expression AST (minimal) [x]

Create `openehr_am/adl/expr_ast.py` for minimal expression AST. Add tests.

### 7.3 Parse expressions into Expression AST (MVP) [x]

Parse a small expression subset into Expression AST. Add tests.

---

## Phase 8 — AOM2 semantic model (dataclasses)

### 8.1 Implement core AOM dataclasses [x]

Implement AOM dataclasses under `openehr_am/aom/` for Archetype/Template,
terminology, and a constraint skeleton (CComplexObject, CAttribute, etc.).
Prefer slots/frozen where appropriate. Add tests.

### 8.2 Implement identifiers and parsing helpers [x]

Implement helpers for archetype ids and node ids (`atNNNN`, `acNNNN`). Add
tests.

### 8.3 AST → AOM builder: header + terminology + minimal definition [x]

Build AOM objects from ADL AST + cADL AST for the supported subset. Preserve
source locations. Add tests.

### 8.4 Add debug serializers [x]

Add deterministic `to_dict()` helpers for AOM objects (debug). Add tests.

---

## Phase 9 — Validation framework (registry + layers)

### 9.1 Validation context + registry [x]

Implement a validation registry that runs checks by layer: `syntax`, `semantic`,
`rm`, `opt`. Add `ValidationContext` carrying artefact + optional RM repo. Add
tests.

### 9.2 Syntax validation wrapper [x]

Implement `validate_syntax(text/path)` that calls parsers and returns Issues.
Add tests.

### 9.3 Semantic validation runner [x]

Implement `validate_semantic(aom_obj)` calling registered semantic checks. Add
tests with a stub check.

### 9.4 Enforce Issue codes documentation [x]

Add a test that checks Issue codes used in code are present in
`docs/issue-codes.md` (simple grep heuristic ok initially). Add docs.

---

## Phase 10 — AOM2 semantic rules (task-by-task)

### 10.1 Terminology references defined [x]

Implement check: every referenced `atNNNN`/`acNNNN` exists in terminology. Emit
`AOM200`. Add tests.

### 10.2 Node id format validation [x]

Implement check: node ids match expected patterns and specialization depth
basics. Emit `AOM210` / `AOM230`. Add tests.

### 10.3 Duplicate node ids / duplicate paths [x]

Implement check: detect duplicates in scopes (basic). Emit `AOM240`. Add tests.

### 10.4 Occurrences/cardinality sanity [x]

Check min<=max and invariants. Emit `AOM250`. Add tests.

### 10.5 Value sets integrity [x]

Validate value set references and emptiness rules. Emit `AOM260`. Add tests.

### 10.6 Language/original_language integrity [x]

Validate language presence and basic structure. Emit `AOM270`. Add tests.

### 10.7 Template overlays/exclusions (basic) [x]

Add basic checks for templates: excluded nodes exist, overlays reference valid
paths. Emit `AOM280`. Add tests.

### 10.8 Rules reference validity (basic) [x]

Validate that rule references point to known paths/codes for supported subset.
Emit `AOM290`. Add tests.

---

## Phase 11 — openEHR path parsing + resolution (expand)

### 11.1 Path AST + parser [x]

Implement `openehr_am/path/parser.py` returning Path AST. Emit `PATH900` on
parse failure. Add tests.

### 11.2 Path resolver against AOM [x]

Resolve paths against your AOM constraint tree (subset). Emit `PATH910` when
resolves to no nodes. Add tests.

### 11.3 Normalization and string round-trip [x]

Implement `to_string()` and round-trip parsing for supported subset. Add tests.

---

## Phase 12 — BMM loader and RM repository (expand)

### 12.1 BMM dataclasses (minimal) [x]

Implement BMM dataclasses: Model, Package, Class, Property, TypeRef,
Multiplicity. Add tests.

### 12.2 BMM persistence parser (ODIN-backed) [x]

Implement `load_bmm(path)` mapping ODIN AST → BMM dataclasses (subset). Add
tests with tiny fixture.

### 12.3 ModelRepository loader for a directory [x]

Implement `ModelRepository.load_from_dir(dir)` that loads multiple `.bmm`,
resolves class refs, and provides `get_class(name)`. Add tests.

### 12.4 RM conformance: rm_type_name exists [x]

Validate referenced RM types exist. Emit `BMM500`. Add tests.

### 12.5 RM conformance: rm_attribute_name exists [x]

Validate referenced RM attributes exist on the RM type. Emit `BMM510`. Add
tests.

### 12.6 RM conformance: multiplicity compatibility (basic)

Validate multiplicity doesn’t exceed RM constraints (subset). Emit `BMM520`. Add
tests.

---

## Phase 13 — Archetype repository + dependency management

### 13.1 ArchetypeRepository indexing

Implement `ArchetypeRepository` that loads `.adl` files from a directory, parses
them, and indexes by archetype id. Add tests.

### 13.2 Dependency graph and cycle detection

Implement dependency extraction and detect cycles. Emit `OPT705` for cycles. Add
tests.

### 13.3 Caching and incremental load (optional)

Add simple caching to avoid reparsing unchanged files. Add tests.

---

## Phase 14 — OPT2 model + compilation (expand)

### 14.1 OPT dataclasses

Implement `openehr_am/opt/model.py` dataclasses for an OperationalTemplate
subset + flattened constraints. Add tests.

### 14.2 OPT JSON export (deterministic)

Implement deterministic `to_dict()` and JSON export for OPT. Add tests.

### 14.3 OPT compilation: resolve included archetypes

Implement `compile_opt` resolving included archetypes; emit `OPT700` if missing.
Add tests.

### 14.4 OPT compilation: slot filling (basic)

Implement slot filling for a subset; emit `OPT720` if no match. Add tests.

### 14.5 OPT compilation: specialization flattening (basic)

Implement minimal flattening rules; emit `OPT730` on conflict. Add tests.

### 14.6 OPT integrity checks

Implement `validate_opt(opt)` integrity checks; emit `OPT750`. Add tests.

---

## Phase 15 — Public API stabilization

### 15.1 Define stable API in `openehr_am/__init__.py`

Expose a minimal stable API:

- `parse_archetype`, `parse_template`
- `validate(obj, level=..., rm=...)`
- `load_bmm_repo(dir)`
- `compile_opt(template, archetype_dir=..., rm=...)` Add flow tests.

### 15.2 Compatibility and experimental policy

Add `docs/compatibility.md` describing stability guarantees until v1.0.

---

## Phase 16 — CLI (Typer + Rich) fully implemented

### 16.1 Implement CLI command: `lint`

Implement `openehr-am lint <file>` that parses and prints Issues with Rich
tables. Add `--json` output. Add tests.

### 16.2 Implement CLI command: `validate`

Implement `openehr-am validate <file--rm <dir>` that validates semantic + RM
(when rm provided). Add tests.

### 16.3 Implement CLI command: `compile-opt`

Implement
`openehr-am compile-opt <template--repo <archetypes_dir--rm <dir--out <file>`
and output opt JSON. Add tests.

### 16.4 CLI UX polish

Add options:

- `--strict` (treat warnings as errors)
- `--format` (text|json) Ensure exit codes: 0 ok, 1 validation errors, 2
  IO/usage. Add tests.

---

## Phase 17 — Documentation (task-by-task)

### 17.1 Quickstart doc

Add `docs/quickstart.md` with real CLI and API examples, including `--json`.

### 17.2 Architecture doc

Expand `docs/architecture.md` with module boundaries and pipeline.

### 17.3 Parser dev doc

Flesh out `docs/dev/parsers.md` with regeneration steps and CI drift policy.

### 17.4 Validation docs

Add `docs/validation_levels.md` describing `syntax|semantic|rm|opt|all`.

### 17.5 OPT compilation doc

Add `docs/opt_compilation.md` describing what’s supported and planned.

---

## Phase 18 — Test harness expansion (quality)

### 18.1 Corpus test runner

Add a corpus harness that runs parse/validate across files in `tests/corpus/`.
Add a few small corpus files.

### 18.2 Snapshot-friendly output

Add helper that prints Issues deterministically for tests. Add tests.

### 18.3 Coverage reporting (optional)

Add coverage tooling and CI job. Document locally.

### 18.4 Fuzz testing (optional)

Add a small fuzz test for ODIN/ADL ensuring “no crashes” on random input.

---

## Phase 19 — Optional: instance validation vs OPT

### 19.1 Instance model (small subset)

Create `openehr_am/instance/model.py` for a minimal instance representation. Add
tests.

### 19.2 Instance validator MVP

Implement `validate_instance(instance_json, opt)` for a tiny supported subset.
Emit `INST800` codes. Add tests and docs.

### 19.3 CLI support for instance validation

Add `openehr-am validate-instance <json--opt <opt.json>` as experimental. Add
tests.

---

## Phase 20 — Release readiness

### 20.1 Build artifacts workflow

Add CI job building sdist/wheel and running `twine check`. Add docs.

### 20.2 CHANGELOG

Add `CHANGELOG.md` and document update policy.

### 20.3 Release checklist

Add `docs/releasing.md` with steps: bump version, update baseline, run CI, tag
release.

---

## Notes (non-negotiable policies)

- **ANTLR generated code policy:** Commit generated code in
  `openehr_am/_generated/` and enforce regeneration via CI (`git diff` must be
  clean).
- **Rich output policy:** Human output uses Rich; `--json` outputs strict JSON
  only.
- **Pure Python policy:** Do not wrap Java/.NET reference implementations.
- **Python 3.14 annotations:** Avoid `from __future__ import annotations`; use
  `annotationlib` if introspection is needed.
