# AGENTS — openehr_am package

Folder-specific guidance for the core library.

## Generated code

- `openehr_am/_generated/` is generated from ANTLR grammars — do not edit
  manually.

## Layering

- Keep parsing, semantic model, validation, and OPT compilation separate.
- Avoid circular imports between `adl/`, `aom/`, `validation/`, and `opt/`.

## Diagnostics

- Prefer returning `Issue` lists.
- Ensure Issue codes are stable and documented (see `docs/issue-codes.md`).
