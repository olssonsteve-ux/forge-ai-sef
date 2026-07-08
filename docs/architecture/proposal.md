# Architecture Proposal

Forge should be a constitution-led, contract-first platform with optional automation.

## Architectural Style

Forge should separate stable platform concepts from executable tooling.

The durable core is the set of files, schemas, decisions, standards, templates, and workflows that define how a project is governed. Automation should read and write those contracts rather than inventing behavior hidden inside code.

## Future Layers

### 1. Platform Contracts

Defines the repository files, document formats, lifecycle rules, and version expectations.

Examples:

- project state contract
- project brain contract
- AI handoff contract
- decision record contract
- roadmap contract
- changelog contract

### 2. Template Library

Provides reusable starting documents and project structures.

Templates should remain visible and editable. Generated output should be understandable without Forge installed.

### 3. Standards Library

Defines engineering expectations for architecture, testing, Git, release management, documentation, and AI collaboration.

Standards should be written for humans first and checked by tools later.

### 4. Bootstrap Engine

Creates a project foundation from a selected profile.

The bootstrap engine should be conservative. It should avoid destructive operations and should explain what it will create or change.

### 5. Governance Engine

Inspects a project and reports whether it follows Forge expectations.

Governance should start as advisory. Strict enforcement can be added only after standards are mature.

### 6. CLI Adapter

Provides a human-facing command interface.

The CLI should call documented platform behavior rather than becoming the architecture itself.

### 7. Integration Adapters

Connect Forge to external tools such as Git, CI systems, editors, and AI agents.

Adapters should be replaceable and should not leak vendor-specific assumptions into the core platform.

## Initial Physical Structure

For `0.1`, the physical structure should remain documentation-focused:

- `docs/architecture/` for architecture discovery and proposals
- `docs/decisions/` for architectural decisions
- `docs/vision/` for purpose, vision, and boundaries
- `standards/` for future standards
- `templates/` for future templates
- `forge/` reserved for future Python implementation
- `tests/` reserved for future tests

## Evolution Rule

Do not add a code module until there is a documented contract or behavior for it.

Do not add automation until the relevant contract has passed architecture review.
