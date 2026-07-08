# 0007 - Standard And Template Governance

Date: 2026-07-08

## Status

Accepted

## Context

Forge will eventually provide standards and templates. Without governance, these assets could grow inconsistently or become hidden implementation behavior.

## Decision

Forge will define standard categories in `standards/categories.md` and template governance in `templates/governance.md`.

Standards must be human-readable before automation checks them.

Templates must be transparent and useful without Forge installed.

## Consequences

- Standards and templates have acceptance criteria before implementation.
- Future `forge init` behavior must use accepted template rules.
- Validation automation must follow accepted standards rather than inventing rules.
