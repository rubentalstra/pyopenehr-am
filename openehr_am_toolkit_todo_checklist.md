# openEHR AM Toolkit (Pure Python) — TODO / Checklist

A repository checklist for building a **pure-Python** toolkit that:

- Parses **ADL2** (archetypes/templates) and embedded **ODIN**
- Builds an **AOM2** in-memory model
- Validates artefacts (syntax + semantics + RM conformance)
- Compiles **OPT2** (Operational Templates)
- Exposes a developer-friendly **Python API + CLI**

> **Important:** This checklist is for _building the package itself_. Your users
> will call your Python API/CLI; they won’t implement these steps manually.
>
> Internally, your package should behave like a compiler pipeline: **Parse →
> Build AOM → Validate → Compile OPT → (Optional) Validate Instances**
>
> - **Compile OPT** = compile templates/archetypes into an **Operational
>   Template** used for runtime validation.
> - **Validate Instances (optional)** = validate the _composition JSON/object_
>   that a migration tool produces against the OPT.

---

## 0. Project Setup

- [ ] Create repo structure
  - [ ] `openehr_am/`
  - [ ] `openehr_am/odin/`
  - [ ] `openehr_am/adl/`
  - [ ] `openehr_am/aom/`
  - [ ] `openehr_am/bmm/`
  - [ ] `openehr_am/validation/`
  - [ ] `openehr_am/opt/`
  - [ ] `openehr_am/path/`
  - [ ] `openehr_am/cli/`
  - [ ] `tests/`
  - [ ] `docs/`
- [ ] Choose license (e.g., MIT)
- [ ] Pick Python support policy (e.g., 3.12+)
- [ ] Add standard tooling
  - [ ] `pyproject.toml` (build, deps)
  - [ ] Formatting: `ruff` + `black` (or `ruff format`)
  - [ ] Type checking: `pyright`
  - [ ] Testing: `pytest`
  - [ ] CI (GitHub Actions) running lint + tests
- [ ] Add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`
- [ ] Add `CHANGELOG.md` (Keep a Changelog format)

---

## 1. Spec Baseline (Pinned Versions)

- [ ] Create `SPEC_BASELINE.md` documenting pinned spec releases:
  - [ ] ADL2 (archetypes + templates)
  - [ ] AOM2 (semantic model + validity rules)
  - [ ] ODIN (serialization syntax used within ADL + BMM)
  - [ ] OPT2 (operational templates)
  - [ ] BMM (RM schema representation)
  - [ ] Expression Language / Rules (defer if needed)
- [ ] Add a repo policy: **no changing spec baselines without a version bump**
- [ ] Add `docs/glossary.md` (ADL, AOM, RM, BMM, OPT, archetype vs template)

---

## 2. Core Data Structures

### 2.1 Diagnostics & Error Reporting (First, so everything uses it)

- [ ] Implement common `Issue` model (dataclass)
  - [ ] `code`, `message`, `severity` (`INFO|WARN|ERROR`)
  - [ ] `file`, `line`, `col`, `span`
  - [ ] `aql_path` / `adl_path` (optional)
  - [ ] `node_id` (optional)
- [ ] Implement `IssueCollector` helper
- [ ] Implement exception types
  - [ ] `ParseError`, `ValidationError`, `CompileError`

### 2.2 Source Locations Everywhere

- [ ] Ensure every AST/AOM node can optionally carry:
  - [ ] `source_file`, `line`, `col`, `end_line`, `end_col`

---

## 3. Parsing Layer

### 3.1 Integrate ANTLR Grammars

- [ ] Add ANTLR4 toolchain to dev workflow
  - [ ] Document how to regenerate parsers
- [ ] Generate Python parsers from ADL/ODIN grammars
  - [ ] Commit generated code or generate in CI (decide + document)

### 3.2 ODIN Parser + AST

- [ ] Implement `odin.parse(text) -> OdinNode`
- [ ] Support ODIN primitives
      (string/int/float/bool/date/time/datetime/duration)
- [ ] Support ODIN structures (objects, lists, keyed lists)
- [ ] Add robust syntax error recovery and diagnostics
- [ ] Unit tests: minimal ODIN snippets + malformed cases

### 3.3 ADL2 Parser + AST

- [ ] Implement `adl.parse(text) -> AdlAst`
- [ ] Capture:
  - [ ] archetype/template header
  - [ ] language/description sections (ODIN blocks)
  - [ ] terminology section (ODIN blocks)
  - [ ] definition section (cADL)
  - [ ] rules section (can defer semantics v1)
  - [ ] annotations (ODIN)
- [ ] Unit tests: minimal archetype fixtures + malformed cases

---

## 4. AOM2 Model (In-Memory Semantic Objects)

### 4.1 Minimal AOM2 Types (MVP)

- [ ] Implement dataclasses for:
  - [ ] `Archetype`, `Template`
  - [ ] `CArchetypeRoot`
  - [ ] `CComplexObject`, `CAttribute`
  - [ ] `CPrimitiveObject` (and primitive constraints)
  - [ ] `ArchetypeSlot`
  - [ ] `Cardinality`, `Occurrences`, `Interval`
  - [ ] Terminology structures:
    - [ ] term defs (`atNNNN`)
    - [ ] constraint defs (`acNNNN`)
    - [ ] value sets, term bindings
- [ ] Implement identifiers
  - [ ] archetype id parsing + validation
  - [ ] specialization depth / parent id support

### 4.2 AST → AOM Builder

- [ ] Implement `build_aom(adl_ast) -> Archetype|Template`
- [ ] Preserve source locations and original codes
- [ ] Add builder tests (round-trip sanity on small samples)

---

## 5. Validation (Layered)

### 5.1 Syntax Validation (Parser-Level)

- [ ] Expose parser diagnostics via unified `Issue` model
- [ ] Provide `validate_syntax(text|path)`

### 5.2 AOM2 Semantic Validation (Core)

Implement as independent checks that return `Issue`s.

- [ ] Structural validity
  - [ ] missing/duplicate sections
  - [ ] invalid node id formats
  - [ ] invalid occurrences/cardinalities
- [ ] Terminology integrity
  - [ ] every `at`/`ac` referenced exists in terminology
  - [ ] value sets well-formed
  - [ ] bindings consistent
- [ ] Path integrity
  - [ ] paths resolve against definition tree
  - [ ] no duplicate paths where forbidden
- [ ] Specialisation rules
  - [ ] valid parent archetype id linkage
  - [ ] specialization level rules for codes
  - [ ] redefinition rules respected
- [ ] Template-specific rules (MVP subset)
  - [ ] no illegal exclusions
  - [ ] slot fillings valid (basic)

Deliverable:

- [ ] `validate_aom(aom_obj) -> list[Issue]`

### 5.3 Path Parser/Resolver

- [ ] Implement path grammar (openEHR path syntax)
- [ ] `parse_path(str) -> PathExpr`
- [ ] `resolve_path(aom_obj, path) -> node(s)`
- [ ] Tests: common path patterns + edge cases

---

## 6. RM Awareness via BMM (Reference Model Conformance)

### 6.1 BMM Loader

- [ ] Implement `bmm.load(text|path) -> BmmModel`
  - [ ] BMM is ODIN-based; reuse ODIN parser output
- [ ] Support:
  - [ ] packages, classes, properties
  - [ ] generics where present
  - [ ] inheritance
  - [ ] multiplicities
- [ ] Create `ModelRepository`
  - [ ] load a folder of BMM schemas
  - [ ] resolve class references across packages

### 6.2 RM Conformance Validator

- [ ] Validate that AOM constraint nodes reference valid RM types
  - [ ] `rm_type_name` exists
  - [ ] `rm_attribute_name` exists on that type
  - [ ] attribute/containment multiplicities align
- [ ] Add tests using a small BMM fixture + minimal archetype

Deliverable:

- [ ] `validate_rm(aom_obj, model_repo) -> list[Issue]`

---

## 7. OPT2 Compiler (Templates + Archetypes → Operational Template)

### 7.1 Repository Model

- [ ] Implement `ArchetypeRepository`
  - [ ] load all `.adl` under a directory
  - [ ] index by archetype id
  - [ ] dependency resolution

### 7.2 Flattening & Expansion (MVP)

- [ ] Implement OPT compilation pipeline:
  - [ ] resolve `use_archetype` / inclusion points
  - [ ] fill `ArchetypeSlot` with chosen archetypes
  - [ ] flatten specialization (differential → flat)
  - [ ] remove excluded nodes
  - [ ] normalize paths/node ids
- [ ] Define `OperationalTemplate` dataclasses (OPT2 subset)
- [ ] Serialization
  - [ ] `opt.to_json()` (MVP)
  - [ ] `opt.to_odin()` (optional later)

Deliverable:

- [ ] `compile_opt(template, archetype_repo, model_repo) -> OperationalTemplate`

### 7.3 OPT Validation

- [ ] Validate compiled OPT internal integrity
- [ ] Cross-check: required nodes present, no broken references

---

## 8. Public API (Pythonic)

- [ ] Define stable API surface in `openehr_am/__init__.py`
- [ ] Core functions:
  - [ ] `parse_archetype(path|text) -> Archetype`
  - [ ] `parse_template(path|text) -> Template`
  - [ ] `validate(obj, *, level="syntax|semantic|rm|all") -> list[Issue]`
  - [ ] `compile_opt(template, *, archetype_dir, bmm_dir) -> OperationalTemplate`
- [ ] Add convenience helpers:
  - [ ] `Issue.pretty()` for human-readable output
  - [ ] `Issue.to_dict()` for JSON logging
- [ ] Add “strict mode” and “warnings as errors” options

---

## 9. CLI

- [ ] `openehr-am lint <file.adl>`
- [ ] `openehr-am validate <file.adl> [--rm <bmm_dir>]`
- [ ] `openehr-am compile-opt <template.adl> --repo <archetypes_dir> --rm <bmm_dir> --out <opt.json>`
- [ ] Exit codes:
  - [ ] `0` success
  - [ ] `1` errors present
  - [ ] `2` usage/IO errors
- [ ] Ensure CLI prints useful diagnostics (file:line:col)

---

## 10. Test Plan (Conformance & Quality)

### 10.1 Unit Tests

- [ ] ODIN: primitives, nested structures, error recovery
- [ ] ADL: small archetype fixtures, terminology references, malformed cases
- [ ] AOM builder: AST → AOM sanity checks
- [ ] Validators: targeted rule tests

### 10.2 Golden Corpus Tests

- [ ] Create `tests/corpus/`
- [ ] Add a corpus loader and run:
  - [ ] parse all files
  - [ ] validate all files
  - [ ] compile OPT for selected templates
- [ ] Track failures with snapshot-friendly output

### 10.3 Property / Fuzz Testing (Later)

- [ ] Fuzz ODIN and ADL parsers for crashes
- [ ] Ensure invalid inputs produce issues, not exceptions

---

## 11. Documentation

- [ ] `README.md`
  - [ ] what this project is / is not
  - [ ] supported specs and versions (link to `SPEC_BASELINE.md`)
  - [ ] install + quickstart examples
- [ ] `docs/architecture.md` (pipeline diagram)
- [ ] `docs/api.md` (public API)
- [ ] `docs/cli.md` (commands and exit codes)
- [ ] `docs/validation_levels.md` (what each validation level guarantees)
- [ ] `docs/opt_compilation.md` (what “compile” means)

---

## 12. Packaging & Releases

- [ ] Publish to PyPI
- [ ] Semantic versioning
- [ ] Wheels for major platforms
- [ ] Version pinning for ANTLR runtime dependency
- [ ] Add `openehr-am --version` output (includes spec baseline id/hash)

---

## 13. Optional (Highly Valuable) Extensions

### 13.1 Instance Validation vs OPT (for migration builders)

- [ ] Define a simple “instance model” (likely JSON input)
- [ ] Validate JSON instances against OPT constraints
- [ ] Helpful for people transforming legacy data into openEHR compositions

### 13.2 Expression Language / Rules Semantics

- [ ] Parse rules sections
- [ ] Validate rule references and types
- [ ] Evaluate rules (optional; big scope)

### 13.3 AQL Helpers (Out of Scope for MVP)

- [ ] Provide path → AQL snippet helpers
- [ ] Not required for archetype/template validation

---

## “Definition of Done” for v1.0

- [ ] Can parse ADL2 and ODIN reliably (no crashes on malformed input)
- [ ] Builds AOM2 objects for archetypes and templates
- [ ] Validates:
  - [ ] syntax
  - [ ] AOM2 semantics (core rule set)
  - [ ] RM conformance using BMM
- [ ] Compiles OPT2 (minimum viable operational template)
- [ ] CLI works with clear diagnostics and correct exit codes
- [ ] Test suite includes unit tests + corpus tests
- [ ] Docs cover installation, API, CLI, and spec baseline

---

## Notes / Decisions Log

- [ ] Decide whether to commit generated ANTLR parser code to the repo
- [ ] Decide JSON formats (AOM/OPT) for serialization; document them
- [ ] Decide whether “warnings” should fail CI or not
- [ ] Decide how to ship BMM schemas (bundle vs user-supplied)
