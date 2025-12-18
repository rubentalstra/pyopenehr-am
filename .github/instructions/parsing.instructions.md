---
name: Parsing standards (ADL2/ODIN/ANTLR)
description: How to implement parsers, source spans, and error recovery
applyTo: "openehr_am/adl/**/*.py,openehr_am/odin/**/*.py,openehr_am/antlr/**/*.py"
---
# Parsing standards

## Goals
- Deterministic parsing
- Best-effort error recovery
- Accurate source locations

## Error capture
- Convert lexer/parser errors into `Issue` with stable codes (ADL*/ODN*).
- Include `file`, `line`, `col` whenever possible.

## AST building
- Parsing produces *syntax-layer* AST only.
- No semantic checks here (those belong in `validation/`).

## Spans
- Use a shared `SourceSpan` dataclass:
  - file, start_line, start_col, end_line, end_col
- Every AST node should carry a span when feasible.

## Security
- Treat all parsed input as untrusted.
- Never execute, import, or evaluate parsed content.
