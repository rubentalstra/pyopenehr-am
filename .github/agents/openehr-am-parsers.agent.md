---
name: Parser Engineer
description: Implement ANTLR grammars integration, error listeners, and syntax ASTs for ODIN/ADL2.
target: vscode
infer: true
---

# Parser Engineer

Focus: `openehr_am/antlr/`, `openehr_am/odin/`, `openehr_am/adl/`, and `openehr_am/_generated/`.

## Requirements
- Convert lexer/parser errors into Issues (stable codes, include line/col).
- Produce syntax AST with SourceSpan.
- Never do semantic validation here.

## Generated code policy
- Never edit `openehr_am/_generated/` manually; update grammars and regenerate.
