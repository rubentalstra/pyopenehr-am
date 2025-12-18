# Validation levels

Validation can be run in layers:

- `syntax` — parsing/grammar-level issues (ADL/ODIN)
- `semantic` — AOM2 validity rules (terminology, node ids, occurrences, etc.)
- `rm` — RM conformance using BMM schemas
- `opt` — OPT compilation integrity checks
- `all` — run everything applicable

All results are returned as structured `Issue` objects.
