---
template_name: bootstrap-readme
version: 0.1.0
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

## Next Step

Begin architecture discovery before writing production code.
