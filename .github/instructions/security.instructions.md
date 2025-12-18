---
name: Security and robustness
description: Safety rules for parsing untrusted artefacts
applyTo: "openehr_am/**/*.py"
---
# Security and robustness

- Treat ADL/ODIN/BMM input as untrusted.
- Never `eval`, `exec`, or dynamically import based on parsed content.
- Avoid regexes that can cause catastrophic backtracking on untrusted input.
- Prefer iterative algorithms for deep trees to avoid recursion limits where possible.
