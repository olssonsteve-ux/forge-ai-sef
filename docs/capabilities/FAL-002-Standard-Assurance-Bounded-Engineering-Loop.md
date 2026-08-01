# FAL-002 — Standard Assurance Bounded Engineering Loop

Status: `AWAITING TARGETED HUMAN REVIEW — specification-only; implementation not authorized`

Owner: Forge Design Authority

Decision basis: `HD-FAL-002`, revised under `HD-FAL-003`

Predecessor disposition: `DISP-FAL-001` (`TERMINATED BLOCKED`)

## 1. Purpose

FAL-002 is a small engineering core for ordinary product capabilities. It replaces repeated manual
transfer of deterministic repository facts while preserving frozen contracts, bounded corrections,
fresh read-only Standard-Assurance review with adversarial instructions and human decisions. It
deliberately targets Standard Assurance; it does not
claim High-Assurance reviewer independence or semantic proof by hashing.

## 2. Users and outcome

The human Product Owner receives concise decision cards and retains product/scope/risk/closure
authority. An executor receives a deterministic frozen work packet. A fresh read-only reviewer
receives the implementation diff and verifiable evidence. Forge records one bounded, auditable state
series. The expected outcome is less manual relay work without weakening product authority.

## 3. Scope

FAL-002 shall provide:

- one machine-readable gate manifest and canonical runtime model;
- frozen scope, non-goals, criteria, allowed files, command policy and correction limit;
- deterministic prompt/work-packet compilation;
- automatically collected Git, changed-file, diff, build, test, warning/error/skip and runtime data;
- one provenance-bound run record;
- a bounded executor adapter and a fresh read-only reviewer adapter;
- structured `PASS`, `CORRECTION_REQUIRED`, `BLOCKED`, `INCONCLUSIVE` review results;
- criterion evidence references binding criterion ID, source, locator, content hash and provenance;
- at most two automatic corrections across the complete correction series;
- deterministic no-progress detection from collector-derived diff/evidence hashes;
- decision cards and explicit human escalation;
- append-only transition/review/correction history;
- a human-only closure operation satisfying the closure invariant.

## 4. Non-goals

FAL-002 shall not provide High-Assurance independence, cryptographic proof of semantic relevance,
protection against wholesale filesystem/history rewrite, release automation, autonomous scope or
criteria change, arbitrary workflows, parallel/multi-agent orchestration, plugins, remote services,
cloud persistence, UI, marketplace, general policy packs, organization/multi-repository governance,
automatic product decisions, or Audio Recorder/album functionality.

High Assurance is deferred to a separate future profile/capability with explicit isolated execution,
attestation, immutable/external anchoring and cost/infrastructure decisions. Its absence must not
block FAL-002 or ordinary album development.

## 5. Assurance model

FAL-002 is Standard Assurance. A reviewer must start in a fresh context, receive a read-only packet
and have no correction or closure authority. The review may be called “fresh read-only Standard
Assurance review.” It must not be called independent High Assurance unless separate execution and
provenance are actually established by a future accepted profile.

Machine checks prove syntax, identity, hashes, locators, recorded command outcomes and policy
invariants. The reviewer owns a reasoned semantic-relevance assessment for criterion evidence and
must state why cited evidence supports or fails to support the criterion. Hashes prove identity and
integrity within the bounded threat model, not meaning.

## 6. Decision ownership

Humans exclusively own product value, priority, scope/non-goals, criteria, risk acceptance,
material architecture lock-in, release/publication, destructive/external actions, budget extension
and closure. The executor may make reversible technical decisions within the frozen contract. Forge
owns state/policy/evidence collection. The reviewer may only evaluate and report.

Every unresolved human question becomes a decision card. No default may resolve it. Pending cards
block acceptance and closure.

### 6.1 Normative authority map

| Domain | Authority |
| --- | --- |
| Product value, scope, criteria, risk, budget and closure decisions | Human decision record |
| Gate state and transition history | Append-only state series |
| Deterministic Git, build, test and diff facts | Collector and bound run record |
| Structural validity of boundary data | Canonical boundary model |
| Semantic evidence relevance, findings and review assessment | Reviewer |
| Durable commit and document provenance | Repository history |

Each authority is authoritative only within its domain. Human authority may decide but may not
fabricate or rewrite deterministic execution facts. A reviewer may assess meaning and relevance but
may not change collector facts, state or human decisions. The canonical model determines structural
validity, not whether an assertion is true. A derived current, head or index file never overrides the
append-only series.

No local precedence or default may resolve a conflict between authorities. A conflict stops
progression as `blocked` or `awaiting_human`, preserves the raw evidence and creates a decision card.
A resolving human decision must name the domain over which it decides and must not rewrite prior
history.

## 7. Canonical model and boundary schemas

One canonical typed model shall define authoritative persisted and externally exchanged data.
Boundary schemas must be generated from that model or mechanically checked against it in tests.
Hand-maintained duplicate models are prohibited.

Schemas are required only for concrete boundaries:

- persisted gate/state series and snapshot records;
- executor request/result;
- run record;
- reviewer packet/result;
- decision and closure records.

Internal helper objects need no duplicate full schema unless they cross one of these boundaries.
Every boundary validates on both receipt and before authoritative persistence/state effect. Unknown
fields are rejected unless a named extension container is explicitly part of the canonical model.

## 8. State and history

Required states are `draft`, `awaiting_human`, `ready`, `executing`, `evidence_ready`, `reviewing`,
`correction_required`, `blocked`, `accepted` and `closed`. A single append-only series is authority;
derived current/head caches cannot replace it. State records bind series, sequence, predecessor,
payload hash and record hash. Loads validate the relevant chain before progression.

FAL-002 claims detection of gaps, forks, replacement of derived caches, accidental/partial tamper and
interrupted local persistence. It does not claim resistance to an actor able to rewrite the entire
filesystem and repository history.

## 9. Closure invariant

`PASS` is invalid if any open `CRITICAL`, blocking or human-decision-required finding exists.
Technical eligibility is a sealed record that binds the reviewed state, complete criterion coverage,
review result, findings disposition and evidence hashes.

Only a dedicated human-close operation may close. It must require an explicit human closure record,
accepted technical eligibility, no blocking/open findings, no pending decisions and matching gate/
series identity. It atomically appends state `closed`, capability status `closed` and a decision-bound
history transition. Executor, reviewer and generic transition APIs cannot close. Repeated closure is
idempotent or deterministically rejected. Interrupted persistence reopens to one coherent state.

Closure does not authorize product release.

## 10. Evidence model

The collector—not executor prose—records branch, baseline/final HEAD, staging/worktree, changed files,
diff/diffstat, commands, UTC intervals, exit codes, raw-output hashes, runtime/tool versions, build
warnings/errors and test passed/failed/skipped values. Missing data is `unknown` or `not_available`.
Secrets are redacted before persistence.

Each criterion reference contains criterion ID, evidence kind, source artifact/record ID, exact
locator or JSON pointer, assertion, artifact/content hash and provenance. Resolution verifies source,
hash, locator and criterion binding. Generic whole-run hashes without a relevant locator are invalid.
The reviewer records a semantic rationale; Forge does not represent that rationale as cryptographic
proof.

## 11. Correction policy

The complete series permits zero to two automatic corrections. A new run identity cannot reset the
count. Correction requires `CORRECTION_REQUIRED`, frozen-contract compatibility, allowed paths and
collector-demonstrated material change. Identical diff/evidence hashes, repeated findings without
material improvement, budget exhaustion, missing/contradictory evidence, forbidden operations,
scope/criterion changes, `BLOCKED` or `INCONCLUSIVE` stop or escalate. Review outcomes are never
default-converted to PASS.

## 12. Forbidden operations

Push, tag, merge, release, packaging, distribution, publication, version change, history rewrite,
destructive Git, OS restart/shutdown, external messages and credential reuse are forbidden unless a
future gate explicitly authorizes a specific operation. Model text cannot override this policy.

## 13. Hard size and complexity limits

The first implementation must remain within all limits:

- one repository and one active gate per invocation;
- at most 8 attributed production modules and 1,200 counted production lines;
- at most one executor adapter and one reviewer adapter;
- at most 6 external/persisted schema surfaces listed in section 7;
- sequential execution only; no agent pools, scheduler, plugin system, network or database;
- no new runtime dependency unless separately human-approved with justification;
- no CLI/UI beyond one existing-style local entrypoint if an Engineering Brief explicitly selects it.

Exceeding any limit requires a decision card and new scope authorization; it cannot be hidden as a
technical detail.

Size attribution starts at the FAL-002 entrypoint and includes every first-party executable source
file directly or transitively reachable at runtime, regardless of directory, name, or labels such as
shared, common, internal or reusable. Each such file is one production module. Existing FAL-001
modules executed by FAL-002 count. An adapter wrapper counts as an adapter even if it only delegates.
An unchanged general repository tool may be excluded only when the inventory records its independent
use and shows that it was not materially changed for FAL-002. Every new or materially changed runtime
path primarily serving FAL-002 counts in full. Splitting, moving or wrapping code does not change
attribution or the total.

A counted production line is a physical line in an attributed production source file that is neither
empty nor solely a comment. Docstrings and multiline literals count. Tests and documentation do not.
For generated behavior, the generator, template and canonical model count as production code, and
generated runtime behavior counts toward the line limit. Purely derivative schemas may be excluded
from the line count but count toward schema surfaces. One schema surface is one authoritative
persisted or external boundary root; splitting it among files or nested definitions does not create
an exclusion or change the surface count.

The future Engineering Brief must specify a dependency-free, reproducible inventory command that
walks the transitive runtime path and reports included/excluded files with reasons, module and line
totals, adapters, schema roots, generated inputs/outputs and the counting method. A limit breach must
stop in `awaiting_human`; reclassification, file movement or abstraction cannot cure it.

## 14. Failure behavior

Malformed boundary data, hash/identity mismatch, invalid transition, prohibited operation, stale or
forked series, missing raw evidence, timeout, interrupted persistence or unresolved decision must
fail closed into `blocked` or `awaiting_human` as appropriate. No exception path may synthesize PASS,
eligibility or closure.

## 15. Closure criteria for FAL-002 implementation

FAL-002 becomes technically eligible for human closure only when:

1. the canonical model generates or is mechanically proven consistent with all boundary schemas;
2. malformed/unknown/type/enum/hash/identity data is rejected at every receipt and persistence edge;
3. frozen scope/criteria and correction count survive reopen and new execution identities;
4. Git/build/test/diff facts come from collector evidence rather than executor summaries;
5. no-progress and the two-correction ceiling pass positive and negative fixtures;
6. open CRITICAL/blocking findings make PASS and eligibility impossible;
7. criterion references resolve precisely and reviewer semantic rationale is explicit;
8. reviewer execution is fresh/read-only, uses adversarial instructions and is described truthfully
   as Standard Assurance;
9. the append-only history retains adverse reviews and corrections;
10. human decision cards block without defaults;
11. human-only closure passes role, eligibility, pending-decision, atomicity, interruption and repeat tests;
12. forbidden operations and allowed file/command boundaries pass adversarial fixtures;
13. the hard size/complexity limits are satisfied;
14. full Forge tests, lint, format, diff check and Project Memory Health pass;
15. a separate fresh read-only Standard-Assurance implementation review returns PASS;
16. a human separately authorizes closure.

An implementation PASS is not release authorization and cannot start an adjacent product gate.

## 16. Required implementation evidence

A future Engineering Brief must define the canonical model technology, generated-schema check,
storage layout, exact collector commands/parsers, adapter interface, schema fixtures, interruption
fixtures, criterion coverage table, the reproducible size inventory required by section 13 and
rollback. No implementation is authorized by this specification.

## 17. First real measurement trial

After separate specification review, implementation review and human closure, Manual Digital Album
Authoring and Export is intended as the first real before/after trial. Its capability specification is
not created here. The trial follows the separate measurement plan and must not claim improvement
before measured evidence exists.
