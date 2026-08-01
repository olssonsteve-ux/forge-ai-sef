# EB-006 — Implement FAL-002 Standard Assurance Bounded Engineering Loop

Status: `AWAITING HUMAN REVIEW`

Date: 2026-08-01

Owner: Chief Architect

Decision basis: `HD-FAL-006`

Specification: `docs/capabilities/FAL-002-Standard-Assurance-Bounded-Engineering-Loop.md`

Implementation authorization: `NOT AUTHORIZED`

## 1. Purpose and gate

This Engineering Brief is the complete Implementation Plan for the smallest implementation of
FAL-002. It freezes concrete inputs and chooses technical structure without changing the normative
specification. No separate implementation-plan artifact is needed under the repository's existing
Engineering Brief convention.

The brief may advance only after a fresh read-only Standard-Assurance review with adversarial
instructions and an explicit human Implementation Authorization decision. Its current state does
not authorize code, schemas, fixtures or tests.

## 2. Governing authority

Implementation must follow, in order:

1. `CONSTITUTION.md` and `AI_ENGINEERING_CONDUCT.md`;
2. `HD-FAL-006` and prior preserved FAL-002 human decisions;
3. the FAL-002 specification, including its authority map and inventory algorithm;
4. `docs/architecture/FAL-002-reuse-matrix.md`;
5. this brief for concrete inputs, component allocation and implementation sequence;
6. a future separately accepted Implementation Authorization decision.

This brief does not define or reinterpret traversal, import resolution, attribution, exclusions,
dynamic-edge handling, stop conditions, module/LOC counting, adapter classification, schema-surface
semantics, dependencies, assurance naming, authority or conflict resolution. If implementation needs
a missing normative rule, the brief returns to `AWAITING_HUMAN` before being review-ready.

## 3. Frozen implementation inputs

| Input | Frozen value |
| --- | --- |
| Canonical entrypoint | `forge/fal002.py` |
| Baseline commit | `7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68` |
| Inventory Python version | `3.14` |
| First-party source roots | `forge/` |
| Executor adapter | `forge/fal002_io.py` |
| Reviewer adapter | `forge/fal002_io.py` |
| General-tool exemption candidates | `NONE` |
| Frozen exemption closures | `NONE` |
| Transitively reused FAL-001 production components | `NONE` |
| Existing allowed runtime dependencies | Python standard library only |
| New dependencies | `NONE` |
| Generator | `forge/fal002_model.py` |
| Templates | `NONE` |
| Generated artifacts | Five schema files listed below |

The package initializer `forge/__init__.py` is necessarily reached when the canonical entrypoint is
loaded and is counted as an unchanged production module. The entrypoint does not import
`forge/adaptive_loop.py`. Reuse from FAL-001 is semantic and explicitly classified in section 8; no
FAL-001 run identity, state, correction budget or runtime module is imported.

### Persisted and external boundary roots

| Stable surface ID | Canonical model root | Generated schema path |
| --- | --- | --- |
| `fal002.gate-record.v1` | `GateRecord` | `schemas/fal002/gate-record-v1.schema.json` |
| `fal002.executor-exchange.v1` | `ExecutorExchange` | `schemas/fal002/executor-exchange-v1.schema.json` |
| `fal002.run-record.v1` | `RunRecord` | `schemas/fal002/run-record-v1.schema.json` |
| `fal002.reviewer-exchange.v1` | `ReviewerExchange` | `schemas/fal002/reviewer-exchange-v1.schema.json` |
| `fal002.human-decision.v1` | `HumanDecisionRecord` | `schemas/fal002/human-decision-v1.schema.json` |

Each root is one actual persisted or exchanged unit, not a synthetic wrapper. `GateRecord` is the
single append-only record shape and its latest record is the derived snapshot representation.
Executor and reviewer exchanges each persist one lifecycle envelope from request/packet through
result. Closure is a decision kind in `HumanDecisionRecord`, not an independent payload surface.

## 4. Planned production structure

| Module | Responsibility | Must not own |
| --- | --- | --- |
| `forge/fal002.py` | Canonical entrypoint, sequential state machine, correction/no-progress control and orchestration | schema definitions, subprocess parsing, review judgment |
| `forge/fal002_model.py` | Canonical typed boundary model, validation, hashes, schema generation and closure invariant | orchestration, command execution, semantic review |
| `forge/fal002_inventory.py` | Exact specification §13 traversal, attribution, LOC, adapter/schema/dependency accounting and deterministic inventory result | exemptions not defined by §13, implementation decisions |
| `forge/fal002_io.py` | Append-only persistence, collector command/Git evidence, executor/reviewer exchange adapters and recovery checkpoints | acceptance, closure, review-result reinterpretation |
| `forge/__init__.py` | Existing package initialization | FAL-002 behavior; remains unchanged |

The four new modules are deliberately cohesive to avoid file-splitting around the module cap. Tests
may use focused files under `tests/`, but test files do not own production policy.

## 5. Canonical sequential execution flow

1. Load the frozen manifest and validate every boundary through `fal002_model`.
2. Run `fal002_inventory` before execution. Any unresolved edge, invalid exemption state, new
   dependency or hard-limit breach appends an `awaiting_human` record and stops.
3. Compile a deterministic executor exchange from frozen scope, criteria, allowed paths, command
   policy and complete-series correction count.
4. Persist the exchange and append `executing`; invoke the sole executor adapter synchronously.
5. Collector code—not executor prose—captures Git, changed paths, diff, commands, build/test totals,
   raw-output hashes, tool versions and timing into one `RunRecord`.
6. Validate and persist the run record; append `evidence_ready`.
7. Build one criterion-bound reviewer exchange and append `reviewing`; invoke the sole reviewer
   adapter synchronously in read-only mode.
8. Validate the result without default conversion. `BLOCKED`, `INCONCLUSIVE`, forbidden operations,
   missing evidence or authority conflict stop fail-closed.
9. `CORRECTION_REQUIRED` may start one sequential correction only when the complete series remains
   below two and collector hashes demonstrate material change. Identical/repeated evidence invokes
   no-progress stop.
10. `PASS` only seals technical eligibility when criterion coverage is complete and no open
    CRITICAL, blocking or human-decision-required finding exists.
11. Only a separate human-close operation with an accepted `HumanDecisionRecord` may append closed
    state. Implementation PASS does not close or release anything.

No parallelism, agent pool, scheduler, plugin, network or database path exists.

## 6. Checkpoint, failure and recovery

- Each authoritative transition is one append-only `GateRecord` written through create-new-file and
  atomic-replace primitives available in the standard library.
- Records bind series ID, sequence, predecessor hash, payload hash and record hash. Derived current
  state is rebuilt from the verified series and never outranks it.
- Exchange and run records are validated before persistence and again before state effect.
- A crash after authoritative append but before derived-state replacement recovers from the series;
  a partial/unverifiable append stops `blocked` without synthesizing progress.
- Boundary/schema failure, hash mismatch, conflicting authorities, command-policy violation,
  unresolved inventory edge, timeout or missing raw evidence stops `blocked` or `awaiting_human` as
  specified. No exception path creates PASS, eligibility or closure.
- Retry is a new execution identity inside the same series and never resets the correction count.

## 7. Planned file scope

Production files planned as new:

- `forge/fal002.py`
- `forge/fal002_model.py`
- `forge/fal002_inventory.py`
- `forge/fal002_io.py`

Generated boundary artifacts planned as new are the five paths in section 3. Planned test files:

- `tests/test_fal002_model.py`
- `tests/test_fal002_inventory.py`
- `tests/test_fal002_flow.py`
- `tests/test_fal002_recovery.py`

Implementation documentation may later update only state, handoff, indexes and implementation
evidence made inaccurate by actual work. `forge/adaptive_loop.py`, FAL-001 artifacts, release files,
Audio Recorder, packaging, versions and album artifacts are excluded.

## 8. Reuse plan

| Reuse class | Planned treatment |
| --- | --- |
| `REUSE_AS_IS` | Reimplement frozen-contract hashing, collector-owned evidence, two-correction ceiling, no-progress detection, decision cards, forbidden operations, append-only records and redaction under the FAL-002 canonical model; do not import FAL-001 runtime |
| `REUSE_AFTER_FIX` | Implement human-only sealed closure, blocking-finding rejection, canonical generated schemas, precise criterion evidence and honest reviewer execution provenance before any path can PASS |
| `DEFER_TO_HIGH_ASSURANCE` | No isolated reviewer infrastructure or external immutable anchoring |
| `DISCARD` | No generic evidence pointer, HMAC authenticity claim, FAL-001 acceptance/reset, orchestration platform, plugin system or semantic-proof claim |

Any later proposal to import a FAL-001 module changes the frozen input and requires human review.

## 9. Hard-limit budget

LOC estimates are conservative maximum allocations using specification §13 physical-line semantics.

| Object | Planned path/boundary | New/changed/reused | Estimated counted LOC | Normative classification | Evidence |
| --- | --- | --- | ---: | --- | --- |
| Package initializer | `forge/__init__.py` | reused unchanged | 2 | production module, `COUNT` | baseline file and inventory hash |
| Sequential core | `forge/fal002.py` | new | 220 | production module, `COUNT` | inventory per-file LOC |
| Canonical model/generator | `forge/fal002_model.py` | new | 250 | production module and generator, `COUNT` | inventory plus generated-schema equivalence tests |
| Inventory | `forge/fal002_inventory.py` | new | 300 | production module, `COUNT` | self-inventory output and paper fixtures |
| Persistence/collector/adapters | `forge/fal002_io.py` | new | 190 | production module; one executor and one reviewer adapter, `COUNT` | role classification and inventory output |
| Gate record | `fal002.gate-record.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Executor exchange | `fal002.executor-exchange.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Run record | `fal002.run-record.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Reviewer exchange | `fal002.reviewer-exchange.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Human decision | `fal002.human-decision.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |

| Budget | Planned | Hard limit | Remaining margin |
| --- | ---: | ---: | ---: |
| Production modules | 5 | 8 | 3 |
| Counted production LOC | 962 | 1,200 | 238 |
| Executor adapters | 1 | 1 | 0 |
| Reviewer adapters | 1 | 1 | 0 |
| Schema surfaces | 5 | 6 | 1 |
| New dependencies | 0 | 0 without human decision | 0 |

Adapters intentionally consume their allowed counts; this is not module/LOC exhaustion. Any module
or LOC estimate breach, sixth-plus module beyond the remaining three, sixth schema surface, second
adapter for either role or dependency change stops `AWAITING_HUMAN` before implementation continues.

## 10. Verification matrix

| Material requirement | Planned component | Verification method | Intended test/paper test | Expected result | Produced evidence | Stop condition |
| --- | --- | --- | --- | --- | --- | --- |
| Canonical boundary consistency | `fal002_model` | generate and compare all schemas | model/schema round trips and drift fixture | exact equality | schema hashes and test output | mismatch → `blocked` |
| Boundary rejection | `fal002_model` | receipt and pre-persist validation | unknown/type/enum/hash/identity cases | all rejected | structured failures | accepted malformed data → `blocked` |
| Frozen contract and series budget | core/model | reopen and identity fixtures | changed scope, new execution ID, reset attempt | all rejected; count retained | series records | reset/change → `blocked` |
| Deterministic inventory | inventory | two independent invocations | byte-identical frozen inputs | byte-identical sorted output | inventory hashes | difference → `awaiting_human` |
| Static/relative/package imports | inventory | AST fixtures | absolute, relative and `__init__` chains | all reachable files counted | edge list | unresolved edge → `awaiting_human` |
| Conditional references | inventory | paper and AST fixtures | platform/version/try/`TYPE_CHECKING` | statically resolvable targets counted | classified edges | implicit exclusion → `blocked` |
| Dynamic/subprocess references | inventory | literal/computed fixtures | importlib/runpy/exec/subprocess | literal counted; computed awaits human | edge reason/status | unresolved → `awaiting_human` |
| Tool exemptions | inventory | complete predicate truth table | true/false/unknown/not-evaluated combinations | unique specified disposition | predicate evidence | invalid combination → `awaiting_human` |
| Module and LOC count | inventory | self-inventory and synthetic files | blank/comment/docstring/generated cases | exact per-file and total count | inventory report | limit breach → `awaiting_human` |
| Adapter count | inventory/model | role fixtures | wrapper, dual-role and second adapter | exact role counts; second rejected | classifications | count >1 → `awaiting_human` |
| Schema-surface count | model/inventory | boundary-root fixtures | split/nested/multiple/synthetic wrapper | semantic surface count | stable IDs | count >6 → `awaiting_human` |
| Dependency assessment | inventory | baseline manifest/lock comparison | stdlib, existing, new direct/transitive | no new dependency | dependency section | new dependency → `awaiting_human` |
| Sequential execution | core | event-order fixture | executor/collector/reviewer/correction journey | one ordered path, no overlap | state series/timestamps | overlap/extra role → `blocked` |
| Collector authority | I/O/model | fake executor contradiction | executor prose differs from Git/test facts | collector facts retained | run record/raw hashes | missing fact → `blocked` |
| Authority map/conflicts | core/model | domain-pair conflict fixtures | human/collector, reviewer/model, cache/series, provenance/history | no cross-domain overwrite; decision card created | raw conflicting records | conflict → `blocked` or `awaiting_human` |
| Human decision cards | core/model | pending/default fixtures | unresolved question, missing choice, attempted default | progression and closure blocked | decision record/state event | pending/invalid → `awaiting_human` |
| Secret redaction | I/O/model | credential-shaped raw output | token/password/key values in command output | persisted value redacted before hashing/storage | redacted artifact and hash | unredacted secret → `blocked` |
| Allowed paths/commands | core/I/O | out-of-contract fixtures | changed path and command outside frozen policy | rejected before state effect | policy failure event | violation → `blocked` |
| Criterion evidence | model/I/O | pointer/hash/provenance fixtures | valid, missing, stale, wrong criterion | only exact binding resolves | reviewer exchange | incomplete binding → no PASS |
| Semantic rationale | reviewer exchange | result validation | absent/present rationale | absent rejected | reviewer result | absent rationale → no PASS |
| Blocking findings | model/core | false-PASS fixtures | CRITICAL/blocking/pending decision | PASS and eligibility rejected | state/review record | attempted PASS → `blocked` |
| No default PASS | core | all result enum cases | missing/unknown/inconclusive | never converted to PASS | transition record | conversion → `blocked` |
| Correction/no-progress | core | positive/negative series fixtures | 0–2 rounds, reset, repeated hashes/findings | ceiling and stops enforced | correction series | breach → `blocked` |
| Append-only recovery | I/O/model | interruption/fork/gap/cache fixtures | append/cache failure and replay | coherent recovery or fail closed | record hashes | invalid chain → `blocked` |
| Human-only closure | model/core/I/O | role/atomicity/repeat fixtures | executor/reviewer/generic close, pending finding | only accepted human record closes | closure record | any other close → `blocked` |
| Forbidden operations | core/I/O | adversarial command fixtures | push/tag/merge/release/etc. | all rejected before execution | policy event | attempt → `blocked` |
| Implementation review event | reviewer adapter | provenance inspection | fresh read-only Standard-Assurance review with adversarial instructions | exact truthful provenance and PASS required | sealed reviewer exchange | missing provenance → no eligibility |
| Hard-limit total | inventory | canonical self-inventory | planned implementation tree | ≤5 modules, ≤962 LOC, 1/1 adapters, 5 surfaces, 0 deps | final inventory output | any planned cap exceeded → `awaiting_human` |

Planned tests are not implementation authorization. Expected results must be independently literal;
tests must not derive every expectation from production constants.

## 11. Implementation sequence after separate authorization

1. Reconfirm frozen inputs and authorized baseline; stop on drift.
2. Add independent failing canonical-model and boundary tests.
3. Implement `fal002_model` and generate the five schemas.
4. Add inventory paper/fixture tests, then implement `fal002_inventory` exactly from specification
   §13 and run its self-inventory after each production change.
5. Add append/recovery and collector tests, then implement `fal002_io`.
6. Add sequential flow, correction, false-PASS and closure tests, then implement `fal002`.
7. Run all focused tests, full Forge tests, Ruff, diff check and Project Memory Health.
8. Run the canonical inventory twice from identical inputs and compare output bytes/hashes.
9. Verify changed paths, hard-limit margins, forbidden surfaces and no FAL-001 runtime import.
10. Update accurate implementation-pending-review state and prepare the separate implementation
    review packet.
11. Conduct a fresh read-only Standard-Assurance review with adversarial instructions whose review
    object is the implementation.
12. Stop for human closure authority; do not start the album capability.

## 12. Completion and authorization gates

This brief becomes review-ready only if its frozen inputs, budget and verification matrix remain
complete and no normative question is open. Current planning finds no open input or architecture
question.

The next permitted gate is human review of EB-006. Even a review PASS does not implement FAL-002.
Implementation requires a separate explicit human decision naming the accepted brief and baseline.
Implementation completion later requires separate implementation review and human-only closure.
Release and album work remain separate gates.

## 13. Risks and rollback

- LOC concentration: enforce per-module ceilings continuously; stop before 1,200 total.
- Schema compression: preserve five actual atomic boundary units; do not hide independent payloads.
- FAL-001 contamination: prohibit runtime import and inventory every reachable first-party module.
- False assurance: retain exact Standard-Assurance review name and provenance.
- Persistence interruption: append authoritative record first and recover derived state only.

Planning rollback is documentation-only: revert EB-006 and the associated approval/state references.
It must not alter FAL-001 history or claim that the accepted human decision never occurred.
