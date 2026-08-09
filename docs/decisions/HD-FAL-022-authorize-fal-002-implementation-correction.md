# HD-FAL-022 — Authorize FAL-002 Implementation Correction

Status: `ACCEPTED`

Decision date: 2026-08-09

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task requesting this decision
against repository `forge-ai-sef`, branch `main`, commit
`36ea966222b01f550d9c32919fbd2612d2ce998b`
(`feat(forge): implement FAL-002 standard assurance loop`), with clean working tree and empty
staging. The request supplies the complete fresh Independent Implementation Review evidence,
including its seven registered blocking findings, and requires a separate committed Human Decision
before correction begins.

Review basis: the Independent Implementation Review outcome is
`FAIL — IMPLEMENTATION CORRECTION REQUIRED`. It registers `FAL002-IR1-01` through
`FAL002-IR1-07` as `BLOCKING` and determines that HD-FAL-021 STOP conditions #9 and #13 were
crossed. Repository inspection confirms the failures are implementation-conformance defects in the
already-authorized contract, not a need for architecture or specification redesign.

## 1. Decision question

Should Forge authorize one bounded implementation-correction campaign for all seven blocking
FAL-002 implementation findings, and what explicit production-LOC budget governs it?

## 2. Decision

**Yes. Authorize `FAL002-CORR-001` as one bounded FAL-002 implementation-correction campaign.**

`HD-FAL-022` is `ACCEPTED`. `FAL002-CORR-001` is `AUTHORIZED — NOT STARTED`. It may correct only
the seven findings and the residual-risk cases necessary to prove those corrections. It does not
accept or close FAL-002, verify or close a finding, authorize release work, or alter FAL-001.

Architecture and scope remain frozen. The production-LOC ceiling is revised from 1,800 to 3,000
because empirical implementation-review evidence demonstrates that complete enforcement of the
already-authorized EB-006 semantics requires more implementation than the 23 remaining lines. This
budget change is not a capability, surface, authority or product-scope expansion.

## 3. Verified decision baseline

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `36ea966222b01f550d9c32919fbd2612d2ce998b`;
- commit subject: `feat(forge): implement FAL-002 standard assurance loop`;
- working tree: clean; and
- staging: empty.

The frozen normative basis remains the FAL-002 specification, EB-006 at its reviewed implementation
contract baseline, HD-FAL-012, HD-FAL-014, HD-FAL-021 and all materially applicable prior decisions.

## 4. Findings and correction mapping

All findings remain `OPEN — BLOCKING`:

| Correction objective | Finding | Required outcome |
| --- | --- | --- |
| `FAL002-CORR-001-01` | `FAL002-IR1-01` | executable canonical sequential loop, complete 17-command collector, concrete two-adapter chain and persisted RunRecord |
| `FAL002-CORR-001-02` | `FAL002-IR1-02` | exact nested canonical models and five schemas generated from the same authority |
| `FAL002-CORR-001-03` | `FAL002-IR1-03` | matching authoritative `PUBLICATION_INTENT` required before committed final publication |
| `FAL002-CORR-001-04` | `FAL002-IR1-04` | exact recovery identity/carry-forward, transient handling and enforceable predecessor sealing |
| `FAL002-CORR-001-05` | `FAL002-IR1-05` | actual ReviewerExchange-to-RunRecord and exact embedded decision authority binding |
| `FAL002-CORR-001-06` | `FAL002-IR1-06` | criterion source/locator/hash/provenance/resolvability required for eligibility |
| `FAL002-CORR-001-07` | `FAL002-IR1-07` | exact event/remediation models and terminal-hash recurrence across occurrences |

These objectives form one correction round. They may not be split to evade shared history, budget
or independent re-review.

## 5. STOP-condition disposition

The review's STOP results are accepted:

- STOP #9, weakened canonical/hash semantics: `TRIGGERED` by semantically under-constrained
  authoritative boundary models and schemas. `CJ`, `CF`, `H` and `HB` remain frozen and are not to
  be redesigned.
- STOP #13, weakened PASS/blocking semantics: `TRIGGERED` by insufficient RunRecord/reviewer and
  criterion-evidence authority binding. The frozen PASS and blocking invariants remain mandatory.

Governance authorizes conformance correction to restore the frozen contracts. It does not accept a
weaker contract or retrospectively declare either stop condition untriggered.

## 6. Architecture determination

Repository inspection finds no remediation that inherently requires a sixth surface, fifth
production module, third adapter, new dependency, mutable global pointer, new HumanDecisionRecord
variant, specification change or change to HD-FAL-012/014 authority. Correction therefore has
disposition:

`IMPLEMENTATION CORRECTION — NO ARCHITECTURE REOPENING`

The following limits remain binding:

- persisted/external surfaces: exactly 5 — GateRecord, ExecutorExchange, RunRecord,
  ReviewerExchange and HumanDecisionRecord;
- new FAL-002 production modules: exactly 4 maximum;
- adapters: exactly 2 — one executor and one reviewer;
- new direct or transitive dependencies: 0; and
- mutable global authority pointers or sixth persisted seal/recovery stores: prohibited.

## 7. Production-LOC analysis and revised ceiling

Current governed production LOC is 1,777. Inspection attributes the remediation estimate as:

| Remediation group | Gross added LOC | Removed/replaced LOC | Estimated net LOC |
| --- | ---: | ---: | ---: |
| orchestration, 17-command collector and executable adapters | 360 | 30 | 330 |
| exact nested models and generated schema constraints | 390 | 100 | 290 |
| publication intent, recovery validation and sealing | 190 | 40 | 150 |
| RunRecord/reviewer, decision and criterion-evidence authority | 175 | 35 | 140 |
| exact finding/remediation and recurrence fold | 85 | 22 | 63 |
| **Total correction estimate** | **1,200** | **227** | **973** |

Estimated corrected production LOC is therefore 1,777 + 973 = approximately 2,750. The revised
hard maximum is **3,000 production LOC**, leaving approximately **250 LOC** of correction margin.
Counting retains the existing EB-006/repository production-LOC definition. Tests, schemas and
documentation may not hide production behavior or be counted as substitutes for implementation.

The correction agent must prefer clear replacement/refactoring where it removes incomplete code,
but must not compress, omit or relocate required behavior merely to meet the ceiling. If correct
implementation requires more than 3,000 counted production LOC, correction must stop and return to
governance before crossing the limit.

## 8. Authorized correction authority

Within the frozen architecture, `FAL002-CORR-001` may:

- implement the EB-006 sequential engineering-loop entrypoint connecting inventory, collector,
  executor, RunRecord, reviewer, findings, decisions, eligibility and persistence/recovery;
- add only the three missing authorized commands `INVENTORY`, `GIT-DIFF` and `GIT-NUMSTAT`, after
  confirming their exact EB-006 identifiers and parsers;
- make exactly the existing executor and reviewer adapters executable while preserving their role
  separation;
- strengthen all five canonical boundary validators and generated schemas from one shared exact
  model, including nested types, fields, enums, discriminators and conditional variants;
- require exact intent, slot, source, target, commitment, staged bytes and current-lineage binding
  before committed final publication;
- enforce recovery-root/predecessor/discovery cross-validation, deterministic transient-versus-
  stable failure handling, complete lineage carry-forward, recovery-N and GateRecord-derived
  predecessor sealing on every publication path;
- bind ReviewerExchange to the actual RunRecord ID, hash, logical origin, physical series, ordinal
  and required freshness/provenance;
- strengthen DecisionRequirement, PendingDecisionCard, PresentationEvidence, DecisionBinding,
  DecisionApplication and offline resolver validation without changing semantic answer identity;
- require criterion ID, source, locator, content/record hash, provenance, resolvability and required
  lineage before evidence contributes to PASS; and
- implement exact FindingEvent and RemediationEvidence models, occurrence-local predecessors and
  explicit prior-terminal recurrence links without erasing history.

## 9. Test and residual-risk authority

Tests may be added or changed to prove all seven findings, including at minimum executable
end-to-end operation, exact model/schema negative cases, missing intent, wrong recovery predecessor,
post-recovery append denial, transient recovery I/O, actual and fabricated RunRecord review binding,
invalid and valid criterion evidence, recurrence after close, and restart/recovery with decisions
and findings together.

The correction must also test arbitrary publication targets, symlinks, online/offline decision
equivalence, the full severity matrix and combined recovery state. These are review risks, not
pre-authorized new findings or scope. A newly exposed material defect outside `FAL002-IR1-01`–`07`
requires stop-and-report rather than silent expansion.

The passing `CJ`/`CF`, `H`/`HB`, create/adopt/conflict persistence, semantic-resolution hashing,
addressed-awaiting-review, empty-review denial and two-correction ceiling behavior are regression-
frozen.

## 10. Prohibited actions

This decision authorizes no:

- sixth surface, fifth module, third adapter or dependency;
- architecture/specification/EB-006 normative change;
- weakening of canonical, authority, finding, PASS, blocking or human-only closure semantics;
- FAL-002 acceptance, closure, release, packaging, version change or album capability work;
- finding verification or closure by the correction implementer; or
- change, correction, restart, acceptance or closure of FAL-001.

## 11. Resulting state and next gate

- Independent Implementation Review: `FAIL — IMPLEMENTATION CORRECTION REQUIRED`;
- `HD-FAL-022`: `ACCEPTED`;
- `FAL002-CORR-001`: `AUTHORIZED — NOT STARTED`;
- `FAL002-IR1-01` through `FAL002-IR1-07`: `OPEN — BLOCKING`;
- FAL-002: implemented, unaccepted, unclosed and awaiting authorized correction;
- architecture: frozen; no reopening authorized;
- production-LOC hard maximum: 3,000;
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.

The exact next permitted step is to execute the authorized FAL-002 implementation correction
against the committed HD-FAL-022 baseline, then perform one fresh independent implementation
review. Correction completion alone cannot accept or close FAL-002 or any finding.
