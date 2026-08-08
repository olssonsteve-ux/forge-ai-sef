# HD-FAL-009 — Reconcile FAL-002 Implementation Scope and Production LOC Budget

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Human Product Owner / Forge Design Authority

Provenance: Explicit user authorization in the Codex task titled
`HD-FAL-009 — Reconcile FAL-002 Implementation Scope and Production LOC Budget`.

Decision baseline: branch `main`, commit
`80afc9671ea545eba195cf999d3c065998e7fd02` (`docs(forge): authorize EB-006 residual correction`),
clean working tree and empty staging area.

## Context

`HD-FAL-008` authorized bounded documentation correction of `EB006-FR-01` through `EB006-FR-07`.
Correction stopped at `CORR-008-07` because the already specified FAL-002 scope did not fit either
the EB-006 plan of 1,100 new production LOC or the normative ceiling of 1,200 counted production
lines. No correction file or implementation artifact was changed after that escalation.

FAL-002 remains unimplemented and `NOT AUTHORIZED`. FAL-001 remains permanently `TERMINATED
BLOCKED`, unaccepted and unclosed, with correction count 2/2.

## Trigger for escalation

The required bottom-up reconciliation estimated 1,660 new production LOC. That is 560 LOC above the
EB-006 plan and 460 LOC above the prior normative ceiling. Existing production code safely reusable
by the planned FAL-002 runtime is zero LOC because the frozen plan prohibits importing FAL-001
runtime and requires new canonical contracts.

`HD-FAL-008` prohibited a local budget increase, reduction of normative requirements or artificial
code compression and therefore required this separate Human Decision.

## Evidence reviewed

- the FAL-002 hard-size rule and counting algorithm in specification section 13;
- the EB-006 production structure, budget and hard-limit verification rows;
- `HD-FAL-008`, especially `CORR-008-07` and its stop/escalation condition;
- the 1,660-LOC bottom-up estimate and its module responsibilities;
- the existing FAL-001 implementation size as comparative evidence only, not reusable scope; and
- Constitution, AI Engineering Conduct and lifecycle/implementation standards for any higher-order
  restriction on budget adjustment.

No higher governing source fixes the FAL-002 ceiling at 1,200 LOC. The limit is a FAL-002 complexity
guardrail and may be reconciled by this explicit Product Owner / Forge Design Authority decision.

## Bottom-up budget analysis

| Module | Required responsibility | Estimated new production LOC |
| --- | --- | ---: |
| `forge/fal002.py` | State machine, orchestration, corrections, decisions and closure | 330 |
| `forge/fal002_model.py` | Five canonical models, validation, serialization, hashes and schema generation | 420 |
| `forge/fal002_inventory.py` | AST traversal, dynamic edges, exemptions, LOC and dependency inventory | 360 |
| `forge/fal002_io.py` | Create-only persistence/recovery, collectors/parsers, redaction and adapters | 550 |
| **Bottom-up total** | **Already specified FAL-002 implementation scope** | **1,660** |

The new ceiling is 1,800 new production LOC, leaving 140 LOC unallocated margin, approximately
8.4 percent of the expected implementation. Test LOC, fixture LOC and documentation are excluded.
Purely derivative generated schemas remain governed by the existing FAL-002 generated-code and
schema-surface policy. No new dependency is authorized.

## Decision

Replace the FAL-002 normative production-LOC ceiling with:

`at most 1,800 new counted production lines`

The expected implementation remains approximately 1,660 new production LOC. The 1,800 ceiling is a
maximum implementation envelope, not a target. This decision reconciles budget authority for the
already approved scope; it does not expand capability scope or authorize implementation.

## Authorized changes

Authorize only:

1. replacement of the FAL-002 normative production-LOC budget rule from 1,200 counted production
   lines to at most 1,800 new counted production lines;
2. corresponding EB-006 budget-row and budget-reference synchronization to the 1,660 expected /
   1,800 maximum envelope;
3. this Human Decision and necessary governance-index/project-memory updates; and
4. resumption of the documentation correction already authorized by `HD-FAL-008` after this
   decision is committed separately.

## Explicit exclusions

This decision does not authorize reduction or reinterpretation of boundary contracts, state-machine
precision, crash recovery, collectors, reviewer independence, schemasurfaces, scenariofixtures,
interruption points or `FAL2-CC-01` through `FAL2-CC-16` coverage. It does not authorize FAL-001
runtime reuse, new dependencies, production/runtime/test code, schemas, fixtures, implemented
adapters or collectors, persistence structures, version changes, Audio Recorder work, finding
closure, Implementation Authorization, release, packaging or distribution.

No non-budget FAL-002 requirement changes. The budget adjustment cannot be used as indirect scope
expansion.

## Revised normative LOC ceiling

| Budget fact | Value |
| --- | ---: |
| Prior EB-006 plan | 1,100 new production LOC |
| Prior normative ceiling | 1,200 counted production LOC |
| Expected implementation | 1,660 new production LOC |
| Revised normative ceiling | 1,800 new production LOC |
| Unallocated margin | 140 new production LOC |

The existing inventory algorithm continues to attribute, count and report every reached production
module and physical counted line. It must report unchanged attributed baseline LOC separately from
new production LOC; baseline LOC is not reusable implementation credit and does not consume the new
LOC envelope.

## Guardrails

- The ceiling is a maximum envelope, never a target or permission to add work.
- Normative behavior cannot be removed or compressed to meet the ceiling.
- Code cannot be added merely to consume margin.
- Production logic cannot be hidden in tests, fixtures, generated artifacts, unusual generation,
  wrappers, file movement or accounting classifications.
- Clarity, auditability, assurance and literal contract behavior outrank code compression.
- The existing module, adapter, schemasurface, sequential-execution and dependency limits remain
  unchanged.
- More than 1,800 new production LOC requires another Human Decision before implementation may
  continue.

## Relationship to HD-FAL-008

`HD-FAL-008` remains accepted and otherwise unchanged. `CORR-008-01` through `CORR-008-06` retain
their exact scope. `CORR-008-07` may resume using the 1,660 expected / 1,800 maximum budget. The full
bounded EB-006 documentation correction must then be completed and verified.

All of `EB006-R1` through `EB006-R3` and `EB006-FR-01` through `EB006-FR-07` remain open for fresh
independent reassessment. This budget decision closes or verifies none of them.

## Required next step

Commit this governance/budget reconciliation separately. Then resume only the bounded EB-006
documentation correction authorized by `HD-FAL-008`. The corrected brief must undergo a fresh
independent read-only Standard-Assurance review before any separate Human Decision may consider
Implementation Authorization.

## Resulting governance state

- `HD-FAL-009`: `ACCEPTED`.
- FAL-002 normative production-LOC ceiling: at most 1,800 new counted production lines.
- EB-006 expected production implementation: approximately 1,660 new LOC with 140 LOC margin.
- EB-006 bounded documentation correction: authorized to resume after this separate commit.
- FAL-002 implementation: `NOT AUTHORIZED`.
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.
- All ten EB-006 findings: open for fresh independent review.
