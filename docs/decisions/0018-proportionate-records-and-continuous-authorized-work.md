# ADR 0018 — Proportionate records and continuous authorized work

Date: 2026-10-11
Status: Accepted for the documentation workflow under the owner's explicit 2026-10-10 request to streamline Forge and autonomously resolve problems while finishing Audio Recorder. Independent consistency review passed on 2026-10-11; see IR-FAL-004 for this documentation assessment, separate from the failing FAL runtime verdict.

## Context

Audio Recorder already adopted a proportionate two-mode model in GD-0001. Forge's current history repeats the same lifecycle summaries and test claims in several memory files and correction handoffs. The owner now explicitly requests less administration, continued problem solving without repetitive questions, and delivery of the actual application including album authoring/export.

## Decision

Keep the constitutional hierarchy, specification-before-code, architecture decisions, independent review, evidence and explicit release authority. Reduce duplicate record-keeping rather than lowering those boundaries:

- One linked assurance record owns a work item's scope, plan, tests, findings, corrections and review disposition unless its governing contract explicitly requires separate records.
- PROJECT_STATE owns current status and next gate. PROJECT_BRAIN owns durable rationale. AI_HANDOFF links these; it need not restate all of their history. Existing required headings and memory schemas remain.
- Explicit authorization persists through ordinary in-scope work and repair. An agent should act on it rather than seek the same approval after each edit, test failure or bounded correction.
- Escalate only concrete missing authority, scope/architecture/dependency changes, destructive/irreversible actions or an explicit contractual STOP boundary. Do not invent approval requirements from optional artifact templates.
- Run appropriate checks once per relevant baseline; repeat after changes or unresolved failures. Preserve provenance and distinguish automated, opt-in, manual and unavailable verification.
- Preserve old findings and decisions; verification is not human closure and implementation is not release.

## Boundaries and compatibility

This is documentation guidance, not a new runtime profile, FAL, adapter, schema, surface or dependency. It does not alter FAL-002, EB-006, HD-FAL-021/022/023, correction counters, LOC ceilings, STOP #9/#13 or human-only closure. The FAL-002 review/correction contract remains binding. No release/tag/push or commit is authorized here. Bootstrap templates remain unchanged because their versioned output contract is separate.

Existing review records remain authoritative for their baseline. Each memory document links this decision without rewriting its historical outcomes. Conduct, AI Implementation Protocol and Lifecycle Standard carry the same consolidation rule.

## Validation and trade-off

Check cross-document consistency and required memory headings/links. Independent review must confirm no authority gate or runtime contract was weakened. A smaller record is easier to maintain but must still identify scope, role, date, evidence, decision and unresolved limitations. Audio Recorder's FCS-002 consolidated record is the concrete application of this approach; no measured productivity improvement is claimed yet.
