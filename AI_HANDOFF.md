# AI Handoff

## Role Context

You are working in Forge, an AI Software Engineering Framework.

Forge is not an application. Do not assume product UI, API routes, database models, or runtime services exist.

## Current Repository State

The repository is at foundation stage and contains documentation only.

There is no production code and no CLI implementation.

## Current Architectural Intent

Forge should be built in this order:

1. architecture and vision
2. project memory contracts
3. standards and templates
4. bootstrap specification
5. minimal CLI
6. automation and governance

## Instructions For Future AI Agents

- Do not write production code unless the user explicitly asks to begin implementation.
- Preserve project memory files when making changes.
- Update `PROJECT_STATE.md` when the project status changes.
- Update `PROJECT_BRAIN.md` when durable decisions or project beliefs change.
- Add architectural decisions under `docs/decisions/` for meaningful direction changes.
- Keep documentation clear enough for a new contributor to understand without chat history.
- Prefer small, reviewable changes over broad framework expansion.

## Immediate Next Step

The next logical work is to define the `0.2` project memory model and the file contracts that future Forge commands will read and write.
