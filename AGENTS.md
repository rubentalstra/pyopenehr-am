# AGENTS — openEHR AM Toolkit

This workspace builds a **pure-Python** openEHR AM toolkit.

## Scope

- ADL2 + ODIN parsing
- AOM2 model building
- Validation (syntax + semantic + RM via BMM)
- OPT2 compilation
- Optional instance validation (later)

## Guardrails

- No runtime bridges to Java/.NET reference implementations.
- Prefer incremental changes with tests.
- Keep public API stable; mark experimental modules clearly.

## Internal pipeline

Parse → Build AOM → Validate → Compile OPT → (Optional) Validate Instances
