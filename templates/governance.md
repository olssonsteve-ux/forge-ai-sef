# Template Governance

Forge templates provide reusable starting points for project documents and structures.

Templates must remain transparent. A project created from templates should be understandable without Forge installed.

## Ownership

Every template must have:

- an owning standard or contract
- a clear intended user
- a documented purpose
- a version compatibility statement

## Versioning

Templates follow the Forge version that introduced or changed them.

Template metadata should eventually include:

- template name
- template version
- compatible Forge versions
- owner document
- change summary

Until template metadata exists, the owning documentation file must describe compatibility manually.

Bootstrap template metadata is now defined in `docs/contracts/bootstrap-template-system.md`.

## Change Rules

Template changes must be classified as:

- patch: wording, formatting, or examples that do not change expected output
- minor: new optional sections or improved defaults
- major: changed required sections, renamed files, removed sections, or changed generated structure

Major template changes before `1.0` are allowed but must be documented in `CHANGELOG.md`.

After `1.0`, major template changes require migration guidance.

## Acceptance Criteria

Every template must define:

- intended use
- required inputs
- output files or sections
- owner document or standard
- compatibility
- known limits
- review checklist

## Prohibited Template Behavior

Templates must not:

- hide architectural decisions
- generate production code before project intent is captured
- require a specific AI vendor
- assume a hosted service
- overwrite existing user files without explicit approval

## Relationship To `forge init`

`forge init` should use accepted templates only.

If no accepted template exists for a generated file, the CLI specification must either defer that file or mark the command as not ready for implementation.

`forge init` must not hardcode generated file contents in CLI code.
