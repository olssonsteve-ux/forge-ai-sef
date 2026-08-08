# HD-FAL-016 — Authorize EB-006 Fifth Residual Assurance Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task titled
`HD-FAL-016 — Authorize EB-006 Fifth Residual Assurance Correction` against branch `main`, commit
`fddff8c147681e68125fc2ea3204db4d8b5deeb8`
(`docs(forge): complete EB-006 fourth residual correction`), with clean working tree and empty
staging.

Review basis: Fresh Independent Standard-Assurance Review IR5 of EB-006 at the exact baseline above.
Its canonical outcome is `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`. IR5 independently
verified the narrow CORR-012-01/EB006-IR4-01 canonical-hash correction and
CORR-012-03/EB006-IR4-03 publication-intent/recovery-discovery correction. It did not verify
CORR-012-02, CORR-012-04 or CORR-012-05 and identified four blocking residual findings,
`EB006-IR5-01` through `EB006-IR5-04`.

Architecture basis: `HD-FAL-012` and `HD-FAL-014` remain binding. This decision preserves the
successor-series architecture, publication-intent architecture, pointer-free recovery discovery,
no-global-pointer invariant and five-surface boundary.

## 1. Verified baseline and current state

Before substantive work, the repository baseline was verified as:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `fddff8c147681e68125fc2ea3204db4d8b5deeb8`;
- commit subject: `docs(forge): complete EB-006 fourth residual correction`;
- working tree: clean; and
- staging: empty.

Current governance state at this decision:

- `HD-FAL-012`, `HD-FAL-014` and `HD-FAL-015`: `ACCEPTED`;
- IR5 outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`;
- `EB006-IR5-01` through `EB006-IR5-04`: open and blocking;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 2. Governance and architecture assessment

Repository evidence confirms IR5's conclusion that all four findings are correction-ready within:

- the approved FAL-002 capability specification;
- `HD-FAL-012` and `HD-FAL-014`;
- the existing GateRecord and HumanDecisionRecord authority allocations;
- exactly five existing persisted/external boundary surfaces;
- the existing production module, adapter, schema and dependency inventory; and
- the approximately 1,660 expected / 1,800 maximum production-LOC envelope.

No finding requires a new architecture choice, changed scope or criteria, a sixth surface, a mutable
pointer, a new authority, role, adapter, production module, dependency or budget increase. The four
objectives are interdependent repairs to one implementation-planning contract and form one bounded
campaign, not four independent scope expansions.

## 3. Finding disposition and authorization mapping

| Finding | Governance disposition | Authorized objective |
| --- | --- | --- |
| `EB006-IR5-01` | correction-ready within existing fixture/test-planning authority | `CORR-013-01` |
| `EB006-IR5-02` | correction-ready within existing decision and GateRecord authority | `CORR-013-02` |
| `EB006-IR5-03` | correction-ready inside the existing GateRecord surface | `CORR-013-03` |
| `EB006-IR5-04` | correction-ready within existing finding/reclassification authority | `CORR-013-04` |

Authorization changes no finding status. All four remain open until correction and fresh independent
review. This decision itself verifies or closes no finding.

## 4. Decision

Authorize exactly one bounded coherent EB-006 documentation/planning correction campaign containing:

- `CORR-013-01` → `EB006-IR5-01`;
- `CORR-013-02` → `EB006-IR5-02`;
- `CORR-013-03` → `EB006-IR5-03`; and
- `CORR-013-04` → `EB006-IR5-04`.

All four objectives must be completed and committed together. Partial local completion does not make
EB-006 review-ready. The correction agent may later claim at most
`ADDRESSED — AWAITING INDEPENDENT REVIEW`; it may not claim verification, closure, PASS,
Implementation Authorization or partial readiness.

## 5. CORR-013-01 — Total independent fixture oracle

Correct `EB006-IR5-01` by replacing incomplete normative fixture descriptions with a total,
independently executable oracle that can be reconstructed from EB-006 alone.

Every constructor must define its complete object and nested fields, literal primitives or exact
deterministic derivations, timestamps, IDs, paths, hashes, provenance, grants, results, version
observations, finding/remediation data, recovery records, decision records and offline-authority
records. Normative placeholders or phrases such as `<every and only ...>`, “use final shape”,
“supply all fields”, “valid X” or “matching X” are forbidden.

Every negative case must define its base fixture, exact JSON pointer or canonical filesystem
location, operation, literal value or exact bytes, rehash behavior, expected files/state, validation
result and failure disposition. Prose such as “put raw 7b”, “place valid-looking root” or “attempt
final without intent” is insufficient without exact deterministic construction steps.

The oracle may use independently specified standard-library algorithms only. It must not call or
import production canonicalization, hashing, schemas, validation, recovery or finding-ledger code.
The independently verified `CJ`, `CF`, `H` and `HB` contract remains unchanged.

## 6. CORR-013-02 — Separate pending question and accepted resolution

Correct `EB006-IR5-02` by defining separate immutable canonical semantics for:

1. DecisionRequirement—the stable semantic obligation;
2. PENDING_CARD—the HumanDecisionRecord representing the question;
3. RESOLUTION—the separate HumanDecisionRecord representing the answer; and
4. ActiveDecisionBinding—the GateRecord-carried relationship identifying the authoritative physical
   pending and accepted records for one stable `decision_identity`.

Define exact pending-card and resolution IDs, locators, hashes, generations, keys and cross-record
references. One immutable HumanDecisionRecord must never be required to be both PENDING and ACCEPTED.
The accepted resolution must reference the same decision identity and pending-card hash, and a later
authoritative GateRecord must explicitly apply its exact record ID/hash without mutating the card.

Correct the closed MANIFEST/initial GateRecord model so the initial DecisionRequirement,
ActiveDecisionBinding and any accepted-resolution application required by lookup are legally
representable using the existing GateRecord surface. Complete-logical-lineage lookup and offline
authority must use the same accepted-resolution semantics, reject inactive/orphan records and remain
stable through physical rebinding.

No sixth surface, new decision authority or changed semantic governance question is authorized.

## 7. CORR-013-03 — Persisted finding history inside GateRecord

Correct `EB006-IR5-03` by adding exact canonical finding-history representation to existing
GateRecord variant fields. Define which existing variants carry immutable FindingEvents,
RemediationEvidence and derived checkpoint/hash data. No separate surface is authorized.

The final model must define event identity/type, finding identity, reviewer/correction/human
authority, severity and blocking observations, remediation content/reference, source records,
artifact locator, commit/baseline, provenance, prior-event binding, ordering, event hash and ledger
hash. It must define required/optional behavior, validation, duplicates, replay/idempotency,
PUBLICATION_INTENT/RECOVERY_ROOT carry-forward and restart reconstruction across the complete logical
lineage.

The exact CONTROL or other selected existing GateRecord variant must legally contain the
RemediationEvidence needed for `ADDRESSED — AWAITING INDEPENDENT REVIEW`; the contract may not rely
on fields rejected by its own `additionalProperties:false` model.

## 8. CORR-013-04 — Deterministic effective-severity fold

Correct `EB006-IR5-04` by distinguishing immutable observed severity from canonical effective current
severity and defining one exact event-fold algorithm. If an accepted human reclassification can
lower severity, define the deterministic epoch/baseline or equivalent semantics, including how later
reviewer observations retain, escalate or propose a non-authoritative decrease.

The algorithm must uniquely resolve:

1. MEDIUM → reviewer HIGH;
2. HIGH → reviewer MEDIUM without human authority;
3. HIGH → accepted human MEDIUM;
4. human MEDIUM → later reviewer HIGH;
5. human MEDIUM → later reviewer LOW;
6. repeated equal severity;
7. recurrence after verification; and
8. closed or superseded occurrences.

For every case define effective severity, blocking, ledger-hash contribution and no-progress effect.
Blocking must use one exact transition/fold rule driven by the same canonical event history. No new
actor or authority is authorized.

## 9. Mandatory integrated consistency

CORR-013 must be implemented as one model:

- fixtures instantiate separate pending-card and accepted-resolution records;
- fixtures instantiate the actual GateRecord finding-event/remediation carrier;
- restart derives the same effective severity and blocking from persisted events;
- severity, blocking, PASS, ledger and no-progress use one canonical current finding state;
- offline authority and ordinary decision lookup use the same accepted-resolution application;
- all new structures use the already verified `CJ`, `CF`, `H` and `HB` contract unchanged;
- decision and finding fields integrate with HD-FAL-012/014 recovery without changing discovery; and
- exactly five surfaces remain.

If these relationships cannot be reconciled, stop without partial completion and request the missing
governance authority.

## 10. Consolidation and replacement strategy

CORR-013 is explicitly permitted and expected to replace or consolidate the affected final EB-006
subsections rather than append another higher-numbered normative overlay. Remove contradictory or
obsolete final text, preserve traceability, and leave one obvious executable normative answer for
fixtures, decisions and findings.

This permission applies only to EB-006 documentation structure. It does not reopen the verified
canonical-hash or recovery-discovery contracts and does not authorize architecture redesign.

## 11. Authorized change surface

The correction may modify only:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`; and
- `docs/README.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md` only as required to
  record correction state, verification evidence and the IR6 gate.

It may not modify the FAL-002 specification, runtime/production code, tests, runtime schemas,
committed fixture implementation, dependencies, versions, Audio Recorder, FAL-001 history or
unrelated architecture/governance artifacts.

## 12. Architecture and scope constraints

HD-FAL-012 and HD-FAL-014 remain binding. CORR-013 may not introduce:

- a sixth boundary/persistence surface;
- a global mutable current-series or authority pointer;
- a new state, recovery, decision or governance authority;
- a new role, module, adapter or dependency;
- generalized database, transaction, consensus, remote-service or directory-enumeration authority;
- reset of scope, criteria, policy, correction count, finding/decision/progress history or ordinal; or
- a new semantic decision identity merely to escape physical obstruction.

## 13. Budget disposition

`HD-FAL-009` remains controlling:

- expected production implementation: approximately 1,660 LOC;
- hard maximum: 1,800 LOC;
- margin: 140 LOC;
- production modules: 4;
- adapters: 2;
- schema surfaces: 5; and
- new dependencies: zero.

This decision changes no budget and does not reopen `EB006-FR-07`. Concrete evidence that the
corrected design structurally exceeds 1,800 LOC requires immediate stop and
`BUDGET AUTHORITY REQUIRED`.

## 14. Completion criteria

CORR-013 is complete only when:

1. the fixture oracle contains no normative placeholders;
2. every fixture constructor is totally instantiated;
3. every negative mutation has exact operation, path, value and result;
4. pending decision and accepted resolution are separate canonical records;
5. active binding distinguishes pending-card and accepted-resolution references;
6. origin GateRecord legally represents required initial decision state;
7. logical-lineage lookup deterministically finds and applies the accepted resolution;
8. offline authority uses that same resolution model;
9. immutable finding events have a legal GateRecord carrier;
10. RemediationEvidence has a legal GateRecord carrier;
11. finding history is restart-reconstructable;
12. recovery carries finding history without reset;
13. effective severity has one deterministic event-fold rule;
14. human downgrade semantics are unambiguous;
15. later escalation after downgrade is unambiguous;
16. blocking derives deterministically;
17. PASS uses the same canonical finding state;
18. no-progress uses the same canonical finding state;
19. fixtures cover corrected decision and finding models;
20. verified hash and recovery-discovery contracts remain unchanged;
21. exactly five surfaces remain;
22. production planning remains within 1,800 LOC; and
23. no unauthorized implementation artifact changes.

## 15. Finding-status discipline

This authorization does not correct, verify, resolve or close any IR5 finding. During correction, the
maximum correction-agent claim for each is `ADDRESSED — AWAITING INDEPENDENT REVIEW`. Only a fresh
independent read-only Standard-Assurance Review IR6 may verify the corrected contracts. Even an IR6
PASS would not authorize FAL-002 implementation; a later separate Human Decision would be required.

## 16. Stop conditions

Stop before or during correction if work requires changing the FAL-002 specification, scope,
criteria, HD-FAL-012/014 architecture, surface allocation, authority, role, module, adapter,
dependency or production budget; modifying implementation/test/schema/fixture code; reopening the
verified `CJ`/`CF`/`H`/`HB` or recovery-discovery contracts; or using a path outside section 11.

## 17. Required verification and next review

The correction commit must run repository tests, Ruff lint, Ruff format check, Git diff check,
Project Memory Health and Repository Status and verify the complete changed-file list. It must then
receive a fresh independent read-only Standard-Assurance Review IR6 against the exact committed
baseline.

IR6 must reassess all four IR5 findings, total fixture reconstruction, pending-card/resolution
separation, logical-lineage/offline lookup, finding-event persistence, restart derivation, severity/
blocking fold, PASS/no-progress integration, five-surface architecture and budget.

## 18. Explicit exclusions

This decision does not:

- execute CORR-013 or modify EB-006;
- implement FAL-002, schemas, fixtures, tests or runtime behavior;
- modify the FAL-002 specification;
- verify or close any IR5 finding;
- accept residual risk or produce PASS, eligibility or closure;
- authorize FAL-002 implementation;
- change FAL-001 or its correction history; or
- authorize push, tag, merge, release, packaging, distribution, publication or version change.

## 19. Resulting governance state

- `HD-FAL-016`: `ACCEPTED`.
- IR5 outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
- `CORR-013-01` through `CORR-013-04`: `AUTHORIZED — NOT STARTED` as one bounded campaign.
- `EB006-IR5-01` through `EB006-IR5-04`: open; none corrected, verified or closed by this decision.
- CORR-012-01/EB006-IR4-01 and CORR-012-03/EB006-IR4-03 retain their IR5 `VERIFIED`
  dispositions but are not closed.
- HD-FAL-012 and HD-FAL-014: binding architecture; not reopened.
- EB-006: unchanged by this authorization decision.
- FAL-002 specification: unchanged.
- FAL-002 implementation: `NOT AUTHORIZED`.
- Boundary surfaces: unchanged at five planned surfaces.
- Budget: approximately 1,660 expected / 1,800 maximum new production LOC.
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 20. Next permitted step

Execute the complete bounded `CORR-013-01`–`CORR-013-04` EB-006 documentation correction in one
separate commit using only section 11 paths. Then conduct fresh independent read-only
Standard-Assurance Review IR6. Neither step may infer Implementation Authorization.
