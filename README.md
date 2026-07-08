# Forge

> Build software with intention.

Forge is an AI-Native Software Engineering Platform.

Forge provides a disciplined engineering environment where humans and AI collaborate to design, build, review, govern and evolve software.

Forge is built upon five permanent ideas:

Architecture before implementation.

Specifications before code.

Capabilities before features.

Review before release.

Continuous engineering improvement.

Forge develops Forge.

## Constitutional Foundation

The highest governing document in Forge is [CONSTITUTION.md](CONSTITUTION.md).

Every future engineering decision should ultimately derive from the Constitution:

```text
Constitution
  |
  v
Product Strategy
  |
  v
Roadmap
  |
  v
Capability Specifications
  |
  v
Capability Slices
  |
  v
Engineering Briefs
  |
  v
Implementation
  |
  v
Testing
  |
  v
Design Authority Review
  |
  v
Release
```

AI agent behavior is governed by [AI_ENGINEERING_CONDUCT.md](AI_ENGINEERING_CONDUCT.md).

## Purpose

Forge exists to make AI-assisted software engineering repeatable, auditable, durable, and governable.

Forge addresses the layer around code: purpose, memory, architecture, specifications, standards, templates, testing, review, release, and human-AI handoff quality.

## Current State

This repository is in Forge `0.3.1` AI Engineering Conduct stage.

Forge includes the first local CLI command:

```text
forge init <project-name>
```

The command creates a Forge-governed project foundation from versioned templates under `templates/bootstrap/`.

Forge 0.3 adds the developer platform needed to maintain the CLI safely: testing standards, code quality standards, and GitHub Actions CI.

Forge `v0.3.1` adds the constitutional identity foundation. The current governance milestone adds the AI conduct layer before Forge 0.4 Governance Runtime begins.

Forge now specifies Governance Runtime as the future operational layer that evaluates constitutional compliance, engineering health, project memory, capability readiness, risk, and release posture. It is specified in [FCS-002](docs/capabilities/FCS-002-Governance-Runtime.md) and is not implemented yet.

The current implementation deliberately does not include `forge review`, plugins, release automation, remote templates, or project profiles beyond bootstrap.

## Scope

Forge is:

- an AI-Native Software Engineering Platform
- a project memory system
- a specification-first capability model
- a standards and review environment
- a bootstrap and template foundation
- a quality and release discipline
- a human-AI collaboration structure
- an AI engineering conduct model

Forge is not:

- a general application framework
- a hosted service by default
- a replacement for engineering judgment
- a hidden code generator
- a task manager
- a single-vendor AI workflow
- a shortcut around architecture, testing, review, or release discipline

## Repository Map

```text
.
+-- .github/workflows/
+-- docs/
|   +-- architecture/
|   +-- capabilities/
|   +-- ci/
|   +-- contracts/
|   +-- decisions/
|   +-- engineering/
|   +-- release/
|   +-- reviews/
|   +-- standards/
|   +-- vision/
+-- forge/
+-- standards/
+-- templates/
+-- tests/
+-- AI_HANDOFF.md
+-- AI_ENGINEERING_CONDUCT.md
+-- CHANGELOG.md
+-- CONSTITUTION.md
+-- PROJECT_BRAIN.md
+-- PROJECT_STATE.md
+-- README.md
+-- ROADMAP.md
+-- pyproject.toml
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

## Engineering Model

Forge develops through durable governing artifacts:

- the Constitution defines permanent identity and principles
- AI Engineering Conduct defines how AI agents must behave
- the roadmap orders strategic work
- Forge Capability Specifications define permanent capabilities
- Capability Slices decompose large capabilities into implementation-sized increments
- Governance Runtime will interpret the governance model operationally
- Engineering Briefs define bounded implementation work
- tests and standards verify quality
- Design Authority Reviews protect long-term coherence
- releases publish only reviewed work

## Implementation Language

Forge uses Python because Python is practical for developer tooling, file orchestration, document generation, test automation, AI workflow integration, and cross-platform scripting.

The CLI uses Typer.

## Version Direction

Forge will evolve from constitutional foundation to a stable AI-native engineering platform:

- `0.1`: foundation and architecture
- `0.2`: bootstrap MVP and dogfooding
- `0.3`: developer platform, CI, testing, code quality, and constitutional identity
- future milestones: Governance Runtime, review, knowledge, capability runtime, and ecosystem maturity
- `1.0`: stable platform contract

See [ROADMAP.md](ROADMAP.md) for the full roadmap.
