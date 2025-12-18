# Architecture

pyopenehr-am is **pure Python only** and targets **Python 3.14+ only**.

The library is organized as a compiler-style pipeline:

**Parse → Build AOM → Validate → Compile OPT → (Optional) Validate Instances**

```text
           ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
ADL2/ODIN  │ Parse        │     │ Build AOM    │     │ Validate         │     │ Compile OPT  │
text  ───▶ │ (adl/odin/)  ├───▶ │ (aom/)       ├───▶ │ (validation/ +   ├───▶ │ (opt/+ json) │
           └──────────────┘     └──────────────┘     │  bmm/ for RM)    │     └──────────────┘
                                                     └──────────────────┘

Diagnostics: every stage emits structured Issues (no exceptions for invalid artefacts).
```

For background on the standards, see https://specifications.openehr.org/

## Module boundaries

The top-level package is structured by pipeline stage. Most users should only
need the stable public API in `openehr_am/__init__.py`.

- `openehr_am/adl/`: ADL2 parsing. Produces syntax AST nodes with source spans.
- `openehr_am/odin/`: ODIN parsing + emitting (used by ADL and standalone ODIN
  use-cases).
- `openehr_am/aom/`: Semantic object model (AOM2-ish) and builders that
  transform syntax AST → AOM.
- `openehr_am/validation/`: Validation rules that operate at different pipeline
  levels and return `Issue` objects (no exceptions for invalid artefacts).
- `openehr_am/bmm/`: BMM repository loading and lookup primitives used by RM
  conformance checks.
- `openehr_am/opt/`: Template flattening/compilation to Operational Template
  (OPT2-ish) and JSON serialization helpers.
- `openehr_am/path/`: openEHR path parsing/normalization/resolution.
- `openehr_am/aql/`: AQL parsing.
- `openehr_am/antlr/`: Shared ANTLR runtime helpers and `Span` primitives (used
  by generated parsers).
- `openehr_am/_generated/`: Committed generated parser code (never edit by
  hand).
- `openehr_am/cli/`: Typer-based CLI that wraps the stable public API and
  renders Issues either as Rich tables or strict JSON (`--json` /
  `--format json`).

### Diagnostics boundary (non-negotiable)

All recoverable problems are reported as structured `Issue` objects:

- Stable `code` + `severity` + message
- Best-effort location (`file`, `line`, `col`, optional end span)

This keeps parsing/validation usable as a library (callers can collect Issues)
and as a CLI (Issues can be rendered as tables or JSON).

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

## Pipeline walkthrough (Parse → AOM → Validate → OPT)

This is the intended end-to-end flow and the primary object types passed between
layers.

1. Parse text

- ADL2: `openehr_am.adl` returns a syntax artefact + Issues.
- ODIN: `openehr_am.odin` returns an ODIN AST + Issues.

2. Build semantic model (AOM)

- `openehr_am.aom.builder` converts ADL syntax artefacts into semantic AOM
  objects (`Archetype` or `Template`).

3. Validate

- Syntax: validate raw ADL text or a file path.
- Semantic: validate an AOM `Archetype` / `Template`.
- RM: validate an AOM object using a loaded BMM repo (`openehr_am.bmm`).
- OPT: validate an `OperationalTemplate` produced by compilation.

4. Compile OPT (template-focused)

- `openehr_am.opt.compiler` compiles a `Template` plus an archetype repository
  into an `OperationalTemplate`.
- `openehr_am.opt.json` provides deterministic JSON export.

## Public API surface

Until v1.0, the stable entry points are:

- `parse_archetype`, `parse_template`
- `validate(obj, level=..., rm=...)`
- `load_bmm_repo(dir)`
- `compile_opt(template, archetype_dir=..., rm=...)`

Everything else should be treated as internal plumbing unless you are extending
the toolkit itself.
