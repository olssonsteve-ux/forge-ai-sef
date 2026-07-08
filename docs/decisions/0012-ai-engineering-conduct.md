# ADR 0012 - AI Engineering Conduct

Status: Accepted

Date: 2026-07-08

## Context

Forge is constitutionally governed as of `v0.3.1`.

The Constitution defines Forge's identity, principles, governance hierarchy, and decision framework. The next layer needed before Governance Runtime is a clear conduct model for AI agents working inside Forge-governed projects.

Without an AI conduct layer, AI agents may follow local instructions inconsistently, over-implement, skip project memory, claim unverified work, or treat uncertainty as fact.

## Decision

Forge will create `AI_ENGINEERING_CONDUCT.md` at the repository root.

This document defines required AI engineering behavior for Forge and Forge-governed projects.

It is subordinate to `CONSTITUTION.md`, accepted ADRs, project standards, and explicit human direction that remains within constitutional bounds. It is above ordinary session habits.

## Rationale

The Constitution defines what Forge is and how it is governed. AI Engineering Conduct defines how AI agents must behave while applying that governance.

Root placement is intentional because AI conduct is not merely a documentation topic. It is a project-wide behavioral contract that should be visible before implementation or automation work begins.

## Required Conduct Themes

AI agents must:

- read before changing
- understand before implementing
- motivate before deciding
- specify before coding
- test before claiming completion
- review before release
- document before moving on
- preserve architecture unless a justified ADR supports change
- follow the Constitution
- escalate uncertainty instead of inventing certainty

## Consequences

- Future AI sessions have an explicit conduct contract.
- `AI_HANDOFF.md` can reference conduct instead of restating all behavioral rules.
- Future Governance Runtime work can treat AI conduct as an accepted governance input.
- AI automation must remain explainable, scoped, and reviewable.
- Human direction remains authoritative for task scope, but cannot be used to bypass the Constitution or accepted governance.

## Rejected Alternatives

Embedding AI conduct only in `AI_HANDOFF.md` was rejected because handoff guidance is operational and current-state oriented, while conduct is permanent governance.

Embedding AI conduct only in `CONSTITUTION.md` was rejected because the Constitution should remain timeless and concise. Conduct requires more practical workflow detail.

Deferring AI conduct until implementation was rejected because Governance Runtime should not begin before AI behavior expectations are explicit.
