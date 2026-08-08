# HD-FAL-008 — Authorize EB-006 Residual Documentation Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Design Authority

Provenance: Explicit user authorization in the Codex task titled
`HD-FAL-008 — Authorize EB-006 Residual Documentation Correction`.

Review baseline: branch `main`, commit
`c6c23df80d2c417a4728574d654ba439511db88b` (`docs(forge): address EB-006 review residuals`),
clean working tree and empty staging area.

Review verdict: `NOT READY FOR IMPLEMENTATION AUTHORIZATION`.

Governance recommendation: `Return EB-006 for another bounded documentation correction`.

Addresses: `EB006-FR-01` through `EB006-FR-07`.

## Context

The fresh independent read-only Standard-Assurance review found that revised `EB-006` still leaves
boundary-model, state-transition, fixture, adapter, recovery, collector and budget decisions to a
future implementer. `EB006-R1`, `EB006-R2` and `EB006-R3` were independently assessed as only
`PARTIALLY ADDRESSED`. FAL-002 remains unimplemented and `NOT AUTHORIZED`.

## Evidence reviewed

- the fresh independent read-only Standard-Assurance review at the review baseline above;
- `EB-006 — Implement FAL-002 Standard Assurance Bounded Engineering Loop`;
- `HD-FAL-006` and `HD-FAL-007`;
- the approved FAL-002 specification and its normative reuse, assurance, authority, inventory and
  closure constraints;
- current governance indexes and project memory; and
- the preserved FAL-001 disposition and correction history.

## Decision

Authorize one further strictly bounded documentation correction of `EB-006` solely to address
`EB006-FR-01` through `EB006-FR-07`. The corrected brief must undergo a new fresh independent
read-only Standard-Assurance review before Implementation Authorization may be considered.

This decision is authorization for documentation correction only. It is not Implementation
Authorization, finding closure, review acceptance or self-certification.

## Authorized scope

The correction may change only:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`; and
- `docs/README.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md` only as required to
  record this decision, the bounded correction state, continued non-authorization and required
  subsequent independent review.

The decision record and its required governance/project-memory registration are committed
separately before correction of `EB-006` begins.

## Explicit exclusions

This authority excludes changes to the FAL-002 specification; FAL-001 or its history and correction
count; Forge runtime or existing implementations; production or test code; schemas; fixtures;
dependencies; versions; Audio Recorder code; implemented collectors; implemented executor or
reviewer adapters; runtime persistence structures; experiments or implementation changes made to
prove the design; Implementation Authorization; capability closure; release, packaging or
distribution; and closure or verification of any finding by this decision itself.

No other file or change surface is implicitly authorized. If a required correction cannot be made
within this documentation mandate, work stops and a new Human Decision is required.

## Correction objectives

### CORR-008-01 — Canonical boundary contracts

Address `EB006-FR-01` by specifying complete normative contracts for `GateRecord`,
`ExecutorExchange`, `RunRecord`, `ReviewerExchange` and `HumanDecisionRecord`: every field, type,
cardinality, required/optional rule, null/unknown semantics, enum, identity and deterministic-ID
rule, canonical ordering and serialization, hash preimage, cross-field invariant, validation order,
schema version, unknown-version behavior, compatibility and extension policy, and round-trip
expectation. No canonical field metadata may remain future design work.

### CORR-008-02 — Exhaustive state-transition model

Address `EB006-FR-02` with an exhaustive matrix of current state, event, preconditions,
authoritative evidence, allowed actor, created records, next state, failure disposition and
retry/resume behavior. It must cover every normative state and the named draft/ready, executor and
reviewer retry, correction rounds, no-progress, ceiling, conflict, stale/repeated/resumed decision,
technical eligibility versus accepted, human closure and closure-replay paths. Every unlisted
transition is forbidden.

### CORR-008-03 — Literal fixtures and interruption contracts

Address `EB006-FR-03` by turning all 19 scenario fixtures into literal arrange/act/assert contracts
with initial state and files, sequence/ordinal, complete input, stimulus, validation result, created
records and order, deterministic identities/hashes, prohibited records, final state and error or
disposition. Coverage must explicitly include missing tool, timeout, malformed output, invalid
encoding/byte failure, retry/replay, positive corrections, no-progress, correction ceiling,
authority conflict, closure atomicity and partial persistence. All nine interruption points require
exact pre-state, possible bytes, post-state and recovery contracts.

### CORR-008-04 — Adapter lifecycle and reviewer independence

Address `EB006-FR-04` by specifying request creation, input/result persistence, invocation and
transition ownership, invocation identity, same-ID replay, idempotence or non-idempotence, timeout,
interruption, provenance, mutations, retry and stale-data handling for both adapters. Define how a
fresh review context is established and evidenced, how executor/reviewer authority is separated,
and the fail-closed result when separation or provenance cannot be proven. This objective selects no
actual adapter or implementation.

### CORR-008-05 — Complete crash and partial-write recovery

Address `EB006-FR-05` with a complete create-only recovery algorithm for every interruption phase,
including possible files/bytes, authority, preservation, path and ordinal reuse, next ordinal,
recovery record, human intervention, state and replay. It must provide exactly-once or at-most-once
decision-card semantics and guarantee exactly one deterministic authority-conflict card after crash
without overwrite or history rewrite.

### CORR-008-06 — Exact collector contracts

Address `EB006-FR-06` with one complete contract row per collector covering phase, argv, working
directory, environment, network policy, input derivation, timeout and exit codes; stdout, stderr and
raw bytes; decoding and invalid encoding; redaction and stored representation; hash preimage; parser
grammar, ambiguity, malformed/conflicting output, missing executable, timeout/process error;
normalization, record mapping and authority. A network prohibition that cannot be enforced within
the architecture becomes an explicit precondition or escalation condition.

### CORR-008-07 — Bottom-up budget reconciliation

Address `EB006-FR-07` with a bottom-up decomposition for all five planned production modules,
including responsibilities, functions/classes/protocols, collectors/schemas, persistence/recovery,
new and reused LOC, margin and risk. Demonstrate that all requirements realistically fit within the
current plan of at most 1,100 new production LOC and the normative maximum. Demonstrate that stdlib
and existing dependencies suffice without weakening requirements. If the estimate does not fit, do
not change the budget or omit requirements: stop, document the variance and request a separate
scope/budget Human Decision.

## Finding and control mapping

The corrected brief must map `CORR-008-01` through `CORR-008-07` directly to `EB006-FR-01` through
`EB006-FR-07`. This decision does not close or verify `EB006-R1`, `EB006-R2`, `EB006-R3` or any
`EB006-FR-*` finding. The next independent review must assess all ten findings.

The `FAL2-CC-01` through `FAL2-CC-16` coverage matrix must give each control its normative
requirement, canonical contract, implementation mapping, relevant transition/state mapping,
verification mapping, concrete fixture/test and failure disposition. General text or intention is
not full coverage.

## Invariants

- FAL-002 remains `NOT AUTHORIZED`; `EB-006` must not claim otherwise.
- FAL-001 remains permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.
- FAL-001 identity, history, reviews and findings remain unchanged.
- No finding is closed or verified by this decision or by correction self-certification.
- Scope, criteria, authority and the approved FAL-002 specification remain frozen.
- Only a separate subsequent Human Decision may authorize FAL-002 implementation.

## Stop and escalation conditions

Correction stops without local invention if it requires a normative specification change, changed
scope or criteria, architecture/authority choice outside this mandate, budget increase, new
dependency, implementation experiment or any excluded change. An unresolved contradiction,
unrealistic bottom-up estimate or inability to prove reviewer separation also stops for a new Human
Decision.

## Required verification

After correction, run the full repository test suite, Ruff lint, Ruff format check, `git diff
--check`, Forge Project Memory Health/status, version consistency, working-tree and staging checks.
The known `pyproject.toml` `0.5.0` versus release tag `v0.4.1` warning is reported but not corrected.
Passing existing checks verifies documentation/repository health only; it is not FAL-002
implementation evidence.

## Required subsequent review

The corrected EB-006 must receive a new fresh independent read-only Standard-Assurance review with
adversarial instructions. The correction author, EB executor or self-review cannot substitute for
that review. Even a review recommendation of readiness does not authorize implementation.

## Resulting governance state

- `HD-FAL-008`: `ACCEPTED`.
- `EB-006`: bounded documentation correction authorized; artifact correction has not yet begun.
- FAL-002: `NOT AUTHORIZED` and unimplemented.
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.
- `EB006-R1`–`EB006-R3` and `EB006-FR-01`–`EB006-FR-07`: open for independent reassessment.
- Next gate: separately committed EB-006 documentation correction, verification and fresh
  independent read-only Standard-Assurance review.
