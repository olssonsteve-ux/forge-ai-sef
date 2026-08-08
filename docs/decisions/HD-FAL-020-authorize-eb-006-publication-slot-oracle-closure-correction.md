# HD-FAL-020 — Authorize EB-006 PublicationSlot Oracle Closure Correction

Status: `ACCEPTED`

Decision date: 2026-08-09

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task requesting this Human Decision
against repository `forge-ai-sef`, branch `main`, commit
`6d08d3a8d7fde53ba86ef06c8cf753aaef5421b0`
(`docs(forge): complete EB-006 oracle totality correction`), with clean working tree and empty
staging. The task supplies the complete Independent Standard-Assurance Review IR9 evidence and
restricts this decision to authorization of one residual final-§48 documentation correction.

Review basis: IR9's canonical outcome is `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
It assigns `CORR-016-01` `PARTIALLY VERIFIED` and `EB006-IR6-02` `NOT VERIFIED`, creates no new
finding and preserves `EB006-IR6-01` as independently `VERIFIED`. IR9 independently verifies the
DecisionRequirement, DecisionBinding, EvidenceBinding, matrix, eligibility, recovery, successor,
semantic-answer and five-surface regressions. Its sole remaining demonstrated defect is the
standalone PublicationSlot REHASH family and the self-check that fails to detect its missing
executable closure.

## 1. Verified baseline and current state

Before substantive decision work, the repository baseline was verified as:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `6d08d3a8d7fde53ba86ef06c8cf753aaef5421b0`;
- commit subject: `docs(forge): complete EB-006 oracle totality correction`;
- working tree: clean; and
- staging: empty.

Current governance state:

- IR9: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`;
- `CORR-016-01`: `PARTIALLY VERIFIED`;
- `EB006-IR6-01`: independently `VERIFIED`, not closed;
- `EB006-IR6-02`: `NOT VERIFIED`, open and blocking;
- IR9 created no new finding and closed no finding;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 2. Governance and architecture determination

The remaining defect is correction-ready inside final EB-006 §48's existing test-only normative
oracle. It requires no architecture or production-semantic change, no new persisted/external
surface, module, adapter, dependency, role, authority, scope or budget.

Any execution that instead requires a change to §§44–47, the FAL-002 specification, architecture,
runtime, schemas, five-surface boundary or budget must stop for separate governance. This decision
does not authorize such a change.

## 3. Normative necessity determination and selected solution

The §48 caller audit finds no normative fixture, affected matrix row or oracle entrypoint that
directly calls standalone PublicationSlot REHASH. Required publication-slot mutation is exercised
through the independently verified GateRecord-contained PUBLICATION_INTENT constructor path.

Therefore select **Option B — prohibit standalone PublicationSlot REHASH**. This is the smallest
oracle capability consistent with required assurance coverage. CORR-017-01 must:

- classify standalone `PublicationSlot` as `REHASH_PROHIBITED`;
- make direct standalone REHASH deterministically raise `OracleDefinitionError` with the exact
  `REHASH_PROHIBITED` disposition before mutation;
- retain NO_REHASH as an explicit stale-identity/validator-failure test; and
- preserve the separate GateRecord-contained publication-intent mutation path as supported and
  fully constructor-driven.

Option A is not authorized by this decision. If a future concrete normative caller requires direct
standalone mutation, work must stop for new evidence and governance rather than silently expanding
the oracle.

## 4. Decision and mapping

Authorize exactly one narrowly bounded residual EB-006 documentation correction:

`CORR-017-01` → `EB006-IR6-02`

Authorized status:

`CORR-017-01`: `AUTHORIZED — NOT STARTED`

This authorization neither executes nor verifies the correction and does not address, close or
accept the finding. It is not PASS, planning completion or Implementation Authorization.

## 5. Dispatch and dependency self-check requirements

The final §48 self-check must make `VALID` require executable policy completeness. It must prove:

- every registered family resolves to exactly one implemented dispatch behavior;
- every supported family has an explicit complete handler or explicitly authorized generic
  behavior with no context-sensitive descendants;
- every context-required family has a handler, context schema, semantic context validator and
  recomputation path;
- every prohibited family deterministically rejects before mutation;
- no context-required or prohibited family can reach generic `rehash_value(work)`;
- supported/context-required handlers rebuild every declared derived descendant or delegate to a
  total constructor that does; and
- unknown canonical families reject.

The self-check must detect the IR9 failure shape: context-required registry policy plus absent
context-aware handler. It must also test missing, wrong and valid context for every retained
context-required family. Key presence alone is not semantic context validation.

## 6. Mandatory PublicationSlot evidence

CORR-017-01 must add executable evidence for:

1. direct standalone PublicationSlot REHASH → `REHASH_PROHIBITED`;
2. standalone NO_REHASH target mutation → stale target path/slot identity and validator failure;
3. GateRecord-contained publication-intent target mutation → valid target path, slot ID,
   commitment and outer GateRecord hash recomputation; and
4. dispatch self-check → failure if the prohibited handler is removed or any registered family can
   reach an unauthorized fallback.

No matrix row may be rewritten to depend on the prohibited standalone operation.

## 7. Frozen verified regressions

CORR-017-01 must preserve without semantic redesign:

- DecisionRequirement nested REHASH and NO_REHASH;
- DecisionBinding missing-, valid- and wrong-context behavior;
- EvidenceBinding `content_hash` prohibition;
- matrix B1, B2 and B3 and all 24 affected rows;
- ADDRESSED_AWAITING_REVIEW, empty-review, CRITICAL, independent-verification and recovery
  eligibility results;
- recovery through depth three;
- Run0/1/2, Review0/1/2 and actual-run review-event binding;
- stable semantic-answer identity across physical relocation;
- finding persistence, restart, no-progress and correction count;
- CJ, CF, H and HB; and
- exactly five persisted/external surfaces.

`EB006-IR6-01` remains independently `VERIFIED` and must not be reopened absent concrete
contradictory evidence.

## 8. Authorized change surface and exclusions

Permitted later CORR-017-01 changes are limited to:

- final §48 of `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`;
- `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md`; and
- `docs/README.md` only if genuinely required for index consistency.

Forbidden are changes to the FAL-002 specification, §§44–47 semantic contracts, runtime or
production code, tests, runtime schemas, committed fixtures, dependencies, versions, Audio
Recorder, architecture decisions, FAL-001 and unrelated artifacts. No new surface, module, adapter,
dependency or authority is authorized. Final §48 must be corrected directly; no normative overlay
may be added.

## 9. Budget

`HD-FAL-009` remains controlling:

- expected production implementation: approximately 1,660 LOC;
- hard maximum: 1,800 LOC;
- margin: 140 LOC;
- production modules: 4;
- adapters: 2;
- schema surfaces: 5; and
- new dependencies: zero.

No budget reopening is authorized.

## 10. Completion criteria

CORR-017-01 may claim only `ADDRESSED — AWAITING INDEPENDENT REVIEW` after all of these hold:

1. the necessity audit and Option B choice are recorded in final §48;
2. standalone PublicationSlot REHASH is executable deterministic prohibition;
3. standalone NO_REHASH exposes stale identity and validator failure;
4. registry policy and executable behavior agree for every family;
5. context-required and prohibited families cannot reach generic fallback;
6. dispatch coverage and derived-descendant coverage are executable self-check invariants;
7. wrong but key-complete context rejects for every retained context-required family;
8. the GateRecord publication-intent path remains valid;
9. DecisionBinding, EvidenceBinding and DecisionRequirement regressions pass;
10. all 24 affected matrix rows pass;
11. eligibility, recovery-N, successor and semantic-answer regressions pass;
12. five surfaces and the fixed budget remain unchanged; and
13. no forbidden file changes occur.

## 11. Status discipline and next gate

Resulting state is only:

- `HD-FAL-020`: `ACCEPTED`;
- `CORR-017-01`: `AUTHORIZED — NOT STARTED`;
- `EB006-IR6-02`: `NOT VERIFIED`, open and blocking;
- `EB006-IR6-01`: independently `VERIFIED`, not closed;
- IR9 created no new finding;
- no finding is closed and no residual risk is accepted;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

The next permitted step is execution of CORR-017-01 as one narrowly bounded final-§48 documentation
correction in a separate commit, followed by one fresh independent read-only Standard-Assurance
Review of that correction baseline. This decision is not Implementation Authorization.
