---
template_name: bootstrap-project-brain
version: 0.1.0
compatible_forge_versions: ">=0.2,<0.3"
description: "Initial PROJECT_BRAIN.md for durable project memory."
variables:
  - PROJECT_NAME
  - PROJECT_DESCRIPTION
  - FORGE_VERSION
required_variables:
  - PROJECT_NAME
  - FORGE_VERSION
optional_variables:
  - PROJECT_DESCRIPTION
---
# Project Brain

This file captures durable project knowledge that future human and AI contributors should preserve.

## Core Identity

`{{PROJECT_NAME}}` is a Forge-governed software project.

{{PROJECT_DESCRIPTION}}

## Guiding Beliefs

- Project memory should live in the repository.
- Architecture decisions should be explicit and reviewable.
- Implementation should follow documented intent.

## Product Shape

To be defined during architecture discovery.

## Important Boundaries

To be defined during architecture discovery.

## Current Decisions

- Initialized with Forge `{{FORGE_VERSION}}`.

## Open Questions

- What problem does this project solve?
- What is explicitly out of scope?
- What implementation constraints matter?
