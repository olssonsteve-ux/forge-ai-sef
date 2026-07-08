# Testing Standard

Status: Accepted for Forge 0.3

## Purpose

Forge tests protect CLI behavior, template rendering, project generation safety, and documented contracts.

Tests should make it difficult to accidentally break the developer workflow or generated project foundation.

## Required Test Command

```text
python -m pytest
```

## Test Categories

Forge tests should cover:

- CLI command behavior
- project name validation
- dry-run behavior
- overwrite protection
- template discovery
- template metadata validation
- template rendering
- generated output expectations

## Acceptance Criteria

A change is test-ready when:

- relevant tests exist or an explicit reason is documented
- `python -m pytest` passes locally
- CI runs the same test command
- tests avoid network and external service dependencies
- tests use isolated temporary directories for filesystem writes

## Expansion Rules

Add tests when:

- CLI behavior changes
- template validation rules change
- generated output structure changes
- error handling changes
- release or CI behavior changes

Do not add broad, slow, or flaky tests unless the risk justifies them.

## Future Improvements

Future Forge milestones may add:

- coverage reporting
- minimum coverage thresholds
- integration dogfooding tests
- review report fixture tests
- generated project snapshot tests
