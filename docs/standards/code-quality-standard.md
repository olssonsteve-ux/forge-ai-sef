# Code Quality Standard

Status: Accepted for Forge 0.3

## Purpose

Forge code should remain small, readable, predictable, and easy for humans and AI agents to change safely.

The code quality standard defines the minimum local and CI checks for Python source, tests, and supporting scripts.

## Required Commands

```text
python -m ruff check .
python -m ruff format --check .
```

## Tooling

Forge uses Ruff for linting and formatting checks.

Configured rule families:

- `E`: pycodestyle errors
- `F`: pyflakes
- `I`: import sorting
- `UP`: Python upgrade suggestions
- `B`: bugbear checks

## Acceptance Criteria

A code change is quality-ready when:

- Ruff lint passes
- Ruff format check passes
- names are clear and domain-oriented
- generated file contents are not hardcoded in Python
- filesystem writes remain conservative
- errors remain human-readable
- new abstractions are justified by real complexity

## Formatting Policy

Ruff format is the formatter recommendation.

Forge CI currently checks formatting but does not auto-format. Maintainers may run:

```text
python -m ruff format .
```

before committing if `ruff format --check` fails.

## Future Improvements

Future milestones may add:

- type checking
- coverage thresholds
- security scanning
- dependency auditing
- release build verification
