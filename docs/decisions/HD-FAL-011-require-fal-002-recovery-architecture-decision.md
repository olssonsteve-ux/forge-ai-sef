# HD-FAL-011 — Require FAL-002 Recovery Architecture Decision Before Further EB-006 Correction

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Design Authority

Provenance: Explicit user governance instruction in the Codex task following the fresh independent
Standard-Assurance review of EB-006. The review was performed read-only against branch `main`, commit
`48c0929e19906c81b5c7b2a23209b0d4d24b02eb` (`docs(forge): complete EB-006 second residual
correction`), with clean working tree and empty staging. The review result was
`FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`. The review was delivered in the task and was
not persisted as a repository review artifact before this decision.

Addresses: governance disposition of `EB006-IR3-01` through `EB006-IR3-08` and the independently
reviewed status of `CORR-010-01` through `CORR-010-07`.

## Context

The independent IR3 review found eight blocking findings. Its executive summary referred to seven
blocking defects, while its authoritative findings section enumerated `EB006-IR3-01` through
`EB006-IR3-08`. This decision treats that count mismatch as editorial and preserves all eight
findings.

The review independently assessed `CORR-010-03` and `CORR-010-04` as `VERIFIED`;
`CORR-010-01`, `CORR-010-02`, `CORR-010-05` and `CORR-010-07` as `PARTIALLY VERIFIED`; and
`CORR-010-06` as `NOT VERIFIED`. Verification is not finding closure. Residual defects are now
represented by the IR3 findings below, and already verified portions must not be reopened without
new material evidence.

FAL-002 remains unimplemented and `NOT AUTHORIZED`. FAL-001 remains permanently
`TERMINATED BLOCKED`, unaccepted and unclosed, with correction count 2/2 and unchanged history.

## Finding disposition

| Finding | Governance assessment | Correctable within current EB-006 documentation authority | Required disposition |
| --- | --- | --- | --- |
| `EB006-IR3-01` | The criterion-evidence boundary omits specification-required `evidence_kind` and `assertion`. | `YES` | Correction-ready after the architecture gate; synchronize the exact boundary, schema-generation contract, hashing, validation and fixtures with FAL-002 §10. |
| `EB006-IR3-02` | Invocation containers and closure-domain placement are incomplete or contradictory. | `YES` | Correction-ready after the architecture gate; define one complete final nested model with no superseded competing shape. |
| `EB006-IR3-03` | The fixture generator does not uniquely determine every primitive, mutation, byte sequence and expected hash. | `YES` | Correction-ready after the architecture gate; define a production-independent, fully reconstructable oracle. |
| `EB006-IR3-04` | An occupied or invalid next canonical gate path prevents the single authoritative state series from recording a terminal fail-closed state. | `NO` | Requires a separate accepted recovery/state architecture decision before EB-006 correction. |
| `EB006-IR3-05` | The conflict-card hash preimage is underdefined, and occupied/invalid card recovery is not total. | `PARTIAL` | The exact preimage is correction-ready, but total authoritative publication depends on the IR3-04 architecture decision. The finding cannot be assigned to correction before that decision. |
| `EB006-IR3-06` | Tool/runtime-version evidence and offline-decision resolution are incomplete. | `YES` | Correction-ready after the architecture gate; define collector-owned fields, parsing, accepted-decision resolution, locators, binding and failure behavior. |
| `EB006-IR3-07` | No cross-review finding lifecycle prevents omission of unresolved historical blockers. | `YES` | Correction-ready within existing surfaces after the architecture gate; use existing review, gate and eligibility records and add no persistence surface. |
| `EB006-IR3-08` | The no-progress function lacks an exact comparison window, operands and precedence. | `YES` | Correction-ready after the architecture gate; define one deterministic function over canonical series evidence. |

## Architecture authority determination

### `EB006-IR3-04`

Resolution is outside current EB-006 correction authority. FAL-002 §8 declares one append-only state
series authoritative. EB-006 derives the next gate's identity and path from its sequence. If that
canonical final path is occupied by invalid bytes, the current model permits neither overwrite,
delete, rename, sequence skipping nor an authoritative alternate state path. A diagnostic or a
decision card cannot substitute for authoritative gate state.

Resolving this requires an explicit architecture decision selecting and bounding a recovery model,
for example an authorized successor-series relationship or another authoritative corruption
disposition. That decision must define identity, history/count carry-forward, authority, closure,
surface accounting, replay and failure semantics. The correction agent may not select the model.

### `EB006-IR3-05`

The canonical source-array/hash preimage can be defined within EB-006. Total recovery cannot yet be:
an occupied invalid card path requires a governed alternate identity or recovery relationship, and
the resulting state transition still depends on the IR3-04 solution. No alternate semantic ID,
surface or authority mechanism is authorized by this decision.

## Decision

Accept the independent IR3 review result:

`FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`

Do not authorize a third EB-006 residual correction at this gate. `CORR-011-01` through
`CORR-011-08` are reserved identifiers only and are not authorized, started or completed.

Require a separate bounded FAL-002 recovery/state architecture decision before any CORR-011 work.
After that decision, a later Human Decision may authorize one coherent EB-006 correction covering
all eight IR3 findings with exact closure conditions. Correction-ready findings may be prepared for
that later decision but must not be edited now.

## Required architecture decision

The next architecture decision must, at minimum:

1. preserve the five existing boundary types unless it explicitly accounts for and authorizes a
   changed schema-surface allocation;
2. select the authoritative state representation when a canonical next gate path is occupied or
   invalid;
3. define whether and how a successor series may retain frozen scope, criteria, correction count,
   ordinals, prior findings and append-only provenance;
4. define total deterministic decision-card identity and publication for occupied or invalid paths;
5. preserve no overwrite, delete, truncate, history rewrite or evidence loss;
6. preserve human-only closure and prevent recovery from creating PASS, eligibility or closure;
7. assess production LOC, module, adapter, surface and dependency consequences before changing any
   limit; and
8. return to human governance if the selected design requires changed FAL-002 scope, criteria,
   specification or budget.

## Future correction closure conditions

This decision does not authorize these corrections. A later correction decision must use the
reserved mapping and require at least:

| Reserved objective | Finding | Minimum closure condition for later authorization |
| --- | --- | --- |
| `CORR-011-01` | `EB006-IR3-01` | Every criterion binding contains the complete FAL-002 §10 field set with exact canonical, schema, hash, validation and fixture behavior. |
| `CORR-011-02` | `EB006-IR3-02` | Executor/reviewer invocation containers and closure decision domain have one complete, non-conflicting canonical shape. |
| `CORR-011-03` | `EB006-IR3-03` | Every fixture/subcase is independently reconstructable to exact bytes, IDs and hashes without production constants or logic. |
| `CORR-011-04` | `EB006-IR3-04` | The architecture-selected mechanism records one authoritative fail-closed state for every occupied/invalid final-path case. |
| `CORR-011-05` | `EB006-IR3-05` | Conflict-card preimage and every crash, duplicate and occupied-path outcome are exact, total, deterministic and compatible with CORR-011-04. |
| `CORR-011-06` | `EB006-IR3-06` | RunRecord represents collector-owned runtime/tool versions and offline evidence resolves to an accepted human decision with exact locator/hash/failure rules. |
| `CORR-011-07` | `EB006-IR3-07` | Eligibility deterministically scans the complete authoritative finding lifecycle and cannot omit an unresolved historical blocker. |
| `CORR-011-08` | `EB006-IR3-08` | One exact no-progress function defines inputs, comparison window, finding equivalence, material improvement and ceiling precedence. |

No correction agent may mark these conditions verified or closed. A completed later correction must
receive another fresh independent read-only Standard-Assurance review.

## Budget disposition

`HD-FAL-009` remains controlling: approximately 1,660 expected and at most 1,800 new production LOC,
with 140 LOC margin, at most eight production modules, one adapter per role, at most six schema
surfaces and no new dependency without Human Decision. `EB006-FR-07` is not reopened. This decision
changes no budget.

The required architecture decision must provide concrete budget evidence before authorizing any
design that adds production behavior, a surface, module, adapter or dependency. A small remaining
margin alone is not evidence of a breach.

## Explicit exclusions

This decision authorizes no change to EB-006, the FAL-002 specification, Forge runtime, tests,
schemas, fixtures, dependencies, versions, Audio Recorder, FAL-001, release state or adjacent
capability. It authorizes no implementation, correction execution, finding closure, PASS,
Implementation Authorization, release, packaging, distribution or publication.

## Resulting governance state

- `HD-FAL-011`: `ACCEPTED`.
- Independent IR3 outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
- `EB006-IR3-01` through `EB006-IR3-08`: open; none closed or verified by this decision.
- `CORR-011-01` through `CORR-011-08`: reserved, `NOT AUTHORIZED`.
- EB-006: `AWAITING HUMAN REVIEW`; further correction blocked on a separate architecture decision.
- FAL-002 implementation: `NOT AUTHORIZED`.
- FAL-002 budget: unchanged at approximately 1,660 expected / 1,800 maximum new production LOC.
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.
- Next gate: separate bounded FAL-002 recovery/state architecture decision.
