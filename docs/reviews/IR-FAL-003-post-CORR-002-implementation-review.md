# IR-FAL-003 — FAL-002 post-CORR-002 independent implementation review

Date: 2026-10-11. Role: independent review agent; no implementation edits, commits or closure.
Decision: **FAIL — residual blocking recovery authority defect independently reproduced**.
Intended repository destination: `docs/reviews/IR-FAL-003-post-CORR-002-implementation-review.md`.
Existing IR-FAL-001/002 filenames concern the older FAL-001 review; 003 is the next unused file identifier.

## Verified baseline and scope

Actual repository: `C:\Users\olsso\Documents\forge-ai-sef`, branch `main`, HEAD
`e8d8ed05d23e5229109139836101d036fb27a7e1`, exactly the requested correction baseline.
Initial working tree clean and staging empty. No reset, discard, checkout or commit occurred.
Audio-Recorder is a separate repository and did not contain this Forge runtime.
During review the coordinating agent added ADR0018 and six documentation-only updates;
production runtime remained at the exact reviewed HEAD. Those concurrent edits are identified below.

This record is a bounded blocking review, not a claim that every 5,423-line EB-006 clause or
all integrated adversarial scenarios were exhausted. A reproduced blocker prevents PASS.
Actual original independent implementation reviews I/II are absent from `docs/reviews`;
their binding findings and disposition are incorporated in HD-FAL-022/023. This limits direct
comparison with the original unpublished falsification details and must remain visible.

## Authority examined

CONSTITUTION, AI_ENGINEERING_CONDUCT, current AI_HANDOFF/PROJECT_STATE, HD-FAL-022,
HD-FAL-023, FAL-002 implementation-review handoff; applicable EB-006 storage, adapter,
verification, recovery and counting sections; HD-FAL-012/014 sealing requirements.
Code inspected: four fal002 production modules (focused on orchestration, publication, decision
resolution and reviewer observation), focused flow/recovery/inventory/model tests and correction
history. This is not an exhaustive read claim for every historic planning artifact.
No governing contract was revised as part of this review.

## Structural verification

Independent AST-assisted physical-line calculation excludes blank/comment-only lines and
standalone docstrings; it does not call the runtime inventory counter:

| Production module | LOC |
| --- | ---: |
| forge/fal002.py | 876 |
| forge/fal002_inventory.py | 158 |
| forge/fal002_io.py | 476 |
| forge/fal002_model.py | 1,806 |
| Total | 3,316 / 3,400 |

Four actual modules, two adapter classes (executor/reviewer), five schema/publication kinds
(GateRecord, ExecutorExchange, RunRecord, ReviewerExchange, HumanDecisionRecord).
Zero new dependencies: correction does not change pyproject.toml and inspected FAL imports use
stdlib and the four modules. Existing project dependency is Typer; it is not a FAL addition.
The runtime inventory independently executed and agreed. Correction commit changes four production
modules, three focused test modules and four handoff/memory documents. No unrelated capability or
structural expansion was found in that correction's file scope. History inspected includes original
implementation 36ea966, CORR-001 b778e98, carry-forward fixture 92c16e9, authority 3082a8a,
and CORR-002 e8d8ed0.

## Corrected finding assessment

| Finding | Original defect / correction evidence | Assessment |
| --- | --- | --- |
| FAL002-IR1-01 | Canonical loop lacked complete integrated publication, decision/progress and provenance authority. Current run_engineering_loop uses publish_committed, decisions_pending and correction_disposition; focused integrated tests pass. Persisted COMMITTED authority still permits the IR1-04 bypass below. | PARTIALLY ADDRESSED; not closed |
| FAL002-IR1-03 | COMMITTED records could bypass matching persisted intent. Public publish_create_only now rejects all non-gate surfaces; publish_staged checks persisted tip, predecessor, slot, stage, target and hashes. Positive/negative publication tests pass. | Direct no-intent failure mode independently verified eliminated; closure withheld pending integrated recovery repair and remaining review |
| FAL002-IR1-04 | Recovery predecessor/carry-forward/sealing were not authoritative. Phantom/hash/series tests and recovery depth three pass, but sealing covers ordinary GateRecords only. | OPEN — BLOCKING, reproduction below |
| FAL002-IR1-05 | Run/reviewer provenance and decision-chain cross-binding were insufficient. resolve_decision now compares identity, requirement, pending card, binding, presentation and resolution; invoke_reviewer rebuilds observed fields; cross-decision and applied/pending tests pass. | PARTIALLY ADDRESSED / closure not asserted by this bounded review; full freshness and failure-path verification remains |

## Material residual: sealed predecessor accepts COMMITTED publication

Mapped to existing FAL002-IR1-04, not a new architecture finding.
Location: `forge/fal002_io.py`, `publish_staged` (line 212 onward); compare
`publish_create_only` calling `_assert_series_unsealed` and HD-FAL-014 item 4 / HD-FAL-012 item 5.

Reproduction uses the existing fully validated `test_publication_requires_exact_intent_and_target`
fixture up to its final publication. Before calling publish_staged, publish a valid
`recovery_root(intent_gate)` through the real create-only API. Then publish the staged pending
decision into the predecessor. Actual result:

```text
SEALED_PREDECESSOR_PUBLICATION=CREATED
target_exists=True
```

Expected: reject sealed predecessor without creating final target. The old intent remains the old
series tip, so every existing publish_staged check succeeds. It never calls the seal guard.
Standalone script: `repro-fal002-sealed-publication.py` alongside this record. Run from Forge with
`python <script> --root <new writable temporary directory>`; it exits 1 when the defect reproduces.
The existing depth-three test exercises only an ordinary GateRecord append. All focused tests can
pass while this failure remains. Repair must cover every COMMITTED surface and identical adoption
semantics, then independently re-review sealing without adding stores or weakening recovery authority.

## Frozen findings and test assessment

IR1-02, IR1-06 and IR1-07 are not reopened. No concrete contradictory regression established;
schema, malformed-boundary, criterion-evidence, recurrence and severity tests pass. Verification
is not a human closure action. Focused tests exercise real filesystem behavior and external
record results, but recovery sealing coverage omitted the COMMITTED path identified above.
Existing helpers construct records through implementation functions; the independent negative
composition above demonstrates why passing fixtures alone cannot establish contract completeness.

## Verification results

- Ruff lint: PASS; format: PASS, 20 files already formatted.
- Five-schema generation check: PASS.
- Inventory: PASS; independent LOC agrees at 3,316.
- Working/staged `git diff --check`: PASS (line-ending warnings only).
- Full suite: **181 passed, 1 failed in 12.35s**. All 40 FAL-focused cases passed in this run.
- Sole full-suite failure: legacy `test_audio_recorder_baseline_fixture_is_unchanged` asserts
  Audio-Recorder has an empty working tree; authorized concurrent album work makes that false.
  Do not reset or hide the user's product work to satisfy this obsolete environment assumption.
- Execution used process-local Git safe.directory entries for the two known repositories and a
  Windows extended-length writable temp path. Earlier attempts exposed sandbox temporary-file,
  dubious-ownership and long-path failures; those were environmental, not evidence of FAL correctness.
- The attempted elevated pytest command was interrupted while approval was pending; no successful
  elevated test result is claimed.
- No packaging/release/system publication was performed. No full manual platform acceptance claimed.

## Separate documentation consistency assessment

ADR0018 plus Conduct, implementation protocol, lifecycle, PROJECT_STATE, PROJECT_BRAIN and
AI_HANDOFF additions reviewed independently: PASS for internal consistency. They retain explicit
FAL contracts, budgets, STOP boundaries, independent review and human closure; consolidation is
conditional on no stricter applicable record requirement. No runtime contract change is authorized
by that text. Optional improvement: replace duplicated memory paragraphs with role-specific short
links. No productivity measurement is claimed.

## Decision and next governance step

FAL-002 remains implemented, unaccepted and unclosed; IR1-04 is still blocking. Implementation
ready to commit: **NO**. FAL-002 ready to close: **NO**. Corrections made during review: none.
Recommended commit message: none for this failing baseline. The authorized coordinating agent
must record appropriate bounded correction authority, repair sealed COMMITTED publication and
add a regression, then obtain fresh independent re-review and complete remaining contract checks.
Do not present this record as a completed exhaustive PASS assessment of the other residuals.

## Supplemental integrated review — 2026-10-11

Further focused investigation establishes additional concrete residuals under existing IR1-01/05.

**IR1-01: adapter exception checkpointing remains OPEN.** Using the existing valid
`_ready_runtime_root` fixture, an executor callback raises
`TimeoutError('token=REVIEW_SENTINEL')`. Actual result was the unchanged raw exception with that
message; latest persisted gate remained `executing` / `EXECUTION`. EB-006 section 16 requires
timeout to BLOCKED and other exceptions redacted, hashed and checkpointed; interruption must
checkpoint and return AWAITING_HUMAN. The canonical loop has no applicable exception handler.
The reviewer invocation has the same unguarded structure. The sentinel is synthetic, not a secret.

**IR1-05: offline decision authority remains OPEN.** Existing passing
`test_real_orchestrator_persists_executor_run_reviewer_and_gate` constructs `_ready_runtime_root`
with literal fabricated offline hashes, locator `decisions/offline.json`, and empty default
decision requirement/binding/application arrays. It persists no corresponding accepted offline
decision, yet reaches eligible=True. Final EB-006 section 46.5 requires complete section 46.4
resolution of applied OFFLINE_EXECUTION/AUTHORIZE_OFFLINE authority before every spawn. The loop
checks only non-None offline metadata, after executor invocation; pending decisions are resolved
after review. This is directly observable contract failure, not a claim about cryptographic trust.

**IR1-05: freshness observation remains insufficient.** EB-006 section 29 specifically requires
a newly constructed reviewer adapter object after executor return. The orchestrator accepts and
uses the reviewer object constructed before executor invocation; it never creates a fresh object.
The existing passing integrated test demonstrates that ordering, while the resulting record
claims fresh_context_verified=True. Same process/module is allowed by the contract; this finding
does not ask for stronger process isolation.

**Recovery pending input is not handled safely.** Publish a valid origin and its valid
recovery_root through real APIs, then invoke run_engineering_loop with that root: raw
`KeyError: 'manifest'` occurs at the unconditional chain[0].payload.manifest access. The root
has state awaiting_human and no accepted resume decision. Expected behavior is a bounded pending
disposition, not automatic resume. This reproduction does not assert that auto-resume is allowed.
Accepted resume requires a HumanDecisionRecord bound to the active root choosing
AUTHORIZE_RECOVERY_RESUME, preserving recorded pre-obstruction state and all carry-forward.
Final section 46.4 requires traversal from origin through validated successors; the available
load_gate_chain helper reads one physical series only. The combined recovery test merely reloads
three fields; it does not fulfill HD-FAL-023 section 11's canonical orchestrator restart scenario.

These findings mean fixing predecessor sealing alone cannot establish FAL-002 PASS. IR1-01 and
IR1-05 are OPEN, with useful portions corrected but their original integrated failure modes
remaining. IR1-03 direct no-intent correction remains verified; no frozen finding is reopened.
