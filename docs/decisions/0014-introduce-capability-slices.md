# ADR 0014 - Introduce Capability Slices

Status: Accepted

Date: 2026-07-08

## Context

Forge's current hierarchy moves directly from Capability Specification to Engineering Brief.

That is sufficient for small capabilities, but Governance Runtime revealed a scaling concern. A single capability may contain many runtime services, review surfaces, scoring policies, memory checks, release checks, and implementation phases.

Forge is expected to grow toward:

- 50+ capabilities
- 100+ engineering briefs
- multiple AI agents
- plugin ecosystem
- enterprise governance
- runtime services
- multiple implementation teams

## Decision

Forge will introduce `Capability Slice` as the engineering layer between Capability Specification and Engineering Brief.

Updated hierarchy:

```text
Constitution
  |
  v
Product Strategy
  |
  v
Roadmap
  |
  v
Capability Specification
  |
  v
Capability Slice
  |
  v
Engineering Brief
  |
  v
Implementation
  |
  v
Testing
  |
  v
Design Authority Review
  |
  v
Release
```

## Rationale

Capability Slices preserve Forge's principle of capabilities before features while giving large capabilities a manageable decomposition layer.

They improve:

- maintainability
- scalability
- governance
- traceability
- AI usability
- enterprise readiness

## Consequences

- Future large capabilities should be decomposed into Capability Slices before Engineering Briefs.
- Engineering Briefs should implement accepted slices, not broad capabilities directly, when the capability is large or multi-service.
- Governance Runtime implementation planning should begin with Capability Slices.
- Existing FCS and EB documents remain valid.
- Future templates and standards should define Capability Slice format and lifecycle.

## Non-Goals

This ADR does not:

- create a new directory
- create a Capability Slice template
- implement Governance Runtime
- change Python code
- change CLI behavior
- require backfilling slices for all existing capabilities

## Related Documents

- `docs/architecture/AR-0001-Engineering-Hierarchy.md`
- `CONSTITUTION.md`
- `docs/capabilities/FCS-002-Governance-Runtime.md`
