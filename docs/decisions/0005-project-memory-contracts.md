# 0005 - Project Memory Contracts

Date: 2026-07-08

## Status

Accepted

## Context

Forge depends on durable project memory. The initial repository included `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, and `AI_HANDOFF.md`, but their structures and update triggers were informal.

Without explicit contracts, future AI agents and automation could update these files inconsistently.

## Decision

Forge will define document contracts for:

- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md`
- `AI_HANDOFF.md`

The contracts live under `docs/contracts/` and define ownership, required sections, optional sections, update triggers, and stability rules.

## Consequences

- Project memory becomes reviewable before automation exists.
- Future tooling can validate these files against documented expectations.
- AI agents have clearer update responsibilities.
- Contract changes should be treated as architecture changes.
