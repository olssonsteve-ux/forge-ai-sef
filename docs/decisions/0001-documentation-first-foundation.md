# 0001 - Documentation-First Foundation

Date: 2026-07-08

## Status

Accepted

## Context

Forge is beginning as an AI Software Engineering Framework, not an application. The project needs architectural clarity before implementation.

Writing code before defining the framework purpose, boundaries, and evolution path would create premature structure and make later governance harder.

## Decision

Forge will begin with documentation only.

The initial repository will include project memory, architecture discovery, decisions, roadmap, standards and templates directories, and reserved future implementation and test directories.

No production code or CLI will be added in `0.1`.

## Consequences

- The project is understandable before implementation.
- Future code can be measured against documented intent.
- Early velocity is lower, but architectural drift risk is reduced.
