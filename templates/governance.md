# Template Governance

Status: Approved - Contract Review `PASS`

Owner: Chief Architect

Authority: Template governance contract under ADR 0007, ADR 0009, and ADR 0017.

This file governs template ownership, versioning, acceptance, and relationship to `forge init`. It is not a versioned bootstrap template asset, is not located under `templates/bootstrap/`, is not discovered or rendered by current bootstrap generation, and does not alter generated output.

The ADR 0017 requirements below are accepted contract requirements. They do not modify current bootstrap templates or generated output and do not authorize implementation.

Forge templates provide reusable starting points for project documents and structures.

Templates MUST remain transparent. A project created from templates SHOULD be understandable without Forge installed.

## Ownership

Every template MUST have:

- an owning standard or contract
- a clear intended user
- a documented purpose
- a version compatibility statement

## Versioning

Templates follow the Forge version that introduced or changed them.

Template metadata SHOULD eventually include:

- template name
- template version
- compatible Forge versions
- owner document
- change summary

Until template metadata exists, the owning documentation file MUST describe compatibility manually.

Bootstrap template metadata is now defined in `docs/contracts/bootstrap-template-system.md`.

## Change Rules

Template changes MUST be classified as:

- patch: wording, formatting, or examples that do not change expected output
- minor: new optional sections or improved defaults
- major: changed required sections, renamed files, removed sections, or changed generated structure

Major template changes before `1.0` are allowed but MUST be documented in `CHANGELOG.md`.

After `1.0`, major template changes require migration guidance.

## Acceptance Criteria

Every template MUST define:

- intended use
- required inputs
- output files or sections
- owner document or standard
- compatibility
- known limits
- review checklist

## Prohibited Template Behavior

Templates MUST NOT:

- hide architectural decisions
- generate production code before project intent is captured
- require a specific AI vendor
- assume a hosted service
- overwrite existing user files without explicit approval

## Relationship To `forge init`

`forge init` SHOULD use accepted templates only.

If no accepted template exists for a generated file, the CLI specification MUST either defer that file or mark the command as not ready for implementation.

`forge init` MUST NOT hardcode generated file contents in CLI code.

### Universal Bootstrap Structure Boundary

Bootstrap templates MUST follow the accepted universal output contract in `docs/contracts/forge-init-spec.md` and the compatibility rules in `docs/contracts/bootstrap-template-system.md`.

Universal bootstrap templates MUST NOT select or imply a source-code directory, language, package name, framework, application structure, or project profile.

For the prospective `forge-bootstrap/2.0.0` output contract:

- generated README guidance MUST explain that no source directory is generated and direct architecture discovery
- generated AI handoff guidance MUST prevent source-layout invention before a project decision
- applicable templates MUST declare and render the accepted bootstrap output-contract identity
- template compatibility ranges and versions MUST be updated coherently when implementation is later authorized

Template changes remain unauthorized until the affected contract revisions are accepted and a bounded Engineering Brief is accepted.
