# `forge init <project-name>` Pre-Implementation Specification

This document specifies expected behavior for the first future CLI command.

It is not an implementation.

## Command

```text
forge init <project-name>
```

## Purpose

Create a new Forge-governed project foundation using documentation-first defaults.

The command should create a project that is ready for architecture discovery before production code begins.

## Input Arguments And Options

### Required Argument

`<project-name>`

The target project directory name.

Validation:

- required
- must not be empty
- must not be `.` or `..`
- must not contain path traversal
- must not contain characters invalid on supported operating systems
- should use a readable directory-safe name

### Required First Option

`--dry-run`

Print the planned initialization without writing files.

The first implementation should include this option so users can inspect generated structure before files are created.

### Reserved Future Options

These are not required for the first implementation, but the design should leave room for them:

- `--force`
- `--template <name>`
- `--output <path>`
- `--no-git`

## Generated Folders

The initial generated project should contain:

```text
<project-name>/
├── docs/
│   ├── architecture/
│   ├── contracts/
│   ├── decisions/
│   └── vision/
├── forge/
├── standards/
├── templates/
└── tests/
```

The generated `forge/` and `tests/` directories should exist as placeholders only. They must not contain production code.

## Generated Files

The initial generated project should contain:

```text
README.md
ROADMAP.md
CHANGELOG.md
PROJECT_STATE.md
PROJECT_BRAIN.md
AI_HANDOFF.md
docs/README.md
docs/architecture/discovery.md
docs/architecture/proposal.md
docs/contracts/README.md
docs/contracts/project-state-schema.md
docs/contracts/project-brain-schema.md
docs/contracts/ai-handoff-schema.md
docs/contracts/adr-lifecycle.md
docs/decisions/0001-documentation-first-foundation.md
docs/vision/purpose.md
docs/vision/vision.md
docs/vision/boundaries.md
standards/README.md
templates/README.md
forge/.gitkeep
tests/.gitkeep
```

The exact generated content should come from accepted templates once template contracts exist.

## Overwrite Behavior

Default behavior must be conservative.

Rules:

- If `<project-name>` does not exist, create it.
- If `<project-name>` exists and is empty, initialization may continue.
- If `<project-name>` exists and contains files, the command must fail by default.
- The first implementation should not support destructive overwrite.
- A future `--force` option may be considered only after explicit ADR approval.

## Dry-Run Behavior

`--dry-run` should print the planned actions without writing files.

Dry-run output should include:

- target directory
- folders that would be created
- files that would be created
- files that would block initialization
- validation result

Dry-run must not:

- create directories
- create files
- modify existing files
- initialize Git

## Validation Rules

Before writing anything, the command should validate:

- project name is present and valid
- target path can be resolved safely
- target does not require path traversal
- target parent exists or can be created safely
- target is absent or empty
- required templates are available
- generated file plan has no duplicate paths

## Error Handling

Errors should be human-readable and action-oriented.

Expected errors:

- missing project name
- invalid project name
- target already exists and is not empty
- target parent cannot be written
- template source missing
- generated file conflict
- unexpected filesystem failure

The command should avoid partial writes. If partial writes occur due to an unexpected failure, the error should say which path failed and what may have been created.

## Success Output

Successful output should be concise:

```text
Forge project initialized: <project-name>
Created folders: <count>
Created files: <count>
Next step: review PROJECT_STATE.md and begin architecture discovery.
```

## Non-Goals For First Implementation

- no production code generation
- no dependency installation
- no virtual environment creation
- no Git remote setup
- no CI setup
- no application framework selection
- no AI vendor configuration
- no package publishing setup

## Readiness Rule

Implementation may begin only after:

- project memory contracts are accepted
- ADR lifecycle is accepted
- template governance is accepted
- this command behavior is reviewed
