# OPT compilation

## Goal

Compile an ADL template + referenced archetypes into an Operational Template
(OPT2) that can be used for runtime validation.

# Spec: https://specifications.openehr.org/releases/AM/latest/OPT2.html

# Spec: https://specifications.openehr.org/releases/AM/latest/AOM2.html

## What’s supported (current MVP)

The current compiler is intentionally small and deterministic. It aims to be a
useful base for downstream tooling without claiming full OPT2 conformance.

### Inputs

- Template: parsed into an AOM `Template` (`parse_template(...)`).
- Archetype repository: a directory of `.adl` archetype files.

### Dependency handling

- Loads all archetypes from the repository directory.
- Resolves specialisation-parent dependencies.
- Emits `OPT700` when a referenced parent archetype is missing.
- Uses a deterministic dependency order for the component archetype list.

### Template slot filling (subset)

The compiler performs basic archetype slot selection when the template
definition contains `CArchetypeSlot` nodes.

- Matches repository archetype IDs against slot `include` / `exclude` patterns.
- Pattern kinds supported:
  - exact match
  - regex (full match)
- On multiple matches, the selected archetype is the deterministically first one
  (sorted by archetype id).
- Emits `OPT720` when a slot has no matching archetype.

Compilation scope behavior:

- If slots are present and successfully resolved, compilation is restricted to
  the selected archetypes plus their specialisation dependencies.
- Otherwise, compilation falls back to compiling all archetypes found in the
  repository directory.

### Specialisation flattening (subset)

The compiler flattens an archetype’s definition across its specialisation chain
by merging the child definition over the parent definition.

- Output is deterministic (sorted attribute/child ordering).
- Emits `OPT730` for detected structural conflicts.

### OPT definition export (subset)

- Converts flattened AOM constraint nodes into OPT constraint nodes.
- Supported constraint kinds include:
  - complex objects (with attributes + children)
  - primitive constraints (string/integer/real/boolean)
  - occurrences, existence, and cardinality

Slots that remain unresolved are not expected in the exported OPT definition.

### Deterministic JSON export

- OPT objects can be exported via deterministic JSON helpers.
- The CLI writes an OPT JSON file in a deterministic way.

## What is explicitly not supported yet

- Full AOM2/OPT2 flattening rules (beyond the minimal specialisation merge).
- Full template overlay rules.
- RM-aware compilation and RM-path resolution during compilation.
- Instance validation against OPT (data validation).

## Planned next (direction)

These are intended future capabilities as the compiler grows:

- More complete template slot resolution behavior.
- More complete specialisation flattening (beyond structural merge).
- Template overlay support aligned with OPT2 expectations.
- RM-aware compilation using BMM repositories.
- Instance validation against compiled OPT.

## CLI and Python entry points

- CLI: `openehr-am compile-opt <template> --repo <dir> --out <file>`
- Python: `compile_opt(template, archetype_dir=..., rm=...)`

Note: `rm=...` is reserved for future RM-aware compilation.
