# Documentation Map

This directory contains Forge's durable architecture documentation.

Forge's highest governing document is `CONSTITUTION.md` at the repository root. Every document in `docs/` derives from it.

Forge documentation is intentionally split by authority. Files may reference the same concepts, but each concept should have one primary home.

## Document Authority

| Topic | Primary Document | Supporting Documents |
| --- | --- | --- |
| Constitutional identity and governance | `CONSTITUTION.md` | `README.md`, `PROJECT_BRAIN.md`, ADRs |
| Project identity and quick orientation | `README.md` | `CONSTITUTION.md`, `docs/vision/purpose.md`, `docs/vision/vision.md` |
| Purpose | `CONSTITUTION.md` | `docs/vision/purpose.md`, `README.md` |
| Vision | `CONSTITUTION.md` | `docs/vision/vision.md`, `README.md` |
| Boundaries | `docs/vision/boundaries.md` | `docs/architecture/discovery.md` |
| Architecture proposal | `docs/architecture/proposal.md` | `docs/architecture/discovery.md` |
| Architecture discovery and review findings | `docs/architecture/discovery.md` | `docs/architecture/review-000.md` |
| Engineering hierarchy reviews | `docs/architecture/AR-0001-Engineering-Hierarchy.md` | `CONSTITUTION.md`, ADRs |
| Generated project source layout | `docs/decisions/0017-generated-project-source-layout.md` | `docs/contracts/forge-init-spec.md`, `docs/contracts/bootstrap-template-system.md`, `docs/engineering/EB-004-Implement-Universal-Bootstrap-Output-Contract.md`, `docs/architecture/AR-0002-Generated-Project-Source-Layout.md`, `docs/reviews/DAR-AR-0002-Generated-Project-Source-Layout.md`, `docs/reviews/DAR-EB-0003-EB-004-Universal-Bootstrap-Implementation.md` |
| Forge capabilities | `docs/capabilities/` | `docs/decisions/0010-forge-capability-specifications.md` |
| Capability Slices | `docs/standards/capability-slice-standard.md` | `templates/capability-slices/CS-template.md`, `docs/architecture/AR-0001-Engineering-Hierarchy.md`, `docs/decisions/0014-introduce-capability-slices.md` |
| Project Memory Health implementation brief | `docs/engineering/EB-005-Implement-Project-Memory-Health.md` | `docs/capabilities/CS-002.3-Governance-Runtime-Project-Memory-Health.md`, `docs/reviews/DAR-CS-0003-CS-002.3-Project-Memory-Health.md`, `docs/engineering/implementation-review-handoff-EB-005.md`, `docs/reviews/DAR-EB-0004-EB-005-Project-Memory-Health-Implementation.md` |
| Adaptive Loop V1 state and runtime contract | `docs/contracts/adaptive-loop-v1.md` | `schemas/forge-adaptive-loop-v1.schema.json`, `fixtures/adaptive-loop-v1/gate.json`, `docs/reviews/RETRO-0001-audio-recorder-dogfooding.md` |
| FAL-001 final blocked disposition | `docs/decisions/DISP-FAL-001-terminated-blocked.md` | `docs/decisions/HD-FAL-002-terminate-fal-001-design-fal-002.md`, `docs/reviews/IR-FAL-002-human-bounded-correction-final-review.md` |
| FAL-002 Standard Assurance design and implementation plan | `docs/capabilities/FAL-002-Standard-Assurance-Bounded-Engineering-Loop.md` | `docs/decisions/HD-FAL-003-revise-fal-002-specification.md`, `docs/decisions/HD-FAL-004-revise-residual-fal-002-findings.md`, `docs/decisions/HD-FAL-005-revise-final-fal-002-residual-findings.md`, `docs/decisions/HD-FAL-006-approve-fal-002-for-implementation-planning.md`, `docs/decisions/HD-FAL-007-authorize-eb-006-residual-correction.md`, `docs/decisions/HD-FAL-008-authorize-eb-006-residual-documentation-correction.md`, `docs/decisions/HD-FAL-009-reconcile-fal-002-implementation-scope-and-production-loc-budget.md`, `docs/decisions/HD-FAL-010-authorize-eb-006-second-residual-assurance-correction.md`, `docs/decisions/HD-FAL-011-require-fal-002-recovery-architecture-decision.md`, `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`, `docs/architecture/FAL-002-reuse-matrix.md`, `docs/engineering/FAL-002-album-before-after-measurement-plan.md` |
| AI implementation protocol | `docs/standards/ai-implementation-protocol.md` | `AI_ENGINEERING_CONDUCT.md`, Engineering Briefs, `docs/decisions/0015-ai-implementation-protocol.md` |
| Lifecycle governance | `docs/standards/lifecycle-standard.md` | `PROJECT_STATE.md`, `CHANGELOG.md`, `docs/decisions/0016-lifecycle-standard.md` |
| Document contracts | `docs/contracts/` | `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, `AI_HANDOFF.md` |
| Bootstrap template system | `docs/contracts/bootstrap-template-system.md` | `templates/`, `docs/decisions/0009-template-driven-bootstrap-generation.md` |
| First CLI behavior | `docs/contracts/forge-init-spec.md` | `ROADMAP.md`, `docs/decisions/0008-specify-forge-init-before-implementation.md` |
| Version roadmap | `ROADMAP.md` | `README.md` |
| Current project state | `PROJECT_STATE.md` | `AI_HANDOFF.md` |
| Durable project memory | `PROJECT_BRAIN.md` | `AI_HANDOFF.md` |
| AI contributor instructions | `AI_HANDOFF.md` | `PROJECT_STATE.md`, `PROJECT_BRAIN.md` |
| Architectural decisions | `docs/decisions/` | architecture documents |
| Constitutional decision record | `docs/decisions/0011-forge-constitutional-governance-and-product-identity.md` | `CONSTITUTION.md` |
| Standards | `docs/standards/README.md` | `standards/README.md`, standards files |
| Templates | `templates/README.md` | future template files |
| EB-004 implementation readiness evidence | `docs/release/EB-004-universal-bootstrap-output-contract-readiness.md` | `docs/engineering/EB-004-Implement-Universal-Bootstrap-Output-Contract.md`, `docs/reviews/DAR-EB-0003-EB-004-Universal-Bootstrap-Implementation.md`, `docs/release/checklist-0.5.0.md` |

## Update Rules

- Update the primary document when a concept changes.
- Update supporting documents only when their summary would become misleading.
- Add an ADR for durable architecture decisions, governance changes, or implementation constraints.
- Update `PROJECT_STATE.md` when project phase, version, risks, or next work changes.
- Update `PROJECT_BRAIN.md` when a durable belief, boundary, or decision changes.

## Duplication Rule

Short summaries are allowed in orientation files. Detailed ownership belongs in the primary document.

This prevents Forge from becoming a set of well-written documents that slowly disagree with each other.
