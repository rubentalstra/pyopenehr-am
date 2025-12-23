# openEHR Resources

This directory is reserved for openEHR specification-related resources.

## Current Status

**No resources are currently vendored.** All openEHR specifications and
reference materials are accessed via external links documented in:

- `openehr_am_resources.md` (root) - Curated link collection
- `SPEC_BASELINE.md` (root) - Pinned specification versions

## Rationale

The openEHR specifications are:
1. Large HTML documents that change between releases
2. Best accessed via canonical URLs for up-to-date content
3. Subject to openEHR Foundation licensing

Instead of vendoring, we:
- Pin specific release versions in `SPEC_BASELINE.md`
- Document canonical URLs in `openehr_am_resources.md`
- Use minimal hand-crafted test fixtures in `tests/fixtures/`

## Future Considerations

If offline access becomes important, consider:
1. Downloading PDF versions of key specs
2. Creating a Git submodule for BMM schema files
3. Documenting exact commit SHAs for grammar repositories

## Provenance Record

| Resource | Source | Retrieved | Version |
|----------|--------|-----------|---------|
| *None currently vendored* | - | - | - |
