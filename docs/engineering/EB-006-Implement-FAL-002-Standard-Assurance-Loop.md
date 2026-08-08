# EB-006 — Implement FAL-002 Standard Assurance Bounded Engineering Loop

Status: `AWAITING INDEPENDENT REVIEW`

Date: 2026-08-01

Owner: Chief Architect

Decision basis: `HD-FAL-006`

Correction authority: `HD-FAL-007`, `HD-FAL-008`, `HD-FAL-009`, `HD-FAL-010`, `HD-FAL-013`

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

## 21. Historical canonical conventions (superseded where section 35 differs)

Sections 21–27 record the pre-CORR-011 canonical design. Sections 34–42 are the sole final authority
where they add, replace or conflict with this text; no implementer may select an older competing
shape.
`Json` means null, boolean, signed base-10 integer, UTF-8 string, ordered array, or object with string
keys. Floats, duplicate keys, NaN, infinity and lone surrogates are invalid. `Timestamp` is UTC
`YYYY-MM-DDTHH:MM:SS.ffffffZ`; `Sha256` is 64 lowercase hex characters; `PathRel` is a normalized
`/`-separated repository-relative path without empty, `.`, `..`, drive or NUL segments. Set-valued
arrays sort by UTF-8 bytes and reject duplicates. Every unqualified string field below is one required
`NonEmpty` trimmed string. Every unqualified array is required with cardinality 1..65535; only
`changed_paths`, `status`, `findings`, `finding_ids` and `source_record_ids/source_hashes` may be empty.
An explicitly optional/absent field has cardinality 0..1. Every object is required exactly once.

Canonical serialization is RFC-8259 JSON in UTF-8, keys sorted by UTF-8 bytes, separators `,` and
`:`, no insignificant whitespace and one terminal LF. `H(x)` is lowercase SHA-256 of canonical bytes.
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

## 34. CORR-011 authority, precedence and traceability

`HD-FAL-012` is the binding recovery architecture and `HD-FAL-013` authorizes this single bounded
correction. Sections 35–42 are one inseparable final contract. They replace every conflicting exact
field list, command count, fixture rule, recovery rule, finding rule and coverage claim in sections
3–33. Earlier text remains historical rationale only where it differs. Unchanged requirements remain
in force. The five boundary roots and their schema IDs remain exactly §3.

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

## 35. Final canonical boundary model

### 35.1 Common rules and final payload union

Section 21's JSON grammar, canonical UTF-8 serialization, hash algorithm, validation order, schema
version and unknown-field rejection remain final. A string declared `NonEmpty` is valid only when it
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

## 36. Authoritative successor recovery lineage

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

## 37. Conflict-card identity and authority

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

## 38. Collector versions and offline authority

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

## 39. Complete-lineage findings and deterministic no-progress

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

## 40. Independent reproducible fixture oracle

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

## 41. Final boundary, consistency and adversarial closure

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

## 42. Budget, scope and final correction state

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
