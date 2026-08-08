# HD-FAL-015 — Authorize EB-006 Fourth Residual Assurance Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Governance Authority

Provenance: Explicit user governance authorization in the Codex task titled
`HD-FAL-015 — Authorize EB-006 Fourth Residual Assurance Correction` against branch `main`, commit
`725ed3a97749df848ac855d19f7be5804dfa0da4`
(`docs(forge): clarify FAL-002 recovery discovery`), with clean working tree and empty staging.

Review basis: Independent Standard-Assurance Review IR4, canonically interpreted as
`FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`, with five open blocking findings,
`EB006-IR4-01` through `EB006-IR4-05`.

Architecture basis: `HD-FAL-012` and `HD-FAL-014`. HD-FAL-014 provided the missing architecture
authority for IR4-03 and removed the architecture dependency blocking later correction of IR4-04.
Neither architecture decision corrected, verified or closed a finding.

## 1. Verified baseline and current state

Before substantive work, the repository baseline was verified as:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `725ed3a97749df848ac855d19f7be5804dfa0da4`;
- commit subject: `docs(forge): clarify FAL-002 recovery discovery`;
- working tree: clean; and
- staging: empty.

Current governance state at this decision:

- `HD-FAL-011`, `HD-FAL-012`, `HD-FAL-013` and `HD-FAL-014`: `ACCEPTED`;
- IR4 outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`;
- `EB006-IR4-01` through `EB006-IR4-05`: open;
- CORR-012: not authorized before this decision;
- FAL-002 implementation: `NOT AUTHORIZED`; and
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 2. Governance assessment

All five IR4 findings are now correctable through one bounded EB-006 documentation/planning
correction within:

- the approved FAL-002 capability specification;
- the `HD-FAL-012` successor-series architecture;
- the `HD-FAL-014` discovery, publication-intent and decision-continuity clarification;
- the existing five boundary surfaces;
- the existing production-module, adapter and dependency boundaries; and
- the existing approximately 1,660 expected / 1,800 maximum production-LOC envelope.

No finding requires another architecture selection, capability-scope change, criterion change,
sixth surface, mutable pointer, new authority, role, adapter, production module, dependency or budget
increase before documentation correction can begin.

The five objectives are interdependent repairs to one canonical model, fixture oracle, recovery,
decision lookup and finding-control contract. They form one correction campaign, not five independent
scope expansions.

## 3. Finding disposition and authorization mapping

| Finding | Severity | Governance disposition | Authorized objective |
| --- | --- | --- | --- |
| `EB006-IR4-01` | `CRITICAL` | correction-ready within existing canonical-model authority | `CORR-012-01` |
| `EB006-IR4-02` | `HIGH` | correction-ready within existing fixture/test-planning authority | `CORR-012-02` |
| `EB006-IR4-03` | `CRITICAL` | architecture authority supplied by HD-FAL-014; normative EB incorporation remains | `CORR-012-03` |
| `EB006-IR4-04` | `HIGH` | architecture dependency removed by HD-FAL-014; exact logical-lineage lookup remains | `CORR-012-04` |
| `EB006-IR4-05` | `CRITICAL` | correction-ready within existing finding/ledger/no-progress authority | `CORR-012-05` |

Authorization changes no finding status. All five remain open.

## 4. Decision

Authorize exactly one bounded coherent EB-006 documentation correction campaign containing:

- `CORR-012-01` → `EB006-IR4-01`;
- `CORR-012-02` → `EB006-IR4-02`;
- `CORR-012-03` → `EB006-IR4-03`;
- `CORR-012-04` → `EB006-IR4-04`; and
- `CORR-012-05` → `EB006-IR4-05`.

All five objectives must be completed and committed together. Partial local completion does not make
EB-006 review-ready. The correction agent may record interim work in the working tree but may not
claim verification, closure, PASS, Implementation Authorization or partial readiness.

## 5. CORR-012-01 — Universal canonical hash-preimage contract

Correct `EB006-IR4-01` by establishing exactly one universal rule that explicitly distinguishes:

1. persisted canonical record/file bytes; and
2. canonical bytes supplied as input to `H(...)`.

The corrected EB-006 must define, without competing normative clauses:

- terminal-LF treatment for both byte categories;
- UTF encoding and invalid-Unicode behavior;
- object-key and set-valued-array ordering;
- separators, escaping and insignificant whitespace;
- null versus absent fields;
- timestamp normalization;
- exact hash preimage composition;
- SHA-256 algorithm and lowercase hexadecimal output; and
- explicit domain separation for every identity whose contract requires it.

Every normative hash use must be reconciled under that rule, including boundary record, payload,
content, provenance, grant, finding identity, ledger, progress, conflict-card, recovery-condition,
recovery-discovery, publication-intent and fixture hashes.

Local exceptions are forbidden unless they are explicitly named, semantically necessary and fully
canonical. The correction must remove or mark historical every conflicting LF/no-LF rule; precedence
language alone is insufficient when two incompatible exact definitions remain plausibly normative.

## 6. CORR-012-02 — Complete independent fixture oracle

Correct `EB006-IR4-02` by making every required fixture independently reproducible without importing
or copying production canonicalization, hashing, generated schema or validation logic.

The oracle contract must supply complete literal primitives and exact nested values for every
constructor, including as applicable:

- HumanDecisionRecord owner, provenance, question, target, sources, choices and rationale;
- invocation grants, context IDs and observations;
- inventory files, edges, counts, dependency hashes and unresolved/exemption arrays;
- executor and reviewer request/result containers;
- all RunRecord runtime, tool, repository, command, diff and build values;
- EvidenceBindings and semantic rationales;
- finding observations, remediation evidence, ledger snapshots and progress snapshots;
- publication intents, obstruction descriptors, recovery roots and discovery candidates; and
- decision requirements, binding generations, physical records and resolutions.

Every mutation must name the exact source constructor/case, exact RFC 6901 pointer or other fully
defined canonical location, exact operation, exact value, rehash behavior, expected canonical bytes
or rejection, expected hashes, final filesystem/state, reason code and replay result.

Phrases such as “different valid bytes”, “delete command index 1”, “modify the gate” or “change the
hash” are not sufficient without one uniquely constructable source object and exact operation.

The final oracle must apply the CORR-012-01 universal hash rule and cover every corrected contract.
Production constants or helpers may not generate expected values.

## 7. CORR-012-03 — Normative incorporation of HD-FAL-014

Correct `EB006-IR4-03` by incorporating, not redesigning, the accepted HD-FAL-014 architecture.

### 7.1 PUBLICATION_INTENT

Define `PUBLICATION_INTENT` as a GateRecord form with exact:

- requirement and exemption conditions;
- payload field shape and canonical types;
- predecessor and publication-slot binding;
- target surface, record ID and canonical path;
- intended-record hash/commitment and reconstruction classification;
- provenance, sequence and state semantics;
- validation and universal hashing;
- staged and final persistence order;
- crash/replay/idempotency behavior; and
- fail-closed dispositions.

It commits publication facts under existing GateRecord state authority. It is not a separate business
decision, state authority or sixth surface. The correction must state whether the assurance/business
state label is retained while the publication facts advance in sequence.

### 7.2 Semantic recovery identity

Define the complete canonical `recovery_condition_hash` preimage and ordering. It describes why
recovery exists and retains intended-record and obstruction evidence.

### 7.3 Physical discovery identity

Define the complete canonical `recovery_discovery_key` input selected by HD-FAL-014. It derives only
from authoritative persisted origin, predecessor GateRecord and publication-slot facts available to a
fresh consumer. Intended output and ephemeral process state cannot be locator dependencies.

### 7.4 Successor candidates and discovery

Define the binding namespace/domain, UUIDv5 name, ordinal representation, exact candidate path,
smallest-eligible rule, target inspection, validation, collision behavior, first-absent termination,
external-repair limit and complete fresh-consumer traversal from the authoritative origin.

Directory presence, heuristic directory enumeration, staging and `current.json` cannot establish
authority. Only a valid RECOVERY_ROOT with exact predecessor, publication-slot, discovery,
semantic-condition and carry-forward bindings changes the active segment.

### 7.5 Decision rebinding and replay

Define how the same stable semantic `decision_identity` receives a newer physical active-lineage
binding generation after obstruction without changing question, domain, choices or semantic target.
Cover crashes and replay before/after intended-byte stage, publication intent, attempted target final,
obstruction detection, candidate root, RECOVERY_ROOT final and decision-record rebinding.

All behavior must remain within GateRecord and HumanDecisionRecord surfaces.

## 8. CORR-012-04 — Complete logical-lineage decision lookup

Correct `EB006-IR4-04` by operationalizing HD-FAL-014 for every HumanDecisionRecord and offline-
authority lookup.

The corrected contract must define exactly:

1. lookup begins at the logical-lineage origin;
2. each successor is accepted only through validated GateRecord lineage bindings;
3. the complete decision-requirement ledger is derived in logical-lineage order;
4. only the latest valid active-lineage binding generation for one semantic decision identity is
   authoritative;
5. physical locator and record ID derive deterministically from that binding;
6. inactive, orphan, forked and unjustified-higher-ordinal decision records are evidence only;
7. record schema, canonical bytes, hash, semantic identity, payload hash, binding generation,
   target, status and choice are validated;
8. an earlier accepted resolution may satisfy a rebound requirement only when the active GateRecord
   lineage explicitly carries its immutable exact reference;
9. offline-evidence locator, content hash, decision hash, policy hash and freshness are validated;
10. missing, malformed, stale, unavailable, declined or mismatched data receives one exact fail-
    closed disposition; and
11. replay reuses the same identity/binding and never creates a default or competing resolution.

The phrases “same series decision path” and “canonical decision path” must be replaced by this one
complete logical-lineage algorithm. Offline authority must resolve identically before and after
physical recovery, subject only to its explicit freshness rules.

## 9. CORR-012-05 — Deterministic finding evolution

Correct `EB006-IR4-05` inside the existing stable finding identity and complete-lineage ledger. Do
not create a parallel finding system.

### 9.1 Severity

Define one exact authority and transition rule for unchanged, increased and decreased severity. State
whether decreases require fresh reviewer evidence, human disposition or are forbidden. Preserve
historical values and define the sole current value used by eligibility and hashes. Implementations
may not choose independently between latest-value, maximum-severity or another rule.

### 9.2 Blocking status

Define whether `blocking` is intrinsic, reviewer-observed, severity-derived or explicitly
transitioned; define the one permitted evolution rule and authority. Historical values remain
append-only. No implementation-local OR, last-write-wins or inferred mapping is allowed.

### 9.3 Remediation evidence

Define the exact canonical evidence required for transition from OPEN to
`ADDRESSED_AWAITING_REVIEW`, including evidence kind, source authority, artifact/record ID, locator,
content/record hash, correction objective, remediation claim, timestamp/order and validation.
Missing or incomplete evidence must leave the finding OPEN or fail the transition. Executor or
correction-agent remediation claims never become independent verification.

### 9.4 Recurrence and disposition

Define exact behavior when an addressed finding remains present, an independently verified finding
recurs, a closed/superseded defect materially reappears, severity/blocking changes, or a locator moves.
Automatic semantic collapsing remains forbidden; any equivalence/supersession across different keys
requires the already human-owned disposition mechanism.

### 9.5 Eligibility and no-progress

One canonical current FindingLedger state must feed unresolved finding hashes, introduced-blocker
logic, no-progress, PASS eligibility and closure. Recovery cannot reset it. Add fixtures for severity
increase/decrease, blocking transition, invalid transition, missing/valid remediation evidence,
recurrence, supersession and incomplete history.

## 10. Mandatory cross-correction consistency

CORR-012 is complete only as one coherent model:

- hash contract ↔ fixture oracle: every expected hash uses the universal rule;
- publication intent ↔ hash contract: commitment and record hashes use the same canonical semantics;
- semantic recovery ↔ physical discovery: separate preimages, one shared canonical encoding rule;
- recovery ↔ decision lookup: rebinding and offline resolution use the same logical lineage;
- finding evolution ↔ no-progress: fingerprints use the canonical current ledger;
- finding evolution ↔ PASS/closure: the same ledger and unresolved definition govern eligibility;
- fixtures ↔ all contracts: every changed valid, invalid, crash and replay rule has independent
  expected evidence; and
- precedence ↔ final model: no contradictory earlier exact definition remains plausibly normative.

If one objective cannot be reconciled with the others, stop the campaign without claiming partial
completion and request the missing governance authority.

## 11. Authorized change surface

The correction may modify only:

- `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`; and
- `docs/README.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md` and `AI_HANDOFF.md` only as required to
  record correction state, verification evidence and the next IR5 review gate.

No other path is implicitly authorized. In particular, CORR-012 may not modify:

- the FAL-002 capability specification;
- Forge runtime code or tests;
- committed runtime schemas or fixture implementation;
- dependency or version files;
- Audio Recorder or album artifacts;
- FAL-001 artifacts or history; or
- unrelated capability, architecture, release or governance records.

## 12. Architecture and scope constraints

HD-FAL-012 and HD-FAL-014 are binding. The correction must implement their selected architecture and
may not introduce:

- a sixth boundary/persistence surface;
- a global mutable current-series or authority pointer;
- a new recovery, state or decision authority;
- a new role, executor/reviewer adapter, production module or dependency;
- generalized transaction, database, consensus, remote service or directory-heuristic authority;
- reset of scope, criteria, policy, correction count, ordinal, findings, decisions or progress; or
- a new semantic decision identity solely to escape physical collision.

If correction requires changed capability scope/criteria, FAL-002 specification, architecture,
surface allocation, authority, role, module, adapter or dependency, stop with the corresponding
governance-authority requirement.

## 13. Budget disposition

`HD-FAL-009` remains controlling:

- expected production implementation: approximately 1,660 LOC;
- hard maximum: 1,800 LOC;
- current margin: 140 LOC;
- planned production modules: unchanged;
- executor/reviewer adapters: unchanged;
- boundary surfaces: five; and
- new dependencies: zero.

This decision changes no budget and does not reopen `EB006-FR-07` without new material evidence.
CORR-012 must reconcile bottom-up inventory and allocation text after incorporating publication intent
and decision rebinding. Concrete evidence that the complete design structurally exceeds 1,800 LOC
requires immediate stop and `BUDGET AUTHORITY REQUIRED`.

## 14. Completion criteria

CORR-012 is complete only when:

1. one universal canonical hash-preimage rule exists;
2. persisted file bytes and hash-preimage bytes are unambiguously distinguished;
3. every normative `H(...)` use is reconciled;
4. every fixture primitive, nested value and mutation is independently reconstructable;
5. HD-FAL-014 is fully and normatively represented in EB-006;
6. PUBLICATION_INTENT is unambiguously a GateRecord form;
7. successor discovery uses only authoritative persisted derivation material;
8. semantic recovery identity and physical discovery identity are distinct and exact;
9. decision identity survives physical rebinding without semantic replacement;
10. logical-lineage HumanDecisionRecord lookup is total and deterministic;
11. offline evidence resolves under that same lookup before and after recovery;
12. severity and blocking evolution are canonical;
13. remediation evidence and authority are explicitly modeled;
14. recurrence, closure and supersession behavior are exact;
15. no-progress consumes deterministic canonical finding state;
16. PASS and closure eligibility consume the same complete-lineage ledger;
17. independent fixtures cover every changed contract and crash/replay boundary;
18. exactly five boundary surfaces remain;
19. bottom-up production planning remains within the 1,800-LOC maximum;
20. no unauthorized artifact is changed;
21. repository tests, lint, format, diff check, Project Memory Health and Repository Status pass; and
22. every correction/finding status is recorded only as
    `ADDRESSED — AWAITING INDEPENDENT REVIEW`.

## 15. Finding-status discipline

This authorization does not correct, verify, resolve or close a finding. During correction, the
maximum correction-agent claim for each IR4 finding is:

`ADDRESSED — AWAITING INDEPENDENT REVIEW`

Only a fresh independent read-only Standard-Assurance Review IR5 may verify the corrected contracts.
Even an IR5 PASS would not authorize FAL-002 implementation; a later separate Human Decision would
still be required.

## 16. Stop conditions

Stop before or during correction if work requires:

- changing the FAL-002 capability specification, scope or criteria;
- reopening HD-FAL-012 or HD-FAL-014 architecture;
- another surface, mutable pointer, authority, role, module, adapter or dependency;
- a production-budget increase;
- implementation experiments, runtime/test/schema/fixture-code changes;
- a path outside section 11; or
- an inconsistent partial correction that cannot satisfy section 10.

Preserve evidence, claim no completion and request the missing Human Decision.

## 17. Required verification and review

The correction commit must run repository-standard tests, Ruff lint, Ruff format check, Git diff
check, Project Memory Health and Repository Status. It must verify the complete changed-file list
before commit.

After the correction is committed separately, the only next review gate is a fresh independent
read-only Standard-Assurance Review IR5 against that exact committed baseline. IR5 must reassess all
five findings, the universal hash model, full independent oracle, HD-FAL-014 incorporation,
publication-intent/recovery/decision crash paths, complete-lineage lookup, finding evolution,
no-progress, PASS/closure, five-surface boundary and budget.

## 18. Explicit exclusions

This decision does not:

- execute CORR-012 or modify EB-006;
- implement FAL-002, schemas, fixtures, tests or runtime behavior;
- modify the FAL-002 specification;
- verify or close any IR4 finding;
- accept residual risk or produce PASS/eligibility/closure;
- authorize FAL-002 implementation;
- change FAL-001 or its correction history; or
- authorize push, tag, merge, release, packaging, distribution, publication or version change.

## 19. Resulting governance state

- `HD-FAL-015`: `ACCEPTED`.
- IR4 outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
- `CORR-012-01` through `CORR-012-05`: `AUTHORIZED — NOT STARTED` as one bounded campaign.
- `EB006-IR4-01` through `EB006-IR4-05`: open; none corrected, verified or closed by this decision.
- HD-FAL-012 and HD-FAL-014: binding architecture; not reopened.
- EB-006: unchanged by this authorization decision.
- FAL-002 specification: unchanged.
- FAL-002 implementation: `NOT AUTHORIZED`.
- Boundary surfaces: unchanged at five planned surfaces.
- Budget: approximately 1,660 expected / 1,800 maximum new production LOC.
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 20. Next permitted step

Execute the complete bounded `CORR-012-01`–`CORR-012-05` EB-006 documentation correction in one
separate commit, using only section 11 paths. Then conduct a fresh independent read-only
Standard-Assurance Review IR5. Neither step may infer Implementation Authorization.
