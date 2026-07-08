# AI Handoff

## Role Context

You are working in Forge, an AI Software Engineering Framework.

Forge is not an application. Do not assume product UI, API routes, database models, or runtime services exist.

## Current Repository State

The repository is at Forge 0.1 RC1 pre-implementation hardening stage and contains documentation only.

There is no production code and no CLI implementation.

Milestone 0 architecture review has been recorded in `docs/architecture/review-000.md`.

Project memory schemas, ADR lifecycle rules, standard categories, template governance, and the `forge init <project-name>` pre-implementation specification are documented under `docs/contracts/`, `standards/`, and `templates/`.

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
- Check `docs/README.md` before changing documentation authority or duplicating concepts.
- Follow `docs/contracts/` before changing project memory or CLI behavior.
- Keep documentation clear enough for a new contributor to understand without chat history.
- Prefer small, reviewable changes over broad framework expansion.

## Forbidden Actions

- Do not implement `forge init` until the user explicitly approves CLI implementation.
- Do not add production code during architecture or hardening work.
- Do not add destructive overwrite behavior without an ADR.
- Do not add dependency installation behavior to `forge init`.

## Immediate Next Step

The next logical work is to review the `forge init <project-name>` specification, confirm template readiness, and define CLI testing expectations.

Do not implement `forge init` until bootstrap behavior is specified and reviewed.
