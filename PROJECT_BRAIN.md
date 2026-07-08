# Project Brain

This file captures durable project knowledge that future human and AI contributors should preserve.

## Core Identity

Forge is an AI Software Engineering Framework.

Forge is not an application. It is a foundation for creating and governing future applications and software projects.

## Guiding Beliefs

- Good AI engineering starts with context quality.
- Project memory must live in the repository, not only in chat history.
- Architecture decisions should be explicit, dated, and reviewable.
- Automation should follow documented contracts.
- Human control should remain visible at key decision points.
- A framework should make good defaults easy without making exceptions impossible.
- Documentation needs clear authority so repeated summaries do not drift.
- Architecture review gates protect Forge from premature automation.
- Project memory files are contracts, not casual notes.
- CLI behavior must be specified before it is implemented.
- Bootstrap generation must be template-driven, not hardcoded in CLI code.
- Templates are versioned architecture assets.
- Permanent Forge capabilities are specified through FCS documents before implementation.
- Reviews must produce scores and narrative findings, not scores alone.
- The first implementation must stay narrow and prove the template-driven bootstrap path.

## Product Shape

Forge may eventually include:

- project bootstrap
- AI development workflow
- project memory
- engineering standards
- templates
- documentation governance
- architecture governance
- testing standards
- Git workflow
- release management

## Important Boundaries

- Forge should not become a hosted SaaS by default.
- Forge should not require a specific AI vendor.
- Forge should not hide architectural decisions in generated output.
- Forge should not generate production code before project intent is captured.

## Current Decisions

- Use documentation-first development for `0.1`.
- Use Python as the expected implementation language.
- Defer CLI implementation.
- Evaluate Typer before implementation, but do not introduce it yet.
- Keep empty implementation and test directories to establish future structure.
- Use `docs/README.md` as the documentation authority map.
- Require explicit architecture review gates before major implementation milestones.
- Accept Forge 0.1 RC1 as the architecture foundation.
- Define project memory schemas under `docs/contracts/`.
- Use ADR lifecycle and status rules from `docs/contracts/adr-lifecycle.md`.
- Govern standards through categories and acceptance criteria before automation.
- Govern templates through ownership, versioning, and change rules before generation.
- Specify `forge init <project-name>` before implementation.
- Use `templates/bootstrap/` as the source for generated project files.
- Require every template to define metadata, variables, required variables, and optional variables.
- Reject unknown or missing template variables before writing files.
- Verify first CLI behavior against the `forge init` specification before expanding scope.
- Use `docs/capabilities/` for Forge Capability Specifications.
- Accept FCS-001 as the Review Capability specification.
- Implement Forge `0.2.0` as a Typer-based Python CLI.
- Implement only `forge init <project-name>` for the first MVP.
- Keep generated file content in `templates/bootstrap/`, not in Python code.
- Use tests to protect dry-run, validation, overwrite protection, and template rendering.
- Release Forge `0.2.0` as local editable only.
- Use tag format `vX.Y.Z`, starting with `v0.2.0`.
- Do not publish Forge `0.2.0` to a package index.

## Open Questions

- What project profiles should Forge support first?
- Should Forge generate files directly or produce plans for human approval?
- How strict should Forge be when a project violates standards?
- Should Forge support plugin-style extensions before `1.0`?
- What scoring model should future architecture reviews use?
- What migration metadata should generated projects store after Forge `0.2`?
- Where should Forge Review Reports be stored?
- Should review project memory updates be automatic, suggested, or manual?
- Should `forge init` eventually write template provenance metadata into generated projects?
- What packaging channel should Forge use after local editable releases?
