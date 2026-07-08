# AR-0001 - Engineering Hierarchy

Date: 2026-07-08

Status: Accepted architecture review

## Purpose

This architecture review evaluates whether Forge should introduce an additional engineering artifact between:

```text
Capability Specification
  |
  v
Engineering Brief
```

The review is prompted by Forge's expected growth into Governance Runtime, runtime services, plugin ecosystems, enterprise governance, multiple AI agents, and multiple implementation teams.

This is not an implementation task, capability specification, or engineering brief.

## Current Hierarchy

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
Capability Specification
  |
  v
Engineering Brief
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

## Growth Pressure

The current hierarchy is sufficient while Forge has only a few capabilities and a single implementation path.

It becomes strained when Forge contains:

- 50+ capabilities
- 100+ engineering briefs
- multiple AI agents
- plugin ecosystem
- enterprise governance
- runtime services
- multiple implementation teams

The gap is not between roadmap and capability. The gap is between a durable capability and the many independently deliverable increments needed to implement it safely.

Example: Governance Runtime is one capability, but it may eventually include project status, governance status, constitution compliance, engineering readiness, release readiness, risk detection, recommendations, project health, capability health, and knowledge health. Treating each directly as an Engineering Brief would make the capability difficult to trace, sequence, and review.

## Alternatives Evaluated

Scores use:

- `1`: weak
- `2`: limited
- `3`: adequate
- `4`: strong
- `5`: excellent

| Option | Maintainability | Scalability | Governance | Traceability | Documentation Clarity | Engineering Workflow | AI Usability | Human Usability | Platform Evolution | Enterprise Readiness | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Keep current hierarchy | 3 | 2 | 3 | 2 | 4 | 3 | 3 | 4 | 2 | 2 | 28 |
| Feature Specification | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 4 | 2 | 2 | 28 |
| Capability Slice | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 48 |
| Service Specification | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 4 | 4 | 38 |
| Runtime Specification | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 3 | 32 |
| Implementation Slice | 4 | 4 | 3 | 4 | 3 | 5 | 4 | 4 | 3 | 3 | 37 |

## Option Review

### Keep The Current Hierarchy

Benefits:

- simplest model
- no migration required
- least documentation overhead
- easy for small projects

Risks:

- large capabilities become too broad to move directly into Engineering Briefs
- traceability from capability intent to individual implementation increments weakens
- multiple AI agents may produce overlapping briefs
- runtime services may be inconsistently named and scoped
- enterprise governance may require a clearer intermediate planning layer

Assessment:

Keep the current hierarchy only if Forge remains small. It is not strong enough for Governance Runtime scale.

### Feature Specification

Benefits:

- familiar to product teams
- easy for humans to understand
- useful for user-facing product increments

Risks:

- "feature" language conflicts with Forge's principle of capabilities before features
- may encourage product-feature thinking rather than platform capability decomposition
- weaker fit for non-user-facing runtime services and governance functions

Assessment:

Rejected. It would blur Forge's capability-first model.

### Capability Slice

Benefits:

- preserves capability-first governance
- decomposes large capabilities into implementation-sized increments
- improves traceability between FCS and EB
- supports multiple teams and agents without fragmenting the capability
- works for runtime services, plugin APIs, governance checks, and project workflows
- enterprise-friendly because each slice can carry scope, dependencies, risks, and acceptance criteria

Risks:

- adds one more artifact
- may become bureaucratic if used for trivial work
- needs clear lifecycle rules to avoid duplicating Engineering Briefs

Assessment:

Recommended. It is the smallest layer that solves the scaling problem without changing Forge's philosophy.

### Service Specification

Benefits:

- strong fit for runtime services
- clear boundary for service-like capabilities
- useful for Governance Runtime

Risks:

- too narrow for non-service capabilities
- may force every capability into service language
- less useful for documentation, standards, templates, or review workflows

Assessment:

Rejected as the general layer. It may be useful as a subtype of Capability Slice later.

### Runtime Specification

Benefits:

- useful for runtime-oriented systems
- strong for Governance Runtime

Risks:

- too narrow for Forge as a whole
- not every capability is a runtime capability
- could confuse capability specs with implementation architecture

Assessment:

Rejected as the general layer.

### Implementation Slice

Benefits:

- familiar to delivery teams
- strongly tied to execution
- can be used to split work into manageable increments

Risks:

- too close to implementation
- weaker governance posture
- may duplicate Engineering Brief responsibilities
- may understate documentation, review, and governance obligations

Assessment:

Rejected. It solves delivery sizing but not governance traceability.

## Recommendation

Introduce a new engineering layer named:

```text
Capability Slice
```

Updated hierarchy:

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
Capability Specification
  |
  v
Capability Slice
  |
  v
Engineering Brief
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

## Capability Slice Definition

### Purpose

A Capability Slice decomposes an accepted Capability Specification into a coherent, implementation-sized increment that can be briefed, built, tested, reviewed, and released without losing the parent capability's intent.

### Responsibilities

A Capability Slice defines:

- parent capability
- slice purpose
- slice scope
- non-goals
- required inputs
- expected outputs
- dependencies
- acceptance criteria
- risks
- governance impact
- testing expectations
- documentation impact
- implementation readiness

### Inputs

A Capability Slice may use:

- `CONSTITUTION.md`
- `AI_ENGINEERING_CONDUCT.md`
- roadmap item
- accepted FCS
- ADRs
- standards
- project memory
- prior reviews
- known risks

### Outputs

A Capability Slice produces:

- a bounded slice definition
- implementation readiness criteria
- required Engineering Brief topics
- test and review expectations
- documentation update requirements
- known risks and dependencies

### Lifecycle

Suggested lifecycle:

```text
Proposed
  |
  v
Accepted
  |
  v
Briefed
  |
  v
Implemented
  |
  v
Reviewed
  |
  v
Released
```

Possible terminal states:

- Superseded
- Deprecated
- Rejected

### Relationship To Capability Specifications

Capability Specifications define permanent platform capabilities.

Capability Slices decompose accepted capabilities into coherent increments. A slice must not introduce behavior outside the parent FCS unless the FCS is updated first.

### Relationship To Engineering Briefs

Engineering Briefs define the specific work required to implement a slice.

A Capability Slice answers "which part of the capability are we implementing and why?"

An Engineering Brief answers "what exact work will be done now?"

### Relationship To Implementation

Implementation should trace to an Engineering Brief, which traces to a Capability Slice, which traces to an FCS.

Implementation must not use a slice as permission to skip an Engineering Brief when the work is substantial.

### Relationship To Design Authority Reviews

Design Authority Reviews should evaluate whether implemented work stayed within the accepted slice and whether the slice still aligns with the parent FCS and Constitution.

## Migration Analysis

### Benefits

- improves traceability from capability to delivery
- reduces oversized Engineering Briefs
- supports multiple AI agents and teams
- makes runtime service sequencing clearer
- supports enterprise governance
- reduces capability drift
- improves future release notes and review scope

### Risks

- adds documentation overhead
- may be overused for small work
- could duplicate Engineering Briefs if poorly defined
- requires updates to governance hierarchy documents

### Migration Complexity

Migration complexity is medium.

Forge does not need to rewrite existing FCS documents immediately. Existing work can remain valid. Capability Slices should be introduced for future large capabilities and for Governance Runtime implementation planning.

### Backward Compatibility

Backward compatibility impact is low.

Existing FCS and EB documents remain valid. The new layer applies prospectively unless a future review decides to backfill slices for major existing capabilities.

### Existing Documents

Existing FCS-001 and FCS-002 remain valid.

Future implementation of Governance Runtime should begin with one or more Capability Slices before Engineering Briefs are created.

## Repository Impact

Documents that must change now:

- `CONSTITUTION.md`
- `README.md`
- `docs/README.md`
- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md`
- `AI_HANDOFF.md`
- `CHANGELOG.md`
- ADR record

Documents that should change before implementation begins:

- capability specification standard or README
- Engineering Brief standard or template
- future Capability Slice template
- Governance Runtime implementation planning documents
- release and review guidance if slices become release gates

Project structure impact:

- no immediate directory changes are required
- a future `docs/capability-slices/` directory may be considered, but this review does not create it

## Decision

REQUIRES ARCHITECTURAL CHANGE

Forge should introduce Capability Slice as the engineering layer between Capability Specification and Engineering Brief.

## Final Recommendation

Introduce a new engineering layer.

Official name:

```text
Capability Slice
```

Reason:

Capability Slice is the clearest name that preserves Forge's capability-first model while giving large capabilities a scalable, traceable, implementation-ready decomposition layer.
