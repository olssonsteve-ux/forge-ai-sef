# GitHub Actions Standard

Status: Accepted for Forge 0.3

## Purpose

Forge CI provides a shared quality gate for changes before they become part of the framework.

CI should be simple, fast, and aligned with the local developer workflow.

## Required Triggers

GitHub Actions workflows must run on:

- `push`
- `pull_request`

## Required Steps

The Forge CI workflow must:

- check out the repository
- set up Python
- install the project with development dependencies
- run `python -m pytest`
- run `python -m ruff check .`
- run `python -m ruff format --check .`

## Python Version

CI should use Python `3.11` as the baseline because Forge declares `requires-python = ">=3.11"`.

Additional versions may be added later if compatibility risk justifies a matrix.

## Acceptance Criteria

CI is acceptable when:

- it runs on push and pull request
- it uses the same commands documented in local standards
- it does not require secrets for normal verification
- it does not publish packages
- it does not deploy artifacts
- it fails fast enough to be useful during development

## Future Improvements

Future milestones may add:

- Python version matrix
- coverage reporting
- build verification
- release checklist automation
- security and dependency scanning
