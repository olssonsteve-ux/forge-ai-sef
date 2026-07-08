# Forge Capability Specifications

Forge Capability Specifications define permanent platform capabilities before they are implemented.

An FCS is not an engineering brief. It describes what Forge must be able to do, why it exists, what inputs it uses, what workflow it follows, what deliverables it produces, and how implementation readiness is judged.

Large capabilities should be decomposed through Capability Slices before Engineering Briefs. A Capability Slice defines a coherent implementation-sized increment of an accepted FCS without replacing the FCS or the Engineering Brief.

Capability Slices are governed by `docs/standards/capability-slice-standard.md`.

## Accepted Capability Specifications

- `FCS-001-Review.md` - Review Capability.
- `FCS-002-Governance-Runtime.md` - Governance Runtime.

## Capability Slices

- `CS-002.1-Governance-Runtime-Status-Service.md` - first Governance Runtime slice; defines read-only status evaluation for the future `forge status` command.

## Naming

Capability specifications use this format:

```text
FCS-NNN-Capability-Name.md
```

Example:

```text
FCS-001-Review.md
```

## Rules

- Each FCS must be durable and implementation-independent.
- Each FCS must define acceptance criteria.
- Each FCS must identify risks and future extensions.
- Implementation may begin only after the relevant FCS is accepted.
- Changes to accepted capability behavior require an ADR when they alter architecture, workflow, scoring, or deliverables.
- Large or multi-service capabilities should identify Capability Slices before implementation briefs are written.
