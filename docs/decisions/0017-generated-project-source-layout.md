# ADR 0017 - Generated Project Source Layout

Status: Accepted

Date: 2026-07-10

## Context

Forge `v0.4.1` implements `forge init <project-name>` as a conservative, template-driven bootstrap command. The current bootstrap contract and implementation create an empty `forge/` directory in every generated project.

The name and location originated in Forge's own architecture. ADR 0002 selected Python for Forge's implementation and reserved `forge/` for Forge's Python package. The first generated-project contract copied that placeholder into arbitrary projects even though Forge does not generate production code and does not require generated projects to use Python.

Gate 1 dogfooding identified that the generated directory can conflate:

- Forge, the AI-Native Software Engineering Platform
- a project governed by Forge documents and practices
- the generated project's own source-code identity and layout

AR-0002 evaluated retaining `forge/`, generating universal `src/`, generating Python-style `src/<project_name>/`, introducing profile-dependent layouts, and generating a minimal governance foundation without a source directory.

DAR-AR-0002 returned `PASS`. It accepted the minimal governance bootstrap as the appropriate universal default and confirmed that the decision is bounded, language-neutral, and ready to be recorded in an ADR. The Design Authority Review did not authorize contract, template, test, CLI, runtime, or generated-output changes.

## Decision

Forge adopts the following generated project source-layout policy:

1. The universal Forge bootstrap MUST generate no source-code directory.
2. Forge MUST retain `forge/` as the Python package for Forge's own implementation repository.
3. A generated project MUST select its source layout during architecture discovery unless a future explicitly selected and accepted project profile governs that choice.
4. The universal bootstrap MUST remain language-neutral.
5. `src/` MUST NOT be imposed as a universal default.
6. `src/<package_name>/` is reserved as a possible layout for a future governed Python project profile; it is not approved by this ADR for current generation.
7. Profile-dependent layouts are separate future capability work and MUST NOT be introduced as part of this bounded source-layout change.
8. Existing generated projects MUST NOT be automatically migrated.
9. Manual compatibility guidance is sufficient for existing generated projects.
10. Populated generated directories are project-owned and MUST NOT be removed, renamed, or moved automatically.
11. Empty generated placeholders MAY be removed manually by project maintainers after a project-owned decision, or by future automation only when explicitly accepted governance authorizes that behavior.
12. A future implementation of this decision MUST include:
    - explicit generated README guidance that no source layout has been selected
    - explicit generated AI handoff guidance directing source-layout selection through architecture discovery
    - accurate dry-run output and folder counts
    - release notes describing the generated-structure change
    - truthful template and output-contract compatibility metadata
    - no migration tooling

The accepted decision changes the future universal bootstrap contract. It does not change current generated output until the required follow-on governance and implementation gates are completed.

## Decision Authority

The Forge Design Authority approved the direction through `docs/reviews/DAR-AR-0002-Generated-Project-Source-Layout.md` with a `PASS` decision.

The Chief Architect owns this durable architecture and bootstrap-contract decision. Product Owner authority is not used to select a language or profile through this ADR. Future release timing remains under Product Owner release-goal authority and Release Authority approval.

This ADR authorizes the Chief Architect to prepare the affected bootstrap contract revisions and manual compatibility guidance for review and acceptance. The Implementation Agent is not authorized by this ADR to change contracts, templates, tests, Python, CLI behavior, runtime behavior, or generated output.

## Alternatives Considered

### Retain `forge/`

Rejected as the universal default. It preserves compatibility but incorrectly couples arbitrary project source code to Forge's own package identity and Python implementation.

### Generate `src/`

Rejected as the universal default. It removes Forge-specific naming but still imposes a source-tree convention before project type, language, repository boundaries, and deployment architecture are known.

### Generate `src/<project_name>/`

Rejected as the universal default. It assumes a package-oriented, Python-style structure and incorrectly treats a display or directory name as a valid package name. A future Python profile may define `src/<package_name>/` with a separately governed normalized variable.

### Generate Profile-Dependent Layouts

Deferred. Profiles could eventually provide intentional layouts, but Forge does not yet define profile identities, selection semantics, variables, validation, manifests, compatibility, or migration policy. Introducing profiles here would expand the change beyond its accepted boundary.

### Generate No Source-Code Directory

Accepted. This preserves the documentation-first and architecture-first universal foundation while leaving source layout to project-owned discovery or future explicitly selected profiles.

## Consequences

Positive consequences:

- Forge-governed projects are no longer conceptually presented as Forge packages.
- The universal bootstrap remains applicable to Python, non-Python, application, library, infrastructure, documentation-led, and pre-implementation projects.
- Source layout becomes an explicit project architecture decision.
- Future profiles retain a clean extension path without being introduced prematurely.
- The bootstrap remains aligned with Forge's identity as a platform rather than an application framework.

Negative or constraining consequences:

- New users may expect a source directory and require explicit explanation that its absence is intentional.
- The generated folder plan and folder counts will change when implemented.
- Scripts or expectations tied to the current empty `forge/` placeholder may require adjustment.
- Bootstrap contracts, generated guidance, tests, compatibility metadata, changelog, and release notes must be updated coherently.
- Projects may choose different layouts until optional profiles are governed.

The decision does not weaken `forge init`'s core purpose: establishing a governed foundation that is ready for architecture discovery before production code begins.

## Compatibility and Migration Policy

This decision applies prospectively to new projects generated after its implementation is reviewed and released.

Existing generated projects remain valid Forge-governed projects and require no migration. Their files and directories are project-owned after generation.

Required manual guidance:

- an empty `forge/` placeholder may remain, or a maintainer may remove or replace it after recording the project's architecture decision
- a populated `forge/` directory MUST be treated as project-owned code and left unchanged
- a project that intentionally uses `forge/` as its own package may continue to do so
- an existing project does not need to match the latest bootstrap structure to remain Forge-governed

Forge MUST NOT automatically delete, rename, move, or rewrite an existing generated directory. Forge currently lacks template and output-plan provenance sufficient to distinguish an untouched placeholder from project-owned content. No migration tool is justified for this bounded change.

The future release must identify the affected default behavior, compatibility expectations, known limitations, and absence of automatic migration. Pre-`1.0` compatibility permits the generated-structure change only when it is explicit, reviewed, documented, and released through normal governance.

## Implementation Boundaries

This ADR records architecture only. During ADR creation:

- Python MUST NOT be modified.
- CLI behavior MUST NOT be modified.
- Bootstrap templates MUST NOT be modified.
- Tests MUST NOT be modified.
- Generated output MUST NOT be modified.
- Bootstrap contracts MUST NOT be revised.
- An Engineering Brief MUST NOT be created.
- Project profiles MUST NOT be created.
- Migration tooling MUST NOT be created.

Implementation readiness remains `NOT READY` until all of the following are complete:

1. affected bootstrap contracts are revised and accepted
2. manual compatibility guidance is defined
3. the bounded implementation scope is captured in an accepted Engineering Brief

The future implementation must preserve conservative overwrite protection, template-driven generated file bodies, transparent dry-run planning, and the prohibition on production-code generation.

## Follow-on Governance

The required sequence is:

1. Revise and obtain acceptance of `docs/contracts/forge-init-spec.md` to define the new universal folder plan and user-visible guidance obligations.
2. Revise and obtain acceptance of `docs/contracts/bootstrap-template-system.md` and related compatibility guidance where the generated-structure contract is affected.
3. Define concise manual compatibility guidance for existing generated projects.
4. After the affected contracts are accepted and manual compatibility guidance is defined, create a bounded Engineering Brief covering the folder plan, generated README and AI handoff guidance, CLI reporting, tests, documentation, compatibility metadata, and release evidence.
5. Implement only the accepted Engineering Brief.
6. Perform implementation review before release or closure.
7. Release the changed default with explicit notes and compatibility evidence.

A new Capability Slice is not required. This is a bounded change to an existing bootstrap output rule and does not add a capability. Any work on selectable project profiles, profile manifests, language-specific generation, or migration automation requires separate capability governance.

## Deferred Questions

The following questions do not block this decision:

- Which future capability owns project-profile definitions and selection?
- What normalized `package_name` contract should a future Python profile use?
- Which pre-`1.0` release should carry the implemented layout change?
- When should generated projects record template and output-plan provenance?
- Should governance-only initialization eventually receive an explicit profile name?

Profile ownership, Python package naming, and an explicit governance-only profile name are intentionally deferred until profile capability work begins. Release timing and provenance are non-blocking follow-up governance.

## Superseded or Affected Documents

This ADR does not supersede another ADR.

ADR 0002 remains authoritative for Forge's own Python implementation and `forge/` package. ADR 0008 remains authoritative for specification-before-implementation. ADR 0009 remains authoritative for template-driven generated file content.

The following accepted documents are affected and require later revision before implementation:

- `docs/contracts/forge-init-spec.md`
- `docs/contracts/bootstrap-template-system.md`
- template compatibility guidance under `templates/governance.md`

The following implementation and release artifacts will be affected later but MUST NOT change during this ADR task:

- generated README and AI handoff templates
- bootstrap output planning and CLI reporting
- bootstrap tests
- generated-project compatibility guidance
- changelog and release notes for the implementing release

Until the contracts are revised and implementation passes review, current `forge init` behavior remains the implemented behavior.

## Evidence and References

- `docs/architecture/AR-0002-Generated-Project-Source-Layout.md`
- `docs/reviews/DAR-AR-0002-Generated-Project-Source-Layout.md`
- `docs/reviews/GATE-0001-Dogfooding-ForgePlayground.md`
- `docs/contracts/bootstrap-template-system.md`
- `docs/contracts/forge-init-spec.md`
- `CONSTITUTION.md`
- `AI_ENGINEERING_CONDUCT.md`
- `docs/standards/lifecycle-standard.md`
- `docs/decisions/0002-python-as-implementation-language.md`
- `docs/decisions/0007-standard-and-template-governance.md`
- `docs/decisions/0008-specify-forge-init-before-implementation.md`
- `docs/decisions/0009-template-driven-bootstrap-generation.md`
- `docs/decisions/0014-introduce-capability-slices.md`
