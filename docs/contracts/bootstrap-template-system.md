# Bootstrap Template System

Forge project generation must be template-driven.

The CLI must never hardcode the contents of generated project files. `forge init <project-name>` should read versioned templates, validate metadata and variables, render them, and write the rendered output to the target project.

This document defines the architecture contract for that behavior. It is not an implementation.

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

The accepted first bootstrap templates generate root project files only. Documentation subdirectories are created as empty working areas for future architecture documents.

### `templates/documentation/`

Templates for future documentation artifacts such as architecture reviews, discovery documents, and handoff notes.

### `templates/engineering/`

Templates for future engineering workflow files, testing plans, and release checklists.

### `templates/standards/`

Templates for future Forge standard documents.

## Template Metadata

Every template must include a metadata block at the top of the file.

Metadata is part of the template source and must not be emitted into the generated project file unless a template explicitly says otherwise.

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

## Substitution Rules

- Variables are case-sensitive.
- Variable names must use uppercase letters, numbers, and underscores.
- Variables must be declared in template metadata before use.
- Required variables must receive non-empty values.
- Optional variables may be empty.
- Unknown variables must fail validation.
- Missing required variables must fail validation before writing files.
- Substitution should be plain text replacement only.
- No logic, loops, expressions, shell expansion, or code execution is allowed in templates.
- Escaping rules should be specified before implementation if literal `{{` or `}}` is needed.

## Template Validation

Forge should validate templates before rendering.

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

Deprecation metadata may be added later once template registry behavior exists.

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

## Project Compatibility

Generated projects should remain compatible with newer Forge versions through explicit compatibility metadata and migration guidance.

Rules:

- Generated files should include `FORGE_VERSION` where useful for traceability.
- Forge should know which template version generated each file before automated migration is attempted.
- New Forge versions should avoid breaking generated project contracts without migration guidance.
- Pre-1.0 compatibility may change, but changes must be documented.
- After `1.0`, breaking template changes require documented migration steps.

## Migration Strategy

Forge should eventually support template migration by comparing:

- project Forge version
- source template name
- source template version
- current template version
- changed required variables
- changed output paths

Initial migration can be manual and documentation-led. Automated migration is out of scope for the first `forge init` implementation.

## Relationship To `forge init`

`forge init <project-name>` should:

1. load accepted bootstrap templates
2. validate template metadata
3. collect or derive variable values
4. validate required variables
5. build an output plan
6. detect conflicts
7. render templates
8. write generated files only after validation succeeds

The command must not embed generated file bodies in Python code.

The first accepted output mapping is defined in `docs/contracts/forge-init-spec.md`.

## First Implementation Boundary

The first implementation may use only `templates/bootstrap/`.

The first implementation should not support:

- template selection
- remote templates
- template migration
- template registry publishing
- executable template hooks
- conditionals or loops

Those capabilities require future ADRs.
