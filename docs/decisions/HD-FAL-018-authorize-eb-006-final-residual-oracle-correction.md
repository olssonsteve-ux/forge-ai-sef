# HD-FAL-018 — Authorize EB-006 Final Residual Oracle Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task titled
`HD-FAL-018 — Authorize EB-006 Final Residual Oracle Correction` against branch `main`, commit
`79867c4ce1d5855b9c18e5451ea9c56c173c769f`
(`docs(forge): complete EB-006 sixth residual correction`), with clean working tree and empty
staging. The task supplies the complete Independent Standard-Assurance Review IR7 evidence and
requires this decision only if the sole residual finding is correction-ready.

Review basis: Independent Standard-Assurance Review IR7 of EB-006 at the exact baseline above. Its
canonical outcome is `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`. IR7 independently
verified `CORR-014-01` and `EB006-IR6-01`, did not verify `CORR-014-02` or `EB006-IR6-02`, and
created no new finding. Its demonstrated failures are residual aspects of `EB006-IR6-02`.

Architecture basis: `HD-FAL-012`, `HD-FAL-014` and the independently verified semantic-decision,
recovery/discovery, finding-state and canonical/hash contracts remain binding and frozen.

## 1. Verified baseline and current state

Before substantive work, the repository baseline was verified as:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `79867c4ce1d5855b9c18e5451ea9c56c173c769f`;
- commit subject: `docs(forge): complete EB-006 sixth residual correction`;
- working tree: clean; and
- staging: empty.

Current governance state:

- `HD-FAL-012`, `HD-FAL-014` and `HD-FAL-017`: `ACCEPTED`;
- IR7: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`;
- `EB006-IR6-01`: independently `VERIFIED`, not closed;
- `EB006-IR6-02`: open and blocking;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 2. Governance assessment

The sole remaining blocker is correction-ready inside the existing EB-006 documentation and
fixture-oracle planning authority. IR7 demonstrated no architecture, specification, scope, budget,
decision-semantics, finding-state, severity, PASS, no-progress or correction-ceiling defect.

The required direction is oracle to frozen normative model. No production-governing contract may
be changed to accommodate the oracle. Contrary evidence requires the correction to stop for a new
governance decision.

## 3. Decision and mapping

Authorize exactly one narrowly bounded residual EB-006 documentation correction:

`CORR-015-01` → `EB006-IR6-02`

The objective is to make final §48's independent normative fixture oracle total and faithful to the
already verified models. This authorization does not execute the correction, verify or close the
finding, create PASS, or authorize implementation.

## 4. Authorized lineage correction

Every stateful fixture constructor must derive the current physical series, path and predecessor
state from an explicit `OracleLineageState`, except a constructor explicitly creating origin state.
Audit and correct GateRecord, PUBLICATION_INTENT, RECOVERY_ROOT, CONTROL, RunRecord,
ReviewerExchange, decision/rebinding and path constructors. No successor constructor may silently
default to `ORIGIN`, call an implicit gate-zero/ready chain or select an ambient run/checkpoint.

The final executable oracle must construct:

`origin → CONTROL → PUBLICATION_INTENT → RECOVERY_ROOT-1 → CONTROL → PUBLICATION_INTENT → RECOVERY_ROOT-2`

Recovery-2 must use recovery-1's active physical state while preserving logical origin, complete
finding and decision history, correction count and progress/no-progress state. It must also create
origin, successor and recovery-N RunRecord/ReviewerExchange pairs whose FindingEvents bind the
actual reviewed RunRecord.

## 5. Authorized REHASH correction

Define an executable, topologically ordered dependency graph for every fixture-mutatable derived
hash. At minimum, mutation of `DecisionRequirement.semantic_input` must recompute, in order:

1. canonical semantic payload;
2. `semantic_payload_hash`;
3. dependent semantic identity/hash values;
4. `decision_requirement_hash`;
5. affected binding, resolution, application or evidence hashes;
6. containing checkpoint/container hashes; and
7. containing surface payload and record hashes.

Audit DecisionRequirement, DecisionResolution, DecisionBinding, DecisionApplication, FindingEvent,
RemediationEvidence, FindingCheckpoint, EvidenceBinding, GateRecord state and progress fingerprints.
An outer hash may never be recomputed over a stale nested derived hash. Preserve `NO_REHASH` exactly:
it intentionally retains stale hashes and must fail with the specified mismatch.

## 6. Fixture and matrix completion

Convert every affected §48.10 normative operation— including informal `derive`, `obstruct`,
`repeat recovery_root` and `same snapshots` steps—into explicit constructor/function calls. Each row
must declare its initial lineage/VFS, all arguments and locals, ordered mutation/VFS operations,
expected state and exact disposition. No ambient filesystem, series, root, binding, application,
run or checkpoint is permitted.

Minimum executable scenarios are finding chain, finding recovery, review binding, semantic decision
relocation, REHASH/NO_REHASH, base VFS, recovery-N and successor run/review. Before completion they
must cover:

- MANIFEST → CONTROL0 → CONTROL1 → RECOVERY_ROOT1;
- RECOVERY_ROOT1 → CONTROL2 → RECOVERY_ROOT2;
- successor Run → successor Review → FindingEvent;
- DecisionRequirement semantic-input mutation with REHASH and NO_REHASH; and
- semantic DecisionResolution relocation through recovery-N.

## 7. Frozen contracts

CORR-015-01 must preserve unchanged:

- CJ, CF, H and HB;
- PUBLICATION_INTENT, recovery-condition/discovery hashes, pointer-free candidate discovery,
  RECOVERY_ROOT, logical lineage and recovery chaining semantics;
- DecisionRequirement, ResolutionSemanticInput, stable `resolution_semantic_hash`,
  PresentationEvidence, pending-card rebinding, resolution relocation, DecisionApplication and
  offline semantic/physical separation;
- FindingEvent, RemediationEvidence, FindingCheckpoint, restart fold, severity epochs, blocking
  latch, PASS, no-progress and correction ceiling;
- GateRecord as sole state authority; and
- exactly five external/persisted surfaces.

`EB006-IR6-01` remains independently `VERIFIED` and must not be reopened.

## 8. Authorized change surface and exclusions

Permitted changes are limited to:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`;
- `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md`; and
- `docs/README.md` only if required for index consistency.

The correction may not change the FAL-002 specification, runtime/production code, tests, runtime
schemas, committed fixtures, dependencies, versions, Audio Recorder, architecture decisions,
FAL-001 or unrelated artifacts. No new surface, authority, role, module, adapter, dependency or
mutable pointer is authorized.

## 9. Budget

`HD-FAL-009` remains controlling:

- expected production implementation: approximately 1,660 LOC;
- hard maximum: 1,800 LOC;
- margin: 140 LOC;
- production modules: 4;
- adapters: 2;
- schema surfaces: 5; and
- new dependencies: zero.

This decision does not reopen `EB006-FR-07`.

## 10. Completion and status discipline

CORR-015-01 is complete only when every completion criterion in the authorizing task is satisfied,
including active-series propagation, executable recovery-N, successor run/review binding, complete
REHASH dependency closure, exact NO_REHASH failure, total matrix rows, preserved frozen contracts,
five surfaces, unchanged budget and no forbidden file changes.

After correction, the correction agent may claim only:

`CORR-015-01`: `ADDRESSED — AWAITING INDEPENDENT REVIEW`

`EB006-IR6-02` remains open pending fresh independent review. The correction agent may not claim
VERIFIED, CLOSED, PASS, Implementation Authorization or planning completion.

## 11. Verification and next review

The correction must run pytest, Ruff lint, Ruff format check, Git diff check, Project Memory Health,
Repository Status and the complete normative oracle, then verify its exact changed-file list. It
must be committed separately and receive one fresh independent read-only Standard-Assurance Review.

That review must reassess only the remaining oracle blocker and regressions against frozen
contracts. It must not reopen `EB006-IR6-01` absent concrete contradictory evidence.

## 12. Resulting governance state

- `HD-FAL-018`: `ACCEPTED`.
- `CORR-015-01`: `AUTHORIZED — NOT STARTED`.
- `EB006-IR6-01`: independently `VERIFIED`, not closed.
- `EB006-IR6-02`: open and blocking.
- No finding is closed and no residual risk is accepted.
- FAL-002 implementation: `NOT AUTHORIZED`.
- No runtime implementation is authorized or performed.
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.
- Surfaces and budget: unchanged.

## 13. Next permitted step

Execute the single bounded `CORR-015-01` EB-006 fixture-oracle documentation correction in one
separate commit using only §8 paths. Then conduct one fresh independent read-only Standard-Assurance
Review. This decision is not Implementation Authorization.
