# Forge Concept v1.0

Status: frozen concept baseline, 2026-10-11, by explicit project-owner instruction.
Implementation status: public testing candidate; stable implementation acceptance remains blocked.

## Purpose and authority

The [statement of intent](../INTENT.md) defines the public purpose. The
[Constitution](../CONSTITUTION.md) remains governing authority. ADR 0018 defines proportionate
records and persistent authorization; ADR 0019 defines the initial isolated-task implementation.

The owner authorized committing and pushing the existing Forge work, opening this repository
for public testing and using the MIT License. This supersedes earlier no-commit/no-publication
instructions for this Forge publication only. It does not publish Audio Recorder, close FAL work
or certify the runtime as stable.

## Frozen v1 scope

1. Explicit purpose, requirements, boundaries and acceptance evidence before implementation.
2. Repository-based memory that preserves decisions and continuity across sessions.
3. Persistent authorization for ordinary work within an agreed scope.
4. Isolated, bounded agent changes with explicit project verification.
5. Independent review that can reject an implementation even when its tests pass.
6. Visible failure, recoverable interruption and explicit application of verified changes.
7. One evidence owner per work item and proportionate documentation.
8. Human authority for consequential decisions and truthful release claims.

The initial command contract covers init, status, verify and task create/show/run/resume/apply.
Task specifications and verification configuration use schema version 1. Existing repositories
are preserved; init is for new projects. The detailed implementation contract remains in the
[assurance record](engineering/Forge-1.0-assurance.md).

## Boundaries

The concept is intended to support evolving agents and models. This candidate contains one
Codex CLI adapter. It does not promise support for all providers, platforms or CLI versions.
It does not provide a hosted service, automatic release, unrestricted autonomous correction,
automatic migration or a multi-file transactional apply guarantee.

Historical FAL-001 and FAL-002 experiments remain outside installed package code. Their findings
and lifecycle dispositions remain intact. Neither concept freeze nor public access accepts them.

## Change and acceptance

The concept baseline is a reference, not a ban on fixes or learning. Clarifications and defects
should be addressed with proportionate evidence. A material change to purpose, authority or
scope requires a recorded decision explaining compatibility and consequences.

Stable implementation 1.0 still requires successful real execution, verification, fresh read-only
review and apply, permission-boundary evidence, the bounded Audio Recorder maintenance trial,
and independent release acceptance. V1-Q-01 remains open.

The public candidate uses package version 1.0.0rc1 and Git tag v1.0.0-rc.1.
There is no stable v1.0.0 implementation tag in this publication.
