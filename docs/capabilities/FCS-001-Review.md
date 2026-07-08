# FCS-001 - Review Capability

## Status

Accepted specification.

## 1. Purpose

The Review Capability defines how Forge evaluates the health, quality, risks, and implementation readiness of a software project.

Forge reviews should make project state visible and actionable. They should help humans and AI agents understand whether a project is architecturally coherent, maintainable, tested, documented, secure enough for its context, and ready for the next milestone.

The Review Capability is a permanent Forge capability. It is not an engineering brief and does not define implementation tasks.

## 2. Scope

The Review Capability applies to Forge-governed projects and to Forge itself.

In scope:

- repository review
- architecture review
- documentation review
- code quality review
- testing review
- security review
- performance review
- maintainability review
- extensibility review
- technical debt review
- project health review
- review scoring
- review recommendations
- updates to project memory

Out of scope for the first implementation:

- automatic code modification
- automatic remediation
- dependency installation
- remote repository mutation
- release publishing
- compliance certification
- replacement of human code review

## 3. Inputs

A Forge review may use the following inputs when available.

### Repository

The project directory, repository structure, tracked files, ignored files, and current working tree state.

### Git History

Commit history, branches, tags, diffs, changed files, and release history.

### Project State

`PROJECT_STATE.md`, including current version, objective, existing assets, missing assets, architectural posture, and recommended next work.

### Project Brain

`PROJECT_BRAIN.md`, including durable beliefs, boundaries, decisions, and open questions.

### Architecture Documents

Files under `docs/architecture/`, including architecture discovery, proposals, review records, diagrams, and architecture notes.

### Engineering Briefs

Future implementation briefs or task specifications that describe intended work.

### ADR

Architecture Decision Records under `docs/decisions/`.

### Source Code

Application, library, tooling, scripts, package files, and generated code when present.

### Documentation

README files, contracts, standards, templates, handoff notes, roadmap, changelog, and user-facing docs.

### Tests

Unit tests, integration tests, regression tests, smoke tests, fixtures, snapshots, and test configuration.

### Configuration

Build configuration, runtime configuration, CI configuration, linting configuration, packaging metadata, environment examples, and release configuration.

## 4. Review Workflow

Forge reviews should follow a repeatable workflow.

1. Establish review scope.
   Define whether the review is full-project or focused on architecture, code, documentation, tests, release readiness, or another capability.

2. Collect inputs.
   Read the repository state, project memory, relevant documentation, ADRs, source code, tests, and configuration.

3. Check repository condition.
   Identify current branch, uncommitted changes, recent commits, ignored files, and generated artifacts that may affect review accuracy.

4. Build project context.
   Summarize purpose, current objective, version, architectural posture, known decisions, and open questions.

5. Evaluate review categories.
   Score each applicable category using the scoring model in this specification.

6. Identify findings.
   Record inconsistencies, risks, missing contracts, weak decisions, quality issues, documentation drift, test gaps, security concerns, and technical debt.

7. Assign severity.
   Classify findings by impact and urgency.

8. Calculate scores.
   Produce category scores, weighted scores, and the Overall Forge Score.

9. Determine outcome.
   Produce `PASS`, `PASS WITH COMMENTS`, or `FAIL`.

10. Produce deliverables.
    Create or update the Forge Review Report and update project memory files when the review changes durable state.

11. Capture lessons.
    Record lessons learned and architecture notes so future work benefits from the review.

12. Recommend next actions.
    Provide prioritized improvements before implementation, release, or the next milestone.

## 5. Review Categories

Each review category receives a score from `0` to `100`.

### Architecture

Evaluates purpose alignment, boundaries, ADR quality, module direction, dependency direction, and architectural consistency.

### Code Quality

Evaluates readability, cohesion, coupling, error handling, naming, duplication, and alignment with local patterns.

### Documentation

Evaluates completeness, accuracy, authority, discoverability, project memory quality, and drift risk.

### Testing

Evaluates test presence, relevance, coverage by risk, regression protection, reliability, and verification clarity.

### Security

Evaluates secret handling, input validation, dependency risk, unsafe operations, authentication and authorization where applicable, and secure defaults.

### Performance

Evaluates algorithmic concerns, resource usage, scalability risks, startup behavior, I/O behavior, and unnecessary work.

### Maintainability

Evaluates ease of future change, clarity of ownership, simplicity, dependency footprint, and long-term project comprehension.

### Extensibility

Evaluates whether the project can evolve without breaking core contracts, creating brittle coupling, or forcing premature abstractions.

### Technical Debt

Evaluates known shortcuts, deferred decisions, TODOs, temporary structures, brittle areas, and unmanaged complexity.

### Project Health

Evaluates overall repository hygiene, roadmap clarity, changelog quality, handoff readiness, active risks, and milestone readiness.

## 6. Scoring Model

Every applicable category receives:

- raw score from `0` to `100`
- weight
- weighted score

### Score Meaning

| Score | Meaning |
| --- | --- |
| `90-100` | Excellent; strong confidence and low review concern. |
| `75-89` | Good; usable with minor or moderate improvements. |
| `60-74` | Caution; meaningful gaps or risks exist. |
| `40-59` | Weak; significant issues should be addressed before major progress. |
| `0-39` | Critical; project is not ready for the reviewed milestone. |

### Default Weights

| Category | Weight |
| --- | ---: |
| Architecture | 15 |
| Code Quality | 12 |
| Documentation | 12 |
| Testing | 12 |
| Security | 10 |
| Performance | 6 |
| Maintainability | 12 |
| Extensibility | 8 |
| Technical Debt | 7 |
| Project Health | 6 |

Weights total `100`.

### Weighted Score

```text
weighted_score = category_score * category_weight / 100
```

### Overall Forge Score

```text
overall_forge_score = sum(weighted_scores)
```

If a category is not applicable, the review must state why. Future implementations may either preserve the default total with `N/A` categories excluded and weights normalized, or require all categories for full reviews. The first implementation must document which approach it uses before scoring automation is introduced.

## 7. Review Outcomes

### PASS

The project is ready for the reviewed milestone.

Minimum guidance:

- Overall Forge Score is `85` or higher.
- No critical findings remain.
- No required deliverables are missing.

### PASS WITH COMMENTS

The project can proceed, but improvements are recommended.

Minimum guidance:

- Overall Forge Score is `70` or higher.
- No unresolved blocker exists.
- Findings are documented and actionable.

### FAIL

The project should not proceed to the reviewed milestone.

Any of the following may cause failure:

- Overall Forge Score below `70`.
- Critical security, architecture, or project health finding.
- Required project memory is missing or misleading.
- Review inputs are insufficient for a reliable conclusion.
- Required deliverables cannot be produced.

## 8. Required Deliverables

Every Forge review must produce or update the following deliverables.

### Forge Review Report

A review report that includes:

- review date
- reviewer
- scope
- inputs reviewed
- category scores
- weighted score table
- Overall Forge Score
- outcome
- findings
- risks
- recommendations
- next actions

### Updated Project Brain

Update `PROJECT_BRAIN.md` when the review reveals durable beliefs, decisions, boundaries, lessons, or open questions.

### Updated Project State

Update `PROJECT_STATE.md` when the review changes status, objective, known assets, missing assets, risks, blockers, or next recommended work.

### Updated AI Handoff

Update `AI_HANDOFF.md` when future AI agents need new instructions, warnings, required reading, or next-step context.

### Recommendations

Prioritized actions that should happen after the review.

### Lessons Learned

Durable lessons that should influence future Forge or project work.

### Architecture Notes

Architecture observations that do not yet require ADRs but should not be lost.

## 9. Acceptance Criteria

FCS-001 is accepted when:

- purpose is clear
- scope and non-scope are defined
- review inputs are listed
- workflow is repeatable
- review categories are defined
- scoring model includes raw scores, weights, weighted scores, and Overall Forge Score
- outcomes are defined as `PASS`, `PASS WITH COMMENTS`, and `FAIL`
- required deliverables are defined
- risks are documented
- future extensions are documented
- project memory and documentation map are updated
- ADRs are added where needed

Implementation of this capability may begin only when:

- report file location and naming are specified
- scoring behavior for `N/A` categories is finalized
- first command scope is chosen
- output format is defined

## 10. Future Extensions

Future review commands may include:

```text
forge review architecture
forge review code
forge review docs
forge review tests
forge review release
```

Other future extensions:

- review profiles
- review report templates
- machine-readable review output
- trend tracking across reviews
- review baselines
- release readiness gates
- security-focused review mode
- pull request review mode
- CI integration
- automated project memory update suggestions

## 11. Risks

### False Precision

Scores may appear more objective than they are. Mitigation: require written findings and rationale beside scores.

### Over-Automation

Forge could generate review output without enough human judgment. Mitigation: preserve reviewer notes and require explicit scope.

### Missing Context

Reviews may miss important project context if project memory is stale. Mitigation: check `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, and `AI_HANDOFF.md` as required inputs when present.

### Category Drift

Review categories may expand inconsistently. Mitigation: change accepted categories through FCS updates and ADRs when behavior changes.

### Security Understatement

General reviews may underweight severe security concerns. Mitigation: any critical security finding can force `FAIL` regardless of total score.

### Documentation Burden

Required deliverables may feel heavy for small projects. Mitigation: allow focused reviews, but require scope and skipped sections to be explicit.

## 12. ADRs

This specification is supported by ADR `0010 - Forge Capability Specifications`.

Future ADRs are required before:

- adding scoring automation
- changing default category weights
- defining review report persistence behavior
- allowing review commands to edit files automatically
- using review outcomes as release gates

## 13. Documentation Updates

This capability requires updates to:

- `docs/README.md`
- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md`
- `AI_HANDOFF.md`
- `CHANGELOG.md`

## Implementation Readiness

This capability is fully specified at the capability level.

Before implementation begins, Forge must still define:

- review report file location and naming
- `N/A` scoring behavior
- first command scope
- output format
- whether project memory updates are automatic, suggested, or manual
