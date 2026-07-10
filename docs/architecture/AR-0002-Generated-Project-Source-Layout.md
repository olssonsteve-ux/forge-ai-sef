# AR-0002 - Generated Project Source Layout

Status: Approved - Design Authority Review `PASS`

Date: 2026-07-10

Owner: Forge Design Authority

Review type: Architecture Review

## 1. Context

Forge `v0.4.1` implements `forge init <project-name>` as a conservative, template-driven bootstrap command. The accepted output contract creates governance and project-memory files, documentation directories, `standards/`, `templates/`, `tests/`, and an empty `forge/` directory.

Gate 1 dogfooding found that `forge/` is understandable inside the Forge repository but potentially misleading inside an arbitrary generated project. A generated project may be a Python library, a non-Python application, an infrastructure repository, or a documentation-led project that has not selected an implementation architecture. In those contexts, `forge/` may appear to be a required Forge runtime package or a mandated home for project code.

The issue was explicitly deferred from the `0.2.x` patch and retained in project memory as an architecture decision. At review initiation, no source-layout change had been approved. Design Authority Review has now approved the recommendation for ADR creation; the current contract remains unchanged, and this review does not authorize implementation.

## 2. Problem Statement

Forge must decide whether its universal bootstrap contract should choose a source-code directory before the generated project has completed architecture discovery.

The decision must separate four concepts:

- the Forge platform's own implementation package
- governance files that make a project Forge-governed
- the generated project's source-code organization
- future language-specific or project-profile-specific layouts

The current `forge/` default conflates the first and third concepts. Replacing it universally with `src/` or `src/<project_name>/` could remove the product-name coupling while still imposing an implementation convention before the project has established its architecture.

## 3. Current-State Analysis

### 3.1 Original Purpose of `forge/`

The original Forge architecture reserved `forge/` for Forge's future Python implementation. ADR 0002 states that Python is Forge's expected implementation language and that future implementation should reserve `forge/` for Python package code. Architecture discovery likewise describes `forge/` and `tests/` as empty placeholders that reserve Forge's future implementation shape.

The first `forge init` specification copied that repository shape into generated projects. It requires an empty `forge/` placeholder but prohibits production-code generation. The runtime implements the requirement as a literal folder in its output plan; the bootstrap templates do not generate code into it and do not require a source-layout variable.

The directory therefore began as a reservation for Forge's own package and was generalized into a bootstrap placeholder. The governing documents do not establish that arbitrary generated projects need a package named `forge`.

### 3.2 Does the Original Purpose Remain Valid?

The purpose remains valid for the Forge repository itself: `forge/` is Forge's Python package. It does not remain valid as a universal generated-project convention.

A Forge-governed project is governed through explicit repository-local contracts, memory, standards, reviews, and workflows. It does not become Forge-governed by placing source code under a directory named `forge/`. Keeping that directory in every generated project creates product-specific coupling without providing a governance capability.

### 3.3 Conceptual Coupling

The current name can imply any of the following incorrect relationships:

- the generated project's code is part of the Forge platform
- Forge must be installed or imported by the generated project
- the generated project is required to be a Python package
- project code belongs in a package named `forge`

Those implications conflict with Forge's identity as an AI-Native Software Engineering Platform rather than an application framework or product-specific business-logic framework. Forge should govern how architecture is chosen; it should not silently choose the generated product's package identity.

### 3.4 Current Implementation and Contract Surface

The source-layout choice currently affects:

- `docs/contracts/forge-init-spec.md`, which declares the generated folder tree
- `forge/bootstrap.py`, which contains the literal folder output plan
- CLI dry-run and success counts
- `tests/test_init.py` and any structure assertions or snapshots
- Gate, release, README, project-memory, and handoff descriptions of generated output
- bootstrap guidance that tells users when to begin architecture discovery

The eight root-file templates do not currently depend on a source directory. No source-layout-specific template variable exists. Generated-project template provenance is not yet recorded.

## 4. Architectural Principles and Constraints

The decision is governed by these principles:

- **Architecture before implementation:** a bootstrap default must not harden an unreviewed product architecture.
- **Explicit behavior over hidden behavior:** generated structure must remain visible in the bootstrap contract and dry-run plan.
- **Capabilities before features:** a future profile system must be governed before profile-specific output is implemented.
- **Platform, not application framework:** Forge must not make every project resemble Forge or require one technology stack.
- **Documentation-led bootstrap:** the universal bootstrap should prepare architecture discovery before production code begins.
- **Language neutrality:** Forge's Python implementation language does not govern the implementation language of generated projects.
- **Conservative compatibility:** existing generated projects remain project-owned and must not be rewritten automatically.
- **Template-driven content:** generated file bodies must remain template-driven; source-layout planning must remain an explicit contract even where folders are created by the bootstrap engine.
- **No production-code generation:** this review must not introduce framework scaffolding, package modules, dependencies, or executable code.

The universal bootstrap structure, language-specific source layouts, project-profile-specific layouts, and governance-only initialization are separate concerns and must remain separately governed.

## 5. Options Considered

### Option 1 - Retain `forge/`

Continue generating an empty `forge/` directory in every project.

This preserves the current contract and has no migration cost, but it retains the conceptual coupling identified by Gate 1. It is appropriate for Forge itself, not for arbitrary projects.

### Option 2 - Generate `src/`

Replace `forge/` with an empty, neutral-looking `src/` directory.

`src/` avoids Forge product-name coupling and is familiar across several ecosystems. It is not architecture-neutral, however. Infrastructure repositories may organize by environments or modules; applications may use `app/`, `packages/`, or service directories; documentation-led projects may have no code; and monorepositories may need multiple roots. A universal `src/` would turn one premature convention into a less confusing but still premature convention.

### Option 3 - Generate `src/<project_name>/`

Generate a Python-style source layout beneath `src/`.

This can be a strong default for a Python package profile because it separates importable code from the repository root and supports packaging discipline. It is unsuitable as a universal default. It assumes a package-oriented architecture, and the project directory name may not be a valid Python import name. A Python profile would require a separately governed normalized package-name variable and packaging decisions.

### Option 4 - Generate Profile-Dependent Layouts

Select different structures for Python packages, applications, infrastructure repositories, documentation-led projects, and other profiles.

This is the most adaptable long-term direction, but Forge does not yet define project-profile identities, selection semantics, validation, compatibility, or profile-specific output contracts. Implementing profile-dependent layouts now would hide ungoverned branching inside `forge init`. Profiles must be specified and reviewed before this option can be supported.

### Option 5 - Minimal Governance Bootstrap

Generate the governance, memory, documentation, standards, template, and other accepted bootstrap foundation without creating a source-code directory.

The generated project would choose its source layout during architecture discovery. A later accepted project profile or project-owned architecture decision could introduce `src/`, `src/<package_name>/`, `app/`, `services/`, `modules/`, or no source tree at all.

This option removes the false coupling and best matches the existing rule that production architecture follows documented intent. It does not prevent Forge from offering profile-specific layouts later.

## 6. Evaluation Criteria

The options are evaluated against:

- conceptual clarity
- language neutrality
- ease of onboarding
- compatibility with the current contract and generated projects
- implementation complexity
- migration cost
- ability to support future project profiles
- template and output-plan maintainability
- governance consistency
- risk of premature architectural commitment

## 7. Comparative Assessment

Ratings are relative: `Strong`, `Mixed`, or `Weak`.

| Criterion | Retain `forge/` | Generate `src/` | Generate `src/<project_name>/` | Profile-dependent | Minimal governance bootstrap |
| --- | --- | --- | --- | --- | --- |
| Conceptual clarity | Weak - conflates Forge with project code | Strong - purpose is familiar | Mixed - clear for packages, misleading elsewhere | Strong after profiles exist | Strong - source architecture is explicitly undecided |
| Language neutrality | Weak | Mixed | Weak | Strong | Strong |
| Ease of onboarding | Mixed - directory exists but name misleads | Strong for conventional code projects | Strong for Python packages only | Strong after selection UX exists | Mixed - requires clear next-step guidance |
| Current compatibility | Strong | Mixed - changes output contract | Weak - changes structure and naming | Weak - changes command contract substantially | Mixed - removes one empty placeholder |
| Implementation complexity | Strong | Strong | Mixed | Weak | Strong |
| Migration cost | Strong | Mixed | Weak | Weak | Strong - no existing-project migration required |
| Future project profiles | Weak | Mixed | Mixed | Strong | Strong - preserves an uncommitted base |
| Template maintainability | Mixed - simple but misleading | Strong | Mixed - needs naming variables | Weak until profile contracts and manifests exist | Strong - no source-layout variables |
| Governance consistency | Weak | Mixed | Weak as a universal default | Weak now; strong after profile governance | Strong |
| Risk of premature commitment | Weak | Mixed | Weak | Mixed - explicit choice, but profiles are undefined | Strong |

### 7.1 Suitability by Project Type

| Project type | `forge/` | `src/` | `src/<project_name>/` | Profile-dependent | Minimal bootstrap |
| --- | --- | --- | --- | --- | --- |
| Python library | Misnamed | Acceptable | Strong with normalized package name | Strong after profile definition | Strong before architecture; profile may add layout later |
| Non-Python project | Misleading | Ecosystem-dependent | Unsuitable | Strong after profile definition | Strong |
| Application | Misleading | Sometimes suitable | Usually too package-specific | Strong after profile definition | Strong |
| Infrastructure repository | Misleading | Often unsuitable | Unsuitable | Strong after profile definition | Strong |
| Documentation-led project | Unnecessary | Unnecessary | Unsuitable | Strong if a documentation profile exists | Strong |
| Pre-implementation project | Premature | Premature | Premature | Premature until a profile is intentionally selected | Strong |

## 8. Compatibility and Migration Implications

### 8.1 New Projects

If accepted and implemented, new default bootstrap runs should omit `forge/` and make the absence of a source directory explicit in generated README and AI handoff guidance. The project should be told to select source layout during architecture discovery, not left to infer that generation failed.

Removing `forge/` changes the generated structure and therefore changes the bootstrap output contract. Under the Bootstrap Template System's versioning rules, changed generated structure is a major template-system change even if no file template body is removed. Before Forge `1.0`, the break is permitted only with a changelog entry, an ADR, compatibility documentation, and migration guidance.

The release that ships the behavior should identify it as an intentional generated-structure change. Because Forge is pre-`1.0`, the Release Authority should select the release version under the accepted release policy; this review does not assign a version.

### 8.2 Existing Generated Projects

Existing generated projects require no mandatory migration. Their contents are project-owned after generation.

Documentation-led optional guidance is sufficient:

- if `forge/` is empty, maintainers may remove it or replace it after accepting their project architecture
- if `forge/` contains project code, Forge must not rename or move it automatically
- if the directory intentionally represents a project package, it may remain
- generated projects do not need to match the latest bootstrap tree to remain Forge-governed

No automated migration should be attempted because Forge does not record template provenance and cannot reliably distinguish an untouched placeholder from a project-owned directory.

### 8.3 Template Provenance

The absence of generated-project provenance limits automated compatibility analysis, but it does not block changing the default for new projects. The release notes and manual guidance must identify the affected Forge versions and structure. Template provenance remains separate future governance work.

## 9. Impact Assessment

No impact in this section is authorized for implementation by this review.

### `forge init <project-name>`

The accepted folder plan would remove the literal `forge/` entry. Dry-run output and created-folder counts would change. Conservative target validation and overwrite protection would remain unchanged.

### Bootstrap Templates

The existing root-file templates do not create `forge/`. Their generated README and AI handoff guidance should eventually explain that source layout is intentionally deferred. Template metadata versions and compatibility ranges must be reviewed because the generated project contract changes.

### Template Variables

The recommended minimal bootstrap requires no new variable. A future Python profile would need a governed package or module name distinct from the display-oriented `PROJECT_NAME`.

### Generated README and AI Handoff

Future template revisions should state that no production source directory has been selected and direct maintainers to record the choice through architecture discovery. They must not imply that all projects should choose `src/`.

### Tests

Future implementation tests must verify the exact new folder plan, the absence of a generated `forge/` source placeholder, updated folder counts, dry-run accuracy, no production-code generation, and unchanged overwrite protection. Tests for profile selection are out of scope.

### Documentation

The `forge init` specification, bootstrap template contract, generated-structure descriptions, project memory, handoff guidance, changelog, and release notes would require coordinated updates.

### Existing Generated Projects

No files or directories should be modified. Optional manual guidance is the complete compatibility action.

### Migration and Compatibility

A concise manual migration note is required; a migration specification or tool is not. The note must distinguish empty placeholders from project-owned code.

### Release and Versioning

The release record must identify the output-contract change, affected default behavior, known limitations, compatibility expectations, and absence of automatic migration. Template compatibility metadata must remain truthful.

## 10. Risks and Trade-offs

### Minimal Bootstrap Can Appear Incomplete

New users may expect a code directory. Mitigation: generated README, AI handoff, and CLI success guidance must state that source layout is intentionally selected during architecture discovery.

### Users May Choose Inconsistent Layouts

Deferring the choice allows legitimate variation but reduces uniformity. Mitigation: future reviewed profiles may offer explicit, opt-in defaults without changing the universal base.

### Output-Contract Change

Even removal of an empty folder can break scripts or expectations. Mitigation: ADR, contract revision, release note, dry-run accuracy, and manual compatibility guidance.

### Profile Work May Be Pulled Forward Prematurely

The desire for a Python-friendly default may encourage an unreviewed profile switch. Mitigation: prohibit profile-dependent output until profile identity, selection, variables, compatibility, and validation are specified.

### Existing `forge/` Directories Are Ambiguous

Without provenance, Forge cannot know whether the directory is untouched or project-owned. Mitigation: no automated migration or deletion.

## 11. Recommended Direction

Adopt **Option 5 - Minimal Governance Bootstrap** as the universal default.

The default `forge init <project-name>` output should not create a source-code directory. Specifically, future implementation should remove the empty generated `forge/` placeholder and should not replace it universally with `src/`.

The recommendation establishes these boundaries:

- Forge itself retains `forge/` as its Python package.
- A generated project becomes Forge-governed through governance and memory artifacts, not through a Forge-named code directory.
- A generated project selects its source layout during architecture discovery.
- `src/<package_name>/` may be considered later for an explicitly selected Python profile.
- Profile-dependent layouts must wait until project profiles have accepted contracts.
- Governance-only initialization remains the universal base and must remain useful without Forge installed.

Design Authority Review accepted this recommendation with a `PASS` decision in `docs/reviews/DAR-AR-0002-Generated-Project-Source-Layout.md`. ADR 0017 records the binding decision. Neither the review nor the ADR authorizes changes to contracts, runtime behavior, templates, or tests.

## 12. Required Follow-on Governance

Following the Design Authority Review `PASS` decision:

1. ADR 0017 records the durable generated-layout decision and compatibility policy. This gate is complete.
2. Revise `docs/contracts/forge-init-spec.md` before implementation.
3. Revise `docs/contracts/bootstrap-template-system.md` and template compatibility guidance where the structure contract is affected.
4. Add manual migration guidance for existing generated projects; do not create migration tooling.
5. Create an Engineering Brief covering the bounded implementation, template guidance, tests, documentation, and release evidence.
6. Perform implementation review before closing the work or releasing the changed default.

A new Capability Slice is not required for this recommendation. It changes one bounded output rule of the existing bootstrap behavior and does not introduce a new capability. If follow-on work expands into selectable project profiles, profile manifests, or multiple generated layouts, that work must begin as separately governed capability work and may require a Capability Specification and Capability Slice before an Engineering Brief.

## 13. Explicit Exclusions

This review does not:

- change Python, CLI, runtime, tests, or templates
- change the current `forge init` contract
- remove or rename any directory in an existing generated project
- implement `src/` or `src/<project_name>/`
- define project profiles or profile selection
- define Python package normalization
- generate production code
- introduce migration tooling
- redesign overwrite protection, template rendering, or unrelated `forge init` behavior
- decide whether other non-source placeholders should change
- assign a Forge release version

## 14. Decision Readiness

Decision readiness: **DECISION RECORDED - IMPLEMENTATION NOT READY**.

The evidence is sufficient to choose the universal default independently of future profile details. The future profile taxonomy, Python package naming, and provenance mechanism do not block the decision to stop imposing `forge/` universally.

The Design Authority accepted the recommendation, and ADR 0017 records the decision. Contract revision and manual compatibility guidance are the next governance gates. Template changes, test changes, and implementation changes MUST NOT begin until the affected contracts are revised and a bounded Engineering Brief is accepted.

## 15. Open Questions

The following questions do not block Design Authority Review:

- Which future capability should own project-profile definitions and profile selection?
- What normalized variable should a future Python profile use for package names?
- In which pre-`1.0` release should an accepted output-contract change ship?
- When should generated projects begin recording template and output-plan provenance?
- Should a future governance-only profile be named explicitly, or remain the unqualified universal default?
