# DAR-AR-0002 - Generated Project Source Layout

## Review Status

PASS.

## Reviewed Artifact

`docs/architecture/AR-0002-Generated-Project-Source-Layout.md`

## Review Date

2026-07-10

## Review Scope

This Design Authority Review evaluates the recommended universal source-layout behavior for `forge init <project-name>` before an ADR, contract revision, Engineering Brief, or implementation change.

Reviewed sources:

- `CONSTITUTION.md`
- `AI_ENGINEERING_CONDUCT.md`
- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md`
- `AI_HANDOFF.md`
- `docs/architecture/AR-0002-Generated-Project-Source-Layout.md`
- `docs/contracts/bootstrap-template-system.md`
- `docs/contracts/forge-init-spec.md`
- `docs/reviews/GATE-0001-Dogfooding-ForgePlayground.md`
- `docs/reviews/DAR-0001-Forge-0.2.md`
- `docs/standards/lifecycle-standard.md`
- `docs/decisions/0002-python-as-implementation-language.md`
- `docs/decisions/0007-standard-and-template-governance.md`
- `docs/decisions/0008-specify-forge-init-before-implementation.md`
- `docs/decisions/0009-template-driven-bootstrap-generation.md`
- `docs/decisions/0014-introduce-capability-slices.md`
- `ROADMAP.md`
- current bootstrap implementation, templates, and tests for impact analysis only

No implementation behavior is approved or changed by this review.

## Decision Assessed

The reviewed recommendation is to:

- make the universal bootstrap governance-only with no generated source-code directory
- retain `forge/` only as Forge's own implementation package
- require generated projects to choose source layout during architecture discovery
- reserve `src/<package_name>/` for a future governed Python profile
- exclude project profiles and migration tooling from the bounded change

## Summary

AR-0002 correctly identifies that the generated `forge/` directory inherited Forge's own Python package reservation and does not represent a universal need of Forge-governed projects.

The recommended minimal bootstrap is architecturally justified. It preserves language neutrality, human authority, documentation-first project formation, and Forge's identity as an AI-Native Software Engineering Platform rather than an application framework. It also avoids replacing a product-specific assumption with a universal `src/` assumption before project architecture is known.

The recommendation remains useful because `forge init` continues to establish project identity, memory, documentation areas, governance context, standards, templates, and architecture-discovery guidance. The absence of a source directory must be explicit in generated README, AI handoff, dry-run, and success guidance when the change is later specified and implemented.

No condition blocks ADR creation. Contract, template, test, or implementation work remains prohibited until an ADR accepts the durable decision.

## Findings

### Problem Framing

The problem is correctly framed as conceptual coupling between three distinct identities:

- Forge, the platform and its own Python implementation
- a project governed by Forge contracts and practices
- that project's source-code organization

The current generated `forge/` placeholder can incorrectly imply package ownership, Python use, runtime dependency, or platform membership. AR-0002 demonstrates that governance comes from explicit project artifacts and authority, not from a Forge-named code directory.

### Options Completeness

All materially relevant options are assessed:

- retaining `forge/`
- universal `src/`
- Python-style `src/<project_name>/`
- profile-dependent layouts
- no universal source-code directory

The review also evaluates the options across the required project types and comparative criteria. No omitted option would materially change the universal-default decision.

### Constitutional and Product Alignment

The minimal bootstrap aligns with:

- architecture before implementation
- explicit behavior over hidden behavior
- capabilities before features
- documentation-led and contract-led development
- human authority over architectural decisions
- backward compatibility for project-owned generated output
- Forge's boundary against becoming a universal application framework

Forge's use of Python remains an implementation decision for Forge itself and does not become a constraint on generated projects.

### Universal Default

Generating no source-code directory is the appropriate universal default.

`src/` is more neutral in name than `forge/`, but it is not neutral in architecture. It remains unsuitable as a mandatory shape for infrastructure, documentation-led, monorepository, service-oriented, and pre-implementation projects. `src/<project_name>/` adds package and naming assumptions that belong only in a future language-specific profile.

The minimal bootstrap makes the undecided state explicit and leaves a clean path for later profiles without implementing them prematurely.

### Bootstrap Usefulness and Guidance

The recommendation does not weaken the core value of `forge init`. The command's primary value is the governed project foundation: project memory, documentation, decisions, standards, templates, traceability, and a clear first architecture session.

The generated project would be confusing if the source directory simply disappeared without explanation. AR-0002 prevents that outcome by requiring future generated README and AI handoff guidance to state that source layout is intentionally deferred and must be selected during architecture discovery. The future contract revision and Engineering Brief must make this guidance testable.

This guidance requirement is an implementation gate, not a condition on the architectural decision or ADR creation.

### Architecture Discovery as the Decision Point

Architecture discovery is sufficiently defined for this decision. Existing bootstrap guidance already directs maintainers to establish purpose, boundaries, risks, durable decisions, and implementation readiness before production code.

Source layout is an architectural consequence of project type, language, packaging, deployment, and repository boundaries. Selecting it during that process is more coherent than selecting it during universal bootstrap.

A future profile may make an explicit source-layout choice at initialization, but only after profile selection and output contracts are governed. That future possibility does not weaken architecture discovery as the default decision point.

### Impact Completeness

AR-0002 identifies the relevant impact surface:

- bootstrap folder output plan and created-folder count
- dry-run and success output
- generated README and AI handoff guidance
- bootstrap contract and template compatibility guidance
- absence of a new variable for the minimal default
- need for a separate normalized package variable in a future Python profile
- exact-structure and no-production-code tests
- existing generated projects
- manual compatibility guidance
- template provenance limitations
- changelog, release notes, and pre-`1.0` version selection

No hidden implementation assumption remains in the recommendation. Implementation details must be specified later in the contract revision and Engineering Brief.

### Existing Generated Projects

Existing generated projects must not be automatically migrated.

Forge lacks provenance sufficient to distinguish an untouched empty placeholder from project-owned source. Automatic deletion or movement would violate conservative behavior and human ownership. Existing projects remain Forge-governed regardless of whether they retain, rename, remove, or use their `forge/` directory.

Manual compatibility guidance is sufficient:

- empty placeholders may be removed or replaced after a project-owned architecture decision
- populated directories must be treated as project-owned
- intentional packages may remain unchanged
- projects do not need to match the newest bootstrap tree

A migration specification or migration tool is not required for this bounded change.

### Capability Boundary

The change is bounded to one existing bootstrap output rule plus the guidance, test, documentation, and release evidence needed to change it safely. It does not add a new user capability, selection mode, profile manifest, or migration behavior.

A new Capability Slice is not required. A bounded Engineering Brief may follow the accepted ADR and contract revision. Any expansion into selectable profiles or multiple generated layouts is separate capability work and must be governed independently.

### ADR Requirement

An ADR is required after this `PASS` decision and before:

- revision of `docs/contracts/forge-init-spec.md`
- revision of bootstrap template contracts or compatibility rules
- bootstrap template changes
- test changes
- Python, CLI, or runtime implementation changes

The ADR must record the universal minimal-bootstrap default, the separation from future profiles, the compatibility policy for existing projects, and the prohibition on automatic migration.

## Open-Question Classification

| Open question | Classification | Assessment |
| --- | --- | --- |
| Which future capability should own project profiles? | Intentionally deferred | Must be decided before profile work; does not affect the universal default. |
| What normalized package-name variable should a Python profile use? | Intentionally deferred | Belongs to the future Python profile contract; no such variable is needed now. |
| Which pre-`1.0` release should carry the layout change? | Non-blocking follow-up | Release Authority should decide after ADR, contract revision, implementation review, and release evidence exist. |
| When should generated projects record template and output-plan provenance? | Non-blocking follow-up | Provenance should be governed separately before automated migration; manual guidance is sufficient here. |
| Should governance-only initialization receive an explicit profile name? | Intentionally deferred | The universal default does not need a profile system or profile label. |

Blocking open questions: none.

## Compatibility Assessment

The change affects new bootstrap output and is therefore a generated-structure contract change. Pre-`1.0` compatibility permits the change when it is explicit, reviewed, documented, and released with compatibility guidance.

Compatibility risk is limited because the current `forge/` output is an empty placeholder and no production code is generated into it. Risk is further contained by prospective application, accurate dry-run output, no automatic migration, manual guidance, and release disclosure.

The future implementation must preserve target validation, overwrite protection, template-driven content, and the rule against production-code generation.

## Risks

- New users may interpret the absent source tree as incomplete generation unless guidance is explicit.
- Scripts may rely on the existing folder count or `forge/` placeholder.
- Profile behavior could be added accidentally if implementation scope is not kept narrow.
- Template compatibility metadata could become misleading if the structure change is not versioned and documented coherently.

These risks are understood and have explicit follow-on controls. None blocks ADR creation.

## Conditions

None.

## Required Follow-on Governance

1. Create and accept an ADR before changing contracts, templates, tests, runtime behavior, or generated output.
2. Revise the `forge init` and bootstrap template contracts after the ADR.
3. Add manual compatibility guidance; do not add migration tooling.
4. Create a bounded Engineering Brief covering implementation, generated guidance, tests, documentation, and release evidence.
5. Perform implementation review before release or closure.
6. Keep project profiles and language-specific layouts outside this work.

## Decision

PASS.

AR-0002 is approved for ADR creation.

The universal default should generate no source-code directory. This decision does not itself authorize contract, template, test, Python, CLI, runtime, or generated-output changes.

## Implementation Readiness

NOT READY.

Implementation remains blocked pending an accepted ADR, revised bootstrap contracts, and an accepted Engineering Brief.
