---
template_name: bootstrap-ai-handoff
version: 1.0.0
compatible_forge_versions: ">=1.0.0rc1,<2.0"
description: "Initial AI_HANDOFF.md for AI contributors."
variables:
  - PROJECT_NAME
  - FORGE_VERSION
  - BOOTSTRAP_OUTPUT_CONTRACT
  - CREATED_DATE
required_variables:
  - PROJECT_NAME
  - FORGE_VERSION
  - BOOTSTRAP_OUTPUT_CONTRACT
  - CREATED_DATE
optional_variables: []
---
# AI Handoff

## Role Context

You are working in `{{PROJECT_NAME}}`, a Forge-governed project.

## Current Repository State

The repository was initialized with Forge `{{FORGE_VERSION}}` on `{{CREATED_DATE}}`.

Bootstrap output contract: `{{BOOTSTRAP_OUTPUT_CONTRACT}}`

There is no production code unless project maintainers have added it after initialization.

## Current Architectural Intent

No source layout has been accepted. Universal bootstrap intentionally created no source-code
directory and selected no language, package, framework, or deployment architecture.

Begin with architecture discovery, project memory, and ADRs before implementation. Establish the
project purpose, boundaries, language, packaging or deployment constraints, and source layout
through the project's architecture process.

## Instructions For Future AI Agents

- Read `PROJECT_STATE.md` before making changes.
- Read `PROJECT_BRAIN.md` before making architectural decisions.
- Add ADRs for durable decisions.
- Do not assume implementation details that are not documented.
- Do not invent or create source structure before the project records an accepted decision.

## Immediate Next Step

Perform architecture discovery for `{{PROJECT_NAME}}`.

Recommended first-session sequence:

1. Read `README.md`, `PROJECT_STATE.md`, and `PROJECT_BRAIN.md`.
2. Ask for or define the project purpose, boundaries, and non-goals.
3. Establish language, packaging or deployment constraints, and source layout.
4. Identify architectural risks before proposing implementation.
5. Record accepted decisions in `docs/decisions/`.
6. Update project memory before writing production code.
