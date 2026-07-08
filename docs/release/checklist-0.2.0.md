# Forge 0.2.0 Release Checklist

## Release Scope

Forge `0.2.0` introduces the first MVP implementation layer.

Included:

- Python package configuration
- Typer-based CLI entrypoint
- `forge init <project-name>`
- bootstrap rendering from `templates/bootstrap/`
- project name validation
- dry-run mode
- conservative overwrite protection
- template metadata validation
- template variable validation
- template compatibility validation
- tests for the core `forge init` contract

Not included:

- `forge review`
- plugins
- project profiles beyond bootstrap
- template migration tooling
- release automation
- package publishing

## Versioning

Release version: `0.2.0`

Version rationale: minor release because Forge gains its first implemented CLI capability.

## Test Expectations

Required before tagging:

```text
python -m pytest
```

Expected result:

```text
7 passed
```

Required CLI smoke test:

```text
python -m forge init release-smoke --dry-run
```

Expected result:

- exits successfully
- reports validation `OK`
- reports `9` folders
- reports `8` files
- does not create `release-smoke`

## Known Limitations

- Template metadata parsing is intentionally minimal and supports the current front matter shape only.
- Failed writes can leave partial folders or files; rollback is not implemented.
- Generated projects do not yet record template provenance metadata.
- `forge init` supports only bootstrap templates.
- `forge init` does not install dependencies, initialize Git, configure CI, or choose an application framework.
- `forge review` is specified but not implemented.
- Package publishing is not configured.

## Packaging Decision

Forge `0.2.0` is local editable only.

Supported local development install:

```text
python -m pip install -e ".[dev]"
```

No package index publishing is recommended for `0.2.0`.

## Release Checklist

- [x] Version is set to `0.2.0` in `pyproject.toml`.
- [x] Version is set to `0.2.0` in `forge/__init__.py`.
- [x] `CHANGELOG.md` includes `0.2.0`.
- [x] `PROJECT_STATE.md` reflects release readiness.
- [x] `PROJECT_BRAIN.md` records release decisions.
- [x] `AI_HANDOFF.md` includes release-state guidance.
- [x] Release standard exists.
- [x] Test expectations are documented.
- [x] Known limitations are documented.
- [x] Packaging decision is documented.
- [x] Tag recommendation is documented.

## Tag Recommendation

Recommended tag:

```text
v0.2.0
```

Only tag after release readiness documentation is committed and the working tree is clean.

## Release Readiness

Ready to tag v0.2.0: YES
