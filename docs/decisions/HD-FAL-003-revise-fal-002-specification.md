# HD-FAL-003 — Revise FAL-002 specification

Status: `ACCEPTED`

Decision date: 2026-08-01

Decision owner: Human Product Owner / Forge Design Authority

Provenance: Explicit user authorization in the Codex task titled
`HUMAN REVIEW DECISION — REVISE FAL-002 SPECIFICATION`.

Addresses: `FAL2-HR-001`, `FAL2-HR-002`, `FAL2-HR-003`, `FAL2-HR-004`

## Decision

Authorize exactly one documentation-bounded revision of the FAL-002 specification and first-trial
measurement plan to address the four named human-review findings. The revision may also update the
direct documentation index required to expose the decision.

After revision, FAL-002 remains specification-only, implementation remains unauthorized, and its
status becomes `AWAITING TARGETED HUMAN REVIEW`.

## Constraints

This decision does not authorize FAL-002 implementation, an Engineering Brief, an album capability
specification or gate, Forge runtime/schema/fixture/test changes, Audio Recorder changes, reopening
or reclassifying FAL-001, or push, tag, merge, release, packaging, distribution or version changes.

FAL-001 remains permanently `TERMINATED BLOCKED`, with correction count 2/2 and its complete history
unchanged. This decision is not residual-risk acceptance, implementation approval, closure or
release authorization.

## Review-finding traceability

| Finding | Required normative revision |
| --- | --- |
| `FAL2-HR-001` | Measurement plan: baseline/comparison freeze, operational definitions, measure register and PASS/FAIL/INCONCLUSIVE outcome rule |
| `FAL2-HR-002` | FAL-002 specification section 13: transitive attribution, module/line/generated/schema counting and reproducible inventory |
| `FAL2-HR-003` | FAL-002 specification section 6.1: normative authority map and fail-closed conflict rules |
| `FAL2-HR-004` | FAL-002 specification sections 1, 5 and criterion 8: Standard-Assurance review terminology |
