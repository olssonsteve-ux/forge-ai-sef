---
template_name: bootstrap-readme
version: 1.0.0
compatible_forge_versions: ">=0.5,<0.6"
description: "README for a new Forge-governed project."
variables:
  - PROJECT_NAME
  - PROJECT_DESCRIPTION
  - AUTHOR
  - FORGE_VERSION
  - BOOTSTRAP_OUTPUT_CONTRACT
  - CREATED_DATE
required_variables:
  - PROJECT_NAME
  - FORGE_VERSION
  - BOOTSTRAP_OUTPUT_CONTRACT
  - CREATED_DATE
optional_variables:
  - PROJECT_DESCRIPTION
  - AUTHOR
---
# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

This project was initialized with Forge `{{FORGE_VERSION}}` on `{{CREATED_DATE}}`.

Bootstrap output contract: `{{BOOTSTRAP_OUTPUT_CONTRACT}}`

No source-code directory was generated intentionally. Universal bootstrap does not select a
language, package, framework, deployment architecture, or source layout. Select those through
architecture discovery before creating source structure.

## Status

Foundation stage.

## Ownership

Author: {{AUTHOR}}

## First Session

Begin architecture discovery before writing production code.

Recommended first-session sequence:

1. Define the project purpose.
2. Define project boundaries and non-goals.
3. Select language, packaging, deployment constraints, and source layout.
4. Identify architectural risks.
5. Record durable decisions in `docs/decisions/`.
6. Update `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, and `AI_HANDOFF.md`.
