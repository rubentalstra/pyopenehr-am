# Security

All ADL/ODIN/BMM inputs are treated as untrusted.

- Never execute parsed content.
- Avoid catastrophic regex patterns.
- Prefer deterministic algorithms for tree walking.
- Limit recursion depth or use iterative traversals for deeply nested artefacts.
