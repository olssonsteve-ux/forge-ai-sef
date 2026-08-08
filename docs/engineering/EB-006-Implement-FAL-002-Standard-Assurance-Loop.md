# EB-006 — Implement FAL-002 Standard Assurance Bounded Engineering Loop

Status: `AWAITING HUMAN REVIEW`

Date: 2026-08-01

Owner: Chief Architect

Decision basis: `HD-FAL-006`

Correction authority: `HD-FAL-007`, `HD-FAL-008`, `HD-FAL-009`

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

## 21. Normative implementation-complete conventions

Sections 21–27 refine sections 3–20 and control wherever earlier shorthand is less specific.
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

Besides the common envelope, exact fields are `record_id=run_id`, `execution_id`, `ordinal:int 0..9999`,
`repository`, `commands`, `diff`, `build`. `repository` is exactly `{root:".",branch,
baseline_head:hex40|hex64,final_head:hex40|hex64,status:string[],changed_paths:PathRel[]}`. `commands`
contains exactly 13 entries in §24 order. Each is `{command_id,phase,argv:string[],cwd:PathRel,
environment_keys:string[],started_at,ended_at,exit_code:int|null,termination:
EXITED|TIMEOUT|INTERRUPTED|SPAWN_ERROR,stdout_sha256,stderr_sha256,stdout_text,stderr_text,
redaction_count:int>=0,parser_version:1,parsed:Json,classification:
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
`{decision_card:{question,domain,source_record_ids,source_hashes,allowed_choices}}`. RESOLUTION
requires ACCEPTED or DECLINED and payload `{resolves_decision_id,chosen_value:string|absent,
rationale}`; chosen value is absent iff declined. CLOSURE requires ACCEPTED and payload
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
| executing | `COLLECT_COMPLETE` | collector; all 13 command entries | run, gate | evidence_ready | missing/malformed → blocked gate |
| evidence_ready | `START_REVIEW` | core; packet and independence precheck | gate with review packet | reviewing | failed separation → card, awaiting_human gate; invoke only after durability |
| reviewing | `REVIEW_PASS` | reviewer; complete valid PASS | reviewer result, eligibility gate | accepted | blocking/missing → blocked gate |
| reviewing | `REVIEW_CORRECTION` | reviewer; CORRECTION_REQUIRED | reviewer result, gate | correction_required | count=2 → ceiling event |
| reviewing | `REVIEW_BLOCKED` | reviewer; BLOCKED/INCONCLUSIVE | reviewer result, gate | blocked | no automatic retry |
| reviewing | `REVIEW_INTERRUPTED` | recovery; no durable result | gate | awaiting_human | accepted retry uses next ordinal, count unchanged |
| correction_required | `START_CORRECTION` | core; count<2, allowed paths | executor request, gate | executing | ordinal/count increment once; failure blocked |
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

## 23. Adapter lifecycle and Standard-Assurance separation

Core creates requests; I/O persists executor request in the executing gate and reviewer packet in the
reviewing gate; core invokes only after that gate is durable. Adapters create no ID, record or
transition and only return a value. Model validates, I/O create-persists the complete exchange once
after return, and core transitions. The request copied into the exchange must be byte-identical to
the gate-embedded request; no null-result exchange file is ever persisted.
Both roles are externally non-idempotent and called at most once per invocation ID. Same-ID replay
reads a durable result without adapter call. Missing result after interruption requires human retry
and a new ordinal/ID. Changed/stale input, different duplicate result, timeout or exception follows
§22 and §25. Executor/reviewer audit evidence is request/result hashes, invocation ID/times, adapter,
principal, process and context IDs, and resulting gate IDs.

A fresh Standard-Assurance review context is newly initialized for one review with
`context_id=H("review-context:"+review_id+":"+run_record_hash)[:24]`, no prior executor/reviewer
messages or state, and input limited byte-for-byte to the packet plus fixed adversarial instructions.
It receives no executor prompt, transcript, private reasoning, credentials, mutable workspace handle
or correction authority. This is structural Standard Assurance, not High-Assurance isolation.

`reviewer_execution` is exactly `{invocation_id:review_id,context_id,role:"reviewer",adapter_id,
principal_id,process_id:int,fresh_context:true,read_only:true,received_packet_hash,instructions_hash,
started_at,ended_at:string|absent}`. Executor invocation records equivalent identity fields. Required
separation is different `principal_id`, `adapter_id` and `context_id`; process IDs may match but are
truthfully recorded. Equality of a separated value, missing provenance, inherited executor-only field
or writable capability creates a deterministic independence card and `awaiting_human` before reviewer
call. No PASS/eligibility follows. Executor mutates only executor result; reviewer mutates only review
result. Cancellation/interruption produces no result and uses the retry rule above.

## 24. Exact collector execution contract

Common contract: resolve `git` from PATH and Python as exact `sys.executable` 3.14; verified root cwd;
closed stdin; exact environment keys from §15 with all other inheritance removed. On timeout terminate
the process group, wait five seconds, then kill. This stdlib design cannot enforce network isolation;
an externally verified offline precondition is required or a card/`AWAITING_HUMAN` occurs before any
command. Redact stdout/stderr bytes before decode/hash by replacing case-insensitive UTF-8 matches of
`(token|password|secret|api[_-]?key|authorization)=` through next whitespace/NUL with `<REDACTED>`.
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

Order is the table order and execution is sequential. This replaces ambiguous `GIT-HEAD`; RunRecord
therefore has 13 entries. The manifest is exactly gate 0 bytes at §3 path: read, §21.1 validate,
require manifest variant, canonical-reserialize byte-identically, verify hash, then pass that literal
path in argv. No actor summary substitutes for collector evidence.

## 25. Deterministic create-only recovery

Authoritative create is validate → exclusive create final path → write all canonical bytes → flush/
fsync → close → reread/hash → directory fsync. Final paths are never overwritten, deleted, truncated
or renamed. A partial final path is preserved forever and makes that physical series terminal; no
later gate may skip its occupied sequence. Operational disposition is `AWAITING_HUMAN` derived from
the last verified predecessor plus corrupt-tail diagnostic, not a fabricated gate. Only a later Human
Decision could authorize a successor series carrying the complete correction count/history; this
brief does not authorize one.

| IP | Possible filesystem and authority | Allowed recovery, reuse and resulting state |
| --- | --- | --- |
| IP-01 | no new bytes; prior chain authoritative | revalidate; same path/sequence/ordinal reusable; invalid → BLOCKED diagnostic |
| IP-02 | no final path; prior chain authoritative | retry exclusive create using same IDs/path; no next ordinal |
| IP-03 | final path contains any prefix; non-authoritative | preserve bytes/path; no reuse/delete/truncate/overwrite/next sequence/ordinal; terminal AWAITING_HUMAN diagnostic |
| IP-04 | complete but unconfirmed file | reread; exact canonical bytes/hash adopts once with same IDs; otherwise IP-03 |
| IP-05 | confirmed record authoritative | same-hash replay reads it; continue next required record; no duplicate append |
| IP-06 | earlier record durable, later path absent | replay orchestration using same later ID/path; absent adapter result requires human retry/new ordinal, count unchanged |
| IP-07 | target already exists | same hash idempotent; different hash preserves claim and creates conflict card/gate if paths free, else terminal diagnostic |
| IP-08 | gap or predecessor mismatch | preserve all; no append/path/sequence reuse; terminal AWAITING_HUMAN diagnostic |
| IP-09 | derived temp may be partial | temp name `current.{gate_record_hash}.tmp`; same valid hash may replace current; partial/different temp is preserved/ignored and next gate uses its own hash temp; authoritative state unchanged |

Derived temp files are internal cache material, not boundary payloads. Atomic replace may replace only
`current.json`. Authority-conflict order is card then gate. Card ID is
`DC-{series_prefix}-{sequence}-{H(sorted(source_id+source_hash pairs))[:12]}`. Same conflict always
derives the same ID. Crash before card durability recreates it; after card durability/before gate,
replay adopts same-hash card then creates gate. Partial card/gate invokes IP-03 and no second card.
Both sources/hashes are in card and checkpoint; history never changes.

Closure order is accepted closure decision then closed gate. Crash between them adopts decision and
appends deterministic closed gate. A partial decision/gate leaves the last verified accepted gate
authoritative and cannot claim closure.

## 26. Literal scenario-fixture contracts

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
above. Future fixture content must spell out resulting canonical JSON and hashes; tests compare literal
bytes without production constants. IP-01–IP-09 use the same constants and assert every §25 outcome.
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
