---
name: CLI behavior (Typer + Rich)
description: Standards for CLI commands, output, and exit codes
applyTo: "openehr_am/cli/**/*.py"
---
# CLI behavior (Typer + Rich)

## Must-haves
- Framework: **Typer**
- Human output: **Rich** tables for Issues
- `--json` / `--format json`: strict JSON only (no Rich markup)

## Commands
- `lint` — parse only (syntax)
- `validate` — semantic + optional RM (BMM)
- `compile-opt` — compile template to OPT JSON

## Flags
- `--rm <dir>`: RM schema directory (BMM)
- `--repo <dir>`: archetype repository dir (templates)
- `--strict`: treat warnings as errors
- `--no-color`: disable colors (CI)

## Exit codes
- 0: no errors
- 1: validation errors (or warnings in strict mode)
- 2: IO/usage errors
