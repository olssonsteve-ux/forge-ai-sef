# ADR 0015 - AI Implementation Protocol

Status: Accepted

Date: 2026-07-09

## Context

Forge implementation work has matured into a repeatable pattern.

Engineering Brief implementation sessions consistently require agents to read governing documents, understand the parent capability and slice, implement only approved scope, avoid unrelated refactors, run tests and quality checks, update documentation, and hand work off for review.

Leaving this process as chat convention creates drift risk as Forge gains more capabilities, more Engineering Briefs, more AI agents, and more implementation teams.

## Decision

Forge will adopt `docs/standards/ai-implementation-protocol.md` as the mandatory implementation protocol for AI agents implementing Engineering Briefs.

The protocol becomes the default implementation process for every future Engineering Brief unless an Engineering Brief defines stricter requirements.

## Rationale

The protocol improves:

- implementation consistency
- scope control
- traceability from capability to code
- AI usability
- human review quality
- project memory discipline
- release readiness

It also reinforces Forge's constitutional principles:

- Architecture before implementation.
- Specifications before code.
- Review before release.
- Continuous engineering improvement.

## Consequences

- Future Engineering Brief implementations must follow the AI Implementation Protocol.
- Implementation reports should use the protocol reporting format.
- Engineering Briefs may reference the protocol instead of repeating generic implementation process requirements.
- Project memory and AI handoff guidance should point implementation agents to the protocol.
- Deviations from the protocol should be explicit and justified.

## Non-Goals

This ADR does not:

- change Python code
- change CLI behavior
- implement a protocol checker
- replace Engineering Briefs
- replace Design Authority Reviews
- approve releases automatically
- define product strategy or architecture

## Related Documents

- `CONSTITUTION.md`
- `AI_ENGINEERING_CONDUCT.md`
- `docs/standards/ai-implementation-protocol.md`
- `docs/standards/capability-slice-standard.md`
- `docs/decisions/0012-ai-engineering-conduct.md`
- `docs/decisions/0014-introduce-capability-slices.md`
