# Continuation Checklist — pyopenehr-am

A fresh, project-specific plan for continuing development of the pure-Python
openEHR AM toolkit. Based on current code state, test coverage, and spec
requirements.

> **Next Actions:** See the prioritized list at the end of this document.

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
- [ ] Document how to obtain reference archetypes from CKM for testing

---

## Phase 3: Parsing (ADL2/ODIN/BMM) Milestones

### ODIN Parser

- [x] ODIN AST dataclasses (primitives, objects, lists, keyed lists)
- [x] `parse_odin()` API returning `(OdinNode | None, list[Issue])`
- [x] ODIN parse-tree → AST visitor
- [x] ODIN serializer for round-trip testing
- [ ] Expand ODIN primitive support (duration, dates, intervals)
- [ ] Add ODIN error recovery tests for edge cases

### ADL2 Parser

- [x] ADL AST skeleton (header, language, description, terminology, definition)
- [x] `parse_adl()` API returning `(AdlAst | None, list[Issue])`
- [x] ADL fixtures folder (`tests/fixtures/adl/`)
- [ ] Expand cADL definition parsing coverage
- [ ] Parse `annotations` section
- [ ] Parse `component_terminologies` for templates

### AQL Parser

- [x] AQL grammar files in `grammars/aql/`
- [x] Generated AQL parser code
- [ ] AQL AST dataclasses
- [ ] `parse_aql()` API
- [ ] AQL error recovery tests

---

## Phase 4: Semantic Model Building (AOM2)

### Core AOM Types

- [x] `Archetype`, `Template` dataclasses
- [x] `CComplexObject`, `CAttribute`, `CPrimitiveObject`
- [x] `ArchetypeSlot` model
- [x] `Cardinality`, `Occurrences`, `Interval`
- [x] Terminology structures (term defs, constraint defs, value sets)
- [x] Archetype ID parsing and validation

### AST → AOM Builder

- [x] Basic `build_aom_from_adl()` implementation
- [x] Source location preservation
- [ ] Improve builder error messages with better spans
- [ ] Support more cADL constraint types in builder

---

## Phase 5: Validation Rules Coverage

### Validation Framework

- [x] `Issue` model with stable codes
- [x] `IssueCollector` with deterministic ordering
- [x] Validation registry with layer support (syntax/semantic/rm/opt)
- [x] `validate_syntax()`, `validate_semantic()`, `validate_rm()`, `validate_opt()`

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

### RM Conformance (BMM500-BMM599)

- [x] BMM500: Unknown RM type
- [x] BMM510: Unknown RM attribute
- [x] BMM520: Multiplicity mismatch
- [ ] BMM530: Inheritance chain validation
- [ ] Add RM type compatibility for constraints

---

## Phase 6: Template Compilation to OPT2

### Archetype Repository

- [x] `ArchetypeRepository` loading from directory
- [x] Dependency graph and cycle detection (OPT705)
- [ ] Incremental/cached loading

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

### Integration Tests

- [x] Public API flow tests (`test_public_api_flow.py`)
- [ ] End-to-end CLI tests with realistic archetypes

### Corpus Tests

- [x] Corpus test harness (`tests/corpus/`)
- [ ] Add more real-world archetype samples
- [ ] Golden file comparisons for OPT output

### Property/Fuzz Tests

- [x] Fuzz test infrastructure (`tests/fuzz/`)
- [ ] Expand fuzz coverage for ODIN/ADL edge cases
- [ ] Add hypothesis property tests for validation

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

---

## Phase 10: Examples & Migration Integration

- [x] `demo_repo/` with sample archetypes and templates
- [x] CLI quickstart in `docs/quickstart.md`
- [ ] Add migration pipeline example (legacy → openEHR)
- [ ] Add BMM repository setup example
- [ ] Add multi-template compilation example

---

## Next High-Leverage Tasks

**Prioritized list of 10 tasks that will move the project forward:**

1. **Expand cADL parsing coverage** — More constraint types means more useful
   validation. See ADL2 spec section on cADL.
   - Module: `openehr_am/adl/cadl_ast.py`, `openehr_am/adl/parser.py`
   - Success: Parse `C_ARCHETYPE_ROOT`, `ARCHETYPE_SLOT`, inline constraints

2. **Add corpus tests with real CKM archetypes** — Validate parser against
   production archetypes.
   - Module: `tests/corpus/`
   - Success: Parse 10+ diverse archetypes from openEHR CKM without crashes

3. **Implement full specialization flattening** — Required for correct OPT
   compilation.
   - Module: `openehr_am/opt/flattening.py`
   - Success: Flatten child archetype over parent correctly

4. **Add instance validation against OPT** — Key feature for migration tools.
   - Module: `openehr_am/instance/` (new)
   - Success: Validate JSON instance against compiled OPT constraints

5. **Document BMM schema setup** — Enable RM validation testing.
   - Deliverable: Guide in `docs/` for downloading and using BMM schemas
   - Success: Users can run RM validation with official BMM files

6. **Add AQL parsing support** — Complete the parser suite.
   - Module: `openehr_am/aql/`
   - Success: `parse_aql()` returns AST for valid queries

7. **Add CHANGELOG.md** — Prepare for v1.0 release.
   - Deliverable: `CHANGELOG.md` following Keep a Changelog format
   - Success: Document all changes since v0.0.1

8. **Expand CLI with --verbose and --quiet modes** — Better UX for different use
   cases.
   - Module: `openehr_am/cli/`
   - Success: Verbose shows all issues; quiet shows only errors

9. **Add migration pipeline example** — Demonstrate SDK usage.
   - Deliverable: Example in `examples/` showing data transformation
   - Success: Working example that transforms sample data

10. **Improve error messages with code snippets** — Better developer experience.
    - Module: `openehr_am/validation/issue.py`
    - Success: Issues include source code context when available
