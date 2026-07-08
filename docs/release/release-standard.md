# Forge Release Standard

This document defines how Forge releases are prepared and accepted.

Forge releases should be deliberate, reviewable, and reversible where possible. A release is not just a version number; it is a documented statement about capability, limitations, tests, packaging, and next-step risk.

## Versioning Policy

Forge uses semantic versioning.

Format:

```text
MAJOR.MINOR.PATCH
```

### Major

Increment `MAJOR` for stable post-1.0 breaking changes.

Before `1.0`, breaking changes are allowed when they improve the platform contract, but they must be documented in `CHANGELOG.md`.

### Minor

Increment `MINOR` for new capabilities, new commands, accepted contracts, or meaningful platform behavior.

Examples:

- first CLI command
- new Forge Capability Specification
- new template system
- new project memory contract

### Patch

Increment `PATCH` for fixes that do not change public contracts.

Examples:

- bug fixes
- test improvements
- documentation corrections
- compatibility metadata fixes

## Release Requirements

Every release must define:

- version
- release scope
- included capabilities
- known limitations
- test expectations
- packaging decision
- tag recommendation
- changelog entry

## Test Expectations

Before a release is tagged:

- automated tests must pass
- CLI smoke tests must pass for implemented commands
- release-specific checklist must record the test commands used
- known untested areas must be documented as limitations

## Packaging Decision

Every release must state whether Forge is:

- local editable only
- packaged but not published
- published to a package index
- distributed another way

Packaging decisions must be explicit so users do not assume an installation channel exists.

## Release Checklist Rules

Each release should have a checklist under `docs/release/`.

Checklist file naming:

```text
checklist-X.Y.Z.md
```

Example:

```text
checklist-0.2.0.md
```

## Tag Recommendation

Release tags should use:

```text
vX.Y.Z
```

Example:

```text
v0.2.0
```

Do not tag a release until:

- release checklist is complete
- tests pass
- changelog is updated
- project memory reflects release state
- working tree is clean after committing release readiness changes

## Release Outcome

Each release checklist must end with:

```text
Ready to tag vX.Y.Z: YES/NO
```
