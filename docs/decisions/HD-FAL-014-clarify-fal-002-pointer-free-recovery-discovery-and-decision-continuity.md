# HD-FAL-014 — Clarify FAL-002 Pointer-Free Recovery Discovery and Decision Continuity

Status: `ACCEPTED`

Decision date: 2026-08-08

Decision owner: Forge Architecture / Human Design Authority

Provenance: Explicit user architecture-clarification authority in the Codex task titled
`HD-FAL-014 — Clarify FAL-002 Pointer-Free Recovery Discovery and Decision Continuity` against
branch `main`, commit `045ef3d455fc33659150c59fc5f6c5790bbf4c45`
(`docs(forge): complete EB-006 third residual correction`), with clean working tree and empty
staging. The task supplies the Independent Standard-Assurance Review IR4 disposition and limits this
decision to the architecture authority gap in `EB006-IR4-03`.

Decision scope: clarify the pointer-free discovery and pending-decision continuity portions of the
accepted `HD-FAL-012` recovery architecture. This decision does not modify EB-006, correct a
finding, authorize CORR-012 or authorize FAL-002 implementation.

## 1. Verified baseline and governance context

Before substantive work, the repository baseline was verified as:

- repository: `forge-ai-sef`;
- branch: `main`;
- HEAD: `045ef3d455fc33659150c59fc5f6c5790bbf4c45`;
- commit subject: `docs(forge): complete EB-006 third residual correction`;
- working tree: clean; and
- staging: empty.

`HD-FAL-011`, `HD-FAL-012` and `HD-FAL-013` remain `ACCEPTED`. CORR-011 is documentation-complete
but not independently fully verified. FAL-002 remains unimplemented and `NOT AUTHORIZED`. FAL-001
remains permanently `TERMINATED BLOCKED`, unaccepted and unclosed, with correction count 2/2.

Independent IR4 ended with the abbreviated token `FAIL`, while its substantive disposition states
that implementation authorization is not recommended and FAL-002 remains unauthorized. The
canonical governance interpretation is therefore:

`FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`

The abbreviated token is a non-material review-output formatting deviation. This normalization does
not edit the review, verify a correction or close a finding.

IR4 records five open blocking findings:

| Finding | Severity | Status at this decision |
| --- | --- | --- |
| `EB006-IR4-01` | `CRITICAL` | open; not addressed here |
| `EB006-IR4-02` | `HIGH` | open; not addressed here |
| `EB006-IR4-03` | `CRITICAL` | architecture authority provided; remains open |
| `EB006-IR4-04` | `HIGH` | open; architecture dependency clarified only |
| `EB006-IR4-05` | `CRITICAL` | open; not addressed here |

## 2. Problem requiring clarification

`HD-FAL-012` correctly selected deterministic successor physical series forming one logical
append-only lineage. EB-006 then used the full semantic obstruction descriptor, including
`intended_record_hash`, to derive the successor UUID. That conflates two different identities.

First, a fresh consumer may be unable to reconstruct non-persisted adapter output and therefore
cannot derive the intended hash needed to locate an already authoritative successor. Successor
state then exists but is not discoverable from the authoritative predecessor alone.

Second, when a pending HumanDecisionRecord path is itself obstructed, creating a new recovery card
for the physical obstruction can leave the original human governance obligation without one
resolvable active-lineage representation. Recovery must relocate representation, not silently
replace the semantic question.

## 3. Binding HD-FAL-012 invariants retained

This clarification retains the selected `HD-FAL-012` architecture:

1. Physical successor segments form exactly one logical lineage.
2. `RECOVERY_ROOT` remains a variant of the existing GateRecord surface.
3. A valid published recovery root is the sole successor authority transition.
4. The predecessor becomes permanently sealed at that transition.
5. Recovery state is `awaiting_human` and cannot create PASS, eligibility or closure.
6. Frozen scope, criteria, policy, correction count, ordinals, findings, decisions and progress
   history carry forward without reset.
7. HumanDecisionRecord remains decision authority only and never state authority.
8. No global mutable current-series pointer, recovery registry or sixth boundary surface exists.
9. All publication remains append-only and occupied evidence is preserved.

This decision narrowly replaces only the assumption that semantic recovery identity and physical
successor discovery identity must share the same preimage.

## 4. Alternatives assessed

### Alternative A — discovery identity independent of intended output

Assessment: **selected**. A physical successor locator can be uniquely anchored to the authoritative
predecessor and its next publication slot. `intended_record_hash` remains inside the semantic
recovery descriptor and recovery root, but is not needed to locate that root.

This preserves append-only history, deterministic collision handling and the five surfaces. The
exclusive create of one candidate root resolves concurrent observations of the same blocked slot.

### Alternative B — persisted publication intent

Assessment: **selected narrowly** for bytes that are not guaranteed reconstructable from existing
authoritative state. The intended boundary bytes are durably staged, then an existing-surface
GateRecord commits their target and hash before the final target publication is attempted.

This adds a bounded GateRecord transition and write amplification for non-reconstructable output,
but adds no surface, module, adapter or dependency. Reconstructable GateRecord transitions do not
need a redundant intent record when their complete bytes are deterministically derivable from the
authoritative predecessor.

### Alternative C — deterministic successor ordinal enumeration

Assessment: **selected**. Consumers calculate and probe only the exact candidate paths defined by
the predecessor-derived discovery key and non-negative recovery ordinal. They do not enumerate
directory entries or choose among heuristic candidates.

The first absent candidate proves that no higher candidate can be authoritative. A valid candidate
is adopted only when every lower candidate is either that same valid root or a preserved stable
obstruction. Resource/path exhaustion remains the already bounded external-repair condition.

### Alternative D — deterministic lineage-relative physical namespace

Assessment: **rejected as authority**. A deterministic directory layout remains useful storage, but
directory ancestry or presence cannot establish a lineage edge. Only a valid RECOVERY_ROOT carrying
the exact predecessor and discovery bindings establishes authority.

### Alternative E — existing-surface decision rebinding

Assessment: **selected** for pending decisions. A stable semantic decision identity is carried in
GateRecord lineage state and may be bound to a new HumanDecisionRecord locator in a successor
segment. The semantic question does not change and no alternate decision identity is minted merely
to escape a physical collision.

## 5. Required distinction: semantic recovery identity

`semantic_recovery_identity` describes **why** recovery exists. Its canonical value remains the
`recovery_condition_hash` over the complete obstruction descriptor required by `HD-FAL-012`,
including:

- origin and predecessor series identity;
- predecessor gate ID/hash;
- blocked publication slot and target path;
- intended record hash;
- obstruction kind and path-object kind;
- observed-content hash when readable; and
- inherited frozen-contract hash.

The semantic identity is evidence-bound inside RECOVERY_ROOT. It distinguishes different observed
conditions and binds the intended record that failed publication. It does not determine where the
successor must be looked up.

Universal canonical-byte and hash-preimage spelling remains subject to open `EB006-IR4-01`. A later
correction must apply that one universal rule to both semantic and discovery objects; this decision
does not select competing LF/hash behavior.

## 6. Required distinction: physical discovery identity

`physical_discovery_identity` describes **where** a successor can be found from facts that are
already authoritative. Its architecture-level preimage contains exactly these semantic fields:

```text
{
  domain: "fal002-recovery-discovery-v1",
  origin_series_id,
  predecessor_series_id,
  predecessor_gate_id,
  predecessor_gate_hash,
  publication_slot: {
    target_surface,
    target_record_id,
    target_path
  }
}
```

No timestamp, process identity, observed obstruction bytes, obstruction kind, intended bytes or
intended record hash participates. The later EB-006 correction must give each field its exact final
canonical type after resolving `EB006-IR4-01`.

`recovery_discovery_key` is the canonical hash of that object. Candidate successor UUID uses the
existing `HD-FAL-012` namespace UUID and the exact logical name form:

`fal002-recovery-discovery-v1:{recovery_discovery_key}:{recovery_ordinal}`

where `recovery_ordinal` begins at zero. This narrowly supersedes the `HD-FAL-012` rule that used
`recovery_condition_hash` in the UUID name. The successor's RECOVERY_ROOT binds both identities so
physical discovery cannot detach from semantic obstruction evidence.

## 7. Persisted publication slot and derivation material

A `publication_slot` is the one boundary publication permitted next by the active authoritative
GateRecord. It is not a new record or surface. It is either explicitly present in that GateRecord or
uniquely derivable from its exact state and payload.

Before a final create-only publication may be attempted, authoritative lineage state must determine:

- origin and active predecessor series ID;
- active predecessor gate ID and record hash;
- target surface ID;
- target record ID;
- canonical target path; and
- whether intended bytes are `RECONSTRUCTABLE` or `COMMITTED`.

For a next GateRecord whose complete bytes are deterministically reconstructable from authoritative
inputs, its sequence, ID and path form the publication slot without another transition.

For ExecutorExchange, RunRecord, ReviewerExchange, externally supplied HumanDecisionRecord or any
other output whose complete bytes are not guaranteed reconstructable after crash:

1. validate the complete intended boundary object;
2. durably stage its exact canonical bytes at a deterministic non-authoritative staging location
   derived from the predecessor and publication slot, not from the intended hash;
3. append and validate a `PUBLICATION_INTENT` GateRecord under the existing GateRecord surface that
   binds target surface, record ID, path and intended record hash; and
4. only then attempt create-only publication at the target final path.

The staged object is evidence and replay material, never authority. The publication-intent
GateRecord is authority for the intended hash. A crash before the intent gate becomes authoritative
leaves the earlier gate active; replay may use only a schema-valid staged object matching the
predecessor-derived slot. A crash after the intent gate preserves every fact required to construct
and validate recovery without adapter re-execution.

If publication of the intent GateRecord itself is obstructed, its physical successor locator is
still derivable from the earlier authoritative predecessor and that gate's implicit next-gate slot.
Its intended bytes are recoverable from the already durable deterministic stage. The final recovery
root, if published, carries their semantic intended hash.

Facts used only as obstruction evidence—kind, path-object kind and observed-content hash—may be
collected after obstruction. They affect semantic recovery identity and RECOVERY_ROOT validation but
never physical discovery. Ephemeral process values never affect either identity.

## 8. Pointer-free successor discovery algorithm

A fresh consumer performs exactly this read-only algorithm:

1. Begin at the frozen origin manifest series ID.
2. Validate that physical segment's complete GateRecord chain and select its latest valid gate.
3. Derive the sole permitted `publication_slot` from that gate. If no publication is pending or
   permitted, stop at that segment.
4. Inspect the exact normal target named by the slot. Exact valid intended bytes are ordinarily
   adopted and recovery lookup is unnecessary. An absent target leaves the predecessor active for
   ordinary publication/replay. Only a stable conflicting, malformed, non-regular or unreadable
   target proceeds to recovery lookup.
5. Compute `recovery_discovery_key` from section 6 using only the validated origin, predecessor gate
   and publication slot.
6. For ordinal `n = 0, 1, 2, ...`, compute the one UUID and exact gate-zero path defined by section 6.
7. If candidate `n` is absent, stop: no higher ordinal is eligible and the predecessor remains the
   active segment, unable to progress until the deterministic recovery root is published.
8. If candidate `n` contains a stable obstruction, preserve it and continue to `n + 1`.
9. If candidate `n` is a schema/hash-invalid regular record, a wrong predecessor/discovery binding,
   or a valid-looking root with incompatible carry-forward, treat its path as a preserved stable
   obstruction and continue.
10. If candidate `n` is a valid RECOVERY_ROOT binding the exact predecessor, publication slot,
   discovery key, semantic recovery identity and complete carry-forward, adopt it, seal the
   predecessor and repeat this algorithm from the successor segment.
11. The first eligible valid root is unique authority. Any higher candidate is non-authoritative;
    directory presence and `current.json` never affect the result.

This is deterministic lookup over an architecture-defined keyspace, not directory scanning. Within
the local accidental-tamper threat model, enumeration terminates at the first absent or valid
candidate. Inability to test/create further candidates because the series root or storage is
unusable remains `AWAITING_HUMAN_EXTERNAL_REPAIR`, not permission for a pointer or heuristic branch.

Two consumers given identical authoritative records and path observations therefore derive the same
candidate sequence and active logical lineage.

## 9. Crash and replay consequences

| Crash boundary | Authoritative result and replay |
| --- | --- |
| before intended bytes are durably staged | predecessor stays active; no final publication was permitted |
| after stage, before publication-intent gate | predecessor stays active; deterministic slot finds and validates the stage; replay publishes the same intent or recovers its obstructed gate path |
| after publication-intent gate, before target final | intended hash/path are authoritative; replay publishes the same target or derives the same recovery discovery key |
| after target obstruction, before recovery-root final | predecessor remains active but unable to progress; replay derives the same candidate sequence without ephemeral output |
| after recovery-root final | successor is authoritative; replay adopts it and completes only missing bound decision publication |
| recovery-root candidate collision | preserve the candidate obstruction and advance to the next exact ordinal |
| decision-record collision after root authority | preserve it and create the next recovery successor carrying the same semantic decision requirement with a new physical binding |

No replay may re-invoke an executor or reviewer merely to reconstruct an intended hash already
committed in authoritative state. Existing separately governed retry rules remain applicable only
when no such commitment became authoritative.

## 10. Decision-continuity terminology

The following distinctions are binding:

- `decision_identity`: stable semantic identifier for one human governance question. Its semantic
  preimage contains domain, normalized question, ordered choices, original governance target and
  immutable semantic source references. It excludes physical series, locator, recovery ordinal and
  path-obstruction evidence.
- `decision_requirement`: the active GateRecord-lineage obligation stating that
  `decision_identity` remains pending, together with its semantic payload hash and disposition.
- `decision_record`: one schema/hash-valid HumanDecisionRecord physically representing that
  requirement or its resolution.
- `decision_locator`: the exact series-relative HumanDecisionRecord path named by an active-lineage
  binding.
- `active-lineage binding`: a hash-covered GateRecord or RECOVERY_ROOT entry associating the stable
  decision identity and semantic payload hash with exactly one current physical record ID, locator,
  record hash and non-negative binding generation.
- `resolution`: an ACCEPTED or DECLINED HumanDecisionRecord whose identity, selected choice,
  rationale, target and hash are validated against the active requirement and whose application is
  recorded by an authoritative GateRecord transition.

A decision record alone never changes state. The GateRecord lineage owns whether the requirement is
pending or applied.

## 11. Pending-decision rebinding

When the current decision locator is obstructed, recovery must not mint a different semantic
question. The next valid RECOVERY_ROOT shall:

1. carry the same `decision_identity`, semantic payload hash, domain, question and ordered choices;
2. preserve the obstructed locator and observed obstruction as evidence;
3. increment only the physical `binding_generation`;
4. bind one precomputed HumanDecisionRecord under the new successor series using the same semantic
   decision identity;
5. bind that record's exact locator and record hash without making it state authority; and
6. leave the decision requirement pending until a valid resolution is applied by GateRecord state.

The rebound decision record may change only physical binding fields required to name the active
successor and its recovery condition. It must explicitly identify the preceding binding or its
obstructed locator. The question, domain, allowed choices and original semantic target cannot change.

Because the recovery root must bind the decision record before either is published, the record
targets the successor series, recovery discovery key and semantic recovery identity rather than the
recovery-root record hash. The root then binds the complete precomputed decision-record hash, avoiding
a hash cycle.

If the rebound path is also obstructed, the same rule repeats with another recovery successor and a
higher binding generation. This creates neither a new semantic decision nor a competing authority.
Byte-identical replay at the active locator is idempotent. Same locator/different bytes is preserved
obstruction evidence and cannot resolve the requirement.

## 12. Complete-logical-lineage decision lookup

A fresh consumer resolves decisions using only validated lineage bindings:

1. Start with the origin manifest segment and an empty derived decision-requirement ledger.
2. Validate every GateRecord in that segment and apply its decision requirement, binding,
   resolution-reference and disposition transitions in gate sequence.
3. Discover the next segment only through section 8 and repeat in logical-lineage order.
4. For each still-pending identity, accept only the latest active-lineage binding with the greatest
   valid binding generation reached through that lineage. Binding generation cannot skip.
5. Read only the exact HumanDecisionRecord locator named by that binding. Do not scan a decisions
   directory or select a record by filename resemblance.
6. Validate surface/schema, canonical bytes, record hash, semantic decision identity, semantic
   payload hash, binding generation, active recovery target and allowed choices.
7. Reject records from inactive, orphan, unjustified-higher-ordinal or forked segments as
   non-authoritative evidence. A formerly active record remains history but cannot satisfy a later
   rebinding unless the current GateRecord binding explicitly carries its exact resolution reference.
8. If an earlier valid accepted resolution exists but its state-application gate was obstructed, a
   recovery root may carry that exact immutable resolution reference forward. It may not alter the
   choice or rationale. The requirement is satisfied only when the active GateRecord lineage
   validates and applies that referenced resolution.
9. If the bound path is absent, malformed, hash-different or obstructed, the requirement remains
   pending and progression fails closed; recovery/rebinding follows section 11.
10. Replay reuses the same semantic identity, binding generation, exact locator and record hash. It
    never creates a second semantic decision or selects a default.

This supplies the architecture basis needed for a later exact correction of the phrases “same
series decision path” and “canonical decision path” in `EB006-IR4-04`. It does not itself correct,
verify or close IR4-04.

## 13. Authority and surface accounting

The clarification uses only the five authorized surfaces:

| Surface | Clarified use |
| --- | --- |
| GateRecord | publication intent, recovery discovery binding, pending-decision ledger and resolution application |
| ExecutorExchange | unchanged |
| RunRecord | unchanged |
| ReviewerExchange | unchanged |
| HumanDecisionRecord | physical pending/resolution records and rebinding representation |

`PUBLICATION_INTENT` and RECOVERY_ROOT are GateRecord payload/state forms, not independent persisted
roots. Decision binding/rebinding remains within GateRecord and HumanDecisionRecord. Staging is
non-authoritative replay material and cannot be consulted to choose current authority.

No manifest, registry, recovery index, locator file, current-series file, authority pointer or
sidecar is introduced. Per-segment `current.json` remains a replaceable derived cache with no
authority. Physical path layout cannot establish authority without a valid GateRecord lineage.

## 14. Scope and budget assessment

Classification: **bounded within the existing budget**.

The clarification adds one bounded GateRecord intent form, a predecessor-derived discovery-key
calculation, exact candidate probing and decision binding-generation handling inside responsibilities
already assigned to `forge/fal002.py`, `forge/fal002_model.py` and `forge/fal002_io.py`. It requires:

- no new production module;
- no new executor or reviewer adapter;
- no new dependency;
- no new top-level schema/boundary surface;
- no network, database, transaction service or generalized recovery framework; and
- no change to scope, criteria or version.

The controlling envelope remains approximately 1,660 expected and at most 1,800 new production LOC,
with 140 LOC margin. This architecture decision does not add LOC authority or reopen `EB006-FR-07`.
A later correction must update bottom-up accounting. Concrete evidence that the clarified behavior
cannot fit at or below 1,800 requires `BUDGET AUTHORITY REQUIRED` before implementation authority can
be considered.

## 15. Answers to the required architecture questions

### Q1 — Pointer-free successor discovery

Derive a discovery key from the validated origin, predecessor gate and its sole persisted/derivable
publication slot; probe only exact UUIDv5 ordinal candidates; follow only the first eligible valid
RECOVERY_ROOT. No ephemeral intended output, arbitrary directory scan or global pointer participates.

### Q2 — Persisted derivation material

Origin/predecessor identity and the publication slot must already be authoritative. A non-
reconstructable intended hash must be committed by a GateRecord before target publication.
Obstruction facts are later semantic evidence and do not locate the successor.

### Q3 — Intended-record identity

Select A plus bounded B: retain intended record hash in semantic recovery identity, remove it from
physical discovery identity and require persisted publication intent where reconstruction is not
guaranteed.

### Q4 — Successor enumeration

Use deterministic enumeration of exact candidates derived from one predecessor discovery key and
ordinal. The valid recovery root's explicit predecessor and publication-slot bindings establish the
edge; path presence alone does not.

### Q5 — Pending-decision continuity

Carry one stable semantic decision identity and requirement. Rebind only its physical
HumanDecisionRecord locator/hash in the successor, increment binding generation and preserve every
prior record/obstruction as evidence. Do not mint a new semantic question for a path collision.

### Q6 — Decision resolution lookup

Traverse the complete validated logical lineage, derive the latest binding for each semantic
identity, read only that exact locator or an explicitly carried immutable resolution reference,
validate all hashes/targets/generations and apply resolution only through an authoritative
GateRecord transition.

## 16. Effect on IR4 findings

This decision's effect on `EB006-IR4-03` is exactly:

`ARCHITECTURE AUTHORITY PROVIDED — FINDING REMAINS OPEN`

The architecture dependency blocking correction of `EB006-IR4-04` is removed. IR4-04 itself remains
open and requires exact EB-006 decision/offline lookup text and fixtures.

`EB006-IR4-01`, `EB006-IR4-02` and `EB006-IR4-05` remain open and unchanged. The only constraints
this decision places on their future correction are:

- one universal canonical hash rule must cover semantic identity, discovery identity, publication
  intent and decision binding;
- the independent oracle must cover every intent/discovery/rebinding/crash case; and
- finding ledger carry-forward must remain complete across every physical successor.

No finding is corrected, independently verified, resolved or closed by this decision.

## 17. Explicit exclusions

This decision does not:

- modify EB-006 or the FAL-002 capability specification;
- authorize or execute `CORR-012-01` through `CORR-012-05`;
- implement FAL-002, schemas, fixtures, tests or runtime behavior;
- authorize Implementation, PASS, eligibility, closure or residual-risk acceptance;
- change Forge runtime, Audio Recorder or album capability code;
- change FAL-001 or its history;
- authorize push, tag, merge, release, packaging, distribution, publication or version change; or
- introduce a mutable authority pointer or sixth persistence surface.

## 18. Resulting governance state

- `HD-FAL-014`: `ACCEPTED`.
- IR4 canonical outcome: `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
- `EB006-IR4-03`: `ARCHITECTURE AUTHORITY PROVIDED — FINDING REMAINS OPEN`.
- Architecture dependency for later correction of `EB006-IR4-04`: removed; finding remains open.
- `EB006-IR4-01` through `EB006-IR4-05`: all open; none verified or closed.
- `CORR-012-01` through `CORR-012-05`: reserved mapping only, `NOT AUTHORIZED`.
- EB-006: unchanged by this decision.
- FAL-002 specification: unchanged.
- FAL-002 implementation: `NOT AUTHORIZED`.
- Boundary surfaces: unchanged at five planned surfaces.
- Budget: approximately 1,660 expected / 1,800 maximum new production LOC.
- FAL-001: permanently `TERMINATED BLOCKED`, unaccepted and unclosed, correction count 2/2.

## 19. Next governance gate

The next permitted action is a separate Human Decision considering whether to authorize one bounded
documentation correction campaign with the reserved mapping:

- `CORR-012-01` → `EB006-IR4-01`;
- `CORR-012-02` → `EB006-IR4-02`;
- `CORR-012-03` → `EB006-IR4-03`;
- `CORR-012-04` → `EB006-IR4-04`; and
- `CORR-012-05` → `EB006-IR4-05`.

That later decision may authorize correction only. It must not infer Implementation Authorization,
finding verification, finding closure or PASS from this architecture clarification.
