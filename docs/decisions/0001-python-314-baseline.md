# ADR 0001 — Python 3.14 baseline

## Status

Accepted

## Decision

This project targets **Python 3.14+ only**.

## Rationale

- Simplifies typing and annotation behavior (3.14 deferred annotations by
  default).
- Enables modern standard-library tooling (`annotationlib`) for introspection.
- Reduces maintenance cost of compatibility shims.

## Consequences

- Users on older Python versions must use older library versions (once releases
  exist).
