# Grammars

This directory holds grammar sources for parser generation (e.g. ANTLR `.g4`).

## Policy

- Grammar changes must be followed by regeneration of committed output under
  `openehr_am/_generated/`.
- Do not commit local, machine-specific artefacts here.

## Optional: pinned submodule strategy

If we later decide to vendor grammars from an upstream repository, we can pin
them as a Git submodule under `grammars/` (preferred: a fixed commit SHA). The
output under `openehr_am/_generated/` remains committed in this repository.
