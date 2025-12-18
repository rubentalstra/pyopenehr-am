# Architecture

pyopenehr-am is **pure Python only** and targets **Python 3.14+ only**.

The library is organized as a compiler-style pipeline:

**Parse → Build AOM → Validate → Compile OPT → (Optional) Validate Instances**

For background on the standards, see https://specifications.openehr.org/

## Layers

### Parsing

- Inputs: ADL2, ODIN (text)
- Outputs: syntax AST with source spans
- No semantic validation here

### Semantic model (AOM2)

- Converts syntax AST into a semantic representation suitable for validation and
  compilation.

### Validation

- Syntax issues: parser output
- Semantic issues: AOM2 validity rules
- RM conformance: BMM-backed type/property checks
- OPT integrity: compiler output consistency checks

### OPT compilation

- Inputs: Template + archetypes + RM schemas
- Output: Operational Template (OPT) structure with deterministic JSON export
