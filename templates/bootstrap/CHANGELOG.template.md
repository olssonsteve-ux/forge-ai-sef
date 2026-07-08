---
template_name: bootstrap-changelog
version: 0.1.0
compatible_forge_versions: ">=0.1,<0.2"
description: "Initial changelog for a Forge-governed project."
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
# Changelog

All notable changes to `{{PROJECT_NAME}}` will be documented in this file.

## [Unreleased]

### Added

- Initialized project with Forge `{{FORGE_VERSION}}` on `{{CREATED_DATE}}`.
