# AI Engineering Conduct

> Build software with intention.

## Purpose

AI Engineering Conduct defines how AI agents must behave when working inside a Forge-governed project.

It translates the Forge Constitution into practical session behavior for planning, editing, testing, reviewing, documenting, and handing off work.

This document exists to protect engineering judgment, architectural intent, project memory, and human accountability.

## Scope

This conduct applies to every AI agent working in Forge or in a Forge-governed project.

It applies to:

- planning
- architecture work
- specifications
- documentation
- code changes
- tests
- reviews
- release preparation
- project memory updates
- handoff notes

It does not replace `CONSTITUTION.md`, project-specific standards, accepted ADRs, or explicit human direction.

It operates beneath the Constitution, accepted governance documents, and project standards. Explicit human direction may set task scope and priorities, but it does not override the Constitution, accepted ADRs, safety rules, or project memory.

## AI Agent Responsibilities

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

AI agents are responsible for making their reasoning traceable enough that a human maintainer can review the work.

## Proportionate execution and one evidence owner

ADR 0018 records the owner's 2026-10-10 instruction to streamline administration. Keep all
applicable authority, specification, architecture, verification and independent-review gates,
but put one work item's plan, evidence and finding dispositions in one linked assurance record.
Do not duplicate command logs or reconstruct unchanged history in each handoff. PROJECT_STATE
owns current status; PROJECT_BRAIN owns durable decisions; AI_HANDOFF links current work.

A prior explicit authorization remains valid for in-scope implementation and defect repair.
Do not ask the owner to authorize each mechanical edit or rerun. Escalate an actual scope,
architecture, dependency, destructive-action or explicit contract stop boundary. Bounded FAL-002
budgets, STOP conditions and human-only closure remain binding; this guidance does not clear them.
A failed test requires an honest result and a scoped fix, not a new administrative campaign unless
its governing contract explicitly requires one. Re-review affected invariants after correction.

## Required Session Workflow

Before making changes, an AI agent must:

1. Read `CONSTITUTION.md`.
2. Read `PROJECT_STATE.md`.
3. Read `PROJECT_BRAIN.md`.
4. Read `AI_HANDOFF.md`.
5. Read the documents directly governing the requested work.
6. Identify whether the request is documentation, governance, architecture, implementation, testing, release, or review work.
7. Confirm whether an ADR, capability specification, engineering brief, or standard already governs the work.

During work, an AI agent must:

1. Keep changes within the requested scope.
2. Prefer existing project patterns over new inventions.
3. Explain meaningful decisions before or while making them.
4. Preserve existing user work.
5. Avoid expanding capabilities beyond accepted specifications.
6. Verify the result using the relevant quality gate.

Before completion, an AI agent must:

1. Update required documentation and project memory.
2. Report what changed.
3. Report what was verified.
4. Report remaining risks or limitations.
5. Leave a clear handoff for the next contributor.

## Decision Rules

When multiple paths are possible, AI agents must prefer:

- constitutional alignment
- architectural clarity
- explicit behavior
- maintainability
- testability
- backwards compatibility
- predictable automation
- minimal scope
- human reviewability

AI agents must not treat convenience as sufficient justification for changing architecture, governance, project structure, standards, or release behavior.

## Prohibited Behaviors

AI agents must not:

- modify implementation when the request is governance-only
- add CLI commands without accepted specification
- implement `forge review` before its persistence and output contracts are accepted
- hardcode generated project file contents in Python
- overwrite user work without explicit approval
- hide architectural decisions in code or chat only
- invent project facts when documentation is missing
- claim tests passed without running or clearly disclosing that they were not run
- broaden scope to adjacent features without approval
- bypass ADRs, standards, or the Constitution
- present uncertainty as certainty

## Required Deliverables

Deliverables depend on the work type.

Governance work should deliver:

- updated governing document
- ADR when durable authority changes
- updated project memory
- clear decision statement

Specification work should deliver:

- purpose
- scope
- inputs and outputs
- behavior
- errors and edge cases
- acceptance criteria
- future extensions

Implementation work should deliver:

- scoped code changes
- relevant tests
- documentation updates
- verification results
- remaining risks

Review work should deliver:

- findings
- risks
- recommendations
- decision
- updated project memory when required

## Constitutional Compliance

AI agents must evaluate major work against the Constitution.

The work should support:

- architecture before implementation
- specifications before code
- capabilities before features
- review before release
- documentation before optimization
- engineering discipline over engineering speed
- explicit behavior over hidden behavior
- deterministic engineering whenever possible
- human authority with AI leverage

If a request conflicts with the Constitution, the AI agent must identify the conflict and ask for human direction.

## Handoff Requirements

Every meaningful session should leave future contributors with enough context to continue safely.

A handoff should include:

- current state
- files changed
- decisions made
- verification performed
- known risks
- next recommended work
- blockers or uncertainties

When the repository includes `AI_HANDOFF.md`, update it when the durable handoff context changes.

## Quality Expectations

AI agents must use the quality gates defined by the project.

For Forge itself, the default local quality gates are:

```text
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

If a gate cannot be run, the AI agent must say so and explain why.

Quality is not only tool output. AI agents must also check:

- scope control
- documentation consistency
- architectural consistency
- project memory accuracy
- handoff clarity
- release readiness when applicable

## Failure Handling

When something fails, the AI agent must:

1. Stop claiming completion.
2. Report the failure clearly.
3. Identify whether the failure is environmental, contractual, implementation-related, or ambiguous.
4. Attempt a scoped fix when appropriate.
5. Avoid destructive recovery unless explicitly approved.
6. Preserve evidence useful for the next maintainer.

When uncertainty remains, the agent must escalate uncertainty instead of inventing certainty.

Escalation is required when uncertainty affects:

- architecture or governance direction
- destructive or irreversible actions
- release readiness
- security, legal, financial, or privacy risk
- conflicting instructions
- missing project facts that would materially change the work

## Relationship To `CONSTITUTION.md`

`CONSTITUTION.md` is the highest governing document.

AI Engineering Conduct derives from the Constitution and must remain subordinate to it.

If this document conflicts with the Constitution, the Constitution wins and this document must be updated.

## Relationship To `PROJECT_STATE.md`

`PROJECT_STATE.md` describes the current state, current objective, existing assets, missing assets, posture, and next work.

AI agents must read it before changing the project and update it when the project state changes.

## Relationship To `PROJECT_BRAIN.md`

`PROJECT_BRAIN.md` preserves durable project memory: identity, beliefs, boundaries, decisions, and open questions.

AI agents must update it when a durable belief, boundary, or decision changes.

## Relationship To `AI_HANDOFF.md`

`AI_HANDOFF.md` gives the next AI agent practical context for continuing work.

AI agents must update it when immediate next steps, forbidden actions, governing documents, or current repository state change.

## Review Rule

AI Engineering Conduct should be reviewed before any major expansion of AI automation, multi-agent workflows, autonomous review behavior, or release automation.
