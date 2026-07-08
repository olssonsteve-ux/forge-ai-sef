# Changelog

All notable changes to Forge will be documented in this file.

Forge follows a deliberate pre-1.0 evolution model. Until `1.0`, breaking changes are allowed when they improve the long-term platform contract, but they must be documented.

## [0.3.0] - 2026-07-08

### Added

- Added `CONSTITUTION.md` as Forge's highest governing document.
- Established the motto: "Build software with intention."
- Established Forge's official identity as an AI-Native Software Engineering Platform.
- Added ADR 0011 for constitutional governance and product identity.
- Aligned README, project memory, vision, architecture, roadmap, and documentation authority with the constitutional model.
- Added Developer Platform engineering brief.
- Added testing standard.
- Added code quality standard.
- Added GitHub Actions CI standard.
- Added GitHub Actions workflow for push and pull request verification.
- Added Ruff as the lightweight lint and format check tool.
- Added local quality command documentation.

### Not Added

- No `forge review` implementation.
- No new user-facing CLI commands.
- No project profile expansion.
- No release automation or package publishing.

## [0.2.2] - 2026-07-08

### Fixed

- Updated package and runtime version metadata so generated projects report Forge `0.2.1`.
- Strengthened generated `README.md` and `AI_HANDOFF.md` guidance for the first architecture discovery session.

### Known Issues

- Generated projects still use a `forge/` placeholder directory. This remains a known Forge `0.3` design item and is not redesigned in this patch.

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
- Added DAR-0001 Design Authority Review for Forge `0.2.0`.

### Not Added

- No `forge review` implementation.
- No plugin system.
- No project profiles beyond bootstrap.
- No template migration tooling.
- No release automation.
- No package publishing.

## [0.2.1] - 2026-07-08

### Added

- Added Gate 1 dogfooding review for bootstrapping `ForgePlayground`.
- Recorded successful outside-repository execution of `python -m forge init ForgePlayground`.
- Documented generated project usefulness, template quality, project memory usefulness, and folder structure findings.

### Known Issues

- Generated projects report Forge `0.2.0` even when dogfooding release tag `v0.2.1`.
- Generated projects use a `forge/` placeholder directory, which may be less appropriate than `src/` for non-Forge projects.
- Bootstrap templates need stronger first-session architecture discovery guidance.
