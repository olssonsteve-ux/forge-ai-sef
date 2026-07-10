# AI Handoff

## Role Context

You are working in Forge, an AI-Native Software Engineering Platform.

Forge is not an application. Do not assume product UI, API routes, database models, or runtime services exist.

Forge's motto is: Build software with intention.

## Current Repository State

The repository is released as Forge `v0.4.1` with the Governance Runtime Status Service and Version Consistency Status implemented.

`docs/standards/ai-implementation-protocol.md` is now the default implementation protocol for AI agents implementing Engineering Briefs. ADR 0015 records this decision.

`docs/standards/lifecycle-standard.md` is now the lifecycle authority for Forge artifacts. ADR 0016 records this decision.

PRR-0001 records a post-release version consistency issue discovered after `v0.4.0`: some active documentation still referenced Forge `0.3.3` after tagging. The documentation was corrected, and the durable lesson is that Governance Runtime needs an explicit version consistency check.

CS-002.2 now specifies that future version consistency check as a read-only `forge status` extension.

DAR-CS-0002 reviews CS-002.2 and gives it a decision of `PASS WITH COMMENTS`. The slice is ready for EB-002.2.

`docs/engineering/EB-002.2-Implement-Version-Consistency-Check.md` is the accepted implementation brief for adding Version Consistency Status to `forge status`. The implementation is now present in `forge/status.py`.

`docs/reviews/DAR-EB-0002-EB-002.2-Version-Consistency-Implementation.md` reviews the EB-002.2 implementation and gives it a `PASS` decision. CS-002.2 is now closed.

The highest governing document is `CONSTITUTION.md`. Future strategy, roadmap, capability specifications, engineering briefs, implementation, testing, Design Authority Review, and release decisions should derive from it.

AI agent behavior is governed by `AI_ENGINEERING_CONDUCT.md`.

Governance Runtime is specified in `docs/capabilities/FCS-002-Governance-Runtime.md`. Its first read-only Status Service is implemented.

AR-0001 reviews the Forge engineering hierarchy and accepts Capability Slice as the layer between Capability Specification and Engineering Brief.

Capability Slices are governed by `docs/standards/capability-slice-standard.md`. New slices should start from `templates/capability-slices/CS-template.md`.

The first Governance Runtime Capability Slice is `docs/capabilities/CS-002.1-Governance-Runtime-Status-Service.md`. It defines a read-only Status Service that will later support `forge status`.

The second Governance Runtime Capability Slice is `docs/capabilities/CS-002.2-Governance-Runtime-Version-Consistency-Check.md`. It defines read-only version consistency checks across Git tags, active documentation, project memory, changelog, package metadata when present, release documentation, and repository metadata.

`docs/reviews/DAR-CS-0002-CS-002.2-Version-Consistency.md` records the architecture review for CS-002.2.

EB-002.2 requires conservative parsing, local Git-only inspection, no new CLI command, no automatic fixes, no report persistence, no release approval, and no runtime project memory mutation.

`docs/reviews/DAR-CS-0001-CS-002.1-Status-Service.md` reviews CS-002.1 and gives it a decision of `PASS WITH COMMENTS`. It confirms that the slice is ready for Engineering Brief creation.

`docs/engineering/EB-002.1-Implement-Status-Service.md` is the accepted implementation brief for the first Governance Runtime service and future `forge status` command.

`forge/status.py` implements the read-only Status Service. `forge status` is wired in `forge/cli.py`. Version Consistency Status compares the latest local release tag with active release-facing references in README, changelog, project state, AI handoff, and package metadata when present.

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

ADR 0015 records the decision to adopt the AI Implementation Protocol.

ADR 0016 records the decision to adopt the Forge Lifecycle Standard.

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
- Follow `docs/standards/ai-implementation-protocol.md` before implementing any Engineering Brief.
- Follow `docs/standards/lifecycle-standard.md` before changing artifact lifecycle status.
- Follow `docs/capabilities/CS-002.1-Governance-Runtime-Status-Service.md` before creating the first Governance Runtime Engineering Brief or implementing `forge status`.
- Follow `docs/capabilities/CS-002.2-Governance-Runtime-Version-Consistency-Check.md` before extending `forge status` with version consistency behavior.
- Follow `docs/reviews/DAR-CS-0002-CS-002.2-Version-Consistency.md` before creating EB-002.2.
- Follow `docs/engineering/EB-002.2-Implement-Version-Consistency-Check.md` before implementing version consistency behavior.
- Follow `docs/reviews/DAR-EB-0002-EB-002.2-Version-Consistency-Implementation.md` before closing CS-002.2 or extending version consistency behavior.
- Follow `docs/reviews/DAR-CS-0001-CS-002.1-Status-Service.md` before creating EB-002.1.
- Follow `docs/engineering/EB-002.1-Implement-Status-Service.md` before implementing `forge status`.
- Follow `docs/release/release-standard.md` before tagging or changing release process.
- Read `docs/reviews/PRR-0001-v0.4.0-Post-Release-Review.md` before changing release checks or extending Governance Runtime release/status behavior.
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
- Read `docs/decisions/0015-ai-implementation-protocol.md` before changing implementation workflow expectations.
- Read `docs/decisions/0016-lifecycle-standard.md` before changing lifecycle terminology or status rules.
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
- Do not add automatic version updates, changelog rewrites, release approval, or project memory mutation without a dedicated accepted Capability Slice and Engineering Brief.
- Do not implement CS-002.2 before it passes DAR-CS and has an accepted Engineering Brief.
- Do not implement version consistency outside the EB-002.2 scope.
- Do not implement future Engineering Briefs without following the AI Implementation Protocol.
- Do not change lifecycle status without evidence and related project memory updates when required.

## Immediate Next Step

The next logical Governance Runtime work is selecting or defining the next Capability Slice.

Any future version consistency enhancement should begin as a new Capability Slice rather than expanding EB-002.2 opportunistically.

Do not change `forge init`, bootstrap templates, `forge review`, plugins, project profiles, or migration tooling as part of the Status Service review.

Before expanding functionality, revisit the remaining bootstrap concern from Gate 1: generated `forge/` versus `src/`.
