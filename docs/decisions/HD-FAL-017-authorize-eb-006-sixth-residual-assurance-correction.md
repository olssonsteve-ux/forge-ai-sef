# HD-FAL-017 — Authorize EB-006 Sixth Residual Assurance Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task titled
`HD-FAL-017 — Authorize EB-006 Sixth Residual Assurance Correction` against branch `main`, commit
`3d06f906217e2e7bcb0221fba523a0d12a231ac2`
(`docs(forge): complete EB-006 fifth residual correction`), with clean working tree and empty
staging. The task supplies the complete Independent Standard-Assurance Review IR6 evidence and
requires this decision only if its two residual findings are correction-ready.

Review basis: Independent Standard-Assurance Review IR6 of EB-006 at the exact baseline above. Its
canonical outcome is `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`. IR6 verified
`CORR-013-03`/`EB006-IR5-03` and `CORR-013-04`/`EB006-IR5-04`, partially verified
`CORR-013-02`/`EB006-IR5-02`, did not verify `CORR-013-01`/`EB006-IR5-01`, and recorded exactly two
open blocking residual findings: `EB006-IR6-01` and `EB006-IR6-02`.

Architecture basis: `HD-FAL-012` and `HD-FAL-014` remain binding. This decision preserves the
five-surface model, PUBLICATION_INTENT, pointer-free recovery discovery, RECOVERY_ROOT, logical-
lineage continuity and GateRecord state authority.

## 1. Verified baseline and current state

Before substantive work, the repository baseline was verified as:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `3d06f906217e2e7bcb0221fba523a0d12a231ac2`;
- commit subject: `docs(forge): complete EB-006 fifth residual correction`;
- working tree: clean; and
- staging: empty.

Current governance state at this decision:

- `HD-FAL-012`, `HD-FAL-014` and `HD-FAL-016`: `ACCEPTED`;
- IR6 outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`;
- `EB006-IR6-01` and `EB006-IR6-02`: open and blocking;
- no finding is closed;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 2. Governance and architecture assessment

Repository and IR6 evidence confirm that both residual findings are correction-ready inside the
approved FAL-002 specification, the existing EB-006 implementation-planning authority and the
binding `HD-FAL-012`/`HD-FAL-014` architecture.

The correction requires no new architecture decision, scope, criteria, boundary surface, state or
recovery authority, role, module, adapter, dependency or budget. `EB006-IR6-01` separates stable
semantic answer evidence from relocatable pending-card representation inside the existing decision
model. `EB006-IR6-02` makes the existing independent fixture oracle faithfully instantiate the
already selected lineage, finding and recovery models.

If execution discovers that either objective requires changing the frozen contracts in section 8,
the correction must stop for governance rather than invent authority.

## 3. Finding disposition and authorization mapping

| Finding | Governance disposition | Authorized objective |
| --- | --- | --- |
| `EB006-IR6-01` | correction-ready within existing decision, HumanDecisionRecord and GateRecord authority | `CORR-014-01` |
| `EB006-IR6-02` | correction-ready within existing fixture/test-planning authority | `CORR-014-02` |

This decision changes no finding status. Both findings remain open and blocking. It verifies,
resolves and closes no finding.

## 4. Decision

Authorize exactly one tightly bounded, coherent EB-006 documentation/planning correction campaign:

- `CORR-014-01` → `EB006-IR6-01`; and
- `CORR-014-02` → `EB006-IR6-02`.

Both objectives must be completed and committed together. A correction agent may later claim at
most `ADDRESSED — AWAITING INDEPENDENT REVIEW`; it may not claim VERIFIED, CLOSED, PASS,
Implementation Authorization or partial readiness.

## 5. CORR-014-01 — Stable semantic answer through physical relocation

Correct the final §46 decision model so `DecisionResolution` binds the stable semantic
DecisionRequirement and human answer independently of a physically relocatable pending-card record
hash.

The corrected model must distinguish:

1. stable semantic answer binding: decision identity, requirement/question hash, selected answer,
   rationale, human authority/provenance and decision time; and
2. current physical publication binding: active pending-card and resolution IDs, locators, hashes,
   binding generation and lineage.

If the answered card is evidenced, the model must distinguish an immutable original answered-card
reference from the current physical pending-card binding. A relocation must not require a second
human answer or change the semantic resolution hash merely because P0 and P1 have different record
hashes.

DecisionResolution remains a HumanDecisionRecord and never becomes state authority.
DecisionApplication remains the GateRecord-owned state effect.

## 6. CORR-014-01 resolver and conflict requirements

The complete-lineage resolver must separately validate:

- semantic correctness against the stable DecisionRequirement; and
- physical validity of the current active-lineage pending/resolution binding.

It must produce one result for ordinary publication, pending-card rebinding, resolution relocation,
byte-identical replay and the same semantic answer with permitted physical metadata changes. A
different semantic answer for the same decision identity is `AUTHORITY_CONFLICT`. Stale, inactive
and orphan resolutions remain non-authoritative evidence.

Offline authority must use this same resolver at origin, recovery-1 and recovery-N. A pending card
alone or an accepted-looking record outside the active lineage cannot authorize execution.

Required fixtures cover P0/R0, P0 obstruction and P1, R0 obstruction and R1, unequal P0/P1 physical
hashes with stable semantic answer, replay, conflicting answer, stale/orphan resolution and offline
authority after both pending and resolution relocation.

## 7. CORR-014-02 — Total lineage-aware independent oracle

Correct final §48 directly. The normative independent oracle must be executable, total, stdlib-only
and independent of production canonicalization, hashes, schemas, validation, recovery, resolver and
finding-fold implementations.

It must provide executable normative definitions for `replace`, `add`, `remove`, raw-byte/VFS
mutation, `REHASH` and `NO_REHASH`, including exact JSON Pointer traversal, object/array behavior,
invalid pointers, missing parents, absent removal targets, canonical reserialization and hash
recalculation order.

Every fixture row must explicitly construct every local value and its initial object/VFS state.
No ambient `fs`, `key`, `root1`, `binding0`, `application0` or equivalent implicit value is allowed.
Each row records constructor inputs, ordered mutations, expected object/filesystem and exact
disposition.

## 8. Lineage-aware constructor requirements

The test-only oracle may define an `OracleLineageState` or equivalent in-memory structure. It is not
a runtime surface or authority. It must carry all predecessor-derived inputs needed by fixture
constructors, including active gate/chain, global finding events, checkpoint, maximum prior ordinal,
decisions, runs/reviews, correction/progress state and VFS.

The corrected constructors must:

- make CONTROL append its delta to complete predecessor history, validate the next global ordinal
  and recompute the full checkpoint;
- make RECOVERY_ROOT carry the actual predecessor checkpoint, maximum ordinal, decisions,
  applications, progress and correction count without reset;
- make `review_event` bind the actual reviewed RunRecord, including ordinal and recovery segment;
- make decision fixtures use the corrected stable semantic answer model; and
- give every filesystem case its own exact initial VFS, paths, bytes and operation order.

Minimum oracle executions are:

1. MANIFEST → finding event 0 → remediation event 1 → verification event 2, checkpoint count 3;
2. MANIFEST → event 0 → event 1 → RECOVERY_ROOT, checkpoint count retained at 2;
3. run/review/event 0 binds run 0 and run/review/event 1 binds run 1;
4. D → P0 → answer A → P1/recovery → same semantic A → DecisionApplication; and
5. one complete negative JSON mutation with exact base, pointer, operation, value, rehash mode and
   validation result.

## 9. Frozen verified contracts

CORR-014 must preserve unchanged:

- `CJ`, `CF`, `H` and `HB`;
- PUBLICATION_INTENT, `recovery_condition_hash`, `recovery_discovery_key`, pointer-free UUIDv5
  probing, RECOVERY_ROOT and one logical lineage;
- GateRecord-carried FindingEvent, RemediationEvidence and FindingCheckpoint;
- restart reconstruction and current-finding-state derivation;
- severity order, human reclassification epochs and conservative blocking latch;
- PASS, no-progress and correction-ceiling semantics;
- GateRecord as sole state authority; and
- exactly five external/persisted surfaces.

No change to these contracts is authorized. A concrete contradiction requiring one must stop the
campaign for a new governance decision.

## 10. Consolidation strategy

Correct §§46 and 48 directly and leave §§44–50 as the single obvious final normative layer. Do not
append another avoidable precedence overlay. Preserve historical traceability without restoring a
superseded model to normative force.

## 11. Authorized change surface

The correction may modify only:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`; and
- `docs/README.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md` only when required to
  record correction state, verification evidence and the IR7 handoff.

It may not modify the FAL-002 specification, runtime/production code, tests, runtime schemas,
committed fixtures, dependencies, versions, Audio Recorder, FAL-001 or unrelated artifacts.

No new surface, module, adapter, dependency, role, authority or mutable pointer is authorized.

## 12. Budget disposition

`HD-FAL-009` remains controlling:

- expected production implementation: approximately 1,660 LOC;
- hard maximum: 1,800 LOC;
- margin: 140 LOC;
- production modules: 4;
- adapters: 2;
- schema surfaces: 5; and
- new dependencies: zero.

This decision changes no budget and does not reopen `EB006-FR-07`. Concrete evidence that the
corrected design structurally exceeds the limit requires `BUDGET AUTHORITY REQUIRED`.

## 13. Completion and status discipline

CORR-014 is complete only when every completion criterion in the authorizing task is satisfied,
including stable semantic answer relocation, common offline resolution, executable mutations,
explicit row-local state, lineage-aware CONTROL/recovery/review constructors, independently
reproducible VFS cases, preserved frozen contracts, five surfaces and unchanged budget/scope.

On completion, the only permitted correction-agent statuses are:

- `CORR-014-01`: `ADDRESSED — AWAITING INDEPENDENT REVIEW`; and
- `CORR-014-02`: `ADDRESSED — AWAITING INDEPENDENT REVIEW`.

Both IR6 findings remain open pending fresh independent review. Correction does not verify or close
them.

## 14. Stop conditions

Stop before or during correction if it requires changing the FAL-002 specification, scope,
criteria, `HD-FAL-012`/`HD-FAL-014` architecture, frozen section 9 contracts, surface allocation,
authority, role, module, adapter, dependency or budget; modifying implementation/test/schema/
fixture code; or using a path outside section 11.

## 15. Verification and next review

The correction commit must run pytest, Ruff lint, Ruff format check, Git diff check, Project Memory
Health and Repository Status and verify the complete changed-file list. It must then receive a fresh
independent read-only Standard-Assurance Review IR7 against the exact committed baseline.

IR7 must reassess `EB006-IR6-01`, `EB006-IR6-02`, decision relocation, offline resolution,
lineage-aware fixture construction, mutation completeness, five-surface integrity and budget.

## 16. Explicit exclusions

This decision does not:

- execute CORR-014 or modify EB-006;
- implement FAL-002, schemas, fixtures, tests or runtime behavior;
- change the FAL-002 specification;
- verify, resolve or close any finding;
- accept residual risk or produce PASS, eligibility or closure;
- authorize FAL-002 implementation;
- alter FAL-001 or its correction history; or
- authorize push, tag, merge, release, packaging, distribution, publication or version change.

## 17. Resulting governance state

- `HD-FAL-017`: `ACCEPTED`.
- IR6 outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
- `CORR-014-01` and `CORR-014-02`: `AUTHORIZED — NOT STARTED` as one bounded campaign.
- `EB006-IR6-01` and `EB006-IR6-02`: open and blocking; neither verified nor closed.
- IR6 dispositions for prior objectives remain recorded without closing their source findings.
- `HD-FAL-012` and `HD-FAL-014`: binding and not reopened.
- EB-006 and the FAL-002 specification: unchanged by this decision.
- FAL-002 implementation: `NOT AUTHORIZED`.
- Surfaces: five; budget: unchanged.
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 18. Next permitted step

Execute the complete bounded `CORR-014-01`–`CORR-014-02` EB-006 documentation correction in one
separate commit using only section 11 paths. Then conduct fresh independent read-only
Standard-Assurance Review IR7. Neither step may infer Implementation Authorization.
