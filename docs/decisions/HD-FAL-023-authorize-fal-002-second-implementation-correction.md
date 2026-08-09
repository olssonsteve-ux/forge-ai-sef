# HD-FAL-023 — Authorize FAL-002 Second Implementation Correction

Status: `ACCEPTED`

Decision date: 2026-08-09

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task requesting this Human Decision
against repository `forge-ai-sef`, branch `main`, commit
`92c16e9e7e2b6871a65bd545be2e3d0dce88e5fc`
(`test(forge): cover FAL-002 recovery carry-forward`), with clean working tree and empty staging.
The request supplies Independent Implementation Review II and its reproduced falsification evidence.

Review basis: Independent Implementation Review II concluded
`FAIL — IMPLEMENTATION CORRECTION REQUIRED`. It independently verified `FAL002-IR1-02`,
`FAL002-IR1-06` and `FAL002-IR1-07`, found no new finding, and left four findings blocking:
`FAL002-IR1-01` partially verified, `FAL002-IR1-03` not verified, `FAL002-IR1-04` partially
verified and `FAL002-IR1-05` partially verified. HD-FAL-021 STOP conditions #9 and #13 remain
triggered.

## 1. Decision question

Should Forge authorize one further bounded implementation-correction campaign for the four residual
FAL-002 findings, and what explicit production-LOC ceiling governs it?

## 2. Decision

**Yes. Authorize `FAL002-CORR-002` as one bounded second implementation-correction campaign.**

`HD-FAL-023` is `ACCEPTED`. `FAL002-CORR-002` is `AUTHORIZED — NOT STARTED`. It may correct only
the four mapped residual findings and add the tests necessary to prove those corrections. It does not
accept or close FAL-002, close any finding, authorize release work, or alter FAL-001.

Disposition: `IMPLEMENTATION CORRECTION — NO ARCHITECTURE REOPENING`.

The production-LOC hard maximum is revised from 3,000 to **3,400**. This is an explicit correction
budget for enforcing the already-frozen contract, not a scope, surface, dependency, architecture or
product-capability expansion.

## 3. Verified governance baseline

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `92c16e9e7e2b6871a65bd545be2e3d0dce88e5fc`;
- preceding correction commit: `b778e98d9532e0fe8a34485ffc068d35b7129112`
  (`fix(forge): correct FAL-002 implementation conformance`);
- review-fixture commit: `92c16e9e7e2b6871a65bd545be2e3d0dce88e5fc`
  (`test(forge): cover FAL-002 recovery carry-forward`);
- working tree: clean; and
- staging: empty.

The FAL-002 specification, EB-006, HD-FAL-012, HD-FAL-014, HD-FAL-021 and all materially
applicable prior decisions remain authoritative and unchanged.

## 4. Finding and correction mapping

| Correction objective | Finding | Required outcome |
| --- | --- | --- |
| `FAL002-CORR-002-01` | `FAL002-IR1-01` | existing canonical loop integrates exclusive intent-aware publication, actual decision state, derived progress and I/O-owned reviewer provenance |
| `FAL002-CORR-002-02` | `FAL002-IR1-03` | no intent-required COMMITTED final record can bypass matching authoritative `PUBLICATION_INTENT` |
| `FAL002-CORR-002-03` | `FAL002-IR1-04` | RECOVERY_ROOT publication/adoption resolves and validates the actual persisted predecessor and complete carry-forward |
| `FAL002-CORR-002-04` | `FAL002-IR1-05` | exact RunRecord/reviewer provenance and decision requirement/binding/resolution/application authority chain |

These four objectives form one campaign and may not be split to reset history or avoid shared
authority, budget or re-review requirements.

`FAL002-IR1-01`, `FAL002-IR1-03`, `FAL002-IR1-04` and `FAL002-IR1-05` remain
`OPEN — BLOCKING`. `FAL002-IR1-02`, `FAL002-IR1-06` and `FAL002-IR1-07` remain
`INDEPENDENTLY VERIFIED — NOT CLOSED` and may not be reopened absent concrete regression evidence.

## 5. STOP-condition disposition

- HD-FAL-021 STOP #9: `TRIGGERED`. Direct COMMITTED publication can bypass intent and an internally
  consistent recovery root can claim a nonexistent predecessor.
- HD-FAL-021 STOP #13: `TRIGGERED`. Cross-decision resolution confusion, callback-controlled
  reviewer observation and unresolved decision-state integration weaken authority before eligibility.

This decision authorizes correction to restore the frozen contracts. It does not weaken either
contract or declare either stop condition cleared.

## 6. Architecture determination

Code inspection finds that the four residuals can be corrected by replacing and centralizing logic
inside the existing four production modules. No remediation inherently requires another surface,
module, adapter, dependency, mutable authority pointer, specification revision or architecture
decision.

The following remain frozen:

- exactly four FAL-002 production modules;
- exactly two adapters, one executor and one reviewer;
- exactly five persisted/external surfaces;
- zero new direct or transitive dependencies;
- no mutable authority pointer or sixth recovery/seal store;
- FAL-002 specification and EB-006 semantics; and
- HD-FAL-012/014 recovery and decision authority.

## 7. Production-LOC analysis and revised ceiling

Current governed production LOC is **2,998**:

| Module | Current LOC |
| --- | ---: |
| `forge/fal002.py` | 693 |
| `forge/fal002_inventory.py` | 158 |
| `forge/fal002_io.py` | 367 |
| `forge/fal002_model.py` | 1,780 |
| **Total** | **2,998** |

Inspection estimates the bounded remediation as:

| Remediation group | Gross added LOC | Removed/replaced LOC | Estimated net LOC |
| --- | ---: | ---: | ---: |
| exclusive publication authority and orchestrator call-site conversion | 95 | 35 | 60 |
| persisted predecessor validation and full recovery carry-forward | 60 | 10 | 50 |
| decision-chain cross-checking and applied/pending orchestration | 90 | 25 | 65 |
| I/O-owned reviewer provenance and no-progress integration | 55 | 20 | 35 |
| **Total estimate** | **300** | **90** | **210** |

Expected corrected production LOC is approximately **3,208**. The revised hard maximum is
**3,400 production LOC**, leaving approximately **192 LOC** of prudent correction margin. Tests,
schemas and documentation may not conceal production behavior. Code golf, validation deletion,
authority weakening and relocation into uncounted files are prohibited. If compliant implementation
requires more than 3,400 counted LOC, correction must stop and return to governance before crossing
the ceiling.

## 8. Authorized orchestration and publication correction

The existing canonical loop may be corrected, but no second orchestrator may be created. It must:

1. route every intent-required COMMITTED final publication through one exclusive authority path;
2. resolve requirements, current bindings, resolutions and applications rather than treating the
   historical existence of a requirement as pending;
3. invoke the frozen no-progress calculation and persist its derived result;
4. make invocation observation and immutable freshness/input provenance I/O-owned;
5. preserve the exact 17-command collector, two adapters and actual RunRecord persistence.

The raw create/adopt/conflict primitive may remain private/internal for reconstructable and already-
authorized writes, but must not be operationally callable as an authority bypass. Matching intent,
lineage, slot, stage, target identity/path and hashes are mandatory for COMMITTED final records.

## 9. Authorized recovery correction

Before RECOVERY_ROOT publication or adoption, runtime must load the claimed predecessor from its
deterministic canonical path and validate CF, record/hash, series, sequence, logical origin, slot,
discovery condition/key/ordinal, publication state, carry-forward and sealing transition. Internal
agreement inside the candidate root is insufficient. A phantom or orphan predecessor must reject.

Recovery-N, post-recovery append denial, transient-I/O failure, correction-count retention and
combined decision/finding/progress/eligibility restart behavior remain mandatory.

## 10. Authorized decision and reviewer correction

Decision resolution must cross-check the requested identity and exact requirement semantic/hash,
pending card, current binding/generation, presentation evidence, resolution identity/semantic hash,
selected allowed choice, application identity/hash/physical target and current lineage. A resolution
for decision B must never satisfy decision A. Semantic relocation P0→P1 and R0→R1→R2 for the same
decision remains valid.

Reviewer callbacks may provide only authorized review result content. I/O must own observed
invocation identity, immutable input hash, timing/termination and the facts used for freshness and
read-only provenance. Callback output cannot authoritatively replace those observations.

## 11. Test authority

Tests may be added or changed only to prove the four objectives and protect the three verified
findings. Required coverage includes:

- direct no-intent attempts for HumanDecisionRecord, ExecutorExchange, RunRecord and
  ReviewerExchange, plus exact positive and mismatched-intent cases;
- complete production publication call-site classification;
- phantom, wrong-hash and wrong-series predecessors, valid recovery, sealing and recovery depth 3;
- combined recovery/restart with decisions, findings, progress, correction and eligibility;
- cross-decision resolution rejection using fully validated records;
- validated online/offline equivalence, stale/orphan/conflicting/relocated decision cases;
- applied-versus-pending orchestration and real no-progress behavior;
- I/O-owned reviewer provenance; and
- regressions for exact models/schemas, criterion evidence and recurrence.

One combined end-to-end scenario must use actual persisted decision requirement/card/binding/
resolution/application, RunRecord/reviewer evidence, finding state, criterion evidence and progress
through the canonical orchestrator.

## 12. Stop-and-report boundaries

A new material defect outside `FAL002-IR1-01`, `FAL002-IR1-03`, `FAL002-IR1-04` and
`FAL002-IR1-05`, or a regression of independently verified `IR1-02`, `IR1-06` or `IR1-07`, requires
stop-and-report. The correction agent may not silently enlarge `FAL002-CORR-002`.

No runtime/schema/test correction is part of this Human Decision. It authorizes no architecture,
specification, release, packaging, version, album-capability, finding-closure or FAL-001 work.

## 13. Resulting lifecycle state and next gate

- Independent Implementation Review II: `FAIL — IMPLEMENTATION CORRECTION REQUIRED`;
- `HD-FAL-023`: `ACCEPTED`;
- `FAL002-CORR-002`: `AUTHORIZED — NOT STARTED`;
- residual blocker count: 4; new finding count: 0;
- STOP #9 and STOP #13: `TRIGGERED`;
- FAL-002: `Implemented — correction required`, unaccepted and unclosed;
- no finding is closed by this decision;
- architecture remains frozen;
- production-LOC hard maximum: 3,400; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

The exact next permitted step is to execute `FAL002-CORR-002` against the committed HD-FAL-023
baseline, then perform **one fresh independent implementation review**. Correction completion alone
cannot verify or close a finding or accept/close FAL-002.
