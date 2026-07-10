# `forge init <project-name>` Pre-Implementation Specification

Status: Approved - Contract Review `PASS`

Revision authority: ADR 0017

Owner: Chief Architect

Implementation readiness: `NOT READY`

This document specifies the prospective universal bootstrap behavior accepted architecturally in ADR 0017. It is a contract, not an implementation. Current `forge init` behavior remains unchanged until a bounded Engineering Brief is accepted, implementation is authorized, and implementation passes review.

## Command

```text
forge init <project-name>
```

## Purpose

Create a new Forge-governed project foundation using language-neutral, documentation-first defaults.

The command MUST create a project that is immediately understandable and ready for architecture discovery before production code begins. The universal bootstrap MUST NOT select or create a source-code layout.

## Input Arguments And Options

### Required Argument

`<project-name>`

The target project directory name.

Validation:

- required
- MUST NOT be empty
- MUST NOT be `.` or `..`
- MUST NOT contain path traversal
- MUST NOT contain characters invalid on supported operating systems
- SHOULD use a readable directory-safe name

### Required First Option

`--dry-run`

Print the exact planned initialization without writing files.

The implementation MUST include this option so users can inspect the complete generated structure and bootstrap output-contract identity before files are created.

### Reserved Future Options

These are not required for the bounded implementation, but the design SHOULD leave room for them:

- `--force`
- `--template <name>`
- `--output <path>`
- `--no-git`

## Universal Bootstrap Boundary

The universal bootstrap owns only the language-neutral project foundation:

- project identity and orientation
- project memory
- architecture and decision working areas
- documentation, standards, and template working areas
- a test working area without selecting a test framework
- repository foundation files governed by accepted templates

The universal bootstrap MUST NOT:

- create `forge/`, `src/`, `src/<package_name>/`, `app/`, or any other source-code directory
- select a language, package name, application structure, framework, deployment shape, or source layout
- treat Forge's own `forge/` Python package as a generated-project convention
- select a project profile
- generate production code

Architecture discovery owns the project-specific source-layout decision. A project MAY choose a layout only after its purpose, boundaries, project type, implementation language, packaging or deployment needs, and relevant risks are understood and the decision is recorded through that project's governance.

Future language-specific or project-profile-specific layouts are outside the universal bootstrap contract. They MUST NOT be added until separately accepted capability, profile-selection, variable, validation, compatibility, and output contracts exist.

## Bootstrap Output Contract Identity

The prospective output contract defined by this revision is:

```text
forge-bootstrap/2.0.0
```

The identifier format is:

```text
forge-bootstrap/MAJOR.MINOR.PATCH
```

`forge-bootstrap` is the fixed namespace. The three version components MUST be non-negative decimal integers. The identifier MUST NOT use a leading `v` and MUST NOT be compared as a Forge product release version.

`forge-bootstrap/1.x` identifies the historical universal output shape that included the empty generated `forge/` placeholder. The exact historical template and Forge versions remain evidenced by release history because generated projects did not record a dedicated output-contract identity.

The future implementation MUST associate its output plan, generated README, generated AI handoff, dry-run output, verification evidence, and release notes with `forge-bootstrap/2.0.0`. This identity describes the universal generated structure independently of the Forge release version and individual template versions.

A future breaking structure change MUST increment the output-contract major version. A backward-compatible additive structure or guidance change SHOULD increment the minor version. A clarification that does not change generated output MAY increment the patch version.

The Chief Architect owns the output-contract identity and authorizes proposed version changes through reviewed contract revisions. Release Authority MAY publish an accepted output-contract version as part of a Forge release but MUST NOT redefine its identity or compatibility meaning.

This identity is defined within the existing bootstrap contracts. A separate compatibility contract is not required. Template and output-plan provenance beyond this explicit identity remains deferred governance work.

## Generated Folders

The prospective universal generated project MUST contain exactly these directories:

```text
<project-name>/
├── docs/
│   ├── architecture/
│   ├── contracts/
│   ├── decisions/
│   └── vision/
├── standards/
├── templates/
└── tests/
```

The generated `tests/` directory is a language-neutral working area only. It MUST NOT contain generated tests, select a test framework, or imply a source-code layout.

No source-code directory is part of the universal folder plan. In particular, this contract MUST NOT create `forge/`, `src/`, or another source-code directory.

The exact generated directory count is `8`: `docs/`, its four listed child directories, `standards/`, `templates/`, and `tests/`.

## Generated Files

The prospective universal generated project MUST contain:

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

The exact generated file count is `8`.

Generated file contents MUST come from `templates/bootstrap/`. The CLI MUST NOT hardcode generated document bodies.

The generated `README.md` MUST:

- state that no source-code directory was generated intentionally
- explain that Forge does not select a language, framework, package, or source layout through universal bootstrap
- direct maintainers to architecture discovery before creating source structure
- identify `forge-bootstrap/2.0.0`

The generated `AI_HANDOFF.md` MUST:

- tell the first AI agent that no source layout has been accepted
- direct the agent to establish purpose, boundaries, language and packaging constraints, and source layout through architecture discovery
- prohibit the agent from inventing or creating source structure before the project records that decision
- identify `forge-bootstrap/2.0.0`

## Template Output Mapping

The bounded implementation MUST use this mapping:

| Template | Generated file |
| --- | --- |
| `templates/bootstrap/README.template.md` | `README.md` |
| `templates/bootstrap/PROJECT_STATE.template.md` | `PROJECT_STATE.md` |
| `templates/bootstrap/PROJECT_BRAIN.template.md` | `PROJECT_BRAIN.md` |
| `templates/bootstrap/AI_HANDOFF.template.md` | `AI_HANDOFF.md` |
| `templates/bootstrap/CHANGELOG.template.md` | `CHANGELOG.md` |
| `templates/bootstrap/ROADMAP.template.md` | `ROADMAP.md` |
| `templates/bootstrap/LICENSE.template` | `LICENSE` |
| `templates/bootstrap/gitignore.template` | `.gitignore` |

Additional generated files require accepted templates and an accepted output-contract revision before they can be added to `forge init`.

## Overwrite Behavior

Default behavior MUST remain conservative.

Rules:

- If `<project-name>` does not exist, the command MAY create it.
- If `<project-name>` exists and is empty, initialization MAY continue.
- If `<project-name>` exists and contains files, the command MUST fail by default.
- The implementation MUST NOT support destructive overwrite under this contract.
- A future `--force` option MAY be considered only after explicit ADR approval.

## Dry-Run Behavior

`--dry-run` MUST print the exact planned actions without writing files.

Dry-run output MUST include:

- bootstrap output-contract identity `forge-bootstrap/2.0.0`
- target directory
- the complete ordered directory set that would be created
- the complete ordered file set that would be created
- confirmation that no source-code directory will be generated
- files that would block initialization
- validation result

The reported directory and file counts MUST exactly match the displayed plan: `8` directories and `8` files. Dry-run MUST NOT report `forge/`, `src/`, or another source-code directory.

Dry-run MUST NOT:

- create directories
- create files
- modify existing files
- initialize Git

## Validation Rules

Before writing anything, the command MUST validate:

- project name is present and valid
- target path can be resolved safely
- target does not require path traversal
- target parent exists or can be created safely
- target is absent or empty
- required templates are available
- template metadata is valid
- template variables can be resolved
- generated file plan has no duplicate paths
- generated directory plan exactly matches `forge-bootstrap/2.0.0`
- generated directory plan contains no source-code directory
- rendered README and AI handoff contain the required architecture-discovery and output-contract guidance

Validation and overwrite protection MUST continue to apply to the entire output plan before any write begins.

## Error Handling

Errors MUST be human-readable and action-oriented.

Expected errors:

- missing project name
- invalid project name
- target already exists and is not empty
- target parent cannot be written
- template source missing
- generated file conflict
- unexpected filesystem failure

The command SHOULD avoid partial writes. If partial writes occur due to an unexpected failure, the error MUST say which path failed and what may have been created.

## Implementation Verification Expectations

The future bounded implementation MUST include tests or equivalent verification for:

- valid project name creates the expected output plan
- invalid project names fail before writing files
- non-empty target directory fails by default
- `--dry-run` writes no files or directories
- all bootstrap templates are discovered
- template metadata is validated
- missing required variables fail validation
- unknown template variables fail validation
- generated output strips template metadata
- generated file contents come from templates, not hardcoded CLI strings
- exact `forge-bootstrap/2.0.0` folder and file plan
- no generated `forge/`, `src/`, `src/<package_name>/`, or other source-code directory
- dry-run output exactly matches the write plan and reports the output-contract identity
- generated README explains why no source directory exists and directs architecture discovery
- generated AI handoff prevents source-layout invention and directs architecture discovery
- success output reports accurate folder and file counts
- validation and overwrite protection remain unchanged
- no existing project is inspected, rewritten, or migrated

## Success Output

Successful output MUST be concise and MUST identify the next architecture action:

```text
Forge project initialized: <project-name>
Created folders: 8
Created files: 8
Bootstrap output contract: forge-bootstrap/2.0.0
Source layout: not selected
Next step: review PROJECT_STATE.md and select source layout through architecture discovery.
```

## Non-Goals For First Implementation

- no production code generation
- no dependency installation
- no virtual environment creation
- no Git remote setup
- no CI setup
- no application framework selection
- no language, package name, or source-layout selection
- no AI vendor configuration
- no package publishing setup
- no project profiles
- no migration tooling or automatic migration

## Manual Compatibility Guidance

Projects created under the historical `forge-bootstrap/1.x` shape MUST NOT be automatically migrated.

- A populated `forge/` directory is project-owned and MUST NOT be renamed, moved, deleted, or rewritten automatically.
- An empty generated `forge/` placeholder MAY be removed manually after the project records that choice through its own governance.
- Existing projects MAY retain their current directory layout indefinitely.
- Adoption of `src/`, `src/<package_name>/`, or any other layout is a project architecture decision, not a Forge compatibility requirement.
- Forge provides no migration tooling through this change.
- This guidance is advisory unless an existing project adopts it through its own governance.

The absence of historical output-plan provenance means Forge MUST treat every existing directory conservatively. Automated detection of an "unused" placeholder is not reliable evidence for deletion.

## Future Engineering Brief Surface

After this contract revision and its compatibility guidance are accepted, the bounded Engineering Brief MUST address only:

- the bootstrap directory output plan
- dry-run and success reporting, counts, and output-contract identity
- generated README guidance
- generated AI handoff guidance
- output validation and overwrite-protection regression requirements
- tests for the exact plan and absence of a source-code directory
- template metadata and variables required to render `forge-bootstrap/2.0.0`
- documentation and manual compatibility guidance
- changelog, release notes, compatibility evidence, and implementation review

The Engineering Brief MUST NOT add project profiles, language-specific layouts, migration tooling, dependency installation, framework selection, or unrelated `forge init` changes.

## Contract Questions

Blocking questions: none.

The output-contract identity and manual compatibility policy are defined within the existing contracts. Template provenance, profile ownership, Python package-name normalization, and release timing remain non-blocking deferred governance.

## Contract Acceptance Criteria

This revision is acceptable when reviewers confirm that:

- the universal output plan is exact, language-neutral, and contains no source-code directory
- the boundary between universal bootstrap, architecture discovery, project-owned layout, and future profiles is normative and unambiguous
- README and AI handoff guidance requirements make the generated foundation immediately understandable
- dry-run, validation, overwrite protection, and test obligations are explicit
- `forge-bootstrap/2.0.0` provides a sufficient compatibility identity within existing contracts
- manual compatibility guidance protects populated project-owned directories and prohibits automatic migration
- future implementation surfaces are bounded and complete
- no Capability Slice, project profile, migration tool, or unrelated bootstrap redesign is introduced
- implementation remains unauthorized pending an accepted Engineering Brief

## Readiness Rule

Contract review result: `PASS`.

This revised contract, the corresponding Bootstrap Template System revision, and the manual compatibility guidance are accepted. Engineering Brief creation is now authorized.

Implementation remains `NOT READY` and MUST NOT begin until a bounded Engineering Brief is created, accepted, and reaches `Implementation Ready` under the Lifecycle Standard.

Contract acceptance authorizes only Engineering Brief creation. It does not authorize Python, CLI, test, template, runtime, migration, profile, or generated-output changes.
