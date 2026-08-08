# HD-FAL-019 — Authorize EB-006 Residual Oracle Totality Correction

Status: `ACCEPTED`

Decision date: 2026-08-09

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task requesting the Human Decision
for the IR8-preserved `EB006-IR6-02` residual, against repository `forge-ai-sef`, branch `main`,
commit `b100170e565d743de9fb5f43a7fb930728b9e8ab`
(`docs(forge): complete final EB-006 oracle correction`), with clean working tree and empty staging.
The task supplies the complete Independent Standard-Assurance Review IR8 evidence and limits this
decision to governance authorization of one §48 documentation correction.

Review basis: Independent Standard-Assurance Review IR8 at the exact baseline above. Its canonical
outcome is `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`; `CORR-015-01` is
`PARTIALLY VERIFIED`, `EB006-IR6-02` is `NOT VERIFIED`, and no new finding ID was created. IR8
preserved `EB006-IR6-01` as independently `VERIFIED` and demonstrated three residual manifestations
of `EB006-IR6-02`: incomplete executable REHASH policy/closure, non-executable affected matrix rows,
and an eligibility constructor that does not enforce the frozen PASS invariant.

Architecture basis: `HD-FAL-012`, `HD-FAL-014`, `HD-FAL-017` and `HD-FAL-018` remain binding. IR8
verified recovery through depth three, successor RunRecord/ReviewerExchange binding, exact
review-event evidence binding, the DecisionRequirement nested REHASH case, NO_REHASH behavior,
semantic-answer relocation and the five-surface boundary.

## 1. Verified baseline and current state

Before substantive decision work, the repository baseline was verified as:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `b100170e565d743de9fb5f43a7fb930728b9e8ab`;
- commit subject: `docs(forge): complete final EB-006 oracle correction`;
- working tree: clean; and
- staging: empty.

Current governance state:

- IR8: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`;
- `CORR-015-01`: `PARTIALLY VERIFIED`;
- `EB006-IR6-01`: independently `VERIFIED`, not closed;
- `EB006-IR6-02`: `NOT VERIFIED`, open and blocking;
- no finding was created or closed by IR8;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 2. Governance and architecture determination

The IR8 failures are correction-ready inside final EB-006 §48's existing documentation and
fixture-oracle authority. They require the oracle to conform to already valid production-governing
contracts. They require no new architecture decision, persistence surface, state authority, role,
module, adapter, dependency, scope or budget.

Any correction that instead requires changed §§44–47 semantics, specification, architecture,
surface count, runtime authority or budget must stop for a new Human Decision. This decision does
not authorize such changes.

## 3. Decision and mapping

Authorize exactly one tightly bounded residual EB-006 documentation correction:

`CORR-016-01` → `EB006-IR6-02`

Authorized status:

`CORR-016-01`: `AUTHORIZED — NOT STARTED`

The correction is one objective with three inseparable work packages:

1. executable REHASH policy and complete dependency enforcement;
2. executable affected fixture-matrix rows; and
3. eligibility-oracle fidelity to the frozen finding/PASS model.

This authorization does not execute, address, verify or close the correction or finding. It does
not create PASS, planning completion or Implementation Authorization.

## 4. Frozen contracts

CORR-016-01 must preserve unchanged:

- canonical/hash: CJ, CF, H and HB;
- recovery/discovery: PUBLICATION_INTENT, `recovery_condition_hash`,
  `recovery_discovery_key`, pointer-free recovery, RECOVERY_ROOT and arbitrary recovery depth;
- decision semantics: DecisionRequirement, PendingDecisionCard, DecisionResolution,
  ResolutionSemanticInput, stable `resolution_semantic_hash`, PresentationEvidence,
  DecisionBinding, DecisionApplication, semantic/physical relocation separation and offline
  authority;
- finding/governance: FindingEvent, RemediationEvidence, FindingCheckpoint, restart reconstruction,
  severity epochs, blocking latch, PASS eligibility, no-progress and correction ceiling;
- GateRecord as sole state authority; and
- exactly five persisted/external surfaces.

`EB006-IR6-01` remains independently `VERIFIED` and must not be reopened absent concrete
contradictory evidence.

## 5. Executable REHASH policy

Final §48 must classify every mutation path as exactly one of:

- `REHASH_SUPPORTED`: complete dependency closure is derivable from the object;
- `REHASH_REQUIRES_CONTEXT`: exact named source objects are mandatory; or
- `REHASH_PROHIBITED`: required semantic/evidence authority cannot be derived.

The executable registry must normalize the path, resolve the rule, validate required context,
reject prohibited or context-deficient operations before returning a rehashed object, invalidate
all transitive dependents, recompute innermost-to-outermost and validate final consistency. The
registry may not remain prose-only metadata.

## 6. Required REHASH residual repairs

- Bare mutation of `DecisionBinding.binding_generation` must reject unless exact new-generation
  PendingDecisionCard ID, hash, locator, predecessor binding and other generation-specific source
  context are supplied. If supported with context, all dependent physical and semantic fields must
  be coherent; generation-0 card data may not survive in generation 1.
- Publication target mutation must recompute `slot_id` from the final canonical slot preimage and
  then recompute every parent, or reject without exact required source context.
- Bare REHASH of `EvidenceBinding.content_hash` must raise `OracleDefinitionError` or the exact
  final repository-standard equivalent when source evidence is absent.
- DecisionRequirement, DecisionResolution, DecisionBinding, DecisionApplication, EvidenceBinding,
  publication slots, FindingEvent, RemediationEvidence, FindingCheckpoint, GateRecord,
  recovery-derived values and progress/no-progress inputs must each have full closure or an
  executable context/prohibition rule.

Mandatory adversarial cases are: valid DecisionRequirement REHASH; rejected bare binding-generation
REHASH; coherent context-supplied binding REHASH if supported; publication target mutation with
correct changed slot identity or rejection; rejected bare EvidenceBinding REHASH; and deterministic
NO_REHASH mismatch.

## 7. Matrix-row executability

Every normative row affected by CORR-015 or CORR-016 must execute from exact declared inputs with no
ambient state or prose-only transition. In particular:

- `intent-not-required` must test the actual canonical `variant_kind` field, not nonexistent
  `payload.kind`;
- `intent-required-missing` must construct a COMMITTED/non-reconstructable output, an exact
  predecessor/slot, absence of matching PUBLICATION_INTENT and an attempted final publication whose
  executable validator produces `FORBIDDEN_TRANSITION` or the exact normative equivalent; and
- `recovery-crash-after-root` must use only actual RECOVERY_ROOT, GateRecord and
  OracleLineageState fields and verify the real carried decision requirement/binding state.

One executable matrix gate must run every affected row and require zero unexpected `KeyError`, zero
undeclared variable, zero prose-only transition and exact observed-versus-declared disposition.

## 8. Eligibility and PASS fidelity

The §48 eligibility constructor must consume or derive the same authoritative FindingCheckpoint,
CurrentFindingState, unresolved set, effective severity, blocking latch, lifecycle and independent
verification state governed by frozen §47.

It must reject eligibility when any unresolved blocking or effective CRITICAL finding exists.
`ADDRESSED_AWAITING_REVIEW` remains unresolved. A later review with `findings=[]` does not verify or
erase it. Eligibility may follow only after the already-authorized independent absence/verification
event and every other frozen condition succeeds.

Mandatory executable scenarios must prove both:

1. NEW blocking finding → valid RemediationEvidence → ADDRESSED_AWAITING_REVIEW → empty review →
   eligibility denied; then exact independent verification → eligibility follows frozen §47; and
2. unresolved effective CRITICAL finding plus otherwise PASS-like review → eligibility denied.

## 9. Required regression coverage

The correction must preserve and execute:

- recovery depths 1, 2 and 3;
- Run0/1/2 and Review0/1/2 exact physical-series and reviewed-run bindings;
- exact review-event RunRecord ID/hash bindings and monotonic finding history;
- identical `resolution_semantic_hash` across R0/R1/R2 for the same answer;
- deterministic finding checkpoint/restart reconstruction;
- valid DecisionRequirement REHASH and deterministic NO_REHASH; and
- exactly five surfaces.

## 10. Completion criteria

CORR-016-01 is complete only when all are true:

1. the REHASH registry controls executable behavior;
2. every supported family has full transitive closure;
3. context-required paths require exact explicit context;
4. prohibited paths raise deterministic oracle errors;
5. binding generations cannot mix physical generations;
6. publication target mutation cannot retain stale `slot_id`;
7. EvidenceBinding prohibition is enforced;
8. DecisionRequirement REHASH and NO_REHASH remain correct;
9. all three IR8-failing matrix rows execute with their declared outcomes;
10. every affected matrix row passes the executable matrix gate;
11. eligibility consumes carried canonical finding state;
12. ADDRESSED_AWAITING_REVIEW plus empty review denies eligibility;
13. valid independent verification follows only frozen semantics;
14. unresolved CRITICAL denies eligibility;
15. recovery-N, successor execution and semantic relocation regressions pass;
16. five surfaces, scope and budget remain unchanged; and
17. no forbidden file changes.

## 11. Authorized change surface and exclusions

Permitted later CORR-016 changes are limited to:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`;
- `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md`; and
- `docs/README.md` only if required for index consistency.

Forbidden are changes to the FAL-002 specification, runtime/production code, tests, runtime schemas,
committed fixtures, dependencies, versions, Audio Recorder, architecture decisions, FAL-001 or
unrelated artifacts. No new surface, authority, role, module, adapter or dependency is authorized.
Final §48 must be corrected directly; no new normative overlay may be added. Sections 44–50 remain
the final active layer, and semantic changes outside §48 require STOP and new governance.

## 12. Budget

`HD-FAL-009` remains controlling:

- expected production implementation: approximately 1,660 LOC;
- hard maximum: 1,800 LOC;
- margin: 140 LOC;
- production modules: 4;
- adapters: 2;
- schema surfaces: 5; and
- new dependencies: zero.

IR8 provides no evidence for budget reopening.

## 13. Status discipline and next review

Resulting status is only:

- `HD-FAL-019`: `ACCEPTED`;
- `CORR-016-01`: `AUTHORIZED — NOT STARTED`;
- `EB006-IR6-02`: open and blocking;
- `EB006-IR6-01`: independently `VERIFIED`, not closed;
- no finding closed and no residual risk accepted;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

The next permitted step is execution of the single bounded CORR-016-01 §48 documentation correction
in one separate commit, followed by one fresh independent read-only Standard-Assurance Review of
that correction baseline. This decision is not Implementation Authorization.
