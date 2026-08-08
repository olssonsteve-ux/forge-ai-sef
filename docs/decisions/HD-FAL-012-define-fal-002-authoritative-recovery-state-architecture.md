# HD-FAL-012 — Define FAL-002 Authoritative Recovery-State Architecture

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Forge Architecture / Design Authority

Provenance: Explicit user architecture authority in the Codex task titled
`HD-FAL-012 — Define FAL-002 Authoritative Recovery-State Architecture` against branch `main`,
commit `00ef983e97de5fdafb9363a0bd417fd77344f289`
(`docs(forge): require FAL-002 recovery architecture decision`), with clean working tree and empty
staging.

Decision scope: remove the architecture authority gap recorded by `HD-FAL-011` for
`EB006-IR3-04` and the recovery/publication portion of `EB006-IR3-05` without implementing or
correcting FAL-002.

## 1. Context and problem

FAL-002 uses an append-only sequence of canonical `GateRecord` files as state authority. If the next
canonical final path is occupied by malformed, conflicting or unusable content, the previous design
cannot overwrite that evidence, cannot skip the sequence and cannot publish an authoritative
fail-closed transition. Leaving the previous gate authoritative may falsely report an active
execution or review state. A diagnostic, cache or decision card cannot replace state authority.

The same obstruction affects conflict-card recovery. A deterministic decision path can be occupied,
and a card cannot establish the missing gate-state transition.

Independent IR3 therefore left `EB006-IR3-04` and `EB006-IR3-05` open and blocking. `HD-FAL-011`
required this architecture decision before any CORR-011 work.

## 2. Considered alternatives

### Option A — deterministic successor state series

Create a new physical state-series segment with a canonical link to the last valid gate and the
observed obstruction. The successor's first `GateRecord` records authoritative fail-closed state.
Discovery follows verified lineage links rather than a mutable pointer.

Assessment: satisfies the invariants with existing `GateRecord` and `HumanDecisionRecord` surfaces.
It adds bounded lineage/recovery behavior but no module, adapter, dependency or top-level boundary.

### Option B — reserved recovery namespace/path

Publish recovery state outside normal gate sequencing.

Rejected: it creates a second state namespace whose precedence over the ordinary series would need
independent authority and collision recovery. Calling it recovery metadata would conceal a new
authoritative surface.

### Option C — distinct terminal seal/recovery record

Publish a separate terminal record when normal append is blocked.

Rejected as a separate record type because it would be a sixth top-level persistence surface and
would duplicate `GateRecord` state authority. A recovery-root `GateRecord` inside Option A provides
the required seal without a new surface.

### Option D — higher-order series manifest or mutable authority pointer

Maintain a separate object naming the current series.

Rejected: it adds a new authoritative persistence surface, creates its own interrupted-update and
collision problem, and risks circular recovery. `current.json` remains a derived cache only.

### Option E — terminate without local continuation

Stop and require external repair while leaving the previous gate as authority.

Rejected as the normal solution because it does not make the terminal condition authoritative and
therefore does not resolve IR3-04. External repair remains the honest limit when the entire allowed
series root cannot accept any create-only publication.

## 3. Selected architecture

Select **Option A: deterministic successor state-series segments forming one logical authoritative
lineage**.

FAL-002 has exactly one logical state lineage. A lineage begins with the original manifest series
and may contain one or more physical series segments. Within a physical segment, ordinary sequence
and predecessor rules remain unchanged. At any time exactly one verified segment is active. A valid
recovery-root `GateRecord` atomically seals its predecessor segment and becomes the first
authoritative state of the successor segment.

A successor segment is another instance of the existing `fal002.gate-record.v1` surface, not a new
surface. Its first record uses a normatively distinct `RECOVERY_ROOT` payload variant under the same
canonical model and generated GateRecord schema.

## 4. Authoritative-state invariants

The later EB-006 correction shall preserve these rules:

1. Every previously valid record remains byte-identical and authoritative for its historical point.
2. No occupied path is overwritten, renamed, deleted or truncated.
3. Only a schema-valid, hash-valid, canonically located `RECOVERY_ROOT` final file changes the active
   segment.
4. A successor root has exactly one canonical predecessor segment, last valid gate and obstruction.
5. A predecessor segment is permanently sealed when its canonical successor root becomes
   authoritative.
6. A recovery root is always `awaiting_human`; recovery cannot create PASS, eligibility or closure.
7. Scope, criteria, frozen hash, correction count, maximum prior execution/review ordinal, unresolved
   finding set and pending decisions carry forward without reset.
8. Executor, collector and reviewer outputs cannot select a successor identity or make it
   authoritative.
9. Derived caches and directory presence never establish lineage authority.
10. All consumers validate the complete lineage before progression or closure.

## 5. Recovery trigger

For an intended next authoritative record with canonical final path `P` and precomputed canonical
bytes/hash `R`, normal create-only publication applies when `P` is absent and exact-idempotent
adoption applies when `P` contains `R`.

Recovery is triggered only when a stable persisted obstruction prevents those outcomes:

- `P` is a regular file whose bytes are readable but malformed, non-canonical or hash-different;
- `P` is a symlink, directory or other non-regular path object;
- `P` is persistently unreadable while its path object can be stably identified; or
- exclusive publication reports an occupied path and reread does not prove exact bytes `R`.

A transient I/O error with no stable persisted obstruction does not invent a successor. It halts
progress and retries the same operation after recovery/restart. If the allowed series root itself
cannot create directories or files, no local filesystem architecture can persist authority; the
process halts without progression for explicit external repository repair. That bounded platform
failure must not be represented as PASS or successful recovery.

## 6. Canonical obstruction descriptor

The recovery identity is constrained by one canonical descriptor containing:

- architecture domain literal `fal002-recovery-lineage-v1`;
- predecessor series ID;
- last valid predecessor gate ID and record hash;
- blocked sequence number;
- intended canonical target path and intended record hash;
- obstruction kind from `CONFLICTING_FILE`, `MALFORMED_FILE`, `NONREGULAR_PATH` or
  `UNREADABLE_PATH`;
- SHA-256 of exact observed bytes when readable, otherwise absent;
- canonical path-object kind when non-regular; and
- the inherited frozen-contract hash.

The descriptor is canonical JSON under the existing FAL-002 serialization rules. Its SHA-256 is the
`recovery_condition_hash`. No timestamp, process ID, actor prose or random value participates.

## 7. Successor identity and duplicate prevention

Candidate recovery ordinal is a non-negative canonical decimal integer. Candidate zero is tried
first. The candidate series ID is UUIDv5 using fixed namespace
`6f1b8e9e-6a37-5e3a-9d9e-50dc93295943` and name
`fal002-recovery-lineage-v1:{recovery_condition_hash}:{recovery_ordinal}`.

The candidate root path is the existing path form:

`.forge/fal002/series/{candidate_series_id}/gate/00000000.json`

The smallest ordinal whose root can contain the exact canonical recovery root is the only eligible
candidate. A lower ordinal may be bypassed only when its canonical root path contains a preserved
stable obstruction. An absent lower root makes every higher candidate non-authoritative. An exact
same-hash root is idempotently adopted. A different or invalid root is preserved and advances the
candidate ordinal. There is no fixed ordinal ceiling; storage/path exhaustion is an external repair
condition, not permission to choose a non-canonical branch.

Two conforming publishers derive identical candidate IDs and bytes. Exclusive staged publication
therefore produces one adoptable root under concurrency. A higher valid-looking root that fails the
smallest-eligible-ordinal rule is non-authoritative evidence.

## 8. Canonical recovery root

The successor's sequence-zero record remains the existing `GateRecord` boundary and shall contain a
`RECOVERY_ROOT` payload. EB-006 must define its exact JSON, but architecture requires it to bind:

- the full canonical obstruction descriptor and recovery-condition hash;
- predecessor series ID and last valid gate ID/hash;
- successor series ID and recovery ordinal;
- inherited frozen scope/criteria/policy hash;
- inherited correction count and maximum prior ordinal;
- a hash-bound complete unresolved-finding and pending-decision carry-forward;
- state `awaiting_human`, actor `recovery` and event `RECOVERY_SUCCESSOR`;
- the intended conflict-card identity; and
- an explicit permanent predecessor-seal assertion.

Its ordinary same-segment predecessor field is null because it is sequence zero. The payload link,
covered by payload and record hashes, is the cross-segment predecessor. This distinction prevents a
same-segment sequence rule from being silently reinterpreted.

The recovery root itself establishes state authority. No card, cache, directory or project-memory
entry can do so.

## 9. Recovery authority

Authority is separated as follows:

| Responsibility | Authority |
| --- | --- |
| Detect and byte-hash the persisted obstruction | Forge I/O collector under canonical path policy |
| Construct descriptor, candidate identity and recovery-root bytes | Forge core using this decision and canonical model |
| Validate schema, hashes, lineage, carry-forward and smallest ordinal | Canonical model |
| Stage and publish exact bytes | Forge I/O create-only persistence |
| Establish authoritative state | Successful publication and validation of the canonical recovery-root `GateRecord` |
| Decide whether work may later resume or be abandoned | Human through an accepted `HumanDecisionRecord` |

The actor whose output was being persisted supplies none of the recovery identity, descriptor,
ordinal or state choice.

## 10. Persistence, crash and replay lifecycle

1. A healthy active segment attempts its next canonical publication.
2. I/O detects and records the stable obstruction without mutating it.
3. Core deterministically constructs the descriptor, successor ID, recovery root and pending
   conflict-card bytes entirely in memory.
4. Card bytes and recovery-root bytes are staged under their candidate successor paths using the
   existing non-authoritative staged-publication mechanism.
5. The recovery-root final is linked and validated first. This is the single authority-transition
   point and permanently seals the predecessor.
6. The staged `HumanDecisionRecord` is then linked to its final path and validated.
7. A crash before root publication leaves the predecessor active but unable to progress; replay
   adopts complete stages or creates the next stage attempt and publishes the same root.
8. A crash after root publication adopts the successor as authoritative. An absent card is then
   published from its exact stage; state remains safely `awaiting_human` meanwhile.
9. If the candidate root is obstructed before publication, select the next canonical recovery
   ordinal. If the card path becomes obstructed after root authority, the active recovery segment
   itself triggers the same successor algorithm; the next recovery root records that card
   obstruction.
10. Replay of the same condition adopts the same lowest eligible valid successor and creates no new
    semantic terminal state.

Staging files and orphaned non-authoritative artifacts are preserved for audit. They never outrank
the selected lineage. A card is authoritative for decision resolution only when it is canonical,
valid and linked from the active recovery lineage; all other card-like files are evidence only.

## 11. Discovery and current authority

Consumers begin at the frozen original manifest series ID. They validate its complete gate chain,
derive any terminal obstruction descriptor and enumerate only canonical successor IDs produced by
section 7. They follow the unique smallest-eligible valid recovery root and repeat until no valid
successor exists. The resulting segment and its latest valid gate are current authority.

This graph traversal is deterministic and read-only. No global `current-series` file, symbolic link,
registry or mutable pointer is authoritative. Per-segment `current.json` remains a rebuildable cache
of that segment's latest valid gate.

Forks, higher-ordinal roots without justified lower obstructions, mismatched carry-forward or more
than one eligible successor fail closed and create no new authority.

## 12. Continuation after recovery

Recovery is terminal for automatic execution. The active recovery root remains `awaiting_human`.
Only an accepted HumanDecisionRecord bound to the recovery root may either:

- `ABANDON_LINEAGE`, producing a later blocked gate in the successor segment; or
- `AUTHORIZE_RECOVERY_RESUME`, permitting a later gate in that same successor segment to resume the
  carried state selected by the decision.

Resume cannot change frozen scope, criteria, budget or policy; cannot reduce correction count or
ordinal; cannot dismiss findings; and cannot create PASS, eligibility or closure. Any requested
change to those values requires its separately governed scope/criteria/budget decision.

## 13. Conflict-card role

The conflict card remains an existing `HumanDecisionRecord`. It explains the obstruction, names the
active recovery root and offers only the fixed human choices allowed by the later EB-006 contract.
It is not state authority, cannot activate a successor and cannot repair or rewrite evidence.

The later EB-006 correction must define the card's canonical source array and hash preimage. Card ID
must derive from the recovery-condition hash, successor series ID and a deterministic card ordinal.
Only the card linked from the selected active recovery lineage can be resolved. Orphaned, conflicting
or higher-ordinal cards remain preserved non-authoritative evidence.

## 14. Boundary-surface impact

No new boundary or persistence surface is introduced.

- Recovery state is a `RECOVERY_ROOT` variant of the existing `GateRecord` surface.
- Conflict and recovery choices use the existing `HumanDecisionRecord` surface.
- ExecutorExchange, RunRecord and ReviewerExchange are unchanged by this decision.
- A successor directory is another instance of the existing series storage root, not an independent
  payload type or authority namespace.
- Staging remains internal non-authoritative persistence.
- No global lineage manifest or mutable pointer is added.

The architecture keeps five planned surfaces and leaves one of the six permitted slots unused.

## 15. IR3 closure enablement

This decision does not correct or close either finding.

- `EB006-IR3-04`: the later EB-006 correction can now define an authoritative fail-closed
  continuation using the selected recovery-root GateRecord and deterministic lineage discovery.
- `EB006-IR3-05`: the later correction can now define total card identity/publication by binding the
  card to the authoritative recovery root and using the same successor mechanism when a card path is
  obstructed.

Both findings remain open pending CORR-011 authorization, correction and fresh independent review.

## 16. Budget and implementation impact

Expected production effect is **bounded within the existing budget**. The design adds lineage
derivation/validation, one GateRecord payload variant and recovery discovery to responsibilities
already allocated to `fal002.py`, `fal002_model.py` and `fal002_io.py`. It requires:

- no new production module;
- no new executor or reviewer adapter;
- no new dependency;
- no new top-level schema surface; and
- no version change.

The approximately 1,660 expected / 1,800 maximum production-LOC envelope and 140-line margin remain
controlling. This decision does not reopen `EB006-FR-07` or increase the budget. A later correction
must update the bottom-up allocation and stop for budget authority if concrete accounting shows the
hard maximum is no longer credible.

## 17. Consequences and constraints on later correction

A later Human Decision may authorize `CORR-011-01` through `CORR-011-08` as one coherent EB-006
documentation correction. That correction must:

1. implement this architecture normatively in EB-006 without changing its selected alternative;
2. define exact `RECOVERY_ROOT`, descriptor, UUIDv5, card and carry-forward schemas and hashes;
3. cover original-gate, successor-root and card-path obstruction plus every crash boundary in
   literal independent fixtures;
4. define discovery, sealing, replay, fork rejection and human resume transitions end to end;
5. keep conflict cards explanatory and HumanDecision-owned, never state authority;
6. synchronize closure, finding lifecycle and correction/no-progress behavior across the full
   logical lineage;
7. retain all other IR3 corrections within their existing problem boundaries; and
8. report updated bottom-up LOC allocation without changing the authorized ceiling.

This architecture decision does not authorize that correction, implementation, schemas, fixtures,
tests, release or finding closure.

## 18. Resulting governance state

- `HD-FAL-012`: `ACCEPTED`.
- Selected architecture: deterministic successor state-series segments forming one logical
  authoritative lineage.
- Boundary surfaces: unchanged at five planned surfaces.
- `EB006-IR3-04` and `EB006-IR3-05`: open; architecture authority gap removed only.
- `CORR-011-01` through `CORR-011-08`: reserved and `NOT AUTHORIZED`.
- EB-006: unchanged and awaiting a separate correction-authority decision.
- FAL-002 implementation: `NOT AUTHORIZED`.
- FAL-002 budget: approximately 1,660 expected / 1,800 maximum new production LOC.
- FAL-001: permanently `TERMINATED BLOCKED`, correction count 2/2.
- Next gate: separate Human Decision deciding whether to authorize the bounded CORR-011 correction.
