# Bootstrap Template System

Status: Approved - Contract Review `PASS`

Revision authority: ADR 0017

Owner: Chief Architect

Implementation readiness: `NOT READY`

Forge project generation MUST be template-driven.

The CLI MUST NOT hardcode the contents of generated project files. `forge init <project-name>` MUST read versioned templates, validate metadata and variables, render them, and write the rendered output to the target project.

This document defines the contract for that behavior and for compatibility of the universal bootstrap output. It is not an implementation. Current templates and generated output remain unchanged until a bounded Engineering Brief is accepted and implementation is authorized.

## Why Template-Driven Generation

Template-driven generation is preferred because it keeps generated project content visible, reviewable, versioned, and changeable without modifying CLI code.

Benefits:

- generated documents can be reviewed before implementation changes
- template changes can be tracked in Git
- different project profiles can evolve without branching CLI logic
- generated files remain understandable after creation
- Forge can support migration guidance when templates change
- the CLI becomes an engine that applies contracts instead of becoming the source of truth

Hardcoding generated content inside the CLI would make architecture harder to review, encourage hidden behavior, and couple project structure to implementation details.

## Template Organization

Templates are organized by purpose:

```text
templates/
├── bootstrap/
│   ├── README.template.md
│   ├── PROJECT_STATE.template.md
│   ├── PROJECT_BRAIN.template.md
│   ├── AI_HANDOFF.template.md
│   ├── CHANGELOG.template.md
│   ├── ROADMAP.template.md
│   ├── LICENSE.template
│   └── gitignore.template
├── documentation/
├── engineering/
└── standards/
```

### `templates/bootstrap/`

Templates used by `forge init <project-name>` to create the initial repository foundation.

The universal bootstrap templates generate root project files only. Documentation subdirectories are created as empty working areas for future architecture documents.

The universal bootstrap MUST NOT create or imply a source-code directory, language, package name, framework, application structure, or project profile. The exact directory and file plan is owned by `docs/contracts/forge-init-spec.md`.

### `templates/documentation/`

Templates for future documentation artifacts such as architecture reviews, discovery documents, and handoff notes.

### `templates/engineering/`

Templates for future engineering workflow files, testing plans, and release checklists.

### `templates/standards/`

Templates for future Forge standard documents.

## Template Metadata

Every template MUST include a metadata block at the top of the file.

Metadata is part of the template source and MUST NOT be emitted into the generated project file unless a template explicitly says otherwise.

Metadata format:

```text
---
template_name: bootstrap-readme
version: 0.1.0
compatible_forge_versions: ">=0.1,<0.2"
description: "Bootstrap README for a new Forge-governed project."
variables:
  - PROJECT_NAME
  - PROJECT_DESCRIPTION
  - AUTHOR
  - FORGE_VERSION
  - CREATED_DATE
required_variables:
  - PROJECT_NAME
  - FORGE_VERSION
  - CREATED_DATE
optional_variables:
  - PROJECT_DESCRIPTION
  - AUTHOR
---
```

Required metadata fields:

- `template_name`
- `version`
- `compatible_forge_versions`
- `description`
- `variables`
- `required_variables`
- `optional_variables`

## Template Variables

Template variables use double braces:

```text
{{PROJECT_NAME}}
```

Initial supported variables:

- `{{PROJECT_NAME}}`
- `{{PROJECT_DESCRIPTION}}`
- `{{AUTHOR}}`
- `{{LICENSE}}`
- `{{YEAR}}`
- `{{FORGE_VERSION}}`
- `{{CREATED_DATE}}`

The prospective `forge-bootstrap/2.0.0` implementation MUST add:

- `{{BOOTSTRAP_OUTPUT_CONTRACT}}`

Its value MUST be `forge-bootstrap/2.0.0`. Templates that emit required compatibility or orientation guidance MUST declare this variable in metadata before use. Adding the variable to templates and runtime support is implementation work and is not performed by this contract revision.

## Substitution Rules

- Variables are case-sensitive.
- Variable names MUST use uppercase letters, numbers, and underscores.
- Variables MUST be declared in template metadata before use.
- Required variables MUST receive non-empty values.
- Optional variables MAY be empty.
- Unknown variables MUST fail validation.
- Missing required variables MUST fail validation before writing files.
- Substitution SHOULD be plain text replacement only.
- No logic, loops, expressions, shell expansion, or code execution is allowed in templates.
- Escaping rules MUST be specified before implementation if literal `{{` or `}}` is needed.

## Template Validation

Forge MUST validate templates before rendering.

### Missing Variables

Detected when a required variable exists in metadata but no value is provided.

Result: fail before writing files.

### Unknown Variables

Detected when template content contains a `{{VARIABLE}}` token not declared in metadata.

Result: fail before writing files.

### Invalid Templates

A template is invalid when:

- metadata block is missing
- required metadata fields are missing
- metadata variable lists disagree
- variable syntax is malformed
- declared compatibility does not include the active Forge version
- output path would conflict with another template

Result: fail before writing files.

### Deprecated Templates

A template is deprecated when metadata or an owning registry marks it as deprecated.

Result:

- warn during dry run
- fail during generation if no non-deprecated accepted template exists for a required output

Deprecation metadata MAY be added later once template registry behavior exists.

## Template Versioning

Template versions use semantic versioning.

### Patch Changes

Patch changes fix wording, formatting, examples, or metadata clarity without changing required variables or generated structure.

Expected compatibility: backwards compatible.

### Minor Changes

Minor changes add optional variables, optional sections, clearer defaults, or new templates that do not break existing generated projects.

Expected compatibility: backwards compatible.

### Major Changes

Major changes rename files, remove sections, change required variables, change generated structure, or alter meaning in a way that affects downstream projects.

Expected compatibility: breaking.

Major changes require:

- changelog entry
- ADR if architecture or workflow changes
- migration guidance
- compatibility range update

Removing the historical generated `forge/` placeholder is a major generated-structure change. Its prospective output-contract identity is `forge-bootstrap/2.0.0`.

## Bootstrap Output Contract Compatibility

Individual template versions identify file-content evolution. `compatible_forge_versions` identifies which Forge releases may render a template. Neither value alone identifies the complete generated folder and file plan.

The universal generated structure therefore has its own identity:

```text
forge-bootstrap/2.0.0
```

The output-contract identity MUST be:

- defined by `docs/contracts/forge-init-spec.md`
- available to future templates as `{{BOOTSTRAP_OUTPUT_CONTRACT}}`
- rendered into the generated README and AI handoff for repository-local traceability
- reported by dry-run and success output
- included in implementation verification and release evidence

The exact identifier syntax, ownership, and version-increment rules are defined by `docs/contracts/forge-init-spec.md`. Bootstrap contract identifiers and Forge release versions are separate namespaces and MUST NOT be compared as the same version type.

This existing contract is sufficient to define compatibility metadata for the bounded change. A separate compatibility contract is not required. A future provenance system MAY add a manifest or richer per-file history only through separate accepted governance.

## Project Compatibility

Generated projects SHOULD remain compatible with newer Forge versions through explicit compatibility metadata and migration guidance.

Rules:

- Generated files SHOULD include `FORGE_VERSION` where useful for traceability.
- Generated README and AI handoff files MUST include the bootstrap output-contract identity.
- Forge MUST know which template and output-contract versions apply before automated migration is considered.
- New Forge versions SHOULD avoid breaking generated project contracts without migration guidance.
- Pre-1.0 compatibility MAY change, but changes MUST be documented.
- After `1.0`, breaking template changes MUST include documented migration steps.

## Manual Compatibility Guidance for Historical Projects

This section is the authoritative manual compatibility guidance for projects created with the historical universal output shape that included an empty `forge/` placeholder.

- Existing generated projects MUST NOT be automatically migrated.
- A populated `forge/` directory is project-owned and MUST NOT be renamed, removed, moved, or rewritten automatically.
- An empty placeholder directory MAY be removed manually after the project adopts that action through its own governance.
- Existing projects MAY retain their current layout indefinitely.
- Adoption of a different layout is a project architecture decision.
- Forge MUST NOT provide migration tooling as part of the `forge-bootstrap/2.0.0` change.
- This guidance is advisory unless an existing project adopts it through its own governance.

Forge does not have historical output-plan provenance sufficient to distinguish every empty generated placeholder from later project-owned state. The absence of files is not sufficient authority for automatic deletion.

## Migration Strategy

Future separately governed migration capabilities MAY compare:

- project Forge version
- source template name
- source template version
- current template version
- changed required variables
- changed output paths

For the `forge-bootstrap/2.0.0` structure change, migration is manual and documentation-led. Automated migration and migration tooling are prohibited within this change.

## Relationship To `forge init`

`forge init <project-name>` MUST:

1. load accepted bootstrap templates
2. validate template metadata
3. collect or derive variable values
4. validate required variables
5. build an output plan
6. detect conflicts
7. render templates
8. write generated files only after validation succeeds

The command MUST NOT embed generated file bodies in Python code.

The prospective `forge-bootstrap/2.0.0` output mapping and directory plan are defined in `docs/contracts/forge-init-spec.md`. The command MUST NOT create a source-code directory under the universal contract.

The generated README MUST explain that no source directory exists because source layout is selected through architecture discovery. The generated AI handoff MUST direct the first agent to architecture discovery and MUST prohibit inventing source structure before a project decision exists.

Dry-run output MUST exactly match the generated directory and file plan, identify `forge-bootstrap/2.0.0`, and confirm that no source-code directory will be created.

## First Implementation Boundary

The bounded implementation MAY use only `templates/bootstrap/`.

The bounded implementation MUST NOT support:

- template selection
- remote templates
- template migration
- template registry publishing
- executable template hooks
- conditionals or loops

Those capabilities require future ADRs.

The bounded implementation also MUST NOT support project profiles, language-specific source layouts, migration tooling, or automatic modification of existing generated projects.

## Future Implementation Surfaces

The future Engineering Brief MUST account for:

- bootstrap output-plan constants and directory counts
- dry-run and success reporting
- template-variable support for `BOOTSTRAP_OUTPUT_CONTRACT`
- README and AI handoff template metadata and guidance
- output-plan, validation, overwrite-protection, and rendering tests
- manual compatibility documentation
- changelog, release notes, compatibility ranges, and implementation-review evidence

These surfaces are identified for planning only. This contract revision does not authorize changes to Python, CLI behavior, tests, templates, runtime behavior, or generated output.

## Contract Questions

Blocking questions: none.

Compatibility metadata is fully definable in the existing `forge init` and Bootstrap Template System contracts through `forge-bootstrap/2.0.0` and `BOOTSTRAP_OUTPUT_CONTRACT`. Richer provenance, project profiles, Python package normalization, and migration automation remain deferred.

## Contract Acceptance Criteria

This revision is acceptable when reviewers confirm that:

- template-driven generation remains mandatory
- the exact universal output plan is owned by `docs/contracts/forge-init-spec.md`
- templates cannot imply or create a universal source-code layout
- generated README and AI handoff guidance requirements are explicit
- output-contract identity is distinct from Forge and individual template versions
- manual compatibility guidance protects project-owned directories and prohibits automatic migration
- template, runtime, test, and release surfaces are bounded for a future Engineering Brief
- no separate compatibility contract is required
- no blocking contract question remains
- implementation remains `NOT READY` pending an accepted Engineering Brief

## Contract Readiness

Contract review result: `PASS`.

This revision, the corresponding `forge init` specification revision, and the manual compatibility guidance are accepted. Engineering Brief creation is now authorized.

Implementation remains `NOT READY` and MUST NOT begin until a bounded Engineering Brief is created, accepted, and reaches `Implementation Ready` under the Lifecycle Standard.
