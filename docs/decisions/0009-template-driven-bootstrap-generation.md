# 0009 - Template-Driven Bootstrap Generation

Date: 2026-07-08

## Status

Accepted

## Context

Forge will eventually implement `forge init <project-name>`. The command needs to create project files, but generated content must remain visible and governed.

If the CLI hardcodes generated file bodies, documentation and implementation will drift. Template changes would require code changes, and reviewers would need to inspect Python implementation to understand generated project structure.

## Decision

Forge bootstrap generation will be template-driven.

The CLI must render versioned templates from `templates/bootstrap/` and must not hardcode generated project file contents.

Template architecture, metadata, variables, validation, versioning, and compatibility rules are defined in `docs/contracts/bootstrap-template-system.md`.

## Consequences

- Generated content remains reviewable as documentation assets.
- Template evolution can be governed independently from CLI engine behavior.
- `forge init` implementation must include template loading and validation.
- Template compatibility becomes part of Forge release management.
- Future migration support has a clear source of truth.
