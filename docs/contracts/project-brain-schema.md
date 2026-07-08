# PROJECT_BRAIN.md Schema

`PROJECT_BRAIN.md` is durable project memory.

It answers: "What must future contributors remember?"

## Ownership

`PROJECT_BRAIN.md` is owned by the project maintainers. AI agents may update it when durable beliefs, boundaries, or decisions change.

It should not be used as a work log.

## Required Sections

### Core Identity

Defines what the project is and what it is not.

### Guiding Beliefs

Durable principles that should influence future decisions.

Beliefs should be stable enough to survive multiple milestones.

### Product Shape

High-level description of what Forge may eventually include.

This section should remain capability-oriented, not implementation-oriented.

### Important Boundaries

Rules that prevent the project from drifting into adjacent but unwanted shapes.

### Current Decisions

Accepted decisions that future contributors should know before acting.

Each item should either be backed by an ADR or be small enough not to require one.

### Open Questions

Important unresolved questions.

Open questions should be pruned when answered or moved into ADRs when resolved.

## Optional Sections

### Vocabulary

Canonical terms and definitions.

### Rejected Ideas

Ideas that were considered and intentionally not pursued.

### Operating Principles

Reusable collaboration or governance rules that are broader than one decision.

## Update Triggers

Update this file when:

- a durable project belief changes
- a boundary is added or removed
- an ADR changes the direction contributors need to remember
- an open question is resolved
- a new open question materially affects architecture

## Stability Rule

`PROJECT_BRAIN.md` should change less often than `PROJECT_STATE.md`.

If a detail is temporary, tactical, or milestone-specific, keep it in `PROJECT_STATE.md` instead.
