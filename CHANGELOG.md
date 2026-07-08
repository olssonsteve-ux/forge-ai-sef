# Changelog

All notable changes to Forge will be documented in this file.

Forge follows a deliberate pre-1.0 evolution model. Until `1.0`, breaking changes are allowed when they improve the long-term framework contract, but they must be documented.

## [0.1.0] - 2026-07-08

### Added

- Established Forge as an AI Software Engineering Framework.
- Added foundation documentation.
- Added architecture discovery documents.
- Added project state and project memory files.
- Added AI handoff document.
- Added repository structure for future implementation, tests, standards, templates, and documentation.
- Added Milestone 0 architecture review.
- Added documentation authority map.
- Added architecture review gate ADR.
- Strengthened standards and templates governance.
- Accepted Milestone 0 as Forge 0.1 RC1.
- Added project memory schemas for `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, and `AI_HANDOFF.md`.
- Added ADR lifecycle, naming, and status rules.
- Added standard categories and acceptance criteria.
- Added template ownership, versioning, and change rules.
- Added pre-implementation specification for `forge init <project-name>`.
- Added bootstrap template system contract.
- Added template-driven bootstrap generation ADR.
- Added initial versioned bootstrap templates with metadata and variables.
- Added template category directories for bootstrap, documentation, engineering, and standards templates.
- Added first CLI implementation verification expectations for `forge init`.
- Added Forge Capability Specifications directory.
- Added FCS-001 Review Capability.
- Added ADR for permanent Forge Capability Specifications.

### Not Added

- No production code.
- No CLI.
- No package metadata.
- No runtime behavior.

## [0.2.0] - 2026-07-08

### Added

- Added Python package configuration.
- Added Typer-based CLI entrypoint.
- Implemented `forge init <project-name>`.
- Added template-backed bootstrap rendering from `templates/bootstrap/`.
- Added project name validation.
- Added dry-run mode.
- Added conservative overwrite protection for non-empty target directories.
- Added template metadata, variable, and compatibility validation.
- Added tests for project creation, invalid names, dry-run, overwrite protection, template rendering, and template discovery.
- Added release standard.
- Added Forge `0.2.0` release checklist.

### Not Added

- No `forge review` implementation.
- No plugin system.
- No project profiles beyond bootstrap.
- No template migration tooling.
- No release automation.
- No package publishing.
