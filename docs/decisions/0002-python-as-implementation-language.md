# 0002 - Python As Implementation Language

Date: 2026-07-08

## Status

Accepted

## Context

Forge will eventually need developer tooling for project bootstrap, file generation, validation, AI context preparation, Git workflow support, and release management.

These responsibilities are mostly local automation and document orchestration rather than high-throughput runtime behavior.

## Decision

Python is the expected implementation language for Forge when implementation begins.

## Rationale

Python is a strong fit because it provides:

- readable automation
- broad standard library support
- cross-platform file handling
- mature testing tools
- strong markdown and structured-data ecosystem
- simple packaging options
- good ergonomics for AI-assisted development

## Consequences

- Future implementation should reserve `forge/` for Python package code.
- Python packaging decisions are deferred until implementation begins.
- Non-Python adapters remain possible later if a clear need appears.
