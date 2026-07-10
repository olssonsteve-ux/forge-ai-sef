# EB-004 - Implement Universal Bootstrap Output Contract 2.0.0

Status: Closed

Date: 2026-07-10

Owner: Chief Architect

Review result: `PASS`

Implementation status: `Implementation Reviewed`

Implementation review result: `PASS`

Implementation commit: `5c926759591f617a8245526cdc27cdfd10dbb8e5`

Closure date: 2026-07-10

Closure authority: Review Authority, with Chief Architect concurrence for the architecture-governed
scope.

Review Authority accepted this brief, and the Chief Architect originally recorded it as
`Implementation Ready` under the Forge Lifecycle Standard. The authorized implementation was
completed, formally reviewed with final result `PASS`, committed, and then closed. This closure does
not authorize a release transition.

## Lifecycle History

- `Proposed` -> `Implementation Ready` on 2026-07-10 after focused Engineering Brief review `PASS`
  and Chief Architect acceptance.
- `Implementation Ready` -> `Implemented` on 2026-07-10 after the authorized changes and required
  verification were completed under the AI Implementation Protocol.
- `Implemented` -> `Implementation Reviewed` on 2026-07-10 through DAR-EB-0003 final result `PASS`
  with both original conditions closed.
- Implementation commit recorded on 2026-07-10 as
  `5c926759591f617a8245526cdc27cdfd10dbb8e5`.
- `Implementation Reviewed` -> `Closed` on 2026-07-10 after Review Authority confirmed accepted
  review evidence, committed scope, no unresolved implementation findings, and separately tracked
  release follow-up.

Release `v0.5.0` remains `Planned`. EB-004 closure does not create a Release Candidate, tag,
publication, release approval, or `Released` transition.

## 1. Purpose

Implement the accepted Generated Project Source Layout decision as the bounded `forge-bootstrap/2.0.0` universal bootstrap output.

The implementation will remove the historical generated `forge/` source placeholder without replacing it with `src/` or another source-code structure. It will preserve Forge's own internal `forge/` Python package, keep generated projects language-neutral, and direct source-layout selection to architecture discovery.

This Engineering Brief translates accepted architecture and contracts into a reviewable implementation boundary. It does not reconsider the decision or authorize implementation while its status is `Proposed`.

## 2. Governing Decisions and Contracts

Implementation MUST follow:

- `CONSTITUTION.md`
- `AI_ENGINEERING_CONDUCT.md`
- `docs/architecture/AR-0002-Generated-Project-Source-Layout.md`
- `docs/reviews/DAR-AR-0002-Generated-Project-Source-Layout.md`
- `docs/decisions/0017-generated-project-source-layout.md`
- `docs/contracts/forge-init-spec.md`
- `docs/contracts/bootstrap-template-system.md`
- `templates/governance.md`
- `docs/standards/ai-implementation-protocol.md`
- `docs/standards/testing-standard.md`
- `docs/standards/code-quality-standard.md`
- `docs/standards/lifecycle-standard.md`
- `docs/release/release-standard.md`

Authority order for this work is:

```text
ADR 0017
  -> accepted bootstrap contracts
  -> this Engineering Brief
  -> implementation
  -> implementation review
  -> release
```

If this brief conflicts with an accepted decision or contract, the accepted decision or contract wins and the brief MUST return to review.

## 3. Current Behavior

Current `forge init <project-name>` behavior is implemented in `forge/bootstrap.py` and exposed through `forge/cli.py`.

The current universal directory plan contains nine directories because `FOLDER_PATHS` includes an empty generated `forge/` placeholder. It generates eight files from the versioned assets under `templates/bootstrap/`.

Current behavior also:

- passes `FORGE_VERSION` and other existing variables to template rendering
- does not define or render `BOOTSTRAP_OUTPUT_CONTRACT`
- reports nine created folders and eight created files
- prints folder and file paths during dry-run
- omits a distinct bootstrap output-contract identity from CLI reporting
- generates README and AI handoff guidance that begins architecture discovery but does not explicitly explain the absence or deferral of source layout
- generates a `.gitignore` containing Python- and pytest-specific defaults
- validates template metadata, declared variables, required values, and compatibility ranges
- rejects non-empty target directories
- performs no writes during dry-run

The current behavior remains valid until implementation begins under the AI Implementation Protocol and the bounded change passes its required verification and review.

## 4. Target Behavior

The target behavior is the accepted `forge-bootstrap/2.0.0` contract:

- exactly eight generated directories
- exactly eight generated files
- no generated source-code directory
- no `forge/`, `src/`, `src/<package_name>/`, package, application, framework, or profile structure
- explicit `BOOTSTRAP_OUTPUT_CONTRACT=forge-bootstrap/2.0.0` rendering context
- explicit output-contract identity in generated README, generated AI handoff, dry-run, success reporting, verification, and release evidence
- source-layout selection deferred to project architecture discovery
- no changes to existing generated projects
- no migration detection, automation, or tooling

### Exact Contracted Directories

The implementation MUST copy this list exactly from `docs/contracts/forge-init-spec.md`:

```text
docs/
docs/architecture/
docs/contracts/
docs/decisions/
docs/vision/
standards/
templates/
tests/
```

Directory count: `8`.

The target project root is not included in the directory count.

### Exact Contracted Generated Files

The implementation MUST copy this list exactly from `docs/contracts/forge-init-spec.md`:

```text
README.md
ROADMAP.md
CHANGELOG.md
PROJECT_STATE.md
PROJECT_BRAIN.md
AI_HANDOFF.md
LICENSE
.gitignore
```

Generated file count: `8`.

No additional directory or file may be added without a separately accepted contract revision.

## 5. Exact Implementation Scope

### 5.1 Universal Output Plan

In `forge/bootstrap.py`:

- remove only the generated `forge` entry from `FOLDER_PATHS`
- preserve the exact eight contracted directory entries and their deterministic ordering
- preserve the existing eight `TEMPLATE_OUTPUTS` mappings
- do not rename, remove, or add a generated file
- do not change Forge's repository-local `forge/` package or packaging configuration

The implementation MUST NOT inspect or modify an existing generated project. The change applies only when planning and creating a new empty target.

### 5.2 Bootstrap Output-Contract Identity

The single runtime source of the accepted identity MUST be a module-level constant in `forge/bootstrap.py`:

```text
BOOTSTRAP_OUTPUT_CONTRACT = "forge-bootstrap/2.0.0"
```

The value MUST remain separate from `forge.__version__` and package metadata.

Implementation MUST:

- add `BOOTSTRAP_OUTPUT_CONTRACT` to `SUPPORTED_VARIABLES`
- add the constant value to `default_variables()` under the same key
- add an `output_contract` field to `InitResult`
- populate `InitResult.output_contract` from the module-level constant for both dry-run and write execution
- make CLI reporting use `InitResult.output_contract` rather than duplicate the literal
- pass the value through ordinary declared template-variable validation and rendering

The implementation MUST NOT derive the output-contract identity from the Forge product version, Git tags, template versions, project name, or release metadata.

The implementation MUST use the exact identifier `forge-bootstrap/2.0.0`, MUST NOT add a leading `v`, and MUST NOT represent the identity as a Git release tag.

### 5.3 No Migration Behavior

The existing target validation boundary MUST remain unchanged:

- absent target MAY be created
- empty target MAY be initialized
- non-empty target MUST fail by default

No new code may inspect a historical project's `forge/` directory, decide whether it is empty, offer migration, remove it, rename it, or rewrite it.

## 6. Explicit Exclusions

This brief does not authorize:

- reconsidering AR-0002, DAR-AR-0002, or ADR 0017
- changing `forge-bootstrap/2.0.0`
- creating a Capability Slice
- adding `src/`, `src/<package_name>/`, `app/`, or another source directory
- creating project profiles or profile-selection behavior
- adding Python package-name normalization
- adding migration detection, migration guidance automation, or migration tooling
- adding template migration support
- adding a provenance manifest or richer provenance beyond `BOOTSTRAP_OUTPUT_CONTRACT`
- modifying an existing generated project
- changing project-name validation
- changing overwrite policy
- changing filesystem safety behavior
- adding CLI commands, flags, or options
- installing dependencies or selecting a framework
- changing unrelated `forge status` behavior
- changing Forge's internal `forge/` package
- changing Forge product-version policy
- assigning the exact pre-`1.0` release number
- implementation outside this accepted `Implementation Ready` brief or without following the AI Implementation Protocol

## 7. Affected Modules and Files

Expected implementation files:

- `forge/bootstrap.py`
  - exact directory plan
  - output-contract constant
  - supported rendering variable
  - template context
  - `InitResult.output_contract`
- `forge/cli.py`
  - dry-run reporting
  - success reporting
- `tests/test_init.py`
  - exact output, reporting, identity, validation, and compatibility-boundary tests

Expected versioned bootstrap template assets:

- `templates/bootstrap/README.template.md`
- `templates/bootstrap/AI_HANDOFF.template.md`
- `templates/bootstrap/gitignore.template`

Template assets assessed and not expected to change unless brief review identifies a direct contract conflict:

- `templates/bootstrap/PROJECT_STATE.template.md`
- `templates/bootstrap/PROJECT_BRAIN.template.md`
- `templates/bootstrap/CHANGELOG.template.md`
- `templates/bootstrap/ROADMAP.template.md`
- `templates/bootstrap/LICENSE.template`

Those five templates do not currently claim that a source directory exists and do not need the output-contract identity under the accepted contract.

Expected Forge documentation and release evidence:

- `README.md`
- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md`
- `AI_HANDOFF.md`
- `CHANGELOG.md`
- an appropriate release note or release-readiness artifact under `docs/release/`
- a later implementation-review artifact under `docs/reviews/`, created by Review Authority

No other file is in scope unless implementation reveals a direct accepted-contract dependency. Any additional file MUST be justified in the implementation report and reviewed for scope expansion before modification.

## 8. Template Changes

### 8.1 Generated README

`templates/bootstrap/README.template.md` MUST:

- declare `BOOTSTRAP_OUTPUT_CONTRACT` in `variables` and `required_variables`
- render `{{BOOTSTRAP_OUTPUT_CONTRACT}}`
- state that no source-code directory was generated intentionally
- state that universal bootstrap does not select language, package, framework, or source layout
- direct maintainers to decide source layout through architecture discovery
- retain project identity, Forge version, creation date, ownership, and first-session guidance

Adding a required variable is a major template change under template governance. Its template version MUST move from `0.1.1` to `1.0.0`.

### 8.2 Generated AI Handoff

`templates/bootstrap/AI_HANDOFF.template.md` MUST:

- declare `BOOTSTRAP_OUTPUT_CONTRACT` in `variables` and `required_variables`
- render `{{BOOTSTRAP_OUTPUT_CONTRACT}}`
- state that no source layout has been accepted
- direct the first agent to establish purpose, boundaries, language, packaging or deployment constraints, and source layout through architecture discovery
- prohibit the agent from inventing or creating source structure before a project decision exists
- retain the existing read-first and project-memory instructions

Adding a required variable is a major template change. Its template version MUST move from `0.1.1` to `1.0.0`.

### 8.3 Generated `.gitignore`

`templates/bootstrap/gitignore.template` currently includes Python- and pytest-specific entries:

```text
__pycache__/
.pytest_cache/
.venv/
```

Those entries imply a language and test framework in the universal bootstrap. The implementation MUST remove those three entries and MUST NOT replace them with defaults for another language, framework, package manager, or profile.

The following existing common entries MUST remain unchanged:

```text
.DS_Store
Thumbs.db
.env
.env.*
dist/
build/
```

No other `.gitignore` entry may be added, removed, or reordered under this brief. Because the generated meaning changes, the template version MUST move from `0.1.0` to `1.0.0`.

### 8.4 Template Compatibility Ranges

The exact implementing Forge release number is deferred to Release Authority. Before implementation completion:

- each changed template's `compatible_forge_versions` MUST include the runtime version used for the implementing release
- compatibility ranges MUST remain truthful and MUST NOT conflate Forge versions with `forge-bootstrap/2.0.0`
- Release Authority MUST record the chosen pre-`1.0` release classification and target version

If existing Forge runtime and package version sources prevent a truthful compatibility range, implementation MUST stop and escalate that separate version-consistency issue rather than silently broadening this brief.

## 9. CLI and Dry-Run Behavior

No new command, flag, or option is authorized.

### Dry Run

`forge init <project-name> --dry-run` MUST:

- remain read-only
- validate the same templates, variables, target, and output plan as actual generation
- report `Bootstrap output contract: forge-bootstrap/2.0.0`
- report `Source layout: not selected`
- report exactly `Folders to create: 8`
- list the exact eight contracted directory paths in deterministic order
- report exactly `Files to create: 8`
- list the exact eight contracted file paths in deterministic order
- omit `forge/`, `src/`, and every other source-code directory

For equivalence checks, paths MUST be normalized relative to the target project root. The target project root itself and any pre-existing temporary parent directory are incidental and MUST NOT be counted.

The required equivalence rule is:

```text
dry_run_directories == actual_directories == contracted_directories
dry_run_files == actual_files == contracted_files
```

Equality is bidirectional: every path shown by dry-run MUST be created by actual generation, and every path created by actual generation MUST have appeared in dry-run. Ordering MUST also match the deterministic contract order used for reporting.

### Successful Generation

Successful generation MUST report:

```text
Forge project initialized: <project-name>
Created folders: 8
Created files: 8
Bootstrap output contract: forge-bootstrap/2.0.0
Source layout: not selected
Next step: review PROJECT_STATE.md and select source layout through architecture discovery.
```

Counts MUST be derived from the actual `InitResult` collections. The identity MUST be read from `InitResult.output_contract`.

Existing error behavior, project-name validation, template validation, overwrite protection, and dry-run no-write behavior MUST remain unchanged.

## 10. Compatibility Behavior

Implementation compatibility work is prospective and documentation-only for existing projects.

The implementation MUST:

- generate only into a new or empty target under existing validation rules
- make no changes to existing generated projects
- perform no migration or legacy-layout detection
- perform no automatic deletion, rename, move, or rewrite
- treat populated directories as project-owned
- leave existing layouts valid indefinitely
- state in documentation that empty historical placeholders may be removed only by deliberate manual project action under project governance
- create no migration command, prompt, helper, flag, report, or tooling

Manual compatibility guidance in `docs/contracts/bootstrap-template-system.md` remains authoritative. Implementation documentation MAY summarize it but MUST NOT weaken or expand it.

## 11. Validation and Test Requirements

Tests MUST remain focused on the accepted exact-output contract and existing safety behavior.

### Exact Output Tests

Add or update tests that assert actual generation creates exactly these relative directories:

```text
docs
docs/architecture
docs/contracts
docs/decisions
docs/vision
standards
templates
tests
```

Add or update tests that assert actual generation creates exactly these relative files:

```text
README.md
ROADMAP.md
CHANGELOG.md
PROJECT_STATE.md
PROJECT_BRAIN.md
AI_HANDOFF.md
LICENSE
.gitignore
```

Tests MUST assert:

- directory count is `8`
- file count is `8`
- generated `forge/` does not exist
- generated `src/` does not exist
- no additional source-code directory is introduced by the implementation

### Dry-Run and Reporting Tests

Tests MUST verify:

- dry-run writes no target directory or file
- dry-run reports exactly eight directories and eight files
- every dry-run path matches the prospective actual-generation plan
- every actual generated path appeared in dry-run
- dry-run and actual generation use the same deterministic ordering
- dry-run reports `forge-bootstrap/2.0.0`
- success reporting contains accurate counts and the output-contract identity
- both modes report `Source layout: not selected`

Tests SHOULD derive expected paths from the accepted literal contract set in the test, not from `FOLDER_PATHS`, so a defect in the implementation constant cannot make the test pass incorrectly.

### Identity and Template Tests

Tests MUST verify:

- `BOOTSTRAP_OUTPUT_CONTRACT` is supported by the rendering context
- its value is exactly `forge-bootstrap/2.0.0`
- generated README and AI handoff render the identity and contain no unresolved token
- generated README and AI handoff contain the required architecture-discovery guidance
- Forge product version and bootstrap output-contract identity appear under distinct labels and are not derived from one another
- missing `BOOTSTRAP_OUTPUT_CONTRACT` fails required-variable validation
- an undeclared or unknown template token still fails template validation
- template metadata is stripped from generated output
- changed template versions and Forge compatibility ranges pass validation

### Regression Tests

Existing relevant tests MUST continue to cover:

- invalid project-name rejection
- non-empty target overwrite protection
- dry-run no-write behavior
- template discovery of exactly eight generated files
- missing required variable rejection
- unknown variable rejection
- compatibility-range validation
- generated content comes from templates

No test may exercise or create migration behavior.

## 12. Documentation and Release Requirements

Implementation MUST update:

- root `README.md` to describe `forge-bootstrap/2.0.0` behavior accurately
- `PROJECT_STATE.md` with implementation status and review gate
- `PROJECT_BRAIN.md` only if a durable implementation constraint or accepted interpretation changes
- `AI_HANDOFF.md` with the next review action and implementation restrictions
- `CHANGELOG.md` with the changed universal bootstrap behavior and compatibility boundary
- an appropriate release note or release-readiness artifact under `docs/release/`

Release evidence MUST state:

- selected pre-`1.0` Forge release number and classification, chosen by Release Authority
- included `forge-bootstrap/2.0.0` identity
- exact eight-directory and eight-file output
- removal of only the generated `forge/` placeholder
- no replacement source directory
- known compatibility limitations
- no automatic migration or migration tooling
- tests and manual verification performed
- rollback readiness
- implementation-review artifact identifier and result

The exact pre-`1.0` Forge release number is intentionally deferred to Release Authority and is not decided by this brief.

The release number is not required before implementation starts. Release Authority MUST select and record it before implementation is declared complete or release evidence is accepted.

Review Authority MUST create or accept the implementation-review evidence after implementation. The Implementation Agent MUST prepare the handoff but MUST NOT approve its own implementation.

## 13. Implementation Sequence

With this brief accepted as `Implementation Ready`, implementation MUST proceed in this order:

1. Inspect the current folder-plan, rendering, CLI, template, and test implementation again before editing.
2. Add the bootstrap output-contract constant and update the exact folder plan in `forge/bootstrap.py`.
3. Add `BOOTSTRAP_OUTPUT_CONTRACT` to supported variables, default rendering context, and `InitResult`.
4. Update only the three affected versioned template assets and their governed metadata.
5. Update dry-run and success reporting in `forge/cli.py`.
6. Update and add the exact-output, identity, validation, and regression tests in `tests/test_init.py`.
7. Update Forge documentation, manual compatibility summaries, changelog, and release evidence.
8. Run targeted and full automated verification.
9. Perform manual dry-run and actual-generation comparison in a temporary location.
10. Inspect the final diff for scope, confirm Forge's internal `forge/` package is otherwise unchanged, and prepare implementation-review handoff.

The code, changed templates, and tests SHOULD be delivered as one reviewable implementation because partial rollout can make template variables or compatibility validation fail.

## 14. Completion Criteria

Implementation is complete only when:

- actual generated output matches `forge-bootstrap/2.0.0`
- actual generation creates exactly eight contracted directories and eight contracted files
- no source-code directory is generated
- only the historical generated `forge/` placeholder behavior is removed
- Forge's internal `forge/` package remains present and otherwise unchanged outside the bounded implementation files
- README and AI handoff output explain deliberate source-layout deferral and provide the architecture-discovery next action
- `.gitignore` no longer selects Python or pytest through universal defaults
- dry-run and actual output plans agree exactly
- dry-run remains read-only
- success and dry-run counts are accurate
- product version and output-contract identity remain distinct
- validation and overwrite protection remain effective
- no existing project is modified
- no migration or profile behavior exists
- all required automated and manual verification passes
- implementation and release documentation are updated
- the change is ready for formal implementation review

## 15. Verification Requirements

Before claiming completion, the Implementation Agent MUST run:

```text
python -m pytest tests/test_init.py
python -m pytest
python -m ruff check .
python -m ruff format --check .
git diff --check
```

The Implementation Agent MUST also:

1. Run `python -m forge init <temporary-name> --dry-run` from a temporary parent directory.
2. Capture the reported identity, directory list, file list, and counts.
3. Run `python -m forge init <temporary-name>` in a clean temporary parent directory.
4. Compare the actual relative directory and file sets with the dry-run plan and the accepted literal contract lists.
5. Confirm both contain exactly eight directories and eight files.
6. Confirm neither contains `forge/`, `src/`, or another source-code directory.
7. Confirm generated README and AI handoff contain `forge-bootstrap/2.0.0`, render no unresolved variables, and provide the required architecture-discovery guidance.
8. Confirm the repository's internal `forge/` package still exists and that no file within it changed except the explicitly scoped `forge/bootstrap.py` and `forge/cli.py` changes.
9. Search the implementation for migration, profile, rename, removal, or existing-project mutation behavior and confirm none was added.

Temporary generated projects MUST remain outside the repository or be removed through a safe, verified cleanup that does not touch project-owned paths.

## 16. Review Handoff Requirements

The implementation handoff MUST include:

- the accepted brief identifier and final lifecycle state
- changed-file inventory
- exact before-and-after directory plans
- exact generated file plan
- output-contract constant and rendering flow
- template metadata and content changes
- test additions and updated assertions
- automated verification commands and results
- manual dry-run versus generation comparison
- generated README and AI handoff excerpts sufficient to verify guidance
- compatibility and no-migration confirmation
- selected release classification and release-evidence link
- known limitations and risks
- rollback procedure
- confirmation that prohibited profile, migration, source-layout, and unrelated CLI behavior was not added

Review Authority MUST verify:

- traceability to ADR 0017 and the accepted contracts
- exact output lists and counts
- complete file and module impact analysis
- objective completion criteria
- compatibility boundaries
- implementation sequence and verification evidence
- Forge product version and bootstrap output-contract separation
- absence of hidden profile, migration, or replacement-source expansion
- no modification of existing generated projects

The Implementation Agent MUST NOT mark the work `Implementation Reviewed`, `Closed`, or `Released`.

## 17. Risks and Rollback Considerations

### Template and Runtime Atomicity

Adding a required template variable before runtime context support, or vice versa, can make all bootstrap generation fail validation.

Mitigation: implement runtime context, templates, and tests in one bounded change and verify both dry-run and actual generation before review.

### Output Count Drift

CLI counts can appear correct while the displayed or actual path set is wrong.

Mitigation: compare literal expected relative sets against both dry-run reporting and actual output.

### Version Namespace Confusion

Forge product version, template versions, and `forge-bootstrap/2.0.0` may be conflated.

Mitigation: keep separate constants and labels, test all identities, and let Release Authority choose the Forge release number.

### Accidental Language Assumptions

Generated guidance or `.gitignore` content may continue to imply Python even after the source directory is removed.

Mitigation: review all eight generated outputs for source-layout and language assumptions; change only README, AI handoff, and `.gitignore` where direct conflicts exist.

### Existing-Project Safety

An implementation could accidentally add migration or cleanup behavior.

Mitigation: retain new-or-empty target validation, add no existing-project inspection, and verify no migration code path exists.

### Rollback

If the implementation fails review or causes bootstrap regression, rollback MUST:

- restore the prior `FOLDER_PATHS` output plan
- remove `BOOTSTRAP_OUTPUT_CONTRACT` runtime and result plumbing
- restore prior CLI reporting
- restore the three affected template versions and contents
- revert the new or changed tests and implementation documentation
- leave ADR 0017, AR-0002, DAR-AR-0002, and accepted contracts unchanged unless a new governance review supersedes them
- never modify a generated project as part of rollback

Rollback readiness MUST be documented before release. A failed implementation MUST return the brief or implementation to the appropriate pre-review state rather than rewriting accepted decision history.

## Engineering Brief Review Gate

Review Authority MUST verify before acceptance that:

- all governing decisions and contracts are traced
- the exact eight-directory and eight-file lists match the accepted contract verbatim
- affected modules, templates, tests, documentation, and release evidence are complete
- acceptance and completion criteria are objective and testable
- compatibility remains prospective, manual, and non-destructive
- sequencing prevents partial template/runtime rollout
- `forge-bootstrap/2.0.0` remains distinct from the Forge release version
- no project profile, migration, replacement source directory, or unrelated `forge init` behavior is included
- no blocking implementation question remains

This focused review returned `PASS`, and Chief Architect acceptance transitions the brief from `Proposed` to `Implementation Ready`.

## Blocking Questions

Blocking questions: none identified in the accepted contracts or this accepted brief.

The exact pre-`1.0` release number and template compatibility range are Release Authority decisions that MUST be resolved before implementation completion but do not block brief review.
