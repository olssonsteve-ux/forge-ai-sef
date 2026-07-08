# Capability Slice Standard

Status: Accepted

## 1. Purpose

Capability Slices exist to convert large accepted Forge capabilities into small, traceable, implementation-sized units.

A Capability Slice sits between a Capability Specification and an Engineering Brief. It preserves the parent capability's intent while defining a bounded increment that can be briefed, implemented, tested, reviewed, and released.

Capability Slices prevent large capabilities from becoming vague implementation programs, overlapping briefs, or loosely connected task lists.

## 2. Scope

A Capability Slice is required when:

- a capability contains multiple services, modes, commands, workflows, or policy areas
- implementation can be delivered in meaningful increments
- multiple agents or teams may work on the capability
- release planning needs a smaller unit than the full capability
- review scope would be unclear without decomposition
- the capability has meaningful persistence, runtime, scoring, policy, or integration concerns

A Capability Slice is not required when:

- the parent capability is already small enough to brief directly
- the change is documentation-only and does not decompose implementation
- the work is a minor correction to an accepted artifact
- the Engineering Brief can fully describe scope, behavior, tests, and review expectations without ambiguity

When uncertain, prefer creating a Capability Slice for large or multi-service work and skipping it for narrow maintenance work.

## 3. Artifact Hierarchy

Forge uses this engineering hierarchy:

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

The Capability Specification defines what Forge must be able to do.

The Capability Slice defines which coherent increment of that capability is being prepared for implementation.

The Engineering Brief defines the exact engineering work to implement the slice.

## 4. Naming Convention

Capability Slice files use this format:

```text
CS-NNN.S-descriptive-name.md
```

Example:

```text
CS-002.1-Governance-Runtime-Status-Service.md
```

Rules:

- `CS` means Capability Slice.
- `NNN` is the parent capability number, matching the FCS number.
- `S` is the slice number within that parent capability.
- The descriptive name uses Pascal-style words separated by hyphens.
- Slice numbers are never reused within the same parent capability.
- File names should remain stable after approval.

## 5. Required Sections

Each Capability Slice must include:

- Title
- Status
- Parent Capability
- Purpose
- Scope
- Non-goals
- Inputs
- Outputs
- Dependencies
- Runtime behavior
- Persistence behavior
- Failure behavior
- CLI/API surface if applicable
- Acceptance criteria
- Testing expectations
- Documentation expectations
- Constitutional compliance
- Relationship to Engineering Briefs
- Release readiness criteria

## 6. Lifecycle

Capability Slice statuses:

### Draft

The slice is being explored and is not binding.

### Specified

The slice has purpose, scope, boundaries, outputs, and acceptance criteria.

### Approved

The slice is accepted as the intended decomposition of the parent capability.

### Implementation Ready

The slice has enough detail for an Engineering Brief to be written.

### Implemented

The implementation work has been completed.

### Reviewed

The implementation has passed the required review.

### Released

The slice has been included in a release.

### Deprecated

The slice is no longer recommended or has been replaced.

## 7. Transition Rules

- `Draft` to `Specified` requires all required sections to be present.
- `Specified` to `Approved` requires architectural agreement that the slice is valid.
- `Approved` to `Implementation Ready` requires clear acceptance criteria, testing expectations, failure behavior, and documentation expectations.
- `Implementation Ready` to `Implemented` requires an Engineering Brief and completed implementation.
- `Implemented` to `Reviewed` requires verification and review evidence.
- `Reviewed` to `Released` requires release readiness evidence.
- Any material scope change after `Approved` requires review and may require an ADR.
- A slice must not become `Implementation Ready` if it conflicts with the Constitution, parent FCS, or accepted ADRs.

## 8. Ownership

### Product Owner

Owns product intent, user value, priority, and roadmap alignment.

### Chief Architect

Owns constitutional alignment, architecture fit, boundaries, and relationship to the parent capability.

### Implementation Agent

Uses the slice to prepare or execute an Engineering Brief. The agent must not expand the slice without approval.

### Review Authority

Reviews whether the implemented work remained inside the slice and parent capability.

### Quality Authority

Owns testing expectations, quality gates, release readiness evidence, and verification standards.

## 9. Traceability

A Capability Slice must trace to:

- `CONSTITUTION.md`
- parent FCS
- relevant ADRs
- Engineering Briefs created from the slice
- implementation files when built
- tests when built
- Design Authority Review when reviewed
- release tag when released

Traceability should be explicit enough for a future human or AI agent to answer:

- why the slice exists
- what capability it belongs to
- what it permits
- what it excludes
- what proves it is complete

## 10. Size Guidance

A good Capability Slice is:

- independently understandable
- independently testable
- implementation-sized
- reviewable
- valuable
- not too broad
- clearly bounded
- traceable to one parent capability
- small enough for one Engineering Brief or a small set of related briefs

If a slice requires many unrelated briefs, it is probably too broad.

If a slice cannot produce a meaningful acceptance decision, it is probably too vague.

## 11. Anti-Patterns

Avoid:

- a slice too large to review
- a slice that only repeats the parent capability
- a slice that describes implementation only
- a slice with no acceptance criteria
- a slice with no clear boundary
- a slice that combines unrelated services
- a slice that bypasses the parent FCS
- a slice that replaces an Engineering Brief
- a slice that hides architecture decisions
- a slice that defines CLI behavior without stating whether CLI is in scope

## 12. Template

The canonical template is:

```text
templates/capability-slices/CS-template.md
```

New Capability Slices should start from the template unless a specific reason is documented.

## 13. Acceptance Criteria

This standard is accepted when:

- purpose and scope are clear
- hierarchy position is defined
- naming convention is defined
- required sections are defined
- lifecycle and transition rules are defined
- ownership is defined
- traceability expectations are defined
- size guidance and anti-patterns are defined
- template exists
- project memory and documentation map are updated

## 14. Future Automation

Future Governance Runtime services may validate:

- file naming
- required sections
- lifecycle status
- parent FCS references
- missing acceptance criteria
- missing test expectations
- missing release readiness criteria
- traceability to Engineering Briefs, tests, reviews, and tags
