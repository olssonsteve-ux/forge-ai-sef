# Project State

## Status

Forge 0.2.2 patch readiness in progress.

## Current Version

`0.2.1`

## Current Objective

Resolve non-blocking Gate 1 bootstrap issues before starting Forge `0.3`.

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
- Python package configuration
- Typer-based CLI entrypoint
- implemented `forge init <project-name>`
- template loading and validation
- bootstrap rendering from `templates/bootstrap/`
- dry-run mode
- conservative overwrite protection
- automated tests for the first CLI command
- release standard
- Forge `0.2.0` release checklist
- documented packaging decision
- tag recommendation for `v0.2.0`
- DAR-0001 Design Authority Review baseline
- Gate 1 dogfooding review for `ForgePlayground`
- patch update aligning generated Forge version with `v0.2.1`
- strengthened first-session guidance in bootstrap README and AI handoff templates

## What Does Not Exist

- release automation
- template migration tooling
- implemented review command
- review report template
- automated review scoring
- plugin system
- project profiles beyond bootstrap
- CI pipeline
- formal testing standard
- review report persistence contract
- generated-project template provenance
- generated architecture discovery starter

## Architectural Posture

Forge should be documentation-led first, then contract-led, then implementation-led.

Implementation should only begin after the core framework concepts are explicit enough to test and review.

Milestone 0 adds an explicit architecture review gate before implementation work. Architecture review findings should be recorded under `docs/architecture/`, and durable governance decisions should be recorded as ADRs.

Forge 0.1 RC1 is accepted as the architecture foundation. Pre-implementation hardening defines contracts for project memory, ADRs, standards, templates, and the first CLI command without writing production code.

The final architecture milestone defines Forge as template-driven. `forge init <project-name>` must render versioned templates from `templates/bootstrap/` and must not hardcode generated file contents.

Forge now evolves permanent capabilities through Forge Capability Specifications under `docs/capabilities/`. FCS-001 defines how Forge performs project reviews before any review command is implemented.

Forge 0.2 introduces the first implementation layer. `forge init <project-name>` is intentionally narrow: it renders bootstrap templates, creates the default folder structure, supports dry-run, validates project names, and refuses to overwrite non-empty directories.

Forge 0.2.0 is prepared as a local-editable release. It should not be published to a package index yet.

DAR-0001 gives Forge `0.2.0` a decision of `PASS WITH COMMENTS`. The main baseline risks are roadmap drift, lack of CI, missing testing standard, minimal template metadata parsing, missing review persistence, and missing template provenance.

Gate 1 dogfooding verified that `python -m forge init ForgePlayground` runs successfully from outside the Forge repository and creates a usable project foundation. The decision is `PASS WITH COMMENTS`. The main findings were version traceability drift between tag `v0.2.1` and generated `0.2.0` content, possible confusion from generating a `forge/` folder in arbitrary projects, and a need for stronger first-session guidance in generated templates.

The non-blocking Gate 1 issues are being handled as a narrow patch. Generated projects should now report Forge `0.2.1`, and the generated README and AI handoff templates should better guide the first architecture discovery session. The generated `forge/` folder concern is documented as a Forge `0.3` design item and is intentionally not redesigned in this patch.

## Next Recommended Work

1. Run patch readiness checks.
2. Commit the Forge `0.2.2` patch readiness changes.
3. Decide whether generated projects should use `src/` instead of `forge/` during Forge `0.3` planning.
4. Define testing standard and CI expectations.
5. Specify review report persistence before implementing `forge review`.
