# Forge Roadmap

Forge will evolve deliberately. Each version should add one clear layer of capability without collapsing architecture, documentation, implementation, and automation into the same step.

## 0.1 - Foundation

Goal: establish Forge as a real project before production code exists.

Scope:

- define purpose and vision
- define project boundaries
- document architecture direction
- create project memory documents
- create repository structure
- create initial standards and templates directories
- create first architectural decisions

Exit criteria:

- repository is understandable to a new human or AI agent
- no production code exists
- future implementation direction is explicit

## 0.2 - Project Memory Model

Goal: define how Forge stores durable project context.

Scope:

- specify project memory layers
- define project state format
- define AI handoff format
- define decision record lifecycle
- define context refresh workflow

Exit criteria:

- a project can preserve important context across AI sessions
- memory has clear ownership and update rules

## 0.3 - Standards and Templates

Goal: provide reusable starting material for future projects.

Scope:

- engineering standards templates
- architecture review templates
- testing standards templates
- Git workflow templates
- release note templates
- project bootstrap documentation templates

Exit criteria:

- a human can start a new project manually using Forge documents
- templates are versioned and intentionally scoped

## 0.4 - Bootstrap Specification

Goal: design project bootstrap behavior before implementing it.

Scope:

- define bootstrap inputs and outputs
- define generated repository layout
- define supported project profiles
- define validation checks
- define non-goals and failure modes

Exit criteria:

- CLI behavior can be implemented from documentation
- bootstrap does not depend on hidden assumptions

## 0.5 - CLI Prototype

Goal: introduce the first executable Forge interface.

Scope:

- implement minimal Python package structure
- add a Typer-based or argparse-based CLI decision
- support read-only commands first
- add tests for command behavior

Exit criteria:

- Forge can be installed locally for development
- CLI behavior is tested
- no destructive automation exists

## 0.6 - AI Development Workflow

Goal: formalize AI-assisted engineering operations.

Scope:

- define task intake workflow
- define planning and implementation phases
- define review and handoff workflow
- define AI context bundle generation
- define agent safety boundaries

Exit criteria:

- AI agents can enter a project with consistent context
- human review points are explicit

## 0.7 - Testing and Quality Governance

Goal: make quality expectations enforceable.

Scope:

- define test strategy standards
- define coverage expectations by risk
- define static analysis expectations
- add project health checks
- add quality gate documentation

Exit criteria:

- Forge can describe whether a project is ready for release work
- quality standards are measurable

## 0.8 - Release Management

Goal: define release governance and project lifecycle events.

Scope:

- versioning policy
- changelog workflow
- release checklist
- migration notes
- deprecation policy

Exit criteria:

- projects using Forge can release predictably
- release artifacts are consistent

## 0.9 - Hardening and Dogfooding

Goal: use Forge to manage Forge.

Scope:

- apply Forge workflows to this repository
- reduce ambiguity in standards
- improve templates from real use
- audit architecture decisions
- remove unstable experimental behavior

Exit criteria:

- Forge can govern its own development
- known risks are documented and managed

## 1.0 - Stable Framework Contract

Goal: publish Forge as a stable AI software engineering framework.

Scope:

- stable repository contract
- stable memory contract
- stable template contract
- stable CLI contract if CLI exists
- complete documentation set
- clear migration path from earlier versions

Exit criteria:

- future projects can depend on Forge intentionally
- breaking changes require documented migration guidance
