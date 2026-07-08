---
template_name: bootstrap-ai-handoff
version: 0.1.1
compatible_forge_versions: ">=0.3,<0.4"
description: "Initial AI_HANDOFF.md for AI contributors."
variables:
  - PROJECT_NAME
  - FORGE_VERSION
  - CREATED_DATE
required_variables:
  - PROJECT_NAME
  - FORGE_VERSION
  - CREATED_DATE
optional_variables: []
---
# AI Handoff

## Role Context

You are working in `{{PROJECT_NAME}}`, a Forge-governed project.

## Current Repository State

The repository was initialized with Forge `{{FORGE_VERSION}}` on `{{CREATED_DATE}}`.

There is no production code unless project maintainers have added it after initialization.

## Current Architectural Intent

Begin with architecture discovery, project memory, and ADRs before implementation.

## Instructions For Future AI Agents

- Read `PROJECT_STATE.md` before making changes.
- Read `PROJECT_BRAIN.md` before making architectural decisions.
- Add ADRs for durable decisions.
- Do not assume implementation details that are not documented.

## Immediate Next Step

Perform architecture discovery for `{{PROJECT_NAME}}`.

Recommended first-session sequence:

1. Read `README.md`, `PROJECT_STATE.md`, and `PROJECT_BRAIN.md`.
2. Ask for or define the project purpose, boundaries, and non-goals.
3. Identify architectural risks before proposing implementation.
4. Record accepted decisions in `docs/decisions/`.
5. Update project memory before writing production code.
