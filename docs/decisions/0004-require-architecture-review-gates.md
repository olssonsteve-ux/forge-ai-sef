# 0004 - Require Architecture Review Gates

Date: 2026-07-08

## Status

Accepted

## Context

Forge is intended to become the foundation for future software projects. If implementation begins without explicit architecture review gates, the framework may accumulate automation before its contracts are stable.

The initial foundation established architecture direction, but the requirement to review that direction before implementation was implicit.

## Decision

Forge will require explicit architecture review gates before major implementation milestones.

At minimum, an architecture review is required before:

- first production code
- first CLI command
- first bootstrap behavior
- first standards validation behavior
- first release-management automation

Each review should document:

- scope
- findings
- risks
- score or readiness assessment
- required changes before implementation

## Consequences

- Forge keeps human architectural accountability visible.
- Implementation may move slower, but with less drift.
- Review documents become part of project memory.
- Future automation must be justified by accepted contracts.
