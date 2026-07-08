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
| Forge capabilities | `docs/capabilities/` | `docs/decisions/0010-forge-capability-specifications.md` |
| Capability Slices | `docs/standards/capability-slice-standard.md` | `templates/capability-slices/CS-template.md`, `docs/architecture/AR-0001-Engineering-Hierarchy.md`, `docs/decisions/0014-introduce-capability-slices.md` |
| Document contracts | `docs/contracts/` | `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, `AI_HANDOFF.md` |
| Bootstrap template system | `docs/contracts/bootstrap-template-system.md` | `templates/`, `docs/decisions/0009-template-driven-bootstrap-generation.md` |
| First CLI behavior | `docs/contracts/forge-init-spec.md` | `ROADMAP.md`, `docs/decisions/0008-specify-forge-init-before-implementation.md` |
| Version roadmap | `ROADMAP.md` | `README.md` |
| Current project state | `PROJECT_STATE.md` | `AI_HANDOFF.md` |
| Durable project memory | `PROJECT_BRAIN.md` | `AI_HANDOFF.md` |
| AI contributor instructions | `AI_HANDOFF.md` | `PROJECT_STATE.md`, `PROJECT_BRAIN.md` |
| Architectural decisions | `docs/decisions/` | architecture documents |
| Constitutional decision record | `docs/decisions/0011-forge-constitutional-governance-and-product-identity.md` | `CONSTITUTION.md` |
| Standards | `standards/README.md` | future standards files |
| Templates | `templates/README.md` | future template files |

## Update Rules

- Update the primary document when a concept changes.
- Update supporting documents only when their summary would become misleading.
- Add an ADR for durable architecture decisions, governance changes, or implementation constraints.
- Update `PROJECT_STATE.md` when project phase, version, risks, or next work changes.
- Update `PROJECT_BRAIN.md` when a durable belief, boundary, or decision changes.

## Duplication Rule

Short summaries are allowed in orientation files. Detailed ownership belongs in the primary document.

This prevents Forge from becoming a set of well-written documents that slowly disagree with each other.
