# 0003 - Defer CLI Implementation

Date: 2026-07-08

## Status

Accepted

## Context

Forge will likely need a CLI, but the command contract is not defined yet.

Introducing a CLI immediately would force premature decisions about command names, arguments, configuration, dependencies, and behavior.

## Decision

Forge will not implement a CLI in `0.1`.

The project will defer CLI implementation until after project memory, template, standards, and bootstrap contracts are better understood.

## Typer Position

Typer is a strong candidate for the future CLI because it is ergonomic, type-hint-friendly, and well-suited to Python developer tools.

However, Typer should not be added until Forge has a real command set to evaluate.

## Consequences

- No CLI package is added now.
- No Typer dependency is added now.
- CLI design should be revisited around `0.5`.
