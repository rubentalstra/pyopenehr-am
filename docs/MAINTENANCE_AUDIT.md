# Maintenance Audit (December 2025)

This document summarizes findings from a repository-wide audit and identifies
obsolete, duplicated, or missing documentation and configuration.

## Summary of Changes

### Files Archived

The following files have been moved to `docs/archive/` as they represent
historical planning artifacts that are now superseded by `CHECKLIST.md`:

| File | Reason |
|------|--------|
| `openehr_am_toolkit_todo_checklist.md` | Replaced by `CHECKLIST.md`; generic template-style checklist |
| `openehr_am_prompt_list_expanded.md` | Agent prompt sequences for AI; replaced by consolidated agent configs |
| `PACK_INDEX.md` | Pack manifest for initial setup; no longer needed |

### Files Updated

| File | Changes |
|------|---------|
| `README.md` | Removed reference to archived files; updated doc links |
| `openehr_am_resources.md` | Added version pins and provenance; clarified vendored vs external |

### Files Created

| File | Purpose |
|------|---------|
| `CHECKLIST.md` | Fresh continuation plan with concrete deliverables |
| `resources/README.md` | Provenance and usage notes for fetched resources |
| `docs/MAINTENANCE_AUDIT.md` | This audit report |

---

## Markdown Files Inventory

### Top-Level Documentation

| File | Purpose | Status | Notes |
|------|---------|--------|-------|
| `README.md` | Project overview, install, quickstart | **Keep** | Central entry point |
| `CONTRIBUTING.md` | Contribution guidelines | **Keep** | Aligned with project policies |
| `CODE_OF_CONDUCT.md` | Community standards | **Keep** | Standard CoC |
| `SECURITY.md` | Security reporting policy | **Keep** | Important for untrusted input handling |
| `LICENSE` | MIT license | **Keep** | Required |
| `SPEC_BASELINE.md` | Pinned spec versions | **Keep** | Critical for standards compliance |
| `AGENTS.md` | Top-level agent instructions | **Keep** | Useful for AI-assisted development |
| `CHECKLIST.md` | **NEW** Continuation plan | **Created** | Replaces older planning docs |

### Archived (Historical Planning)

| File | Original Purpose | Status |
|------|------------------|--------|
| `openehr_am_toolkit_todo_checklist.md` | Generic todo template | **Archived** |
| `openehr_am_prompt_list_expanded.md` | Agent prompt sequences | **Archived** |
| `PACK_INDEX.md` | Pack manifest for setup | **Archived** |

### Documentation (`docs/`)

| File | Purpose | Status |
|------|---------|--------|
| `docs/architecture.md` | Pipeline architecture | **Keep** |
| `docs/quickstart.md` | Usage examples | **Keep** |
| `docs/compatibility.md` | Stability guarantees | **Keep** |
| `docs/glossary.md` | Term definitions | **Keep** |
| `docs/issue-codes.md` | Issue code registry | **Keep** |
| `docs/validation-rule-template.md` | Rule template | **Keep** |
| `docs/validation_levels.md` | Validation layer docs | **Keep** |
| `docs/opt_compilation.md` | OPT compiler docs | **Keep** |
| `docs/security.md` | Security engineering notes | **Keep** |
| `docs/roadmap.md` | Version roadmap | **Keep** |
| `docs/releasing.md` | Release checklist | **Keep** |
| `docs/dev/README.md` | Dev setup | **Keep** |
| `docs/dev/parsers.md` | Parser generation docs | **Keep** |
| `docs/dev/ci.md` | CI documentation | **Keep** |
| `docs/decisions/0001-python-314-baseline.md` | ADR | **Keep** |
| `docs/MAINTENANCE_AUDIT.md` | This audit | **Created** |

### Package Documentation

| File | Purpose | Status |
|------|---------|--------|
| `openehr_am/AGENTS.md` | Package-level agent hints | **Keep** |
| `openehr_am/_generated/README.md` | Generated code policy | **Keep** |
| `grammars/README.md` | Grammar policy | **Keep** |

---

## Agent Configuration Inventory

### GitHub Copilot Configuration

| File | Purpose | Status |
|------|---------|--------|
| `.github/copilot-instructions.md` | Main Copilot instructions | **Keep** |
| `.github/instructions/*.instructions.md` | Module-scoped rules (10 files) | **Keep** |
| `.github/agents/*.agent.md` | Specialized agent definitions (7 agents) | **Keep** |
| `AGENTS.md` | Top-level agent summary | **Keep** |
| `openehr_am/AGENTS.md` | Package-level boundaries | **Keep** |

### Other AI Agent Files

No other AI agent configuration files were found (no `.cursorrules`,
`.windsurfrules`, `.aider*`, or `.cline*` files).

---

## CI/Workflow Configuration

| File | Purpose | Status |
|------|---------|--------|
| `.github/workflows/ci.yml` | Main CI (lint, test, type-check) | **Keep** |
| `.github/workflows/release-package-check.yml` | Release build + publish | **Keep** |
| `.github/python-publish.yml` | Legacy PyPI publish | **Review** - possibly redundant |
| `.github/dependabot.yml` | Dependency updates | **Keep** |
| `.github/FUNDING.yml` | GitHub Sponsors | **Keep** |

**Note:** `.github/python-publish.yml` appears to be a template file that
duplicates functionality in `release-package-check.yml`. Consider removing.

---

## Resource Files

### `openehr_am_resources.md`

Contains curated links to openEHR specifications. Updated to:
- Pin specific release versions where available
- Distinguish between external links and potentially vendored resources
- Add retrieval dates for provenance

### `resources/` Directory

Created to house fetched reference materials with clear provenance.

---

## Identified Gaps

### Missing Documentation

1. **CHANGELOG.md** - No changelog file exists; releases tracked via GitHub releases
2. **API Reference** - No generated API docs; quickstart serves as primary guide

### Missing Test Infrastructure

1. **Corpus tests** - `tests/corpus/` exists but may need more test files
2. **Fuzz tests** - `tests/fuzz/` exists but coverage unclear

---

## Recommendations

1. **Remove** `.github/python-publish.yml` if `release-package-check.yml` is the canonical release workflow
2. **Add** `CHANGELOG.md` when preparing for v1.0
3. **Consider** generating API reference docs for stable public API
4. **Expand** corpus test coverage as more archetypes become available
