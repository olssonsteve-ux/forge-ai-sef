# AI Handoff

## Role Context

You are working in Forge, an AI-Native Software Engineering Platform.

Forge is not an application. Do not assume product UI, API routes, database models, or runtime services exist.

Forge's motto is: Build software with intention.

## Current Repository State

The repository is at Forge `0.3.3` Governance Runtime Status Service implementation stage.

The highest governing document is `CONSTITUTION.md`. Future strategy, roadmap, capability specifications, engineering briefs, implementation, testing, Design Authority Review, and release decisions should derive from it.

AI agent behavior is governed by `AI_ENGINEERING_CONDUCT.md`.

Governance Runtime is specified in `docs/capabilities/FCS-002-Governance-Runtime.md`. Its first read-only Status Service is implemented.

AR-0001 reviews the Forge engineering hierarchy and accepts Capability Slice as the layer between Capability Specification and Engineering Brief.

Capability Slices are governed by `docs/standards/capability-slice-standard.md`. New slices should start from `templates/capability-slices/CS-template.md`.

The first Governance Runtime Capability Slice is `docs/capabilities/CS-002.1-Governance-Runtime-Status-Service.md`. It defines a read-only Status Service that will later support `forge status`.

`docs/reviews/DAR-CS-0001-CS-002.1-Status-Service.md` reviews CS-002.1 and gives it a decision of `PASS WITH COMMENTS`. It confirms that the slice is ready for Engineering Brief creation.

`docs/engineering/EB-002.1-Implement-Status-Service.md` is the accepted implementation brief for the first Governance Runtime service and future `forge status` command.

`forge/status.py` implements the read-only Status Service. `forge status` is wired in `forge/cli.py`.

There is now a Python package and Typer CLI implementation for `forge init <project-name>` and `forge status`.

Release readiness documentation lives under `docs/release/`.

DAR-0001 lives at `docs/reviews/DAR-0001-Forge-0.2.md` and is the baseline for Forge `0.3`.

Gate 1 dogfooding lives at `docs/reviews/GATE-0001-Dogfooding-ForgePlayground.md`. It verified that `python -m forge init ForgePlayground` runs successfully from outside the repository and produced a decision of `PASS WITH COMMENTS`.

The current patch resolves non-blocking Gate 1 issues by aligning generated Forge version output with `v0.2.1` and strengthening first-session architecture discovery guidance in the generated README and AI handoff templates.

Forge 0.3 adds the Developer Platform baseline: testing standard, code quality standard, GitHub Actions CI standard, Ruff configuration, and a CI workflow under `.github/workflows/ci.yml`.

ADR 0011 records the decision to use `CONSTITUTION.md` as the highest governing document and to identify Forge as an AI-Native Software Engineering Platform.

ADR 0012 records the decision to establish `AI_ENGINEERING_CONDUCT.md` as the root AI behavior contract.

ADR 0013 records the decision to establish Governance Runtime as a permanent Forge capability.

ADR 0014 records the decision to introduce Capability Slices.

Milestone 0 architecture review has been recorded in `docs/architecture/review-000.md`.

Project memory schemas, ADR lifecycle rules, standard categories, template governance, and the `forge init <project-name>` pre-implementation specification are documented under `docs/contracts/`, `standards/`, and `templates/`.

The bootstrap template system is defined in `docs/contracts/bootstrap-template-system.md`. `forge init` must use versioned templates from `templates/bootstrap/` and must not hardcode generated file contents.

Forge Capability Specifications live under `docs/capabilities/`. FCS-001 defines the Review Capability and should be read before any `forge review` implementation work.

## Current Architectural Intent

Forge should be built in this order:

1. architecture and vision
2. project memory contracts
3. standards and templates
4. bootstrap specification
5. minimal CLI
6. automation and governance

## Instructions For Future AI Agents

- Keep production code scoped to explicitly approved Forge capabilities.
- Read `CONSTITUTION.md` before major planning, governance, capability, review, or release work.
- Read `AI_ENGINEERING_CONDUCT.md` before any meaningful project work.
- Preserve project memory files when making changes.
- Update `PROJECT_STATE.md` when the project status changes.
- Update `PROJECT_BRAIN.md` when durable decisions or project beliefs change.
- Add architectural decisions under `docs/decisions/` for meaningful direction changes.
- Check `docs/README.md` before changing documentation authority or duplicating concepts.
- Follow `docs/contracts/` before changing project memory or CLI behavior.
- Follow `docs/contracts/bootstrap-template-system.md` before changing bootstrap templates or generation behavior.
- Follow `docs/capabilities/FCS-001-Review.md` before designing or implementing review behavior.
- Follow `docs/capabilities/FCS-002-Governance-Runtime.md` before designing or implementing governance runtime behavior.
- Follow `docs/architecture/AR-0001-Engineering-Hierarchy.md` before changing the engineering hierarchy.
- Follow `docs/standards/capability-slice-standard.md` before creating or changing Capability Slices.
- Follow `docs/capabilities/CS-002.1-Governance-Runtime-Status-Service.md` before creating the first Governance Runtime Engineering Brief or implementing `forge status`.
- Follow `docs/reviews/DAR-CS-0001-CS-002.1-Status-Service.md` before creating EB-002.1.
- Follow `docs/engineering/EB-002.1-Implement-Status-Service.md` before implementing `forge status`.
- Follow `docs/release/release-standard.md` before tagging or changing release process.
- Follow `docs/engineering/EB-003-Developer-Platform.md` before changing developer tooling.
- Follow `docs/standards/testing-standard.md` before changing test expectations.
- Follow `docs/standards/code-quality-standard.md` before changing lint or format behavior.
- Follow `docs/ci/github-actions-standard.md` before changing CI behavior.
- Read `docs/reviews/DAR-0001-Forge-0.2.md` before planning Forge `0.3`.
- Read `docs/reviews/GATE-0001-Dogfooding-ForgePlayground.md` before changing bootstrap templates, generated structure, or Forge `0.3` scope.
- Read `docs/decisions/0011-forge-constitutional-governance-and-product-identity.md` before changing Forge identity or governance hierarchy.
- Read `docs/decisions/0012-ai-engineering-conduct.md` before changing AI conduct rules.
- Read `docs/decisions/0013-governance-runtime-capability.md` before changing Governance Runtime direction.
- Read `docs/decisions/0014-introduce-capability-slices.md` before creating or bypassing Capability Slices.
- Keep documentation clear enough for a new contributor to understand without chat history.
- Prefer small, reviewable changes over broad platform expansion.

## Forbidden Actions

- Do not expand `forge init` beyond bootstrap without an accepted specification.
- Do not add destructive overwrite behavior without an ADR.
- Do not add dependency installation behavior to `forge init`.
- Do not hardcode generated project file contents in CLI code.
- Do not implement `forge review` until report persistence, `N/A` scoring behavior, command scope, and output format are specified.
- Do not publish Forge `0.2.0` to a package index.
- Do not redesign the generated `forge/` folder as part of the `0.2.x` patch.
- Do not start Forge `0.4` Governance Runtime until AI Engineering Conduct is accepted.
- Do not implement Governance Runtime until its first service, interface, inputs, outputs, persistence, scoring policy, and failure behavior are specified.
- Do not create Engineering Briefs for large multi-service capabilities until a Capability Slice is accepted.
- Do not add `forge plan`, `forge doctor`, `forge score`, `forge memory`, `forge risks`, or `forge release` yet.
- Do not make the first Status Service mutate files, approve releases, create reviews, update project memory, or score complex code quality.
- Do not add strict mode, JSON output, persisted reports, Governance Score, policy packs, or release-blocking behavior as part of EB-002.1.

## Immediate Next Step

The next logical work is to review the EB-002.1 implementation and confirm `forge status` remains read-only, informational, and scoped to CS-002.1.

The implementation includes a read-only Status Service, separate CLI wiring, human-readable output, no runtime file writes, no project memory mutation, and tests proving read-only behavior.

Do not change `forge init`, bootstrap templates, `forge review`, plugins, project profiles, or migration tooling as part of the Status Service review.

Before expanding functionality, revisit the remaining bootstrap concern from Gate 1: generated `forge/` versus `src/`.
