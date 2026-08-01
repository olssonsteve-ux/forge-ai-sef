# FAL-002 Reuse Matrix

Status: Proposed with FAL-002 specification; implementation not authorized

Source baseline: FAL-001 at `efd532f`, disposition `DISP-FAL-001`

Reuse is conceptual and selective. FAL-001 remains blocked; this matrix does not upgrade its code or
findings into accepted authority.

| FAL-001 asset/mechanism | Classification | FAL-002 treatment |
| --- | --- | --- |
| Frozen scope, non-goals, criteria, allowed paths and policy hash | `REUSE_AS_IS` | Preserve invariant and deterministic hashing semantics. |
| Deterministic prompt/work-packet compiler | `REUSE_AS_IS` | Retain sorted/versioned deterministic compilation without model reinterpretation. |
| Collector-owned Git/command/test evidence and unknown values | `REUSE_AS_IS` | Retain provenance, exit codes, raw-output hashes and no invented facts. |
| Maximum two automatic corrections | `REUSE_AS_IS` | Preserve across the complete series; execution identity cannot reset it. |
| Diff/evidence no-progress detection | `REUSE_AS_IS` | Derive hashes only from collector evidence. |
| Decision cards and human ownership taxonomy | `REUSE_AS_IS` | Pending decisions block; recommendations are not defaults. |
| Forbidden operations and actor restrictions | `REUSE_AS_IS` | Executor/reviewer cannot accept, close, release or mutate policy. |
| Append-only local snapshot ledger | `REUSE_AS_IS` | Use bounded local threat model; current/head remains derived only. |
| Secret redaction and changed-path normalization | `REUSE_AS_IS` | Retain with boundary fixtures. |
| Human-close operation | `REUSE_AFTER_FIX` | Add sealed eligibility and reject any open CRITICAL/blocking finding before closure. |
| Review-result application | `REUSE_AFTER_FIX` | PASS must reject blocking findings before state effect; no default conversion. |
| Hand-maintained JSON schemas plus parallel Python validation | `REUSE_AFTER_FIX` | Replace with one canonical typed model and generated/mechanically checked boundary schemas. |
| Criterion evidence resolver | `REUSE_AFTER_FIX` | Require precise source/locator/hash/provenance and criterion association; reviewer supplies semantic rationale. |
| Reviewer execution metadata | `REUSE_AFTER_FIX` | Record fresh/read-only Standard-Assurance execution honestly; never infer High-Assurance independence from labels. |
| Generic whole-content evidence pointer | `DISCARD` | It is insufficiently criterion-specific. |
| HMAC as hostile in-process authenticity boundary | `DISCARD` | Use collector ownership for accidental-tamper integrity; make no adversarial in-process claim. |
| FAL-001 acceptance/closure status or correction reset | `DISCARD` | FAL-001 remains blocked and its history cannot seed a green FAL-002 state. |
| Separate isolated reviewer infrastructure and attestation | `DEFER_TO_HIGH_ASSURANCE` | Requires a future profile/capability and explicit infrastructure authority. |
| External immutable ledger anchoring | `DEFER_TO_HIGH_ASSURANCE` | Not required for Standard Assurance local threat model. |
| Multi-agent orchestration, plugins, policy packs, remote service | `DISCARD` | Violates FAL-002 hard complexity boundary. |
| Cryptographic proof of semantic criterion relevance | `DISCARD` | Reviewer reasoning evaluates relevance; hashes prove identity, not meaning. |

Any future implementation review must map every reused runtime element back to this matrix and reject
unclassified carry-over.
