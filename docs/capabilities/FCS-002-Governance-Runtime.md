# FCS-002 - Governance Runtime

## Status

Accepted specification.

## 1. Purpose

The Governance Runtime defines how Forge continuously evaluates whether a project complies with its engineering governance model.

It is the operational layer that interprets the Constitution, AI Engineering Conduct, capability specifications, engineering briefs, standards, reviews, project memory, and release expectations.

The Governance Runtime is not a CLI implementation. It is a permanent Forge capability specification.

The Governance Runtime exists to make engineering health visible, explainable, and actionable before drift becomes expensive.

## 2. Scope

The Governance Runtime applies to Forge-governed projects and to Forge itself.

It evaluates:

- Constitution compliance
- AI Engineering Conduct compliance
- capability completeness
- Engineering Brief completeness
- ADR consistency
- documentation completeness
- review completeness
- testing readiness
- release readiness
- repository health
- project memory health
- standards alignment
- roadmap alignment
- risk visibility
- handoff quality

The Governance Runtime evaluates governance state. It does not modify implementation by itself.

## 3. Relationship To Forge Governance

### Constitution

`CONSTITUTION.md` is the highest governing document.

The Governance Runtime interprets project state through the Constitution. It should identify when work, documents, reviews, or releases do not clearly derive from the constitutional model.

### AI Engineering Conduct

`AI_ENGINEERING_CONDUCT.md` defines expected AI agent behavior.

The Governance Runtime should evaluate whether AI work follows required conduct, including reading project memory, escalating uncertainty, verifying claims, preserving architecture, and updating handoff context.

### Capability Specifications

Forge Capability Specifications define permanent platform capabilities before implementation.

The Governance Runtime should evaluate whether capability work has an accepted FCS and whether implementation has exceeded, ignored, or drifted from that specification.

### Engineering Briefs

Engineering Briefs define bounded engineering work.

The Governance Runtime should evaluate whether briefs are complete enough to support implementation and whether the completed work remains within the brief.

### Implementation

Implementation turns accepted specifications and briefs into working behavior.

The Governance Runtime should evaluate implementation readiness and alignment, but it must not write source code or change implementation automatically.

### Testing

Testing verifies behavior against accepted contracts.

The Governance Runtime should evaluate whether appropriate tests exist, whether relevant quality gates are documented, and whether test results support readiness claims.

### Design Authority Review

Design Authority Review evaluates architecture, maintainability, quality, governance, and readiness.

The Governance Runtime should identify when a DAR is required, missing, stale, or incomplete.

### Release

Release publishes work that has satisfied its gates.

The Governance Runtime should evaluate release readiness, missing release evidence, unresolved risks, and whether a release should proceed, but it must not approve releases automatically.

## 4. Runtime Services

Future implementations of Governance Runtime may provide the following services.

### Project Status

Summarizes current version, objective, milestone, known assets, missing assets, blockers, and recommended next work.

### Governance Status

Summarizes whether required governance documents exist, agree with one another, and derive from the Constitution.

### Constitution Compliance

Evaluates whether project direction, decisions, capabilities, reviews, and releases align with constitutional principles.

### Engineering Readiness

Evaluates whether a project is ready for implementation based on accepted specifications, briefs, ADRs, standards, and memory.

### Release Readiness

Evaluates whether release gates, checks, changelog entries, tags, and review evidence support release.

### Risk Detection

Identifies architecture drift, documentation drift, capability drift, missing tests, stale memory, weak handoff context, and release blockers.

### Recommendation Engine

Produces prioritized next actions with rationale and references to governing documents.

### Project Health

Evaluates repository hygiene, current status, documentation health, test readiness, release posture, and maintainability signals.

### Capability Health

Evaluates whether capability specifications are complete, accepted, implemented consistently, and reviewed.

### Knowledge Health

Evaluates whether project memory, ADRs, handoff context, review lessons, and architectural knowledge remain current and useful.

## 5. Future CLI

Future CLI commands may expose Governance Runtime services.

These commands are examples only and must not be implemented until accepted specifications and engineering briefs exist.

```text
forge status
forge plan
forge review
forge doctor
forge score
forge memory
forge risks
forge release
```

Potential command meanings:

- `forge status`: summarize current project and governance status
- `forge plan`: recommend next governance-aligned work
- `forge review`: run accepted review workflows
- `forge doctor`: detect repository and governance health issues
- `forge score`: report governance and engineering scores
- `forge memory`: inspect project memory health
- `forge risks`: list known and inferred risks
- `forge release`: evaluate release readiness

## 6. Runtime Outputs

The Governance Runtime may produce:

- health reports
- risk reports
- recommendations
- compliance reports
- governance summaries
- quality score
- engineering score
- governance score
- release readiness summaries
- project memory health summaries
- capability health summaries
- missing artifact lists
- drift findings

Outputs should be explainable and cite the documents or evidence used.

Outputs should distinguish between:

- confirmed facts
- inferred findings
- missing evidence
- recommendations
- human decisions required

## 7. Governance Score

The Governance Score is a future measure of how well a project aligns with Forge governance.

It differs from code quality.

Code quality evaluates source code properties such as readability, maintainability, style, correctness, and testability.

Governance Score evaluates whether the project is governable:

- constitutional alignment
- accepted specifications
- complete briefs
- consistent ADRs
- current project memory
- sufficient reviews
- release evidence
- risk visibility
- AI conduct compliance
- documentation authority

This specification defines the concept only. It does not define formulas, weights, thresholds, or automation behavior.

Future scoring formulas require a separate specification update or ADR before implementation.

## 8. Decision Model

The Governance Runtime should reach recommendations by comparing current project evidence against accepted governance expectations.

Examples of decision signals:

- missing Constitution references
- missing ADR for durable decisions
- missing or incomplete capability specification
- missing Engineering Brief
- missing tests for implemented behavior
- missing review before release
- architecture drift
- documentation drift
- capability drift
- stale `PROJECT_STATE.md`
- stale `PROJECT_BRAIN.md`
- stale `AI_HANDOFF.md`
- unverified completion claims
- unresolved release risks
- CI or quality gate failure

Recommendations should include:

- finding
- evidence
- governing source
- risk
- recommended action
- urgency
- whether human decision is required

The Governance Runtime must not present inferred recommendations as settled facts.

## 9. Non-Goals

The Governance Runtime shall not:

- modify source code
- write implementation
- create CLI commands without accepted implementation work
- change architecture automatically
- approve releases automatically
- override human engineering judgment
- bypass the Constitution
- bypass AI Engineering Conduct
- replace Design Authority Review
- replace project maintainers
- hide uncertainty
- mutate project memory without explicit accepted behavior
- publish packages or tags

## 10. Acceptance Criteria

FCS-002 is accepted when:

- purpose is clear
- scope and non-goals are defined
- relationship to the Constitution is defined
- relationship to AI Engineering Conduct is defined
- relationship to capabilities, briefs, implementation, testing, DAR, and release is defined
- runtime services are described
- future CLI examples are documented as non-implemented
- runtime outputs are defined
- Governance Score is introduced conceptually without formula
- decision model is described
- implementation prerequisites are listed
- project memory is updated
- ADR is added if needed

Implementation may begin only when:

- first Governance Runtime service is selected
- input sources are specified
- output format is specified
- persistence behavior is specified
- scoring behavior is specified or explicitly deferred
- project memory mutation behavior is specified
- command scope is accepted if a CLI surface is planned
- tests and fixtures are planned
- failure behavior is specified

## 11. Future Evolution

Future evolution may include:

- Governance Runtime v2
- continuous governance
- enterprise governance
- policy packs
- custom governance rules
- multi-project governance
- governance trend reports
- governance baselines
- release gate integration
- project memory freshness checks
- automated recommendation history
- machine-readable governance output

Future evolution must preserve human authority and constitutional alignment.

## 12. Risks

### False Authority

Runtime recommendations may appear more authoritative than the evidence supports.

Mitigation: outputs must distinguish confirmed facts, inferred findings, recommendations, and human decisions required.

### Over-Automation

Governance Runtime could become an automatic gatekeeper that replaces engineering judgment.

Mitigation: it must not approve releases automatically or override human authority.

### Scoring Misuse

Governance Score could be treated as objective truth.

Mitigation: formulas are explicitly deferred and future scoring must include rationale and evidence.

### Documentation Burden

Governance checks may encourage excessive documents.

Mitigation: recommendations should be proportional to project scope and risk.

### Drift Between Runtime And Constitution

Runtime rules may drift from the Constitution.

Mitigation: constitutional compliance must be a runtime service and FCS changes require governance review.

## 13. ADRs

This capability is supported by ADR `0013 - Governance Runtime Capability`.

Future ADRs are required before:

- defining Governance Score formulas
- allowing runtime output to mutate project files
- making runtime checks release-blocking
- introducing policy packs
- introducing multi-project governance
- adding autonomous remediation

## Implementation Readiness

Governance Runtime is specified at the capability level.

Implementation is not ready yet.

Before implementation begins, Forge must define:

- first runtime service
- first Capability Slice
- command or non-command interface
- input document set
- output format
- persistence rules
- scoring policy
- project memory update policy
- test strategy
- failure and uncertainty behavior
