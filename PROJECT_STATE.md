# Project State

## Status

Capability specification stage.

## Current Version

`0.1 RC1`

## Current Objective

Define FCS-001 Review Capability as the first permanent Forge capability.

## What Exists

- repository structure
- project purpose
- project vision
- architecture proposal
- initial architectural decisions
- roadmap from `0.1` to `1.0`
- project memory documents
- AI handoff document
- Milestone 0 architecture review record
- documentation authority map
- accepted project memory schemas
- ADR lifecycle and status rules
- standard categories and acceptance criteria
- template ownership, versioning, and change rules
- pre-implementation specification for `forge init <project-name>`
- bootstrap template system contract
- versioned bootstrap template directory
- initial bootstrap templates with metadata and variables
- Forge Capability Specification directory
- FCS-001 Review Capability specification
- ADR for Forge Capability Specifications

## What Does Not Exist

- production code
- CLI
- Python package configuration
- generated project bootstrap behavior
- automated tests
- release automation
- implemented `forge init`
- accepted first CLI verification expectations
- accepted release standard
- automated template validation
- template migration tooling
- implemented review command
- review report template
- automated review scoring

## Architectural Posture

Forge should be documentation-led first, then contract-led, then implementation-led.

Implementation should only begin after the core framework concepts are explicit enough to test and review.

Milestone 0 adds an explicit architecture review gate before implementation work. Architecture review findings should be recorded under `docs/architecture/`, and durable governance decisions should be recorded as ADRs.

Forge 0.1 RC1 is accepted as the architecture foundation. Pre-implementation hardening defines contracts for project memory, ADRs, standards, templates, and the first CLI command without writing production code.

The final architecture milestone defines Forge as template-driven. `forge init <project-name>` must render versioned templates from `templates/bootstrap/` and must not hardcode generated file contents.

Forge now evolves permanent capabilities through Forge Capability Specifications under `docs/capabilities/`. FCS-001 defines how Forge performs project reviews before any review command is implemented.

## Next Recommended Work

1. Decide whether to implement `forge init` first or specify review report persistence before review implementation.
2. For FCS-001 implementation, define review report file location and naming.
3. Finalize `N/A` scoring behavior for review categories.
4. Choose the first review command scope.
5. Keep review automation advisory until memory update behavior is specified.
