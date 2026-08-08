# HD-FAL-021 — Authorize FAL-002 Implementation

Status: `ACCEPTED`

Decision date: 2026-08-09

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task requesting the FAL-002
Implementation Authorization decision against repository `forge-ai-sef`, branch `main`, commit
`88e53fcbaa31ace83740699cd531f74f2d7e88b6`
(`docs(forge): close PublicationSlot oracle rehash gap`), with clean working tree and empty staging.
The task supplies the complete Independent Standard-Assurance Review IR10 evidence and requires a
separate Human Decision before implementation.

Review basis: IR10's canonical outcome is
`PASS — RECOMMEND IMPLEMENTATION AUTHORIZATION`. IR10 independently verified `CORR-017-01`,
`EB006-IR6-02` and the preserved `EB006-IR6-01`; found no remaining blocking Standard-Assurance
finding; and concluded that Standard-Assurance planning is complete for the reviewed baseline.

## 1. Decision question

Has FAL-002 completed sufficient architecture, implementation planning and independent
Standard-Assurance review to authorize implementation strictly according to the reviewed EB-006
baseline?

## 2. Decision

**Yes. Authorize implementation of FAL-002 strictly according to the reviewed EB-006 implementation
contract at `88e53fcbaa31ace83740699cd531f74f2d7e88b6`.**

`HD-FAL-021` is `ACCEPTED`. Under the repository Lifecycle Standard, FAL-002 is now
`Implementation Ready`. EB-006 is the authorized implementation-planning contract. This decision
does not implement, accept as complete or close FAL-002, and it authorizes no release activity.

Planning assurance has converged. No IR11 is required absent a material change to the reviewed
baseline. IR10 is planning assurance only; it is not the later implementation review.

## 3. Verified decision and implementation baseline

The decision baseline was verified before substantive decision work:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `88e53fcbaa31ace83740699cd531f74f2d7e88b6`;
- commit subject: `docs(forge): close PublicationSlot oracle rehash gap`;
- working tree: clean; and
- staging: empty.

The authorized implementation contract is locked to the versions at that exact commit of:

- `docs/capabilities/FAL-002-Standard-Assurance-Bounded-Engineering-Loop.md`;
- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`;
- applicable `HD-FAL-002` through `HD-FAL-020` decisions;
- `docs/architecture/FAL-002-reuse-matrix.md`;
- `CONSTITUTION.md`; and
- `AI_ENGINEERING_CONDUCT.md`.

The post-decision commit may add only this authority and synchronize governance/index/project
memory. Those non-normative state updates do not revise the locked implementation contract. Any
later material contract change requires governance reassessment before implementation continues.

## 4. Assurance-completion determination

IR10 independently established all of the following for the locked baseline:

- `CORR-017-01 = VERIFIED`;
- `EB006-IR6-02 = VERIFIED`;
- `EB006-IR6-01 = VERIFIED`;
- no blocking Standard-Assurance finding remains;
- oracle totality and the GateRecord-contained publication-intent path are preserved;
- canonical/hash, recovery/discovery, decision, finding/restart, severity/blocking/PASS,
  no-progress and correction-ceiling contracts are preserved;
- exactly five persisted/external surfaces are preserved; and
- implementation scope and budget are preserved.

Therefore Standard-Assurance planning is complete for
`88e53fcbaa31ace83740699cd531f74f2d7e88b6`.

## 5. Authorized implementation inventory and hard boundary

The authorized inventory is binding:

| Item | Authority |
| --- | --- |
| Expected new production LOC | approximately 1,660 |
| Hard maximum new production LOC | 1,800 |
| Unallocated margin | 140 LOC |
| New production modules | 4 |
| Executor adapters | 1 |
| Reviewer adapters | 1 |
| Total adapters | 2 |
| Persisted/external schema surfaces | exactly 5 |
| New dependencies | 0 |

The five surfaces are exclusively:

1. `GateRecord`;
2. `ExecutorExchange`;
3. `RunRecord`;
4. `ReviewerExchange`; and
5. `HumanDecisionRecord`.

No sixth persisted/external surface, auxiliary authority file, mutable current pointer, recovery
index, authoritative sidecar or required authoritative cache is authorized. Derived in-memory
structures are permitted only when reconstructable and non-authoritative under EB-006.

## 6. Frozen canonical and hash contracts

Implementation must preserve the reviewed `CJ`, `CF`, `H` and `HB` contracts exactly. Alternate
serialization, trailing-newline behavior, hash preimages or domain separation are not authorized.
Any discrepancy is an implementation defect, not permission to reinterpret the plan.

## 7. Frozen recovery and discovery contracts

Implementation must preserve `PUBLICATION_INTENT`, `recovery_condition_hash`,
`recovery_discovery_key`, pointer-free deterministic discovery, UUIDv5 candidate derivation and
probing, `RECOVERY_ROOT`, predecessor sealing, complete logical-lineage carry-forward, recovery-N
and the prohibition on global mutable pointer authority. No alternate discovery authority is
authorized.

The planning oracle's prohibition of standalone `PublicationSlot` REHASH is a fixture/oracle
capability rule. It does not remove or weaken the reviewed GateRecord-contained publication-intent
production path, and it does not authorize a generic runtime mutation capability.

## 8. Frozen decision contracts

Implementation must preserve `DecisionRequirement`, stable `decision_identity`,
`PendingDecisionCard`, `DecisionResolution`, `ResolutionSemanticInput`,
`resolution_semantic_hash`, `PresentationEvidence`, `DecisionBinding`, `DecisionApplication`,
semantic-answer identity independent of physical relocation, P0/P1 rebinding, R0/R1/RN
relocation and offline authority through the same logical-lineage resolver.

A `HumanDecisionRecord` alone is not runtime state authority. `GateRecord` remains the state-authority
carrier for decision application.

## 9. Frozen finding and gate-governance contracts

Implementation must preserve immutable `FindingEvent` history, `RemediationEvidence`,
`FindingCheckpoint`, full logical-lineage replay, restart reconstruction, occurrence/predecessor
ordering, duplicate rejection, recurrence semantics and the distinction between remediation and
independent verification. Hidden runtime finding state may not replace persisted canonical history.

Severity ordering, human reclassification epochs, the conservative blocking latch, current-finding
fold, unresolved-finding semantics, `ADDRESSED_AWAITING_REVIEW` as unresolved, independent
absence/verification events, PASS eligibility, no-progress and the two-correction ceiling remain
binding. Empty review never implies verification. PASS is forbidden while any open `CRITICAL` or
blocking finding exists. An executor may neither approve nor close its own work, review output may
not default to PASS, and actual closure remains human-only.

The FAL-002 reuse matrix is mandatory. Implementation must not create parallel canonical-JSON,
hashing, persistence, validation, recovery or project-state authority where EB-006 requires existing
repository authority.

## 10. Binding implementation stop conditions

Implementation must stop and return to governance if it:

1. requires a sixth persisted/external surface;
2. requires a new dependency;
3. requires more than four new production modules;
4. requires more than two adapters;
5. must exceed 1,800 new production LOC;
6. proves a frozen normative contract internally impossible to implement;
7. requires changing the FAL-002 specification;
8. requires changing architecture authority from `HD-FAL-012` or `HD-FAL-014`;
9. requires weakening canonical/hash semantics;
10. requires mutable pointer authority;
11. requires dropping finding or recovery history;
12. requires changing decision semantic identity;
13. requires weakening PASS or blocking semantics; or
14. uncovers a material planning contradiction not already resolved.

The implementation agent may not self-authorize around any stop condition. The 1,800-line maximum
is a ceiling, not a target; correctness may neither be compressed nor omitted to meet it.

## 11. Execution and review discipline

Implementation may begin only after this Human Decision is committed. A future implementation
agent must start from the authorized post-decision baseline, inspect EB-006 and governing decisions,
change only authorized implementation surfaces, preserve unrelated behavior, implement the planned
production tests/schemas/fixtures, run repository quality gates and commit implementation separately.

The documentation oracle is not a substitute for production tests. Implementation verification
must exercise the EB-006 planning-critical canonical/hash, five-surface, publication-intent,
create-only persistence, pointer-free recovery, recovery-N, decision lifecycle and relocation,
offline authority, finding/restart, severity/blocking/PASS, no-progress/correction-ceiling and
adversarial/corrupt-history behaviors.

Implementation completion is neither acceptance nor closure. A fresh independent implementation
review must assess actual runtime code and tests against FAL-002, EB-006, this decision, applicable
Human Decisions and the authorized scope/budget.

## 12. Finding disposition and predecessor isolation

IR10 independently verified `EB006-IR6-01` and `EB006-IR6-02`. Repository precedent distinguishes
remediation, independent verification and governance closure; this decision does not need closure
to authorize the independently verified planning baseline. Both findings remain
`INDEPENDENTLY VERIFIED — NOT CLOSED` in the historical assurance record. No residual risk is
accepted and no prior review history is rewritten.

FAL-001 remains permanently `TERMINATED BLOCKED`, unaccepted and unclosed, with correction count
2/2 and its complete history unchanged. FAL-002 does not reset, conceal or rewrite FAL-001.

## 13. Resulting governance state and next gate

- `HD-FAL-021`: `ACCEPTED`;
- IR10: `PASS — RECOMMEND IMPLEMENTATION AUTHORIZATION`;
- Standard-Assurance planning: complete for `88e53fcbaa31ace83740699cd531f74f2d7e88b6`;
- FAL-002: `Implementation Ready`;
- FAL-002 implementation: authorized but not begun by this decision;
- EB-006: authorized implementation-planning contract at the locked baseline;
- `EB006-IR6-01`: `INDEPENDENTLY VERIFIED — NOT CLOSED`;
- `EB006-IR6-02`: `INDEPENDENTLY VERIFIED — NOT CLOSED`;
- no IR11 required absent material baseline change; and
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.

The next permitted step is to implement FAL-002 according to EB-006 in a separate implementation
change, then perform fresh independent implementation review.
