# Architecture Map (pyopenehr-am)

This map summarizes the major subsystems, their responsibilities, and the
high-leverage files that most often need specification citations.

## Module tree (high level)

- `openehr_am/adl/` — ADL2 parsing and cADL AST.
- `openehr_am/odin/` — ODIN parsing and AST.
- `openehr_am/antlr/` — shared lexer/parser helpers and spans.
- `openehr_am/aom/` — Archetype Object Model (semantic objects).
- `openehr_am/validation/` — validation layers (syntax, semantic, RM, OPT).
- `openehr_am/bmm/` — BMM loading and RM repository.
- `openehr_am/opt/` — OPT2 compiler and operational template model.
- `openehr_am/path/` — openEHR path parsing/resolution.
- `openehr_am/cli/` — Typer CLI entrypoints.
- `openehr_am/aql/` — AQL grammar scaffolding (AST/parse WIP).

## Responsibilities (per subsystem)

- **ADL2 parsing (`adl/`)**: parse artefact headers/sections, minimal cADL subset,
  surface Issues instead of exceptions.
- **ODIN (`odin/`)**: parse ODIN embedded sections and standalone payloads,
  map parse-tree → ODIN AST.
- **ANTLR glue (`antlr/`)**: error listeners, source spans, generated parser
  README.
- **AOM (`aom/`)**: in-memory AOM2 domain types, occurrences/cardinality, terminology
  containers.
- **Validation (`validation/`)**: Issue model + registries; syntax/semantic/RM/OPT
  rule checks with stable codes.
- **BMM (`bmm/`)**: load RM schemas from ODIN/P_BMM, expose class/property lookup
  via ModelRepository.
- **OPT (`opt/`)**: archetype repository, flattening, slot filling, OPT dataclasses,
  deterministic JSON export.
- **Path (`path/`)**: openEHR path parsing and resolution against AOM trees.
- **CLI (`cli/`)**: Typer commands (`lint`, `validate`, `compile-opt`) with Rich
  rendering and JSON output.
- **AQL (`aql/`)**: ANTLR grammar presence; AST/API still to be completed.

## Hotspots for spec citations (top 10)

1. `openehr_am/adl/parser.py` — ADL2 sections, cADL subset.
2. `openehr_am/adl/cadl_ast.py` — cADL constraint nodes.
3. `openehr_am/odin/parser.py` — ODIN grammar + recovery.
4. `openehr_am/validation/semantic/*.py` — AOM2 validity rules (AOM200–AOM299).
5. `openehr_am/validation/rm/*.py` — BMM-driven RM conformance (BMM500+).
6. `openehr_am/validation/opt/*.py` — OPT integrity checks (OPT7xx).
7. `openehr_am/opt/flattening.py` and `opt/compiler.py` — OPT2 flatten/compile.
8. `openehr_am/bmm/loader.py` — BMM parsing and repository wiring.
9. `openehr_am/path/parser.py` — path grammar semantics.
10. `openehr_am/cli/commands.py` (and submodules) — CLI output/exit codes.

## Gaps / TODO hotspots

- AQL AST + parser implementation (`openehr_am/aql/`).
- Broader cADL coverage and specialization flattening in ADL/OPT pipeline.
- RM-aware OPT compilation steps.
- Corpus/regression fixtures comparing generated OPT vs ADL Workbench.

If a source reference is missing for a hotspot, add a `Sources:` block using
`docs/SOURCE_CITATION_STYLE.md` and resource identifiers from
`openehr_am_resources.md`.
