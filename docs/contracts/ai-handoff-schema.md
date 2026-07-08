# AI_HANDOFF.md Schema

`AI_HANDOFF.md` is the entry document for AI agents.

It answers: "What should an AI agent know before making changes?"

## Ownership

`AI_HANDOFF.md` is owned by the project maintainers and should be updated whenever the workflow, active restrictions, immediate next step, or implementation permissions change.

## Required Sections

### Role Context

Brief explanation of what the project is and how an AI agent should frame its role.

### Current Repository State

Current high-level repo status, including whether production code exists.

### Current Architectural Intent

Ordered list or concise explanation of how the project should evolve.

### Instructions For Future AI Agents

Actionable rules for AI contributors.

These instructions should include update responsibilities for project memory files and ADRs.

### Immediate Next Step

The next recommended action.

This should be concrete enough that a new agent can continue without chat history.

## Optional Sections

### Forbidden Actions

Actions the agent must not take without explicit approval.

### Required Reading

Documents an agent should read before touching specific areas.

### Handoff Notes

Short notes from the previous work session.

## Update Triggers

Update this file when:

- implementation permissions change
- the immediate next step changes
- a milestone is accepted
- a workflow rule changes
- a new document becomes required reading
- a previously forbidden action becomes allowed

## Stability Rule

`AI_HANDOFF.md` should be operational and concise. Deep rationale belongs in architecture docs and ADRs.
