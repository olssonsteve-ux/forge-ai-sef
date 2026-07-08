# Contracts

This directory defines Forge document contracts.

Contracts describe the expected structure, ownership, and update rules for files that Forge depends on. They are written as documentation first so future tooling can be implemented against stable behavior.

## Contract Rules

- A contract must name the file or behavior it governs.
- A contract must define required sections.
- A contract must define update triggers.
- A contract must define ownership.
- A contract must avoid implementation details unless they are required for future compatibility.

## Current Contracts

- `project-state-schema.md`
- `project-brain-schema.md`
- `ai-handoff-schema.md`
- `adr-lifecycle.md`
- `bootstrap-template-system.md`
- `forge-init-spec.md`
