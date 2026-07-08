# ADR 0013 - Governance Runtime Capability

Status: Accepted

Date: 2026-07-08

## Context

Forge has reached `v0.3.2` with a Constitution, AI Engineering Conduct, Developer Platform, Capability Specifications, Engineering Briefs, Design Authority Reviews, ADRs, standards, bootstrap behavior, and CI.

The next evolution is not another CLI feature. Forge needs an operational governance capability that can evaluate whether a project remains aligned with its engineering model.

## Decision

Forge will define Governance Runtime as a permanent capability in `docs/capabilities/FCS-002-Governance-Runtime.md`.

Governance Runtime is the operational layer that interprets the Constitution and evaluates engineering health, governance compliance, readiness, risk, project memory, capability health, and release posture.

The capability is specification-only at this milestone.

## Rationale

The Constitution establishes identity and authority. AI Engineering Conduct establishes agent behavior. Governance Runtime will operationalize those documents by evaluating whether project evidence aligns with them.

Defining the capability before implementation prevents Forge from prematurely adding commands or automation without a stable governance model.

## Consequences

- Governance Runtime becomes a durable Forge capability.
- Future status, planning, review, scoring, memory, risk, and release commands should derive from FCS-002.
- Governance Runtime must not modify code, approve releases, or override human judgment by default.
- Implementation cannot begin until the first runtime service, inputs, outputs, persistence, scoring policy, and failure behavior are specified.

## Rejected Alternatives

Implementing `forge status` immediately was rejected because the runtime model is not yet bounded.

Treating Governance Runtime as part of `forge review` was rejected because runtime governance is broader than review reports.

Deferring Governance Runtime until after more CLI commands was rejected because future commands need a shared governance model before they are added.
