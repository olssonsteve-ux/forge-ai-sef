# Project State

## Status

Forge 0.2.0 release readiness stage.

## Current Version

`0.2.0`

## Current Objective

Prepare Forge `0.2.0` for tagging.

## What Exists

- repository structure
- project purpose
- project vision
- architecture proposal
- initial architectural decisions
- roadmap from `0.1` to `1.0`
- project memory documents
- AI handoff document
- Milestone 0 architecture review record
- documentation authority map
- accepted project memory schemas
- ADR lifecycle and status rules
- standard categories and acceptance criteria
- template ownership, versioning, and change rules
- pre-implementation specification for `forge init <project-name>`
- bootstrap template system contract
- versioned bootstrap template directory
- initial bootstrap templates with metadata and variables
- Forge Capability Specification directory
- FCS-001 Review Capability specification
- ADR for Forge Capability Specifications
- Python package configuration
- Typer-based CLI entrypoint
- implemented `forge init <project-name>`
- template loading and validation
- bootstrap rendering from `templates/bootstrap/`
- dry-run mode
- conservative overwrite protection
- automated tests for the first CLI command
- release standard
- Forge `0.2.0` release checklist
- documented packaging decision
- tag recommendation for `v0.2.0`

## What Does Not Exist

- release automation
- template migration tooling
- implemented review command
- review report template
- automated review scoring
- plugin system
- project profiles beyond bootstrap

## Architectural Posture

Forge should be documentation-led first, then contract-led, then implementation-led.

Implementation should only begin after the core framework concepts are explicit enough to test and review.

Milestone 0 adds an explicit architecture review gate before implementation work. Architecture review findings should be recorded under `docs/architecture/`, and durable governance decisions should be recorded as ADRs.

Forge 0.1 RC1 is accepted as the architecture foundation. Pre-implementation hardening defines contracts for project memory, ADRs, standards, templates, and the first CLI command without writing production code.

The final architecture milestone defines Forge as template-driven. `forge init <project-name>` must render versioned templates from `templates/bootstrap/` and must not hardcode generated file contents.

Forge now evolves permanent capabilities through Forge Capability Specifications under `docs/capabilities/`. FCS-001 defines how Forge performs project reviews before any review command is implemented.

Forge 0.2 introduces the first implementation layer. `forge init <project-name>` is intentionally narrow: it renders bootstrap templates, creates the default folder structure, supports dry-run, validates project names, and refuses to overwrite non-empty directories.

Forge 0.2.0 is prepared as a local-editable release. It should not be published to a package index yet.

## Next Recommended Work

1. Run `python -m pytest`.
2. Run `python -m forge init release-smoke --dry-run`.
3. Commit release readiness documentation.
4. Tag `v0.2.0` if the working tree is clean.
5. After tagging, specify review report persistence before implementing `forge review`.
