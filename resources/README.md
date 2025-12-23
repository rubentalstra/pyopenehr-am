# Resources

This directory contains reference materials for the pyopenehr-am project.

## Provenance Policy

For each resource:
- Record the source URL
- Record the retrieval date
- Record the version/tag/commit if available
- Note licensing considerations

## Directory Structure

```
resources/
├── README.md          # This file
└── openehr/           # openEHR specification resources
    └── README.md      # Provenance for openEHR resources
```

## External Resources (Not Vendored)

The following resources are **not** vendored due to size or licensing
considerations. Use the canonical links in `openehr_am_resources.md`.

### Specifications (External Links Only)

| Resource | Canonical URL | Notes |
|----------|---------------|-------|
| ADL2 Spec | https://specifications.openehr.org/releases/AM/Release-2.3.0/ADL2.html | Pinned release (see `SPEC_BASELINE.md`) |
| AOM2 Spec | https://specifications.openehr.org/releases/AM/Release-2.3.0/AOM2.html | Pinned release |
| OPT2 Spec | https://specifications.openehr.org/releases/AM/Release-2.3.0/OPT2.html | Pinned release |
| ODIN Spec | https://specifications.openehr.org/releases/LANG/Release-1.0.0/odin.html | Pinned release |
| BMM Spec | https://specifications.openehr.org/releases/LANG/Release-1.0.0/bmm.html | Pinned release |

### Git Repositories (External Links Only)

| Resource | Repository | Notes |
|----------|------------|-------|
| ANTLR Grammars | https://github.com/openEHR/adl-antlr | Reference grammars |
| BMM Schemas | https://github.com/openEHR/specifications-ITS-BMM | RM schema files |
| ADL Tools | https://github.com/openEHR/adl-tools | Reference implementation |

## Usage in Tests

Test fixtures that require specific archetype or BMM files should:
1. Use minimal, hand-crafted fixtures in `tests/fixtures/`
2. Reference this document for provenance of any external materials

## Updating Resources

When updating pinned versions:
1. Update `SPEC_BASELINE.md` with new release versions
2. Update `openehr_am_resources.md` with new URLs
3. Update this README if any resources are added or removed
