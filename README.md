# Forge

Forge is an AI Software Engineering Framework.

It is not an application, product, or service. Forge is the foundation for how future software projects are started, guided, documented, governed, tested, released, and handed between humans and AI agents.

## Purpose

Forge exists to make AI-assisted software engineering repeatable, auditable, and durable.

Its purpose is to define the operating system around a project before production code exists:

- how a project begins
- how decisions are captured
- how memory is preserved
- how engineering standards are applied
- how tests are expected to prove quality
- how Git and releases are managed
- how AI agents receive context and hand work back safely

Forge should help future projects move quickly without losing architectural control.

## Vision

Forge will become the reusable foundation for future software projects. A project using Forge should have a clear starting structure, an explicit architecture process, living project memory, consistent standards, and a practical AI development workflow.

Forge should feel like a senior engineering organization in a box: opinionated enough to prevent chaos, light enough to adapt to each project, and transparent enough that humans remain in control.

## Current State

This repository is in Forge `0.3.0` Developer Platform stage.

Forge now includes the first local CLI command:

```text
forge init <project-name>
```

The command creates a Forge-governed project foundation from versioned templates under `templates/bootstrap/`.

Forge 0.3 adds the developer platform needed to maintain the CLI safely: testing standards, code quality standards, and GitHub Actions CI.

The current implementation deliberately does not include `forge review`, plugins, release automation, remote templates, or project profiles beyond bootstrap.

Milestone 0 adds an explicit architecture review gate. See [docs/architecture/review-000.md](docs/architecture/review-000.md).

## Project Boundaries

Forge will define and eventually automate software engineering workflow.

Forge will not:

- become a general task manager
- replace human architectural ownership
- hide decisions inside AI conversations only
- generate production systems without reviewable structure
- couple itself to one future application domain
- require a hosted service to be useful

## Repository Map

```text
.
├── docs/
│   ├── architecture/
│   ├── ci/
│   ├── decisions/
│   ├── engineering/
│   ├── standards/
│   └── vision/
├── .github/workflows/
├── forge/
├── standards/
├── templates/
├── tests/
├── pyproject.toml
├── AI_HANDOFF.md
├── CHANGELOG.md
├── PROJECT_BRAIN.md
├── PROJECT_STATE.md
├── README.md
└── ROADMAP.md
```

See [docs/README.md](docs/README.md) for documentation ownership and update rules.

## Local Usage

Install Forge locally for development:

```text
python -m pip install -e ".[dev]"
```

Run a dry run:

```text
python -m forge init my-project --dry-run
```

Create a project:

```text
python -m forge init my-project
```

Run tests:

```text
python -m pytest
```

Run lint checks:

```text
python -m ruff check .
```

Run format checks:

```text
python -m ruff format --check .
```

The GitHub Actions workflow runs the same quality gate on push and pull request.

## Implementation Language

Forge uses Python because Python is practical for developer tooling, file orchestration, document generation, test automation, AI workflow integration, and cross-platform scripting.

The CLI uses Typer.

## Version Direction

Forge will evolve from documentation foundation to an installable engineering framework:

- `0.1`: foundation and architecture
- `0.2`: project memory model
- `0.3`: developer platform, CI, testing, and code quality standards
- `0.4`: bootstrap design
- `0.5`: CLI prototype
- `0.6`: workflow automation
- `0.7`: testing and quality governance
- `0.8`: release governance
- `0.9`: hardening and dogfooding
- `1.0`: stable framework contract

See [ROADMAP.md](ROADMAP.md) for the full roadmap.
