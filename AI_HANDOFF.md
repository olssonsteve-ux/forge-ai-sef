# AI Handoff

## Role Context

You are working in Forge, an AI Software Engineering Framework.

Forge is not an application. Do not assume product UI, API routes, database models, or runtime services exist.

## Current Repository State

The repository is at Forge 0.1 RC1 pre-implementation hardening stage and contains documentation only.

There is no production code and no CLI implementation.

Milestone 0 architecture review has been recorded in `docs/architecture/review-000.md`.

Project memory schemas, ADR lifecycle rules, standard categories, template governance, and the `forge init <project-name>` pre-implementation specification are documented under `docs/contracts/`, `standards/`, and `templates/`.

The bootstrap template system is defined in `docs/contracts/bootstrap-template-system.md`. `forge init` must use versioned templates from `templates/bootstrap/` and must not hardcode generated file contents.

Forge Capability Specifications live under `docs/capabilities/`. FCS-001 defines the Review Capability and should be read before any `forge review` implementation work.

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
- Follow `docs/contracts/bootstrap-template-system.md` before changing bootstrap templates or generation behavior.
- Follow `docs/capabilities/FCS-001-Review.md` before designing or implementing review behavior.
- Keep documentation clear enough for a new contributor to understand without chat history.
- Prefer small, reviewable changes over broad framework expansion.

## Forbidden Actions

- Do not implement `forge init` until the user explicitly approves CLI implementation.
- Do not add production code during architecture or hardening work.
- Do not add destructive overwrite behavior without an ADR.
- Do not add dependency installation behavior to `forge init`.
- Do not hardcode generated project file contents in CLI code.
- Do not implement `forge review` until report persistence, `N/A` scoring behavior, command scope, and output format are specified.

## Immediate Next Step

The next logical work is to either begin `forge init` implementation after explicit approval or continue specifying FCS-001 implementation details such as review report storage, `N/A` scoring, command scope, and output format.

Do not implement `forge init` until bootstrap behavior is specified and reviewed.
