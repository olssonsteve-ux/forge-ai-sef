# PROJECT_STATE.md Schema

`PROJECT_STATE.md` is the current operational snapshot of a Forge-governed repository.

It answers: "Where is this project right now?"

## Ownership

`PROJECT_STATE.md` is owned by the current project maintainer or acting AI engineering agent.

It should be updated whenever project status, version, active objective, completed foundation work, missing capabilities, or next recommended work changes.

## Required Sections

### Status

Short lifecycle label.

Examples:

- `Foundation stage`
- `Milestone 0 architecture review stage`
- `Forge 0.1 RC1 pre-implementation hardening`
- `0.2 project memory design`

### Current Version

The current Forge version or candidate version.

Examples:

- `0.1.0`
- `0.1 RC1`
- `0.2.0-draft`

### Current Objective

One concise sentence describing the active work.

### What Exists

Bulleted list of accepted project assets, documents, contracts, or implemented capabilities.

This section should describe stable facts, not aspirations.

### What Does Not Exist

Bulleted list of important missing capabilities or intentionally deferred work.

This section is a guardrail against accidental assumptions.

### Architectural Posture

Short statement describing how the project should be approached architecturally.

### Next Recommended Work

Ordered list of the next practical work items.

The first item should be the highest-leverage next step.

## Optional Sections

### Active Risks

Known risks that should influence near-term work.

### Blockers

Anything preventing meaningful progress.

### Recently Completed

Useful when a milestone or release candidate has just been accepted.

## Update Triggers

Update this file when:

- a milestone is accepted
- an RC is declared
- a major document contract is accepted
- implementation begins or is explicitly deferred
- a major capability moves from missing to existing
- next work changes materially

## Stability Rule

`PROJECT_STATE.md` should be brief, current, and practical. Long-term beliefs belong in `PROJECT_BRAIN.md`.
