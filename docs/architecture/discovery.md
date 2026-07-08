# Architecture Discovery

## 1. Purpose

Forge is an AI Software Engineering Framework. Its purpose is to provide a durable foundation for future software projects by combining project bootstrap, memory, standards, architecture governance, testing expectations, Git workflow, and release management.

Forge focuses on the system around software delivery rather than the product being delivered.

## 2. Project Vision

Forge should become the default foundation for future projects. It should help humans and AI agents collaborate through clear context, stable repository conventions, documented decisions, and reviewable automation.

The long-term vision is a framework that can initialize, guide, inspect, and govern software projects while keeping human ownership visible.

## 3. Project Boundaries

Forge is not an application and should not be shaped like one.

Forge owns framework contracts, documentation, templates, standards, and future developer tooling.

Forge does not own product-specific business logic, UI, hosted runtime behavior, database schemas, or application deployment by default.

## 4. Risks

### Overbuilding Too Early

Forge could become too broad before its core contracts are stable. The mitigation is versioned evolution with narrow exit criteria.

### Documentation Drift

If automation evolves separately from documentation, Forge will lose trust. The mitigation is contract-first development and documentation updates with every behavior change.

### AI Context Fragility

If project memory is vague or stale, AI agents may make confident but incorrect changes. The mitigation is explicit memory files, update rules, and handoff practices.

### Excessive Opinionation

Forge must provide useful defaults without blocking legitimate project differences. The mitigation is project profiles and documented override points.

### Tooling Lock-In

Forge should avoid depending on one AI vendor, cloud provider, editor, or hosting service. The mitigation is local-first design and adapter boundaries.

### Premature CLI Design

A CLI can make weak concepts look finished. The mitigation is delaying implementation until file contracts and workflows are clear.

## 5. Repository Structure

Forge should use a documentation-first repository structure:

```text
.
├── docs/
│   ├── architecture/
│   │   ├── discovery.md
│   │   └── proposal.md
│   ├── decisions/
│   │   ├── 0001-documentation-first-foundation.md
│   │   ├── 0002-python-as-implementation-language.md
│   │   └── 0003-defer-cli-implementation.md
│   └── vision/
│       ├── boundaries.md
│       ├── purpose.md
│       └── vision.md
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

The `forge/` and `tests/` directories are intentionally present but empty except for placeholder files. They reserve the future implementation shape without starting production code.

## 6. Version Evolution

Forge should evolve through capability layers:

- `0.1`: foundation and architecture
- `0.2`: project memory model
- `0.3`: standards and templates
- `0.4`: bootstrap specification
- `0.5`: CLI prototype
- `0.6`: AI workflow automation
- `0.7`: quality governance
- `0.8`: release governance
- `0.9`: hardening and dogfooding
- `1.0`: stable framework contract

Each version should have a clear exit criterion and should update project memory.

Implementation milestones should also pass an explicit architecture review gate. The first review is recorded in `docs/architecture/review-000.md`.

## 7. Architecture Proposal

Forge should be organized around contracts and adapters.

The core contract layer defines files, schemas, workflows, and standards. The adapter layer can later implement command-line behavior, template rendering, Git integration, AI context generation, and validation.

Proposed future components:

- Framework Core: shared concepts and project model
- Memory System: project state, project brain, AI handoff, decisions
- Template System: reusable project files and standards
- Bootstrap Engine: creates project foundations from profiles
- Governance Engine: validates standards, decisions, tests, and release readiness
- CLI Adapter: human-facing command interface
- Integration Adapters: Git, AI tools, editors, and CI systems

The first implementation should keep these as conceptual boundaries. Physical modules should only appear when behavior exists.

Documentation authority is defined in `docs/README.md`. Future updates should change the primary document for each concept first, then update summaries only where they would otherwise become misleading.

## 8. Why Python

Python is the correct expected implementation language for Forge because Forge is developer tooling with heavy file-system, documentation, process, and automation concerns.

Python is strong for:

- cross-platform scripting
- readable automation
- template rendering
- filesystem orchestration
- subprocess integration
- test tooling
- markdown and structured file processing
- AI workflow integration
- fast iteration without complex build steps

Python also has a low barrier for future contributors and is widely understood by both humans and AI coding tools.

Forge does not currently need the performance profile, compile-time guarantees, or deployment model that would justify a lower-level language.

## 9. Typer Decision

Typer should likely be used when Forge introduces a CLI, but it should not be introduced in `0.1`.

Reasons to use Typer later:

- excellent developer ergonomics
- type-hint-driven command definitions
- good help output
- strong fit for Python developer tooling
- simpler than building CLI UX manually

Reasons to defer:

- no CLI contract exists yet
- file and workflow contracts should come first
- adding a dependency now creates the appearance of implementation

Current recommendation: defer Typer until `0.5`, then compare Typer against `argparse` using the actual command set.

## 10. Roadmap

The roadmap from `0.1` to `1.0` is captured in `ROADMAP.md`.
