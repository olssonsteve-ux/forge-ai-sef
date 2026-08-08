# HD-FAL-013 — Authorize EB-006 Third Residual Assurance Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user authorization in the Codex task titled
`HD-FAL-013 — Authorize EB-006 Third Residual Assurance Correction` against branch `main`, commit
`055db259f72ea8aad4e756e859142df3d698c36e`
(`docs(forge): define FAL-002 recovery-state architecture`), with clean working tree and empty
staging.

Review basis: independent IR3 outcome `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED` with
eight open blocking findings, `EB006-IR3-01` through `EB006-IR3-08`.

Architecture basis: `HD-FAL-012`, which selected deterministic successor state-series segments
forming one logical authoritative lineage and removed the architecture authority gap without
correcting or closing a finding.

## 1. Context

`HD-FAL-011` preserved all eight IR3 findings and blocked further EB-006 correction pending a
recovery/state architecture decision. `HD-FAL-012` supplied that decision for `EB006-IR3-04` and the
recovery-dependent portion of `EB006-IR3-05` while retaining the existing five boundary surfaces,
module/adapter/dependency limits and production budget.

The remaining work is one documentation/planning correction of EB-006. The eight objectives are
interdependent refinements of the same canonical model, evidence, recovery, review and control
contract. They are not eight independent scope expansions.

FAL-002 remains unimplemented and `NOT AUTHORIZED`. FAL-001 remains permanently
`TERMINATED BLOCKED`, unaccepted and unclosed, with correction count 2/2 and unchanged history.

## 2. Governance assessment

All eight findings are correctable within the approved FAL-002 specification, the `HD-FAL-012`
architecture and the current EB-006 planning surface:

| Finding | Assessment | Authorized objective |
| --- | --- | --- |
| `EB006-IR3-01` | EvidenceBinding can be reconciled directly with approved FAL-002 §10. | `CORR-011-01` |
| `EB006-IR3-02` | Competing nested definitions can be replaced by one final canonical model. | `CORR-011-02` |
| `EB006-IR3-03` | A complete independent fixture oracle can be specified in test-planning text. | `CORR-011-03` |
| `EB006-IR3-04` | `HD-FAL-012` now fixes the recovery architecture choice. | `CORR-011-04` |
| `EB006-IR3-05` | Card identity/publication can be bound to the selected recovery lineage. | `CORR-011-05` |
| `EB006-IR3-06` | Collector/runtime fields and offline-decision resolution fit existing boundaries. | `CORR-011-06` |
| `EB006-IR3-07` | Finding lifecycle can use existing review, gate and eligibility records. | `CORR-011-07` |
| `EB006-IR3-08` | No-progress can be defined as a deterministic function over canonical lineage facts. | `CORR-011-08` |

No finding is corrected, verified or closed by this assessment.

## 3. Decision

Authorize exactly one bounded coherent EB-006 documentation correction campaign containing:

- `CORR-011-01`;
- `CORR-011-02`;
- `CORR-011-03`;
- `CORR-011-04`;
- `CORR-011-05`;
- `CORR-011-06`;
- `CORR-011-07`; and
- `CORR-011-08`.

All eight objectives must be completed and committed together in the correction commit. Partial
local completion does not make EB-006 review-ready. The correction agent may record interim work in
the working tree but may not claim partial verification, PASS or closure.

## 4. Authorized correction objectives

### `CORR-011-01` — Complete criterion EvidenceBinding

Address `EB006-IR3-01`. Reconcile EB-006 with approved FAL-002 §10 by defining `evidence_kind` and
`assertion` together with exact types, enums, normalization, canonical serialization, hash
participation, schema generation/validation, reviewer packet/result use and positive/negative
fixture cases. No competing evidence model is authorized.

Completion requires every criterion binding to represent the complete approved field set and for
wrong/missing kind, assertion, source, locator, hash or provenance to fail closed deterministically.

### `CORR-011-02` — Reconcile final nested canonical models

Address `EB006-IR3-02`. Define one complete final `ExecutorExchange.invocation` and one complete
final `ReviewerExchange.reviewer_execution`, including the `HD-FAL-010` Forge-owned grant and
observed-invocation provenance. Explicitly supersede every incompatible legacy exact form.

Define one closure decision representation and one unambiguous domain/discriminator rule using the
already authorized HumanDecisionRecord surface. Completion requires that an implementer and schema
generator need make no unstated field, presence, hash or discriminator choice.

### `CORR-011-03` — Make the fixture oracle independently reproducible

Address `EB006-IR3-03`. Specify either literal expected fixtures/hashes or a complete normative
test-only generator independent of production constants and logic. Define every primitive and nested
field, record order, mutation JSON pointer/location and value, canonical byte output, expected hash,
failure code, final filesystem/state and replay result for every fixture and subcase.

Completion requires two independent test authors using only EB-006 to produce byte-identical
expectations. Production code and generated runtime schemas may not generate their own oracle.

### `CORR-011-04` — Incorporate authoritative recovery lineage

Address `EB006-IR3-04` by implementing `HD-FAL-012` normatively inside EB-006 without choosing a
different architecture. Define obstruction detection, descriptor, predecessor sealing, UUIDv5
successor identity, recovery ordinal, logical lineage, exact `RECOVERY_ROOT` GateRecord, sequence-zero
semantics, carried state, construction/validation/publication authority, authority-transition point,
crash/replay, collision handling, discovery, terminal state and human-only continuation.

Completion requires every stable occupied/invalid canonical final-path condition inside the approved
filesystem threat model to produce exactly one deterministically discoverable authoritative
`awaiting_human` continuation or the explicitly bounded external-repair stop for an unwritable
series root.

### `CORR-011-05` — Complete conflict-card identity and publication

Address `EB006-IR3-05`. Define the exact canonical source-array shape, ordering and hash preimage;
deterministic card ID; relationship to the active recovery root; occupied/invalid card-path handling;
orphan/conflicting-card treatment; crash/replay behavior; and invocation of the `HD-FAL-012`
successor mechanism when card publication is obstructed.

Completion requires exactly one card to be authoritative for human resolution through the selected
lineage. Cards remain HumanDecisionRecords and never become state authority. No alternate identity
outside the `HD-FAL-012` derivation is permitted.

### `CORR-011-06` — Complete collector/runtime and offline evidence

Address `EB006-IR3-06`. Define collector-owned runtime and tool-version fields, placement, parsers,
normalization, validation and unsupported/missing-version behavior. Define offline-evidence lookup to
an accepted HumanDecisionRecord, locator grammar and resolution, canonical hash/preimage binding,
freshness and exact fail-closed reason codes.

Completion requires RunRecord and the evidence contract to represent every approved FAL-002 §10
collector fact without actor prose or an unresolved authority claim.

### `CORR-011-07` — Define cross-review finding lifecycle

Address `EB006-IR3-07`. Define deterministic finding identity, introduction, canonical ordering,
carry-forward across the full logical lineage, lifecycle states, permitted transitions and authority,
reviewer disposition versus human closure, duplicate and supersession behavior, hashing and complete-
lineage unresolved-finding discovery.

Completion requires PASS and eligibility to scan every unresolved historical finding. An omitted or
empty later reviewer findings array cannot erase a prior blocker. Executor, correction agent and
reviewer receive no human closure authority.

### `CORR-011-08` — Define exact no-progress function

Address `EB006-IR3-08`. Define the complete comparison input, canonical diff/evidence hashes,
prior/current window, finding-set identity/equivalence, boolean combination, material-improvement
rule, newly introduced finding behavior, correction-ceiling precedence and exact output/disposition.

Completion requires two conforming implementations presented with the same verified logical lineage
to reach the same progress and stop result.

## 5. Cross-correction consistency

The correction must define one coherent model and test plan. At minimum:

- EvidenceBinding fields and collector-owned values must agree with reviewer packet/result models.
- Finding lifecycle identity must be used by recovery carry-forward, eligibility and no-progress.
- Recovery carry-forward must preserve the complete-series correction count and maximum ordinal.
- Conflict cards must bind to the exact active recovery root but never establish state authority.
- The independent fixture oracle must cover every final canonical model and every recovery/card
  crash path.
- Invocation provenance must use only the final exchange containers.
- Supersession clauses must remove, not layer over, contradictory earlier exact definitions.

If consistency requires a change to the approved FAL-002 capability specification, the correction
must stop and report `SPECIFICATION AUTHORITY REQUIRED`. This decision authorizes no capability-
specification change.

## 6. Architecture and scope constraints

The correction must implement, not reopen, `HD-FAL-012`. It may not introduce:

- a sixth top-level boundary surface;
- a global mutable state/series pointer;
- another semantic state authority outside GateRecord;
- another recovery authority or competing conflict-card authority;
- generalized external transactions, consensus, database or lock infrastructure;
- another executor, reviewer or collector role;
- a new module, adapter or dependency without separate authority; or
- reset of frozen scope, criteria, correction count, ordinal, finding history or pending decisions.

Discovery remains deterministic from the original manifest lineage. Recovery root remains
`awaiting_human`; only an accepted HumanDecisionRecord may later authorize resume or abandonment.

If the selected architecture cannot be expressed under these constraints, stop and report
`ARCHITECTURE AUTHORITY REQUIRED` rather than inventing a substitute.

## 7. Authorized change surface

The correction may modify only:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`; and
- `docs/README.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md` only as required to
  record correction state, evidence and the next independent-review gate.

No other path is implicitly authorized. In particular, the correction may not modify Forge runtime,
tests, committed schemas, committed fixtures, dependencies, versions, Audio Recorder, the approved
FAL-002 specification, FAL-001 artifacts, unrelated architecture or another capability.

## 8. Budget disposition

`HD-FAL-009` remains controlling:

- expected production implementation: approximately 1,660 LOC;
- hard maximum: 1,800 LOC;
- current margin: 140 LOC;
- production modules: 5 of 8 planned;
- executor adapters: 1;
- reviewer adapters: 1;
- schema surfaces: 5 of 6; and
- new dependencies: 0.

`EB006-FR-07` is not reopened. `HD-FAL-012` classified the selected recovery architecture as bounded
within this envelope. CORR-011 must reconcile EB-006's bottom-up allocation with the selected
architecture without increasing the maximum. Concrete evidence that the design cannot remain at or
below 1,800 LOC requires an immediate stop and `BUDGET AUTHORITY REQUIRED`.

## 9. Completion and finding discipline

CORR-011 is complete only when:

1. all eight objectives are materially incorporated in EB-006;
2. `HD-FAL-012` is represented without architectural deviation;
3. no contradictory final exact models remain;
4. all approved FAL-002 boundary fields are represented;
5. fixture expectations are independently reproducible;
6. recovery is total within the approved threat model;
7. conflict-card identity/publication is deterministic and subordinate to GateRecord authority;
8. unresolved findings survive the complete review/recovery lineage until a permitted disposition;
9. no-progress is one exact deterministic function;
10. the bottom-up plan remains within the 1,800-LOC hard maximum;
11. no unauthorized artifact is changed;
12. repository tests, lint, format, diff check and Project Memory Health pass;
13. each IR3 finding is recorded only as `ADDRESSED — AWAITING INDEPENDENT REVIEW`; and
14. the next gate is a fresh independent read-only Standard-Assurance Review.

The correction agent may not use `VERIFIED`, `CLOSED`, `ACCEPTED`, `PASS`, `FULLY COVERED` or
`IMPLEMENTATION READY` for any IR3 finding. Correction completion is not review approval.

## 10. Stop conditions

Stop before further correction if work requires changed capability scope/criteria, a FAL-002
specification edit, architecture deviation, another surface/authority/role, new dependency, budget
increase, implementation experiments or any path outside section 7. Preserve completed documentation
work without claiming completion and request the missing Human Decision.

## 11. Required independent review

After the correction is committed separately, perform a fresh independent read-only
Standard-Assurance Review against its exact baseline. It must reassess all eight IR3 findings,
cross-contract consistency, the complete canonical model, the independent fixture oracle, recovery
lineage/card crash paths, collector/offline evidence, finding lifecycle, no-progress, scope and budget.

Even a review PASS is not Implementation Authorization. A later separate Human Decision must decide
whether FAL-002 implementation may begin.

## 12. Explicit exclusions

This decision does not implement CORR-011 or FAL-002; modify EB-006; verify, resolve or close a
finding; certify review readiness; authorize implementation; accept residual risk; change FAL-001;
or authorize release, packaging, distribution, publication, push, tag or merge.

## 13. Resulting governance state

- `HD-FAL-013`: `ACCEPTED`.
- `CORR-011-01` through `CORR-011-08`: `AUTHORIZED — NOT STARTED` as one bounded campaign.
- `EB006-IR3-01` through `EB006-IR3-08`: open; none independently verified or closed.
- EB-006: correction authorized; substantive document unchanged by this decision.
- `HD-FAL-012`: binding recovery/state architecture; not reopened.
- FAL-002 implementation: `NOT AUTHORIZED`.
- FAL-002 budget: approximately 1,660 expected / 1,800 maximum new production LOC.
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.
- Next gate: execute the bounded CORR-011 documentation correction in a separate commit, then conduct
  a fresh independent read-only Standard-Assurance Review.
