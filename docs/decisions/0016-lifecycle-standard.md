# ADR 0016 - Forge Lifecycle Standard

Status: Accepted

Date: 2026-07-09

## Context

Forge now uses lifecycle status across many artifact types, including Capability Specifications, Capability Slices, Engineering Briefs, ADRs, reviews, standards, templates, and releases.

CS-002.2 closure revealed that lifecycle states were being used without a single governing standard. That creates ambiguity about the difference between `Implemented`, `Implementation Reviewed`, `Closed`, `Released`, `Deprecated`, and related states.

## Decision

Forge will adopt `docs/standards/lifecycle-standard.md` as the common lifecycle standard for Forge artifacts.

The standard defines common, artifact-specific, and release lifecycle states; governs withdrawal, archival, and reopening; and defines status ownership, transition evidence, anti-patterns, and documentation requirements.

## Rationale

The lifecycle standard improves:

- governance consistency
- artifact traceability
- AI agent usability
- review discipline
- release clarity
- project memory quality

It also prevents review status, implementation status, closure status, and release status from being conflated.

## Consequences

- Future Forge artifacts should use lifecycle language from the lifecycle standard.
- Capability Slices should follow the explicit slice lifecycle through `Closed`.
- Releases should use release-specific lifecycle states.
- `Withdrawn` records intentionally stopped incomplete work; `Archived` records non-active retention while preserving the prior substantive disposition.
- Closed or completed work must not be silently reopened or rewritten; governed resumption requires explicit authorization, preserved history, and downstream revalidation.
- Project memory should be updated when lifecycle changes alter current state or durable direction.
- Existing artifacts may be aligned opportunistically when they are touched for relevant work.

## Non-Goals

This ADR does not:

- modify Python code
- change CLI behavior
- add lifecycle automation
- require immediate migration of every historical artifact
- replace ADR lifecycle rules
- replace release readiness standards

## Related Documents

- `CONSTITUTION.md`
- `AI_ENGINEERING_CONDUCT.md`
- `docs/standards/lifecycle-standard.md`
- `docs/standards/capability-slice-standard.md`
- `docs/standards/ai-implementation-protocol.md`
- `docs/release/release-standard.md`
