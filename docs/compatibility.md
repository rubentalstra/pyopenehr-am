# Compatibility & stability (pre-1.0)

pyopenehr-am is a **pure-Python** toolkit targeting **Python 3.14+**.

Until version **1.0**, the project is still converging on full
ADL2/AOM2/BMM/OPT2 coverage. This document describes what is considered
**stable**, what may change, and how we communicate breaking changes.

## Stability scopes

### Stable public API

The following names are the **stable public API** until v1.0:

- `openehr_am.parse_archetype(...)`
- `openehr_am.parse_template(...)`
- `openehr_am.validate(obj, level=..., rm=...)`
- `openehr_am.load_bmm_repo(dir)`
- `openehr_am.compile_opt(template, archetype_dir=..., rm=...)`

We aim to keep:

- function names and signatures stable
- return shapes stable (notably returning `Issue` objects for recoverable
  problems)
- Issue `code` values stable (see [issue-codes.md](issue-codes.md))

### Internal / non-stable API

Everything else is considered **internal** and may change at any time before
v1.0, including (but not limited to):

- subpackage module layouts
- helper functions and registry implementation details
- intermediate syntax AST structures

The internal architecture still follows the project pipeline:

**Parse → Build AOM → Validate → Compile OPT**

## Experimental policy

Some features are intentionally shipped as **experimental** prior to v1.0:

- incomplete spec subsets (e.g. partial ADL2/cADL support)
- new validation rules and new validation layers
- template compilation features beyond the MVP compiler

Experimental behavior can change in minor releases. When a behavior becomes
stable, it is exposed (or kept) behind the stable public API listed above.

## Versioning and breaking changes

We follow Semantic Versioning (SemVer) conventions, with the caveat that pre-1.0
releases may still introduce breaking changes.

- We avoid breaking changes to the **stable public API**.
- If we must break it pre-1.0, it will be called out prominently in release
  notes.
- Breaking changes outside the stable public API may occur as the implementation
  evolves.

## Backwards compatibility expectations

- **Python**: only Python 3.14+ is supported.
- **Diagnostics**: for recoverable problems, callers should expect `Issue`
  objects rather than exceptions.
- **Determinism**: ordering of returned issues is intended to be deterministic.

## How to depend on pyopenehr-am pre-1.0

- Depend only on the stable public API.
- Treat other modules as internal implementation details.
- Pin versions if you rely on experimental behavior.
