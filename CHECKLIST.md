# Continuation Checklist — pyopenehr-am

A fresh, project-specific plan for continuing development of the pure-Python
openEHR AM toolkit. Based on current code state, test coverage, and spec
requirements.

> **Next Actions:** See the prioritized list at the end of this document.

---

## How to use this checklist (sources and order)

- [ ] Keep [`SPEC_BASELINE.md`](SPEC_BASELINE.md) and [`openehr_am_resources.md`](openehr_am_resources.md) aligned with current spec URLs before starting any work.
- [ ] Re-read the pinned specs so tasks map to concrete clauses:
  - [ ] ADL2 syntax (AM 2.3.0): https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL2.html
  - [ ] AOM2 semantics (Release 2.1.0): https://specifications.openehr.org/releases/AM/Release-2.1.0/AOM2.html
  - [ ] ODIN (latest): https://specifications.openehr.org/releases/LANG/latest/odin.html
  - [ ] BMM (latest) + persistence format: https://specifications.openehr.org/releases/LANG/latest/bmm.html and https://specifications.openehr.org/releases/BASE/Release-1.0.4/bmm_persistence.html
  - [ ] OPT2 (AM 2.3.0): https://specifications.openehr.org/releases/AM/Release-2.3.0/OPT2.html
  - [ ] AQL query semantics (latest): https://specifications.openehr.org/releases/QUERY/latest/AQL.html
- [ ] For every new validation rule or compiler behavior, capture a short `# Spec:` URL comment pointing to the clause above.
- [ ] When adding fixtures or reference outputs, note the provenance (CKM URL, AWB version, or BMM repo commit) inside the test file header.

---

## Phase 1: Repo Hygiene & Documentation Alignment

- [x] Create `CHECKLIST.md` (this file)
- [x] Create `docs/MAINTENANCE_AUDIT.md` with inventory
- [x] Create `resources/` directory with provenance docs
- [x] Archive obsolete planning docs to `docs/archive/`
- [x] Update `README.md` to remove references to archived files
- [x] Update `openehr_am_resources.md` with version pins and provenance

---

## Phase 2: Specs/Resources Finalization

- [x] Verify `SPEC_BASELINE.md` has correct release versions
- [x] Verify `openehr_am_resources.md` links are current
- [ ] Add instructions for fetching BMM schemas for RM testing  
      Source: https://github.com/openEHR/specifications-ITS-BMM
- [ ] Mirror a spec-hosted BMM URL for quick tests  
      Example: https://specifications.openehr.org/releases/ITS-BMM/latest/components/RM/latest/openehr_rm_data_types.bmm
- [ ] Document how to obtain reference archetypes from CKM for testing  
      Source: https://ckm.openehr.org/ckm/ (include license note and caching strategy)
- [ ] Add a short “reading order” snippet referencing release_baseline and development_baseline indexes  
      Source: https://specifications.openehr.org/release_baseline

---

## Phase 3: Parsing (ADL2/ODIN/BMM) Milestones

- [ ] Document ANTLR regeneration workflow and pin the grammar commit hash used  
      Grammar source: https://github.com/openEHR/adl-antlr
- [ ] Add CI guard that fails if generated parsers are stale relative to pinned grammar commit

### ODIN Parser

- [x] ODIN AST dataclasses (primitives, objects, lists, keyed lists)
- [x] `parse_odin()` API returning `(OdinNode | None, list[Issue])`
- [x] ODIN parse-tree → AST visitor
- [x] ODIN serializer for round-trip testing
- [ ] Expand ODIN primitive support (duration, dates, intervals)
- [ ] Add ODIN error recovery tests for edge cases
- [ ] Add P_BMM parsing fixture to exercise ODIN persistence format  
      Source: https://specifications.openehr.org/releases/BASE/Release-1.0.4/bmm_persistence.html

### ADL2 Parser

- [x] ADL AST skeleton (header, language, description, terminology, definition)
- [x] `parse_adl()` API returning `(AdlAst | None, list[Issue])`
- [x] ADL fixtures folder (`tests/fixtures/adl/`)
- [ ] Expand cADL definition parsing coverage
- [ ] Parse `annotations` section
- [ ] Parse `component_terminologies` for templates
- [ ] Add ADL2 syntax error recovery tests using examples from the spec  
      Source: https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL2.html
- [ ] Validate that parser emits `Issue` codes matching ADL* ranges for malformed header/description sections

### AQL Parser

- [x] AQL grammar files in `grammars/aql/`
- [x] Generated AQL parser code
- [ ] AQL AST dataclasses
- [ ] `parse_aql()` API
- [ ] AQL error recovery tests
- [ ] Align AQL path parsing with QUERY latest spec examples  
      Source: https://specifications.openehr.org/releases/QUERY/latest/AQL.html

---

## Phase 4: Semantic Model Building (AOM2)

### Core AOM Types

- [x] `Archetype`, `Template` dataclasses
- [x] `CComplexObject`, `CAttribute`, `CPrimitiveObject`
- [x] `ArchetypeSlot` model
- [x] `Cardinality`, `Occurrences`, `Interval`
- [x] Terminology structures (term defs, constraint defs, value sets)
- [x] Archetype ID parsing and validation
- [ ] Add rule/statement nodes placeholder for Expression Language hooks (https://specifications.openehr.org/releases/LANG/latest/expression_language.html)
- [ ] Add support for `C_DOMAIN_TYPE` / `CONSTRAINT_BINDING` where present in AOM2

### AST → AOM Builder

- [x] Basic `build_aom_from_adl()` implementation
- [x] Source location preservation
- [ ] Improve builder error messages with better spans
- [ ] Support more cADL constraint types in builder
- [ ] Preserve differential vs flat markers to aid specialization flattening
- [ ] Ensure terminology bindings propagate from component terminologies into the AOM template model

---

## Phase 5: Validation Rules Coverage

### Validation Framework

- [x] `Issue` model with stable codes
- [x] `IssueCollector` with deterministic ordering
- [x] Validation registry with layer support (syntax/semantic/rm/opt)
- [x] `validate_syntax()`, `validate_semantic()`, `validate_rm()`, `validate_opt()`
- [ ] Document rule template with `# Spec:` comment examples drawn from `docs/validation-rule-template.md`
- [ ] Add validation trace logging toggle for debugging (kept off by default)

### Semantic Rules (AOM200-AOM299)

- [x] AOM200: Terminology references defined
- [x] AOM210: Node ID format validation
- [x] AOM230: Specialization level rules
- [x] AOM240: Duplicate node ID / path detection
- [x] AOM250: Occurrences/cardinality sanity
- [x] AOM260: Value set integrity
- [x] AOM270: Language/original_language integrity
- [x] AOM280: Template overlay/exclusion rules
- [x] AOM290: Rules reference validity
- [ ] Add more specialization redefinition checks
- [ ] Add external terminology binding validation
- [ ] Add constraint ref validity for `acNNNN`/`atNNNN` per AOM2 §4  
      Source: https://specifications.openehr.org/releases/AM/Release-2.1.0/AOM2.html
- [ ] Add rule to ensure sibling node id uniqueness within same RM type (specialization safety)

### RM Conformance (BMM500-BMM599)

- [x] BMM500: Unknown RM type
- [x] BMM510: Unknown RM attribute
- [x] BMM520: Multiplicity mismatch
- [ ] BMM530: Inheritance chain validation
- [ ] Add RM type compatibility for constraints
- [ ] Validate `existence`/`cardinality` against BMM property multiplicities  
      Source: https://specifications.openehr.org/releases/LANG/latest/bmm.html
- [ ] Add RM conformance rule ensuring terminology binding target types match RM attribute types

---

## Phase 6: Template Compilation to OPT2

### Archetype Repository

- [x] `ArchetypeRepository` loading from directory
- [x] Dependency graph and cycle detection (OPT705)
- [ ] Incremental/cached loading
- [ ] Add repository provenance metadata (source directory + timestamp) to aid reproducibility

### OPT Compiler

- [x] OPT dataclasses (`OperationalTemplate`)
- [x] OPT JSON export (deterministic)
- [x] Resolve included archetypes (OPT700)
- [x] Basic slot filling (OPT720)
- [x] Basic specialization flattening (OPT730)
- [x] OPT integrity checks (OPT750)
- [ ] Full specialization flattening rules
- [ ] Template overlay expansion
- [ ] RM-aware compilation using BMM
- [ ] Validate compiled OPT against OPT2 structural rules  
      Source: https://specifications.openehr.org/releases/AM/Release-2.3.0/OPT2.html
- [ ] Add regression fixtures comparing generated OPT JSON against ADL Workbench outputs  
      Source: https://openehr.github.io/adl-tools/adl_workbench_guide.html

---

## Phase 7: Public API Design (SDK Usability)

- [x] Stable API in `openehr_am/__init__.py`
- [x] `parse_archetype()`, `parse_template()`
- [x] `validate()` with level parameter
- [x] `load_bmm_repo()`
- [x] `compile_opt()`
- [ ] Add `validate_instance()` for data validation against OPT
- [ ] Add `to_json()` / `from_json()` for AOM serialization
- [ ] Consider adding `flatten_archetype()` for standalone flattening
- [ ] Add strict/warn-as-error toggles to CLI + API (consistent exit codes documented in `docs/cli.md`)
- [ ] Add stable JSON schema for Issue serialization for downstream tools

---

## Phase 8: Testing Strategy

### Unit Tests

- [x] ODIN parsing tests
- [x] ADL parsing tests
- [x] AOM builder tests
- [x] Validation rule tests
- [x] Path parser/resolver tests
- [x] BMM loader tests
- [x] OPT compiler tests
- [ ] Add ODIN/BMM round-trip tests using spec-hosted fixtures  
      Source: https://specifications.openehr.org/releases/ITS-BMM/latest/components/RM/latest/openehr_rm_data_types.bmm
- [ ] Add regression tests that compare Issue JSON output to a schema snapshot

### Integration Tests

- [x] Public API flow tests (`test_public_api_flow.py`)
- [ ] End-to-end CLI tests with realistic archetypes
- [ ] Add CLI `--json` output validation for lint/validate/compile-opt commands

### Corpus Tests

- [x] Corpus test harness (`tests/corpus/`)
- [ ] Add more real-world archetype samples
- [ ] Golden file comparisons for OPT output
- [ ] Add CKM-sourced corpus with provenance metadata recorded per fixture

### Property/Fuzz Tests

- [x] Fuzz test infrastructure (`tests/fuzz/`)
- [ ] Expand fuzz coverage for ODIN/ADL edge cases
- [ ] Add hypothesis property tests for validation
- [ ] Add grammar-level fuzz inputs derived from openEHR/adl-antlr examples

---

## Phase 9: Packaging/CI

### Python 3.14+ Support

- [x] `requires-python = ">=3.14"` in pyproject.toml
- [x] CI runs on Python 3.14
- [x] No `from __future__ import annotations` (test enforced)

### Tooling

- [x] ruff lint + format
- [x] pyright type checking
- [x] pytest with coverage
- [x] pre-commit hooks

### Release

- [x] PyPI publishing workflow
- [x] `docs/releasing.md` checklist
- [ ] Add CHANGELOG.md before v1.0
- [ ] Automate version bumping
- [ ] Add reproducible build documentation (exact Python version, dependency hashes)
- [ ] Pin ANTLR runtime version in `pyproject.toml` with rationale in `docs/compatibility.md`

---

## Phase 10: Examples & Migration Integration

- [x] `demo_repo/` with sample archetypes and templates
- [x] CLI quickstart in `docs/quickstart.md`
- [ ] Add migration pipeline example (legacy → openEHR)
- [ ] Add BMM repository setup example
- [ ] Add multi-template compilation example
- [ ] Add AQL query validation example using compiled OPT paths  
      Source: https://specifications.openehr.org/releases/QUERY/latest/AQL.html
- [ ] Add security considerations section to examples (handling untrusted artefacts)

---

## Next High-Leverage Tasks

**Prioritized list of 10 tasks that will move the project forward:**

1. **Document RM/CKM asset acquisition** — unblock RM validation and corpus work.
   - Deliverable: Guide covering key sources with caching/licensing notes.  
     Sources: https://github.com/openEHR/specifications-ITS-BMM and https://ckm.openehr.org/ckm/
   - Success: A new developer can fetch BMM + archetypes and run `validate_rm` following the doc.

2. **Expand cADL parsing coverage** — more constraint types per ADL2 §8.
   - Module: `openehr_am/adl/cadl_ast.py`, `openehr_am/adl/parser.py`
   - Success: Parse `C_ARCHETYPE_ROOT`, `ARCHETYPE_SLOT`, inline constraints with correct spans.

3. **Implement full specialization flattening** — required for correct OPT compilation.
   - Module: `openehr_am/opt/flattening.py`
   - Success: Child archetype flattened over parent per OPT2 spec with regression fixture.

4. **Add CLI `--json` regression tests + schema** — keep API stable for tooling.
   - Module: `tests/cli/`, `docs/cli.md`, Issue JSON schema (new)
   - Success: CLI outputs validate against schema and include deterministic ordering.

5. **Add Issue JSON schema + warn-as-error toggle** — improve SDK ergonomics.
   - Module: `openehr_am/validation/issue.py`, `docs/cli.md`
   - Success: Schema published; CLI/API honor `--strict` / `warn_as_error`.

6. **Add CKM corpus with provenance** — real-world coverage.
   - Module: `tests/corpus/`
   - Success: At least 10 CKM archetypes with recorded source URLs parsed without crashes.

7. **Add instance validation against OPT** — key feature for migration tools.
   - Module: `openehr_am/instance/` (new)
   - Success: Validate JSON instance against compiled OPT constraints.

8. **Add AQL AST + `parse_aql()`** — complete query parsing.
   - Module: `openehr_am/aql/`
   - Success: Valid queries parsed with error recovery.  
     Source: https://specifications.openehr.org/releases/QUERY/latest/AQL.html

9. **Compare OPT output with ADL Workbench** — ensure compiler fidelity.
   - Module: `openehr_am/opt/`, fixtures under `tests/fixtures/opt/`
   - Success: Generated OPT JSON matches ADL Workbench output for sample templates.  
     Source: https://openehr.github.io/adl-tools/adl_workbench_guide.html

10. **Add CHANGELOG.md + reproducible build note** — prepare for v1.0.
    - Deliverable: `CHANGELOG.md`, build inputs (Python, deps, ANTLR runtime) documented
    - Success: Release cut instructions in `docs/releasing.md` reference the changelog and pin runtime versions.
