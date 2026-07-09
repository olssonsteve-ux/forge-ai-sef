# AI Implementation Protocol

Status: Accepted

Owner: Forge Design Authority

Last updated: 2026-07-09

## Purpose

The AI Implementation Protocol defines the mandatory implementation process for AI agents working in Forge-governed projects.

Forge Engineering Briefs should not be implemented through improvised session habits. Every implementation must follow a repeatable protocol that preserves constitutional intent, respects approved scope, verifies behavior, updates documentation, and prepares the work for review.

This protocol becomes the default implementation process for every future Engineering Brief unless an Engineering Brief defines stricter requirements.

## Scope

This protocol applies when an AI agent implements an accepted Engineering Brief.

It applies to:

- Forge itself
- Forge-governed generated projects
- CLI implementation work
- runtime service implementation work
- tests and quality tooling
- documentation updates required by an Engineering Brief

It also applies when an implementation is small. Small changes may move faster, but they do not bypass scope discipline, verification, or reporting.

## Relationship To Forge Governance

### CONSTITUTION.md

`CONSTITUTION.md` is the highest authority. Implementation must preserve Forge's identity, principles, boundaries, and governance hierarchy.

If implementation pressure conflicts with the Constitution, the Constitution wins.

### AI_ENGINEERING_CONDUCT.md

`AI_ENGINEERING_CONDUCT.md` defines AI behavior. This protocol operationalizes that behavior for implementation sessions.

The conduct document says how AI agents must behave. This protocol defines the specific workflow for implementing Engineering Briefs.

### Capability Specifications

Capability Specifications define permanent Forge capabilities. Implementations must understand the parent capability before changing code.

An implementation must not add capability behavior that is absent from the accepted Capability Specification.

### Capability Slices

Capability Slices convert large capabilities into implementation-sized units. Implementations should follow the accepted slice boundary and avoid expanding into adjacent slices.

When a slice exists, the Engineering Brief implements that slice, not the whole parent capability.

### Engineering Briefs

Engineering Briefs are the direct implementation contract. The Engineering Brief defines the approved scope, expected files, tests, verification commands, non-goals, documentation updates, and rollback strategy.

This protocol is mandatory, but the Engineering Brief may add stricter implementation requirements.

### Design Authority Reviews

Design Authority Reviews validate architectural readiness before implementation and implementation quality after implementation.

The implementation report produced under this protocol becomes the handoff material for implementation review.

### Release Process

The release process consumes reviewed implementation work. This protocol does not approve releases, create tags, or replace release readiness checks.

Implementation may prepare a commit, but release decisions remain governed by release standards and review outcomes.

## Mandatory Implementation Workflow

An AI agent implementing an Engineering Brief must follow this workflow:

1. Read `CONSTITUTION.md`.
2. Read `AI_ENGINEERING_CONDUCT.md`.
3. Read the parent Capability Specification.
4. Read the Capability Slice, if one exists.
5. Read the Capability Slice Design Authority Review, if one exists.
6. Read the Engineering Brief.
7. Understand and restate the approved scope before making changes when the scope is complex or risky.
8. Implement only the approved scope.
9. Avoid unrelated improvements, opportunistic refactors, and adjacent features.
10. Run required tests from the Engineering Brief.
11. Run required quality checks from the Engineering Brief and project standards.
12. Update required documentation and project memory after implementation changes are known.
13. Perform or request implementation review according to the Engineering Brief.
14. Prepare a commit only after implementation, verification, and documentation are complete.
15. Await approval before committing or releasing when the user, Engineering Brief, or release process requires approval.

## Implementation Rules

AI agents must follow these rules:

- Never implement beyond the approved scope.
- Never change architecture without an accepted ADR or explicit architecture review outcome.
- Never silently refactor unrelated code.
- Never change existing behavior unless the Engineering Brief requires it or a defect blocks the approved scope.
- Never modify project memory at runtime unless an accepted capability explicitly allows runtime memory writes.
- Never introduce hidden behavior, hidden network calls, hidden file writes, or hidden Git operations.
- Keep implementations deterministic where deterministic behavior is possible.
- Keep CLI output clear, honest, and proportional to the command's authority.
- Preserve existing user work and unrelated uncommitted changes.
- Prefer narrow, reviewable changes over broad cleanup.
- Add tests that prove the contract, not only the happy path.
- Treat documentation as part of the implementation when behavior, commands, standards, or project state change.
- Report uncertainty instead of inventing certainty.

## Required Verification

Every implementation must run the verification commands required by its Engineering Brief.

Unless the Engineering Brief explicitly says otherwise, Forge implementations should run:

```text
python -m pytest
python -m ruff check .
python -m ruff format --check .
git diff --check
```

When a Forge command is implemented or changed, the relevant command must also be run locally, for example:

```text
python -m forge status
```

Additional checks may include:

- focused test modules
- dry-run commands
- generated output inspection
- packaging checks
- CI workflow checks
- repository status checks
- command-specific read-only verification

If a required verification command cannot be run, the implementation report must say why and describe the residual risk.

## Documentation Updates

Implementation must update documentation when behavior or project state changes.

Common required updates include:

- `README.md`
- `CHANGELOG.md`
- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md`
- `AI_HANDOFF.md`
- relevant capability, slice, brief, standard, or release documents

Documentation updates must describe actual behavior, not intended future behavior.

## Reporting Standard

Implementation reports must include:

- Summary
- Files changed
- Tests run
- Verification results
- Remaining risks
- Implementation status
- Ready for review

Recommended final format:

```text
Summary:
...

Files changed:
...

Verification:
...

Remaining risks:
...

Implementation status:
PASS / PASS WITH COMMENTS / REQUIRES REWORK / FAIL

Ready for implementation review:
YES / NO
```

## Review Handoff

The implementation handoff to a reviewer must include:

- the Engineering Brief implemented
- the parent Capability Specification and Capability Slice
- any relevant DAR
- files changed
- behavior added, changed, or intentionally left unchanged
- tests added or updated
- verification command results
- known warnings or limitations
- documentation updated
- residual risks
- any deviation from the Engineering Brief

The reviewer should be able to evaluate the implementation without relying on hidden chat context.

## Acceptance Criteria

An implementation follows this protocol when:

- governing documents were read before implementation
- scope stayed within the Engineering Brief
- unrelated refactors and adjacent features were avoided
- required tests and quality checks were run or explicitly reported as blocked
- documentation and project memory were updated when required
- runtime behavior did not mutate files unless explicitly approved
- the final report follows the reporting standard
- the work is ready for implementation review or clearly marked as not ready

## Non-Goals

This protocol does not define:

- product strategy
- architecture discovery
- capability planning
- Capability Slice design
- Engineering Brief authoring
- release planning
- release approval
- ADR lifecycle
- code style details beyond invoking project quality checks
- multi-agent orchestration policy

## Future Extensions

Future versions may define:

- protocol profiles for documentation-only, code, release, and emergency work
- autonomy levels for AI agents
- multi-agent implementation coordination
- parallel implementation rules
- enterprise implementation controls
- machine-readable implementation reports
- automated protocol compliance checks

