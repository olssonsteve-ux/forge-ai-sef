# HD-FAL-010 — Authorize EB-006 Second Residual Assurance Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Design Authority

Provenance: Explicit user authorization in the Codex task titled
`HD-FAL-010 — Authorize EB-006 Second Residual Assurance Correction`.

Review baseline: branch `main`, commit
`ea83a81504309b214f15056456dd646ad2b1bbd5` (`docs(forge): complete EB-006 assurance correction`),
clean working tree and empty staging area.

Review verdict: `NOT READY FOR IMPLEMENTATION AUTHORIZATION`.

Governance recommendation: `Return EB-006 for another bounded correction`.

Addresses: `EB006-IR2-01` through `EB006-IR2-07` and the corresponding residual portions of
`EB006-R1` through `EB006-R3` and `EB006-FR-01` through `EB006-FR-06`.

## Context

The fresh independent read-only Standard-Assurance review found that revised EB-006 still leaves
material choices in nested boundary structures, literal fixtures, reviewer provenance, correction
request persistence, terminal corruption, authority-conflict card recovery and collector
representations. Historical findings remained only partially addressed except `EB006-FR-07`, which
the review assessed as verified addressed.

FAL-002 remains unimplemented and `NOT AUTHORIZED`. FAL-001 remains permanently `TERMINATED
BLOCKED`, unaccepted and unclosed, with correction count 2/2.

## Review trigger and evidence

This decision follows the review completed against `ea83a81`, which reported:

- six new blocking findings, `EB006-IR2-01` through `EB006-IR2-06`;
- one material non-blocking finding, `EB006-IR2-07`;
- partial resolution of `EB006-R1` through `EB006-R3` and `EB006-FR-01` through `EB006-FR-06`;
- verified budget reconciliation for `EB006-FR-07`; and
- clean repository/documentation verification with the known non-blocking version warning.

Evidence considered includes EB-006, the approved FAL-002 specification, `HD-FAL-006` through
`HD-FAL-009`, the independent review, relevant architecture/measurement material, governance and
lifecycle authority, and current project memory.

## Decision

Authorize one further strictly bounded documentation correction of EB-006 solely to address
`EB006-IR2-01` through `EB006-IR2-07` and their corresponding unresolved historical findings.

This is documentation-correction authority only. It is not Implementation Authorization, review
approval, finding verification, finding closure or self-certification. The decision record and
governance registration must be committed separately before correction begins.

## Authorized scope

Correction may modify only:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`; and
- `docs/README.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md` only as needed to
  register this decision, correction state and subsequent independent-review requirement.

The FAL-002 capability specification is not an authorized change surface. A required specification
change stops correction for a new higher-order Human Decision.

## Explicit exclusions

This authority excludes production/runtime/test implementation; actual schemas or fixtures;
implemented collectors, adapters or persistence structures; new dependencies; version changes;
Audio Recorder code; FAL-001 runtime, history or correction count; capability scope expansion;
Implementation Authorization; release, packaging or distribution; and finding closure or
self-certification.

No other path or change is implicitly authorized.

## Correction objectives

### CORR-010-01 — Complete nested canonical models

Define exact fields, types, cardinalities, enums, null/unknown semantics, invariants, references,
serialization, hash participation and schema fragments for every GateRecord payload variant,
including inventory, evidence, initial/correction execution, review, human-decision and closure
bindings. Replace generic RunRecord `parsed:Json` with a command-ID-discriminated parsed-result union.
Define HumanDecision domain enum, allowed choices per domain, selected-choice semantics, target,
resume/closure effect and default prohibition. No “referenced/relevant/corresponding” placeholder may
remain in a canonical contract.

### CORR-010-02 — Truly literal fixtures

For all 19 fixtures and each subcase, define exact initial files and canonical JSON/bytes,
deterministic IDs/hashes/predecessors/sequence/ordinal, operation and mutation, reason code, created
record order and bytes, final state, forbidden files and replay behavior.

A normative fixture generator is permitted only if its complete input vocabulary, primitive values,
timestamps, IDs, hashes, paths and output bytes are deterministic, reconstructable from EB-006 alone
and independent of production constants and logic. Randomness is forbidden unless a single fixed seed
and complete algorithm are specified.

### CORR-010-03 — Verifiable reviewer provenance

Define the authority or collector outside adapter results that issues executor/reviewer identities,
binds roles before invocation, collects provenance and verifies different authorized principals and
fresh observable context. Specify permitted same-process and same-binary behavior and fail closed when
provenance cannot be verified. Self-reported IDs, booleans or context labels cannot prove
independence. If this requires a new authority architecture not already permitted by FAL-002, stop
for a new Human Decision.

### CORR-010-04 — Single correction-request persistence

Use one persistence pattern for initial and correction execution: core creates request; executing
GateRecord embeds it; gate becomes create-only durable; executor is invoked; complete
ExecutorExchange is created and persisted exactly once after result; then core transitions. No
null-result exchange or separate executor-request surface may persist. Synchronize transition,
adapter, fixture and control text.

### CORR-010-05 — Authoritative terminal corruption

Define one authoritative state for interruption after partial write but before durability, compatible
with create-only, no overwrite/delete/truncate, evidence preservation, append-only history and
deterministic paths/IDs. A disposition existing only outside state authority is insufficient. Use no
new persistence architecture unless already authorized; otherwise stop for higher-order authority.

### CORR-010-06 — Exactly one valid authority-conflict card

Ensure every conflict has exactly one schema-valid canonical HumanDecisionRecord after crash/replay.
At every crash point the card must be either wholly absent and safely recreatable under the same ID,
or wholly durable and adoptable—never a partial final canonical file blocking its ID. Define creation,
staging/finalization if authorized, card ID, physical/logical replay, crash-before/during/after-card,
crash-before/after-gate, same-hash duplicate and conflicting duplicate. Use the same durability model
as CORR-010-05.

### CORR-010-07 — Close collector representation gaps

Define offline-precondition authority, source, locator, ID/hash, collection time, freshness, RunRecord
binding and missing-evidence disposition. Define deterministic redaction byte grammar, encoding,
boundaries, delimiters, quotes, escaping, repeated/overlapping values, replacement bytes, hashing
order and stored bytes. Complete the command-discriminated parsed union from CORR-010-01.

## Authority boundaries and recovery consistency

CORR-010-05 and CORR-010-06 are one recovery-design problem. Gate and decision-card writes use the
same durability model unless an existing primary source explicitly requires otherwise. Correction
must not introduce another canonical surface, persistence namespace or authority mechanism without
existing authority.

The FAL2-CC-01 through FAL2-CC-16 mapping must be updated end-to-end with the completed nested models,
literal fixture evidence, external provenance, authoritative crash disposition, valid exactly-once
card and command-specific parsed schemas. Coverage remains subject to independent review and cannot
be self-certified as fully covered.

## Budget guardrail

`HD-FAL-009` remains controlling: approximately 1,660 expected and at most 1,800 new production LOC,
with no new dependencies. This decision changes neither budget nor capability scope. If completed
contracts make the 1,800 envelope materially unrealistic, correction stops and reports
`BUDGET AUTHORITY ESCALATION REQUIRED` before any scope or budget choice.

`EB006-FR-07` remains undisturbed unless the correction itself creates such a budget consequence.

## Finding discipline

This decision closes or verifies no finding. After actual correction, EB-006 may record the seven
IR2 findings and corresponding historical findings only as `ADDRESSED — AWAITING INDEPENDENT REVIEW`.
Only the subsequent independent review may use `VERIFIED ADDRESSED`, `FULLY COVERED` or `READY`.

## Stop and escalation conditions

Stop without local invention if correction requires changing the FAL-002 specification, capability
scope, authority model beyond existing Standard Assurance, budget, dependency policy, production
architecture or any prohibited artifact. Stop also if authoritative partial-write recovery,
independence provenance or valid exactly-once decision-card semantics cannot be expressed within
existing authority.

## Required independent review

After correction and repository verification, conduct a fresh independent read-only
Standard-Assurance review. It must independently re-evaluate all nested canonical contracts, all
literal fixtures/subcases, provenance root, correction persistence, IP-03 authority, partial-card
recovery, collector representations, CC-01 through CC-16 and implementation determinism.

Even a READY recommendation is not implementation authority. Only a separate later Human Decision
may authorize implementation.

## Resulting governance state

- `HD-FAL-010`: `ACCEPTED`.
- EB-006: bounded second residual documentation correction authorized; correction not yet begun.
- FAL-002 implementation: `NOT AUTHORIZED`.
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.
- FAL-002 maximum: 1,800 new production LOC; expected approximately 1,660.
- All findings remain open for independent review.
- Next gate after correction: fresh independent read-only Standard-Assurance review.
