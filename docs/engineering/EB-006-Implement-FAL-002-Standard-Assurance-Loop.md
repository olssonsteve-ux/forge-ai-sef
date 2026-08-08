# EB-006 — Implement FAL-002 Standard Assurance Bounded Engineering Loop

Status: `AWAITING INDEPENDENT REVIEW`

Date: 2026-08-01

Owner: Chief Architect

Decision basis: `HD-FAL-006`

Correction authority: `HD-FAL-007`, `HD-FAL-008`, `HD-FAL-009`, `HD-FAL-010`, `HD-FAL-012`,
`HD-FAL-013`, `HD-FAL-014`, `HD-FAL-015`, `HD-FAL-016`, `HD-FAL-017`, `HD-FAL-018`

Specification: `docs/capabilities/FAL-002-Standard-Assurance-Bounded-Engineering-Loop.md`

Implementation authorization: `NOT AUTHORIZED`

Residual finding status:

| Finding | Status |
| --- | --- |
| `EB006-R1` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-R2` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-R3` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-FR-01` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-FR-02` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-FR-03` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-FR-04` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-FR-05` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-FR-06` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-FR-07` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR2-01` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR2-02` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR2-03` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR2-04` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR2-05` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR2-06` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR2-07` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-01` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-02` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-03` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-04` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-05` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-06` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-07` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR3-08` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR5-01` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR5-02` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR5-03` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR5-04` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `EB006-IR6-01` | `INDEPENDENTLY VERIFIED — NOT CLOSED` |
| `EB006-IR6-02` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |

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
| Runtime persisted root | `.forge/fal002/series/{series_id}/` |
| Runtime exchange root | In-memory canonical exchanges plus persisted series paths in section 14 |
| Runtime allowed read root | Verified repository root `.` plus resolved `git` and Python executables |
| Runtime allowed write root | `.forge/fal002/series/{series_id}/` only |
| Implementation allowed paths | `forge/fal002.py`, `forge/fal002_model.py`, `forge/fal002_inventory.py`, `forge/fal002_io.py`, the five exact schema paths in section 17, `tests/test_fal002_model.py`, `tests/test_fal002_inventory.py`, `tests/test_fal002_flow.py`, `tests/test_fal002_recovery.py`, `tests/fixtures/fal002/*.json`, `docs/engineering/FAL-002-implementation-review-handoff.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, `AI_HANDOFF.md`, `docs/README.md` |
| Manifest input path | `.forge/fal002/series/{series_id}/gate/00000000.json` |
| Command policy | Only command IDs and exact argv in section 15; shell execution forbidden |

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

LOC estimates are the bottom-up expected implementation using specification §13 physical-line
semantics. The 1,800-line ceiling is a maximum envelope, not a target.

| Object | Planned path/boundary | New/changed/reused | Estimated counted LOC | Normative classification | Evidence |
| --- | --- | --- | ---: | --- | --- |
| Package initializer | `forge/__init__.py` | reused unchanged | 2 | production module, `COUNT` | baseline file and inventory hash; first-party imports `NONE` |
| Sequential core | `forge/fal002.py` | new | 330 | production module, `COUNT` | inventory LOC; imports `fal002_model`, `fal002_inventory`, `fal002_io` |
| Canonical model/generator | `forge/fal002_model.py` | new | 420 | production module and generator, `COUNT` | schema-equivalence tests; first-party imports `NONE` |
| Inventory | `forge/fal002_inventory.py` | new | 360 | production module, `COUNT` | self-inventory; imports `fal002_model` |
| Persistence/collector/adapters | `forge/fal002_io.py` | new | 550 | production module; one executor and one reviewer adapter, `COUNT` | role inventory; imports `fal002_model` |
| Gate record | `fal002.gate-record.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Executor exchange | `fal002.executor-exchange.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Run record | `fal002.run-record.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Reviewer exchange | `fal002.reviewer-exchange.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |
| Human decision | `fal002.human-decision.v1` | new boundary | 0 | one schema surface | generated schema ID/hash |

| Budget | Planned | Hard limit | Remaining margin |
| --- | ---: | ---: | ---: |
| Production modules | 5 | 8 | 3 |
| New counted production LOC | 1,660 | 1,800 | 140 |
| Executor adapters | 1 | 1 | 0 |
| Reviewer adapters | 1 | 1 | 0 |
| Schema surfaces | 5 | 6 | 1 |
| New dependencies | 0 | 0 without human decision | 0 |

Adapters intentionally consume their allowed counts. The four new module estimates total 1,660 new
production LOC; the unchanged two-line package initializer is reported separately and is not reusable
implementation credit. Sections 14–20 are included in the bottom-up estimate. Any module or LOC
hard-limit breach, sixth-plus module beyond the remaining three,
sixth schema surface, second
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
| Authority map/conflicts | core/model | domain-pair conflict fixtures | human/collector, reviewer/model, cache/series, provenance/history | one decision card and final `awaiting_human` | raw sources plus `HumanDecisionRecord.payload.decision_card` | conflict → `awaiting_human` only |
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
| Hard-limit total | inventory | canonical self-inventory | planned implementation tree | ≤5 modules, expected ≤1,660 and maximum ≤1,800 new LOC, 1/1 adapters, 5 surfaces, 0 deps | final inventory output | any maximum exceeded → `awaiting_human` |

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
question. The corrected findings remain addressed but not closed pending independent review.

The next permitted gate is human review of EB-006. Even a review PASS does not implement FAL-002.
Implementation requires a separate explicit human decision naming the accepted brief and baseline.
Implementation completion later requires separate implementation review and human-only closure.
Release and album work remain separate gates.

## 13. Risks and rollback

- LOC concentration: enforce the bottom-up module estimates continuously; stop before 1,800 new
  production LOC and never treat unused margin as implementation scope.
- Schema compression: preserve five actual atomic boundary units; do not hide independent payloads.
- FAL-001 contamination: prohibit runtime import and inventory every reachable first-party module.
- False assurance: retain exact Standard-Assurance review name and provenance.
- Persistence interruption: append authoritative record first and recover derived state only.

Planning rollback is documentation-only: revert EB-006 and the associated approval/state references.
It must not alter FAL-001 history or claim that the accepted human decision never occurred.

## 14. Exact runtime storage and surface mapping

### 14.1 Canonical paths and segment derivation

The verified repository root is the single path returned by command `GIT-ROOT` in section 15 and
must equal the invocation working directory after `Path.resolve(strict=True)`. Runtime paths resolve
beneath that root; no home, temporary or user-specific default is permitted.

- `series_id`: lowercase canonical UUID supplied by the validated frozen manifest.
- `sequence`: zero-based gate sequence formatted as exactly eight decimal digits.
- `ordinal`: zero-based execution/review ordinal formatted as exactly four decimal digits.
- `run_id`: `run-{ordinal}-{sha256(series_id + ":" + ordinal + ":" + frozen_hash)[:12]}`.
- `execution_id`: `exec-{ordinal}-{sha256(run_id + ":executor")[:12]}`.
- `review_id`: `review-{ordinal}-{sha256(run_id + ":reviewer")[:12]}`.
- `decision_id`: an accepted external human-decision ID, or generated card
  `DC-{series_id_without_hyphens[:12]}-{sequence}`.

Every segment must match its grammar before path construction. The resolved target and every
existing parent are checked against the verified root with `Path.relative_to`; symlinks are resolved
and rejected when the final target leaves the allowed root. Missing, ambiguous, traversing or
escaping paths return `AWAITING_HUMAN`. No path comes from user or environment defaults.

### 14.2 Concrete tree and operations

```text
.forge/fal002/series/{series_id}/
├── gate/{sequence:08d}.json
├── executor/{execution_id}.json
├── runs/{run_id}.json
├── reviewer/{review_id}.json
├── decisions/{decision_id}.json
└── current.json
```

| Form/path | Writer → readers | Operation and durability | Recovery | Surface / placement |
| --- | --- | --- | --- | --- |
| `gate/{sequence}.json` | core/I/O → all | create-only; validate, write canonical UTF-8 with `x`, flush, `os.fsync`, close, reread/hash; never overwrite/delete | longest verified predecessor chain; partial tail → `AWAITING_HUMAN` | `GateRecord`; top-level record |
| `executor/{execution_id}.json` | executor adapter/I/O → collector/core | create-only after result validation and durability sequence | absent after executing checkpoint permits only decision-card-controlled retry; malformed/duplicate → `AWAITING_HUMAN` | `ExecutorExchange`; top-level exchange |
| `runs/{run_id}.json` | collector/I/O → reviewer/core | create-only after command facts are sealed | absence/invalid blocks review; duplicate path/hash conflict → `AWAITING_HUMAN` | `RunRecord`; top-level record |
| `reviewer/{review_id}.json` | reviewer adapter/I/O → core/human | create-only after result validation | absent result retries only by human decision; malformed/duplicate → `AWAITING_HUMAN` | `ReviewerExchange`; top-level exchange |
| `decisions/{decision_id}.json` | human boundary/core → core/human | create-only accepted record or generated pending card | same ID/hash idempotent; different hash → `AWAITING_HUMAN` | `HumanDecisionRecord`; top-level decision |
| `current.json` | I/O → readers | derived only; write `current.json.tmp`, flush/fsync/verify, atomic replace; never authority | rebuild from gate chain | `GateRecord`; exact latest verified record |

Directory creation is allowed only beneath the series root. Authoritative files are never updated,
appended in place, renamed over, deleted or truncated. “Append” means create the next sequence file
after its predecessor is durable. Durability is successful reread/hash verification after file
`fsync`; progression before it is forbidden. `current.json` is the sole replaceable path.

### 14.3 Embedded forms—no hidden surfaces

| Logical form | Owning surface and exact field | Writer → reader | Why not independent |
| --- | --- | --- | --- |
| Inventory output | `GateRecord.payload.inventory` in pre-execution gate record | inventory/core → core/reviewer | state effect and inventory are one gate transition; no separate file/exchange |
| Collector evidence/provenance | `RunRecord.commands[]` and `RunRecord.repository` | collector → reviewer/core | collected and consumed only as the run record |
| Criterion evidence/rationale | `ReviewerExchange.result.criterion_evidence[]` and `.semantic_rationale` | reviewer → core/human | part of the one reviewer response |
| Decision card | `HumanDecisionRecord.payload.decision_card` | core → human/core | decision is the persisted unit |
| Correction/no-progress | `GateRecord.payload.control` | core → core/reviewer | control belongs to the gate transition |
| Recovery/checkpoint/interruption | `GateRecord.payload.checkpoint` plus envelope hashes | I/O/core → recovery | authoritative checkpoint is the gate record; no sidecar |
| Derived state | `current.json`, exact `GateRecord` copy | I/O → readers | replaceable cache of an existing surface |
| Eligibility/final disposition | `GateRecord.payload.eligibility` and `.disposition` | core → human/core | transition payloads; human closure decision remains separate |

Allowed runtime reads are the verified repository root, `.git/`, frozen inputs, committed schemas and
current series tree. Allowed creates/replaces are only the paths above. External exchange occurs only
through section 16 typed calls and accepted human-decision input. Any other persisted/external form
is counted as an additional surface and returns `AWAITING_HUMAN` before use.

### 14.4 Deterministic authority conflict

Every conflict between authority domains uses exactly this mapping: stop the technical loop;
preserve both canonical source records and provenance in the next `GateRecord.payload.checkpoint`;
create exactly one deterministically identified `HumanDecisionRecord.payload.decision_card`; append
the gate transition only after the card is durable; and set final disposition `AWAITING_HUMAN`.
Executor/reviewer PASS, eligibility and closure are forbidden. `BLOCKED` may occur only as a
diagnostic reason inside the checkpoint, never as an alternative final disposition. Identical
canonical sources produce identical ordering, card ID, hash and disposition.

## 15. Exact collector commands and parsers

Commands use `shell=False`, verified repository root as `cwd`, closed stdin, forbidden network and
strict UTF-8 output. Allowed environment keys are `PATH`, `SYSTEMROOT`, `TEMP`, `TMP`, plus fixed
`PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`; proxy/credential variables are removed. `PYTHON` is
resolved `sys.executable` at exactly Python 3.14. Git timeout is 30 seconds, inventory/schema/status 120,
Ruff 300 and pytest 900. Missing executable, timeout, invalid UTF-8, unexpected exit, parser failure
or contradictory fact returns `BLOCKED`; inventory unresolved semantics retain `AWAITING_HUMAN`.

| ID | Exact executable and argv | Exit/parser/normalization | Evidence field |
| --- | --- | --- | --- |
| `GIT-ROOT` | `git`, `["git","rev-parse","--show-toplevel"]` | exit 0; exactly one absolute line; resolve and equal `cwd` | `RunRecord.repository.root` |
| `GIT-HEAD` | `git`, `["git","rev-parse","HEAD"]` | exit 0; one lowercase hex line length 40 or 64 | `.baseline_head`/`.final_head` |
| `GIT-BRANCH` | `git`, `["git","branch","--show-current"]` | exit 0; one non-empty trimmed line | `.branch` |
| `GIT-STATUS` | `git`, `["git","status","--porcelain=v1","-z","--untracked-files=all"]` | exit 0; NUL records, exact XY prefix; rename/copy consumes next path; `/` normalization and bytewise sort | `.status[]`, `.changed_paths[]` |
| `GIT-DIFF` | `git`, `["git","diff","--no-ext-diff","--binary","7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68","--"]` | exit 0; raw UTF-8 after redaction; no semantic parser | `.diff.text`, `.diff.sha256` |
| `GIT-NUMSTAT` | `git`, `["git","diff","--no-ext-diff","--numstat","-z","7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68","--"]` | exit 0; tab fields/NUL paths; decimal or `-`; canonical sort | `.diff.numstat[]` |
| `INVENTORY` | `PYTHON`, `[PYTHON,"-m","forge.fal002","inventory","--manifest",MANIFEST,"--output","-"]` | exit 0 or 3 (`AWAITING_HUMAN`); one canonical JSON object validated as inventory field; sorted compact keys | `GateRecord.payload.inventory` plus raw hash |
| `SCHEMA-CHECK` | `PYTHON`, `[PYTHON,"-m","forge.fal002","schemas","--output-root","schemas/fal002","--check"]` | exit 0 exact, 1 mismatch; sorted schema IDs/hashes only | `RunRecord.commands[SCHEMA-CHECK]` |
| `PYTEST` | `PYTHON`, `[PYTHON,"-m","pytest","-q"]` | exit 0 pass, 1 failure, 5 no tests; anchored final-summary parser | `RunRecord.commands[].derived.tests` |
| `RUFF-LINT` | `PYTHON`, `[PYTHON,"-m","ruff","check","."]` | exit 0 pass, 1 findings; exit/raw hash authoritative | `.derived.lint` |
| `RUFF-FORMAT` | `PYTHON`, `[PYTHON,"-m","ruff","format","--check","."]` | exit 0 pass, 1 mismatch; exit/raw hash authoritative | `.derived.format` |
| `FORGE-STATUS` | `PYTHON`, `[PYTHON,"-m","forge","status"]` | exit 0; exact unique headings for Project Memory Health and Version Consistency with enum plus indented evidence | `.derived.project_memory`, `.derived.version_consistency` |

The pytest grammar is the anchored final non-empty summary line containing comma-separated decimal
counts followed by exactly `passed`, `failed`, `skipped`, `xfailed`, `xpassed`, `error`/`errors` or
`warning`/`warnings` and optional duration. Absent categories are zero; unknown tokens fail parsing.
Every command persists argv, cwd, permitted environment-key names, UTC start/end, exit code,
stdout/stderr hashes, redaction count and parser version. Build is `not_available`: no accepted
non-packaging build exists and packaging is forbidden. Inventory supplies module/LOC, adapter,
schema and dependency facts from Python AST and `pyproject.toml`; no actor prose replaces facts.

## 16. Exact adapter interfaces

Both protocols live in `forge/fal002_io.py` but remain distinct roles:

```python
class FAL002ExecutorAdapter(Protocol):
    def execute(
        self, exchange: ExecutorExchange, *, timeout_seconds: float
    ) -> ExecutorExchange: ...

class FAL002ReviewerAdapter(Protocol):
    def review(
        self, exchange: ReviewerExchange, *, timeout_seconds: float
    ) -> ReviewerExchange: ...
```

Input validates before call; output validates immediately after return and before persistence. The
executor may change only `ExecutorExchange.result` and write only exchange-frozen paths. It cannot
state PASS, create collector/reviewer facts, history or decisions. The read-only reviewer may change
only `ReviewerExchange.result` with allowed result, findings, criterion references, semantic
rationale and execution provenance. It cannot correct, mutate facts/history, close or write outside
the returned exchange.

Wrong type, changed input fields, missing output, executor disposition, invalid reviewer result,
missing evidence/rationale for PASS or invalid provenance maps to `BLOCKED` with no eligibility.
`TimeoutError` maps to `BLOCKED`; `KeyboardInterrupt`/process interruption safely appends a checkpoint
then returns `AWAITING_HUMAN`. Other exceptions are redacted, hashed, checkpointed and `BLOCKED`.

## 17. Schema generation contracts

Generator signature is
`generate_schemas(output_root: Path, *, check: bool = False) -> tuple[GeneratedSchema, ...]` in
`forge/fal002_model.py`. Generation argv is
`[PYTHON,"-m","forge.fal002","schemas","--output-root","schemas/fal002"]`; check adds `"--check"`.
Output is UTF-8 JSON, sorted keys, two-space indentation and one terminal newline. Check generates
bytes in memory and returns nonzero on committed-byte mismatch without writing.

| Schema path | Canonical ID | Owning model/surface | Planned fixtures |
| --- | --- | --- | --- |
| `schemas/fal002/gate-record-v1.schema.json` | `fal002.gate-record.v1` | `GateRecord` | `FX-GATE-VALID`, `FX-GATE-INVALID` |
| `schemas/fal002/executor-exchange-v1.schema.json` | `fal002.executor-exchange.v1` | `ExecutorExchange` | `FX-EXEC-VALID`, `FX-EXEC-INVALID` |
| `schemas/fal002/run-record-v1.schema.json` | `fal002.run-record.v1` | `RunRecord` | `FX-RUN-VALID`, `FX-RUN-INVALID` |
| `schemas/fal002/reviewer-exchange-v1.schema.json` | `fal002.reviewer-exchange.v1` | `ReviewerExchange` | `FX-REVIEW-VALID`, `FX-REVIEW-INVALID` |
| `schemas/fal002/human-decision-v1.schema.json` | `fal002.human-decision.v1` | `HumanDecisionRecord` | `FX-DECISION-VALID`, `FX-DECISION-INVALID` |

Templates remain `NONE`. Canonical field metadata is the sole schema source; each artifact binds its
ID and generator/model hash. Hand-maintained schema rules are forbidden.

## 18. Planned schema and scenario fixtures

No fixture is created by this brief. Every future path is under `tests/fixtures/fal002/` and contains
the named model's minimum fields unless its scenario names the mutation.

| Fixture ID / planned path | Schema/scenario | Expected disposition and evidence |
| --- | --- | --- |
| `FX-GATE-VALID` / `gate-valid.json` | minimal valid `GateRecord` | valid; canonical hash |
| `FX-GATE-INVALID` / `gate-invalid.json` | missing predecessor | `BLOCKED`; field error |
| `FX-EXEC-VALID` / `executor-valid.json` | valid exchange | valid; exchange hash |
| `FX-EXEC-INVALID` / `executor-invalid.json` | executor attempts PASS | `BLOCKED`; authority error |
| `FX-RUN-VALID` / `run-valid.json` | valid repository/commands | valid; evidence hashes |
| `FX-RUN-INVALID` / `run-invalid.json` | unknown field/bad hash | `BLOCKED`; exact errors |
| `FX-REVIEW-VALID` / `reviewer-valid.json` | PASS with complete bindings/rationale | valid; coverage map |
| `FX-REVIEW-INVALID` / `reviewer-invalid.json` | missing criterion evidence | no PASS; `BLOCKED` |
| `FX-DECISION-VALID` / `decision-valid.json` | accepted human decision | valid; provenance hash |
| `FX-DECISION-INVALID` / `decision-invalid.json` | missing owner/unknown field | `BLOCKED` |
| `FX-HASH-ORDER` / `hash-order.json` | wrong sequence/hash/order | `BLOCKED`; chain error |
| `FX-DUPLICATE` / `duplicate-record.json` | duplicate path/different hash | `AWAITING_HUMAN`; both hashes |
| `FX-PARTIAL` / `partial-record.json` | truncated trailing JSON | `AWAITING_HUMAN`; raw hash |
| `FX-AUTH-CONFLICT` / `authority-conflict.json` | human contradicts collector | one card; `AWAITING_HUMAN` |
| `FX-REDACTED-RELEVANT` / `redacted-relevant.json` | redaction removes criterion locator | no PASS; `BLOCKED` |
| `FX-CONDITIONAL` / `conditional-import.json` | platform/TYPE_CHECKING import | target `COUNT` |
| `FX-DYNAMIC-LITERAL` / `dynamic-literal.json` | literal import/subprocess | target `COUNT` |
| `FX-DYNAMIC-COMPUTED` / `dynamic-computed.json` | computed target | `AWAITING_HUMAN` |
| `FX-HIDDEN-SURFACE` / `hidden-recovery-surface.json` | separate recovery payload proposed | sixth surface; `AWAITING_HUMAN` |

Each invalid fixture has an independently authored literal expected record/error; expected status
must not be computed from production tables.

## 19. Interruption and recovery matrix

The write algorithm is `validate → create → write → flush/fsync → close → reread/hash → next append`.
Only derived `current.json` adds `tmp → atomic replace` after authoritative durability.

`IP-01` through `IP-05` are parameterized over exactly the five authoritative path templates in
section 14.2; fixture field `record_kind` selects one and no other path is allowed. Their planned
paths are `tests/fixtures/fal002/ip-01.json` through `ip-05.json`. `IP-06` through `IP-09` use
respectively `ip-06.json` through `ip-09.json` in the same directory.

Each `FX-IPnn` file validates as a minimal `GateRecord` containing `series_id`, `sequence`,
`predecessor`, envelope/payload hashes and `payload.checkpoint` fields `interruption_id`,
`record_kind`, canonical `target_path`, `phase`, `last_durable_sequence` and `observed_hash`. The
scenario mutates only the phase-specific file-state description; expected disposition and evidence
are the corresponding row below.

| ID | Point/path | Last durable prefix and crash state | Required recovery / fixture-test |
| --- | --- | --- | --- |
| `IP-01` | before validation; any record | prior verified gate sequence | no file; resume after revalidation / `FX-IP01`, `test_recovery_ip01` |
| `IP-02` | after validation, before create | prior prefix | no file; resume same append / `FX-IP02`, `test_recovery_ip02` |
| `IP-03` | after write, before flush | prior prefix; possible partial tail | preserve bytes, never overwrite; `AWAITING_HUMAN` / `FX-PARTIAL`, `test_recovery_ip03` |
| `IP-04` | after fsync, before reread | file possibly durable/unconfirmed | reread; exact valid hash adopts once, else await human / `FX-IP04`, `test_recovery_ip04` |
| `IP-05` | after confirmation, before next record | new durable prefix | continue with next record; duplicate same hash idempotent / `FX-IP05`, `test_recovery_ip05` |
| `IP-06` | between two required record types | earlier durable, later absent | decision-card-controlled retry or await human; never fabricate / `FX-IP06`, `test_recovery_ip06` |
| `IP-07` | duplicate append after restart | target exists | same hash idempotent; different hash awaits human / `FX-DUPLICATE`, `test_recovery_ip07` |
| `IP-08` | missing/mismatched predecessor | chain before gap | no progression; `AWAITING_HUMAN` / `FX-HASH-ORDER`, `test_recovery_ip08` |
| `IP-09` | derived temp before replace | authority unaffected | discard/rebuild temp, atomic replace / `FX-IP09`, `test_recovery_ip09` |

Authoritative files are never overwritten/deleted. Contradiction, unverifiable recovery or missing
evidence awaits human; recovery cannot synthesize evidence or reset series/correction identity.

## 20. Exhaustive closure-criterion coverage

Test IDs are future planned tests; fixture IDs resolve to sections 18–19. Evidence fields are exact
locations in the five declared surfaces.

| ID / source | Component/contract | Test / fixture | Expected evidence field | Missing-evidence disposition |
| --- | --- | --- | --- | --- |
| `FAL2-CC-01` / spec §15.1 | model, schema check §17 | `test_schema_generation_exact` / valid schemas | `RunRecord.commands[SCHEMA-CHECK]` | `BLOCKED` |
| `FAL2-CC-02` / §15.2 | boundary validation | `test_boundary_rejection` / invalid fixtures | `GateRecord.payload.checkpoint.validation` | `BLOCKED` |
| `FAL2-CC-03` / §15.3 | frozen series | `test_frozen_reopen_identity` / `FX-HASH-ORDER` | `GateRecord.payload.control` | `BLOCKED` |
| `FAL2-CC-04` / §15.4 | collector §15 | `test_collector_owns_facts` / `FX-RUN-VALID` | `RunRecord.repository`, `.commands[]`, `.diff` | `BLOCKED` |
| `FAL2-CC-05` / §15.5 | correction/no-progress | `test_correction_ceiling_and_progress` / gate pair | `GateRecord.payload.control.corrections` | `BLOCKED` |
| `FAL2-CC-06` / §15.6 | PASS invariant | `test_blocking_finding_rejects_pass` / `FX-REVIEW-INVALID` | `ReviewerExchange.result.findings[]` | no PASS; `BLOCKED` |
| `FAL2-CC-07` / §15.7 | binding resolver | `test_criterion_binding_and_rationale` / reviewer pair | `.criterion_evidence[]`, `.semantic_rationale` | no PASS; `BLOCKED` |
| `FAL2-CC-08` / §15.8 | reviewer provenance | `test_standard_assurance_provenance` / `FX-REVIEW-VALID` | `.reviewer_execution` | no eligibility |
| `FAL2-CC-09` / §15.9 | append-only chain | `test_adverse_history_retained` / `FX-HASH-ORDER` | `GateRecord.predecessor`, `.payload.history` | `AWAITING_HUMAN` |
| `FAL2-CC-10` / §15.10 | human cards | `test_pending_card_blocks` / `FX-AUTH-CONFLICT` | `HumanDecisionRecord.payload.decision_card` | `AWAITING_HUMAN` |
| `FAL2-CC-11` / §15.11 | human close/recovery | `test_human_only_atomic_close` / decision + IP fixtures | `HumanDecisionRecord`, `GateRecord.payload.eligibility` | no closure; `BLOCKED` |
| `FAL2-CC-12` / §15.12 | command/path policy | `test_forbidden_operations_paths` / policy literals | `GateRecord.payload.checkpoint.policy` | `BLOCKED` |
| `FAL2-CC-13` / §15.13 | inventory §13 | `test_hard_limits` / `FX-HIDDEN-SURFACE` | `GateRecord.payload.inventory.limits` | `AWAITING_HUMAN` |
| `FAL2-CC-14` / §15.14 | pytest/Ruff/status/diff commands | `test_required_command_evidence` / `FX-RUN-VALID` | `RunRecord.commands[]` | no PASS; `BLOCKED` |
| `FAL2-CC-15` / §15.15 | reviewer exchange | `test_separate_implementation_review` / `FX-REVIEW-VALID` | `ReviewerExchange.result`, `.reviewer_execution` | no eligibility |
| `FAL2-CC-16` / §15.16 | human authority | `test_human_closure_decision_required` / decision pair | `HumanDecisionRecord.decision_kind=closure` | no closure |

Material inventory tests are `test_inventory_static_relative_init`,
`test_inventory_conditional_dynamic`, `test_exemption_truth_table`,
`test_loc_module_adapter_surfaces` and `test_dependency_diff`; they produce
`GateRecord.payload.inventory.{files,edges,exemptions,counts,dependencies,disposition}`. Authority
conflict test `test_authority_conflict_awaits_human` produces both raw sources and exactly one card.
Redaction test `test_redaction_blocks_missing_locator` uses `FX-REDACTED-RELEVANT`. Every requirement
fails closed when its named evidence is missing; no integration-test wildcard supplies coverage.

## 21. Historical canonical conventions (non-normative; superseded by sections 44–49)

Sections 21–27 record the pre-CORR-011 canonical design. They have no normative force after
CORR-012. In particular, the terminal-LF/hash language formerly in this section is withdrawn rather
than subject to a “later section wins” choice. Sections 44–49 are the sole final authority for
canonical bytes, hashing, boundary refinements, recovery, decisions, findings and fixtures.
`Json` means null, boolean, signed base-10 integer, UTF-8 string, ordered array, or object with string
keys. Floats, duplicate keys, NaN, infinity and lone surrogates are invalid. `Timestamp` is UTC
`YYYY-MM-DDTHH:MM:SS.ffffffZ`; `Sha256` is 64 lowercase hex characters; `PathRel` is a normalized
`/`-separated repository-relative path without empty, `.`, `..`, drive or NUL segments. Set-valued
arrays sort by UTF-8 bytes and reject duplicates. Every unqualified string field below is one required
`NonEmpty` trimmed string. Every unqualified array is required with cardinality 1..65535; only
`changed_paths`, `status`, `findings`, `finding_ids` and `source_record_ids/source_hashes` may be empty.
An explicitly optional/absent field has cardinality 0..1. Every object is required exactly once.

Historical only: canonical serialization was described as RFC-8259 JSON with one terminal LF and
`H(x)` over unspecified “canonical bytes”. That definition is **withdrawn**. It must not be
implemented or used by fixtures. The only final byte and hash definitions are §44.
Hash preimages omit only the field holding that hash. Runtime object → canonical model → schema
validation → canonical bytes → deterministic ID/hash must round-trip byte-identically before state
effect. There are no implicit defaults, nullable fields or extension containers. Optional means
absent; present null is invalid unless explicitly allowed below.

All surfaces require `schema_id`, `schema_version=1`, `record_id`, `series_id`, `created_at`,
`payload_hash` and `record_hash`. Unknown fields/enums/schema IDs/versions are `BLOCKED`. Version 1
accepts only version 1: no forward compatibility, backward conversion or extension field. A future
version requires Human Decision and a new schema ID. `payload_hash=H(payload)` and
`record_hash=H(record without record_hash)`. Validation order is JSON grammar → exact keys → schema/
version → primitive types/normalization → IDs/paths → enums/cardinality → hashes → cross-field
invariants → predecessor/series chain → authority invariants. The payload hash input is GateRecord
`payload`; ExecutorExchange `{request,result,invocation}`; RunRecord `{repository,commands,diff,build}`;
ReviewerExchange `{packet,result,reviewer_execution}`; and HumanDecisionRecord
`{decision_kind,status,owner,provenance,payload}`.

For collector observations `created_at` is the recorded UTC observation time. For deterministic
cards it is the lexicographically greatest source-record timestamp; the following gate uses that card
timestamp. Consequently identical canonical conflict inputs produce identical card and gate bytes.

Generated schemas use JSON Schema draft 2020-12, root `$id` equal to the canonical surface ID,
`type:object`, exact `required`, `additionalProperties:false`, explicit integer/string/array bounds and
`oneOf` only for the stated variants. Schema output and check behavior remain §17. Model→bytes→schema
validate→model→bytes equality is required for every valid fixture; every invalid fixture must fail
both model and schema at the same validation category.

### 21.1 `GateRecord` — `fal002.gate-record.v1`

| Field | Type / cardinality / requirement | Meaning and invariant |
| --- | --- | --- |
| `schema_id` | literal, one, required | `fal002.gate-record.v1` |
| `schema_version` | integer, one, required | exactly 1 |
| `record_id` | string, one, required | `gate-{sequence:08d}` |
| `series_id` | canonical UUID, one, required | frozen manifest identity |
| `sequence` | integer 0..99999999, one, required | zero initially; otherwise predecessor + 1 |
| `predecessor` | `Sha256` or null, one, required | null iff sequence zero; otherwise prior gate hash |
| `state` | enum, one, required | `draft|ready|executing|evidence_ready|reviewing|correction_required|blocked|awaiting_human|accepted|closed` |
| `actor` | enum, one, required | `human|core|collector|executor|reviewer|recovery` |
| `event` | §22 event enum, one, required | must permit predecessor state → state |
| `created_at` | `Timestamp`, one, required | evidence; included in hashes, never IDs |
| `payload` | exact object variant, one, required | below |
| `payload_hash`, `record_hash` | `Sha256`, each one, required | common hash rules |

`payload` contains exactly `frozen_hash:Sha256`, `correction_count:int 0..2` and one object variant:
`manifest|inventory|execution|evidence|review|control|checkpoint|eligibility|closure`. `manifest` has
`scope_hash`, `criteria_hash`, `allowed_paths:PathRel[]`, `command_policy_hash`; `control` has
`ordinal:int 0..9999`, `diff_hash`, `evidence_hash`, `finding_ids:string[]`; `checkpoint` has
`reason_code`, `source_record_ids:string[]`, `source_hashes:Sha256[]`, and optional
`interruption_id`, `decision_id`, `resume_state`; `eligibility` has `review_id`, `review_hash`,
`criterion_ids`, `finding_ids`, `eligible:boolean`; `closure` has `decision_id`, `decision_hash`.
`execution` contains `{execution_id,run_id,ordinal,request,request_hash}` and is the persisted request
before executor invocation. `review` contains `{review_id,run_id,ordinal,packet,packet_hash}` and is
the persisted request before reviewer invocation. Other variants contain exactly the referenced
top-level record ID and hash. Gate zero is
`draft/INITIALIZE`, actor human, manifest variant, count zero. `accepted` requires eligible true;
`closed` requires prior accepted gate and matching accepted closure decision.

### 21.2 `ExecutorExchange` — `fal002.executor-exchange.v1`

Besides the common envelope, exact fields are `record_id=execution_id`, `run_id`, `ordinal:int 0..9999`,
`request`, `result`, `invocation`. `request` has exactly `frozen_hash`, `scope:PathRel[]`,
`criteria:string[]`, `allowed_paths:PathRel[]`, `command_ids:string[]`, `correction_count:int 0..2`,
`work_packet_hash`. `result` is required null before invocation or exactly `{status:
COMPLETED|FAILED,changed_paths:PathRel[],summary:string,error_code:string|absent}` after return.
`invocation` has `invocation_id=execution_id`, `role=executor`, `adapter_id`, `principal_id`,
`context_id`, `process_id:int`, `started_at`, optional `ended_at`, `timeout_seconds:int>0`, `input_hash`.
Result may change only null→object; all request bytes remain identical. PASS, review, evidence,
decision and closure fields are forbidden.

### 21.3 `RunRecord` — `fal002.run-record.v1`

This pre-CORR-011 shape is historical; final RunRecord is exclusively §35.4. Historically, fields
were `record_id=run_id`, `execution_id`, `ordinal:int 0..9999`, `repository`, `commands`, `diff`,
`build`, and `repository` was `{root:".",branch,
baseline_head:hex40|hex64,final_head:hex40|hex64,status:string[],changed_paths:PathRel[]}`. `commands`
contained 13 entries in §24 order; final count is 17. Each historical entry was `{command_id,phase,argv:string[],cwd:PathRel,
environment_keys:string[],started_at,ended_at,exit_code:int|null,termination:
EXITED|TIMEOUT|INTERRUPTED|SPAWN_ERROR,stdout_sha256,stderr_sha256,stdout_text,stderr_text,
redaction_count:int>=0,parser_version:1,parsed:CommandParsed,classification:
PASS|FAIL|NOT_AVAILABLE|BLOCKED|AWAITING_HUMAN}`; null exit code is valid only when not EXITED.
`diff` is `{redacted_text,sha256,numstat:[{path,added:int|null,deleted:int|null}]}`; null counts are
valid only for binary files. `build` is exactly `{status:"not_available",reason:
"packaging_forbidden"}`. Repository/command/diff facts have collector authority.

### 21.4 `ReviewerExchange` — `fal002.reviewer-exchange.v1`

Besides the common envelope, exact fields are `record_id=review_id`, `run_id`, `ordinal:int 0..9999`,
`packet`, `result`, `reviewer_execution`. `packet` is exactly `{frozen_hash,run_record_id,
run_record_hash,criterion_ids:string[],evidence_index:[{criterion_id,source_record_id,locator,
content_hash,provenance}],instructions_hash}`. It contains no executor prompt, transcript, private
reasoning or mutable handle. `result` is null before invocation or exactly `{outcome:
PASS|CORRECTION_REQUIRED|BLOCKED|INCONCLUSIVE,findings:[{finding_id,severity:
CRITICAL|HIGH|MEDIUM|LOW,blocking:boolean,status:OPEN|ADDRESSED,criterion_ids,statement}],
criterion_evidence:[{criterion_id,source_record_id,locator,content_hash,provenance}],
semantic_rationale:[{criterion_id,rationale}]}`. PASS requires every criterion exactly once, no open
CRITICAL/blocking finding and no pending decision. Reviewer execution is defined in §23.

### 21.5 `HumanDecisionRecord` — `fal002.human-decision.v1`

Besides the common envelope, exact fields are `record_id=decision_id`, `decision_kind:
PENDING_CARD|RESOLUTION|CLOSURE`, `status:PENDING|ACCEPTED|DECLINED`, `owner`, `provenance:
{source,locator,content_hash}`, `payload`. PENDING_CARD requires PENDING and payload
`{decision_card:{question,domain,source_record_ids,source_hashes,allowed_choices}}`. The historical
RESOLUTION `chosen_value` shape is withdrawn; final RESOLUTION and CLOSURE are exclusively §35.5.
Historically, CLOSURE required ACCEPTED and payload
`{eligible_gate_id,eligible_gate_hash,review_id,review_hash}`. Decisions cannot rewrite facts/history.
Same ID/hash is idempotent; same ID/different hash is authority conflict. IDs derive exactly by §14.1;
card conflict suffix is refined in §25.

## 22. Exhaustive state-transition contract

Every event not listed for the current state is `FORBIDDEN TRANSITION`: append a `blocked` gate when
the next path is writable, otherwise return a `BLOCKED` diagnostic; retry requires accepted human
resolution. Required evidence always means a schema-valid, hash-valid, authoritative record.

| Current | Event | Preconditions; actor/authority; evidence | Records created in order | Next | Failure; retry/resume |
| --- | --- | --- | --- | --- | --- |
| none | `INITIALIZE` | human; valid frozen manifest | gate 0 | draft | invalid → BLOCKED diagnostic; same-hash replay adopts |
| draft | `MARK_READY` | core; inventory PASS, no pending card | gate | ready | unresolved/limit → awaiting_human gate |
| draft | `ESCALATE` | core; unresolved input | card, gate | awaiting_human | accepted resolution only |
| ready | `START_EXECUTION` | core; ordinal=max prior ordinal+1, or 0 if none; request valid | gate with execution request | executing | persistence → §25; invoke only after gate durability |
| executing | `EXECUTOR_COMPLETED` | executor; matching result | executor result | executing | same hash idempotent; conflict → conflict event |
| executing | `EXECUTOR_FAILED` | core; failed/timeout/error result | gate | blocked | human resolution only |
| executing | `EXECUTOR_INTERRUPTED` | recovery; interruption checkpoint | gate | awaiting_human | accepted retry uses next ordinal, count unchanged |
| executing | `COLLECT_COMPLETE` | collector; all final §35.1 command entries | run, gate | evidence_ready | missing/malformed → blocked gate |
| evidence_ready | `START_REVIEW` | core; packet and independence precheck | gate with review packet | reviewing | failed separation → card, awaiting_human gate; invoke only after durability |
| reviewing | `REVIEW_PASS` | reviewer; complete valid PASS | reviewer result, eligibility gate | accepted | blocking/missing → blocked gate |
| reviewing | `REVIEW_CORRECTION` | reviewer; CORRECTION_REQUIRED | reviewer result, gate | correction_required | count=2 → ceiling event |
| reviewing | `REVIEW_BLOCKED` | reviewer; BLOCKED/INCONCLUSIVE | reviewer result, gate | blocked | no automatic retry |
| reviewing | `REVIEW_INTERRUPTED` | recovery; no durable result | gate | awaiting_human | accepted retry uses next ordinal, count unchanged |
| correction_required | `START_CORRECTION` | core; count<2, allowed paths; request valid | executing gate with embedded request | executing | persist gate, then invoke; ordinal/count increment once; complete exchange only after result |
| correction_required | `NO_PROGRESS` | core; repeated diff/evidence or findings | gate | blocked | human resolution only |
| correction_required | `CEILING_REACHED` | core; count=2 | card, gate | awaiting_human | no automatic correction |
| any non-closed | `AUTHORITY_CONFLICT` | core; two valid domain sources | card, gate | awaiting_human | exactly-once replay §25 |
| any non-closed | `INVALID_EVIDENCE` | model/core; malformed/missing/stale/gap | gate if writable | blocked | facts unchanged; human resolution only |
| any non-closed | `PENDING_DECISION` | core; unresolved human question | card, gate | awaiting_human | no default |
| awaiting_human | `DECISION_ACCEPTED` | human; matching accepted resolution | decision, gate | stored `resume_state` | target only ready/evidence_ready/correction_required; interrupted executor→ready, reviewer→evidence_ready |
| awaiting_human | `DECISION_DECLINED` | human; matching declined resolution | decision, gate | blocked | no resume |
| blocked | `HUMAN_REOPEN` | human; accepted decision names evidence/target | decision, gate | ready or awaiting_human | count/ordinal/history retained |
| accepted | `HUMAN_CLOSE` | human; accepted closure, exact eligibility, no open/pending | decision, gate | closed | pair recovery §25 |
| closed | `HUMAN_CLOSE` | same closure ID/hash | none | closed | idempotent success |
| closed | any other | none | none | closed | FORBIDDEN/BLOCKED diagnostic |

Same-hash replay creates nothing. Different-hash duplicate uses AUTHORITY_CONFLICT when both claims
are valid authorities, otherwise INVALID_EVIDENCE. Correction rounds increment correction count;
every retry or correction uses max prior ordinal + 1, so retries never consume or reset corrections.
`accepted` means sealed technical eligibility only, not
risk acceptance, capability closure or release.

## 23. Adapter lifecycle and Standard-Assurance separation (provenance superseded by §29)

Core creates requests; I/O persists executor request in the executing gate and reviewer packet in the
reviewing gate; core invokes only after that gate is durable. Adapters create no ID, record or
transition and only return a value. Model validates, I/O create-persists the complete exchange once
after return, and core transitions. The request copied into the exchange must be byte-identical to
the gate-embedded request; no null-result exchange file is ever persisted.
Both roles are externally non-idempotent and called at most once per invocation ID. Same-ID replay
reads a durable result without adapter call. Missing result after interruption requires human retry
and a new ordinal/ID. Changed/stale input, different duplicate result, timeout or exception follows
§22 and §30. Executor mutates only executor result; reviewer mutates only review result. Cancellation
or interruption produces no result and uses the retry rule above. All identity, audit evidence, fresh-
context and separation rules are exclusively §29; the earlier self-reported provenance design is
withdrawn and must not be implemented.

## 24. Exact collector execution contract

Common contract: resolve `git` from PATH and Python as exact `sys.executable` 3.14; verified root cwd;
closed stdin; exact environment keys from §15 with all other inheritance removed. On timeout terminate
the process group, wait five seconds, then kill. Network precondition authority/evidence and the exact
redaction byte machine are exclusively §32; the prior generic regex description is withdrawn.
Strict UTF-8 decode; invalid bytes BLOCKED. Store CRLF/CR normalized to LF, but hash
`H({command_id,stream,redacted_bytes_hex})` before line normalization. Stderr never proves success.
Spawn/permission error, timeout, interruption, unexpected exit, missing/multiple/contradictory parse
candidate or forbidden trailing noise is BLOCKED. Every entry maps to `RunRecord.commands[]`; only
named parsed facts have collector authority.

| Collector / phase | Exact argv; input; timeout | Exit/parser; mapping |
| --- | --- | --- |
| `GIT-ROOT` / preflight | `git rev-parse --show-toplevel`; none; 30s | 0; exactly one absolute line/no noise, resolve=cwd → root |
| `GIT-HEAD-BASELINE` / pre-execution | `git rev-parse HEAD`; none; 30s | 0; exactly one lowercase hex40/64 matching frozen baseline → baseline_head |
| `GIT-BRANCH` / pre-execution | `git branch --show-current`; none; 30s | 0; exactly one non-empty line → branch |
| `INVENTORY` / pre-execution | Python inventory argv §15; manifest path; 120s | manifest procedure below; exit 0 PASS or 3 AWAITING_HUMAN; one JSON object/no noise → gate inventory |
| `GIT-HEAD-FINAL` / post-executor | `git rev-parse HEAD`; none; 30s | same grammar, separate invocation → final_head |
| `GIT-STATUS` / post-executor | exact argv §15; none; 30s | 0; exact NUL grammar; trailing fragment invalid → status/paths |
| `GIT-DIFF` / post-executor | exact baseline argv §15; 30s | 0; entire normalized redacted stdout → diff text/hash |
| `GIT-NUMSTAT` / post-executor | exact baseline argv §15; 30s | 0; every NUL record exact tab grammar, sorted path → numstat |
| `SCHEMA-CHECK` / verification | Python schema argv §17 `--check`; 120s | 0 and one JSON array of five sorted `{schema_id,sha256}`; exit 1/other BLOCKED |
| `PYTEST` / verification | `PYTHON -m pytest -q`; 900s | exit 0/1/5 recognized; only 0 PASS. Final non-empty line is sole anchored summary candidate; earlier candidate, contradiction, missing/malformed summary or interruption BLOCKED. Warning count is a summary category |
| `RUFF-LINT` / verification | `PYTHON -m ruff check .`; 300s | 0 PASS, 1 FAIL, other BLOCKED; text cannot override exit |
| `RUFF-FORMAT` / verification | `PYTHON -m ruff format --check .`; 300s | 0 PASS, 1 FAIL, other BLOCKED |
| `FORGE-STATUS` / verification | `PYTHON -m forge status`; 120s | 0 and exactly one required heading/status each; duplicate/missing/unknown BLOCKED |

The historical order was sequential and replaced ambiguous `GIT-HEAD`; final order and 17-entry
RunRecord are exclusively §35.1/§35.4. The manifest is exactly gate 0 bytes at §3 path: read, §21.1 validate,
require manifest variant, canonical-reserialize byte-identically, verify hash, then pass that literal
path in argv. No actor summary substitutes for collector evidence.

## 25. Historical create-only recovery analysis (superseded by §30)

The direct-final-write design previously recorded here is withdrawn because it could leave a partial
canonical path without authoritative disposition. It must not be implemented. Section 30 is the sole
normative recovery, publication, conflict-card and closure durability contract.

## 26. Scenario-fixture case inventory (oracle superseded by §31)

Constants: `series_id=00000000-0000-4000-8000-000000000002`, `frozen_hash=H("F")`, baseline
`7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68`, branch `main`, time
`2026-08-01T00:00:00.000000Z`. “Base” is literal valid gate 0 draft plus gate 1 ready, count/ordinal 0,
clean repository. IDs/hashes use §§14/21 expressions. Each file is exactly
`{fixture_id,cases:[{arrange,act,assert}]}` and expected values are literal, not imported constants.

| Fixture / cases | Arrange; act | Assert: records in order; final; forbidden |
| --- | --- | --- |
| `FX-GATE-VALID` | gate 0; validate/MARK_READY | gate 1; ready; no exchange/run/review/decision |
| `FX-GATE-INVALID` | missing predecessor and unknown-field cases; validate | none; BLOCKED diagnostic; unchanged filesystem |
| `FX-EXEC-VALID` | Base; START_EXECUTION then completed return | executing gate with request, complete executor exchange; executing; no run/review |
| `FX-EXEC-INVALID` | Base plus executor PASS field; validate | no result/gate; BLOCKED authority error |
| `FX-RUN-VALID` | completed executor; collect 13 commands | run, evidence_ready gate; exact derived IDs/hashes; no review |
| `FX-RUN-INVALID` | bad hash, unknown field, missing executable, timeout, invalid UTF-8, malformed output and ambiguous pytest cases; collect | no run/evidence gate; blocked gate if writable; §24 code |
| `FX-REVIEW-VALID` | valid run; fresh PASS review | reviewing gate with packet, complete reviewer exchange, accepted eligibility gate; no closure |
| `FX-REVIEW-INVALID` | missing criterion, reused executor principal, inherited context cases; precheck/validate | evidence error→blocked gate; independence error→card, awaiting_human gate; no PASS |
| `FX-DECISION-VALID` | awaiting_human/matching card; accepted resolution | resolution, resume gate; stored target; no rewrite |
| `FX-DECISION-INVALID` | missing owner, unknown field, stale and declined cases; apply | malformed/stale→blocked; declined→decision, blocked gate; no resume |
| `FX-HASH-ORDER` | predecessor mismatch, gap, stale sequence cases; load | none; terminal AWAITING_HUMAN diagnostic; no later gate |
| `FX-DUPLICATE` | same-hash and different-hash cases; replay append | same→none/idempotent; different→card, awaiting_human gate if free else terminal |
| `FX-PARTIAL` | IP-03 for gate/executor/run/reviewer/decision; recover | exact prefix preserved; terminal AWAITING_HUMAN; no reuse/delete/next record |
| `FX-AUTH-CONFLICT` | human/collector disagreement plus crash-before/after-card cases; conflict | one deterministic card, gate; awaiting_human; replay no semantic duplicate |
| `FX-REDACTED-RELEVANT` | secret removes locator; collect/review | redacted text/hash; blocked review; no eligibility |
| `FX-CONDITIONAL` | literal platform and TYPE_CHECKING imports; inventory | both targets COUNT; inventory gate; no exclusion |
| `FX-DYNAMIC-LITERAL` | literal importlib/subprocess target; inventory | target COUNT/edges; deterministic inventory hash |
| `FX-DYNAMIC-COMPUTED` | computed target; inventory | card, awaiting_human gate; no executor request |
| `FX-HIDDEN-SURFACE` | cases sixth surface, correction 1/2, no-progress, ceiling, closure, failed closure; inventory/flow | sixth→awaiting_human; rounds→ordinals/counts 1/2; repeat→blocked; ceiling→card/awaiting_human; closure→decision/closed gate; partial closure→accepted remains |

Each case specifies exact initial file list/bytes, operation entrypoint, mutation, expected validation
code, record list/order, final state, forbidden files and replay outcome using the constants and table
above. The definitive §31 generator spells out canonical JSON and hashes independently of production
constants. IP-01–IP-09 use the same constants and assert every §30 outcome.
No additional fixture artifact path is created.

## 27. Reconciled budget and end-to-end control coverage

| Module | Principal functions/classes/protocols and included logic | New LOC | Reuse | Risk allocation |
| --- | --- | ---: | ---: | ---: |
| `fal002.py` | Event/transition table, apply_event, orchestration, correction/no-progress, decisions, eligibility, closure | 330 | 0 | 25 |
| `fal002_model.py` | five dataclasses, nested validators, canonical JSON, ID/hash, schema generator/checker, error enums | 420 | 0 | 35 |
| `fal002_inventory.py` | manifest, AST resolver, dynamic/subprocess edges, exemptions, LOC/module/adapter/surface/dependency output | 360 | 0 | 30 |
| `fal002_io.py` | exclusive persistence, load/recovery, 13 collectors/parsers, redaction, two protocols, provenance checks/error mapping | 550 | 0 | 50 |
| **Expected** | **all production behavior** | **1,660** | **0** | **140 to 1,800 maximum** |

Risk allocation is shared unallocated margin, not expected LOC or scope. Production logic, generators
and generated runtime code count. Test LOC, 19 fixture files, five purely derivative schemas and
documentation are excluded; schemas still consume five surfaces. No dependency is added. Exceeding
1,800 new LOC, eight modules, one adapter per role, six surfaces or zero new dependencies requires a
new Human Decision. The envelope is a maximum, never a target.

| Control | Normative requirement | Canonical contract / implementation | State/authority mapping | Verification / fixture | Failure |
| --- | --- | --- | --- | --- | --- |
| `FAL2-CC-01` | generated schemas equal model | §21; model generator | pre-persist model authority | byte round-trip; five VALID cases | BLOCKED |
| `FAL2-CC-02` | reject malformed boundaries | §21 order; validators | INVALID_EVIDENCE | invalid Gate/Run/Decision cases | BLOCKED |
| `FAL2-CC-03` | frozen identity/count persists | Gate payload; chain loader | reopen never resets | HASH-ORDER/correction cases | BLOCKED |
| `FAL2-CC-04` | collector owns facts | RunRecord; collectors | COLLECT_COMPLETE | RUN-VALID/executor contradiction | BLOCKED |
| `FAL2-CC-05` | two corrections/no-progress | Gate control; core | §22 correction events | HIDDEN-SURFACE flow cases | BLOCKED/awaiting_human |
| `FAL2-CC-06` | blockers forbid PASS | Review/eligibility validators | REVIEW_PASS guard | REVIEW-INVALID | BLOCKED |
| `FAL2-CC-07` | criterion binding/rationale | Review fields; resolver | reviewer semantic authority | review valid/invalid | no eligibility/BLOCKED |
| `FAL2-CC-08` | truthful fresh review | §23 provenance/precheck | START_REVIEW guard | principal/context cases | card/awaiting_human |
| `FAL2-CC-09` | adverse append-only history | Gate chain; recovery | never rewrite | HASH-ORDER/PARTIAL/CONFLICT | awaiting_human |
| `FAL2-CC-10` | cards block defaults | HumanDecision; core | decision events | DECISION cases | awaiting_human/blocked |
| `FAL2-CC-11` | human-only atomic close | closure fields; core/I/O | HUMAN_CLOSE only | closure/replay/IP cases | no closure |
| `FAL2-CC-12` | forbidden command/path | request policy; allowlist | before execution | EXEC invalid/policy literals | BLOCKED |
| `FAL2-CC-13` | hard limits | inventory output | MARK_READY guard | HIDDEN-SURFACE/self-inventory | awaiting_human |
| `FAL2-CC-14` | complete command evidence | RunRecord 13; I/O | COLLECT_COMPLETE guard | RUN collector cases | BLOCKED |
| `FAL2-CC-15` | separate implementation review | ReviewerExchange/§23 | PASS/eligibility | REVIEW-VALID/independence cases | no eligibility |
| `FAL2-CC-16` | human closure decision | CLOSURE model; core | accepted→closed only | closure/replay/partial | no closure |

Failure `reason_code` is exactly one of `MALFORMED_BOUNDARY`, `UNSUPPORTED_VERSION`, `HASH_MISMATCH`,
`FORBIDDEN_TRANSITION`, `AUTHORITY_CONFLICT`, `MISSING_EVIDENCE`, `STALE_RECORD`, `DUPLICATE_CONFLICT`,
`PREDECESSOR_GAP`, `COMMAND_FAILURE`, `TIMEOUT`, `INTERRUPTED`, `INDEPENDENCE_FAILURE`,
`NO_PROGRESS`, `CORRECTION_CEILING`, `LIMIT_BREACH` or `PENDING_DECISION`.

`CORR-008-01` through `CORR-008-07` and all ten listed findings are `ADDRESSED — AWAITING
INDEPENDENT REVIEW`. This statement is not verification, PASS, closure or Implementation
Authorization. The next gate is a fresh independent read-only Standard-Assurance review.

## 28. CORR-010 nested canonical contracts (superseded where sections 35–40 differ)

Sections 28–32 record the `HD-FAL-010` refinements. Sections 34–42 are the final `HD-FAL-013`
replacement wherever they differ, including evidence bindings, invocation containers, decisions,
RunRecord versions, recovery, cards, finding lifecycle, no-progress and fixture generation. No
`Json` catch-all remains at a boundary.

### 28.1 Gate payload discriminated union

Every `GateRecord.payload` has exactly `frozen_hash:Sha256`, `correction_count:int 0..2`,
`variant_kind` and the same-named variant object below. The nine pre-CORR-011 variants were:

| `variant_kind` | Exact variant object |
| --- | --- |
| `MANIFEST` | `manifest:{scope_hash:Sha256,criteria_hash:Sha256,allowed_paths:PathRel[1..65535],command_policy_hash:Sha256,executor_principal_id:NonEmpty,reviewer_principal_id:NonEmpty,executor_adapter_id:NonEmpty,reviewer_adapter_id:NonEmpty,offline_evidence:OfflineEvidence}` |
| `INVENTORY` | `inventory:{entrypoint:PathRel,baseline_commit:hex40|hex64,python_version:"3.14",files:InventoryFile[1..8],edges:InventoryEdge[0..65535],exemptions:Exemption[0..65535],counts:InventoryCounts,dependencies:DependencyInventory,unresolved_targets:UnresolvedTarget[0..65535],disposition:"PASS"|"AWAITING_HUMAN"}` |
| `EXECUTION` | `execution:{execution_id:ExecutionId,run_id:RunId,ordinal:int 0..9999,request_kind:"INITIAL"|"CORRECTION",request:ExecutorRequest,request_hash:Sha256,invocation_grant:InvocationGrant}` |
| `EVIDENCE` | `evidence:{run_id:RunId,run_record_hash:Sha256,execution_id:ExecutionId,command_ids:CommandId[13],evidence_hash:Sha256}` |
| `REVIEW` | `review:{review_id:ReviewId,run_id:RunId,ordinal:int 0..9999,packet:ReviewerPacket,packet_hash:Sha256,invocation_grant:InvocationGrant}` |
| `CONTROL` | `control:{ordinal:int 0..9999,correction_count:int 0..2,diff_hash:Sha256,evidence_hash:Sha256,finding_ids:NonEmpty[0..65535],progress:"MATERIAL"|"NONE"|"CEILING"}` |
| `CHECKPOINT` | `checkpoint:{reason_code:ReasonCode,source_record_ids:NonEmpty[0..65535],source_hashes:Sha256[0..65535],interruption_id:InterruptionId|absent,decision_id:DecisionId|absent,resume_state:"ready"|"evidence_ready"|"correction_required"|absent,staging_path:PathRel|absent}` |
| `ELIGIBILITY` | `eligibility:{review_id:ReviewId,review_hash:Sha256,criterion_ids:NonEmpty[1..65535],finding_ids:NonEmpty[0..65535],eligible:boolean}` |
| `CLOSURE` | `closure:{decision_id:DecisionId,decision_hash:Sha256,eligible_gate_id:GateId,eligible_gate_hash:Sha256}` |

`InventoryFile` is exactly `{path:PathRel,content_hash:Sha256,parent_edge:NonEmpty|absent,
inbound_edges:NonEmpty[0..65535],reason:"ENTRYPOINT"|"STATIC_IMPORT"|"DYNAMIC_LITERAL"|
"SUBPROCESS_LITERAL"|"PACKAGE_INIT",classification:"COUNT"|"EXEMPT",counted_loc:int>=0,
roles:("EXECUTOR_ADAPTER"|"REVIEWER_ADAPTER")[0..2]}`. `InventoryEdge` is exactly
`{edge_id:NonEmpty,source:PathRel,target:PathRel,kind:"IMPORT"|"DYNAMIC"|"SUBPROCESS"|
"PACKAGE_INIT",locator:NonEmpty}`. `Exemption` is exactly `{path,baseline_hash,current_hash,
provenance_ref,closure:PathRel[],predicates:[{name,status:"VERIFIED_TRUE"|"VERIFIED_FALSE"|
"UNKNOWN"|"NOT_EVALUATED",evidence_ref}],classification:"EXEMPT"|"COUNT"|"AWAITING_HUMAN"}`.
`InventoryCounts` is exactly `{modules:int>=0,new_production_loc:int>=0,executor_adapters:int>=0,
reviewer_adapters:int>=0,schema_surfaces:int>=0}`. `DependencyInventory` is exactly
`{stdlib:NonEmpty[],existing_third_party:NonEmpty[],new_direct:NonEmpty[],new_transitive:NonEmpty[],
manifest_hash:Sha256,lock_hash:Sha256|absent}`. `UnresolvedTarget` is exactly
`{source:PathRel,locator,expression,kind:"DYNAMIC"|"SUBPROCESS"|"IMPORT",reason}`.

`ExecutorRequest` is exactly `{frozen_hash,scope:PathRel[],criteria:NonEmpty[],allowed_paths:
PathRel[],command_ids:CommandId[13],correction_count:int 0..2,work_packet_hash,request_kind:
"INITIAL"|"CORRECTION"}`. `ReviewerPacket` is exactly `{frozen_hash,run_record_id:RunId,
run_record_hash,criterion_ids:NonEmpty[],evidence_index:EvidenceBinding[],instructions_hash}`.
`EvidenceBinding` is exactly `{criterion_id,source_record_id,locator,content_hash,provenance:
{authority:"COLLECTOR"|"REVIEWER",collector_id:CommandId|absent,record_id,record_hash}}`.

For every variant `variant_kind` must match its sole present variant key; all other variant keys are
absent. MANIFEST is legal only at sequence zero. EXECUTION `request_kind` must equal its nested value;
CORRECTION requires correction count 1 or 2. EVIDENCE must reference a durable RunRecord. REVIEW must
reference that evidence gate. ELIGIBILITY requires a valid PASS result. CLOSURE requires the
immediately preceding accepted gate and accepted closure decision. Arrays use §21 ordering rules.
Every nested value participates in `payload_hash`; JSON Schema uses `$defs` for the exact types above,
`oneOf` keyed by the literal discriminator and `additionalProperties:false` at every object.

### 28.2 Command-discriminated parsed-result union

`CommandEntry.parsed` is one of the following exact objects, selected by `command_id`; no other
shape is valid. Failure entries retain the same shape with `available:false`, all value fields absent,
and required `failure_reason:ReasonCode`. Success entries require `available:true`, value fields, and
no failure reason.

| Command ID | Exact success `parsed` object |
| --- | --- |
| `GIT-ROOT` | `{available:true,root:"."}` |
| `GIT-HEAD-BASELINE` | `{available:true,head:hex40|hex64,kind:"BASELINE"}` |
| `GIT-BRANCH` | `{available:true,branch:NonEmpty}` |
| `INVENTORY` | `{available:true,inventory_hash:Sha256,disposition:"PASS"|"AWAITING_HUMAN",counts:InventoryCounts}` |
| `GIT-HEAD-FINAL` | `{available:true,head:hex40|hex64,kind:"FINAL"}` |
| `GIT-STATUS` | `{available:true,entries:[{xy:two ASCII status bytes,path:PathRel,original_path:PathRel|absent}],changed_paths:PathRel[]}` |
| `GIT-DIFF` | `{available:true,redacted_content_hash:Sha256,byte_count:int>=0}` |
| `GIT-NUMSTAT` | `{available:true,entries:[{path:PathRel,added:int|null,deleted:int|null}]}` |
| `SCHEMA-CHECK` | `{available:true,schemas:[{schema_id:SurfaceId,sha256:Sha256}]}` exactly five, sorted by ID |
| `PYTEST` | `{available:true,passed:int>=0,failed:int>=0,skipped:int>=0,xfailed:int>=0,xpassed:int>=0,errors:int>=0,warnings:int>=0,duration_seconds_decimal:NonEmpty}` |
| `RUFF-LINT` | `{available:true,status:"PASS"|"FAIL"}` |
| `RUFF-FORMAT` | `{available:true,status:"PASS"|"FAIL"}` |
| `FORGE-STATUS` | `{available:true,categories:[{name:NonEmpty,status:"OK"|"WARNING"|"NOT_APPLICABLE",evidence_lines:NonEmpty[]}]}` |

`CommandId` is exactly those 13 literals. `SurfaceId` is exactly the five IDs in §3. Git status
entries remain raw command order while `changed_paths` sorts bytewise; numstat and schemas sort by
path/ID. Decimal duration is the exact ASCII decimal token without unit and is never converted to
float. Binary numstat alone permits null counts. Classification and exit/termination must agree with
§24; mismatch is `MALFORMED_BOUNDARY`.

### 28.3 Human-decision vocabulary

`domain` is exactly `SCOPE`, `CRITERIA`, `BUDGET`, `AUTHORITY_CONFLICT`, `EXECUTOR_RETRY`,
`REVIEWER_RETRY`, `RECOVERY`, or `CLOSURE`. Allowed choices are fixed:

| Domain | `allowed_choices` exact ordered array | Accepted choice effect |
| --- | --- | --- |
| `SCOPE` | `["AUTHORIZE_NEW_SERIES","DECLINE"]` | new series only under later scope Human Decision; current series remains awaiting_human |
| `CRITERIA` | `["AUTHORIZE_NEW_SERIES","DECLINE"]` | same, with new frozen criteria authority required |
| `BUDGET` | `["AUTHORIZE_BUDGET_CHANGE","DECLINE"]` | later budget decision only; no local change |
| `AUTHORITY_CONFLICT` | `["SELECT_SOURCE_A","SELECT_SOURCE_B","ABANDON_SERIES"]` | chosen source ID must equal card source A/B; abandon blocks |
| `EXECUTOR_RETRY` | `["RETRY","DECLINE"]` | RETRY resumes ready with new ordinal, unchanged correction count |
| `REVIEWER_RETRY` | `["RETRY","DECLINE"]` | RETRY resumes evidence_ready with new ordinal |
| `RECOVERY` | `["AUTHORIZE_SUCCESSOR_SERIES","ABANDON_SERIES"]` | successor requires separately accepted recovery decision carrying chain/count |
| `CLOSURE` | `["CLOSE","DECLINE"]` | CLOSE allowed only with exact sealed eligibility |

`decision_card` is exactly `{question,domain,target:{series_id,gate_id,gate_hash},source_a:
{record_id,record_hash,authority},source_b:{record_id,record_hash,authority}|absent,allowed_choices}`.
`authority` is exactly `HUMAN|COLLECTOR|CANONICAL_MODEL|REVIEWER|STATE_SERIES|REPOSITORY_HISTORY`.
RESOLUTION adds exactly `{resolves_decision_id,selected_choice,rationale}`. No choice is implied or
defaulted. The selected choice must be a member of the card array and satisfy the domain invariant.
DECLINED status requires the domain's DECLINE/ABANDON choice. The former undefined CLOSURE-domain
requirement is withdrawn; final closure is exclusively §35.5. Decision target and source hashes
participate in payload and record hashes.

## 29. Forge-owned invocation provenance

Forge core, not either adapter, owns role provenance. Gate-zero MANIFEST binds distinct human-selected
`executor_principal_id`, `reviewer_principal_id`, `executor_adapter_id` and `reviewer_adapter_id`.
Equality is invalid before ready. These identifiers name authorized roles, not adapter-returned claims.

Immediately before invocation core creates an `InvocationGrant` embedded in the durable EXECUTION or
REVIEW gate. It is exactly `{grant_id,role:"EXECUTOR"|"REVIEWER",principal_id,adapter_id,context_id,
input_record_id,input_hash,issued_by:"FORGE_CORE",issued_at,prior_context_id:NonEmpty|absent,
allowed_effect:"RETURN_EXECUTOR_RESULT"|"RETURN_REVIEW_RESULT"}`. `grant_id=H({series_id,
gate_sequence,role,principal_id,adapter_id,input_hash})`. The immutable grant is part of the gate hash.
Adapter output contains only `grant_id`; identity/freshness facts never come from adapter output.

I/O records caller-side `ObservedInvocation` exactly as `{grant_id,resolved_adapter_path:PathRel,
adapter_content_hash:Sha256,process_id:int,thread_id:int,object_identity:int,started_at,ended_at|absent,input_hash,
output_hash:Sha256|absent,termination:"RETURNED"|"TIMEOUT"|"INTERRUPTED"|"ERROR"}`. Adapter path/hash
must equal frozen inventory attribution. OS process/thread values are sampled by I/O before/after
entry and cannot be supplied by the result. The executor observation is exactly
`ExecutorExchange.invocation.observed`; the reviewer observation is exactly
`ReviewerExchange.reviewer_execution.observed`. Their grants are copied from the embedding gate and
both objects participate in exchange payload/record hashes.

A fresh reviewer context requires all of: REVIEW grant and manifest reviewer identities; context ID
`H("review-context:"+review_id+":"+run_record_hash)[:24]`; no earlier equal context ID;
`prior_context_id` absent; input hash covering only minimal packet/fixed adversarial instructions;
reviewer principal/adapter distinct from executor; newly constructed reviewer adapter object after
executor return; and no write or transition callback in its Protocol.

Same process/module is permitted under Standard Assurance only when manifest principals and adapter
entrypoint IDs differ and every check passes; content hashes may match only when both distinct
entrypoints reside in the same frozen attributed module. This is structural separation, not High-
Assurance isolation. Same principal/entrypoint, inherited context, missing/mismatched grant or
adapter-supplied provenance is `INDEPENDENCE_FAILURE`: no reviewer exchange, one card, then
awaiting_human.

## 30. Unified staged publication and authoritative corruption

This replaces §14.2 authoritative-write operations and conflicting §25 clauses. It is the single
durability model for all five authoritative record types. It uses stdlib exclusive creation and
same-volume atomic hard-link publication inside existing series directories; staging is internal
non-authoritative persistence, not a schema surface or new namespace.

For final path `P` and precomputed canonical bytes/hash `R`, staging path is
`P.name+".stage-"+record_hash+"-"+attempt:04d` in `P.parent`. Attempt is the smallest 0..9999 whose
path is absent. Algorithm:

1. validate/build all bytes in memory and resolve final/parent under series root;
2. if final exists, identical bytes/hash are idempotent; different bytes are authority conflict;
3. scan staging attempts: exact complete hash is reusable; partial/different attempts remain preserved;
4. otherwise exclusive-create next attempt, write, flush/fsync, close, reread/hash, fsync parent;
5. publish atomically with `os.link(stage,P)`; `FileExistsError` returns to step 2; a filesystem
   lacking same-volume atomic hard links returns AWAITING_HUMAN before any write;
6. reread/hash final, flush the final file, then and only then grant authority. On POSIX, parent
   directory fsync is additionally mandatory. On Windows (`os.name=="nt"`), where stdlib directory
   fsync is unavailable, successful same-volume link, final-file flush/fsync and reread/hash are the
   accepted local durability boundary; no implementation choice exists.

Staging files are never deleted, truncated, renamed or authoritative. Crash during staging leaves
final wholly absent and retryable with the next attempt; crash after link leaves final wholly present
and adoptable. The algorithm cannot create a partial canonical final. A discovered partial/invalid
final proves an out-of-contract writer: preserve it, stop AWAITING_HUMAN and retain the last valid gate
as authority without asserting a new state.

| IP | Exact authoritative recovery |
| --- | --- |
| IP-01 | no bytes; repeat validation with same IDs |
| IP-02 | no stage/final; same sequence/ordinal, attempt zero |
| IP-03 | partial stage preserved/non-authoritative, final absent; next attempt, same canonical record/sequence/ordinal |
| IP-04 | exact complete stage reused, otherwise preserved and next attempt; final absent |
| IP-05 | linked final is complete; exact hash adopted, mismatch is out-of-contract conflict |
| IP-06 | earlier final authoritative/later absent; reconstruct same later bytes/ID and publish; missing adapter result uses grant retry |
| IP-07 | same final hash idempotent; different final invokes conflict workflow |
| IP-08 | gap prevents publication; preserve files; checkpoint only at next valid free sequence, otherwise last valid gate plus awaiting-human diagnostic |
| IP-09 | hash-named current temp remains cache-only; rebuild/replace from latest valid gate |

The former `H(sorted source tuples)` ID expression is withdrawn; §37 is the sole card identity rule.
Historically, bytes were complete before staging. Crash before/during card staging leaves final absent and replay republishes
identical bytes. Crash after card link adopts it. Only then is the awaiting_human gate staged using the
same model. Crash during gate staging leaves card durable/gate absent; replay adopts card and publishes
the identical gate. A different final card is preserved as conflict; no alternate semantic ID exists.
Thus every conflict has exactly one schema-valid canonical card.

Closure uses the same decision-then-gate publication. Partial staging cannot close; a published
decision with absent gate is adopted and the identical closed gate is republished. No overwrite,
delete, truncate or evidence loss occurs.

## 31. Historical fixture generator design (withdrawn; replaced by section 40)

The generator described in this section is withdrawn as an oracle because it did not determine every
primitive and mutation. Section 40 is the sole fixture authority. Historically, it proposed a test-only
generator implemented inside `tests/test_fal002_model.py`; it imports only stdlib `json`, `hashlib`
and `pathlib`, never `forge.*`, generated schemas or production constants. There is no randomness.

Primitive vocabulary is fixed: series `00000000-0000-4000-8000-000000000002`; time zero
`2026-08-01T00:00:00.000000Z`; each subsequent record adds one microsecond; baseline
`7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68`; branch `main`; scope `forge/fal002.py`; criterion
`FAL2-CC-01`; principals `principal-executor`/`principal-reviewer`; adapters
`forge/fal002_io.py#executor`/`#reviewer`; fixed content strings `F`, `S`, `C`, `P`, `R` are hashed as
their raw UTF-8 bytes. Canonical encoder and H are the literal §21 algorithm reimplemented locally.
The valid command oracle is root `.`, both heads equal baseline, branch `main`, empty status/diff/
numstat, inventory counts `{modules:5,new_production_loc:1660,executor_adapters:1,
reviewer_adapters:1,schema_surfaces:5}`, five schema hashes `H(schema_id raw UTF-8)`, pytest summary
`1 passed in 0.01s` with all other counts zero, both Ruff statuses PASS, and Forge categories
`[{name:"Project Memory Health",status:"OK",evidence_lines:["fixture"]},{name:
"Version Consistency",status:"WARNING",evidence_lines:["fixture"]}]`.

Generator operations are exactly `record(kind,sequence,ordinal,fields)`, `mutate(path,value|DELETE)`,
`stage(record,attempt,prefix_length|FULL)`, and `publish(stage)`. `record` fills only §28 fields,
derives IDs by §14, predecessor from prior literal record hash, created time by sequence microsecond,
then payload/record hashes. `mutate` applies one JSON-pointer replacement after valid construction and
does not recompute hashes unless the case says `REHASH`. `stage` emits the exact prefix of canonical
bytes at the §30 path. `publish` produces a byte-identical final hard-link view. Output is one canonical
JSON fixture file at the existing §18 path containing exact `initial_files`, `operation`, `fault`,
`expected_files`, `forbidden_paths`, `expected_state`, `reason_code`, and `replay` objects. Paths sort
bytewise; file values are lowercase hex of exact bytes. These rules uniquely determine every byte,
ID, predecessor and hash without production logic.

The generator input cases are exhaustive and fixed:

| Fixture | Case IDs and exact generator operation/fault → expected record sequence/state/reason |
| --- | --- |
| `FX-GATE-VALID` | `valid-ready`: gate0 then MARK_READY → gate1/ready/NONE |
| `FX-GATE-INVALID` | `missing-predecessor`: gate1 mutate `/predecessor` DELETE → none/draft/PREDECESSOR_GAP; `unknown-field`: add `/unknown=1`, REHASH → none/draft/MALFORMED_BOUNDARY |
| `FX-EXEC-VALID` | `initial-complete`: gate0,gate1, START_EXECUTION, returned result → gate2 then executor exchange/executing/NONE |
| `FX-EXEC-INVALID` | `executor-pass`: valid result add `/result/outcome="PASS"`, REHASH → no exchange/new gate; executing/FORBIDDEN_TRANSITION |
| `FX-RUN-VALID` | `all-command-success`: completed exchange plus 13 literal parsed successes from §28.2 → run then evidence gate/evidence_ready/NONE |
| `FX-RUN-INVALID` | `bad-hash`, `unknown-field`, `missing-executable`, `timeout`, `invalid-utf8`, `malformed-output`, `ambiguous-pytest`: mutate named command/hash or inject §32 bytes → blocked gate only/blocked with respectively HASH_MISMATCH, MALFORMED_BOUNDARY, COMMAND_FAILURE, TIMEOUT, MALFORMED_BOUNDARY, COMMAND_FAILURE, COMMAND_FAILURE |
| `FX-REVIEW-VALID` | `fresh-pass`: valid run/grant plus complete criterion/rationale → review gate, reviewer exchange, eligibility gate/accepted/NONE |
| `FX-REVIEW-INVALID` | `missing-criterion` → blocked gate/MISSING_EVIDENCE; `same-principal`, `inherited-context` → decision card then awaiting gate/INDEPENDENCE_FAILURE |
| `FX-DECISION-VALID` | `retry-executor`: matching pending card and RETRY → resolution then ready gate/ready/NONE |
| `FX-DECISION-INVALID` | `missing-owner`, `unknown-field`, `stale-target` → blocked gate/MALFORMED_BOUNDARY or STALE_RECORD; `declined` → decision then blocked gate/PENDING_DECISION |
| `FX-HASH-ORDER` | `wrong-predecessor`, `sequence-gap`, `stale-sequence` → no publication/last state/PREDECESSOR_GAP or STALE_RECORD |
| `FX-DUPLICATE` | `same-hash` → no record/idempotent; `different-hash` → card then awaiting gate/AUTHORITY_CONFLICT |
| `FX-PARTIAL` | `gate`, `executor`, `run`, `reviewer`, `decision`: stage each record with prefix length `floor(byte_length/2)` → next attempt publishes same final; normal target state/NONE; prefix retained |
| `FX-AUTH-CONFLICT` | `normal`, `crash-before-card-stage`, `crash-mid-card-stage`, `crash-after-card-link`, `crash-mid-gate-stage`, `crash-after-gate-link` → exactly one final card then awaiting gate/awaiting_human/AUTHORITY_CONFLICT |
| `FX-REDACTED-RELEVANT` | `locator-secret`: raw `criterion=abc token='x y'` → exact §32 replacement; review blocked/MISSING_EVIDENCE |
| `FX-CONDITIONAL` | `platform-and-type-checking`: source bytes `if sys.platform=='x': import forge.a\nif TYPE_CHECKING: import forge.b\n` → both files COUNT/ready/NONE |
| `FX-DYNAMIC-LITERAL` | `import-and-subprocess`: source bytes `importlib.import_module('forge.a'); subprocess.run([sys.executable,'forge/b.py'])\n` → both COUNT/ready/NONE |
| `FX-DYNAMIC-COMPUTED` | `computed-name`: source bytes `importlib.import_module(name)\n` → decision then awaiting gate/awaiting_human/PENDING_DECISION |
| `FX-HIDDEN-SURFACE` | `sixth-surface` → awaiting gate/LIMIT_BREACH; `correction-one`, `correction-two` → executing gates with counts 1/2; `no-progress` → blocked gate/NO_PROGRESS; `ceiling` → card then awaiting gate/CORRECTION_CEILING; `closure` → closure decision then closed gate; `closure-mid-stage` → next staging attempt, same decision/gate, closed |

For every case `forbidden_paths` is all canonical record paths not listed in expected files plus every
out-of-policy path. Replay reruns the same operation and must produce byte-identical filesystem map
with no new final record. Tests must first compare generated fixture bytes to committed fixture bytes,
then supply those bytes to production; production can never generate its own oracle.

## 32. Definitive collector representation rules

### 32.1 Offline precondition

Human authority owns the offline requirement through MANIFEST `offline_evidence`. It is exactly
`{evidence_id,source:"HUMAN_DECISION",decision_id,locator,content_hash,collected_at,valid_until,
command_policy_hash}`. `evidence_id=H({decision_id,locator,content_hash,command_policy_hash})`.
`collected_at` and `valid_until` are Timestamps; valid_until must be at least collector start and no
more than 24 hours after collected_at. Gate-zero hash binds it; core checks time and policy hash before
each command. RunRecord repository adds exact `offline_evidence_id` and `offline_evidence_hash`.
Missing, stale, mismatched or non-human evidence creates PENDING_DECISION/awaiting_human before spawn.

### 32.2 Redaction byte grammar

Input is raw stdout/stderr bytes. Scan left-to-right for ASCII case-insensitive key tokens exactly
`token`, `password`, `secret`, `api_key`, `api-key`, `authorization`. A key begins at byte zero or
after ASCII whitespace or one of `{`, `[`, `(`, `,`, `;`; it is followed by optional ASCII space/tab,
then `=` or `:`, then optional space/tab. Value is either: single/double quoted bytes through the next
matching unescaped quote, where backslash escapes exactly the next byte; or unquoted bytes through
ASCII whitespace, NUL, comma, semicolon, `}`, `]`, `)` or end. Replace value bytes only with ASCII
`<REDACTED>` and retain key, separator, spacing and quotes. Unterminated quote consumes to end.

After replacement, resume after replacement; therefore replacements never rescan. At a position,
choose the longest matching key (`authorization` before shorter alternatives); repeated values are
all replaced. Non-ASCII bytes never form key/delimiter. Apply stdout then stderr independently.
Hash exact redacted bytes using §24 preimage before CR/LF normalization. Stored bytes are strict-
UTF-8 decoded redacted bytes with CRLF and CR replaced by LF; invalid UTF-8 after redaction is
MALFORMED_BOUNDARY. The command-specific parsed union is exclusively §28.2.

## 33. CORR-010 control mapping (superseded by sections 34–42)

This table replaces §27 coverage. Test names are planned implementation tests; fixture cases are
normative generator cases from §31. No status here is independent review verification.

| Control | Exact contract and implementation point | State/authority behavior | Literal verification path | Failure disposition |
| --- | --- | --- | --- | --- |
| `FAL2-CC-01` | §21 schema rules + §28 `$defs`; `fal002_model.generate_schemas` | validate before publication | `test_schema_generation_exact`; five valid generator roots and all invalid subcases | BLOCKED |
| `FAL2-CC-02` | §21 validation order + every §28 object; model validators | INVALID_EVIDENCE gate | GATE/RUN/DECISION invalid cases with literal reason codes | BLOCKED |
| `FAL2-CC-03` | Gate common fields/control + chain loader | reopen carries frozen hash/count/ordinal | HASH-ORDER plus correction-one/two and retry cases | BLOCKED |
| `FAL2-CC-04` | §28.2 parsed union; I/O 13 collectors | only COLLECT_COMPLETE creates evidence | RUN valid/all seven invalid collector cases | BLOCKED |
| `FAL2-CC-05` | CONTROL payload + §22 transitions | count 0→1→2; retries only ordinal; no-progress stops | HIDDEN correction/no-progress/ceiling cases | BLOCKED/AWAITING_HUMAN |
| `FAL2-CC-06` | Reviewer result/ELIGIBILITY invariants | REVIEW_PASS rejected on blocker | REVIEW missing-criterion/blocking cases | BLOCKED |
| `FAL2-CC-07` | EvidenceBinding and rationale arrays | reviewer semantic authority, collector identity authority | REVIEW valid and missing/wrong locator/hash cases | BLOCKED/no eligibility |
| `FAL2-CC-08` | MANIFEST roles + InvocationGrant/ObservedInvocation §29 | independence precheck before reviewer | REVIEW same-principal/inherited-context/mismatched-grant | card/AWAITING_HUMAN |
| `FAL2-CC-09` | staged publication §30 + Gate predecessor | only linked verified finals authoritative | PARTIAL/HASH-ORDER/AUTH-CONFLICT all crash cases | last gate retained/AWAITING_HUMAN |
| `FAL2-CC-10` | §28.3 fixed domains/choices | no default; decision event only | DECISION valid/invalid/stale/declined | BLOCKED/AWAITING_HUMAN |
| `FAL2-CC-11` | CLOSURE payload + staged decision/gate | human decision then closed gate | HIDDEN closure/mid-stage/replay | accepted remains until closed gate |
| `FAL2-CC-12` | historical request mapping; final paths/17 IDs + command policy hash in §35.1 | checked before execution grant | EXEC PASS-field/out-of-policy command/path cases | BLOCKED |
| `FAL2-CC-13` | INVENTORY payload/counts + 1,800 envelope | MARK_READY only on PASS | HIDDEN sixth-surface and self-inventory literal counts | AWAITING_HUMAN |
| `FAL2-CC-14` | historical mapping; final RunRecord has 17 entries under §35.1/§35.4 | missing entry prevents evidence gate | RUN valid/missing/timeout/encoding/parser cases | BLOCKED |
| `FAL2-CC-15` | ReviewerPacket + Forge grant/provenance | PASS/eligibility only after seven fresh checks | REVIEW fresh-pass and three independence failures | no eligibility/AWAITING_HUMAN |
| `FAL2-CC-16` | CLOSURE decision vocabulary/eligibility binding | accepted→closed only by human | closure, repeated closure and mid-stage recovery | no premature closure |

Budget remains the §27 allocation: 1,660 expected, 1,800 maximum and 140 margin. Sections 28–32
make already budgeted model, fixture-test, provenance, recovery and parser responsibilities precise;
they add no production module, dependency, adapter or schema surface and do not reopen `EB006-FR-07`.

`CORR-010-01` through `CORR-010-07`, `EB006-IR2-01` through `EB006-IR2-07`, and corresponding
historical residuals are `ADDRESSED — AWAITING INDEPENDENT REVIEW`. None is VERIFIED, CLOSED, PASS
or implementation-authorized. The required next gate is a fresh independent read-only
Standard-Assurance review.

## 34. CORR-011 historical authority and traceability (non-normative after CORR-012)

`HD-FAL-012` remains binding architecture and `HD-FAL-013` authorized CORR-011. Sections 35–42 now
record the reviewed CORR-011 correction claim only and are explicitly non-normative wherever sections
44–49 define the same subject. No implementer may select a CORR-011 definition for hashing,
recovery/discovery, decision lookup, finding evolution or fixtures. Unchanged structural requirements
not restated in sections 44–49 remain in force. The five boundary roots and schema IDs remain §3.

| Objective | Finding | Architecture dependency | Definitive sections | Contract completed | Status |
| --- | --- | --- | --- | --- | --- |
| `CORR-011-01` | `EB006-IR3-01` | none | §§35.2, 40–41 | complete criterion evidence shape, resolver and fixtures | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-011-02` | `EB006-IR3-02` | `HD-FAL-010` provenance | §§35.3–35.5 | final invocation/reviewer containers and closure discriminator | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-011-03` | `EB006-IR3-03` | none | §40 | total stdlib oracle inputs, constructors, mutations and expected bytes/hashes | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-011-04` | `EB006-IR3-04` | `HD-FAL-012` | §§36, 40.5 | deterministic successor lineage and `RECOVERY_ROOT` | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-011-05` | `EB006-IR3-05` | `HD-FAL-012` | §§37, 40.5 | total card preimage, identity, publication and obstruction recovery | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-011-06` | `EB006-IR3-06` | none | §§35.4, 38, 40.4 | runtime/tool versions and resolved offline authority | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-011-07` | `EB006-IR3-07` | lineage carry-forward | §§35.6, 39.1–39.4, 40.6 | complete-lineage finding identity, lifecycle and eligibility | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-011-08` | `EB006-IR3-08` | finding identity and lineage | §§39.5–39.6, 40.6 | exact progress function and ceiling precedence | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |

These statuses are correction-agent claims only. They are not `VERIFIED`, `CLOSED`, `PASS`,
`FULLY COVERED` or Implementation Authorization.

## 35. Historical CORR-011 canonical boundary model (superseded by sections 44–49)

### 35.1 Common rules and final payload union

The former statement that §21 serialization/hashing remained final is **withdrawn**. Section 44 is
the only final serialization/hash contract. The following CORR-011 shapes are historical unless a
section 44–49 rule expressly incorporates them. A string declared `NonEmpty` is valid only when it
equals its own Unicode string after removal of leading/trailing ASCII space, tab, CR and LF; inputs
are rejected rather than trimmed. No Unicode normalization is performed. A `JsonPointer` is `""` for
the complete object or `/`-prefixed RFC 6901 tokens with only `~0` and `~1` escapes; non-minimal or
invalid escapes are rejected. Resolution is against the canonical source object before hashing.
`PathAbs` is an absolute normalized platform path returned by `Path.resolve(strict=True)`, serialized
with `/`, with uppercase Windows drive letter when present and no trailing `/` except a filesystem
root; non-canonical input is rejected.

`GateRecord.payload.variant_kind` has exactly ten values: `MANIFEST`, `INVENTORY`, `EXECUTION`,
`EVIDENCE`, `REVIEW`, `CONTROL`, `CHECKPOINT`, `ELIGIBILITY`, `CLOSURE`, `RECOVERY_ROOT`. The first
nine use §28.1 except where this section replaces their nested types. `RECOVERY_ROOT` is §36.4.
Exactly one same-named variant key is present. All nested objects use `additionalProperties:false`.

Final command count is **17**, in this exact order:

`GIT-ROOT`, `PYTHON-VERSION`, `GIT-VERSION`, `PYTEST-VERSION`, `RUFF-VERSION`,
`GIT-HEAD-BASELINE`, `GIT-BRANCH`, `INVENTORY`, `GIT-HEAD-FINAL`, `GIT-STATUS`, `GIT-DIFF`,
`GIT-NUMSTAT`, `SCHEMA-CHECK`, `PYTEST`, `RUFF-LINT`, `RUFF-FORMAT`, `FORGE-STATUS`.

Every earlier `[13]`, “13 entries” or thirteen-command policy is replaced by this ordered set.
`ExecutorRequest.command_ids`, `EVIDENCE.command_ids`, RunRecord validation, collectors and fixtures
all use these 17 IDs.

### 35.2 `EvidenceBinding`

`EvidenceBinding` is exactly:

```text
{
  criterion_id: CriterionId,
  evidence_kind: "REPOSITORY_STATE" | "DIFF" | "COMMAND_RESULT" | "TEST_RESULT" |
                 "BUILD_RESULT" | "INVENTORY" | "SCHEMA" | "REVIEW_FINDING" |
                 "HUMAN_DECISION",
  source_surface: SurfaceId,
  source_record_id: NonEmpty,
  locator: JsonPointer,
  assertion: NonEmpty,
  content_hash: Sha256,
  provenance: {
    authority: "COLLECTOR" | "REVIEWER" | "HUMAN",
    record_id: NonEmpty,
    record_hash: Sha256,
    collector_id: CommandId | absent
  }
}
```

All fields are required except `collector_id`. It is required iff authority is `COLLECTOR` and
forbidden otherwise. `source_record_id == provenance.record_id`. `source_surface` is one of the five
§3 IDs. `record_hash` is the artifact hash required by FAL-002 §10. `content_hash` is SHA-256 of the
canonical JSON bytes, without terminal LF, of the value resolved by `locator`; scalar strings are
hashed as JSON strings, not raw text. The locator must resolve exactly once. `assertion` is reviewer-
visible text stating the bounded proposition supported by the resolved value; it participates in
hashes but is never treated as cryptographic semantic proof.

Allowed authority/surface pairs are: COLLECTOR→RunRecord or inventory GateRecord;
REVIEWER→ReviewerExchange; HUMAN→HumanDecisionRecord. `collector_id` must name the command whose
canonical entry contains the resolved value, except INVENTORY for an inventory gate. Wrong surface,
authority, ID, locator, hash, criterion, empty assertion, unknown kind/field or duplicate binding is
`MALFORMED_BOUNDARY` or `HASH_MISMATCH` before review. Bindings sort by
`(criterion_id UTF-8, evidence_kind UTF-8, source_record_id UTF-8, locator UTF-8)` and reject duplicate
tuples.

`ReviewerPacket.evidence_index` and `ReviewerExchange.result.criterion_evidence` contain this exact
type. Result bindings must be byte-identical members of the packet index; a reviewer cannot rewrite
collector identity. PASS requires at least one resolving binding and one semantic rationale for each
criterion, and the complete-lineage finding scan in §39.4.

### 35.3 Final invocation types

`InvocationGrant` is exactly:

```text
{grant_id:Sha256,role:"EXECUTOR"|"REVIEWER",principal_id:NonEmpty,adapter_id:NonEmpty,
 context_id:NonEmpty,input_record_id:NonEmpty,input_hash:Sha256,issued_by:"FORGE_CORE",
 issued_at:Timestamp,prior_context_id:NonEmpty|absent,
 allowed_effect:"RETURN_EXECUTOR_RESULT"|"RETURN_REVIEW_RESULT"}
```

`grant_id` is `H({"domain":"fal002-invocation-grant-v1","series_id":series_id,
"gate_sequence":sequence,"role":role,"principal_id":principal_id,"adapter_id":adapter_id,
"input_hash":input_hash})`. Role and allowed effect must correspond. `prior_context_id` is absent for
a fresh reviewer and permitted only for an executor retry explicitly authorized by a decision.

`ObservedInvocation` is exactly:

```text
{grant_id:Sha256,resolved_adapter_path:PathRel,adapter_content_hash:Sha256,
 process_id:int>=1,thread_id:int>=1,object_identity:int>=1,started_at:Timestamp,
 ended_at:Timestamp|absent,input_hash:Sha256,output_hash:Sha256|absent,
 termination:"RETURNED"|"TIMEOUT"|"INTERRUPTED"|"ERROR"}
```

`ended_at` and `output_hash` are required iff termination is `RETURNED`; `ended_at` is required and
`output_hash` absent for TIMEOUT/ERROR; both are absent only for INTERRUPTED. End cannot precede
start. OS/process/object observations are evidence, not deterministic IDs.

`ExecutorExchange.invocation` is finally and exclusively:

`{grant:InvocationGrant,observed:ObservedInvocation}`.

`ReviewerExchange.reviewer_execution` is finally and exclusively:

`{grant:InvocationGrant,observed:ObservedInvocation,fresh_context_verified:true,
 read_only_packet_verified:true,separation_checks:NonEmpty[7]}`.

The seven separation checks are exact ordered literals `MANIFEST_ROLE_DISTINCT`,
`PRINCIPAL_DISTINCT`, `ADAPTER_ENTRYPOINT_DISTINCT`, `GRANT_MATCH`, `CONTEXT_FRESH`,
`PACKET_MINIMAL`, `NO_WRITE_CALLBACK`. Each is present once. Reviewer grant role/effect, context
formula and observed grant/input hashes must match §29. Missing or false separation is
`INDEPENDENCE_FAILURE`; no ReviewerExchange final is published. These shapes replace §§21.2,
21.4 and every earlier flat/self-reported invocation shape.

### 35.4 Final `RunRecord`

The final top-level shape is the §21.3 common envelope plus exactly `execution_id`, `ordinal`,
`repository`, `runtime`, `tools`, `commands`, `diff`, `build`.

`runtime` is exactly `{python_implementation:"CPython",python_version:SemVer3,
python_executable:PathAbs,python_executable_sha256:Sha256}`. `SemVer3` is three decimal integers with
no leading zero unless zero. Inventory and execution require major/minor `3.14`; another value is
`UNSUPPORTED_VERSION`.

`tools` is exactly four objects sorted by name:

```text
{name:"git"|"python"|"pytest"|"ruff",version:NonEmpty,executable:PathAbs,
 executable_sha256:Sha256,version_command_id:CommandId}
```

Names map one-to-one to `GIT-VERSION`, `PYTHON-VERSION`, `PYTEST-VERSION`, `RUFF-VERSION`.
Executable is resolved before spawn, canonical absolute with symlinks resolved; SHA-256 covers exact
executable bytes. For pytest/ruff the executable is the Python executable and the distribution
version is observed through the exact module command. Missing executable is `COMMAND_FAILURE`;
unparseable or unsupported Python is `UNSUPPORTED_VERSION`; other unparseable versions are
`COMMAND_FAILURE`. Runtime/tools/commands participate in RunRecord payload and record hashes.

`repository` is §21.3 plus required `offline_evidence_id:Sha256` and
`offline_evidence_record_hash:Sha256`. CommandEntry is §21.3 with final `CommandParsed` from §28.2
plus the four forms below:

- PYTHON-VERSION: `{available:true,implementation:"CPython",version:SemVer3}`;
- GIT-VERSION: `{available:true,version:NonEmpty}` from exactly `git version ` plus token;
- PYTEST-VERSION: `{available:true,version:NonEmpty}` from exactly `pytest ` plus token;
- RUFF-VERSION: `{available:true,version:NonEmpty}` from exactly `ruff ` plus token.

Version commands use exact argv `[PYTHON,"--version"]`, `[git,"--version"]`,
`[PYTHON,"-m","pytest","--version"]`, `[PYTHON,"-m","ruff","--version"]`, timeout 30 seconds,
closed stdin and §24 environment/redaction. Exactly one trimmed line and no stderr is permitted.

### 35.5 Final `HumanDecisionRecord` and closure

The common envelope remains §21. Exactly one `decision_kind` discriminates the payload:

- `PENDING_CARD`, status PENDING, payload `{decision_card:DecisionCard}`;
- `RESOLUTION`, status ACCEPTED or DECLINED, payload
  `{resolves_decision_id:DecisionId,selected_choice:NonEmpty,rationale:NonEmpty}`;
- `CLOSURE`, status ACCEPTED, payload
  `{eligible_gate_id:GateId,eligible_gate_hash:Sha256,review_id:ReviewId,review_hash:Sha256,
    finding_ledger_hash:Sha256}`.

`DecisionCard` is exactly `{question:NonEmpty,domain:DecisionDomain,target:DecisionTarget,
sources:ConflictSource[0..65535],allowed_choices:NonEmpty[2..16]}`. `DecisionTarget` is one
discriminated object: `{target_kind:"GATE",series_id:Uuid,gate_id:GateId,gate_hash:Sha256}`;
`{target_kind:"SERIES_INTENT",series_id:Uuid,frozen_hash:Sha256}`; or
`{target_kind:"RECOVERY_ROOT",series_id:Uuid,gate_id:"gate-00000000",
recovery_condition_hash:Sha256}`. OFFLINE_EXECUTION requires SERIES_INTENT; RECOVERY and recovery
conflicts require RECOVERY_ROOT; all other domains require GATE. Sources use §37 and may be empty only
for OFFLINE_EXECUTION before gate zero. Choices must equal the domain's exact ordered array.

Closure has **no `domain` field**. `decision_kind:"CLOSURE"` is its sole discriminator. The closure
operation checks the exact accepted eligibility gate, review and complete-lineage finding-ledger
hash. Pending card `domain` and choices use §28.3 plus `OFFLINE_EXECUTION` with exact choices
`["AUTHORIZE_OFFLINE","DECLINE"]`, and `RECOVERY` choices are finally
`["AUTHORIZE_RECOVERY_RESUME","ABANDON_LINEAGE"]`. Add `FINDING_DISPOSITION` with exact choices
`["CLOSE_VERIFIED","SUPERSEDE","DECLINE"]`; CLOSE_VERIFIED requires the named finding to be
INDEPENDENTLY_VERIFIED, while SUPERSEDE requires a replacement finding key and rationale in the
card sources. RESOLUTION selected choice must belong to the
referenced card. Every earlier `chosen_value`, absent-on-decline or “closure requires domain” rule is
withdrawn.

### 35.6 Finding canonical objects

`FindingObservation` in ReviewerExchange.result is exactly:

```text
{finding_id:FindingId,finding_key:Sha256,assurance_property:
 "BOUNDARY"|"EVIDENCE"|"INDEPENDENCE"|"RECOVERY"|"AUTHORITY"|"CLOSURE"|
 "DETERMINISM"|"SCOPE"|"BUDGET",defect_locator:NonEmpty,severity:
 "CRITICAL"|"HIGH"|"MEDIUM"|"LOW",blocking:boolean,criterion_ids:CriterionId[1..65535],
 statement:NonEmpty,observation:"NEW"|"STILL_PRESENT"|"ABSENT_AFTER_CORRECTION"}
```

Criterion IDs sort bytewise. `defect_locator` is the canonical repository path plus `#` and a
canonical heading or JSON pointer. `finding_key=H({"domain":"fal002-finding-key-v1",
"assurance_property":assurance_property,"defect_locator":defect_locator,
"criterion_ids":criterion_ids})`; `finding_id="F-"+finding_key[:20]`. Wording, severity and physical
series ID do not affect identity. Duplicate keys in one result are invalid. Lifecycle is §39.

## 36. Historical CORR-011 successor recovery lineage (superseded by §45)

### 36.1 Trigger and obstruction descriptor

For intended canonical final path `P`, canonical bytes `R` and `intended_record_hash`, normal
publication occurs only when P is absent; exact bytes are idempotently adopted. A recovery obstruction
exists when P is a readable different/malformed regular file, a non-regular path object, persistently
unreadable stable path object, or an exclusive-create/link collision whose reread is not R. Transient
I/O without a stable path object retries the same publication and creates no successor. An unwritable
series root stops `AWAITING_HUMAN_EXTERNAL_REPAIR`; it cannot synthesize local authority.

`ObstructionDescriptor` is exactly:

```text
{architecture_domain:"fal002-recovery-lineage-v1",origin_series_id:Uuid,
 predecessor_series_id:Uuid,predecessor_gate_id:GateId,predecessor_gate_hash:Sha256,
 blocked_sequence:int 0..99999999,target_path:PathRel,intended_record_hash:Sha256,
 obstruction_kind:"CONFLICTING_FILE"|"MALFORMED_FILE"|"NONREGULAR_PATH"|"UNREADABLE_PATH",
 observed_content_hash:Sha256|absent,path_object_kind:"REGULAR"|"SYMLINK"|"DIRECTORY"|"OTHER",
 frozen_hash:Sha256}
```

Observed hash is required for readable regular files and absent otherwise. Path kind REGULAR is
required for CONFLICTING/MALFORMED/UNREADABLE; NONREGULAR forbids REGULAR. The descriptor fields are
serialized by §21 canonical JSON without terminal LF and
`recovery_condition_hash=sha256(bytes)`. No time/process/random value participates.

### 36.2 Successor identity

For recovery ordinal `n>=0`, UUIDv5 name is exact UTF-8:

`fal002-recovery-lineage-v1:{recovery_condition_hash}:{n}`

using namespace UUID `6f1b8e9e-6a37-5e3a-9d9e-50dc93295943`. Python's RFC 4122 UUIDv5 lowercase
hyphenated output is canonical. Candidate path is
`.forge/fal002/series/{uuid}/gate/00000000.json`. Ordinal zero is first. A higher ordinal is eligible
only when every lower candidate root contains a preserved stable obstruction. An absent lower root
invalidates all higher candidates; an exact lower root is adopted. There is no ordinal ceiling.

### 36.3 Carry-forward objects

`FindingSnapshot` is `{finding_id,finding_key,state:"OPEN"|"ADDRESSED_AWAITING_REVIEW"|
"INDEPENDENTLY_VERIFIED"|"CLOSED"|"SUPERSEDED",severity,blocking,
last_transition_record_id,last_transition_hash}`.
`DecisionRef` is `{decision_id,decision_hash,domain}`. `ProgressSnapshot` is
`{run_id,diff_hash,progress_evidence_hash,unresolved_finding_set_hash,correction_count}`.
Arrays sort by finding ID, decision ID and run ID respectively and reject duplicates.

### 36.4 `RECOVERY_ROOT`

The sequence-zero GateRecord has `record_id:"gate-00000000"`, `predecessor:null`, state
`awaiting_human`, actor `recovery`, event `RECOVERY_SUCCESSOR`, common `frozen_hash` and inherited
`correction_count`. Its sole variant is exactly:

```text
{recovery_root:{origin_series_id:Uuid,predecessor_series_id:Uuid,
 predecessor_gate_id:GateId,predecessor_gate_hash:Sha256,
 obstruction:ObstructionDescriptor,recovery_condition_hash:Sha256,
 successor_series_id:Uuid,recovery_ordinal:int>=0,predecessor_sealed:true,
 scope_hash:Sha256,criteria_hash:Sha256,allowed_paths_hash:Sha256,
 command_policy_hash:Sha256,max_prior_ordinal:int 0..9999,
 finding_ledger:FindingSnapshot[0..65535],pending_decisions:DecisionRef[0..65535],
 no_progress_history:ProgressSnapshot[0..65535],intended_conflict_card_id:DecisionId,
 intended_conflict_card_hash:Sha256}}
```

The record's `series_id` equals successor_series_id. Origin is the first manifest series.
`allowed_paths_hash=H(sorted MANIFEST allowed_paths array)`. Scope, criteria, paths, policy,
correction count, maximum ordinal, complete current finding ledger, pending cards
and progress history must byte/hash-match the derived predecessor lineage. Missing or reduced carry-
forward is `HASH_MISMATCH`. The cross-segment link lives inside the hashed payload; same-segment
predecessor remains null.

### 36.5 Authority, publication and sealing

I/O detects/hashes the obstruction; core constructs descriptor, UUID, card and root; model validates
identity/carry-forward; I/O stages exact card and root bytes. Root final is hard-linked first under
§30 and reread/validated. That successful validation is the sole authority transition and instantly
seals the predecessor against ordinary append. The card final is then linked. Executor, collector and
reviewer provide none of the descriptor/ordinal/authority choices.

Crash before root final leaves predecessor authoritative but unable to progress; replay reuses stages
and publishes the identical candidate. Crash after root final adopts the successor and publishes an
absent card. Same root bytes are idempotent. Invalid candidate root advances to the smallest eligible
ordinal. If the card final becomes obstructed after root authority, that obstruction targets the card
path and invokes this same successor algorithm from the active recovery segment.

### 36.6 Discovery, forks and continuation

Consumers start at the frozen origin manifest, validate that segment, derive any terminal obstruction
and enumerate only §36.2 candidates. They follow the unique smallest-eligible valid recovery root and
repeat. Latest gate of the resulting segment is current authority. Directory presence and every
`current.json` are non-authoritative. Multiple eligible roots, unjustified higher ordinals, mismatched
carry-forward or a fork is `AUTHORITY_CONFLICT` with no progression.

Recovery is terminal for automation. Only an accepted HumanDecisionRecord bound to the active root
may choose `AUTHORIZE_RECOVERY_RESUME` or `ABANDON_LINEAGE`. Resume appends within the active
successor, preserves every frozen/correction/finding/progress value and resumes only the recorded
pre-obstruction state. It cannot dismiss findings or create PASS/eligibility/closure. A later
obstruction repeats this section; physical segment changes never reset logical lineage.

## 37. Historical CORR-011 conflict-card identity (superseded by §§44–46)

`ConflictSource` is exactly `{authority:"HUMAN"|"COLLECTOR"|"CANONICAL_MODEL"|"REVIEWER"|
"STATE_SERIES"|"REPOSITORY_HISTORY",record_id:NonEmpty,record_hash:Sha256,locator:JsonPointer}`.
Sources sort by UTF-8 tuple `(authority,record_id,record_hash,locator)` and reject duplicate tuples.

The exact preimage is canonical JSON without terminal LF:

```text
{"domain":"fal002-conflict-card-v1","recovery_condition_hash":Sha256,
 "successor_series_id":Uuid,"card_ordinal":0,"sources":ConflictSource[1..65535]}
```

`conflict_hash=sha256(preimage)` and
`decision_id="DC-R-"+successor_series_id_without_hyphens[:12]+"-"+conflict_hash[:12]+"-0000"`.
Card ordinal is zero for the one semantic card of that recovery root and is never incremented to
evade a collision. A later successor caused by card obstruction has a different recovery condition
and successor ID and therefore a different canonical card identity.

The PENDING_CARD DecisionCard target is `{series_id:successor_series_id,gate_id:"gate-00000000",
recovery_condition_hash}`; it does not contain the recovery-root hash, avoiding a card/root hash
cycle. The recovery root binds the complete precomputed card hash. The card records the sorted sources,
question, domain and allowed choices. Same ID/bytes is idempotent. Malformed/different final is
preserved and invokes §36 after root authority. A staged/orphan/inactive-lineage card is evidence only.
Only the exact card bound by the currently active recovery root may be resolved. No card establishes,
selects or competes with GateRecord state authority.

## 38. Historical CORR-011 versions/offline authority (offline lookup superseded by §46)

### 38.1 Offline evidence model

MANIFEST `offline_evidence` is finally:

```text
{evidence_id:Sha256,decision_id:DecisionId,decision_record_hash:Sha256,
 locator:"/payload/selected_choice",content_hash:Sha256,collected_at:Timestamp,
 valid_until:Timestamp,command_policy_hash:Sha256}
```

Before gate zero, the human boundary create-publishes the referenced HumanDecisionRecord under the
same series decision path. It must be a schema/hash-valid ACCEPTED RESOLUTION of a PENDING_CARD whose
domain is `OFFLINE_EXECUTION`; selected choice must be `AUTHORIZE_OFFLINE`. Locator is the exact
literal above and resolves to the JSON string `"AUTHORIZE_OFFLINE"`.
`content_hash=sha256(canonical JSON bytes of that string without LF)` and
`evidence_id=H({"domain":"fal002-offline-evidence-v1","decision_id":decision_id,
"decision_record_hash":decision_record_hash,"locator":locator,"content_hash":content_hash,
"command_policy_hash":command_policy_hash})`.
`collected_at` equals the accepted resolution record's created_at.

Core resolves the canonical decision path, validates the entire record, ID/hash, referenced pending
card, locator and selected value before every spawn. It also requires collected_at ≤ start ≤
valid_until ≤ collected_at+24h. Missing record/card/locator/value is `MISSING_EVIDENCE`; malformed or
non-accepted/declined decision is `MALFORMED_BOUNDARY`; record/content/policy mismatch is
`HASH_MISMATCH`; expiry is `STALE_RECORD`. Each yields PENDING_DECISION/awaiting_human before spawn.
Arbitrary structural claims never satisfy the precondition.

### 38.2 Version evidence

Section 35.4 is collector-owned. I/O resolves/hashes executables and executes all four version probes
before baseline Git evidence. Parser-produced version objects must equal the RunRecord runtime/tools
objects byte-for-byte. Executor/reviewer prose and package metadata without the observed command
cannot supply versions. Unsupported Python stops `UNSUPPORTED_VERSION`; absent or malformed other
version evidence stops `COMMAND_FAILURE`. All version raw hashes, parsed values and executable hashes
participate in RunRecord hashing and may be referenced by EvidenceBinding.

## 39. Historical CORR-011 finding/no-progress model (superseded by §47)

### 39.1 Lifecycle states and authority

The derived `FindingLedger` is internal canonical state inside Gate control/eligibility and
RECOVERY_ROOT carry-forward, not a sixth surface. Each key has exactly one state:

| From | Event and authority | To |
| --- | --- | --- |
| absent | reviewer NEW observation | `OPEN` |
| `OPEN` | core records executor remediation claim plus changed collector facts | `ADDRESSED_AWAITING_REVIEW` |
| `OPEN` | reviewer STILL_PRESENT | `OPEN` |
| `ADDRESSED_AWAITING_REVIEW` | fresh reviewer ABSENT_AFTER_CORRECTION with exact evidence/rationale | `INDEPENDENTLY_VERIFIED` |
| `ADDRESSED_AWAITING_REVIEW` | reviewer STILL_PRESENT | `OPEN` |
| `INDEPENDENTLY_VERIFIED` | reviewer NEW/STILL_PRESENT evidence for same key | `OPEN` |
| `INDEPENDENTLY_VERIFIED` | accepted human finding-disposition decision | `CLOSED` |
| `OPEN`/`ADDRESSED_AWAITING_REVIEW`/`INDEPENDENTLY_VERIFIED` | accepted human supersession decision naming replacement key and rationale | `SUPERSEDED` |

No other transition exists. Executor/correction agent cannot independently verify or close.
Reviewer cannot close/supersede. Human cannot fabricate collector facts and may close only an
independently verified finding. `CLOSED` and `SUPERSEDED` are terminal. Invalid transitions are
`FORBIDDEN_TRANSITION`.

### 39.2 Duplicates, residuals and wording

Finding identity is §35.6. Same key with different wording is the same finding; latest statement is
display text but history is retained. Duplicate key in one review is malformed. A residual at the
same canonical locator/property/criteria keeps the key and transitions to OPEN/STILL_PRESENT. A
distinct locator/property/criterion set is a new finding even if prose resembles an older one.
Automatic semantic collapsing is forbidden. Supersession requires the accepted human transition.

### 39.3 Ledger derivation and hashes

Traverse every verified ReviewerExchange, remediation CONTROL gate, HumanDecisionRecord and
RECOVERY_ROOT in logical-lineage order: segment order from §36 discovery, then gate sequence and
record timestamp/ID tie-break within the causal transition. Apply only valid transitions above.
Recovery snapshots must equal the derived predecessor ledger. The canonical current ledger is an
array sorted by finding_id; `finding_ledger_hash=H(array)`. Unresolved means state OPEN or
ADDRESSED_AWAITING_REVIEW. Physical successor boundaries never alter identity or state.

### 39.4 PASS, eligibility and closure

Before PASS/eligibility, core derives the complete ledger. PASS is forbidden when any unresolved
finding is CRITICAL or `blocking:true`, any pending human decision exists, or any criterion lacks
valid evidence/rationale. A review with `findings=[]` creates no transitions and cannot remove prior
entries. Eligibility stores the exact finding-ledger hash and unresolved finding IDs. Closure
rederives and matches that hash and requires no unresolved blocker. Missing history or mismatched
snapshot is `HASH_MISMATCH`; attempted PASS is `BLOCKED`.

### 39.5 Stable progress fingerprints

For each completed reviewed run, define:

- `diff_hash = RunRecord.diff.sha256`;
- `progress_evidence_hash = H({repository:{baseline_head,final_head,status,changed_paths},
  diff:{sha256,numstat},runtime,tools,commands:[{command_id,termination,exit_code,classification,
  parsed_without_duration}],build})`; timestamps, process/thread/object IDs, raw text, raw hashes and
  pytest `duration_seconds_decimal` are excluded only from this progress fingerprint and remain in
  authoritative RunRecord hashes;
- `unresolved_finding_set_hash=H([{finding_id,state,severity,blocking}] sorted by finding_id)` after
  applying that review.

`parsed_without_duration` equals parsed exactly except PYTEST omits duration. These exclusions avoid
clock/duration noise while retaining observable outcomes.

### 39.6 Exact no-progress function

No-progress is evaluated only after a corrected run receives `CORRECTION_REQUIRED`; the initial run
has no comparison. Previous is the immediately preceding completed reviewed run in the logical
lineage, including predecessor physical segments. Current is the just-reviewed corrected run.

```text
diff_changed = current.diff_hash != previous.diff_hash
evidence_changed = current.progress_evidence_hash != previous.progress_evidence_hash
resolved_any = any previous OPEN/ADDRESSED_AWAITING_REVIEW key is now
               INDEPENDENTLY_VERIFIED/CLOSED/SUPERSEDED
introduced_blocker = any key absent previously is now unresolved and
                     (severity == CRITICAL or blocking == true)
material_progress = (diff_changed or evidence_changed) and resolved_any and not introduced_blocker
no_progress = not material_progress
```

Addressed-but-not-independently-verified is unresolved and never satisfies `resolved_any`. Changed
diff with identical unresolved findings is no progress. A new blocker makes no progress even if an
older finding was verified. On CORRECTION_REQUIRED, precedence is: compute no-progress first;
no_progress→blocked `NO_PROGRESS`; otherwise if correction_count==2→card/awaiting_human
`CORRECTION_CEILING`; otherwise next correction increments count exactly once. RECOVERY_ROOT carries
all ProgressSnapshots, so recovery cannot reset the window or ceiling.

## 40. Withdrawn CORR-011 fixture oracle (superseded in full by §48)

### 40.1 Sole oracle and canonical algorithm

The sole allowed oracle is a test-only function in `tests/test_fal002_model.py` importing only
stdlib `json`, `hashlib`, `uuid` and `pathlib`; it imports no `forge.*`, schemas, fixtures or
production constants. Canonical encoder is exactly `json.dumps(value,ensure_ascii=False,
allow_nan=False,sort_keys=True,separators=(",",":"))` encoded UTF-8. Record files add one LF;
hash preimages do not unless the defining contract explicitly hashes file bytes. UUIDv5 uses
`uuid.uuid5` with §36 namespace/name. Unknown constructor field is an oracle failure. No randomness,
current clock, filesystem metadata or environment input is permitted.

### 40.2 Total primitive vocabulary

The oracle uses only these literal primitives unless a case row overrides them:

| Name | Literal |
| --- | --- |
| origin series | `00000000-0000-4000-8000-000000000002` |
| time `t(n)` | `2026-08-01T00:00:00.` plus six-digit decimal `n` plus `Z` |
| baseline/final HEAD | `7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68` |
| branch/root | `main` / `.` |
| scope/allowed path | `forge/fal002.py` |
| criterion | `FAL2-CC-01` |
| executor/reviewer principal | `principal-executor` / `principal-reviewer` |
| executor/reviewer adapter | `forge/fal002_io.py#executor` / `forge/fal002_io.py#reviewer` |
| Python | `CPython`, `3.14.0`, `C:/python/python.exe`, `H("python-exe")` |
| tools | git `2.50.0` at `C:/Program Files/Git/cmd/git.exe` hash `HB("git-exe")`; python `3.14.0`, pytest `9.0.0`, ruff `0.12.0` at the Python executable/hash above |
| assertion | `The criterion is supported by the resolved value.` |
| locator | `/commands/12/parsed/schemas/0/sha256` |
| raw fixed strings | `F`, `S`, `C`, `P`, `R`, each hashed as raw UTF-8 only where named content hash requires raw bytes |

`H(value)` means SHA-256 of canonical JSON bytes without LF; `HB(text)` explicitly means SHA-256 of
raw UTF-8 text. Common record IDs derive by §§14/36. `created_at=t(sequence)` for gates and
`t(100+ordinal)`, `t(200+ordinal)`, `t(300+ordinal)`, `t(400+ordinal)` for executor, run, review and
decision records. Started/ended use t(500+2*command_index) and t(501+2*command_index).
Hashes map exactly: frozen_hash=`HB("F")`, scope_hash=`HB("S")`, criteria_hash=`HB("C")`,
command_policy_hash=`HB("P")`, work_packet_hash=`HB("R")`, and
allowed_paths_hash=`H(["forge/fal002.py"])`. Finding K is HIGH/blocking, assurance property EVIDENCE,
defect locator `docs/x.md#one`, criterion FAL2-CC-01 and statement `Required evidence is missing.`;
K2 differs only by locator `docs/x.md#two` and statement `A new blocker is present.`. Their keys/IDs
derive only by §35.6.

### 40.3 Total valid constructors

`offline_authority()` returns PENDING_CARD `DC-OFFLINE-000000000000` at t(398), followed by ACCEPTED
RESOLUTION `HD-OFFLINE-000000000000` at t(399), domain OFFLINE_EXECUTION and selected choice
AUTHORIZE_OFFLINE; IDs, record/content hashes and gate evidence use §38 exactly. `gate0()` is the
exact §35 MANIFEST using the literals above, all hashes recomputed, empty exemption arrays, that
offline authority and correction_count 0. `ready()` is sequence 1
INVENTORY with files sorted exactly `forge/__init__.py`, `forge/fal002.py`,
`forge/fal002_inventory.py`, `forge/fal002_io.py`, `forge/fal002_model.py`. Hashes are respectively
`HB("")` then `HB(path)`; LOC are 2,330,360,550,420; reasons are PACKAGE_INIT, ENTRYPOINT and three
STATIC_IMPORT values; only I/O roles are `["EXECUTOR_ADAPTER","REVIEWER_ADAPTER"]`. Exact edges are
fal002.py→`__init__.py` PACKAGE_INIT locator `/package/forge`, and fal002.py→inventory/io/model IMPORT
locators `/imports/0`, `/imports/1`, `/imports/2`. Each `edge_id="E-"+H({source,target,kind,
locator})[:20]`; target parent_edge equals that ID, inbound_edges is its singleton, entrypoint parent
and inbound arrays are absent/empty as permitted. Counts are 5/1660/1/1/5; stdlib is sorted
`["ast","dataclasses","hashlib","json","os","pathlib","subprocess","sys","uuid"]`; existing/new
dependency, unresolved and exemption arrays are empty; disposition is PASS.

`executor_request(kind,count,ordinal)` uses §28 fields, the 17 command IDs, scope/criteria/paths
singletons above and work_packet_hash H(`{"kind":kind,"ordinal":ordinal}`). `grant(role,...)`,
`observed(role,...)` and exchange containers use §35.3 with process/thread/object 1001/2001/3001 for
executor and 1002/2002/3002 for reviewer, RETURNED, exact input/output object hashes and fixed adapter
paths/content hashes HB(adapter ID).

`run(ordinal)` contains §35.4 runtime/tools, clean repository, empty diff/numstat, build unavailable,
and all 17 commands in order. Each has exact argv from §§24/35.4, cwd `.`, sorted environment keys,
empty stderr, raw hashes of redacted bytes, PASS, parser_version 1 and the success parsed object.
Stdout bytes by command ID are exactly:

| Command | Exact UTF-8 stdout before redaction |
| --- | --- |
| GIT-ROOT | `C:/repo/forge-ai-sef\n` |
| PYTHON-VERSION | `Python 3.14.0\n` |
| GIT-VERSION | `git version 2.50.0\n` |
| PYTEST-VERSION | `pytest 9.0.0\n` |
| RUFF-VERSION | `ruff 0.12.0\n` |
| GIT-HEAD-BASELINE / GIT-HEAD-FINAL | baseline literal plus `\n` |
| GIT-BRANCH | `main\n` |
| INVENTORY | canonical JSON of `ready().payload.inventory` plus `\n` |
| GIT-STATUS / GIT-DIFF / GIT-NUMSTAT | empty bytes |
| SCHEMA-CHECK | canonical JSON array of five `{schema_id,sha256:HB(schema_id)}` objects plus `\n` |
| PYTEST | `1 passed in 0.01s\n` |
| RUFF-LINT | `All checks passed!\n` |
| RUFF-FORMAT | `12 files already formatted\n` |
| FORGE-STATUS | `Project Memory Health: OK\n  fixture\nVersion Consistency Status: WARNING\n  fixture\n` |

Parsed objects are exactly §§28.2/35.4; GIT-ROOT resolves to `.`, absent test categories are zero,
schema hashes are HB(schema ID), and offline IDs/hashes use §38 literals.

`binding()` references the RunRecord schema hash at the literal locator, evidence kind SCHEMA,
collector authority, collector ID SCHEMA-CHECK and exact H(resolved JSON string). `review(outcome,
observations)` contains one criterion, that binding byte-identically in packet/result, the literal
rationale `The resolved schema hash supports exact model/schema consistency.`, final reviewer
execution §35.3 and supplied §35.6 observations. `decision(kind)` uses §35.5/§37 exact forms.
`recovery(obstruction,ordinal)` uses §36 and carries the exact derived ledger/decision/progress arrays.
Every constructor computes payload hash, then record hash, then file bytes; no caller supplies a hash.

### 40.4 Mutation operation

`replace(pointer,value)`, `insert(pointer,value)` and `delete(pointer)` apply RFC 6901 to a deep copy.
`raw(command_id,stream,hexbytes)` replaces the named pre-decode byte stream. `REHASH` recomputes all
hash fields from inner to outer; absent REHASH preserves existing hashes. Expected valid file bytes
are `hex(canonical_record+LF)` and expected hash is lowercase SHA-256 of the contract-defined
preimage. Expected invalid cases publish no invalid boundary final and assert the literal reason code.

### 40.5 Exact case operations

The existing 19 fixture files remain the fixture set. Each row below is exhaustive together with the
constructors above; `B` is `[offline pending card, offline accepted resolution, gate0(),ready()]`.

| Fixture/case | Exact arrange and operation | Exact expected result |
| --- | --- | --- |
| GATE-VALID/ready | gate0; construct ready | gate0,ready bytes/hashes; state ready |
| GATE-INVALID/missing-predecessor | ready; delete `/predecessor`; REHASH | no gate1; PREDECESSOR_GAP |
| GATE-INVALID/unknown | ready; insert `/unknown`, integer 1; REHASH | no gate1; MALFORMED_BOUNDARY |
| EXEC-VALID/initial | B; construct execution gate ordinal 0 and completed exchange | gate2 then exchange; executing |
| EXEC-INVALID/pass | valid exchange; insert `/result/outcome`, string `PASS`; REHASH | no exchange; FORBIDDEN_TRANSITION |
| RUN-VALID/all | completed executor; construct run(0), EVIDENCE gate | run then gate; evidence_ready |
| RUN-INVALID/bad-hash | run; replace `/record_hash` with 64 `0` bytes | blocked gate; HASH_MISMATCH |
| RUN-INVALID/unknown | run; insert `/unknown`,1; REHASH | blocked; MALFORMED_BOUNDARY |
| RUN-INVALID/missing-executable | replace `/commands/1/termination`,`SPAWN_ERROR`; replace exit null; replace parsed with failure COMMAND_FAILURE; REHASH | blocked; COMMAND_FAILURE |
| RUN-INVALID/timeout | replace `/commands/13/termination`,`TIMEOUT`; replace `/commands/13/exit_code`,null; replace `/commands/13/parsed` with `{available:false,failure_reason:"TIMEOUT"}`; REHASH | blocked; TIMEOUT |
| RUN-INVALID/invalid-utf8 | raw PYTEST stdout `ff`; no record mutation | blocked; MALFORMED_BOUNDARY |
| RUN-INVALID/malformed | raw GIT-VERSION stdout hex of `git ???\n` | blocked; COMMAND_FAILURE |
| RUN-INVALID/ambiguous | raw PYTEST stdout hex of `1 passed in 0.01s\n1 passed in 0.01s\n` | blocked; COMMAND_FAILURE |
| REVIEW-VALID/pass | valid run; review PASS with no NEW findings and complete binding/rationale | review gate, exchange, eligibility gate; accepted |
| REVIEW-INVALID/missing-binding | delete `/result/criterion_evidence/0`; REHASH | blocked; MISSING_EVIDENCE |
| REVIEW-INVALID/same-principal | replace reviewer grant principal with `principal-executor`; REHASH | no review final; card/recovery; INDEPENDENCE_FAILURE |
| REVIEW-INVALID/inherited | insert reviewer grant `/prior_context_id`,`ctx-old`; REHASH | no review final; card/recovery; INDEPENDENCE_FAILURE |
| DECISION-VALID/retry | pending EXECUTOR_RETRY card; accepted RETRY resolution | decision then ready gate |
| DECISION-INVALID/missing-owner | delete `/owner`; REHASH | no decision; MALFORMED_BOUNDARY |
| DECISION-INVALID/unknown | insert `/unknown`,1; REHASH | no decision; MALFORMED_BOUNDARY |
| DECISION-INVALID/stale | replace target gate hash with 64 `0`; REHASH | blocked; STALE_RECORD |
| DECISION-INVALID/declined | selected choice DECLINE, status DECLINED | decision then blocked gate |
| HASH-ORDER/wrong | replace gate predecessor with 64 `0`; REHASH | no publication; PREDECESSOR_GAP |
| HASH-ORDER/gap | replace gate sequence with 3 and record_id gate-00000003; REHASH | no publication; PREDECESSOR_GAP |
| HASH-ORDER/stale | replace sequence with 0; REHASH | no publication; STALE_RECORD |
| DUPLICATE/same | publish exact existing bytes | no new file; idempotent |
| DUPLICATE/different | target same path with REHASH after assertion change | §36 recovery root; AUTHORITY_CONFLICT |
| PARTIAL/five-kinds | for each boundary stage prefix `floor(len(bytes)/2)` at attempt 0000 | prefix preserved; attempt 0001 publishes exact final; normal state |
| AUTH-CONFLICT/six-crashes | fault before stage, mid-card-stage, after-card-stage, mid-root-stage, after-root-link, after-card-link | §36 smallest eligible root; exactly one active linked card; awaiting_human |
| REDACTED/locator | raw GIT-DIFF stdout bytes `criterion=abc token='x y'` | exact replacement `criterion=abc token='<REDACTED>'`; missing locator blocks |
| CONDITIONAL/imports | UTF-8 source exactly `if sys.platform=='x': import forge.a\nif TYPE_CHECKING: import forge.b\n` | exact `forge/a.py`, `forge/b.py` COUNT files/edges sorted; ready |
| DYNAMIC-LITERAL/two | UTF-8 source exactly `importlib.import_module('forge.a'); subprocess.run([sys.executable,'forge/b.py'])\n` | exact `forge/a.py`, `forge/b.py` COUNT files/edges sorted; ready |
| DYNAMIC-COMPUTED/name | UTF-8 source exactly `importlib.import_module(name)\n` | pending card then awaiting_human |
| HIDDEN-SURFACE/sixth | inventory schema_surfaces replace 6, REHASH | awaiting_human; LIMIT_BREACH |
| HIDDEN-SURFACE/corrections | construct reviewed runs ordinal 0/1/2 with correction counts 0/1/2 | counts/ordinals retained across gates |
| HIDDEN-SURFACE/no-progress | current diff/evidence/finding set equal previous | blocked; NO_PROGRESS |
| HIDDEN-SURFACE/ceiling | material progress true with count 2 | card/awaiting_human; CORRECTION_CEILING |
| HIDDEN-SURFACE/closure | exact eligible review/ledger plus accepted closure | decision then closed gate |
| HIDDEN-SURFACE/closure-stage | half decision stage, then full next attempt and gate | closed after replay; prefix retained |

The CORR-011 subcases below are also mandatory. Every row starts from the fresh valid constructor
named in Arrange, performs every operation left-to-right, then REHASH unless explicitly `NO_REHASH`.
`Z` is the 64-character zero hash. Expected file bytes/hashes are produced by §40.1 after the exact
operation; invalid input is never published as an authoritative final.

| Case ID | Arrange; exact mutation/fault | Exact expected disposition |
| --- | --- | --- |
| `binding-missing-kind` | review(PASS); delete `/result/criterion_evidence/0/evidence_kind` | MALFORMED_BOUNDARY; no review final/eligibility |
| `binding-unknown-kind` | review(PASS); replace same `/evidence_kind` with `OTHER` | MALFORMED_BOUNDARY |
| `binding-missing-assertion` | review(PASS); delete `/result/criterion_evidence/0/assertion` | MALFORMED_BOUNDARY |
| `binding-wrong-content-hash` | review(PASS); replace `/result/criterion_evidence/0/content_hash` with Z | HASH_MISMATCH |
| `binding-wrong-locator` | review(PASS); replace `/result/criterion_evidence/0/locator` with `/missing` | MISSING_EVIDENCE |
| `grant-mismatch` | review(PASS); replace `/reviewer_execution/observed/grant_id` with Z | INDEPENDENCE_FAILURE; no review final |
| `grant-input-mismatch` | review(PASS); replace `/reviewer_execution/observed/input_hash` with Z | INDEPENDENCE_FAILURE |
| `version-python-missing` | run; delete `/tools/2`; delete command index 1 | MISSING_EVIDENCE; no RunRecord final |
| `version-git-malformed` | raw GIT-VERSION stdout `hex(UTF8("git ???\n"))` | COMMAND_FAILURE |
| `version-pytest-malformed` | raw PYTEST-VERSION stdout `hex(UTF8("pytest unknown extra\n"))` | COMMAND_FAILURE |
| `version-ruff-malformed` | raw RUFF-VERSION stderr `hex(UTF8("ruff 0.12.0\n"))`, stdout empty | COMMAND_FAILURE |
| `version-python-unsupported` | replace `/runtime/python_version` and `/commands/1/parsed/version` with `3.15.0` | UNSUPPORTED_VERSION |
| `offline-decision-missing` | B minus both offline authority files; construct gate0 | MISSING_EVIDENCE; no gate0 authority |
| `offline-decision-declined` | replace accepted resolution `/status` with `DECLINED` and `/payload/selected_choice` with `DECLINE`; reconstruct gate0 reference/evidence ID from that decision hash | MALFORMED_BOUNDARY for offline precondition |
| `offline-locator-malformed` | gate0; replace `/payload/manifest/offline_evidence/locator` with `/payload/~2bad` | MALFORMED_BOUNDARY |
| `offline-hash-mismatch` | gate0; replace `/payload/manifest/offline_evidence/content_hash` with Z | HASH_MISMATCH |
| `recovery-conflicting-file` | B; intended execution gate2 R; put different valid canonical gate bytes at its final path | RECOVERY_ROOT ordinal 0; awaiting_human; CONFLICTING_FILE |
| `recovery-malformed-file` | same; put raw bytes hex `7b` (`{`) at gate2 final | RECOVERY_ROOT ordinal 0; MALFORMED_FILE |
| `recovery-nonregular` | same; path object is DIRECTORY, observed hash absent | RECOVERY_ROOT ordinal 0; NONREGULAR_PATH |
| `recovery-unreadable` | same; regular object returns stable ACCESS_DENIED on two reads, observed hash absent | RECOVERY_ROOT ordinal 0; UNREADABLE_PATH |
| `recovery-crash-before-root` | construct/stage card/root; fault immediately before root hard-link | predecessor remains active/unable to progress; replay publishes identical ordinal 0 root |
| `recovery-crash-after-root` | fault immediately after root reread/validation and before card link | successor authoritative awaiting_human; replay publishes staged identical card |
| `recovery-root-collision` | place raw `{` at ordinal-0 root final before link | preserve it; publish exact ordinal-1 root; ordinal 1 uniquely active |
| `recovery-chain-obstruction` | active ordinal-0 root; obstruct its next gate with raw `{` | derive new descriptor from active root and publish its ordinal-0 successor; one logical lineage |
| `card-path-conflicting` | publish root; put different schema-valid card at intended card final | preserve card; next recovery successor targets card path; only new active-root-linked card resolvable |
| `card-path-malformed` | publish root; put raw `{` at intended card final | same successor behavior with MALFORMED_FILE |
| `card-orphan` | publish valid staged card final but fault before any recovery root | origin remains active/unable; card is non-authoritative; replay publishes matching root |
| `card-inactive-lineage` | put valid card beneath unjustified higher successor UUID | ignored as evidence; cannot resolve; active lineage unchanged |
| `finding-omitted-later` | review0 NEW HIGH/blocking key K; remediation gate marks addressed; review1 result `findings=[]` | K remains ADDRESSED_AWAITING_REVIEW; PASS/eligibility blocked |
| `finding-addressed-not-verified` | K OPEN; remediation claim only; no ABSENT_AFTER_CORRECTION observation | K ADDRESSED_AWAITING_REVIEW and unresolved |
| `finding-duplicate` | one review contains two observations with identical finding_key K | MALFORMED_BOUNDARY; no review final |
| `finding-residual` | review0 NEW K; review1 STILL_PRESENT with same property/locator/criteria and changed statement | same finding_id; state OPEN; both statements retained in history |
| `finding-new` | review1 NEW with defect locator `docs/x.md#two` instead of `docs/x.md#one` | distinct key/ID; both unresolved |

The no-progress truth table constructs previous hashes as HB(`d0`)/HB(`e0`) and current hashes as
the same or HB(`d1`)/HB(`e1`). `resolved_any` is constructed by K moving from OPEN to
INDEPENDENTLY_VERIFIED; `introduced_blocker` by adding NEW HIGH/blocking K2. These sixteen Boolean
rows are exhaustive:

| diff changed | evidence changed | resolved any | introduced blocker | Expected |
| --- | --- | --- | --- | --- |
| false | false | false | false | NO_PROGRESS |
| false | false | false | true | NO_PROGRESS |
| false | false | true | false | NO_PROGRESS |
| false | false | true | true | NO_PROGRESS |
| false | true | false | false | NO_PROGRESS |
| false | true | false | true | NO_PROGRESS |
| false | true | true | false | MATERIAL |
| false | true | true | true | NO_PROGRESS |
| true | false | false | false | NO_PROGRESS |
| true | false | false | true | NO_PROGRESS |
| true | false | true | false | MATERIAL |
| true | false | true | true | NO_PROGRESS |
| true | true | false | false | NO_PROGRESS |
| true | true | false | true | NO_PROGRESS |
| true | true | true | false | MATERIAL |
| true | true | true | true | NO_PROGRESS |

For each MATERIAL row, correction_count 0/1 permits the next correction and increments once; count 2
produces CORRECTION_CEILING after progress evaluation. For every NO_PROGRESS row, NO_PROGRESS takes
precedence at counts 0/1/2. Repeating a row after RECOVERY_ROOT uses the carried ProgressSnapshot and
must produce the same result.

### 40.6 Expected output and independence assertion

For every case the generator emits canonical JSON containing exactly
`{fixture_id,case_id,initial_files:[{path,bytes_hex,sha256}],operation,fault,
expected_files:[{path,bytes_hex,sha256}],forbidden_paths,expected_state,reason_code,replay_files}`.
Arrays sort by path then case ID. `bytes_hex` and `sha256` are computed solely by §§40.1–40.5.
Committed fixture bytes must equal generator output before production receives the decoded boundary
files. A test that imports production, schemas or production constants to compute any expected value
fails the oracle-independence test.

## 41. Historical CORR-011 consistency claim (superseded by §49)

| Surface | Producer → consumer | Authority/lifecycle/recovery |
| --- | --- | --- |
| GateRecord | human/core/inventory/collector/recovery → all | sole state authority; canonical schema/chain; RECOVERY_ROOT is a variant; §36 lineage |
| ExecutorExchange | core grant + executor result + I/O observation → collector/core | one complete post-return exchange; no PASS/closure; §35.3 |
| RunRecord | collector → reviewer/core | Git/command/runtime/tool authority; 17 ordered commands; §35.4/§38 |
| ReviewerExchange | core packet + reviewer assessment + I/O observation → core/human | semantic/finding authority only; complete EvidenceBinding and lifecycle observations |
| HumanDecisionRecord | human boundary/core pending card → core/human | human scope/criteria/budget/recovery/closure authority; cards never state authority |

All five use §21 canonical serialization, generated schema, receipt/pre-persist validation,
create-only §30 publication, unknown-field/version rejection and full hash participation. No sixth
surface, global pointer, new adapter/role/module/dependency or external transaction exists.

The following deterministic dispositions are final: missing assertion/unknown kind→MALFORMED;
provenance/grant mismatch→INDEPENDENCE_FAILURE; absent/malformed versions→COMMAND_FAILURE and
unsupported Python→UNSUPPORTED_VERSION; unresolved offline authority→MISSING_EVIDENCE/
HASH_MISMATCH/STALE_RECORD; occupied final/card→§36 recovery; crash before root→replay same candidate;
crash after root→adopt successor; orphan card→non-authoritative; omitted earlier blocker→ledger
unchanged and no PASS; addressed-not-verified→unresolved; duplicate/residual/new finding→§39 identity;
repeated evidence or same blockers→NO_PROGRESS; changed diff without verified finding→NO_PROGRESS;
recovery preserves progress/count; count two with progress→CORRECTION_CEILING.

The complete-lineage ordering, exact hashes, UUID/card IDs, finding identities, progress function and
oracle inputs leave no permitted nondeterministic choice for two conforming implementations with the
same persisted inputs. Semantic evidence relevance remains reviewer judgment with explicit rationale,
not cryptographic proof.

## 42. Historical CORR-011 correction state (superseded by §§43 and 50)

The selected architecture stays inside the existing four new production modules and five surfaces.
The expected allocation remains core 330, model 420, inventory 360 and I/O 550 = 1,660 new production
LOC. Recovery lineage/finding lifecycle/version parsers are refinements of already allocated
state/model/I/O responsibilities; the 140-line margin to the 1,800 hard maximum remains risk reserve,
not scope. No new dependency, module, adapter or surface is planned. Implementation must continuously
self-inventory and stop `BUDGET AUTHORITY REQUIRED` before exceeding 1,800. `EB006-FR-07` is not
reopened.

Only EB-006 and necessary project-memory/index documents changed in CORR-011. No runtime, test,
schema, fixture, dependency, version, Audio Recorder, FAL-002 specification or FAL-001 artifact was
modified.

`CORR-011-01` through `CORR-011-08` and `EB006-IR3-01` through `EB006-IR3-08` are each
`ADDRESSED — AWAITING INDEPENDENT REVIEW`. No finding is independently verified, closed, accepted or
PASS. FAL-002 remains `NOT AUTHORIZED`; FAL-001 remains permanently `TERMINATED BLOCKED` with
correction count 2/2. The only next gate is a fresh independent read-only Standard-Assurance Review.

## 43. Preserved authority and correction traceability

`HD-FAL-012` and `HD-FAL-014` are binding architecture. `HD-FAL-015` authorizes one inseparable
documentation correction containing `CORR-012-01` through `CORR-012-05`. Sections 44–50 are the sole
final normative contracts for every subject they cover. Sections 21 and 34–42 are explicitly
historical or withdrawn, not alternate implementations. Unchanged field structures and parser rules
are final only where sections 44–49 expressly incorporate them.

| Objective | Source | Authority | Final sections | Completion claim |
| --- | --- | --- | --- | --- |
| `CORR-012-01` | `EB006-IR4-01` | `HD-FAL-015` | §§44, 48–49 | one universal canonical/hash contract and reconciled fixtures |
| `CORR-012-02` | `EB006-IR4-02` | `HD-FAL-015` | §48 | total independent constructors, mutations, bytes, hashes and replay expectations |
| `CORR-012-03` | `EB006-IR4-03` | `HD-FAL-012`, `HD-FAL-014`, `HD-FAL-015` | §§45, 48–49 | PUBLICATION_INTENT, semantic recovery, pointer-free discovery and rebinding |
| `CORR-012-04` | `EB006-IR4-04` | `HD-FAL-014`, `HD-FAL-015` | §§46, 48–49 | complete-logical-lineage HumanDecisionRecord/offline resolver |
| `CORR-012-05` | `EB006-IR4-05` | `HD-FAL-015` | §§47–49 | canonical severity/blocking/remediation/current-state derivation |

The table records the original CORR-012 completion claims. It does not itself close a finding,
create PASS, acceptance or Implementation Authorization.

`CORR-012-01` and `CORR-012-03` were independently verified before CORR-013. Their canonical hash
contract (§44) and publication/recovery/discovery contract (§45) are preserved unchanged. The
following inseparable residual correction is authorized by `HD-FAL-012`, `HD-FAL-014` and
`HD-FAL-016`; its rows are remediation claims pending IR6, not verification:

| Objective | Source | Authority | Final sections | Consolidated model and completion evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `CORR-013-01` | `EB006-IR5-01` | `HD-FAL-016` | §§48–49 | total stdlib oracle, closed constructors, VFS mutation DSL and decision/finding/progress cases | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-013-02` | `EB006-IR5-02` | `HD-FAL-012`, `HD-FAL-014`, `HD-FAL-016` | §§44.6, 45.8, 46, 48–49 | separate immutable requirement, pending card, resolution, binding and GateRecord application; one lineage resolver | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-013-03` | `EB006-IR5-03` | `HD-FAL-016` | §§45.8, 47, 48–49 | GateRecord CONTROL deltas, exact FindingEvent/RemediationEvidence and restart checkpoints | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-013-04` | `EB006-IR5-04` | `HD-FAL-016` | §§47–49 | exact severity epochs, blocking latch, lifecycle fold, PASS and no-progress inputs | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |

IR6 independently verified the frozen CJ/CF/H/HB, publication/recovery/discovery and persisted
finding-state contracts. CORR-014 does not reopen them. `HD-FAL-017` authorizes the following one
inseparable residual documentation correction; these rows are remediation claims pending IR7:

| Objective | Source | Authority | Final sections | Consolidated model and completion evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `CORR-014-01` | `EB006-IR6-01` | `HD-FAL-012`, `HD-FAL-014`, `HD-FAL-017` | §§44.6, 46, 48–49 | stable DecisionRequirement-bound ResolutionSemanticInput, separate PresentationEvidence, physically relocatable DecisionResolution, current-lineage DecisionApplication and offline resolution; executable P0/P1 and R0/R1 scenarios | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |
| `CORR-014-02` | `EB006-IR6-02` | `HD-FAL-017` | §§48–49 | explicit test-only OracleLineageState, predecessor-consuming CONTROL and RECOVERY_ROOT, actual-run review binding, executable JSON Pointer/hash/VFS operations and integrated chain/restart scenarios | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |

IR7 independently verified `CORR-014-01`/`EB006-IR6-01`, did not verify
`CORR-014-02`/`EB006-IR6-02`, and created no new finding. `HD-FAL-018` authorizes only the following
final residual oracle correction; it does not reopen the verified semantic-answer model:

| Objective | Source | Authority | Final sections | Consolidated model and completion evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `CORR-015-01` | `EB006-IR6-02` | `HD-FAL-018` | §§48–50 | explicit active-series propagation; executable recovery-N and successor run/review scenarios; topologically complete DecisionRequirement REHASH/NO_REHASH; create-only VFS and total row operations | `ADDRESSED — AWAITING INDEPENDENT REVIEW` |

## 44. Final universal canonical bytes and hash contract

### 44.1 Canonical JSON value domain

`Json` is exactly null, boolean, signed integer, Unicode string, ordered array or object with string
keys. Floats, decimal/exponent forms, NaN, infinity, duplicate keys, BOM, invalid UTF-8 and lone
surrogates are invalid. Integers serialize as optional `-` followed by `0` or a non-zero decimal digit
and remaining decimal digits; `-0` and leading zeroes are invalid. Booleans are literal `true` or
`false`; null is literal `null`.

Strings are not Unicode-normalized. Input containing a code point valid in Unicode is preserved;
ASCII control characters, quote and backslash use JSON lowercase short escapes where defined
(`\b`, `\t`, `\n`, `\f`, `\r`, `\"`, `\\`) and otherwise lowercase four-hex-digit `\u00xx`.
Non-ASCII code points are emitted as their UTF-8 encoding, not `\u` escapes. A type such as
`NonEmpty`, `Timestamp`, `PathRel`, `PathAbs`, `Uuid` or `Sha256` applies its own validation before
serialization. Inputs are rejected, never trimmed or normalized implicitly.

Objects contain exactly the model-declared present fields. Optional absent means the key is omitted;
present null is valid only when the field explicitly permits null. Object keys sort by their UTF-8
byte sequences. Arrays preserve contract order. An array explicitly declared set-valued sorts by its
declared canonical tuple using UTF-8 byte comparison and rejects duplicates; no implementation may
sort an ordinary ordered array.

`Timestamp` is UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`, exactly 27 ASCII bytes, with a real Gregorian date
and six fractional digits. Equivalent offsets or reduced precision are rejected rather than
normalized.

### 44.2 Canonical value bytes and persisted file bytes

For valid value `x`, `CJ(x)` is exactly Python-stdlib-equivalent:

```text
json.dumps(x, ensure_ascii=False, allow_nan=False, sort_keys=True,
           separators=(",", ":"))
```

encoded as strict UTF-8. `CJ(x)` contains no BOM, leading/trailing whitespace or terminal LF.

For every canonical persisted JSON boundary file, `CF(x) = CJ(x) || 0x0a`. Exactly one terminal LF
is present. Empty lines or additional bytes are invalid. Parsing a valid file, validating its model
and recomputing `CF` must reproduce the file byte-for-byte.

This distinction is universal: persisted boundary files use `CF`; structured hash preimages use
`CJ`. No section may include the file LF in a structured hash preimage.

### 44.3 Universal structured and raw-byte hashing

`H(domain, value)` is exactly:

```text
preimage_object = {"domain": domain, "value": value}
preimage_bytes  = CJ(preimage_object)
digest_bytes    = SHA-256(preimage_bytes)
result          = 64 lowercase hexadecimal ASCII characters
```

`domain` is one required non-empty ASCII literal fixed by §44.5 or the defining final contract. No
NUL, implicit separator, prefix, suffix or terminal LF is added. Calling `H` with one argument, raw
bytes, an invented domain or a domain embedded ad hoc inside `value` is invalid.

`HB(bytes)` is lowercase SHA-256 of the exact supplied byte sequence. It is permitted only for raw
file/executable content, command stdout/stderr, Git diff bytes, staged/final file bytes or another
field explicitly declared raw-byte evidence. `HB` has no JSON transformation or LF rule. A JSON
value's semantic content hash always uses `H("fal002-json-content-v1", value)`, never `HB`.

UUIDv5 receives the exact UTF-8 name specified by its final identity contract and the fixed namespace;
it does not receive `CJ`, `CF` or an additional hash unless stated. UUID output is lowercase RFC 4122
hyphenated text.

### 44.4 Surface payload and record hashes

The five final surfaces incorporate the exact structural field definitions in historical §§35.1–
35.6 only where not replaced below. Every persisted surface envelope has `schema_id`,
`schema_version:1`, `record_id`, `series_id`, `created_at`, `payload_hash`, `record_hash` and its
surface fields. Its hashes are exclusively:

```text
payload_hash = H("fal002-payload-v1:" + schema_id, payload_input)
record_hash  = H("fal002-record-v1:" + schema_id,
                 complete_record_with_record_hash_absent)
file_hash    = HB(CF(complete_record))
```

`payload_input` is GateRecord `payload`; ExecutorExchange `{request,result,invocation}`; RunRecord
`{repository,runtime,tools,commands,diff,build}`; ReviewerExchange
`{packet,result,reviewer_execution}`; and HumanDecisionRecord
`{decision_identity,binding_generation,decision_kind,status,owner,provenance,payload}`.

The `record_hash` field is absent—not null—during its preimage. `payload_hash` is present in the
record-hash preimage. `file_hash` is evidence and is never stored inside the same file it hashes.

### 44.5 Exhaustive domain registry

No other structured-hash domain is permitted in version 1.

| Semantic value | Exact `H` domain |
| --- | --- |
| JSON locator content | `fal002-json-content-v1` |
| Gate/Exchange/Run/Review/Decision payload | `fal002-payload-v1:{schema_id}` |
| Gate/Exchange/Run/Review/Decision record | `fal002-record-v1:{schema_id}` |
| allowed-path set | `fal002-allowed-paths-v1` |
| scope object | `fal002-scope-v1` |
| criteria object | `fal002-criteria-v1` |
| command policy | `fal002-command-policy-v1` |
| work packet | `fal002-work-packet-v1` |
| invocation grant | `fal002-invocation-grant-v1` |
| publication slot | `fal002-publication-slot-v1` |
| publication-intent commitment | `fal002-publication-intent-v1` |
| semantic recovery condition | `fal002-recovery-condition-v1` |
| physical recovery discovery | `fal002-recovery-discovery-v1` |
| conflict-card semantic input | `fal002-conflict-card-v1` |
| semantic decision identity | `fal002-decision-identity-v1` |
| decision requirement | `fal002-decision-requirement-v1` |
| active decision binding | `fal002-decision-binding-v1` |
| offline evidence | `fal002-offline-evidence-v1` |
| finding identity | `fal002-finding-key-v1` |
| remediation evidence | `fal002-remediation-evidence-v1` |
| finding observation | `fal002-finding-observation-v1` |
| finding history | `fal002-finding-history-v1` |
| current finding ledger | `fal002-finding-ledger-v1` |
| progress evidence | `fal002-progress-evidence-v1` |
| unresolved finding set | `fal002-unresolved-findings-v1` |

Manifest source documents, executable binaries, source files, schema files, command streams and Git
diff text use `HB(exact_file_or_stream_bytes)`. Their containing structured records use `H` under
the appropriate domain. `EvidenceBinding.content_hash` is
`H("fal002-json-content-v1", resolved_json_value)`. `EvidenceBinding.provenance.record_hash` is the
source surface's §44.4 record hash.

### 44.6 Reconciled identity formulas

Every prior one-argument `H(...)` formula is withdrawn and replaced as follows:

- `grant_id = H("fal002-invocation-grant-v1", {series_id,gate_sequence,role,principal_id,
  adapter_id,input_hash})`;
- `slot_id = H("fal002-publication-slot-v1", PublicationSlot without slot_id)`;
- `intent_commitment_hash = H("fal002-publication-intent-v1", PublicationIntent without
  intent_commitment_hash)`;
- `recovery_condition_hash = H("fal002-recovery-condition-v1", ObstructionDescriptor)`;
- `recovery_discovery_key = H("fal002-recovery-discovery-v1", RecoveryDiscoveryMaterial)`;
- `conflict_hash = H("fal002-conflict-card-v1", ConflictCardIdentityInput)`;
- `decision_identity = "D-" + H("fal002-decision-identity-v1", DecisionSemanticInput)[:32]`;
- `decision_requirement_hash = H("fal002-decision-requirement-v1", DecisionRequirement without
  decision_requirement_hash)`;
- `presentation_evidence_hash = H("fal002-json-content-v1", PresentationEvidence without
  presentation_evidence_hash)`;
- `binding_key = H("fal002-decision-binding-v1", {binding_object_kind:"PENDING_BINDING",
  value:DecisionBinding without binding_key and pending_card_record_hash})`;
- `application_key = H("fal002-decision-binding-v1", {binding_object_kind:
  "RESOLUTION_APPLICATION",value:DecisionApplication without application_key})`;
- `finding_key = H("fal002-finding-key-v1", FindingIdentityInput)` and
  `finding_id="F-"+finding_key[:20]`;
- `remediation_evidence_hash = H("fal002-remediation-evidence-v1", RemediationEvidence without its
  hash)`;
- `finding_history_hash = H("fal002-finding-history-v1", ordered FindingEvent array)`;
- `finding_ledger_hash = H("fal002-finding-ledger-v1", sorted CurrentFindingState array)`;
- `progress_evidence_hash = H("fal002-progress-evidence-v1", §47.8 progress object)`; and
- `unresolved_finding_set_hash = H("fal002-unresolved-findings-v1", §47.8 unresolved array)`.

Schema ID/file content hashes and executable hashes use `HB`. `RunRecord.diff.sha256` is
`HB(UTF8(redacted_text))`. Command stdout/stderr hashes are `HB(redacted_stream_bytes)`. No hash in
the final model includes a boundary file's terminal LF unless the field is explicitly `file_hash` or
another `HB(CF(record))` byte-evidence field.

### 44.7 Validation and schema generation

Validation order is JSON/file grammar → exact keys → schema/version → primitive normalization →
IDs/paths → enums/cardinality/order → locator resolution → payload hash → record hash → cross-field
invariants → predecessor/logical lineage → authority. Unknown fields, domains, schema IDs or versions
are `MALFORMED_BOUNDARY`; content/preimage/hash mismatch is `HASH_MISMATCH`.

The canonical typed model remains the sole schema source. Generated JSON Schemas express structure,
not the SHA-256 calculation; model and independent fixtures verify hashes. Schema output files use
their own pretty generated representation and `HB(file bytes)` when referenced, but boundary records
always use `CF`.

## 45. Final publication-intent and pointer-free recovery contract

### 45.1 Final GateRecord variants and assurance-state retention

The final GateRecord payload union has exactly eleven variants: the ten historical §35.1 variants
plus `PUBLICATION_INTENT`. The exact MANIFEST and CONTROL shapes are replaced by §§46.4 and 47.4;
the exact RECOVERY_ROOT shape is §45.8. Other variants retain the expressly incorporated §35 shape.
`PUBLICATION_INTENT` and `RECOVERY_ROOT` are GateRecord forms under `fal002.gate-record.v1`, never
separate surfaces.

`PUBLICATION_INTENT` appends a GateRecord sequence and changes state authority, but retains the prior
logical assurance/business state in both envelope `state` and payload `retained_state`. Its event is
`PUBLICATION_INTENT_COMMITTED`, actor `core`; correction count and frozen hash are unchanged. It
authorizes no execution, review, PASS, eligibility, decision or closure.

### 45.2 `PublicationSlot`

`PublicationSlot` is exactly:

```text
{slot_id:Sha256,origin_series_id:Uuid,predecessor_series_id:Uuid,
 predecessor_gate_id:GateId,predecessor_gate_hash:Sha256,
 target_surface:"fal002.gate-record.v1"|"fal002.executor-exchange.v1"|
                "fal002.run-record.v1"|"fal002.reviewer-exchange.v1"|
                "fal002.human-decision.v1",
 target_record_id:NonEmpty,target_path:PathRel,
 reconstruction:"RECONSTRUCTABLE"|"COMMITTED"}
```

All fields are required. `target_path` must equal the §14 canonical path derived from target surface,
active series and target record ID. Gate target ID/sequence must be the sole next permitted transition.
Other target IDs must be present in the predecessor gate payload. `slot_id` uses §44.6. The slot is
unique for one predecessor gate; multiple permitted slots are `AUTHORITY_CONFLICT`.

`RECONSTRUCTABLE` is permitted only for a core-created GateRecord or core-created pending card whose
complete future bytes—including timestamp—are deterministic functions of already authoritative
records. Every other output is `COMMITTED`: completed ExecutorExchange, RunRecord, ReviewerExchange,
human-supplied resolution/closure and any value containing new collector, adapter or human facts.
The classification table is closed; unknown output is `COMMITTED`.

### 45.3 `PUBLICATION_INTENT` exact payload

The GateRecord common payload fields are `frozen_hash`, unchanged `correction_count`,
`variant_kind:"PUBLICATION_INTENT"` and exactly:

```text
{publication_intent:{slot:PublicationSlot,retained_state:
 "draft"|"ready"|"executing"|"evidence_ready"|"reviewing"|
 "correction_required"|"blocked"|"awaiting_human"|"accepted",
 intended_record_hash:Sha256,intended_file_hash:Sha256,
 stage_locator:PathRel,stage_attempt:int 0..9999,
 stage_file_hash:Sha256,source_authority:
 "FORGE_CORE"|"COLLECTOR"|"EXECUTOR_ADAPTER"|"REVIEWER_ADAPTER"|"HUMAN_BOUNDARY",
 source_record_id:NonEmpty,source_record_hash:Sha256,
 intent_commitment_hash:Sha256}}
```

The slot reconstruction is `COMMITTED`. `intended_record_hash` is the validated target record's
§44.4 record hash. `intended_file_hash`, `stage_file_hash` and the actual staged bytes hash all equal
`HB(CF(target_record))`. `stage_locator` is exactly
`.forge/fal002/series/{predecessor_series_id}/.staging/{slot_id}/attempt-{stage_attempt:04d}.json.part`.
The smallest absent attempt is used; occupied attempts are preserved. Source record/hash identify the
durable request/gate whose invocation or collection produced the object; HUMAN_BOUNDARY uses the
accepted input object's externally supplied provenance hash. `intent_commitment_hash` uses §44.6.

Before intent publication, I/O validates target model/hashes, writes `CF(target)` create-only to the
stage, flushes/fsyncs, closes, rereads and verifies `stage_file_hash`. The intent gate is then
create-published normally. Only after that gate is durable may I/O attempt the target final path.

For a `RECONSTRUCTABLE` slot no PUBLICATION_INTENT is allowed: the intended record/file hashes are
recomputed from authoritative inputs during replay and obstruction handling. Presence of an intent
for such a slot or absence of one for a COMMITTED target is `FORBIDDEN_TRANSITION`.

### 45.4 Intent replay and failure

- Crash before a complete durable stage: predecessor remains active; preserve partial stage and use
  next attempt; no intent exists.
- Crash after stage but before intent final: predecessor remains active; replay derives the same slot,
  validates exact stage bytes and publishes the identical intent gate.
- Same intent final bytes: idempotently adopt.
- Same intent path/different bytes: preserve obstruction and invoke recovery using the predecessor's
  reconstructable next-gate slot; the staged intended intent bytes supply semantic evidence only.
- Crash after intent but before target final: intent gate is active; replay reads its exact slot/hash
  and publishes the staged target without re-invoking an adapter, collector or human.
- Intent exists but stage is missing/mismatched: `HASH_MISMATCH`, awaiting human; never reconstruct
  non-reconstructable output by actor replay.
- Target final same bytes: adopt and continue. Different/malformed/nonregular/unreadable target:
  invoke recovery below.

### 45.5 Semantic obstruction descriptor

The final `ObstructionDescriptor` is exactly:

```text
{origin_series_id:Uuid,predecessor_series_id:Uuid,
 predecessor_gate_id:GateId,predecessor_gate_hash:Sha256,
 publication_slot:PublicationSlot,intent_gate_id:GateId|absent,
 intent_gate_hash:Sha256|absent,intended_record_hash:Sha256,
 intended_file_hash:Sha256,target_path:PathRel,
 obstruction_kind:"CONFLICTING_FILE"|"MALFORMED_FILE"|
                  "NONREGULAR_PATH"|"UNREADABLE_PATH",
 observed_content_hash:Sha256|absent,
 path_object_kind:"REGULAR"|"SYMLINK"|"DIRECTORY"|"OTHER",
 frozen_hash:Sha256}
```

Intent gate ID/hash are required iff slot reconstruction is COMMITTED. Observed content hash is
`HB(exact observed file bytes)` and required for readable regular content, absent otherwise.
`recovery_condition_hash=H("fal002-recovery-condition-v1", descriptor)`. Recovery ordinal is not
part of semantic condition: candidate collision cannot create a new reason for recovery.

### 45.6 Persisted recovery-discovery material

`RecoveryDiscoveryMaterial` is exactly:

```text
{origin_series_id:Uuid,predecessor_series_id:Uuid,
 predecessor_gate_id:GateId,predecessor_gate_hash:Sha256,
 publication_slot:{slot_id:Sha256,target_surface:SurfaceId,
                   target_record_id:NonEmpty,target_path:PathRel}}
```

Every value is obtained from the validated active predecessor gate and its sole PublicationSlot.
No intended bytes/hash, obstruction observation, stage, clock, process value or directory entry
participates. `recovery_discovery_key=H("fal002-recovery-discovery-v1", material)`.

### 45.7 Candidate UUID and exact lookup

Use namespace UUID `6f1b8e9e-6a37-5e3a-9d9e-50dc93295943` and exact UTF-8 UUIDv5 name:

`fal002-recovery-discovery-v1:{recovery_discovery_key}:{n}`

where `n` is the minimal ASCII decimal representation of non-negative recovery ordinal (zero is
`0`, no leading zeroes). Candidate path is
`.forge/fal002/series/{candidate_uuid}/gate/00000000.json`.

A fresh consumer validates the origin segment, derives its latest gate and sole slot, and first reads
the normal target. Exact target bytes are adopted; absent target means no recovery root is yet
authoritative. Only a stable obstruction triggers candidate lookup. For n=0,1,...:

1. derive the exact UUID/path without directory enumeration;
2. absent candidate stops—no higher ordinal is eligible;
3. a stable malformed, nonregular, unreadable, wrong-type, wrong-origin, wrong-predecessor,
   wrong-slot, wrong-key, wrong-ordinal, hash-invalid or carry-forward-invalid candidate is preserved
   and permits n+1;
4. a valid root is eligible only when every lower path is a preserved stable obstruction; and
5. adopt the first eligible valid root and stop probing higher candidates.

Inability to read/probe due transient I/O retries the same candidate. Exhausted/unwritable series
storage is `AWAITING_HUMAN_EXTERNAL_REPAIR`. Directory presence, staging and `current.json` never
establish authority.

### 45.8 Final `RECOVERY_ROOT`

The final sequence-zero root retains the §36 GateRecord envelope and state/event but its variant is
replaced by exactly:

```text
{recovery_root:{origin_series_id:Uuid,predecessor_series_id:Uuid,
 predecessor_gate_id:GateId,predecessor_gate_hash:Sha256,
 publication_slot:PublicationSlot,
 recovery_discovery_material:RecoveryDiscoveryMaterial,
 recovery_discovery_key:Sha256,obstruction:ObstructionDescriptor,
 recovery_condition_hash:Sha256,successor_series_id:Uuid,recovery_ordinal:int>=0,
 predecessor_sealed:true,retained_state:GateState,
 scope_hash:Sha256,criteria_hash:Sha256,allowed_paths_hash:Sha256,
 command_policy_hash:Sha256,frozen_hash:Sha256,correction_count:int 0..2,
 max_prior_ordinal:int 0..9999,
  finding_checkpoint:FindingCheckpoint,
  pending_decisions:DecisionRequirement[0..65535],
  active_decision_bindings:DecisionBinding[0..65535],
  applied_decisions:DecisionApplication[0..65535],
  no_progress_history:ProgressSnapshot[0..65535],
  intended_decision_record_id:NonEmpty,
 intended_decision_record_hash:Sha256}}
```

Arrays use §46/47 ordering and reject duplicates. Every inherited value must equal the complete
derived predecessor logical lineage. The root's `series_id` equals successor series ID derived by
§45.7. Root publication and validation are the sole authority transition; at that instant the
predecessor is permanently sealed. Before it, predecessor remains authority and cannot progress past
the obstruction. After it, ordinary append to predecessor is `FORBIDDEN_TRANSITION`.

The root state is `awaiting_human`, actor `recovery`, event `RECOVERY_SUCCESSOR`; it cannot create
PASS, eligibility, closure or reset. Decision-record final publication follows root authority and
uses §46. Obstruction of that path repeats §45 using the same semantic decision requirement.

### 45.9 Normative crash/replay matrix

| Boundary | One authoritative result |
| --- | --- |
| before PUBLICATION_INTENT stage | predecessor active; no intent; retry original deterministic step |
| partial intent target stage | predecessor active; preserve partial; next stage attempt |
| stage durable, intent gate absent | predecessor active; replay same slot/stage and publish same intent |
| intent gate durable, target absent | intent gate active; publish exact staged target without actor retry |
| target path obstructed | intent/reconstructable predecessor active but unable; derive same discovery key |
| candidate derived, root absent | predecessor active; replay same candidate ordinal |
| partial root stage | non-authoritative; preserve and use next stage attempt for same candidate |
| root final valid | successor authoritative; predecessor sealed |
| replay matching root | idempotently adopt same successor |
| candidate path obstructed | preserve; next ordinal under same discovery key/semantic condition |
| bound decision path obstructed | active successor recovery; same decision identity, next binding generation |
| recovery caused by decision obstruction | obstruction descriptor retains the decision publication slot; successor carries the unchanged requirement and advances only its physical binding generation |
| crash after root before decision final | successor authoritative awaiting human; publish exact bound decision on replay |
| repeated semantic condition | same discovery key and lowest eligible root; no second semantic successor |

## 46. Final decision identity, continuity and offline resolver

### 46.1 Semantic decision objects

`DecisionSemanticInput` is exactly:

```text
{domain:DecisionDomain,question:NonEmpty,allowed_choices:NonEmpty[2..16],
 original_target:{target_kind:"GATE"|"SERIES_INTENT"|"RECOVERY_ROOT",
                  origin_series_id:Uuid,target_record_id:NonEmpty,
                  target_semantic_hash:Sha256},
 semantic_sources:[{authority:"HUMAN"|"COLLECTOR"|"CANONICAL_MODEL"|
                    "REVIEWER"|"STATE_SERIES"|"REPOSITORY_HISTORY",
                    record_id:NonEmpty,record_hash:Sha256,locator:JsonPointer}]}
```

Choices retain domain order. Sources sort by `(authority,record_id,record_hash,locator)` UTF-8 and
reject duplicates. `decision_identity="D-"+H("fal002-decision-identity-v1", input)[:32]` and is
stable across physical segments, record locations, recovery ordinals and binding generations.

The final `DecisionDomain` vocabulary is exactly `SCOPE`, `CRITERIA`, `BUDGET`,
`AUTHORITY_CONFLICT`, `EXECUTOR_RETRY`, `REVIEWER_RETRY`, `RECOVERY`, `OFFLINE_EXECUTION`,
`FINDING_DISPOSITION` and `FINDING_RECLASSIFICATION`. Their exact ordered choices are respectively
`["AUTHORIZE_NEW_SERIES","DECLINE"]`, `["AUTHORIZE_NEW_SERIES","DECLINE"]`,
`["AUTHORIZE_BUDGET_CHANGE","DECLINE"]`,
`["SELECT_SOURCE_A","SELECT_SOURCE_B","ABANDON_SERIES"]`, `["RETRY","DECLINE"]`,
`["RETRY","DECLINE"]`, `["AUTHORIZE_RECOVERY_RESUME","ABANDON_LINEAGE"]`,
`["AUTHORIZE_OFFLINE","DECLINE"]`, `["CLOSE_VERIFIED","SUPERSEDE","DECLINE"]`, and
`["SET_LOW_NONBLOCKING","SET_LOW_BLOCKING","SET_MEDIUM_NONBLOCKING","SET_MEDIUM_BLOCKING",
"SET_HIGH_NONBLOCKING","SET_HIGH_BLOCKING","SET_CRITICAL_BLOCKING","DECLINE"]`.
`FINDING_RECLASSIFICATION` has the current GateRecord as semantic target and its semantic sources
must name the finding key, occurrence and current
event hash. The applied selected choice must map one-to-one to the HUMAN_RECLASSIFICATION payload;
no choice permits CRITICAL/nonblocking. `FINDING_DISPOSITION` retains §35.5 choices.

`DecisionRequirement` is immutable and exactly:

```text
{decision_identity:NonEmpty,semantic_input:DecisionSemanticInput,
 semantic_payload_hash:Sha256,required_authority:"HUMAN",
 originating_series_id:Uuid,originating_gate_id:GateId,
 originating_gate_hash:Sha256,created_at:Timestamp,
 decision_requirement_hash:Sha256}
```

Semantic payload hash is `H("fal002-json-content-v1", semantic_input)`. Requirement hash uses §44.6.
Pending/applied state is derived from DecisionBinding and DecisionApplication events; it is not a
mutable field of the requirement. A HumanDecisionRecord alone never changes GateRecord state.

### 46.2 Pending-card binding and accepted-resolution application

`DecisionBinding` binds only the immutable pending question and is exactly:

```text
{decision_identity:NonEmpty,decision_requirement_hash:Sha256,
 binding_generation:int 0..9999,binding_series_id:Uuid,
 pending_card_record_id:NonEmpty,pending_card_locator:PathRel,
 pending_card_record_hash:Sha256,previous_binding_key:Sha256|absent,
 obstruction_evidence_hash:Sha256|absent,binding_key:Sha256}
```

Generation zero has both optional fields absent. Generation n>0 is previous+1, requires the previous
binding key and requires obstruction evidence when rebinding follows path obstruction. Pending record
ID is exactly `{decision_identity}-pending-b{binding_generation:04d}` and locator is
`.forge/fal002/series/{binding_series_id}/decisions/{pending_card_record_id}.json`. Binding key is the
§44.6 PENDING_BINDING projection and excludes the pending record hash to avoid a cycle; the enclosing
GateRecord authenticates the complete binding including that hash.

`ResolutionSemanticInput` is exactly:

```text
{decision_identity:NonEmpty,answered_requirement_hash:Sha256,
 answered_semantic_payload_hash:Sha256,selected_choice:NonEmpty,rationale:NonEmpty,
 human_owner:NonEmpty,human_provenance:{source:NonEmpty,locator:NonEmpty,
 content_hash:Sha256},decided_at:Timestamp}
```

`answered_requirement_hash` equals the immutable DecisionRequirement's
`decision_requirement_hash`; `answered_semantic_payload_hash` equals that requirement's
`semantic_payload_hash`. These two stable hashes bind what governance question was answered. No
binding generation, pending-card ID/hash/locator, physical series, recovery ordinal or physical
resolution metadata participates in `ResolutionSemanticInput`.

`resolution_semantic_hash=H("fal002-json-content-v1", ResolutionSemanticInput)`. A physical
DecisionResolution record ID is
`{decision_identity}-resolution-b{binding_generation:04d}` and its locator uses the same decisions
directory rule. Recovered copies retain byte-identical ResolutionSemanticInput and semantic hash;
only binding generation, series, physical ID/locator, envelope timestamp and record hash may differ.

`PresentationEvidence` is separate non-authoritative evidence and is exactly:

```text
{answered_pending_card_record_id:NonEmpty,answered_pending_card_record_hash:Sha256,
 answered_binding_generation:int 0..9999,answered_binding_key:Sha256,
 presented_at:Timestamp,presentation_evidence_hash:Sha256}
```

Its hash is `H("fal002-json-content-v1", PresentationEvidence without
presentation_evidence_hash)`. It identifies the immutable card presentation actually answered. It
must resolve to a valid historical DecisionBinding/PENDING_CARD for the same requirement and must
not postdate `decided_at`. It need not equal the latest physical pending-card binding after recovery.
Presentation evidence does not participate in `resolution_semantic_hash`; a physically relocated
resolution retains it byte-identically.

`DecisionApplication` is the GateRecord-owned state effect and is exactly:

```text
{decision_identity:NonEmpty,decision_requirement_hash:Sha256,
 binding_generation:int 0..9999,binding_key:Sha256,
 pending_card_record_id:NonEmpty,pending_card_record_hash:Sha256,
 resolution_record_id:NonEmpty,resolution_locator:PathRel,
 resolution_record_hash:Sha256,resolution_semantic_hash:Sha256,
 presentation_evidence_hash:Sha256,
 selected_choice:NonEmpty,application_ordinal:int 0..9999,
 previous_application_key:Sha256|absent,application_key:Sha256}
```

Application ordinal zero has no previous key; a later idempotent physical relocation increments it
and requires the prior key while retaining the same resolution semantic hash and selected choice.
Different semantic hashes or choices for one decision identity are `AUTHORITY_CONFLICT`. Same
resolution record bytes are idempotent. An individually valid orphan, stale binding or unapplied
resolution is evidence only.

### 46.3 Final HumanDecisionRecord variants

HumanDecisionRecord retains the §35.5 envelope and requires top-level `decision_identity` and
`binding_generation`. Its exact variants are:

- PENDING_CARD, status PENDING, physical ID/series/locator equal the current DecisionBinding, payload
  `{decision_requirement_hash,binding_key,semantic_input:DecisionSemanticInput}`;
- RESOLUTION, status ACCEPTED or DECLINED, physical ID
  `{decision_identity}-resolution-b{binding_generation:04d}`, payload
  `{resolution_semantic_input:ResolutionSemanticInput,resolution_semantic_hash:Sha256,
    presentation_evidence:PresentationEvidence}`; and
- CLOSURE, status ACCEPTED, with the existing closure payload plus decision identity and generation.

PENDING_CARD and RESOLUTION are separate create-only files. Neither may replace or mutate the other.
A resolution is eligible for application only when its stable requirement/semantic-payload hashes,
selected choice, human owner/provenance, semantic hash and historical PresentationEvidence validate.
Separately, the DecisionApplication's binding key and pending-card fields must equal the latest
active-lineage DecisionBinding. A valid HumanDecisionRecord without a matching DecisionApplication
has no GateRecord state effect.

Pending-card obstruction advances binding generation through §45 recovery with identical semantic
input. Resolution obstruction uses PUBLICATION_INTENT because human response bytes are COMMITTED;
recovery advances binding generation, creates the canonical rebound pending card and stages a
resolution whose ResolutionSemanticInput, PresentationEvidence and semantic hash are byte-identical
to the obstructed response. The new physical resolution ID/locator/envelope and record hash may
differ. Replay adopts the same semantic hash. A different semantic input or selected choice for the
same identity fails `AUTHORITY_CONFLICT`.

### 46.4 Complete logical-lineage lookup

For one semantic decision identity, core performs exactly:

1. start at and validate the origin MANIFEST GateRecord;
2. traverse only valid §45 successor roots and every gate in logical-lineage order;
3. collect DecisionRequirement, DecisionBinding and DecisionApplication objects from the exact
   MANIFEST, CONTROL and RECOVERY_ROOT carriers in §§46.4.1, 47.4 and 45.8;
4. require one immutable requirement and reject changed semantic input/hash as `AUTHORITY_CONFLICT`;
5. require binding generation zero followed by contiguous increments with valid previous keys;
6. select the greatest valid active-lineage binding and read only its pending-card locator;
7. validate that current pending card's CF/schema/hash/ID/series/generation/requirement/binding/
   owner/provenance independently of any previously accepted semantic answer;
8. collect applications by ordinal; require zero then contiguous increments and one stable resolution
   semantic hash/choice;
9. for the latest application, read only its exact resolution locator and validate CF/schema/hash,
   physical ID, decision identity, generation, stable answered requirement/semantic-payload hashes,
   semantic input/hash, human owner/provenance, PresentationEvidence, status and allowed choice;
10. require the application's binding/current pending fields to equal step 6, require its
    presentation-evidence hash to equal the physical resolution, and permit the presentation card
    to be an older valid binding for the same requirement;
11. return ACCEPTED or DECLINED only from that applied resolution; a pending card or unapplied
    resolution returns PENDING;
12. reject absent as `MISSING_EVIDENCE`, malformed as `MALFORMED_BOUNDARY`, mismatched hash as
    `HASH_MISMATCH`, and stale/orphan/forked/conflicting records as `STALE_RECORD` or
    `AUTHORITY_CONFLICT`; and
13. replay identical bindings, resolutions and applications idempotently; never enumerate a decision
    directory, synthesize a default or mint a new semantic identity.

An obstructed pending or resolution path leaves the requirement at its last applied semantic state
and invokes §45. Pending obstruction advances binding generation without invalidating an already
applied answer. Resolution obstruction retains one semantic response and PresentationEvidence while
advancing physical binding/resolution/application ordinals. Same semantic answer replay is
idempotent even when its physical record differs; two semantic hashes/choices for one decision
identity are `AUTHORITY_CONFLICT`. Exactly one applied semantic answer can satisfy a requirement.

### 46.4.1 Exact MANIFEST decision carrier

Final MANIFEST replaces the historical §28.1 object with exactly:

```text
{scope_hash:Sha256,criteria_hash:Sha256,allowed_paths:PathRel[1..65535],
 command_policy_hash:Sha256,executor_principal_id:NonEmpty,
 reviewer_principal_id:NonEmpty,executor_adapter_id:NonEmpty,
 reviewer_adapter_id:NonEmpty,decision_requirements:DecisionRequirement[0..16],
 decision_bindings:DecisionBinding[0..16],
 decision_applications:DecisionApplication[0..16],
 finding_checkpoint:FindingCheckpoint,offline_evidence:OfflineEvidence|absent}
```

Arrays sort by decision identity then generation/ordinal and reject duplicates. Gate zero may contain
the pre-gate offline requirement, binding and accepted application together; otherwise all four
decision/offline fields are empty/absent. Every referenced HumanDecisionRecord must already exist and
validate before MANIFEST publication. This is the only bootstrap exception to normal later CONTROL
application, and MANIFEST authenticates the complete initial state.

### 46.5 Offline authority

Final MANIFEST `offline_evidence` is exactly:

```text
{evidence_id:Sha256,decision_identity:NonEmpty,
 decision_requirement_hash:Sha256,binding_generation:int 0..9999,
 binding_key:Sha256,pending_card_record_id:NonEmpty,
 pending_card_record_hash:Sha256,resolution_record_id:NonEmpty,
 resolution_record_hash:Sha256,resolution_locator:PathRel,
 resolution_semantic_hash:Sha256,presentation_evidence_hash:Sha256,
 locator:"/payload/resolution_semantic_input/selected_choice",
 content_hash:Sha256,collected_at:Timestamp,valid_until:Timestamp,
 command_policy_hash:Sha256}
```

The origin MANIFEST carries the exact initial requirement, pending binding and accepted application.
Before every spawn, core runs §46.4 across the complete current logical lineage. A pending card alone
never authorizes offline execution. The applied record must be an ACCEPTED DecisionResolution of the
OFFLINE_EXECUTION requirement with choice `AUTHORIZE_OFFLINE`.
`content_hash=H("fal002-json-content-v1","AUTHORIZE_OFFLINE")` and
`evidence_id=H("fal002-offline-evidence-v1", offline_evidence without evidence_id)`.

The stable requirement/semantic-payload hashes and semantic resolution hash must agree with the
accepted answer. Independently, the latest binding key/current pending-card hash and applied physical
resolution ID/hash/locator must agree with the active lineage; presentation evidence may reference
an older valid binding. Human owner/provenance and policy hash must agree. `collected_at` equals
resolution created_at and
`collected_at <= spawn_start <= valid_until <= collected_at+24h`. Recovery may rebind the same
decision identity; semantic authority is unchanged, but evidence must resolve through the latest
binding and its explicit applied-resolution reference. Missing → `MISSING_EVIDENCE`;
malformed/nonaccepted/declined → `MALFORMED_BOUNDARY`; mismatch → `HASH_MISMATCH`; expired →
`STALE_RECORD`. Each stops awaiting human before spawn.

## 47. Final finding events, current state, PASS and no-progress

### 47.1 Immutable event versus derived current state

`FindingObservation`, `RemediationEvidence` and human disposition records are immutable events.
They are never overwritten. `CurrentFindingState` is a deterministic derived value rebuilt from all
valid events across the complete logical lineage. It is the sole input to unresolved-blocker checks,
ledger hashes, eligibility, closure and no-progress.

Final severity order is `LOW < MEDIUM < HIGH < CRITICAL`. `CRITICAL` always implies blocking.

### 47.2 Finding identity and occurrences

Finding identity remains property + canonical defect locator + sorted criterion IDs under §44.6.
Wording, severity, blocking and physical series do not affect the key. Locator movement creates a new
key unless an accepted human supersession explicitly links old and replacement keys; automatic
semantic collapsing is forbidden.

Each finding has `occurrence:int>=0`. First NEW observation creates occurrence zero. A NEW or
STILL_PRESENT observation after CLOSED or SUPERSEDED creates occurrence+1 only when it carries
`recurs_after_event_hash` equal to that terminal event; otherwise it is `FORBIDDEN_TRANSITION`.
Recurrence reopens the same finding identity as a new occurrence while retaining every prior event.

### 47.3 Exact `RemediationEvidence`

```text
{finding_id:FindingId,finding_key:Sha256,occurrence:int>=0,
 correction_objective_id:NonEmpty,authorization_decision_id:NonEmpty,
 authorization_decision_hash:Sha256,corrected_artifact_path:PathRel,
 corrected_locator:NonEmpty,corrected_content_hash:Sha256,
 correction_baseline_head:hex40|hex64,correction_result_head:hex40|hex64|absent,
 correction_actor:"CORRECTION_AGENT",claim:"ADDRESSED_AWAITING_REVIEW",
 created_at:Timestamp,source_run_id:RunId,source_run_hash:Sha256,
 remediation_evidence_hash:Sha256}
```

Every field except result head is required; result head is absent before commit and may be supplied
only by a later repository-provenance event that matches the same content hash. Authorization must
name a valid HumanDecision authorizing that objective/finding. Locator must resolve in the corrected
artifact and content hash is `H("fal002-json-content-v1", resolved value)`. Source run is the durable
collector record proving the changed fact. The subsequent CONTROL GateRecord contains and
authenticates the remediation evidence and therefore need not self-reference. Evidence hash uses
§44.6.

OPEN→ADDRESSED_AWAITING_REVIEW occurs only when core validates this object, changed collector facts,
allowed paths and frozen contract. Missing/incomplete/mismatched evidence leaves OPEN and emits
`MISSING_EVIDENCE` or `HASH_MISMATCH`. A correction claim never verifies or closes.

### 47.4 Final persisted event vocabulary and GateRecord carrier

`FindingEvent` has this common envelope:

```text
{event_id:NonEmpty,event_ordinal:int 0..99999999,event_kind:
 "REVIEW_OBSERVATION"|"REMEDIATION_CLAIM"|"HUMAN_RECLASSIFICATION"|
 "HUMAN_DISPOSITION",finding_id:FindingId,finding_key:Sha256,
 occurrence:int>=0,created_at:Timestamp,source_authority:
 "REVIEWER"|"CORRECTION_AGENT"|"HUMAN",source_record_id:NonEmpty,
 source_record_hash:Sha256,previous_event_hash:Sha256|absent,
 payload:FindingEventPayload,event_hash:Sha256}
```

`FindingEventPayload` is exactly one discriminated object:

- REVIEW_OBSERVATION:
  `{observation:"NEW"|"STILL_PRESENT"|"ABSENT_AFTER_CORRECTION",
    observed_severity:"LOW"|"MEDIUM"|"HIGH"|"CRITICAL",observed_blocking:boolean,
    statement:NonEmpty,criterion_ids:CriterionId[1..65535],
    evidence_bindings:EvidenceBinding[1..65535],rationale:NonEmpty,
    recurs_after_event_hash:Sha256|absent}`;
- REMEDIATION_CLAIM: `{remediation:RemediationEvidence}`;
- HUMAN_RECLASSIFICATION:
  `{new_effective_severity:"LOW"|"MEDIUM"|"HIGH"|"CRITICAL",
    new_blocking:boolean,rationale:NonEmpty,decision_application_key:Sha256}`;
- HUMAN_DISPOSITION:
  `{disposition:"CLOSE_VERIFIED"|"SUPERSEDE",replacement_finding_key:Sha256|absent,
    rationale:NonEmpty,decision_application_key:Sha256}`.

Fields not named by the selected payload variant are forbidden. Criterion/evidence arrays use their
declared canonical order. First event for an occurrence has no previous hash; every later event binds
the immediately preceding event for that finding occurrence. `event_id="FE-"+event_hash[:20]` and
`event_hash=H("fal002-finding-observation-v1", complete event without event_id and event_hash)`.
Event ordinal is the zero-based count of all finding events encountered before this event across the
logical lineage. Duplicate ID/hash is idempotent only when byte-identical; reused ID, ordinal or
previous hash with different content is `AUTHORITY_CONFLICT`.

Final CONTROL replaces the historical §28.1 object with exactly:

```text
{ordinal:int 0..9999,correction_count:int 0..2,diff_hash:Sha256,
 evidence_hash:Sha256,finding_ids:FindingId[0..65535],
 progress:"MATERIAL"|"NONE"|"CEILING",
 decision_requirements:DecisionRequirement[0..65535],
 decision_bindings:DecisionBinding[0..65535],
 decision_applications:DecisionApplication[0..65535],
 finding_events:FindingEvent[0..65535],finding_checkpoint:FindingCheckpoint}
```

CONTROL carries only new immutable decision/finding deltas since its predecessor. Review observations
are copied from one already-final ReviewerExchange with that record as source. Remediation uses the
already-final RunRecord as source. Human events use the already-final accepted DecisionResolution and
its applied DecisionApplication key. Thus no event references its enclosing CONTROL hash and no
self-hash cycle exists.

`FindingCheckpoint` is exactly
`{event_count:int>=0,finding_history_hash:Sha256,current_findings:CurrentFindingState[0..65535],
finding_ledger_hash:Sha256}`. MANIFEST contains the zero-event checkpoint whose history hash covers
`[]`. Every CONTROL checkpoint is derived after applying its deltas. Every other ordinary gate
inherits the prior checkpoint implicitly through its predecessor. RECOVERY_ROOT carries the exact
checkpoint fields/current array from its predecessor and adds no event. This delta strategy is the
only permitted persistence strategy; complete-history duplication in each gate is forbidden.

### 47.5 Exact effective-severity and blocking fold

Observed severity is immutable reviewer evidence. Effective severity is the governance value derived
by this exact fold. Each occurrence begins with `severity_epoch=0`, baseline and effective severity
equal the first NEW observation, and `blocking_latch=observed_blocking`. Apply ordered events:

```text
REVIEW_OBSERVATION:
  if observed_severity > effective_severity: effective_severity = observed_severity
  if observed_blocking: blocking_latch = true
  if observed_severity < effective_severity: retain as downgrade proposal only

HUMAN_RECLASSIFICATION:
  require an applied FINDING_RECLASSIFICATION DecisionResolution
  severity_epoch += 1
  epoch_baseline_severity = new_effective_severity
  effective_severity = new_effective_severity
  blocking_latch = new_blocking
  reject new_effective_severity == CRITICAL and new_blocking == false

current_blocking = (effective_severity == CRITICAL) or blocking_latch
```

Thus MEDIUM→reviewer HIGH yields HIGH; HIGH→reviewer MEDIUM remains HIGH; HIGH→human MEDIUM yields
MEDIUM in a new epoch; human MEDIUM→reviewer HIGH yields HIGH; human MEDIUM→reviewer LOW remains
MEDIUM; equal observations retain the value. A reviewer downgrade proposal creates a pending
reclassification requirement but cannot itself lower severity/blocking. A later reviewer true
relatches blocking. Reclassification never verifies, resolves or closes. Invalid actor/application,
epoch discontinuity or CRITICAL+false is `FORBIDDEN_TRANSITION`.

### 47.6 State transition algorithm

`fold_finding_events(events)` first validates increasing global event ordinal, per-occurrence previous
hashes and identity/occurrence rules, then performs exactly:

```text
absent + REVIEW NEW                              -> OPEN
OPEN + REVIEW STILL_PRESENT                      -> OPEN
OPEN + valid REMEDIATION_CLAIM                   -> ADDRESSED_AWAITING_REVIEW
ADDRESSED_AWAITING_REVIEW + REVIEW STILL_PRESENT -> OPEN
ADDRESSED_AWAITING_REVIEW + REVIEW ABSENT_AFTER_CORRECTION
                                                  -> INDEPENDENTLY_VERIFIED
INDEPENDENTLY_VERIFIED + REVIEW NEW/STILL_PRESENT -> OPEN, same occurrence
INDEPENDENTLY_VERIFIED + HUMAN CLOSE_VERIFIED     -> CLOSED
OPEN/ADDRESSED_AWAITING_REVIEW/INDEPENDENTLY_VERIFIED + HUMAN SUPERSEDE
                                                  -> SUPERSEDED
CLOSED/SUPERSEDED + REVIEW NEW/STILL_PRESENT with terminal previous hash
                                                  -> occurrence+1 OPEN
```

At each event apply §47.5 after lifecycle validation, except remediation changes no severity/blocking.
A new occurrence initializes a fresh severity epoch from its NEW observation. A moved locator is a
new finding key and requires human SUPERSEDE to relate it; wording change alone retains the key. An
empty later findings array creates no event. Any other transition, missing history, noncontiguous
ordinal/occurrence, wrong previous hash, invalid source authority or mismatched checkpoint is
`HASH_MISMATCH`/`FORBIDDEN_TRANSITION` and blocks PASS.

### 47.7 `CurrentFindingState`

```text
{finding_id:FindingId,finding_key:Sha256,occurrence:int>=0,
 state:"OPEN"|"ADDRESSED_AWAITING_REVIEW"|"INDEPENDENTLY_VERIFIED"|
       "CLOSED"|"SUPERSEDED",
 severity_epoch:int>=0,epoch_baseline_severity:"LOW"|"MEDIUM"|"HIGH"|"CRITICAL",
 current_severity:"LOW"|"MEDIUM"|"HIGH"|"CRITICAL",
 current_blocking:boolean,latest_statement:NonEmpty,
 criterion_ids:CriterionId[1..65535],last_event_hash:Sha256,
 remediation_evidence_hash:Sha256|absent,
 replacement_finding_key:Sha256|absent}
```

Current array sorts by `(finding_id,occurrence)`. Unresolved is OPEN or
ADDRESSED_AWAITING_REVIEW. `finding_history_hash` hashes the complete ordered event array and
`finding_ledger_hash` hashes the current array under §44.6. Recovery roots must carry byte-identical
checkpoint/current state and hashes derived from the predecessor logical lineage.

PASS/eligibility is forbidden when any unresolved current occurrence has CRITICAL severity or
current_blocking true, when any pending human decision exists, when history is malformed/incomplete,
or when any criterion lacks valid binding/rationale. ADDRESSED_AWAITING_REVIEW is unresolved. A later
empty review cannot erase it. Closure rederives the identical ledger and requires the existing human-
only closure decision; executor, correction agent and reviewer cannot close.

A fresh consumer reconstructs by validating origin, traversing every authoritative gate/successor,
collecting CONTROL finding-event deltas, checking global ordinals and previous hashes, folding through
§§47.5–47.6, recomputing history/ledger hashes at every CONTROL/RECOVERY_ROOT checkpoint and rejecting
any mismatch. Replay of identical gates/events is idempotent. This algorithm is identical before and
after restart and across any recovery depth.

### 47.8 Deterministic no-progress operands

For every completed reviewed run:

```text
progress_evidence_hash = H("fal002-progress-evidence-v1",
 {repository:{baseline_head,final_head,status,changed_paths},
  diff:{sha256,numstat},runtime,tools,
  commands:[{command_id,termination,exit_code,classification,parsed_without_duration}],
  build})

unresolved_finding_set_hash = H("fal002-unresolved-findings-v1",
 [{finding_id,occurrence,state,severity_epoch,epoch_baseline_severity,
    current_severity,current_blocking,last_event_hash,
    remediation_evidence_hash_or_absent} sorted by finding_id,occurrence])
```

Previous/current window remains consecutive completed reviewed runs across the complete logical
lineage. Define:

```text
diff_changed = current.diff_hash != previous.diff_hash
evidence_changed = current.progress_evidence_hash != previous.progress_evidence_hash
resolved_any = any previous unresolved occurrence is now INDEPENDENTLY_VERIFIED/CLOSED/SUPERSEDED
introduced_blocker = any occurrence absent previously is now unresolved blocker
                     or any existing unresolved occurrence changed
                        current_blocking false→true or severity increased to CRITICAL
residual_blocker = any prior unresolved blocker remains OPEN or ADDRESSED_AWAITING_REVIEW
recurrence_blocker = any new occurrence after terminal history is an unresolved blocker
history_valid = complete ordered events and snapshots agree
material_progress = history_valid and (diff_changed or evidence_changed) and resolved_any
                    and not introduced_blocker and not recurrence_blocker
no_progress = not material_progress
```

Severity epoch/baseline change or blocking clear without an applied human reclassification makes
history invalid. A reviewer-only lower observation leaves the fingerprint unchanged except for the
history/last-event hash; a human reclassification changes epoch, baseline and current state.
Remediation evidence change alone never satisfies resolved_any. Residual blocker does not by itself
force no-progress if another finding is independently resolved and evidence changes, but it continues
to prohibit PASS. Malformed history always yields `NO_PROGRESS` plus `HASH_MISMATCH`/blocked.

On CORRECTION_REQUIRED precedence remains: compute history/no-progress; invalid/no-progress → blocked;
else correction_count==2 → awaiting human `CORRECTION_CEILING`; else increment once. Physical
recovery carries snapshots and never resets comparison or count.

## 48. Final independent fixture oracle

### 48.1 Independence and executable algorithm

The sole normative expected-value oracle is a test-only implementation in
`tests/test_fal002_model.py` that imports exactly stdlib `json`, `hashlib`, `uuid`, `copy` and
`pathlib`. It imports no `forge.*`, production schemas, fixture files, production constants,
canonicalization, hashing, validation, recovery or ledger helpers.

The independent functions are exactly:

```python
import copy
import hashlib
import json
import pathlib
import uuid

def cj(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":")).encode("utf-8")

def cf(value):
    return cj(value) + b"\n"

def h(domain, value):
    return hashlib.sha256(cj({"domain": domain, "value": value})).hexdigest()

def hb(value):
    assert isinstance(value, bytes)
    return hashlib.sha256(value).hexdigest()

def surface_hashes(schema_id, payload_input, record_without_hash):
    payload_hash = h("fal002-payload-v1:" + schema_id, payload_input)
    body = copy.deepcopy(record_without_hash)
    body["payload_hash"] = payload_hash
    record_hash = h("fal002-record-v1:" + schema_id, body)
    body["record_hash"] = record_hash
    return body, cf(body), hb(cf(body))
```

Unknown constructor parameter, missing parameter, implicit default, environment read, current clock,
random value or production import is an oracle failure. Dictionary insertion order never determines
semantic order. Expected boundary file bytes are `cf(record)`; structured hashes use `h`; raw-byte
hashes use `hb`. This code is the only fixture byte/hash rule.

### 48.2 Complete primitive catalog

Unless a case row gives an exact replacement, constructors use only:

| Name | Exact value |
| --- | --- |
| origin series | `00000000-0000-4000-8000-000000000002` |
| successor namespace | `6f1b8e9e-6a37-5e3a-9d9e-50dc93295943` |
| `t(n)` | `2026-08-01T00:00:00.` + six-digit n + `Z` |
| baseline/final head | `7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68` |
| branch/root | `main` / `.` |
| scope/allowed path | `forge/fal002.py` |
| criterion | `FAL2-CC-01` |
| owner | `human-product-owner` |
| human provenance | source `CODEx_TASK`, locator `task://fal002-fixture`, content hash `hb(b"human-authority")` |
| executor/reviewer principal | `principal-executor` / `principal-reviewer` |
| executor/reviewer adapter | `forge/fal002_io.py#executor` / `forge/fal002_io.py#reviewer` |
| executor/reviewer context | `ctx-executor-0000` / `ctx-reviewer-0000` |
| Python | `CPython`, `3.14.0`, `C:/python/python.exe`, executable hash `hb(b"python-exe")` |
| Git | `2.50.0`, `C:/Program Files/Git/cmd/git.exe`, hash `hb(b"git-exe")` |
| pytest/ruff | `9.0.0` / `0.12.0`, Python executable and hash |
| frozen/scope/criteria/policy/work packet | `hb(b"F")` / `h("fal002-scope-v1",["forge/fal002.py"])` / `h("fal002-criteria-v1",["FAL2-CC-01"])` / `h("fal002-command-policy-v1",COMMAND_IDS)` / `h("fal002-work-packet-v1",{"kind":"INITIAL","ordinal":0})` |
| assertion | `The resolved schema hash supports the criterion.` |
| rationale | `The resolved schema hash supports exact model and schema consistency.` |
| finding statement | `Required evidence is missing.` |
| remediation claim | `The authorized EB section now defines the missing evidence.` |
| raw stage source | exact `cf(target_record)` |

The names used by the executable constructors are assigned exactly:

```python
ORIGIN="00000000-0000-4000-8000-000000000002"
NAMESPACE="6f1b8e9e-6a37-5e3a-9d9e-50dc93295943"
HEAD="7bdbc9a9afb57dcd3a6f2e878ed1dc582ff8ad68"
FROZEN=hb(b"F")
SCOPE=h("fal002-scope-v1",["forge/fal002.py"])
CRITERIA=h("fal002-criteria-v1",["FAL2-CC-01"])
COMMAND_IDS=["GIT-ROOT","PYTHON-VERSION","GIT-VERSION","PYTEST-VERSION","RUFF-VERSION",
 "GIT-HEAD-BASELINE","GIT-BRANCH","INVENTORY","GIT-HEAD-FINAL","GIT-STATUS",
 "GIT-DIFF","GIT-NUMSTAT","SCHEMA-CHECK","PYTEST","RUFF-LINT","RUFF-FORMAT","FORGE-STATUS"]
POLICY=h("fal002-command-policy-v1",COMMAND_IDS)
ENV=["PATH","PYTHONIOENCODING","PYTHONUTF8","SYSTEMROOT","TEMP","TMP"]
def t(n): return "2026-08-01T00:00:00."+f"{n:06d}"+"Z"
```

`COMMAND_IDS` is the exact §35.1 ordered 17-ID array. This final section expressly incorporates the
exact argv, timeouts, environment/redaction and success parser rules of historical §24 for its 13
non-version commands and historical §35.4 for the four version commands; every old hash convention
in those sections remains withdrawn. Environment keys are exactly sorted
`["PATH","PYTHONIOENCODING","PYTHONUTF8","SYSTEMROOT","TEMP","TMP"]`, cwd is `.`, stdin is closed.

Exact command stdout bytes are the historical §40.3 table and are expressly incorporated as raw
inputs only. Stderr is empty. Command timestamps are `t(500+2*i)` and `t(501+2*i)` for zero-based
command index i. Exit is 0, termination EXITED, classification PASS and parser version 1. Raw hashes
are `hb(stdout_bytes)`/`hb(b"")`. The exact parsed success objects are the final §28.2 union plus
§35.4 version variants; their structure is expressly incorporated while former hashing is withdrawn.

### 48.3 Complete record constructor

The executable oracle uses these closed field sets; a missing or extra field raises
`OracleDefinitionError`:

```python
SURFACE_FIELDS = {
 "fal002.gate-record.v1": {"sequence","predecessor","state","actor","event","payload"},
 "fal002.executor-exchange.v1": {"run_id","ordinal","request","result","invocation"},
 "fal002.run-record.v1": {"execution_id","ordinal","repository","runtime","tools",
                           "commands","diff","build"},
 "fal002.reviewer-exchange.v1": {"run_id","ordinal","packet","result",
                                  "reviewer_execution"},
 "fal002.human-decision.v1": {"decision_identity","binding_generation","decision_kind",
                                "status","owner","provenance","payload"},
}

def make_record(schema_id, record_id, series_id, created_at, fields):
    assert set(fields) == SURFACE_FIELDS[schema_id]
    body = {"schema_id":schema_id,"schema_version":1,"record_id":record_id,
            "series_id":series_id,"created_at":created_at,**copy.deepcopy(fields)}
    if schema_id == "fal002.gate-record.v1": payload_input=body["payload"]
    elif schema_id == "fal002.executor-exchange.v1":
        payload_input={k:body[k] for k in ("request","result","invocation")}
    elif schema_id == "fal002.run-record.v1":
        payload_input={k:body[k] for k in ("repository","runtime","tools","commands","diff","build")}
    elif schema_id == "fal002.reviewer-exchange.v1":
        payload_input={k:body[k] for k in ("packet","result","reviewer_execution")}
    else:
        payload_input={k:body[k] for k in ("decision_identity","binding_generation",
          "decision_kind","status","owner","provenance","payload")}
    return surface_hashes(schema_id,payload_input,body)

def gate(sequence,state,actor,event,variant_kind,variant,predecessor,count,series):
    assert isinstance(series,str) and series
    assert (sequence == 0) == (predecessor is None)
    payload={"frozen_hash":FROZEN,"correction_count":count,
             "variant_kind":variant_kind,variant_kind.lower():copy.deepcopy(variant)}
    return make_record("fal002.gate-record.v1",f"gate-{sequence:08d}",series,t(sequence),
      {"sequence":sequence,"predecessor":predecessor,"state":state,"actor":actor,
       "event":event,"payload":payload})
```

Payload, record and file hashes are derived only by `make_record`. Every constructor below returns the record object,
its exact `CF` bytes and its `HB(CF)` file hash from `make_record`.

### 48.4 Exact base decision and manifest constructors

The bootstrap constructor is executable and has no implicit fields:

```python
def offline_bundle():
    semantic={"domain":"OFFLINE_EXECUTION",
      "question":"May the bounded collector execute offline?",
      "allowed_choices":["AUTHORIZE_OFFLINE","DECLINE"],
      "original_target":{"target_kind":"SERIES_INTENT","origin_series_id":ORIGIN,
        "target_record_id":"gate-00000000","target_semantic_hash":FROZEN},
      "semantic_sources":[]}
    did="D-"+h("fal002-decision-identity-v1",semantic)[:32]
    req={"decision_identity":did,"semantic_input":semantic,
      "semantic_payload_hash":h("fal002-json-content-v1",semantic),
      "required_authority":"HUMAN","originating_series_id":ORIGIN,
      "originating_gate_id":"gate-00000000","originating_gate_hash":"0"*64,
      "created_at":t(397)}
    req["decision_requirement_hash"]=h("fal002-decision-requirement-v1",req)
    pid=did+"-pending-b0000"
    ploc=f".forge/fal002/series/{ORIGIN}/decisions/{pid}.json"
    bp={"decision_identity":did,"decision_requirement_hash":req["decision_requirement_hash"],
      "binding_generation":0,"binding_series_id":ORIGIN,"pending_card_record_id":pid,
      "pending_card_locator":ploc}
    bkey=h("fal002-decision-binding-v1",
      {"binding_object_kind":"PENDING_BINDING","value":bp})
    pending=make_record("fal002.human-decision.v1",pid,ORIGIN,t(398),
      {"decision_identity":did,"binding_generation":0,"decision_kind":"PENDING_CARD",
       "status":"PENDING","owner":"human-product-owner",
       "provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
                     "content_hash":hb(b"human-authority")},
       "payload":{"decision_requirement_hash":req["decision_requirement_hash"],
                  "binding_key":bkey,"semantic_input":semantic}})[0]
    binding={**bp,"pending_card_record_hash":pending["record_hash"],
             "binding_key":bkey}
    rsi={"decision_identity":did,"answered_requirement_hash":req["decision_requirement_hash"],
      "answered_semantic_payload_hash":req["semantic_payload_hash"],
      "selected_choice":"AUTHORIZE_OFFLINE",
      "rationale":"Offline execution is authorized for this fixture.",
      "human_owner":"human-product-owner",
      "human_provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
                          "content_hash":hb(b"human-authority")},"decided_at":t(399)}
    rsh=h("fal002-json-content-v1",rsi)
    pe={"answered_pending_card_record_id":pid,
      "answered_pending_card_record_hash":pending["record_hash"],
      "answered_binding_generation":0,"answered_binding_key":bkey,"presented_at":t(398)}
    pe["presentation_evidence_hash"]=h("fal002-json-content-v1",pe)
    rid=did+"-resolution-b0000"
    rloc=f".forge/fal002/series/{ORIGIN}/decisions/{rid}.json"
    resolution=make_record("fal002.human-decision.v1",rid,ORIGIN,t(399),
      {"decision_identity":did,"binding_generation":0,"decision_kind":"RESOLUTION",
       "status":"ACCEPTED","owner":"human-product-owner",
       "provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
                     "content_hash":hb(b"human-authority")},
       "payload":{"resolution_semantic_input":rsi,"resolution_semantic_hash":rsh,
                  "presentation_evidence":pe}})[0]
    application={"decision_identity":did,"decision_requirement_hash":req["decision_requirement_hash"],
      "binding_generation":0,"binding_key":bkey,"pending_card_record_id":pid,
      "pending_card_record_hash":pending["record_hash"],"resolution_record_id":rid,
      "resolution_locator":rloc,"resolution_record_hash":resolution["record_hash"],
      "resolution_semantic_hash":rsh,
      "presentation_evidence_hash":pe["presentation_evidence_hash"],
      "selected_choice":"AUTHORIZE_OFFLINE",
      "application_ordinal":0}
    application["application_key"]=h("fal002-decision-binding-v1",
      {"binding_object_kind":"RESOLUTION_APPLICATION","value":application})
    evidence={"decision_identity":did,"decision_requirement_hash":req["decision_requirement_hash"],
      "binding_generation":0,"binding_key":bkey,"pending_card_record_id":pid,
      "pending_card_record_hash":pending["record_hash"],"resolution_record_id":rid,
      "resolution_record_hash":resolution["record_hash"],"resolution_locator":rloc,
      "resolution_semantic_hash":rsh,
      "presentation_evidence_hash":pe["presentation_evidence_hash"],
      "locator":"/payload/resolution_semantic_input/selected_choice",
      "content_hash":h("fal002-json-content-v1","AUTHORIZE_OFFLINE"),"collected_at":t(399),
      "valid_until":"2026-08-02T00:00:00.000399Z","command_policy_hash":POLICY}
    evidence["evidence_id"]=h("fal002-offline-evidence-v1",evidence)
    return req,binding,pending,resolution,application,evidence

def gate0():
    req,binding,pending,resolution,application,evidence=offline_bundle()
    empty={"event_count":0,"finding_history_hash":h("fal002-finding-history-v1",[]),
           "current_findings":[],"finding_ledger_hash":h("fal002-finding-ledger-v1",[])}
    manifest={"scope_hash":SCOPE,"criteria_hash":CRITERIA,
      "allowed_paths":["forge/fal002.py"],"command_policy_hash":POLICY,
      "executor_principal_id":"principal-executor","reviewer_principal_id":"principal-reviewer",
      "executor_adapter_id":"forge/fal002_io.py#executor",
      "reviewer_adapter_id":"forge/fal002_io.py#reviewer","decision_requirements":[req],
      "decision_bindings":[binding],"decision_applications":[application],
      "finding_checkpoint":empty,"offline_evidence":evidence}
    return gate(0,"draft","human","INITIALIZE","MANIFEST",manifest,None,0,ORIGIN)

def oracle_lineage_state():
    req,bnd,pending,resolution,application,evidence=offline_bundle()
    origin=gate0()[0]; fs=vfs()
    publish_record(fs,canonical_path("fal002.gate-record.v1",ORIGIN,origin["record_id"]),origin)
    publish_record(fs,bnd["pending_card_locator"],pending)
    publish_record(fs,application["resolution_locator"],resolution)
    return {"origin_series_id":ORIGIN,"active_series_id":ORIGIN,
      "active_gate":origin,"gate_chain":[origin],"vfs":fs,
      "executor_records":[],"run_records":[],"review_records":[],"decision_requirements":[req],
      "decision_bindings":[bnd],"decision_applications":[application],
      "pending_records":[pending],"resolution_records":[resolution],"finding_events":[],
      "remediation_history":[],"finding_checkpoint":origin["payload"]["manifest"]["finding_checkpoint"],
      "max_global_event_ordinal":-1,"max_prior_ordinal":0,"correction_count":0,
      "recovery_depth":0,"publication_slots":[],"offline_evidence":evidence,
      "no_progress_history":[],"frozen_hash":FROZEN,"scope_hash":SCOPE,
      "criteria_hash":CRITERIA,"command_policy_hash":POLICY,
      "allowed_paths_hash":h("fal002-json-content-v1",["forge/fal002.py"])}
```

`OracleLineageState` is the exact dictionary returned by `oracle_lineage_state()`. It is test-only,
in-memory constructor state. It is never persisted, is not authoritative and is not a sixth surface.
Every lineage-dependent constructor below receives and returns this object explicitly; none reads
hidden globals, reconstructs gate zero or assumes ordinal zero.

The all-zero originating gate hash is permitted only inside this pre-gate bootstrap requirement; the
published MANIFEST authenticates the complete requirement, binding and application.

### 48.5 Exact inventory and request constructors

```python
def edge(target,kind,locator):
    value={"source":"forge/fal002.py","target":target,"kind":kind,"locator":locator}
    return {"edge_id":"E-"+h("fal002-json-content-v1",value)[:20],**value}

def inventory_value():
    edges=[edge("forge/__init__.py","PACKAGE_INIT","/package/forge"),
      edge("forge/fal002_inventory.py","IMPORT","/imports/0"),
      edge("forge/fal002_io.py","IMPORT","/imports/1"),
      edge("forge/fal002_model.py","IMPORT","/imports/2")]
    by_target={e["target"]:e["edge_id"] for e in edges}
    files=[]
    specs=[("forge/__init__.py",2,"PACKAGE_INIT",[]),
      ("forge/fal002.py",330,"ENTRYPOINT",[]),
      ("forge/fal002_inventory.py",360,"STATIC_IMPORT",[]),
      ("forge/fal002_io.py",550,"STATIC_IMPORT",["EXECUTOR_ADAPTER","REVIEWER_ADAPTER"]),
      ("forge/fal002_model.py",420,"STATIC_IMPORT",[])]
    for path,loc,reason,roles in specs:
        item={"path":path,"content_hash":hb(b"") if path=="forge/__init__.py" else
          hb(path.encode("utf-8")),"inbound_edges":([] if path=="forge/fal002.py" else
          [by_target[path]]),"reason":reason,"classification":"COUNT","counted_loc":loc,
          "roles":roles}
        if path!="forge/fal002.py": item["parent_edge"]=by_target[path]
        files.append(item)
    return {"entrypoint":"forge/fal002.py","baseline_commit":HEAD,"python_version":"3.14",
      "files":files,"edges":edges,"exemptions":[],
      "counts":{"modules":5,"new_production_loc":1660,"executor_adapters":1,
                "reviewer_adapters":1,"schema_surfaces":5},
      "dependencies":{"stdlib":["ast","dataclasses","hashlib","json","os","pathlib",
          "subprocess","sys","uuid"],"existing_third_party":[],"new_direct":[],
          "new_transitive":[],"manifest_hash":hb(b"pyproject")},
      "unresolved_targets":[],"disposition":"PASS"}

def ready(lineage):
    predecessor=lineage["active_gate"]
    assert lineage["active_series_id"]==predecessor["series_id"]
    inventory=inventory_value()
    return gate(predecessor["sequence"]+1,"ready","core","INVENTORY_COMPLETE","INVENTORY",
      inventory,predecessor["record_hash"],lineage["correction_count"],
      predecessor["series_id"])

def executor_request(kind,count,ordinal):
    assert kind in ("INITIAL","CORRECTION") and 0 <= count <= 2
    return {"frozen_hash":FROZEN,"scope":["forge/fal002.py"],
      "criteria":["FAL2-CC-01"],"allowed_paths":["forge/fal002.py"],
      "command_ids":COMMAND_IDS,"correction_count":count,
      "work_packet_hash":h("fal002-work-packet-v1",{"kind":kind,"ordinal":ordinal}),
      "request_kind":kind}
```

### 48.6 Exact invocation, exchange and run constructors

```python
def ids(series,ordinal):
    o=f"{ordinal:04d}"
    run="run-"+o+"-"+hashlib.sha256(f"{series}:{o}:{FROZEN}".encode()).hexdigest()[:12]
    exe="exec-"+o+"-"+hashlib.sha256((run+":executor").encode()).hexdigest()[:12]
    rev="review-"+o+"-"+hashlib.sha256((run+":reviewer").encode()).hexdigest()[:12]
    return run,exe,rev

def grant(series,role,input_record_id,input_hash,sequence):
    principal="principal-executor" if role=="EXECUTOR" else "principal-reviewer"
    adapter="forge/fal002_io.py#executor" if role=="EXECUTOR" else "forge/fal002_io.py#reviewer"
    value={"series_id":series,"gate_sequence":sequence,"role":role,"principal_id":principal,
           "adapter_id":adapter,"input_hash":input_hash}
    return {"grant_id":h("fal002-invocation-grant-v1",value),"role":role,
      "principal_id":principal,"adapter_id":adapter,
      "context_id":"ctx-executor-0000" if role=="EXECUTOR" else "ctx-reviewer-0000",
      "input_record_id":input_record_id,"input_hash":input_hash,"issued_by":"FORGE_CORE",
      "issued_at":t(90+sequence),"allowed_effect":"RETURN_EXECUTOR_RESULT" if role=="EXECUTOR"
      else "RETURN_REVIEW_RESULT"}

def observed(role,g,input_hash,output_hash):
    ex=((1001,2001,3001,t(600),t(601)) if role=="EXECUTOR" else
        (1002,2002,3002,t(602),t(603)))
    return {"grant_id":g["grant_id"],"resolved_adapter_path":g["adapter_id"],
      "adapter_content_hash":hb(g["adapter_id"].encode()),"process_id":ex[0],"thread_id":ex[1],
      "object_identity":ex[2],"started_at":ex[3],"ended_at":ex[4],"input_hash":input_hash,
      "output_hash":output_hash,"termination":"RETURNED"}

def executor_exchange(lineage,ordinal):
    series=lineage["active_series_id"]; predecessor=lineage["active_gate"]
    assert predecessor["series_id"]==series
    run_id,execution_id,_=ids(series,ordinal)
    kind="INITIAL" if ordinal==0 else "CORRECTION"
    req=executor_request(kind,lineage["correction_count"],ordinal)
    result={"status":"COMPLETED","changed_paths":["forge/fal002.py"],
            "summary":"Bounded work completed."}
    ih=h("fal002-json-content-v1",req); oh=h("fal002-json-content-v1",result)
    g=grant(series,"EXECUTOR",execution_id,ih,predecessor["sequence"]+1)
    return make_record("fal002.executor-exchange.v1",execution_id,series,t(100+ordinal),
      {"run_id":run_id,"ordinal":ordinal,"request":req,"result":result,
       "invocation":{"grant":g,"observed":observed("EXECUTOR",g,ih,oh)}})

SCHEMAS=["fal002.executor-exchange.v1","fal002.gate-record.v1",
 "fal002.human-decision.v1","fal002.reviewer-exchange.v1","fal002.run-record.v1"]
PY="C:/python/python.exe"; GIT="C:/Program Files/Git/cmd/git.exe"
ARGV={
 "GIT-ROOT":[GIT,"rev-parse","--show-toplevel"],
 "PYTHON-VERSION":[PY,"--version"],"GIT-VERSION":[GIT,"--version"],
 "PYTEST-VERSION":[PY,"-m","pytest","--version"],
 "RUFF-VERSION":[PY,"-m","ruff","--version"],
 "GIT-HEAD-BASELINE":[GIT,"rev-parse","HEAD"],
 "GIT-BRANCH":[GIT,"branch","--show-current"],
 "INVENTORY":[PY,"-m","forge.fal002","inventory","--manifest",
   ".forge/fal002/series/"+ORIGIN+"/gate/00000000.json","--output","-"],
 "GIT-HEAD-FINAL":[GIT,"rev-parse","HEAD"],
 "GIT-STATUS":[GIT,"status","--porcelain=v1","-z","--untracked-files=all"],
 "GIT-DIFF":[GIT,"diff","--no-ext-diff","--binary",HEAD,"--"],
 "GIT-NUMSTAT":[GIT,"diff","--no-ext-diff","--numstat","-z",HEAD,"--"],
 "SCHEMA-CHECK":[PY,"-m","forge.fal002","schemas","--output-root","schemas/fal002","--check"],
 "PYTEST":[PY,"-m","pytest","-q"],"RUFF-LINT":[PY,"-m","ruff","check","."],
 "RUFF-FORMAT":[PY,"-m","ruff","format","--check","."],
 "FORGE-STATUS":[PY,"-m","forge","status"]}
PHASE={**{x:"preflight" for x in COMMAND_IDS[:5]},
 "GIT-HEAD-BASELINE":"pre-execution","GIT-BRANCH":"pre-execution","INVENTORY":"pre-execution",
 "GIT-HEAD-FINAL":"post-executor","GIT-STATUS":"post-executor","GIT-DIFF":"post-executor",
 "GIT-NUMSTAT":"post-executor",**{x:"verification" for x in COMMAND_IDS[12:]}}
TIMEOUT={x:(900 if x=="PYTEST" else 300 if x.startswith("RUFF") else
  120 if x in ("INVENTORY","SCHEMA-CHECK","FORGE-STATUS") else 30) for x in COMMAND_IDS}

def command(i,inventory):
    cid=COMMAND_IDS[i]
    schemas=[{"schema_id":s,"sha256":hb(s.encode())} for s in SCHEMAS]
    stdout={"GIT-ROOT":b"C:/repo/forge-ai-sef\n","PYTHON-VERSION":b"Python 3.14.0\n",
      "GIT-VERSION":b"git version 2.50.0\n","PYTEST-VERSION":b"pytest 9.0.0\n",
      "RUFF-VERSION":b"ruff 0.12.0\n","GIT-HEAD-BASELINE":(HEAD+"\n").encode(),
      "GIT-BRANCH":b"main\n","INVENTORY":cf(inventory),
      "GIT-HEAD-FINAL":(HEAD+"\n").encode(),"GIT-STATUS":b"","GIT-DIFF":b"",
      "GIT-NUMSTAT":b"","SCHEMA-CHECK":cf(schemas),"PYTEST":b"1 passed in 0.01s\n",
      "RUFF-LINT":b"All checks passed!\n","RUFF-FORMAT":b"12 files already formatted\n",
      "FORGE-STATUS":b"Project Memory Health: OK\n  fixture\nVersion Consistency Status: WARNING\n  fixture\n"}[cid]
    parsed={"GIT-ROOT":{"available":True,"root":"."},
      "PYTHON-VERSION":{"available":True,"implementation":"CPython","version":"3.14.0"},
      "GIT-VERSION":{"available":True,"version":"2.50.0"},
      "PYTEST-VERSION":{"available":True,"version":"9.0.0"},
      "RUFF-VERSION":{"available":True,"version":"0.12.0"},
      "GIT-HEAD-BASELINE":{"available":True,"head":HEAD,"kind":"BASELINE"},
      "GIT-BRANCH":{"available":True,"branch":"main"},
      "INVENTORY":{"available":True,"inventory_hash":h("fal002-json-content-v1",inventory),
        "disposition":"PASS","counts":inventory["counts"]},
      "GIT-HEAD-FINAL":{"available":True,"head":HEAD,"kind":"FINAL"},
      "GIT-STATUS":{"available":True,"entries":[],"changed_paths":[]},
      "GIT-DIFF":{"available":True,"redacted_content_hash":hb(b""),"byte_count":0},
      "GIT-NUMSTAT":{"available":True,"entries":[]},
      "SCHEMA-CHECK":{"available":True,"schemas":schemas},
      "PYTEST":{"available":True,"passed":1,"failed":0,"skipped":0,"xfailed":0,
        "xpassed":0,"errors":0,"warnings":0,"duration_seconds_decimal":"0.01"},
      "RUFF-LINT":{"available":True,"status":"PASS"},
      "RUFF-FORMAT":{"available":True,"status":"PASS"},
      "FORGE-STATUS":{"available":True,"categories":[
        {"name":"Project Memory Health","status":"OK","evidence_lines":["fixture"]},
        {"name":"Version Consistency Status","status":"WARNING","evidence_lines":["fixture"]}]}}[cid]
    return {"command_id":cid,"phase":PHASE[cid],"argv":ARGV[cid],"cwd":".",
      "environment_keys":ENV,"started_at":t(500+2*i),"ended_at":t(501+2*i),"exit_code":0,
      "termination":"EXITED","stdout_sha256":hb(stdout),"stderr_sha256":hb(b""),
      "stdout_text":stdout.decode(),"stderr_text":"","redaction_count":0,"parser_version":1,
      "parsed":parsed,"classification":"PASS"}

def run(lineage,executor_record,ordinal):
    series=lineage["active_series_id"]; predecessor=lineage["active_gate"]
    assert predecessor["series_id"]==series==executor_record["series_id"]
    run_id,execution_id,_=ids(series,ordinal); inv=inventory_value()
    assert executor_record["record_id"]==execution_id and executor_record["run_id"]==run_id
    evidence=lineage["offline_evidence"]
    resolutions=[r for r in lineage["resolution_records"]
      if r["record_hash"]==evidence["resolution_record_hash"]]
    assert len(resolutions)==1; resolution=resolutions[0]
    runtime={"python_implementation":"CPython","python_version":"3.14.0",
      "python_executable":PY,"python_executable_sha256":hb(b"python-exe")}
    tools=[{"name":"git","version":"2.50.0","executable":GIT,
       "executable_sha256":hb(b"git-exe"),"version_command_id":"GIT-VERSION"},
      {"name":"pytest","version":"9.0.0","executable":PY,
       "executable_sha256":hb(b"python-exe"),"version_command_id":"PYTEST-VERSION"},
      {"name":"python","version":"3.14.0","executable":PY,
       "executable_sha256":hb(b"python-exe"),"version_command_id":"PYTHON-VERSION"},
      {"name":"ruff","version":"0.12.0","executable":PY,
       "executable_sha256":hb(b"python-exe"),"version_command_id":"RUFF-VERSION"}]
    return make_record("fal002.run-record.v1",run_id,series,t(200+ordinal),
      {"execution_id":execution_id,"ordinal":ordinal,
       "repository":{"root":".","branch":"main","baseline_head":HEAD,"final_head":HEAD,
         "status":[],"changed_paths":[],"offline_evidence_id":evidence["evidence_id"],
         "offline_evidence_record_hash":resolution["record_hash"]},
       "runtime":runtime,"tools":tools,"commands":[command(i,inv) for i in range(17)],
       "diff":{"redacted_text":"","sha256":hb(b""),"numstat":[]},
       "build":{"status":"not_available","reason":"packaging_forbidden"}})

def execution_gate(lineage,executor_record,ordinal=0):
    predecessor=lineage["active_gate"]; series=lineage["active_series_id"]
    run_id,execution_id,_=ids(series,ordinal)
    request=executor_record["request"]
    request_hash=h("fal002-json-content-v1",request)
    value={"execution_id":execution_id,"run_id":run_id,"ordinal":ordinal,
      "request_kind":request["request_kind"],"request":request,"request_hash":request_hash,
      "invocation_grant":grant(series,"EXECUTOR",predecessor["record_id"],request_hash,
        predecessor["sequence"]+1)}
    return gate(predecessor["sequence"]+1,"executing","core","START_EXECUTION",
      "EXECUTION",value,predecessor["record_hash"],lineage["correction_count"],series)

def evidence_gate(lineage,rr):
    predecessor=lineage["active_gate"]; series=lineage["active_series_id"]
    assert rr["series_id"]==series
    value={"run_id":rr["record_id"],"run_record_hash":rr["record_hash"],
      "execution_id":rr["execution_id"],"command_ids":COMMAND_IDS,
      "evidence_hash":h("fal002-json-content-v1",
        {"run_record_id":rr["record_id"],"run_record_hash":rr["record_hash"]})}
    return gate(predecessor["sequence"]+1,"evidence_ready","collector","COLLECT_COMPLETE",
      "EVIDENCE",value,predecessor["record_hash"],lineage["correction_count"],series)

def review_gate(lineage,rr):
    predecessor=lineage["active_gate"]; series=lineage["active_series_id"]
    assert rr["series_id"]==series
    packet={"frozen_hash":FROZEN,"run_record_id":rr["record_id"],
      "run_record_hash":rr["record_hash"],"criterion_ids":["FAL2-CC-01"],
      "evidence_index":[binding(rr)],"instructions_hash":hb(b"adversarial-review-v1")}
    _,_,review_id=ids(series,rr["ordinal"]); packet_hash=h("fal002-json-content-v1",packet)
    value={"review_id":review_id,"run_id":rr["record_id"],"ordinal":rr["ordinal"],
      "packet":packet,"packet_hash":packet_hash,
      "invocation_grant":grant(series,"REVIEWER",rr["record_id"],packet_hash,
        predecessor["sequence"]+1)}
    return gate(predecessor["sequence"]+1,"reviewing","core","START_REVIEW",
      "REVIEW",value,predecessor["record_hash"],lineage["correction_count"],series)

def checkpoint_gate(lineage):
    predecessor=lineage["active_gate"]; series=lineage["active_series_id"]
    value={"reason_code":"INTERRUPTED","source_record_ids":[predecessor["record_id"]],
      "source_hashes":[predecessor["record_hash"]],"interruption_id":"interrupt-0000",
      "resume_state":"ready"}
    return gate(predecessor["sequence"]+1,"awaiting_human","recovery","CHECKPOINT_CREATED",
      "CHECKPOINT",value,predecessor["record_hash"],lineage["correction_count"],series)

def eligibility_gate(lineage,rv):
    predecessor=lineage["active_gate"]; series=lineage["active_series_id"]
    assert rv["series_id"]==series and rv["result"]["outcome"]=="PASS"
    value={"review_id":rv["record_id"],"review_hash":rv["record_hash"],
      "criterion_ids":["FAL2-CC-01"],"finding_ids":[],"eligible":True}
    return gate(predecessor["sequence"]+1,"accepted","core","REVIEW_PASS",
      "ELIGIBILITY",value,predecessor["record_hash"],lineage["correction_count"],series)

def closure_bundle(lineage,eligible,rv):
    series=lineage["active_series_id"]; did="D-"+hb(b"fixture-closure")[:32]
    assert eligible["series_id"]==series==rv["series_id"]
    decision=make_record("fal002.human-decision.v1",did+"-closure-b0000",series,t(900),
      {"decision_identity":did,"binding_generation":0,"decision_kind":"CLOSURE",
       "status":"ACCEPTED","owner":"human-product-owner",
       "provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
        "content_hash":hb(b"human-authority")},
       "payload":{"eligible_gate_id":eligible["record_id"],
        "eligible_gate_hash":eligible["record_hash"],"review_id":rv["record_id"],
        "review_hash":rv["record_hash"],
        "finding_ledger_hash":h("fal002-finding-ledger-v1",[])}})[0]
    value={"decision_id":decision["record_id"],"decision_hash":decision["record_hash"],
      "eligible_gate_id":eligible["record_id"],"eligible_gate_hash":eligible["record_hash"]}
    closed=gate(eligible["sequence"]+1,"accepted","human","HUMAN_CLOSURE",
      "CLOSURE",value,eligible["record_hash"],lineage["correction_count"],series)
    return decision,closed
```

### 48.7 Exact evidence, review and finding constructors

The following code is the complete constructor and fold library. It has no delegated shape or caller-
selected value; test cases may alter its results only through §48.9.

```python
def binding(rr):
    value=rr["commands"][12]["parsed"]["schemas"][0]["sha256"]
    return {"criterion_id":"FAL2-CC-01","evidence_kind":"SCHEMA",
      "source_surface":"fal002.run-record.v1","source_record_id":rr["record_id"],
      "locator":"/commands/12/parsed/schemas/0/sha256",
      "assertion":"The resolved schema hash supports the criterion.",
      "content_hash":h("fal002-json-content-v1",value),
      "provenance":{"authority":"COLLECTOR","record_id":rr["record_id"],
        "record_hash":rr["record_hash"],"collector_id":"SCHEMA-CHECK"}}

def finding_observation(severity="HIGH",blocking=True,observation="NEW"):
    identity={"assurance_property":"EVIDENCE","defect_locator":"docs/x.md#one",
              "criterion_ids":["FAL2-CC-01"]}
    key=h("fal002-finding-key-v1",identity)
    return {"finding_id":"F-"+key[:20],"finding_key":key,
      "assurance_property":"EVIDENCE","defect_locator":"docs/x.md#one",
      "severity":severity,"blocking":blocking,"criterion_ids":["FAL2-CC-01"],
      "statement":"Required evidence is missing.","observation":observation}

def review(lineage,run_record,outcome="CORRECTION_REQUIRED",observations=None):
    observations=[finding_observation()] if observations is None else observations
    series=lineage["active_series_id"]; rr=run_record; ordinal=rr["ordinal"]
    assert rr["series_id"]==series==lineage["active_gate"]["series_id"]
    run_id,_,review_id=ids(series,ordinal); eb=binding(rr)
    packet={"frozen_hash":FROZEN,"run_record_id":rr["record_id"],
      "run_record_hash":rr["record_hash"],"criterion_ids":["FAL2-CC-01"],
      "evidence_index":[eb],"instructions_hash":hb(b"adversarial-review-v1")}
    result={"outcome":outcome,"findings":sorted(observations,
      key=lambda x:(x["finding_id"],x["observation"])),"criterion_evidence":[eb],
      "semantic_rationale":[{"criterion_id":"FAL2-CC-01",
        "rationale":"The resolved schema hash supports exact model and schema consistency."}]}
    ih=h("fal002-json-content-v1",packet); oh=h("fal002-json-content-v1",result)
    g=grant(series,"REVIEWER",rr["record_id"],ih,lineage["active_gate"]["sequence"]+1)
    execution={"grant":g,"observed":observed("REVIEWER",g,ih,oh),
      "fresh_context_verified":True,"read_only_packet_verified":True,
      "separation_checks":["MANIFEST_ROLE_DISTINCT","PRINCIPAL_DISTINCT",
       "ADAPTER_ENTRYPOINT_DISTINCT","GRANT_MATCH","CONTEXT_FRESH","PACKET_MINIMAL",
       "NO_WRITE_CALLBACK"]}
    return make_record("fal002.reviewer-exchange.v1",review_id,series,t(300+ordinal),
      {"run_id":run_id,"ordinal":ordinal,"packet":packet,"result":result,
       "reviewer_execution":execution})

def carry_surface(lineage,record):
    series=lineage["active_series_id"]
    assert record["series_id"]==series
    key={"fal002.executor-exchange.v1":"executor_records",
      "fal002.run-record.v1":"run_records",
      "fal002.reviewer-exchange.v1":"review_records"}.get(record["schema_id"])
    if key is None: raise OracleDefinitionError("NOT_A_CARRIED_EXCHANGE")
    updated=copy.deepcopy(lineage); updated.setdefault(key,[]).append(copy.deepcopy(record))
    publish_record(updated["vfs"],canonical_path(record["schema_id"],series,
      record["record_id"]),record)
    return updated

def review_event(review_record,run_record,observation,event_ordinal,previous=None,
                 occurrence=0,recurs_after=None):
    assert review_record["run_id"]==run_record["record_id"]
    assert review_record["packet"]["run_record_id"]==run_record["record_id"]
    assert review_record["packet"]["run_record_hash"]==run_record["record_hash"]
    assert review_record["series_id"]==run_record["series_id"]
    bindings=copy.deepcopy(review_record["result"]["criterion_evidence"])
    assert all(x["source_record_id"]==run_record["record_id"] for x in bindings)
    payload={"observation":observation["observation"],
      "observed_severity":observation["severity"],
      "observed_blocking":observation["blocking"],"statement":observation["statement"],
      "criterion_ids":observation["criterion_ids"],"evidence_bindings":bindings,
      "rationale":"The resolved schema hash supports exact model and schema consistency."}
    if recurs_after is not None: payload["recurs_after_event_hash"]=recurs_after
    event={"event_ordinal":event_ordinal,"event_kind":"REVIEW_OBSERVATION",
      "finding_id":observation["finding_id"],"finding_key":observation["finding_key"],
      "occurrence":occurrence,"created_at":t(650+event_ordinal),
      "source_authority":"REVIEWER","source_record_id":review_record["record_id"],
      "source_record_hash":review_record["record_hash"],"payload":payload}
    if previous is not None: event["previous_event_hash"]=previous["event_hash"]
    eh=h("fal002-finding-observation-v1",event)
    return {"event_id":"FE-"+eh[:20],**event,"event_hash":eh}

def remediation(finding,rr):
    value={"finding_id":finding["finding_id"],"finding_key":finding["finding_key"],
      "occurrence":0,"correction_objective_id":"CORR-013-03",
      "authorization_decision_id":"HD-FAL-016",
      "authorization_decision_hash":hb(b"hd-fal-016"),
      "corrected_artifact_path":"docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md",
      "corrected_locator":"#47-final-finding-events-current-state-pass-and-no-progress",
      "corrected_content_hash":h("fal002-json-content-v1","final finding model"),
      "correction_baseline_head":HEAD,"correction_actor":"CORRECTION_AGENT",
      "claim":"ADDRESSED_AWAITING_REVIEW","created_at":t(700),
      "source_run_id":rr["record_id"],"source_run_hash":rr["record_hash"]}
    return {**value,"remediation_evidence_hash":h("fal002-remediation-evidence-v1",value)}

def remediation_event(finding,previous,run_record,event_ordinal=1):
    rem=remediation(finding,run_record)
    value={"event_ordinal":event_ordinal,"event_kind":"REMEDIATION_CLAIM",
      "finding_id":finding["finding_id"],"finding_key":finding["finding_key"],
      "occurrence":0,"created_at":t(650+event_ordinal),
      "source_authority":"CORRECTION_AGENT","source_record_id":rem["source_run_id"],
      "source_record_hash":rem["source_run_hash"],
      "previous_event_hash":previous["event_hash"],"payload":{"remediation":rem}}
    eh=h("fal002-finding-observation-v1",value)
    return {"event_id":"FE-"+eh[:20],**value,"event_hash":eh}

def human_event(kind,finding,previous,requirement,resolution,application,event_ordinal,payload):
    assert kind in ("HUMAN_RECLASSIFICATION","HUMAN_DISPOSITION")
    assert requirement["semantic_input"]["domain"]==(
      "FINDING_RECLASSIFICATION" if kind=="HUMAN_RECLASSIFICATION" else "FINDING_DISPOSITION")
    assert resolution["decision_kind"]=="RESOLUTION" and resolution["status"]=="ACCEPTED"
    assert application["resolution_record_hash"]==resolution["record_hash"]
    value={"event_ordinal":event_ordinal,"event_kind":kind,
      "finding_id":finding["finding_id"],"finding_key":finding["finding_key"],
      "occurrence":0,"created_at":t(650+event_ordinal),"source_authority":"HUMAN",
      "source_record_id":resolution["record_id"],"source_record_hash":resolution["record_hash"],
      "previous_event_hash":previous["event_hash"],"payload":copy.deepcopy(payload)}
    assert payload["decision_application_key"]==application["application_key"]
    choice=resolution["payload"]["resolution_semantic_input"]["selected_choice"]
    if kind=="HUMAN_RECLASSIFICATION":
        expected="SET_"+payload["new_effective_severity"]+("_BLOCKING" if payload["new_blocking"]
          else "_NONBLOCKING")
        assert choice==expected
    else: assert choice==payload["disposition"]
    eh=h("fal002-finding-observation-v1",value)
    return {"event_id":"FE-"+eh[:20],**value,"event_hash":eh}

SEVERITY={"LOW":0,"MEDIUM":1,"HIGH":2,"CRITICAL":3}
UNRESOLVED={"OPEN","ADDRESSED_AWAITING_REVIEW"}

def fold_finding_events(events):
    states={}; last={}
    for i,e in enumerate(events):
        assert e["event_ordinal"]==i
        key=(e["finding_key"],e["occurrence"])
        assert (key not in last and "previous_event_hash" not in e) or \
               (key in last and e["previous_event_hash"]==last[key])
        state=states.get(key)
        if e["event_kind"]=="REVIEW_OBSERVATION":
            p=e["payload"]
            if state is None:
                if e["occurrence"]==0:
                    assert p["observation"]=="NEW" and "recurs_after_event_hash" not in p
                else:
                    prior=states[(e["finding_key"],e["occurrence"]-1)]
                    assert prior["state"] in ("CLOSED","SUPERSEDED")
                    assert p["observation"] in ("NEW","STILL_PRESENT")
                    assert p["recurs_after_event_hash"]==prior["last_event_hash"]
                state={"finding_id":e["finding_id"],"finding_key":e["finding_key"],
                  "occurrence":e["occurrence"],"state":"OPEN","severity_epoch":0,
                  "epoch_baseline_severity":p["observed_severity"],
                  "current_severity":p["observed_severity"],
                  "current_blocking":p["observed_blocking"] or
                    p["observed_severity"]=="CRITICAL","latest_statement":p["statement"],
                  "criterion_ids":p["criterion_ids"],"last_event_hash":e["event_hash"]}
            else:
                if SEVERITY[p["observed_severity"]]>SEVERITY[state["current_severity"]]:
                    state["current_severity"]=p["observed_severity"]
                state["current_blocking"]=(state["current_blocking"] or
                  p["observed_blocking"] or state["current_severity"]=="CRITICAL")
                if p["observation"]=="STILL_PRESENT": state["state"]="OPEN"
                if p["observation"]=="ABSENT_AFTER_CORRECTION":
                    assert state["state"]=="ADDRESSED_AWAITING_REVIEW"
                    state["state"]="INDEPENDENTLY_VERIFIED"
                state["latest_statement"]=p["statement"]
                state["last_event_hash"]=e["event_hash"]
        elif e["event_kind"]=="REMEDIATION_CLAIM":
            assert state["state"]=="OPEN"
            state["state"]="ADDRESSED_AWAITING_REVIEW"
            state["remediation_evidence_hash"]=e["payload"]["remediation"]["remediation_evidence_hash"]
            state["last_event_hash"]=e["event_hash"]
        elif e["event_kind"]=="HUMAN_RECLASSIFICATION":
            p=e["payload"]; assert not (p["new_effective_severity"]=="CRITICAL" and not p["new_blocking"])
            state["severity_epoch"]+=1
            state["epoch_baseline_severity"]=p["new_effective_severity"]
            state["current_severity"]=p["new_effective_severity"]
            state["current_blocking"]=p["new_blocking"] or p["new_effective_severity"]=="CRITICAL"
            state["last_event_hash"]=e["event_hash"]
        else:
            p=e["payload"]
            if p["disposition"]=="CLOSE_VERIFIED":
                assert state["state"]=="INDEPENDENTLY_VERIFIED"; state["state"]="CLOSED"
            else:
                state["state"]="SUPERSEDED"; state["replacement_finding_key"]=p["replacement_finding_key"]
            state["last_event_hash"]=e["event_hash"]
        states[key]=state; last[key]=e["event_hash"]
    return [states[k] for k in sorted(states,key=lambda x:(states[x]["finding_id"],x[1]))]

def checkpoint(events):
    current=fold_finding_events(events)
    return {"event_count":len(events),
      "finding_history_hash":h("fal002-finding-history-v1",events),
      "current_findings":current,
      "finding_ledger_hash":h("fal002-finding-ledger-v1",current)}

def control(lineage,events,count=None,progress="NONE",decision_requirements=None,
            decision_bindings=None,decision_applications=None):
    prior=copy.deepcopy(lineage); delta=copy.deepcopy(events)
    dr=[] if decision_requirements is None else copy.deepcopy(decision_requirements)
    db=[] if decision_bindings is None else copy.deepcopy(decision_bindings)
    da=[] if decision_applications is None else copy.deepcopy(decision_applications)
    start=len(prior["finding_events"])
    assert all(e["event_ordinal"]==start+i for i,e in enumerate(delta))
    history=prior["finding_events"]+delta; cp=checkpoint(history)
    actual_count=prior["correction_count"] if count is None else count
    assert prior["correction_count"] <= actual_count <= 2
    predecessor=prior["active_gate"]
    variant={"ordinal":predecessor["sequence"]+1,"correction_count":actual_count,
      "diff_hash":hb(b""),
      "evidence_hash":h("fal002-progress-evidence-v1",
        {"event_count":len(history),"finding_ledger_hash":cp["finding_ledger_hash"]}),
      "finding_ids":sorted({e["finding_id"] for e in delta}),"progress":progress,
      "decision_requirements":dr,"decision_bindings":db,"decision_applications":da,
      "finding_events":delta,"finding_checkpoint":cp}
    record=gate(predecessor["sequence"]+1,"correction_required","core","CONTROL_UPDATED",
      "CONTROL",variant,predecessor["record_hash"],actual_count,
      predecessor["series_id"])[0]
    updated=copy.deepcopy(prior); updated["active_gate"]=record
    updated["gate_chain"].append(record); updated["finding_events"]=history
    updated["finding_checkpoint"]=cp; updated["max_global_event_ordinal"]=len(history)-1
    updated["max_prior_ordinal"]=max(updated["max_prior_ordinal"],len(history)-1)
    updated["correction_count"]=actual_count
    updated["decision_requirements"].extend(dr); updated["decision_bindings"].extend(db)
    updated["decision_applications"].extend(da)
    updated["remediation_history"].extend(
      e["payload"]["remediation"] for e in delta if e["event_kind"]=="REMEDIATION_CLAIM")
    publish_record(updated["vfs"],canonical_path("fal002.gate-record.v1",
      record["series_id"],record["record_id"]),record)
    return record,updated

def progress_inputs(rr,current):
    evidence={"repository":{"baseline_head":rr["repository"]["baseline_head"],
       "final_head":rr["repository"]["final_head"],"status":rr["repository"]["status"],
       "changed_paths":rr["repository"]["changed_paths"]},"diff":rr["diff"],
      "runtime":rr["runtime"],"tools":rr["tools"],
      "commands":[{"command_id":x["command_id"],"termination":x["termination"],
       "exit_code":x["exit_code"],"classification":x["classification"],
       "parsed_without_duration":{k:v for k,v in x["parsed"].items()
        if k!="duration_seconds_decimal"}} for x in rr["commands"]],"build":rr["build"]}
    unresolved=[{"finding_id":x["finding_id"],"occurrence":x["occurrence"],
      "state":x["state"],"severity_epoch":x["severity_epoch"],
      "epoch_baseline_severity":x["epoch_baseline_severity"],
      "current_severity":x["current_severity"],"current_blocking":x["current_blocking"],
      "last_event_hash":x["last_event_hash"],
      "remediation_evidence_hash_or_absent":x.get("remediation_evidence_hash")}
      for x in sorted(current,key=lambda y:(y["finding_id"],y["occurrence"]))
      if x["state"] in UNRESOLVED]
    return {"progress_evidence_hash":h("fal002-progress-evidence-v1",evidence),
      "unresolved_finding_set_hash":h("fal002-unresolved-findings-v1",unresolved),
      "unresolved":unresolved}

def progress_result(previous,current,previous_diff,current_diff,correction_count):
    p={(x["finding_id"],x["occurrence"]):x for x in previous["unresolved"]}
    c={(x["finding_id"],x["occurrence"]):x for x in current["unresolved"]}
    resolved_any=any(k not in c for k in p)
    introduced=any(k not in p and (x["current_blocking"] or x["current_severity"]=="CRITICAL")
      for k,x in c.items()) or any(k in p and
      ((not p[k]["current_blocking"] and x["current_blocking"]) or
       (p[k]["current_severity"]!="CRITICAL" and x["current_severity"]=="CRITICAL"))
      for k,x in c.items())
    material=(previous_diff!=current_diff or
      previous["progress_evidence_hash"]!=current["progress_evidence_hash"]) and \
      resolved_any and not introduced
    return "NO_PROGRESS" if not material else \
      ("CORRECTION_CEILING" if correction_count==2 else "MATERIAL_PROGRESS")
```

### 48.8 Exact publication-intent, recovery and rebinding constructors

These constructors are exhaustive for publication/recovery fixtures. `target_path` is supplied by the
closed `canonical_path` function, never by a case author.

```python
def canonical_path(surface,series,record_id):
    folder={"fal002.gate-record.v1":"gate","fal002.executor-exchange.v1":"executor",
      "fal002.run-record.v1":"run","fal002.reviewer-exchange.v1":"reviewer",
      "fal002.human-decision.v1":"decisions"}[surface]
    name=(f"{int(record_id[5:]):08d}" if surface=="fal002.gate-record.v1" else record_id)
    return f".forge/fal002/series/{series}/{folder}/{name}.json"

def slot(origin_series_id,predecessor,target_surface,target_id,reconstruction):
    value={"origin_series_id":origin_series_id,
      "predecessor_series_id":predecessor["series_id"],
      "predecessor_gate_id":predecessor["record_id"],
      "predecessor_gate_hash":predecessor["record_hash"],"target_surface":target_surface,
      "target_record_id":target_id,
      "target_path":canonical_path(target_surface,predecessor["series_id"],target_id),
      "reconstruction":reconstruction}
    return {"slot_id":h("fal002-publication-slot-v1",value),**value}

def publication_intent(lineage,target_record,source_record,stage_attempt):
    predecessor=lineage["active_gate"]; series=lineage["active_series_id"]
    assert predecessor["series_id"]==series
    assert target_record["series_id"]==series==source_record["series_id"]
    s=slot(lineage["origin_series_id"],predecessor,target_record["schema_id"],
      target_record["record_id"],"COMMITTED")
    value={"slot":s,"retained_state":predecessor["state"],
      "intended_record_hash":target_record["record_hash"],
      "intended_file_hash":hb(cf(target_record)),
      "stage_locator":f".forge/fal002/series/{predecessor['series_id']}/.staging/"
        f"{s['slot_id']}/attempt-{stage_attempt:04d}.json.part",
      "stage_attempt":stage_attempt,"stage_file_hash":hb(cf(target_record)),
      "source_authority":"REVIEWER_ADAPTER" if target_record["schema_id"]==
        "fal002.reviewer-exchange.v1" else "HUMAN_BOUNDARY",
      "source_record_id":source_record["record_id"],
      "source_record_hash":source_record["record_hash"]}
    value["intent_commitment_hash"]=h("fal002-publication-intent-v1",value)
    return gate(predecessor["sequence"]+1,predecessor["state"],"core",
      "PUBLICATION_INTENT_COMMITTED","PUBLICATION_INTENT",value,
      predecessor["record_hash"],lineage["correction_count"],series)

def obstruction(origin_series_id,predecessor,s,intent,target_record,observed=b"\x7b"):
    value={"origin_series_id":origin_series_id,
      "predecessor_series_id":predecessor["series_id"],
      "predecessor_gate_id":predecessor["record_id"],
      "predecessor_gate_hash":predecessor["record_hash"],"publication_slot":s,
      "intended_record_hash":target_record["record_hash"],
      "intended_file_hash":hb(cf(target_record)),"target_path":s["target_path"],
      "obstruction_kind":"MALFORMED_FILE","observed_content_hash":hb(observed),
      "path_object_kind":"REGULAR","frozen_hash":FROZEN}
    if intent is not None:
        value["intent_gate_id"]=intent["record_id"]
        value["intent_gate_hash"]=intent["record_hash"]
    return value

def discovery(origin_series_id,predecessor,s):
    material={"origin_series_id":origin_series_id,
      "predecessor_series_id":predecessor["series_id"],
      "predecessor_gate_id":predecessor["record_id"],
      "predecessor_gate_hash":predecessor["record_hash"],
      "publication_slot":{"slot_id":s["slot_id"],"target_surface":s["target_surface"],
       "target_record_id":s["target_record_id"],"target_path":s["target_path"]}}
    return material,h("fal002-recovery-discovery-v1",material)

def successor_id(key,n):
    return str(uuid.uuid5(uuid.UUID(NAMESPACE),f"fal002-recovery-discovery-v1:{key}:{n}"))

def rebound_bundle(requirement,series,generation,previous,obstruction_hash):
    did=requirement["decision_identity"]; pid=f"{did}-pending-b{generation:04d}"
    base={"decision_identity":did,
      "decision_requirement_hash":requirement["decision_requirement_hash"],
      "binding_generation":generation,"binding_series_id":series,
      "pending_card_record_id":pid,"pending_card_locator":canonical_path(
        "fal002.human-decision.v1",series,pid),"previous_binding_key":previous["binding_key"],
      "obstruction_evidence_hash":obstruction_hash}
    key=h("fal002-decision-binding-v1",{"binding_object_kind":"PENDING_BINDING","value":base})
    pending=make_record("fal002.human-decision.v1",pid,series,t(800+generation),
      {"decision_identity":did,"binding_generation":generation,"decision_kind":"PENDING_CARD",
       "status":"PENDING","owner":"human-product-owner",
       "provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
        "content_hash":hb(b"human-authority")},
       "payload":{"decision_requirement_hash":requirement["decision_requirement_hash"],
        "binding_key":key,"semantic_input":requirement["semantic_input"]}})[0]
    return {**base,"pending_card_record_hash":pending["record_hash"],"binding_key":key},pending

def resolution_for(requirement,bnd,pending,choice,rationale,application_ordinal=0,
                   previous_application=None,semantic_input=None,presentation_evidence=None):
    generation=bnd["binding_generation"]; did=requirement["decision_identity"]
    rsi=({"decision_identity":did,
      "answered_requirement_hash":requirement["decision_requirement_hash"],
      "answered_semantic_payload_hash":requirement["semantic_payload_hash"],
      "selected_choice":choice,"rationale":rationale,"human_owner":"human-product-owner",
      "human_provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
       "content_hash":hb(b"human-authority")},"decided_at":t(820)}
      if semantic_input is None else copy.deepcopy(semantic_input))
    assert rsi["decision_identity"]==did
    assert rsi["answered_requirement_hash"]==requirement["decision_requirement_hash"]
    assert rsi["answered_semantic_payload_hash"]==requirement["semantic_payload_hash"]
    assert rsi["selected_choice"]==choice
    pe=({"answered_pending_card_record_id":pending["record_id"],
      "answered_pending_card_record_hash":pending["record_hash"],
      "answered_binding_generation":generation,"answered_binding_key":bnd["binding_key"],
      "presented_at":pending["created_at"]} if presentation_evidence is None else
      {k:copy.deepcopy(v) for k,v in presentation_evidence.items()
       if k!="presentation_evidence_hash"})
    pe["presentation_evidence_hash"]=h("fal002-json-content-v1",pe)
    semantic_hash=h("fal002-json-content-v1",rsi)
    rid=f"{did}-resolution-b{generation:04d}"
    resolution=make_record("fal002.human-decision.v1",rid,bnd["binding_series_id"],t(821),
      {"decision_identity":did,"binding_generation":generation,"decision_kind":"RESOLUTION",
       "status":"ACCEPTED","owner":"human-product-owner",
       "provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
        "content_hash":hb(b"human-authority")},
       "payload":{"resolution_semantic_input":rsi,"resolution_semantic_hash":semantic_hash,
        "presentation_evidence":pe}})[0]
    app={"decision_identity":did,
      "decision_requirement_hash":requirement["decision_requirement_hash"],
      "binding_generation":generation,"binding_key":bnd["binding_key"],
      "pending_card_record_id":pending["record_id"],
      "pending_card_record_hash":pending["record_hash"],"resolution_record_id":rid,
      "resolution_locator":canonical_path("fal002.human-decision.v1",
        bnd["binding_series_id"],rid),"resolution_record_hash":resolution["record_hash"],
      "resolution_semantic_hash":semantic_hash,
      "presentation_evidence_hash":pe["presentation_evidence_hash"],"selected_choice":choice,
      "application_ordinal":application_ordinal}
    if previous_application is not None:
        app["previous_application_key"]=previous_application["application_key"]
    app["application_key"]=h("fal002-decision-binding-v1",
      {"binding_object_kind":"RESOLUTION_APPLICATION","value":app})
    return resolution,app

def relocate_resolution(requirement,binding0,pending0,resolution0,application0,series1):
    obstruction_hash=hb(b"resolution-path-obstruction")
    generation=binding0["binding_generation"]+1
    binding1,pending1=rebound_bundle(requirement,series1,generation,binding0,obstruction_hash)
    semantic=resolution0["payload"]["resolution_semantic_input"]
    presentation=resolution0["payload"]["presentation_evidence"]
    resolution1,application1=resolution_for(requirement,binding1,pending1,
      semantic["selected_choice"],semantic["rationale"],
      application0["application_ordinal"]+1,application0,semantic,presentation)
    assert pending0["record_hash"]!=pending1["record_hash"]
    assert resolution0["record_hash"]!=resolution1["record_hash"]
    assert resolution0["payload"]["resolution_semantic_hash"]== \
           resolution1["payload"]["resolution_semantic_hash"]
    assert application1["binding_key"]==binding1["binding_key"]
    assert application1["pending_card_record_hash"]==pending1["record_hash"]
    assert application1["presentation_evidence_hash"]== \
           presentation["presentation_evidence_hash"]
    return binding1,pending1,resolution1,application1

def relocate_offline_evidence(evidence0,binding1,pending1,resolution1,application1):
    evidence1={k:copy.deepcopy(v) for k,v in evidence0.items() if k!="evidence_id"}
    evidence1.update({"binding_generation":binding1["binding_generation"],
      "binding_key":binding1["binding_key"],"pending_card_record_id":pending1["record_id"],
      "pending_card_record_hash":pending1["record_hash"],
      "resolution_record_id":resolution1["record_id"],
      "resolution_record_hash":resolution1["record_hash"],
      "resolution_locator":application1["resolution_locator"],
      "resolution_semantic_hash":application1["resolution_semantic_hash"],
      "presentation_evidence_hash":application1["presentation_evidence_hash"],
      "collected_at":resolution1["created_at"]})
    evidence1["evidence_id"]=h("fal002-offline-evidence-v1",evidence1)
    return evidence1

def finding_decision_bundle(current,lineage,domain,choice):
    predecessor=lineage["active_gate"]; origin_series_id=lineage["origin_series_id"]
    assert domain in ("FINDING_RECLASSIFICATION","FINDING_DISPOSITION")
    choices=(["SET_LOW_NONBLOCKING","SET_LOW_BLOCKING","SET_MEDIUM_NONBLOCKING",
      "SET_MEDIUM_BLOCKING","SET_HIGH_NONBLOCKING","SET_HIGH_BLOCKING",
      "SET_CRITICAL_BLOCKING","DECLINE"] if domain=="FINDING_RECLASSIFICATION" else
      ["CLOSE_VERIFIED","SUPERSEDE","DECLINE"])
    assert choice in choices
    semantic={"domain":domain,"question":"What is the authorized finding disposition?",
      "allowed_choices":choices,
      "original_target":{"target_kind":"GATE","origin_series_id":origin_series_id,
       "target_record_id":predecessor["record_id"],
       "target_semantic_hash":predecessor["record_hash"]},
      "semantic_sources":[{"authority":"CANONICAL_MODEL",
       "record_id":current["finding_id"],"record_hash":current["last_event_hash"],
       "locator":"/payload/control/finding_checkpoint/current_findings"}]}
    did="D-"+h("fal002-decision-identity-v1",semantic)[:32]
    value={"decision_identity":did,"semantic_input":semantic,
      "semantic_payload_hash":h("fal002-json-content-v1",semantic),
      "required_authority":"HUMAN","originating_series_id":predecessor["series_id"],
      "originating_gate_id":predecessor["record_id"],
      "originating_gate_hash":predecessor["record_hash"],"created_at":t(825)}
    req={**value,"decision_requirement_hash":h("fal002-decision-requirement-v1",value)}
    bnd,pending=initial_binding(req,predecessor["series_id"])
    resolution,application=resolution_for(req,bnd,pending,choice,
      "Human authority selected the recorded finding disposition.")
    return req,bnd,pending,resolution,application

def conflict_bundle(lineage):
    predecessor=lineage["active_gate"]; origin_series_id=lineage["origin_series_id"]
    semantic={"domain":"AUTHORITY_CONFLICT","question":"Which recorded source governs?",
      "allowed_choices":["SELECT_SOURCE_A","SELECT_SOURCE_B","ABANDON_SERIES"],
      "original_target":{"target_kind":"GATE","origin_series_id":origin_series_id,
       "target_record_id":predecessor["record_id"],
       "target_semantic_hash":predecessor["record_hash"]},
      "semantic_sources":[
       {"authority":"HUMAN","record_id":"source-a","record_hash":hb(b"source-a"),
        "locator":"/payload/resolution_semantic_input"},
       {"authority":"HUMAN","record_id":"source-b","record_hash":hb(b"source-b"),
        "locator":"/payload/resolution_semantic_input"}]}
    did="D-"+h("fal002-decision-identity-v1",semantic)[:32]
    value={"decision_identity":did,"semantic_input":semantic,
      "semantic_payload_hash":h("fal002-json-content-v1",semantic),
      "required_authority":"HUMAN","originating_series_id":predecessor["series_id"],
      "originating_gate_id":predecessor["record_id"],
      "originating_gate_hash":predecessor["record_hash"],"created_at":t(830)}
    req={**value,"decision_requirement_hash":h("fal002-decision-requirement-v1",value)}
    bnd,pending=initial_binding(req,predecessor["series_id"])
    return req,bnd,pending

def recovery_requirement(origin_series_id,predecessor,obs,successor):
    semantic={"domain":"RECOVERY",
      "question":"May this logical lineage resume after the recorded obstruction?",
      "allowed_choices":["AUTHORIZE_RECOVERY_RESUME","ABANDON_LINEAGE"],
      "original_target":{"target_kind":"RECOVERY_ROOT","origin_series_id":origin_series_id,
       "target_record_id":"gate-00000000",
       "target_semantic_hash":h("fal002-recovery-condition-v1",obs)},
      "semantic_sources":[
       {"authority":"CANONICAL_MODEL","record_id":"obstruction-descriptor",
        "record_hash":h("fal002-recovery-condition-v1",obs),"locator":"/payload/obstruction"},
       {"authority":"STATE_SERIES","record_id":predecessor["record_id"],
        "record_hash":predecessor["record_hash"],"locator":"/payload"}]}
    did="D-"+h("fal002-decision-identity-v1",semantic)[:32]
    value={"decision_identity":did,"semantic_input":semantic,
      "semantic_payload_hash":h("fal002-json-content-v1",semantic),
      "required_authority":"HUMAN","originating_series_id":successor,
      "originating_gate_id":"gate-00000000","originating_gate_hash":predecessor["record_hash"],
      "created_at":t(810)}
    return {**value,"decision_requirement_hash":h("fal002-decision-requirement-v1",value)}

def initial_binding(requirement,series):
    did=requirement["decision_identity"]; pid=did+"-pending-b0000"
    base={"decision_identity":did,
      "decision_requirement_hash":requirement["decision_requirement_hash"],
      "binding_generation":0,"binding_series_id":series,"pending_card_record_id":pid,
      "pending_card_locator":canonical_path("fal002.human-decision.v1",series,pid)}
    key=h("fal002-decision-binding-v1",{"binding_object_kind":"PENDING_BINDING","value":base})
    pending=make_record("fal002.human-decision.v1",pid,series,t(811),
      {"decision_identity":did,"binding_generation":0,"decision_kind":"PENDING_CARD",
       "status":"PENDING","owner":"human-product-owner",
       "provenance":{"source":"CODEx_TASK","locator":"task://fal002-fixture",
        "content_hash":hb(b"human-authority")},
       "payload":{"decision_requirement_hash":requirement["decision_requirement_hash"],
        "binding_key":key,"semantic_input":requirement["semantic_input"]}})[0]
    return {**base,"pending_card_record_hash":pending["record_hash"],"binding_key":key},pending

def recovery_root(lineage,target_record,n):
    prior=copy.deepcopy(lineage); predecessor=prior["active_gate"]
    assert predecessor["series_id"]==prior["active_series_id"]==target_record["series_id"]
    origin_series_id=prior["origin_series_id"]
    s=slot(origin_series_id,predecessor,target_record["schema_id"],
      target_record["record_id"],"COMMITTED")
    intent=publication_intent(prior,target_record,target_record,0)[0]
    write_bytes(prior["vfs"],host_path(intent["payload"]["publication_intent"]["stage_locator"]),
      cf(target_record))
    publish_record(prior["vfs"],canonical_path("fal002.gate-record.v1",
      intent["series_id"],intent["record_id"]),intent)
    write_bytes(prior["vfs"],host_path(s["target_path"]),b"\x7b")
    obs=obstruction(origin_series_id,intent,s,intent,target_record,b"\x7b")
    material,key=discovery(origin_series_id,intent,s); successor=successor_id(key,n)
    for lower in range(n):
        lower_path=host_path(canonical_path("fal002.gate-record.v1",
          successor_id(key,lower),"gate-00000000"))
        assert lower_path in prior["vfs"]["regular"] or lower_path in prior["vfs"]["nonregular"]
    req=recovery_requirement(origin_series_id,intent,obs,successor)
    bnd,pending=initial_binding(req,successor)
    root={"origin_series_id":origin_series_id,"predecessor_series_id":intent["series_id"],
      "predecessor_gate_id":intent["record_id"],"predecessor_gate_hash":intent["record_hash"],
      "publication_slot":s,"recovery_discovery_material":material,
      "recovery_discovery_key":key,"obstruction":obs,
      "recovery_condition_hash":h("fal002-recovery-condition-v1",obs),
      "successor_series_id":successor,"recovery_ordinal":n,"predecessor_sealed":True,
      "retained_state":intent["state"],"scope_hash":SCOPE,"criteria_hash":CRITERIA,
      "allowed_paths_hash":h("fal002-json-content-v1",["forge/fal002.py"]),
      "command_policy_hash":POLICY,"frozen_hash":FROZEN,
      "correction_count":prior["correction_count"],
      "max_prior_ordinal":prior["max_prior_ordinal"],
      "finding_checkpoint":copy.deepcopy(prior["finding_checkpoint"]),
      "pending_decisions":prior["decision_requirements"]+[req],
      "active_decision_bindings":prior["decision_bindings"]+[bnd],
      "applied_decisions":copy.deepcopy(prior["decision_applications"]),
      "no_progress_history":copy.deepcopy(prior["no_progress_history"]),
      "intended_decision_record_id":pending["record_id"],
      "intended_decision_record_hash":pending["record_hash"]}
    record=gate(0,"awaiting_human","recovery","RECOVERY_SUCCESSOR","RECOVERY_ROOT",root,
      None,prior["correction_count"],successor)[0]
    updated=copy.deepcopy(prior); updated["active_gate"]=record
    updated["active_series_id"]=successor; updated["recovery_depth"]+=1
    updated["gate_chain"].extend([intent,record]); updated["decision_requirements"].append(req)
    updated["decision_bindings"].append(bnd); updated["pending_records"].append(pending)
    updated["publication_slots"].append(copy.deepcopy(s))
    publish_record(updated["vfs"],canonical_path("fal002.gate-record.v1",successor,
      record["record_id"]),record)
    publish_record(updated["vfs"],bnd["pending_card_locator"],pending)
    return record,pending,updated
```

### 48.9 Canonical mutation function

The mutation implementation is executable and uses strict RFC 6901 tokens. Mutation always returns
a deep copy; the input is unchanged.

```python
class OracleDefinitionError(Exception): pass

def pointer_tokens(pointer):
    if pointer=="": return []
    if not isinstance(pointer,str) or not pointer.startswith("/"):
        raise OracleDefinitionError("INVALID_POINTER")
    out=[]
    for raw_token in pointer[1:].split("/"):
        i=0; token=""
        while i<len(raw_token):
            if raw_token[i]!="~": token+=raw_token[i]; i+=1; continue
            if i+1==len(raw_token) or raw_token[i+1] not in "01":
                raise OracleDefinitionError("INVALID_POINTER_ESCAPE")
            token+=("~" if raw_token[i+1]=="0" else "/"); i+=2
        out.append(token)
    return out

def array_index(token,length,allow_end=False,allow_dash=False):
    if token=="-":
        if allow_dash: return length
        raise OracleDefinitionError("INVALID_ARRAY_INDEX")
    if not token or (len(token)>1 and token[0]=="0") or not token.isascii() or not token.isdigit():
        raise OracleDefinitionError("INVALID_ARRAY_INDEX")
    index=int(token); limit=length if allow_end else length-1
    if index<0 or index>limit: raise OracleDefinitionError("ARRAY_INDEX_OUT_OF_RANGE")
    return index

def pointer_parent(value,tokens):
    current=value
    for token in tokens[:-1]:
        if isinstance(current,dict):
            if token not in current: raise OracleDefinitionError("MISSING_PARENT")
            current=current[token]
        elif isinstance(current,list): current=current[array_index(token,len(current))]
        else: raise OracleDefinitionError("NON_CONTAINER_PARENT")
    return current

def replace(value,pointer,replacement):
    result=copy.deepcopy(value); tokens=pointer_tokens(pointer)
    if not tokens: return copy.deepcopy(replacement)
    parent=pointer_parent(result,tokens); token=tokens[-1]
    if isinstance(parent,dict):
        if token not in parent: raise OracleDefinitionError("MISSING_TARGET")
        parent[token]=copy.deepcopy(replacement)
    elif isinstance(parent,list): parent[array_index(token,len(parent))]=copy.deepcopy(replacement)
    else: raise OracleDefinitionError("NON_CONTAINER_PARENT")
    return result

def add(value,pointer,addition):
    result=copy.deepcopy(value); tokens=pointer_tokens(pointer)
    if not tokens: return copy.deepcopy(addition)
    parent=pointer_parent(result,tokens); token=tokens[-1]
    if isinstance(parent,dict): parent[token]=copy.deepcopy(addition)
    elif isinstance(parent,list):
        parent.insert(array_index(token,len(parent),allow_end=True,allow_dash=True),
                      copy.deepcopy(addition))
    else: raise OracleDefinitionError("NON_CONTAINER_PARENT")
    return result

def remove(value,pointer):
    result=copy.deepcopy(value); tokens=pointer_tokens(pointer)
    if not tokens: raise OracleDefinitionError("REMOVE_ROOT_FORBIDDEN")
    parent=pointer_parent(result,tokens); token=tokens[-1]
    if isinstance(parent,dict):
        if token not in parent: raise OracleDefinitionError("MISSING_TARGET")
        del parent[token]
    elif isinstance(parent,list): del parent[array_index(token,len(parent))]
    else: raise OracleDefinitionError("NON_CONTAINER_PARENT")
    return result

DERIVED_DEPENDENCY_ORDER=(
  "DecisionSemanticInput->semantic_payload_hash",
  "DecisionSemanticInput->decision_identity",
  "DecisionRequirement->decision_requirement_hash",
  "PresentationEvidence->presentation_evidence_hash",
  "ResolutionSemanticInput->resolution_semantic_hash",
  "DecisionBinding->binding_key",
  "DecisionApplication->application_key",
  "RemediationEvidence->remediation_evidence_hash",
  "FindingEvent->event_id,event_hash",
  "FindingEventHistory->FindingCheckpoint",
  "OfflineEvidence->evidence_id",
  "surface payload->payload_hash->record_hash")

REHASH_PATH_POLICY={
  "DecisionRequirement":("/semantic_input",),
  "DecisionResolution":("/payload/resolution_semantic_input",),
  "DecisionBinding":("/decision_requirement_hash","/binding_generation",
    "/binding_series_id","/pending_card_record_id","/pending_card_locator",
    "/previous_binding_key","/obstruction_evidence_hash"),
  "DecisionApplication":("/decision_requirement_hash","/binding_generation","/binding_key",
    "/pending_card_record_id","/pending_card_record_hash","/resolution_record_id",
    "/resolution_locator","/resolution_record_hash","/resolution_semantic_hash",
    "/presentation_evidence_hash","/selected_choice","/application_ordinal",
    "/previous_application_key"),
  "FindingEvent":("/payload",),"RemediationEvidence":("/",),
  "GateRecord":("/payload/manifest/scope_hash","/payload/publication_intent/intended_record_hash",
    "/payload/publication_intent/slot/target_record_id","/payload/control/finding_events")}

REHASH_PROHIBITED_WITHOUT_SOURCE=(
  "PendingDecisionCard.semantic_input","EvidenceBinding.content_hash",
  "FindingCheckpoint without complete FindingEvent history",
  "recovery condition/discovery material without exact obstruction and predecessor",
  "progress fingerprint without exact RunRecord and CurrentFindingState")

def rehash_value(value):
    if isinstance(value,list): return [rehash_value(x) for x in value]
    if not isinstance(value,dict): return copy.deepcopy(value)
    out={k:rehash_value(v) for k,v in value.items()
         if k not in ("payload_hash","record_hash")}
    if "presentation_evidence_hash" in value and "answered_binding_key" in value:
        base={k:v for k,v in out.items() if k!="presentation_evidence_hash"}
        out["presentation_evidence_hash"]=h("fal002-json-content-v1",base)
    if "decision_requirement_hash" in value and "semantic_input" in value:
        out["semantic_payload_hash"]=h("fal002-json-content-v1",out["semantic_input"])
        out["decision_identity"]="D-"+h("fal002-decision-identity-v1",
          out["semantic_input"])[:32]
        base={k:v for k,v in out.items() if k!="decision_requirement_hash"}
        out["decision_requirement_hash"]=h("fal002-decision-requirement-v1",base)
    if "binding_key" in value and "pending_card_locator" in value:
        base={k:v for k,v in out.items() if k not in ("binding_key","pending_card_record_hash")}
        out["binding_key"]=h("fal002-decision-binding-v1",
          {"binding_object_kind":"PENDING_BINDING","value":base})
    if "application_key" in value and "resolution_semantic_hash" in value:
        base={k:v for k,v in out.items() if k!="application_key"}
        out["application_key"]=h("fal002-decision-binding-v1",
          {"binding_object_kind":"RESOLUTION_APPLICATION","value":base})
    if "remediation_evidence_hash" in value and "correction_objective_id" in value:
        base={k:v for k,v in out.items() if k!="remediation_evidence_hash"}
        out["remediation_evidence_hash"]=h("fal002-remediation-evidence-v1",base)
    if "resolution_semantic_hash" in value and "resolution_semantic_input" in value:
        out["resolution_semantic_hash"]=h("fal002-json-content-v1",
          out["resolution_semantic_input"])
    if "event_hash" in value and "event_kind" in value:
        base={k:v for k,v in out.items() if k not in ("event_id","event_hash")}
        event_hash=h("fal002-finding-observation-v1",base)
        out={"event_id":"FE-"+event_hash[:20],**base,"event_hash":event_hash}
    if "evidence_id" in value and "command_policy_hash" in value:
        base={k:v for k,v in out.items() if k!="evidence_id"}
        out={**base,"evidence_id":h("fal002-offline-evidence-v1",base)}
    if "schema_id" in value:
        fields={k:out[k] for k in SURFACE_FIELDS[out["schema_id"]]}
        return make_record(out["schema_id"],out["record_id"],out["series_id"],
          out["created_at"],fields)[0]
    return out

def REHASH(value,lineage=None):
    work=copy.deepcopy(value)
    if isinstance(work,dict) and work.get("schema_id")=="fal002.gate-record.v1" and \
       work["payload"].get("variant_kind")=="CONTROL":
        if lineage is None: raise OracleDefinitionError("LINEAGE_REQUIRED_FOR_CONTROL_REHASH")
        delta=work["payload"]["control"]["finding_events"]
        history=copy.deepcopy(lineage["finding_events"])+copy.deepcopy(delta)
        work["payload"]["control"]["finding_checkpoint"]=checkpoint(history)
    return rehash_value(work)

def NO_REHASH(value,lineage=None): return copy.deepcopy(value)

def validate_requirement_hashes(requirement):
    semantic_hash=h("fal002-json-content-v1",requirement["semantic_input"])
    identity="D-"+h("fal002-decision-identity-v1",requirement["semantic_input"])[:32]
    base={k:v for k,v in requirement.items() if k!="decision_requirement_hash"}
    expected_requirement=h("fal002-decision-requirement-v1",base)
    return ("VALID" if requirement["semantic_payload_hash"]==semantic_hash and
      requirement["decision_identity"]==identity and
      requirement["decision_requirement_hash"]==expected_requirement else "HASH_MISMATCH")
```

`DERIVED_DEPENDENCY_ORDER` is the normative topological order. `REHASH` recursively rebuilds
innermost derived objects, including semantic payload hash before decision identity and requirement
hash, then presentation, binding, application, remediation, resolution and event objects; it derives
a CONTROL checkpoint from explicit complete lineage plus delta, and finally recomputes surface
payload and record hashes. `REHASH_PATH_POLICY` is the complete set of fixture-authorized REHASH
families. A path named by `REHASH_PROHIBITED_WITHOUT_SOURCE` must use `NO_REHASH` or a total
constructor carrying the named source context; direct REHASH raises `OracleDefinitionError` in its
own fixture wrapper. No normative matrix row may request REHASH outside this policy.
`HB(CF(record))` is computed only when the rehashed record is placed in the VFS/output. A required
ancestor context that is absent is `OracleDefinitionError`, never implementer discretion.

The virtual filesystem is a byte map with no host-I/O dependency:

```python
VROOT="/repo/.forge/fal002"
def vfs(): return {"regular":{},"nonregular":{},"operations":[]}
def write_bytes(fs,path,value):
    assert path.startswith(VROOT+"/") and isinstance(value,bytes) and path not in fs["nonregular"]
    fs["regular"][path]=value; fs["operations"].append(["WRITE_BYTES",path,value.hex()])
def remove_path(fs,path):
    fs["regular"].pop(path,None); fs["nonregular"].pop(path,None)
    fs["operations"].append(["REMOVE_PATH",path])
def make_nonregular(fs,path,kind):
    assert kind in ("SYMLINK","DIRECTORY","OTHER") and path not in fs["regular"]
    fs["nonregular"][path]=kind; fs["operations"].append(["MAKE_NONREGULAR",path,kind])
def host_path(relative): return VROOT+"/"+relative.removeprefix(".forge/fal002/")
def publish_record(fs,relative,record):
    path=host_path(relative); value=cf(record)
    if path in fs["nonregular"]: raise OracleDefinitionError("NONREGULAR_PATH")
    if path in fs["regular"]:
        if fs["regular"][path]!=value: raise OracleDefinitionError("DUPLICATE_CONFLICT")
        fs["operations"].append(["ADOPT_IDENTICAL",path,hb(value)]); return
    write_bytes(fs,path,value)
def fixture_files(fs):
    return [{"path":p,"bytes_hex":b.hex(),"file_hash":hb(b)}
            for p,b in sorted(fs["regular"].items())]
def raw(fs,path,hexbytes):
    if not isinstance(hexbytes,str) or len(hexbytes)%2 or any(c not in "0123456789abcdef" for c in hexbytes):
        raise OracleDefinitionError("INVALID_HEX_BYTES")
    write_bytes(fs,path,bytes.fromhex(hexbytes))

def raw_command(record,command_id,stream,hexbytes):
    if stream not in ("stdout","stderr"):
        raise OracleDefinitionError("INVALID_COMMAND_STREAM")
    if not isinstance(hexbytes,str) or len(hexbytes)%2 or any(c not in "0123456789abcdef" for c in hexbytes):
        raise OracleDefinitionError("INVALID_HEX_BYTES")
    matches=[c for c in record["commands"]
             if c["command_id"]==command_id]
    if len(matches)!=1: raise OracleDefinitionError("COMMAND_NOT_UNIQUE")
    return {"record":copy.deepcopy(record),"command_id":command_id,"stream":stream,
            "bytes":bytes.fromhex(hexbytes)}
```

An absent path is one missing from both maps. A staged path, final path and obstruction path are the
literal `host_path(stage_locator)`, `host_path(slot["target_path"])` and the same final path,
respectively. A partial stage writes `cf(target)[:len(cf(target))//2]`; a readable malformed
obstruction writes `b"\x7b"`; a collision writes `b"conflict\n"`. Operation order is exactly the
order in `fs["operations"]`. Filesystem cases may use only these functions.

The mandatory integrated scenarios are executable:

```python
def scenario_finding_chain():
    state=oracle_lineage_state(); state,_,rr0,rv0=make_run_review(state,0)
    finding=finding_observation(); e0=review_event(rv0,rr0,finding,0)
    _,state=control(state,[e0])
    e1=remediation_event(finding,e0,rr0,1); _,state=control(state,[e1])
    state,_,rr1,rv1=make_run_review(state,1)
    absent=finding_observation("HIGH",True,"ABSENT_AFTER_CORRECTION")
    e2=review_event(rv1,rr1,absent,2,e1); _,state=control(state,[e2])
    assert state["finding_checkpoint"]["event_count"]==3
    assert state["max_global_event_ordinal"]==2
    assert checkpoint(state["finding_events"])==state["finding_checkpoint"]
    return state

def scenario_finding_recovery():
    state=oracle_lineage_state(); state,_,rr0,rv0=make_run_review(state,0,publish_review=False)
    finding=finding_observation(); e0=review_event(rv0,rr0,finding,0)
    _,state=control(state,[e0])
    e1=remediation_event(finding,e0,rr0,1); _,state=control(state,[e1])
    before=copy.deepcopy(state["finding_checkpoint"])
    root,_,state=recovery_root(state,rv0,0)
    carried=root["payload"]["recovery_root"]
    assert carried["finding_checkpoint"]==before
    assert carried["finding_checkpoint"]["event_count"]==2
    assert carried["max_prior_ordinal"]==1
    assert state["finding_checkpoint"]==before
    return state

def scenario_review_binding():
    state=oracle_lineage_state(); state,_,rr0,rv0=make_run_review(state,0)
    state,_,rr1,rv1=make_run_review(state,1)
    finding=finding_observation()
    e0=review_event(rv0,rr0,finding,0)
    e1=review_event(rv1,rr1,finding,0)
    assert e0["payload"]["evidence_bindings"][0]["source_record_id"]==rr0["record_id"]
    assert e1["payload"]["evidence_bindings"][0]["source_record_id"]==rr1["record_id"]
    return rr0,rv0,e0,rr1,rv1,e1

def make_run_review(lineage,ordinal,outcome="CORRECTION_REQUIRED",observations=None,
                    publish_review=True):
    executor=executor_exchange(lineage,ordinal)[0]
    state=carry_surface(lineage,executor)
    rr=run(state,executor,ordinal)[0]; state=carry_surface(state,rr)
    rv=review(state,rr,outcome,observations)[0]
    if publish_review: state=carry_surface(state,rv)
    assert executor["series_id"]==rr["series_id"]==rv["series_id"]==state["active_series_id"]
    return state,executor,rr,rv

def scenario_recovery_n():
    state=oracle_lineage_state(); state,_,rr0,rv0=make_run_review(state,0,publish_review=False)
    finding=finding_observation(); e0=review_event(rv0,rr0,finding,0)
    _,state=control(state,[e0],count=1)
    origin_series=state["active_series_id"]
    root1,_,state=recovery_root(state,rv0,0); series1=state["active_series_id"]
    e1=remediation_event(finding,e0,rr0,1); _,state=control(state,[e1])
    state,_,rr1,rv1=make_run_review(state,1,publish_review=False)
    immutable_before=copy.deepcopy(state["vfs"]["regular"])
    root2,_,state=recovery_root(state,rv1,0); series2=state["active_series_id"]
    intent2=state["gate_chain"][-2]
    assert origin_series!=series1 and series1!=series2 and origin_series!=series2
    assert root1["series_id"]==series1 and root2["series_id"]==series2
    assert intent2["series_id"]==series1
    assert root2["payload"]["recovery_root"]["predecessor_series_id"]==series1
    assert state["origin_series_id"]==origin_series and state["recovery_depth"]==2
    assert state["finding_checkpoint"]["event_count"]==2
    assert state["correction_count"]==1 and state["no_progress_history"]==[]
    assert len(state["publication_slots"])==2
    assert len({x["slot_id"] for x in state["publication_slots"]})==2
    assert len({x["target_path"] for x in state["publication_slots"]})==2
    for path,value in immutable_before.items(): assert state["vfs"]["regular"][path]==value
    root_paths=[host_path(canonical_path("fal002.gate-record.v1",x["series_id"],x["record_id"]))
      for x in (root1,root2)]
    assert root_paths[0]!=root_paths[1] and all(p in state["vfs"]["regular"] for p in root_paths)
    return {"state":state,"root1":root1,"root2":root2,"run0":rr0,"review0":rv0,
      "run1":rr1,"review1":rv1,"event0":e0,"event1":e1,
      "origin_series":origin_series,"series1":series1,"series2":series2}

def scenario_successor_run_review():
    state=oracle_lineage_state(); state,_,rr0,rv0=make_run_review(state,0,publish_review=False)
    observation=finding_observation(); e0=review_event(rv0,rr0,observation,0)
    _,state=control(state,[e0],count=1); origin_series=state["active_series_id"]
    _,_,state=recovery_root(state,rv0,0); series1=state["active_series_id"]
    state,_,rr1,rv1=make_run_review(state,1,publish_review=False)
    e1=review_event(rv1,rr1,finding_observation("HIGH",True,"STILL_PRESENT"),1,e0)
    _,state=control(state,[e1])
    _,_,state=recovery_root(state,rv1,0); series2=state["active_series_id"]
    state,_,rr2,rv2=make_run_review(state,2)
    e2=review_event(rv2,rr2,finding_observation("HIGH",True,"STILL_PRESENT"),2,e1)
    _,state=control(state,[e2])
    assert len({origin_series,series1,series2})==3
    assert rr0["series_id"]==rv0["series_id"]==origin_series
    assert rr1["series_id"]==rv1["series_id"]==series1
    assert rr2["series_id"]==rv2["series_id"]==series2
    for record in (rr0,rr1,rr2):
        path=host_path(canonical_path(record["schema_id"],record["series_id"],record["record_id"]))
        assert state["vfs"]["regular"][path]==cf(record)
    assert len({rr0["record_id"],rr1["record_id"],rr2["record_id"]})==3
    assert e0["payload"]["evidence_bindings"][0]["provenance"]["record_hash"]==rr0["record_hash"]
    assert e1["payload"]["evidence_bindings"][0]["provenance"]["record_hash"]==rr1["record_hash"]
    assert e2["payload"]["evidence_bindings"][0]["source_record_id"]==rr2["record_id"]
    assert e2["payload"]["evidence_bindings"][0]["provenance"]["record_hash"]==rr2["record_hash"]
    assert [x["event_ordinal"] for x in state["finding_events"]]==[0,1,2]
    assert state["max_global_event_ordinal"]==2 and state["finding_checkpoint"]["event_count"]==3
    return {"state":state,"origin_series":origin_series,"series1":series1,"series2":series2,
      "run0":rr0,"review0":rv0,"event0":e0,"run1":rr1,"review1":rv1,"event1":e1,
      "run2":rr2,"review2":rv2,"event2":e2}

def scenario_decision_relocation():
    requirement,binding0,pending0,resolution0,application0,evidence=offline_bundle()
    series1="00000000-0000-4000-8000-000000000099"
    binding_before,pending_before=rebound_bundle(requirement,series1,1,binding0,
      hb(b"pending-path-obstruction"))
    resolution_after,application_after=resolution_for(requirement,binding_before,pending_before,
      "AUTHORIZE_OFFLINE","Offline execution is authorized for this fixture.")
    binding1,pending1,resolution1,application1=relocate_resolution(requirement,binding0,
      pending0,resolution0,application0,series1)
    evidence1=relocate_offline_evidence(evidence,binding1,pending1,resolution1,application1)
    assert evidence1["resolution_semantic_hash"]==evidence["resolution_semantic_hash"]
    assert evidence1["resolution_record_hash"]!=evidence["resolution_record_hash"]
    assert evidence1["pending_card_record_hash"]!=evidence["pending_card_record_hash"]
    assert resolution_after["payload"]["resolution_semantic_input"]["answered_requirement_hash"]== \
           requirement["decision_requirement_hash"]
    assert application_after["binding_key"]==binding_before["binding_key"]
    return {"requirement":requirement,"binding0":binding0,"pending0":pending0,
      "resolution0":resolution0,"application0":application0,"binding1":binding1,
      "pending1":pending1,"resolution1":resolution1,"application1":application1,
      "binding_before":binding_before,"pending_before":pending_before,
      "resolution_after":resolution_after,"application_after":application_after,
      "offline_evidence0":evidence,"offline_evidence1":evidence1}

def scenario_mutation():
    base=gate0()[0]
    mutated=replace(base,"/payload/manifest/scope_hash","0"*64)
    stale=NO_REHASH(mutated); current=REHASH(mutated)
    assert stale["record_hash"]==base["record_hash"]
    assert current["record_hash"]!=base["record_hash"]
    return {"base":base,"pointer":"/payload/manifest/scope_hash",
      "operation":"replace","value":"0"*64,"REHASH":current,
      "REHASH_disposition":"AUTHORITY_CONFLICT","NO_REHASH":stale,
      "NO_REHASH_disposition":"HASH_MISMATCH"}

def scenario_rehash_decision_requirement():
    base=offline_bundle()[0]; pointer="/semantic_input/question"
    changed=replace(base,pointer,"May this independently mutated fixture execute offline?")
    current=REHASH(changed); stale=NO_REHASH(changed)
    expected_semantic=h("fal002-json-content-v1",current["semantic_input"])
    expected_identity="D-"+h("fal002-decision-identity-v1",current["semantic_input"])[:32]
    expected_base={k:v for k,v in current.items() if k!="decision_requirement_hash"}
    expected_requirement=h("fal002-decision-requirement-v1",expected_base)
    assert current["semantic_payload_hash"]==expected_semantic
    assert current["decision_identity"]==expected_identity
    assert current["decision_requirement_hash"]==expected_requirement
    assert current["semantic_payload_hash"]!=base["semantic_payload_hash"]
    assert current["decision_requirement_hash"]!=base["decision_requirement_hash"]
    assert validate_requirement_hashes(current)=="VALID"
    assert stale["semantic_payload_hash"]==base["semantic_payload_hash"]
    assert stale["decision_requirement_hash"]==base["decision_requirement_hash"]
    assert validate_requirement_hashes(stale)=="HASH_MISMATCH"
    return {"base":base,"pointer":pointer,"REHASH":current,"NO_REHASH":stale,
      "REHASH_disposition":"VALID","NO_REHASH_disposition":"HASH_MISMATCH"}

def scenario_resolution_relocation_recovery_n():
    recovered=scenario_recovery_n(); decision=scenario_decision_relocation()
    b2,p2,r2,a2=relocate_resolution(decision["requirement"],decision["binding1"],
      decision["pending1"],decision["resolution1"],decision["application1"],
      recovered["series2"])
    assert r2["payload"]["resolution_semantic_hash"]== \
      decision["resolution0"]["payload"]["resolution_semantic_hash"]
    assert len({decision["resolution0"]["record_hash"],decision["resolution1"]["record_hash"],
      r2["record_hash"]})==3
    assert a2["binding_generation"]==2 and b2["binding_generation"]==2
    return {"recovery":recovered,"binding2":b2,"pending2":p2,
      "resolution2":r2,"application2":a2,**decision}

def scenario_vfs_create_only():
    state=oracle_lineage_state(); state,_,_,target=make_run_review(state,0,publish_review=False)
    intent=publication_intent(state,target,target,0)[0]
    intent_path=canonical_path(intent["schema_id"],intent["series_id"],intent["record_id"])
    publish_record(state["vfs"],intent_path,intent); publish_record(state["vfs"],intent_path,intent)
    target_path=canonical_path(target["schema_id"],target["series_id"],target["record_id"])
    raw(state["vfs"],host_path(target_path),"7b")
    preserved=state["vfs"]["regular"][host_path(target_path)]
    try: publish_record(state["vfs"],target_path,target)
    except OracleDefinitionError as error: assert str(error)=="DUPLICATE_CONFLICT"
    else: raise AssertionError("obstruction was overwritten")
    assert state["vfs"]["regular"][host_path(target_path)]==preserved==b"\x7b"
    return {"state":state,"intent":intent,"target":target,
      "disposition":"DUPLICATE_CONFLICT"}

def scenario_progress_across_recovery():
    recovered=scenario_recovery_n(); carried=recovered["root2"]["payload"]["recovery_root"]
    current=recovered["state"]
    assert carried["no_progress_history"]==current["no_progress_history"]==[]
    assert carried["correction_count"]==current["correction_count"]==1
    assert carried["finding_checkpoint"]==current["finding_checkpoint"]
    return {"carried":carried,"current":current,"disposition":"CARRIED_IDENTICALLY"}

def execute_normative_oracle():
    return {"finding_chain":scenario_finding_chain(),
      "finding_recovery":scenario_finding_recovery(),"recovery_n":scenario_recovery_n(),
      "origin_review_binding":scenario_review_binding(),
      "successor_run_review":scenario_successor_run_review(),
      "decision_semantic_relocation":scenario_decision_relocation(),
      "nested_rehash":scenario_rehash_decision_requirement()["REHASH"],
      "nested_no_rehash":scenario_rehash_decision_requirement()["NO_REHASH"],
      "vfs_create_only":scenario_vfs_create_only(),
      "resolution_relocation_recovery_n":scenario_resolution_relocation_recovery_n(),
      "progress_across_recovery":scenario_progress_across_recovery()}

def case_environment():
    state=oracle_lineage_state(); decision=scenario_decision_relocation()
    rr0,rv0,e0,rr1,rv1,e1=scenario_review_binding()
    executor0=executor_exchange(state,0)[0]; intent0=publication_intent(state,rv0,rv0,0)[0]
    slot0=intent0["payload"]["publication_intent"]["slot"]
    root0,pending_recovery,state0=recovery_root(copy.deepcopy(state),rv0,0)
    key=root0["payload"]["recovery_root"]["recovery_discovery_key"]
    collision_state=copy.deepcopy(state)
    candidate0=canonical_path("fal002.gate-record.v1",successor_id(key,0),"gate-00000000")
    raw(collision_state["vfs"],host_path(candidate0),"7b")
    root1,_,_=recovery_root(collision_state,rv0,1)
    return {"state":state,"fs":copy.deepcopy(state["vfs"]),"gate0":gate0()[0],
      "ready":ready(state)[0],"run0":rr0,"run1":rr1,"review0":rv0,"review1":rv1,
      "event0":e0,"event1":e1,"key":key,"root0":root0,"root1":root1,
      "executor0":executor0,"intent0":intent0,"slot0":slot0,
      "stage0":intent0["payload"]["publication_intent"]["stage_locator"],
      "candidate0":candidate0,
      "candidate1":canonical_path("fal002.gate-record.v1",successor_id(key,1),"gate-00000000"),
      "pending_recovery":pending_recovery,"finding_chain":scenario_finding_chain(),
      "finding_recovery":scenario_finding_recovery(),"recovery_n":scenario_recovery_n(),
      "successor_run_review":scenario_successor_run_review(),
      "rehash_requirement":scenario_rehash_decision_requirement(),
      "vfs_create_only":scenario_vfs_create_only(),
      "mutation":scenario_mutation(),**decision}
```

### 48.10 Exact CORR-015 fixture matrix

Every row begins independently with `e=case_environment()`. The rows changed by CORR-015 use exact
Python syntax naming the constructor, mutation or VFS operation to execute; unchanged historical
assertion rows retain their previously reviewed compact notation. Before its operation, each row
assigns every bare local from
this closed map: `state=e["state"]`, `fs=e["fs"]`, `gate0=e["gate0"]`, `ready=e["ready"]`,
`run0=e["run0"]`, `run1=e["run1"]`, `review0=e["review0"]`, `review1=e["review1"]`,
`target=e["review0"]`, `intent=e["intent0"]`, `stage=e["stage0"]`, `key=e["key"]`,
`root0=e["root0"]`, `root1=e["root1"]`, `candidate0=e["candidate0"]`,
`candidate1=e["candidate1"]`, and the `requirement`, `binding0`, `binding1`, `pending0`, `pending1`,
`resolution0`, `resolution1`, `application0`, `application1`, `offline_evidence0`,
`offline_evidence1`, `binding_before`, `pending_before`, `resolution_after`, `application_after`,
`event0` and
`event1` locals are the dictionary members whose keys exactly equal those local names. A row that
names `x` initializes it explicitly
from one of those locals. No row inherits a mutated object or VFS from another row. Operations
execute left-to-right. `REHASH` means the executable
function with `e["state"]`; `NO_REHASH` means its executable function. Expected valid files are
exact `cf(record)` and expected hashes are §48.1 outputs. Invalid input is never published as an
authoritative final.

| Case ID | Base; exact operation | Expected |
| --- | --- | --- |
| `hash-file-lf` | gate0 | file equals `cj(gate0)+0a`; record hash excludes LF |
| `hash-preimage-no-lf` | gate0 | preimage equals `cj({domain:"fal002-record-v1:fal002.gate-record.v1",value:gate0 without record_hash})` |
| `hash-wrong-lf` | gate0; set record_hash to sha256(preimage+0a); NO_REHASH | HASH_MISMATCH; no authority |
| `hash-domain-missing` | gate0; replace record_hash with sha256(cj(record without hash)); NO_REHASH | HASH_MISMATCH |
| `intent-not-required` | `next_gate=ready(state)[0]` | `next_gate["payload"]["kind"]=="READY"`; ordinary reconstructable gate append requires no PUBLICATION_INTENT |
| `intent-required-missing` | `fs=vfs(); target=executor_exchange(state,0)[0]; publish_record(fs,canonical_path(target["schema_id"],target["series_id"],target["record_id"]),target)` | FORBIDDEN_TRANSITION; target ignored because no PUBLICATION_INTENT exists |
| `intent-valid` | `target=review0; intent=publication_intent(state,target,target,0)[0]` | `intent["series_id"]==state["active_series_id"]`; intent gate final; retained reviewing state |
| `intent-wrong-predecessor` | `x=replace(intent,"/payload/publication_intent/slot/predecessor_gate_hash","0"*64); NO_REHASH(x)` | HASH_MISMATCH |
| `intent-wrong-slot` | `x=replace(intent,"/payload/publication_intent/slot/target_record_id","review-wrong"); REHASH(x,state)` | MALFORMED_BOUNDARY |
| `intent-wrong-hash` | `x=replace(intent,"/payload/publication_intent/intended_record_hash","0"*64); REHASH(x,state)` | HASH_MISMATCH |
| `intent-replay` | `publish_record(fs,canonical_path(intent["schema_id"],intent["series_id"],intent["record_id"]),intent)` twice | one final; idempotent |
| `intent-crash-stage` | `write_bytes(fs,host_path(stage),cf(target)[:len(cf(target))//2])` | partial bytes preserved; `stage_attempt=1` selects attempt-0001; predecessor active until intent final |
| `intent-crash-after-final` | `publish_record(fs,canonical_path(intent["schema_id"],intent["series_id"],intent["record_id"]),intent)` | target absent; intent gate active; replay uses `cf(target)` without actor invocation |
| `discovery-zero` | `raw(state["vfs"],host_path(intent["payload"]["publication_intent"]["slot"]["target_path"]),"7b"); root,card,next_state=recovery_root(state,target,0)` | `root["series_id"]==successor_id(root["payload"]["recovery_root"]["recovery_discovery_key"],0)`; authoritative awaiting_human |
| `discovery-candidate-invalid` | `raw(fs,host_path(candidate0),"7b")` | preserve exact byte; candidate-1 eligible |
| `discovery-later` | `raw(state["vfs"],host_path(candidate0),"7b"); root,card,next_state=recovery_root(state,target,1)` | `root["series_id"]==successor_id(key,1)`; ordinal 1 root authoritative |
| `discovery-first-absent` | assert `host_path(candidate0)` absent; `publish_record(fs,candidate1,root1)` | candidate-1 ignored; predecessor remains active |
| `discovery-wrong-lineage` | `x=replace(root0,"/payload/recovery_root/origin_series_id","00000000-0000-4000-8000-000000000003"); NO_REHASH(x)` | HASH_MISMATCH; invalid stable candidate; no authority |
| `discovery-no-directory-heuristic` | `publish_record(fs,canonical_path("fal002.gate-record.v1","00000000-0000-4000-8000-000000000099","gate-00000000"),root0)` | ignored evidence |
| `recovery-crash-before-root` | `write_bytes(fs,host_path(intent["payload"]["publication_intent"]["stage_locator"]),cf(root0)); assert host_path(candidate0) not in fs["regular"]` | predecessor active; replay produces byte-identical `root0` |
| `recovery-crash-after-root` | `publish_record(fs,candidate0,root0); assert host_path(root0["payload"]["recovery_root"]["decision_binding"]["pending_card_locator"]) not in fs["regular"]` | successor authoritative; replay publishes exact bound decision |
| `recovery-chain-two` | `x=scenario_recovery_n()` | `x["root2"]["payload"]["recovery_root"]["predecessor_series_id"]==x["series1"]`; one logical lineage; depth 2 |
| `successor-run-review` | `x=scenario_successor_run_review()` | Run0/1/2 and Review0/1/2 use `x["origin_series"]`, `x["series1"]`, `x["series2"]`; event ordinals equal `[0,1,2]` |
| `decision-binding-zero` | `x=scenario_decision_relocation(); fs=vfs(); publish_record(fs,x["binding0"]["pending_card_locator"],x["pending0"]); assert fs["regular"][host_path(x["binding0"]["pending_card_locator"])]==cf(x["pending0"])` | exact active locator/read succeeds |
| `decision-path-obstructed` | `raw(fs,host_path(binding0["pending_card_locator"]),"7b")` | same decision identity pending; successor recovery and generation 1 |
| `decision-pending-only` | `offline_bundle()`; remove resolution and application files/state | PENDING; no state authority |
| `decision-resolution-separate` | publish pending and resolution to their distinct canonical locators; carry application | ACCEPTED AUTHORIZE_OFFLINE; pending bytes unchanged |
| `decision-pending-rebound-after-answer` | `scenario_decision_relocation()` | `pending0.record_hash != pending1.record_hash`; stable semantic input/hash; application1 binds pending1 and historical presentation0 |
| `decision-pending-rebound-before-answer` | `binding_before,pending_before,resolution_after,application_after` from `scenario_decision_relocation()` | P1 presentation is answered; semantic answer validates against the unchanged requirement; application binds P1 |
| `decision-resolution-obstructed` | `raw(fs,host_path(application0["resolution_locator"]),"7b")`; use `resolution1`/`application1` from `scenario_decision_relocation()` | R0 physical obstruction; R1 physical hash differs; semantic hash identical; one applied answer |
| `decision-resolution-replay` | `publish_record(fs,application1["resolution_locator"],resolution1)` twice with create-only identical-byte adoption | one semantic resolution; idempotent |
| `decision-resolution-conflict` | `x=replace(resolution1,"/payload/resolution_semantic_input/selected_choice","DECLINE"); x=REHASH(x)` | different semantic hash/choice; AUTHORITY_CONFLICT; no application |
| `decision-resolution-orphan` | publish accepted resolution at canonical path for inactive series `00000000-0000-4000-8000-000000000099` | STALE_RECORD; ignored for authority |
| `decision-recovery-n` | `x=scenario_resolution_relocation_recovery_n()` | one semantic resolution hash across R0/R1/R2; physical hashes distinct; `x["binding2"]["binding_generation"]==2` |
| `decision-requirement-rehash` | `x=scenario_rehash_decision_requirement()` | `x["REHASH_disposition"]=="VALID"`; semantic payload, identity and requirement hash recomputed in dependency order |
| `decision-requirement-no-rehash` | `x=scenario_rehash_decision_requirement()` | `x["NO_REHASH_disposition"]=="HASH_MISMATCH"`; stale nested and outer hashes retained |
| `vfs-create-only` | `x=scenario_vfs_create_only()` | identical intent replay adopted; conflicting target bytes preserved; `x["disposition"]=="DUPLICATE_CONFLICT"` |
| `decision-rebound` | compare `binding0,pending0,resolution0` to `binding1,pending1,resolution1` | same decision identity and semantic answer hash; new physical pending/resolution records |
| `decision-generation-gap` | generation 0 then 2 | AUTHORITY_CONFLICT |
| `decision-orphan` | valid record at unbound locator | ignored evidence; cannot resolve |
| `decision-inactive` | valid generation-0 record after generation-1 binding | STALE_RECORD for lookup |
| `decision-wrong-hash` | active record; replace `/record_hash` with 64 `0`; NO_REHASH | HASH_MISMATCH |
| `offline-origin` | gate0 + valid origin offline resolution | pre-spawn resolution succeeds |
| `offline-rebound` | validate `application1`, `resolution1` and `offline_evidence1` through §46.4 | same AUTHORIZE_OFFLINE semantic result despite P0/P1 and R0/R1 hash differences |
| `offline-wrong-locator` | gate0; replace `/payload/manifest/offline_evidence/resolution_locator` with `x.json` | HASH_MISMATCH |
| `offline-wrong-identity` | replace offline `decision_identity` with `D-00000000000000000000000000000000` | HASH_MISMATCH |
| `offline-nonaccepted` | resolution status DECLINED, choice DECLINE | MALFORMED_BOUNDARY; no spawn |
| `finding-same-severity` | NEW HIGH/blocking then STILL_PRESENT HIGH/blocking | current HIGH/blocking OPEN |
| `finding-increase` | NEW MEDIUM/false then STILL_PRESENT HIGH/true | current HIGH/blocking OPEN; introduced_blocker true |
| `finding-decrease-proposal` | NEW HIGH/true then STILL_PRESENT MEDIUM/false | current remains HIGH/true; pending reclassification |
| `finding-invalid-clear` | correction claim attempts current_blocking false directly | FORBIDDEN_TRANSITION |
| `finding-addressed-missing-evidence` | OPEN then CONTROL without RemediationEvidence | remains OPEN; MISSING_EVIDENCE |
| `finding-addressed-valid` | OPEN then exact remediation() | ADDRESSED_AWAITING_REVIEW; unresolved |
| `finding-addressed-empty-review` | addressed then review findings empty | stays addressed; PASS blocked |
| `finding-addressed-still-present` | addressed then STILL_PRESENT | OPEN |
| `finding-verified` | addressed then ABSENT_AFTER_CORRECTION exact evidence/rationale | INDEPENDENTLY_VERIFIED |
| `finding-failed-verification` | addressed then STILL_PRESENT reviewer event | OPEN; unresolved |
| `finding-human-downgrade` | NEW HIGH/true then applied human reclassification MEDIUM/false | MEDIUM/false in epoch 1; lifecycle unchanged |
| `finding-post-human-escalation` | human MEDIUM/false baseline then reviewer HIGH/true | HIGH/true in epoch 1 |
| `finding-post-human-lower` | human MEDIUM/false baseline then reviewer LOW/false | MEDIUM/false in epoch 1 |
| `finding-missing-prior` | remove `previous_event_hash` from event ordinal 1; REHASH | HASH_MISMATCH; reconstruction and PASS blocked |
| `finding-duplicate-identical` | carry the same event ID/hash/bytes twice at the same logical position | idempotent one event |
| `finding-duplicate-conflict` | reuse event ID and ordinal with changed statement; REHASH | AUTHORITY_CONFLICT |
| `finding-restart` | serialize each CONTROL with CF; discard memory; traverse origin and fold stored deltas | byte-identical checkpoint/current state |
| `finding-control-chain` | `state=scenario_finding_chain()` | event count 3; max global ordinal 2; online and restart checkpoints identical |
| `finding-recovery-carry` | `state=scenario_finding_recovery()` | recovery event count 2; max prior ordinal 1; finding/current/progress state retained |
| `review-binding-zero` | `scenario_review_binding()` values `run0,review0,event0` | event0 EvidenceBinding source equals run0 ID/hash |
| `review-binding-one` | `scenario_review_binding()` values `run1,review1,event1` | event1 EvidenceBinding source equals run1 ID/hash |
| `finding-recurrence` | independently verified then STILL_PRESENT | OPEN same occurrence |
| `finding-recurrence-after-close` | CLOSED occurrence 0 then NEW with terminal event hash | occurrence 1 OPEN |
| `finding-bad-recurrence` | CLOSED then NEW without terminal event hash | FORBIDDEN_TRANSITION |
| `finding-supersession` | OPEN then accepted SUPERSEDE naming K2 | occurrence 0 SUPERSEDED; K2 independently derived |
| `finding-incomplete-history` | remove first NEW event from addressed history | HASH_MISMATCH; PASS/no-progress blocked |
| `progress-severity-blocker` | previous MEDIUM/false; current HIGH/true, diff/evidence changed | introduced_blocker; NO_PROGRESS |
| `progress-remediation-only` | same diff/evidence; OPEN→ADDRESSED with evidence | unresolved, resolved_any false; NO_PROGRESS |
| `progress-across-recovery` | `x=scenario_progress_across_recovery()` | `x["disposition"]=="CARRIED_IDENTICALLY"`; checkpoint, correction count and no-progress history equal across physical segments |
| `progress-ceiling` | material progress true, correction_count 2 | CORRECTION_CEILING after progress calculation |
| `progress-diff-only` | change only diff hash | NO_PROGRESS; resolved_any false |
| `progress-evidence-only` | change only progress evidence hash | NO_PROGRESS; resolved_any false |
| `progress-lifecycle-only` | OPEN→INDEPENDENTLY_VERIFIED; keep diff/evidence hashes | NO_PROGRESS |
| `progress-severity-only` | raise current severity only | NO_PROGRESS; introduced_blocker when CRITICAL |
| `progress-blocking-only` | false→true only | NO_PROGRESS; introduced_blocker |
| `progress-verification-only` | ADDRESSED→INDEPENDENTLY_VERIFIED only | NO_PROGRESS without diff/evidence change |
| `mutation-rehash` | `scenario_mutation()["REHASH"]` after exact scope pointer replacement | new canonical record hash; AUTHORITY_CONFLICT against frozen scope |
| `mutation-no-rehash` | `scenario_mutation()["NO_REHASH"]` after same replacement | stale record hash; HASH_MISMATCH |

### 48.11 Legacy fixture coverage under final constructors

The 19 committed fixture filenames remain planned, but their historical bytes/hashes are withdrawn.
They are regenerated only from §§48.1–48.9. Every subcase starts with a fresh
`e=case_environment()` and the indicated base; no object, VFS or mutation is shared. Their exact
normalized operations are:

- GATE invalid predecessor: `remove(e["gate0"],"/predecessor")`; unknown field:
  `add(e["gate0"],"/unknown",1)`;
- EXEC forbidden PASS: `add(e["executor0"],"/result/outcome","PASS")`;
- RUN bad record hash: `NO_REHASH(replace(e["run0"],"/record_hash","0"*64))`; unknown:
  `add(e["run0"],"/unknown",1)`; missing executable begins `x=e["run0"]` and applies, in order,
  `replace(x,"/commands/1/termination","SPAWN_ERROR")`,
  `replace(x,"/commands/1/exit_code",None)` and
  `replace(x,"/commands/1/parsed",{"available":False,"failure_reason":"COMMAND_FAILURE"})`;
  timeout applies the same three operations at command index 13 with termination `TIMEOUT`;
- invalid UTF-8: `raw_command(e["run0"],"PYTEST","stdout","ff")`; malformed Git version:
  `raw_command(e["run0"],"GIT-VERSION","stdout","676974203f3f3f0a")`; ambiguous pytest:
  `raw_command(e["run0"],"PYTEST","stdout","312070617373656420696e20302e3031730a312070617373656420696e20302e3031730a")`;
- REVIEW missing binding: `remove(e["review0"],"/result/criterion_evidence/0")`; same
  principal: `replace(e["review0"],"/reviewer_execution/grant/principal_id","principal-executor")`;
  inherited context: `add(e["review0"],"/reviewer_execution/grant/prior_context_id","ctx-old")`;
- DECISION missing owner: `remove(e["pending0"],"/owner")`; unknown:
  `add(e["pending0"],"/unknown",1)`; stale target replaces the exact
  `/payload/decision_card/original_target/target_semantic_hash` in the applicable closure-card
  constructor with `"0"*64`; declined resolution uses status `DECLINED` and the exact domain choice
  `DECLINE`;
- HASH order wrong predecessor is `replace(e["gate0"],"/predecessor","0"*64)`; gap begins
  `x=e["gate0"]` and applies
  `replace(x,"/sequence",3)` then `replace(x,"/record_id","gate-00000003")`; stale replaces both
  fields with their exact zero equivalents;
- duplicate same publishes exact CF bytes; duplicate different uses
  `REHASH(replace(e["gate0"],"/payload/manifest/scope_hash",hb(b"different")))`;
- partial uses exactly `cf(record)[:len(cf(record))//2]` at attempt zero;
- redaction raw input is UTF-8 `criterion=abc token='x y'` and exact persisted replacement
  `criterion=abc token='<REDACTED>'`;
- conditional source bytes are
  `6966207379732e706c6174666f726d3d3d2778273a20696d706f727420666f7267652e610a696620545950455f434845434b494e473a20696d706f727420666f7267652e620a`;
  literal dynamic bytes are
  `696d706f72746c69622e696d706f72745f6d6f64756c652827666f7267652e6127293b2073756270726f636573732e72756e285b7379732e65786563757461626c652c27666f7267652f622e7079275d290a`;
  computed dynamic bytes are
  `696d706f72746c69622e696d706f72745f6d6f64756c65286e616d65290a` and the target remains awaiting
  human; and
- hidden surface replaces `/payload/inventory/counts/schema_surfaces` with 6; correction/no-progress/
  ceiling/closure cases use §§47–48, never the withdrawn hashes.

### 48.12 Expected oracle output

For every case the oracle emits exactly:

```text
{fixture_id,case_id,
 initial_files:[{path,bytes_hex,file_hash}],
 operation:{kind,pointer_or_command,value_or_hex,rehash:boolean},
 fault:NonEmpty|absent,
 expected_files:[{path,bytes_hex,file_hash}],
 forbidden_paths:PathRel[],expected_state:NonEmpty,
 reason_code:ReasonCode|absent,replay_files:[{path,bytes_hex,file_hash}]}
```

File arrays sort by path; forbidden paths sort bytewise; one case has one operation object or an
ordered operation array when its row names multiple operations. `bytes_hex=cf(record).hex()` and
`file_hash=hb(cf(record))`. The generator also asserts every embedded structured hash by recomputing
§44 from leaves outward. Committed fixture bytes must equal this output before production receives
decoded boundary values. Any import of production, schema or committed fixture expected data fails
the independence test.

## 49. Final systemic, boundary and adversarial closure

### 49.1 Systemic consistency chains

| Chain | Required final proof |
| --- | --- |
| A — requirement → pending card → resolution → application | ResolutionSemanticInput binds the stable requirement and answer, PresentationEvidence binds what the human saw, current binding/application bind physical records, and only an exact DecisionApplication in GateRecord changes state |
| B — obstruction → recovery → rebinding → resolution | One resolution semantic hash survives P0/P1 and R0/R1 physical relocation and recovery-N; generations are contiguous and conflicting semantic answers fail closed |
| C — offline authority → lineage → accepted resolution | MANIFEST legally carries bootstrap requirement/binding/application; the common resolver rejects pending-only, orphan, stale or unapplied records |
| D — review → GateRecord event → remediation → restart | CONTROL deltas and checkpoints reconstruct byte-identical current state; remediation is evidence-backed but remains unverified |
| E — human downgrade → reviewer escalation → current state | A human reclassification starts a severity epoch; a later higher reviewer observation escalates deterministically while a lower one cannot downgrade |
| F — current finding state → PASS | OPEN or ADDRESSED_AWAITING_REVIEW blocker denies PASS; only independent absence produces INDEPENDENTLY_VERIFIED and closure remains human-only |
| G — current state → no-progress → ceiling | Logical-lineage fingerprints and correction count survive recovery; progress is computed before the unchanged 2-correction ceiling |
| H — final models → independent oracle | Five surface constructors, embedded decision/finding objects, explicit test-only lineage state, VFS operations, mutations and expected hashes instantiate §§44–47 without production imports |

Failure of any link is `HASH_MISMATCH`, `AUTHORITY_CONFLICT`, `MISSING_EVIDENCE` or
`FORBIDDEN_TRANSITION` as specified; no chain may synthesize PASS.

### 49.2 Five-surface audit

Exactly five persisted/external surfaces remain:

| Surface | Producer → consumer | Final authority and lifecycle |
| --- | --- | --- |
| GateRecord | human/core/inventory/collector/recovery → all | sole state authority; includes PUBLICATION_INTENT, RECOVERY_ROOT, DecisionBinding/Application and embedded FindingEvent/RemediationEvidence; append-only CF/H; full lineage validation |
| ExecutorExchange | core grant + executor result + I/O observation → collector/core | execution result only; committed intent before non-reconstructable final; no PASS/closure |
| RunRecord | collector → reviewer/core | Git/command/runtime/tool authority; committed intent; 17 commands; raw HB plus surface H |
| ReviewerExchange | core packet + reviewer result + I/O observation → core/human | semantic/finding event authority; committed intent; no correction/closure |
| HumanDecisionRecord | human boundary/core pending representation → core/human | separate immutable PendingDecisionCard, DecisionResolution and conflict/closure cards; never state authority without GateRecord application |

Every surface uses exact model fields incorporated from §§35 and replaced by §§44–47, CF persisted
bytes, §44 hashes, receipt/pre-persist validation, create-only publication, deterministic ordering,
provenance, append-only lifecycle and §45 recovery. Schema/model error, hash error, stale authority,
partial write or obstruction fails closed. PUBLICATION_INTENT and RECOVERY_ROOT are GateRecord
variants; conflict cards and rebound decisions are HumanDecisionRecords. No sixth surface, pointer,
registry, locator file, sidecar, module, adapter, role or dependency exists.

### 49.3 Adversarial dispositions

The following final results are mandatory:

- persisted LF omitted/duplicated → MALFORMED_BOUNDARY; LF included in H or wrong domain →
  HASH_MISMATCH;
- missing/invalid required intent → FORBIDDEN_TRANSITION/HASH_MISMATCH; matching replay idempotent;
- crash after intent → intent gate authoritative and target replayed without actor reinvocation;
- fresh consumer without memory → derives discovery key/candidates from GateRecord only;
- candidate collision/invalid root → preserved and next exact ordinal; first absent forbids higher;
- recovery depth greater than one → same logical lineage, inherited counts/ledger/progress;
- decision obstruction → same identity, generation+1; orphan/inactive/wrong-hash record rejected;
- accepted old-segment resolution → effective only through explicit active binding/application;
- pending-only state returns PENDING; a separately persisted accepted resolution remains evidence until
  application; two different semantic answers fail AUTHORITY_CONFLICT without filesystem tie-break;
- resolution-path obstruction retains one byte-identical semantic answer through intent/recovery and
  rejects a second answer;
- severity escalation/blocking latch → conservative current state; downgrade/clear needs HumanDecision;
- remediation without complete evidence → remains OPEN; correction self-verification forbidden;
- recurrence → deterministic occurrence; empty review never erases; malformed history blocks;
- no-progress and ceiling operate after complete-lineage derivation and survive recovery.

### 49.4 Whole-document supersession audit

The entire EB was searched for terminal LF, hash preimage, one-argument `H(`, canonical bytes,
source tuple ordering, same/canonical decision path, recovery UUID, intended record hash,
PUBLICATION_INTENT, decision locator, severity, blocking, remediation evidence, current finding state
and fixture mutations. Sections 21 and 34–42 are labeled historical/withdrawn. Their contradictory
hash, recovery locator, decision lookup, finding evolution and fixture statements have no normative
force. Sections 44–48 explicitly incorporate only named unchanged structures, parser rules and raw
fixture inputs. No competing normative answer remains.

## 50. Final budget, scope and CORR-015 state

The corrected design retains four new production modules plus unchanged `forge/__init__.py`
attribution, one executor adapter, one reviewer adapter, five schema surfaces and zero new dependency.
Expected allocation remains core 330, model 420, inventory 360 and I/O 550 = 1,660 new production
LOC, with 140 LOC below the 1,800 hard maximum. PUBLICATION_INTENT, discovery-key calculation,
decision binding and finding derivation refine responsibilities already allocated to core/model/I/O;
they add no module or surface. Implementation inventory must continuously prove the limit and stop
`BUDGET AUTHORITY REQUIRED` on contrary concrete evidence. `EB006-FR-07` is not reopened.

Only EB-006 and necessary documentation index/project-memory text may change in CORR-015. Runtime,
tests, schemas, committed fixture implementation, dependencies, versions, Audio Recorder,
FAL-002 specification, FAL-001 and unrelated artifacts remain unchanged.

`CORR-015-01`, mapped to `EB006-IR6-02`, is `ADDRESSED — AWAITING INDEPENDENT REVIEW`. This is only
the correction agent's remediation claim: `EB006-IR6-02` remains open and is not independently
verified, closed, accepted or PASS. IR7's independent verification of `CORR-014-01`/
`EB006-IR6-01` is preserved and not reopened; that finding is not closed.
FAL-002 remains `NOT AUTHORIZED`; no runtime implementation occurred. FAL-001 remains permanently
`TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2. The only next gate is a fresh
independent read-only Standard-Assurance Review against the dedicated CORR-015 commit.
