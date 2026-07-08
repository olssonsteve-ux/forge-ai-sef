# 0006 - ADR Lifecycle And Status Rules

Date: 2026-07-08

## Status

Accepted

## Context

Forge uses ADRs for durable architecture decisions. The initial ADRs were useful, but the repository did not yet define naming, lifecycle, or status rules.

## Decision

Forge will use the ADR lifecycle documented in `docs/contracts/adr-lifecycle.md`.

ADR files must use sequential zero-padded numbering and kebab-case titles.

Accepted status values are:

- Proposed
- Accepted
- Superseded
- Deprecated
- Rejected

## Consequences

- ADRs become easier to review and maintain.
- Decision history remains stable.
- Future changes can supersede decisions without rewriting accepted history.
