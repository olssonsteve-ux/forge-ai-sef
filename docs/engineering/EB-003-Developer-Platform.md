# EB-003 - Developer Platform

Status: Accepted for Forge 0.3

Date: 2026-07-08

## Purpose

Forge 0.3 strengthens Forge as a maintainable Python CLI product before new capabilities are added.

The Developer Platform milestone exists to make local development, automated verification, and contribution expectations explicit and repeatable.

## Scope

In scope:

- Python project quality configuration
- test execution standard
- lint and format check standard
- GitHub Actions CI for push and pull request verification
- developer-facing README updates
- project memory updates

Out of scope:

- `forge review`
- new Forge capabilities
- new user-facing CLI commands
- project profiles
- template migration tooling
- release automation beyond CI verification

## Requirements

Forge 0.3 must provide:

- a documented testing standard
- a documented code quality standard
- a documented GitHub Actions standard
- a CI workflow under `.github/workflows/`
- minimal development dependencies
- repeatable local commands for tests and lint checks
- a passing local verification run before release tagging

## Tooling Decisions

Forge uses:

- `pytest` for tests
- `ruff` for lint checks
- `ruff format --check` as the formatting gate

Ruff is selected because it provides fast linting and formatting checks with one lightweight dependency.

## Local Verification Contract

Before a Forge 0.3 release tag, maintainers should run:

```text
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## CI Contract

GitHub Actions must run on:

- `push`
- `pull_request`

CI must:

- install the project with development dependencies
- run tests
- run lint checks
- run formatting checks when configured

## Acceptance Criteria

Forge 0.3 is accepted when:

- Developer Platform documents exist
- CI workflow exists under `.github/workflows/`
- `pyproject.toml` defines test and quality tooling
- `python -m pytest` passes
- `python -m ruff check .` passes
- `python -m ruff format --check .` passes
- README explains local quality commands
- project memory reflects the Developer Platform baseline

## Risks

- CI can drift from local verification if commands are duplicated inconsistently.
- Formatter checks may fail on existing files if formatting is not applied before the gate is enforced.
- Minimal tooling is intentional, but future complexity may require type checking or coverage thresholds.

## Decision

PASS WITH COMMENTS

Forge 0.3 establishes enough Developer Platform structure to support future capabilities, but coverage thresholds, type checking, and release automation remain future work.
