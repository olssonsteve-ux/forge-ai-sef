# 0010 - Forge Capability Specifications

Date: 2026-07-08

## Status

Accepted

## Context

Forge is evolving beyond foundation documents and bootstrap behavior. Some parts of Forge are permanent capabilities that need durable specification before implementation.

Engineering briefs are not the right artifact for these capabilities because they are task-specific and implementation-oriented. Forge needs a stable specification type for capability behavior, inputs, workflows, outputs, scoring, acceptance criteria, risks, and future extensions.

## Decision

Forge will use Forge Capability Specifications under `docs/capabilities/`.

Capability files use this naming format:

```text
FCS-NNN-Capability-Name.md
```

The first capability is `FCS-001 - Review Capability`.

## Consequences

- Permanent Forge capabilities are specified before implementation.
- Capability design remains separate from engineering briefs.
- Future CLI commands can be traced back to accepted capability specifications.
- Material changes to accepted capability behavior may require ADRs.
