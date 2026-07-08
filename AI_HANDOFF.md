# AI Handoff

## Role Context

You are working in Forge, an AI Software Engineering Framework.

Forge is not an application. Do not assume product UI, API routes, database models, or runtime services exist.

## Current Repository State

The repository is at Forge `0.2.0` release readiness stage.

There is now a Python package and Typer CLI implementation for `forge init <project-name>`.

Release readiness documentation lives under `docs/release/`.

DAR-0001 lives at `docs/reviews/DAR-0001-Forge-0.2.md` and is the baseline for Forge `0.3`.

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

- Keep production code scoped to explicitly approved Forge capabilities.
- Preserve project memory files when making changes.
- Update `PROJECT_STATE.md` when the project status changes.
- Update `PROJECT_BRAIN.md` when durable decisions or project beliefs change.
- Add architectural decisions under `docs/decisions/` for meaningful direction changes.
- Check `docs/README.md` before changing documentation authority or duplicating concepts.
- Follow `docs/contracts/` before changing project memory or CLI behavior.
- Follow `docs/contracts/bootstrap-template-system.md` before changing bootstrap templates or generation behavior.
- Follow `docs/capabilities/FCS-001-Review.md` before designing or implementing review behavior.
- Follow `docs/release/release-standard.md` before tagging or changing release process.
- Read `docs/reviews/DAR-0001-Forge-0.2.md` before planning Forge `0.3`.
- Keep documentation clear enough for a new contributor to understand without chat history.
- Prefer small, reviewable changes over broad framework expansion.

## Forbidden Actions

- Do not expand `forge init` beyond bootstrap without an accepted specification.
- Do not add destructive overwrite behavior without an ADR.
- Do not add dependency installation behavior to `forge init`.
- Do not hardcode generated project file contents in CLI code.
- Do not implement `forge review` until report persistence, `N/A` scoring behavior, command scope, and output format are specified.
- Do not publish Forge `0.2.0` to a package index.

## Immediate Next Step

The next logical work is to commit DAR-0001, then choose Forge `0.3` scope with the DAR risks in view.

Do not implement `forge review`, plugins, project profiles, or migration tooling yet.
