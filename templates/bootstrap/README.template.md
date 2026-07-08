---
template_name: bootstrap-readme
version: 0.1.1
compatible_forge_versions: ">=0.2,<0.3"
description: "README for a new Forge-governed project."
variables:
  - PROJECT_NAME
  - PROJECT_DESCRIPTION
  - AUTHOR
  - FORGE_VERSION
  - CREATED_DATE
required_variables:
  - PROJECT_NAME
  - FORGE_VERSION
  - CREATED_DATE
optional_variables:
  - PROJECT_DESCRIPTION
  - AUTHOR
---
# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

This project was initialized with Forge `{{FORGE_VERSION}}` on `{{CREATED_DATE}}`.

## Status

Foundation stage.

## Ownership

Author: {{AUTHOR}}

## First Session

Begin architecture discovery before writing production code.

Recommended first-session sequence:

1. Define the project purpose.
2. Define project boundaries and non-goals.
3. Identify architectural risks.
4. Record durable decisions in `docs/decisions/`.
5. Update `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, and `AI_HANDOFF.md`.
