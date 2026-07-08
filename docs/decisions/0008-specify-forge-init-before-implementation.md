# 0008 - Specify Forge Init Before Implementation

Date: 2026-07-08

## Status

Accepted

## Context

The first likely CLI command is `forge init <project-name>`. Implementing it before specifying behavior would risk accidental destructive behavior, unclear generated output, and weak validation.

## Decision

Forge will specify `forge init <project-name>` before implementing it.

The pre-implementation specification lives in `docs/contracts/forge-init-spec.md`.

The first implementation must support conservative creation behavior and dry-run behavior. It must not overwrite non-empty directories by default.

## Consequences

- The first CLI command has a reviewable contract.
- Destructive behavior is explicitly deferred.
- Generated project structure must follow accepted documentation and template contracts.
- Implementation readiness can be assessed before code exists.
