# pyopenehr-am

[![CI](https://github.com/rubentalstra/pyopenehr-am/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rubentalstra/pyopenehr-am/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pyopenehr-am)](https://pypi.org/project/pyopenehr-am/)
![Python](https://img.shields.io/badge/Python-3.14%2B-blue)
[![License: MIT](https://img.shields.io/github/license/rubentalstra/pyopenehr-am)](LICENSE)
![Ruff](https://img.shields.io/badge/code%20style-ruff-261230)
![Pyright](https://img.shields.io/badge/type%20checker-pyright-4B32C3)

Pure-Python (**Python 3.14+ only**) openEHR **ADL2 / AOM2 / ODIN / BMM / OPT2**
toolkit. Parse and validate archetypes/templates, and compile templates to
**OPT2**.

This project is intended as a **developer SDK**: teams can embed it in their own
codebases to build migration pipelines from legacy formats into openEHR, while
relying on this library for **standards-based artefact handling**
(archetypes/templates) and **validation**.

---

## Why this exists

When building migration tooling, you usually want openEHR artefact handling to
be: predictable, standards-driven, and easy to embed. This repo focuses on that
core plumbing (parsing, semantic model building, validation, and OPT
compilation).

## What it provides

Core capabilities:

- **Parse ADL2** archetypes and templates
- **Parse ODIN** (embedded sections and BMM persistence)
- Build an in-memory **AOM2** semantic model
- Validate syntax + semantics, and (optionally) **RM conformance** via **BMM**
- Compile templates to **OPT2** (Operational Template)

> Internal architecture: **Parse → Build AOM → Validate → Compile OPT →
> (Optional) Validate Instances**

---

## Non-goals

- Not a “one-click database migrator”
- Not mapping logic for any specific vendor/hospital schema
- Not a wrapper around existing non-Python reference implementations (this repo
  is **pure Python only**)

---

## Project status

**Alpha / under active development.** Expect breaking changes until the first
stable release.

If you need something to be stable long-term, pin versions and treat the public
API as the contract.

Documentation entry points:

- [docs/quickstart.md](docs/quickstart.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/compatibility.md](docs/compatibility.md)

Planned milestones and tasks live in:

- [openehr_am_toolkit_todo_checklist.md](openehr_am_toolkit_todo_checklist.md)
- [docs/issue-codes.md](docs/issue-codes.md) and
  [docs/validation-rule-template.md](docs/validation-rule-template.md)

---

## Install

```bash
pip install pyopenehr-am
```

Verify the CLI:

```bash
openehr-am --help
```

For local development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

---

## Quickstart

The quickest way to see behavior is via the CLI. The Quickstart includes:

- `openehr-am lint` (syntax parsing, JSON Issue output)
- `openehr-am validate` (semantic + optional RM checks)
- `openehr-am compile-opt` (template → OPT2 JSON)

Start here: [docs/quickstart.md](docs/quickstart.md)

---

## Python API (minimal example)

The stable public API is exposed from the top-level package.

```python
from openehr_am import parse_archetype, validate

archetype, parse_issues = parse_archetype(path="demo.archetype.adl")
if archetype is None:
    # parse_issues contains structured diagnostics
    raise SystemExit(1)

issues = validate(archetype, level="all")
```

More examples: [docs/quickstart.md](docs/quickstart.md)

---

## Diagnostics and Issue Codes

All recoverable problems are returned as structured **Issue** objects, with:

- stable `code` (e.g., `ADL001`, `AOM200`, `BMM500`, `OPT700`)
- severity (`INFO|WARN|ERROR`)
- best-effort file/line/col and optional path/node_id

See:

- `docs/issue-codes.md` — canonical registry
- `docs/validation-rule-template.md` — how to add rules

---

## Specs and references

This repo is **standards-driven**. Pin the exact spec releases you implement in:

- [`SPEC_BASELINE.md`](SPEC_BASELINE.md)

Curated links live in:

- [`openehr_am_resources.md`](openehr_am_resources.md)

---

## Security

This project parses untrusted artefacts and treats invalid input as data: most
errors are returned as `Issue` objects (not exceptions).

Security policy / reporting: [SECURITY.md](SECURITY.md)

Engineering notes: [docs/security.md](docs/security.md)

---

## Contributing

Contributions are welcome.

Guidelines:

- Keep diffs small and test-backed
- Use stable Issue codes (update `docs/issue-codes.md`)
- Add a short `# Spec:` URL comment for new validation rules
- Do not edit generated parser code under `openehr_am/_generated/`

---

## License

[MIT](LICENSE)

---

## Acknowledgements

- openEHR specifications and community resources (see `openehr_am_resources.md`)
