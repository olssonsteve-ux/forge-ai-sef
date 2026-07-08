# Forge

Forge is an AI Software Engineering Framework.

It is not an application, product, service, library, or CLI yet. Forge is the foundation for how future software projects are started, guided, documented, governed, tested, released, and handed between humans and AI agents.

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

This repository is in foundation stage.

There is no production code.
There is no CLI.
There is no package.
There is no runtime behavior.

The current goal is to establish architecture, documentation, boundaries, standards, and version direction before implementation begins.

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
│   ├── decisions/
│   └── vision/
├── forge/
├── standards/
├── templates/
├── tests/
├── AI_HANDOFF.md
├── CHANGELOG.md
├── PROJECT_BRAIN.md
├── PROJECT_STATE.md
├── README.md
└── ROADMAP.md
```

## Implementation Language Direction

Forge is expected to use Python when implementation begins because Python is practical for developer tooling, file orchestration, document generation, test automation, AI workflow integration, and cross-platform scripting.

No Python implementation exists yet.

## Version Direction

Forge will evolve from documentation foundation to an installable engineering framework:

- `0.1`: foundation and architecture
- `0.2`: project memory model
- `0.3`: templates and standards
- `0.4`: bootstrap design
- `0.5`: CLI prototype
- `0.6`: workflow automation
- `0.7`: testing and quality governance
- `0.8`: release governance
- `0.9`: hardening and dogfooding
- `1.0`: stable framework contract

See [ROADMAP.md](ROADMAP.md) for the full roadmap.
