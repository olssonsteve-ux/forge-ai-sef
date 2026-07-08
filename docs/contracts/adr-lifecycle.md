# ADR Lifecycle

Forge uses Architecture Decision Records under `docs/decisions/`.

ADRs preserve durable decisions that affect architecture, governance, implementation constraints, repository structure, standards, templates, automation, or release behavior.

## Naming

ADR files use this format:

```text
NNNN-short-kebab-case-title.md
```

Rules:

- `NNNN` is a zero-padded sequential number.
- Numbers are never reused.
- Titles use lowercase kebab case.
- File names should be stable after acceptance.

Example:

```text
0005-project-memory-contracts.md
```

## Required Sections

Each ADR must include:

- title
- date
- status
- context
- decision
- consequences

Optional sections:

- alternatives considered
- migration notes
- review date
- related documents

## Status Values

### Proposed

The decision is being considered but is not yet binding.

### Accepted

The decision is active and should guide future work.

### Superseded

The decision has been replaced by a newer ADR.

Superseded ADRs must link to the replacement ADR.

### Deprecated

The decision is no longer recommended but has not been fully replaced.

### Rejected

The decision was considered and explicitly not adopted.

## Lifecycle

1. Create an ADR as `Proposed` when a meaningful decision needs review.
2. Update the ADR during discussion.
3. Mark it `Accepted` when it becomes binding.
4. If direction changes, create a new ADR and mark the old one `Superseded` or `Deprecated`.
5. Do not rewrite accepted history except for spelling, broken links, or formatting.

## When An ADR Is Required

Create an ADR for:

- implementation language decisions
- CLI framework decisions
- project memory contracts
- repository structure changes
- bootstrap behavior
- standards governance
- template governance
- release policy
- automation that changes files
- irreversible or hard-to-reverse workflow choices

An ADR is not required for:

- typo fixes
- formatting-only changes
- routine documentation clarification
- adding examples that do not change meaning
