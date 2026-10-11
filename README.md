# Forge

> Build software with intention.

**From human intent to working, verified software with AI agents.**

Forge helps people and AI agents design, build, review and maintain software while preserving
purpose, decisions and evidence across sessions. Its goal is to reduce unnecessary manual work
and administration while keeping humans in control of important decisions.

Read the **[statement of intent](INTENT.md)** and the **[Forge Concept v1.0 baseline](docs/Forge-Concept-v1.0.md)**.

## Current State

The v1 concept is frozen. The implementation is **1.0.0rc1**, a public testing candidate
(tag **v1.0.0-rc.1**), **not a stable 1.0 release**.

244 automated tests and bounded independent code review passed before publication preparation.
Real agent execution, fresh runtime review and apply remain unqualified because of a tool-policy
rejection in the build environment (V1-Q-01). See the
[publication record](docs/release/checklist-1.0.0-rc.1.md) for final checks and the
[assurance record](docs/engineering/Forge-1.0-assurance.md) for detailed evidence.
Try the candidate in a disposable repository or a backup and report reproducible findings.

## Install

Download the wheel from [GitHub Releases](https://github.com/olssonsteve-ux/forge-ai-sef/releases)
and install it in a virtual environment:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install .\forge_ai_sef-1.0.0rc1-py3-none-any.whl
.venv\Scripts\python -m forge --help
```

The package is distributed through GitHub, not PyPI. Windows x64 / CPython 3.14 is the current
qualification target. The package metadata permits Python 3.11 and later; other environments
have not been qualified. Codex is optional for init, status and verify. Task execution requires
Codex CLI 0.160.0 on PATH with an existing login and remains experimental pending qualification.

## Commands

```text
forge init <project-name> [--dry-run]
forge status
forge verify [--config forge.toml]
forge task create <id> --spec <task.json>
forge task show <id>
forge task run <id>
forge task resume <id> --reason <text>
forge task apply <id>
```

Use init only for new projects. Existing repositories keep their structure. Status is read-only.
Verification runs the commands you explicitly configure. Tasks capture an authorized baseline,
work in a separate snapshot, run checks, request a fresh review and require explicit apply before
original files change. Verification commands themselves are trusted operator code.

The [user guide](docs/Forge-1.0-guide.md) covers configuration, task specifications, recovery,
limitations and migration.

## Less administration, retained evidence

One linked assurance record owns a work item's scope, checks, findings and review.
PROJECT_STATE owns current status, PROJECT_BRAIN durable rationale and AI_HANDOFF the handoff.
Authorization persists for ordinary in-scope work. This approach was informed by building
Audio Recorder; see [ADR 0018](docs/decisions/0018-proportionate-records-and-continuous-authorized-work.md).

Historical autonomous FAL experiments remain in the source repository with unresolved findings.
They are excluded from installed wheel and source-distribution runtime code and have not been
accepted or closed. The candidate uses explicit retry and apply, without an automatic correction loop.

## Free and open source

Forge is licensed under the **[MIT License](LICENSE)**. You may use, modify and redistribute it,
including commercially, subject to that license. Forge has no license fee; external AI services
may require a paid account or incur usage charges. Third-party dependencies retain their own licenses.

[Report an issue](https://github.com/olssonsteve-ux/forge-ai-sef/issues) or read
[CONTRIBUTING.md](CONTRIBUTING.md) to test, propose improvements or submit a pull request.

## Development and evidence

```text
python -m pip install -e ".[dev]"
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m forge verify
```

- [Current status](PROJECT_STATE.md)
- [Constitution](CONSTITUTION.md) and [engineering conduct](AI_ENGINEERING_CONDUCT.md)
- [Kernel decision](docs/decisions/0019-stable-isolated-task-kernel.md)
- [Stable 1.0 acceptance checklist](docs/release/checklist-1.0.0.md)

Green tests do not supersede recorded defects or establish live runtime qualification.
