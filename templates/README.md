# Templates

This directory will contain reusable Forge templates.

Templates are reusable project starting points, not hidden generators. A generated or copied template should remain understandable without Forge installed.

## Directory Structure

- `bootstrap/` contains templates used by `forge init <project-name>`.
- `documentation/` is reserved for documentation artifact templates.
- `engineering/` is reserved for engineering workflow templates.
- `standards/` is reserved for standard document templates.

## Planned Templates

Planned templates include:

- project README template
- architecture discovery template
- decision record template
- AI handoff template
- project state template
- testing strategy template
- release checklist template

See `governance.md` for template ownership, versioning, and change rules.

See `../docs/contracts/bootstrap-template-system.md` for bootstrap template architecture, metadata, variables, validation, compatibility, and versioning rules.

## Acceptance Criteria

A Forge template should define:

- intended use
- required inputs
- generated or copied outputs
- owner document or standard
- version compatibility
- known limits

## Evolution Rule

Templates should produce output that remains useful even when Forge is not installed.

Template behavior must be specified before any future CLI command creates files from it.
