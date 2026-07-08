# Forge Capability Specifications

Forge Capability Specifications define permanent platform capabilities before they are implemented.

An FCS is not an engineering brief. It describes what Forge must be able to do, why it exists, what inputs it uses, what workflow it follows, what deliverables it produces, and how implementation readiness is judged.

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
