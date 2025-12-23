# openEHR AM Toolkit — Reference Resources

Curated links to **official openEHR specifications**, **schemas**, **grammars**,
**tools**, and **community resources** relevant to implementing a **pure-Python
ADL2/AOM2 validator + OPT2 compiler**.

> **Important:** This project pins specific specification releases in
> [`SPEC_BASELINE.md`](SPEC_BASELINE.md). Use those pinned URLs for implementation
> references. This document provides a broader resource index.

> **Last reviewed:** December 2023

---

## Provenance and Versioning

### What This Repo Pins (Authoritative)

See [`SPEC_BASELINE.md`](SPEC_BASELINE.md) for the exact specification versions
this project implements. Those URLs should be used in code comments and
validation rule references.

### External vs Vendored Resources

| Resource Type | Status | Location |
|--------------|--------|----------|
| Specifications (HTML) | External link only | Links below |
| ANTLR grammars | Vendored in `grammars/` | Local copies |
| BMM schemas | External link only | User-supplied |
| Test archetypes | Minimal fixtures in `tests/fixtures/` | Local copies |

---

## 1) Specifications (Primary Sources)

### 1.1 Archetype Modeling (AM)

- **ADL2 (Archetype Definition Language 2)** — latest:\
  https://specifications.openehr.org/releases/AM/latest/ADL2.html
- **OPT2 (Operational Template 2)** — released (AM 2.3.0):\
  https://specifications.openehr.org/releases/AM/Release-2.3.0/OPT2.html
- **Archetype Identification** — released (AM 2.3.0):\
  https://specifications.openehr.org/releases/AM/latest/Identification.html
- **Archetype Technology Overview** (conceptual + implementer guidance):\
  https://specifications.openehr.org/releases/AM/latest/Overview.html
- **AM release index (shows released vs development versions):**\
  https://specifications.openehr.org/releases/AM/Release-2.3.0

### 1.2 AOM2 (Archetype Object Model 2 — the semantic “truth”)

- **AOM2 (Release 2.1.0 HTML)** (stable reference for semantics + validity
  rules):\
  https://specifications.openehr.org/releases/AM/Release-2.1.0/AOM2.html

> Note: the openEHR spec site also publishes “development” views of AOM2 via the
> `classes/` pages, but for implementation baselines it’s best to pin a released
> spec.

### 1.3 Generic Languages (LANG)

- **ODIN (Object Data Instance Notation)** — latest:\
  https://specifications.openehr.org/releases/LANG/latest/odin.html
- **BMM (Basic Meta-Model)** — latest:\
  https://specifications.openehr.org/releases/LANG/latest/bmm.html
- **P_BMM / BMM Persistence Model and Syntax** (ODIN-like save format used in
  practice):\
  https://specifications.openehr.org/releases/BASE/Release-1.0.4/bmm_persistence.html
- **Expression Language (EL)** — latest:\
  https://specifications.openehr.org/releases/LANG/latest/expression_language.html
- **BEL (Basic Expression Language)** — latest:\
  https://specifications.openehr.org/releases/LANG/latest/BEL.html

### 1.4 Query (Useful for path semantics and testing)

- **AQL (Archetype Query Language)** — latest:\
  https://specifications.openehr.org/releases/QUERY/latest/AQL.html
- **AQL Examples** (handy for understanding path usage in queries):\
  https://specifications.openehr.org/releases/QUERY/Release-1.1.0/AQL_examples.html

### 1.5 Baselines / “what’s current”

- **Release baseline index:**\
  https://specifications.openehr.org/release_baseline
- **Development baseline index:**\
  https://specifications.openehr.org/development_baseline

---

## 2) Grammar Repositories (For Building Parsers in Python)

These are the go-to sources for ANTLR grammars and related test assets.

- **openEHR/adl-antlr** — ANTLR4 grammars for ADL (ADL2-focused):\
  https://github.com/openEHR/adl-antlr
- **openEHR/openEHR-antlr4** — broader development repo for multiple openEHR
  syntaxes:\
  https://github.com/openEHR/openEHR-antlr4

Suggested approach for your project:

- Generate Python parsers from ANTLR4 grammars
- Convert parse trees → your own AST
- Build AOM2 dataclasses from AST
- Validate using AOM2 rules + RM schemas via BMM

---

## 3) RM Schemas and Meta-Models (BMM Files)

### 3.1 Official BMM schema repository

- **openEHR/specifications-ITS-BMM** — canonical place to get RM schemas in BMM
  form:\
  https://github.com/openEHR/specifications-ITS-BMM

### 3.2 Direct BMM assets on the spec site

- **ITS-BMM component index:**\
  https://specifications.openehr.org/releases/ITS-BMM/development
- Example BMM file (datatypes) served from specs site:\
  https://specifications.openehr.org/releases/ITS-BMM/latest/components/RM/latest/openehr_rm_data_types.bmm

---

## 4) Tooling (Great for Comparison Testing / Gold Standards)

Even if you’re writing pure Python, these tools are excellent for:

- generating reference outputs
- comparing diagnostics
- building test corpora

- **ADL Workbench (AWB) user guide:**\
  https://openehr.github.io/adl-tools/adl_workbench_guide.html
- **ADL Workbench source repo (adl-tools):**\
  https://github.com/openEHR/adl-tools
- **openEHR modelling tools page (overview):**\
  https://openehr.org/modelling-tools/
- **openEHR Archetype Designer (web tool):**\
  https://www.openehr.org/archetypedesigner
- **CKM (Clinical Knowledge Manager)** — archetypes/templates repository:\
  https://ckm.openehr.org/ckm/

---

## 5) Community & Support (Where Implementers Hang Out)

- **openEHR Discourse (forums):**\
  https://discourse.openehr.org/
- **Tool Support category:**\
  https://discourse.openehr.org/c/tool-support/29

Useful threads (for Python parser efforts and pitfalls):

- “ADL parser for python” (community discussion):\
  https://discourse.openehr.org/t/adl-parser-for-python/5528

---

## 6) Suggested Reading Order (Practical)

If you’re implementing a validator/compiler from scratch:

1. ADL2 spec (syntax + sections + rules references)\
   https://specifications.openehr.org/releases/AM/latest/ADL2.html
2. AOM2 spec (what the AST _means_ and what “valid” means)\
   https://specifications.openehr.org/releases/AM/Release-2.1.0/AOM2.html
3. ODIN spec (because ADL2 embeds it, and BMM uses it)\
   https://specifications.openehr.org/releases/LANG/latest/odin.html
4. BMM + P_BMM (to load RM schemas and validate RM conformance)\
   https://specifications.openehr.org/releases/LANG/latest/bmm.html\
   https://specifications.openehr.org/releases/BASE/Release-1.0.4/bmm_persistence.html
5. OPT2 spec (compile templates → operational template)\
   https://specifications.openehr.org/releases/AM/Release-2.3.0/OPT2.html
6. BEL/EL (only once you need to validate/interpret rules sections deeply)\
   https://specifications.openehr.org/releases/LANG/latest/BEL.html\
   https://specifications.openehr.org/releases/LANG/latest/expression_language.html

---

## 7) How to Use These Resources in Your Repo

- Keep a `SPEC_BASELINE.md` and pin:
  - the openEHR release(s) you conform to
  - the exact URLs you used
  - the date you last reviewed them
- Add `docs/compatibility.md`:
  - supported ADL versions (e.g., ADL2 only at first)
  - supported OPT2 features (raw OPT vs profiled OPT, etc.)
  - supported BMM schema versions/releases

---

## 8) Handy Link Index (Copy/Paste)

**Pinned releases (use in code comments):**

| Spec | Pinned URL |
|------|------------|
| ADL2 | https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL2.html |
| AOM2 | https://specifications.openehr.org/releases/AM/Release-2.3.0/AOM2.html |
| OPT2 | https://specifications.openehr.org/releases/AM/Release-2.3.0/OPT2.html |
| ODIN | https://specifications.openehr.org/releases/LANG/Release-1.0.0/odin.html |
| BMM | https://specifications.openehr.org/releases/LANG/Release-1.0.0/bmm.html |

**Repositories:**

- ITS-BMM schemas: https://github.com/openEHR/specifications-ITS-BMM
- adl-antlr grammars: https://github.com/openEHR/adl-antlr
- adl-tools (reference impl): https://github.com/openEHR/adl-tools
- CKM (archetypes): https://ckm.openehr.org/ckm/
- Discourse (community): https://discourse.openehr.org/
