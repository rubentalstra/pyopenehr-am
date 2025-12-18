# Spec baseline

This repository is **standards-driven**. The goal of this document is to pin the
_exact_ openEHR specification versions (URLs) that `pyopenehr-am` targets.

**Spec baseline changes require a minor version bump.**

## Pinned specifications

| Area | Spec                            | Chosen release                   | URL                                                                      |
| ---- | ------------------------------- | -------------------------------- | ------------------------------------------------------------------------ |
| ADL2 | Archetype Definition Language 2 | AM Release-2.3.0 (20-Mar-2024)   | https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL2.html   |
| AOM2 | Archetype Object Model 2        | AM Release-2.3.0 (20-Mar-2024)   | https://specifications.openehr.org/releases/AM/Release-2.3.0/AOM2.html   |
| OPT2 | Operational Template 2          | AM Release-2.3.0 (20-Mar-2024)   | https://specifications.openehr.org/releases/AM/Release-2.3.0/OPT2.html   |
| ODIN | Object Data Instance Notation   | LANG Release-1.0.0 (11-May-2020) | https://specifications.openehr.org/releases/LANG/Release-1.0.0/odin.html |
| BMM  | Basic Meta-Model                | LANG Release-1.0.0 (11-May-2020) | https://specifications.openehr.org/releases/LANG/Release-1.0.0/bmm.html  |

## Notes

- Use the release-specific URLs above (not `/latest/`) in docs, code comments,
  and validation-rule `# Spec:` links.
- OPT2 is marked as **DEVELOPMENT** within AM Release-2.3.0; this project still
  targets that pinned document URL so that behavior is deterministic.
