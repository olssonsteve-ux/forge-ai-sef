# Project State

## Status

DAR-CS-0003 returned `PASS` for CS-002.3 Governance Runtime Project Memory Health. The slice is
`DAR Approved`; bounded Engineering Brief creation is authorized, but implementation is not.

## Current Version

`v0.4.1`

## Planned Release

`v0.5.0` — pre-`1.0` minor release; not released or approved for tagging.

## Current Objective

Create and review one bounded Engineering Brief for DAR-approved CS-002.3 without beginning
implementation or release work.

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
- Developer Platform engineering brief
- testing standard
- code quality standard
- GitHub Actions CI standard
- GitHub Actions workflow for tests, lint, and format checks
- Ruff lint and format configuration
- root `CONSTITUTION.md`
- constitutional governance hierarchy
- official Forge identity as an AI-Native Software Engineering Platform
- official motto: "Build software with intention."
- ADR 0011 for constitutional governance and product identity
- root `AI_ENGINEERING_CONDUCT.md`
- ADR 0012 for AI Engineering Conduct
- FCS-002 Governance Runtime capability specification
- ADR 0013 for Governance Runtime Capability
- AR-0001 Engineering Hierarchy architecture review
- ADR 0014 introducing Capability Slices
- Capability Slice standard
- Capability Slice template
- CS-002.1 Governance Runtime Status Service Capability Slice
- DAR-CS-0001 review for CS-002.1
- EB-002.1 implementation brief for the Governance Runtime Status Service
- implemented read-only Governance Runtime Status Service
- implemented `forge status` command
- automated tests for status categories, missing artifacts, no-Git repositories, and read-only behavior
- PRR-0001 post-release review for `v0.4.0`
- CS-002.2 Governance Runtime Version Consistency Check Capability Slice
- DAR-CS-0002 review for CS-002.2
- EB-002.2 implementation brief for Governance Runtime Version Consistency Check
- implemented Version Consistency Status category inside `forge status`
- conservative local version comparison across Git tags, README, changelog, project memory, AI handoff, and `pyproject.toml` when present
- tests for matching versions, mismatches, missing tags, optional package metadata, dirty working trees, and read-only behavior
- AI Implementation Protocol standard
- ADR 0015 adopting the AI Implementation Protocol
- DAR-EB-0002 implementation review for EB-002.2 with a `PASS` decision
- closed CS-002.2 Governance Runtime Version Consistency Check
- Forge Lifecycle Standard
- ADR 0016 adopting the Forge Lifecycle Standard
- `docs/standards/README.md` standards index
- focused Lifecycle Standard re-review with a `PASS` result
- AR-0002 Generated Project Source Layout architecture review
- DAR-AR-0002 Generated Project Source Layout review with a `PASS` decision
- ADR 0017 accepting the Generated Project Source Layout decision
- accepted ADR 0017 revisions to the `forge init` and Bootstrap Template System contracts
- accepted manual compatibility guidance for projects generated with the historical `forge/` placeholder
- accepted `forge-bootstrap/2.0.0` output-contract identity
- focused bootstrap contract review with a `PASS` result
- accepted EB-004 Implement Universal Bootstrap Output Contract 2.0.0 in `Implementation Ready`
- focused EB-004 review with a `PASS` result
- implemented `forge-bootstrap/2.0.0` output identity and exact eight-directory/eight-file plan
- generated README and AI handoff source-layout deferral guidance
- language-neutral generated `.gitignore` baseline
- exact-output, dry-run equivalence, identity, template, and safeguard tests for EB-004
- EB-004 implementation and release-readiness evidence pending formal review
- DAR-EB-0003 formal EB-004 implementation review with `PASS WITH CONDITIONS`
- accepted Release Authority decision targeting `v0.5.0` with template compatibility
  `>=0.5,<0.6`
- planned `v0.5.0` release checklist with tagging blocked pending remaining gates
- focused DAR-EB-0003 condition-closure review with final status `PASS`
- committed EB-004 implementation at `5c926759591f617a8245526cdc27cdfd10dbb8e5`
- closed EB-004 Engineering Brief with no unresolved implementation findings
- DAR-approved CS-002.3 Governance Runtime Project Memory Health
- DAR-CS-0003 formal Design Authority Review with final result `PASS`

## What Does Not Exist

- release automation
- template migration tooling
- implemented review command
- implemented full Governance Runtime
- review report template
- automated review scoring
- plugin system
- project profiles beyond bootstrap
- review report persistence contract
- generated-project template provenance
- generated architecture discovery starter
- coverage threshold
- type checking
- release automation

## Architectural Posture

Forge should be documentation-led first, then contract-led, then implementation-led.

Implementation should only begin after the core platform concepts are explicit enough to test and review.

Milestone 0 adds an explicit architecture review gate before implementation work. Architecture review findings should be recorded under `docs/architecture/`, and durable governance decisions should be recorded as ADRs.

Forge 0.1 RC1 is accepted as the architecture foundation. Pre-implementation hardening defines contracts for project memory, ADRs, standards, templates, and the first CLI command without writing production code.

The final architecture milestone defines Forge as template-driven. `forge init <project-name>` must render versioned templates from `templates/bootstrap/` and must not hardcode generated file contents.

Forge now evolves permanent capabilities through Forge Capability Specifications under `docs/capabilities/`. FCS-001 defines how Forge performs project reviews before any review command is implemented.

Forge 0.2 introduces the first implementation layer. `forge init <project-name>` is intentionally narrow: it renders bootstrap templates, creates the default folder structure, supports dry-run, validates project names, and refuses to overwrite non-empty directories.

Forge 0.2.0 is prepared as a local-editable release. It should not be published to a package index yet.

DAR-0001 gives Forge `0.2.0` a decision of `PASS WITH COMMENTS`. The main baseline risks are roadmap drift, lack of CI, missing testing standard, minimal template metadata parsing, missing review persistence, and missing template provenance.

Gate 1 dogfooding verified that `python -m forge init ForgePlayground` runs successfully from outside the Forge repository and creates a usable project foundation. The decision is `PASS WITH COMMENTS`. The main findings were version traceability drift between tag `v0.2.1` and generated `0.2.0` content, possible confusion from generating a `forge/` folder in arbitrary projects, and a need for stronger first-session guidance in generated templates.

The non-blocking Gate 1 issues are being handled as a narrow patch. Generated projects should now report Forge `0.2.1`, and the generated README and AI handoff templates should better guide the first architecture discovery session. The generated `forge/` folder concern is documented as a Forge `0.3` design item and is intentionally not redesigned in this patch.

Forge 0.3 establishes the Developer Platform baseline. It adds documented testing, code quality, and CI standards plus a GitHub Actions workflow that runs pytest, Ruff lint checks, and Ruff format checks. This milestone intentionally does not add `forge review` or expand `forge init`.

The constitutional milestone establishes `CONSTITUTION.md` as the highest governing document in Forge. Forge now officially identifies as an AI-Native Software Engineering Platform. Future strategy, roadmap, capability specifications, engineering briefs, implementation, testing, Design Authority Review, and release decisions should derive from the Constitution.

The AI Engineering Conduct milestone defines how AI agents must behave inside Forge-governed projects. It requires agents to read before changing, understand before implementing, motivate before deciding, specify before coding, test before claiming completion, review before release, document before moving on, preserve architecture unless an ADR justifies change, follow the Constitution, and escalate uncertainty instead of inventing certainty.

FCS-002 defines Governance Runtime as the future operational layer that interprets the Constitution and continuously evaluates engineering health, governance compliance, project memory health, capability health, risk, and release readiness. It is specification-only and does not implement Python, CLI commands, scoring formulas, file mutation, or release automation.

AR-0001 concludes that Forge should introduce Capability Slice as a new engineering layer between Capability Specification and Engineering Brief. This change is accepted in ADR 0014. Capability Slices decompose large accepted capabilities into implementation-sized increments without replacing FCS documents or Engineering Briefs.

`docs/standards/capability-slice-standard.md` defines Capability Slice purpose, scope, naming, required sections, lifecycle, ownership, traceability, size guidance, and anti-patterns. `templates/capability-slices/CS-template.md` is the canonical starting point for new slices.

`docs/capabilities/CS-002.1-Governance-Runtime-Status-Service.md` defines the first implementation-sized slice of Governance Runtime. It is limited to read-only status evaluation and is intended to support a future `forge status` command. It explicitly excludes automatic file mutation, release approval, review creation, complex code-quality scoring, and replacement of human judgment.

`docs/reviews/DAR-CS-0001-CS-002.1-Status-Service.md` reviews CS-002.1 and gives it a decision of `PASS WITH COMMENTS`. The slice is ready for Engineering Brief creation. The brief must define output shape, strict mode behavior or deferral, repository validity detection, internal module boundaries, and read-only verification tests.

`docs/engineering/EB-002.1-Implement-Status-Service.md` defines the implementation boundary for the first Governance Runtime service and future `forge status` command. The brief requires a read-only service, separates service logic from CLI wiring, defers strict mode, forbids runtime project memory mutation, and requires tests proving no files are written.

Forge now implements EB-002.1 through `forge/status.py` and the `forge status` CLI command. The command inspects the current repository by default, reports human-readable governance/project status, uses simple result states, performs no scoring, and does not write project files or project memory at runtime.

PRR-0001 records a post-release version consistency issue after `v0.4.0`: active documentation still referenced Forge `0.3.3` after the release tag was created. The root cause was a missing release-time version consistency gate. CI did not catch it because CI currently checks tests, lint, and formatting. `forge status` did not catch it because CS-002.1 only checks artifact presence and simple status, not semantic version agreement.

`docs/capabilities/CS-002.2-Governance-Runtime-Version-Consistency-Check.md` specifies a read-only Governance Runtime extension to `forge status`. It defines version consistency as a status category or item group that compares Git tags, active documentation, project memory, package metadata when present, release documentation, and repository metadata without modifying files.

`docs/reviews/DAR-CS-0002-CS-002.2-Version-Consistency.md` reviews CS-002.2 and gives it a decision of `PASS WITH COMMENTS`. The slice is ready for EB-002.2. The Engineering Brief must define exact parsing and matching rules, active versus historical reference policy, status output placement, fixtures, and read-only tests.

`docs/engineering/EB-002.2-Implement-Version-Consistency-Check.md` defines the implementation boundary for adding Version Consistency Status to `forge status`. It requires read-only behavior, conservative parsing, local Git-only inspection, no new CLI command, no automatic fixes, no report persistence, no release approval, and no runtime project memory mutation.

Forge now implements EB-002.2 as an additional read-only `forge status` category. Version Consistency Status compares the latest local release tag with active release-facing references in `README.md`, `CHANGELOG.md`, `PROJECT_STATE.md`, `AI_HANDOFF.md`, and `pyproject.toml` when present. The implementation intentionally avoids broad historical scans, automatic fixes, release approval, report persistence, network calls, and project memory mutation.

`docs/standards/ai-implementation-protocol.md` defines the mandatory implementation workflow for AI agents implementing Engineering Briefs. ADR 0015 accepts it as the default implementation protocol for future Engineering Briefs. The protocol standardizes read-first behavior, scope discipline, verification, documentation updates, reporting, review handoff, and commit preparation.

`docs/reviews/DAR-EB-0002-EB-002.2-Version-Consistency-Implementation.md` reviews the EB-002.2 implementation and gives it a `PASS` decision. The review confirms that Version Consistency Status matches CS-002.2 and EB-002.2, remains read-only, introduces no new command, performs no runtime file modification, avoids scoring and persistence, and reports a clean state on the committed `v0.4.1` repository.

CS-002.2 is now closed after passing implementation review.

`docs/standards/lifecycle-standard.md` defines common, artifact-specific, and release lifecycle states; governs withdrawal, archival, and reopening; and requires explicit authority and auditable evidence for every transition. ADR 0016 accepts it as the governing lifecycle standard for Forge artifacts.

The focused re-review of the Lifecycle Standard corrections returned `PASS`. All required review conditions are closed, and the Lifecycle Standard work is closed.

`docs/architecture/AR-0002-Generated-Project-Source-Layout.md` evaluates the generated `forge/`, universal `src/`, Python-style `src/<project_name>/`, profile-dependent, and minimal-bootstrap options. `docs/reviews/DAR-AR-0002-Generated-Project-Source-Layout.md` accepts the minimal universal bootstrap recommendation with a `PASS` decision. ADR 0017 records the binding decision.

The `forge init` and Bootstrap Template System contracts specify `forge-bootstrap/2.0.0`
universal output with exactly eight directories, eight files, and no source-code directory. The
Bootstrap Template System contract contains the authoritative manual compatibility guidance for
historical projects. Focused contract review returned `PASS`, and the revisions and guidance are
accepted.

`docs/engineering/EB-004-Implement-Universal-Bootstrap-Output-Contract.md` defines the bounded implementation scope, affected runtime and template surfaces, exact-output tests, compatibility boundaries, verification, release evidence, and rollback requirements. Focused review returned `PASS`; the brief is accepted as `Implementation Ready`. Implementation is authorized only within EB-004 and must follow the AI Implementation Protocol.

The EB-004 implementation now produces `forge-bootstrap/2.0.0`: exactly eight contracted
directories and eight generated files, no source-code directory, explicit output-contract identity
in generated guidance and CLI reporting, and language-neutral `.gitignore` defaults. Automated and
manual verification evidence is recorded in
`docs/release/EB-004-universal-bootstrap-output-contract-readiness.md`. DAR-EB-0003 originally
returned `PASS WITH CONDITIONS`. Release Authority selected pre-`1.0` minor release `v0.5.0` and
accepted `>=0.5,<0.6` as the template compatibility range. Runtime and package metadata target
`0.5.0`, and all eight templates validate coherently. Focused condition-closure review returned
`PASS`; both conditions are closed. Commit `5c926759591f617a8245526cdc27cdfd10dbb8e5`
contains the complete reviewed implementation and governance evidence. Review Authority closed
EB-004 after confirming the committed scope and no unresolved implementation findings. Release
`v0.5.0` remains `Planned`; no Release Candidate, tag, publication, approval, or release transition
has occurred.

Product Owner evaluated Shared Governance Runtime result model, JSON status output, persisted
reports, release readiness evaluation, Project Memory Health, and further Version Consistency work.
Project Memory Health is selected because it delivers the strongest next read-only governance value
without scoring or persistence. The existing status result model is sufficient; no shared-model
prerequisite slice is required. DAR-CS-0003 returned `PASS`, accepted one private
`forge/project_memory.py` parsing and resolution helper while retaining status ownership in
`forge/status.py`, and advanced CS-002.3 to `DAR Approved`. Bounded Engineering Brief creation is
authorized; implementation remains unauthorized.

## Next Recommended Work

1. Create and review one bounded Engineering Brief that preserves DAR-CS-0003's deterministic
   rules, private helper boundary, failure behavior, fixtures, and exclusions.
2. Do not implement Project Memory Health until the Engineering Brief is accepted and reaches
   `Implementation Ready`.
3. Keep `v0.5.0` in `Planned`; no release work is authorized by this slice proposal.
