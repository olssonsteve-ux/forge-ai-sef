# FAL-002 Implementation Review Handoff

## FAL002-CORR-002 correction handoff — 2026-08-09

Status: `Implemented — correction addressed — awaiting independent implementation review`.

Starting from committed `HD-FAL-023` baseline
`3082a8ae731b670cb6a77af754cea28527c6b65d`, objectives `FAL002-CORR-002-01` through `-04` are
`ADDRESSED — AWAITING INDEPENDENT REVIEW`. Mapped `FAL002-IR1-01`, `FAL002-IR1-03`,
`FAL002-IR1-04` and `FAL002-IR1-05` remain open. Independently verified `FAL002-IR1-02`,
`FAL002-IR1-06` and `FAL002-IR1-07` remain verified but not closed. No verification, closure or
FAL-002 acceptance is claimed by the implementation agent.

The existing orchestrator now stages each COMMITTED exchange/run, persists an exact
PUBLICATION_INTENT and final-publishes only through the authoritative intent route. The public
create-only API is GateRecord-only; its raw primitive remains internal. Publication resolves the
persisted intent tip and exact predecessor/slot/stage/target/hashes. RECOVERY_ROOT publication and
discovery/adoption validate the actual canonical predecessor tip, logical origin and carried state.
Decision resolution cross-checks requirement, card, binding, presentation, resolution, legal choice
and application; persisted pending/applied state feeds eligibility. Runtime/I/O rebuilds reviewer
observations despite callback tampering. Deterministic progress snapshots yield `NONE` for unchanged
correction state and stop before another executor invocation.

### Publication call-site audit

| Module/function | Classification and validated route | Bypass possible |
| --- | --- | --- |
| `fal002.persist_transition` | GateRecord-only publication; RECOVERY_ROOT validates persisted predecessor | no COMMITTED-surface bypass |
| `fal002.publish_committed` | stage → persisted intent → `publish_staged` | no |
| `fal002_io.publish_create_only` | rejects all four non-gate surfaces | no |
| `fal002_io.publish_staged` | sole COMMITTED route; resolves authoritative intent tip | no |
| `fal002_io._publish_raw_create_only` | internal byte primitive; only the two policy functions call it | no operational caller |

Adversarial results: no-intent HumanDecisionRecord, ExecutorExchange, RunRecord and ReviewerExchange
all reject with absent targets; exact intent succeeds and corrupt stage rejects; phantom, wrong-hash
and wrong-series recovery predecessors reject; valid predecessor/recovery depth three and sealing
pass; Decision B resolution rejects for Decision A; valid same-decision online/offline resolution
agrees; persisted pending/applied states differ correctly; reviewer provenance tampering is replaced;
and unchanged correction state derives `NONE` then stops before retry.

Final inventory: **3,316/3,400 LOC**, four modules, two adapters, five surfaces and zero new direct or
transitive dependencies. Verification: 40 focused FAL-002 tests and 182 full tests pass; Ruff,
format, schema check and inventory pass. Packaging was not run because it is prohibited.

Correction evidence addresses the implementation causes of STOP #9/#13 without weakening their
contracts. Only the required fresh independent implementation review may verify the four findings.
Architecture, FAL-002, EB-006 and HD-FAL-021/022/023 remain unchanged. The exact next permitted step
is **one fresh independent implementation review of the corrected FAL-002 baseline**.

## Independent Implementation Review II and CORR-002 authority — 2026-08-09

Independent Implementation Review II of corrected HEAD
`92c16e9e7e2b6871a65bd545be2e3d0dce88e5fc` returned
`FAIL — IMPLEMENTATION CORRECTION REQUIRED`. It independently verified `FAL002-IR1-02`,
`FAL002-IR1-06` and `FAL002-IR1-07` without closing them. `FAL002-IR1-01`, `FAL002-IR1-03`,
`FAL002-IR1-04` and `FAL002-IR1-05` remain `OPEN — BLOCKING`; no new finding was created; and
HD-FAL-021 STOP #9/#13 remain triggered.

`HD-FAL-023` is `ACCEPTED` and authorizes `FAL002-CORR-002-01` through `-04` only for those four
residuals. Architecture remains frozen at four modules, two adapters, five surfaces and zero new
dependencies. Current governed production LOC is 2,998; the explicit hard maximum is 3,400, with an
expected corrected total near 3,208. FAL-002 remains `Implemented — correction required`, unaccepted
and unclosed. The next permitted step is to execute CORR-002 against the committed HD-FAL-023
baseline, then perform one fresh independent implementation review.

## FAL002-CORR-001 correction handoff — 2026-08-09

Status: `Implemented — correction addressed — awaiting independent implementation review`.

Under `HD-FAL-022`, objectives `FAL002-CORR-001-01` through `-07` are
`ADDRESSED — AWAITING INDEPENDENT REVIEW`. The seven `FAL002-IR1-01` through `-07` findings remain
open; this handoff verifies neither findings nor FAL-002 acceptance/closure.

The corrected implementation adds the executable sequential loop, the exact 17-command collector,
two concrete authority-limited adapters, exact shared runtime/schema models, intent-bound staged
publication, recovery predecessor validation and sealing, authoritative RunRecord/reviewer binding,
resolvable criterion evidence, and occurrence-local recurrence with prior-terminal linkage. Tests
cover the real orchestrator, malformed nested records, schema/runtime agreement, missing or corrupt
publication authority, recovery-N, wrong predecessor, transient I/O, sealed predecessor append,
fabricated evidence/run hashes, exact remediation and recurrence after human closure.

Corrected governed inventory: four production modules, 2,998/3,000 counted production LOC, one
executor adapter, one reviewer adapter, five generated persisted/external surfaces, and zero new
dependencies. Packaging remains prohibited and was not run. The exact next permitted step is one
fresh independent implementation review of the corrected FAL-002 baseline.

Status: `Implemented — awaiting independent implementation review`

Date: 2026-08-09

## Governing work

- capability: `docs/capabilities/FAL-002-Standard-Assurance-Bounded-Engineering-Loop.md`;
- implementation contract: `docs/engineering/EB-006-Implement-FAL-002-Standard-Assurance-Loop.md`
  at planning baseline `88e53fcbaa31ace83740699cd531f74f2d7e88b6`;
- implementation authorization: `HD-FAL-021`, `ACCEPTED`;
- authorized starting HEAD: `80e47375841e4c6faf333145e5a1462c0c3ec12a`; and
- planning assurance: IR10 `PASS — RECOMMEND IMPLEMENTATION AUTHORIZATION`.

The implementation commit is the commit containing this handoff. Implementation is not independently
reviewed, accepted, closed, released or included in an album capability.

## Implemented production inventory

| Module | Responsibility | Counted production LOC |
| --- | --- | ---: |
| `forge/fal002.py` | sequential state machine, correction/no-progress, decision resolution, eligibility and human closure | 355 |
| `forge/fal002_model.py` | CJ/CF, H/HB, closed boundary validation, identities, findings, eligibility and schema generation | 972 |
| `forge/fal002_inventory.py` | deterministic AST/LOC/module/adapter/surface/dependency inventory | 191 |
| `forge/fal002_io.py` | create-only persistence, staging, recovery probing, collection and the two adapters | 259 |
| **Total** | **four new production modules** | **1,777 / 1,800 maximum** |

The count is the deterministic `forge.fal002 inventory` result after final formatting. Test and
documentation lines are excluded from the governed production count.

## Boundary and adapter inventory

Exactly five generated persisted/external boundary schemas exist:

1. `fal002.gate-record.v1`;
2. `fal002.executor-exchange.v1`;
3. `fal002.run-record.v1`;
4. `fal002.reviewer-exchange.v1`; and
5. `fal002.human-decision.v1`.

`PUBLICATION_INTENT`, `RECOVERY_ROOT`, decision objects, finding objects and progress state remain
embedded in GateRecord or the other four authorized surfaces. `current.json` is an exact replaceable
GateRecord cache and is never authority. No sidecar, active-series pointer, recovery index or hidden
finding/decision store exists.

`forge/fal002_io.py` defines exactly one `FAL002ExecutorAdapter` protocol and one
`FAL002ReviewerAdapter` protocol. Inventory reports one adapter per role. No new dependency was
added; production imports only Python stdlib and the four FAL-002 modules. No FAL-001 runtime module
is imported.

## Contract evidence

- `CJ` emits deterministic strict UTF-8 canonical JSON without LF; `CF` appends exactly one LF.
- `H` accepts only the reviewed domain registry and hashes the canonical `{domain,value}` object;
  `HB` hashes exact bytes.
- Runtime validation rejects unknown root and governed nested fields, invalid primitives, malformed
  canonical files and payload/record hash mismatch.
- Generated draft-2020-12 schemas bind exactly the five roots and closed nested boundary objects;
  generation/check is deterministic.
- Authoritative files use create-only durable publication: absent creates, identical bytes adopt,
  and different bytes fail without overwrite.
- COMMITTED outputs support durable staging and exact-byte/hash replay after publication intent.
- Recovery uses the reviewed discovery hash, fixed UUIDv5 namespace, ordinal probing without
  directory enumeration and sequence-zero RECOVERY_ROOT; recovery depth three is tested.
- Decision requirement and semantic resolution hashes exclude relocatable physical bindings;
  GateRecord-owned binding/application and current-lineage lookup reject stale or conflicting state.
- Finding events are immutable, globally ordered and predecessor-bound; replay recomputes checkpoint,
  severity, blocking and current state. Remediation remains distinct from independent absence.
- PASS rejects pending decisions, incomplete criterion evidence/rationale and unresolved CRITICAL or
  blocking findings. Empty findings create no verification event.
- No-progress requires changed evidence plus independent resolution; remediation alone is not
  progress. The two-correction ceiling is retained.
- Closure requires a separate accepted HumanDecisionRecord bound to the exact eligible GateRecord.

## Tests and adversarial coverage

Four new test modules add 30 tests covering canonical/hash literals and malformed bytes, closed
models, schema drift, deterministic inventory, adapter authority, state/correction flow, human-only
closure, create/adopt/conflict persistence, committed staging, recovery-1/2/3, obstructed recovery
candidates, semantic resolution relocation, stale binding, finding remediation/absence/replay,
CRITICAL/addressed eligibility, no-progress and the correction ceiling.

Adversarial cases include duplicate JSON fields, float/BOM/noncanonical/LF input, unknown root and
nested fields, corrupt hashes, conflicting create-only bytes, wrong staged hash, malformed lower
recovery candidate, stale decision application, invalid event ordinal, historical addressed blocker
with empty review and correction ceiling.

## Verification results

- focused FAL-002 tests: `30 passed in 0.34s`;
- full repository tests: `172 passed in 6.62s`;
- `python -m ruff check .`: passed;
- `python -m ruff format --check .`: passed, 20 files already formatted;
- `git diff --check`: passed;
- `python -m forge.fal002 schemas --output-root schemas/fal002 --check`: passed, five hashes emitted;
- deterministic inventory: `PASS`, four modules, 1,777 LOC, 1/1 adapters, five surfaces, zero new
  direct or transitive dependencies, no unresolved target;
- Project Memory Health: `OK`; and
- Repository Status before commit: expected dirty-tree warning only.

The known Version Consistency warning remains: pyproject `0.5.0` versus latest tag `v0.4.1`. No
version or packaging change was made.

## Scope and stop-condition audit

No stop condition was crossed. The implementation adds no sixth surface, dependency, fifth module,
third adapter, mutable authority pointer or lineage reset. It does not change FAL-002, EB-006,
HD-FAL-021, architecture decisions, FAL-001, Audio Recorder, album artifacts, versions, packaging or
release state. Production LOC is 23 below the 1,800 ceiling.

## Review gate

FAL-002 implementation is `Implemented` and awaits a fresh independent implementation review against
FAL-002, EB-006, HD-FAL-021, applicable Human Decisions, this handoff, the actual code/tests and the
authorized scope/budget. Implementation completion is not acceptance or closure. FAL-001 remains
permanently `TERMINATED BLOCKED`, correction count 2/2.
