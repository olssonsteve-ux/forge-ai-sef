---
template_name: bootstrap-project-state
version: 0.1.0
compatible_forge_versions: ">=1.0.0rc1,<2.0"
description: "Initial PROJECT_STATE.md for a Forge-governed project."
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
# Project State

## Status

Foundation stage.

## Current Version

Initialized with Forge `{{FORGE_VERSION}}`.

## Current Objective

Establish the architecture foundation for `{{PROJECT_NAME}}`.

## What Exists

- initial Forge project structure
- project memory files
- documentation directories

## What Does Not Exist

- production code
- implementation plan
- accepted architecture decisions
- test strategy

## Architectural Posture

Begin with purpose, boundaries, risks, and architecture decisions before implementation.

## Next Recommended Work

1. Define project purpose.
2. Define project boundaries.
3. Perform architecture discovery.
4. Record initial ADRs.
5. Decide implementation readiness.
