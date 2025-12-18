# pyopenehr-am

Pure-Python (**Python 3.14+ only**) openEHR **ADL2 / AOM2 / ODIN / BMM / OPT2**
toolkit for parsing, validation, and template compilation.

This project is intended as a **developer SDK**: teams can embed it in their own
codebases to build migration pipelines from legacy formats into openEHR, while
relying on this library for **standards-based artefact handling**
(archetypes/templates) and **validation**.

---

## What this is

A Python package that provides:

- **Parse ADL2** archetypes and templates
- **Parse ODIN** (embedded sections and BMM persistence)
- Build an in-memory **AOM2** semantic model
- Validate:
  - syntax (parser-level)
  - **AOM2 semantic validity**
  - **RM conformance** using **BMM** schemas
- Compile templates/archetypes into **OPT2** (Operational Template)

> Internal architecture: **Parse → Build AOM → Validate → Compile OPT →
> (Optional) Validate Instances**

---

## What this is NOT

- Not a “one-click database migrator”
- Not mapping logic for any specific vendor/hospital schema
- Not a wrapper around existing Java/.NET reference implementations (this repo
  is **pure Python only**)

---

## Project status

🚧 **Early stage / under active development.**\
Expect breaking changes until the first stable release.

Planned milestones and tasks live in:

- `openehr_am_toolkit_todo_checklist.md`
- `docs/issue-codes.md` and `docs/validation-rule-template.md`

---

## Install (planned)

Once published:

```bash
pip install pyopenehr-am
```

For local development (example):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

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

- `SPEC_BASELINE.md` (to be created/maintained)

Curated links live in:

- `openehr_am_resources.md`

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
