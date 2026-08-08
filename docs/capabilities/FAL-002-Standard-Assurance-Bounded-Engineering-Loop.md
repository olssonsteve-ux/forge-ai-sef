# FAL-002 — Standard Assurance Bounded Engineering Loop

Status: `SPECIFICATION APPROVED — Implementation Planning complete; implementation not authorized`

Owner: Forge Design Authority

Decision basis: `HD-FAL-002`, revised under `HD-FAL-003`, `HD-FAL-004` and `HD-FAL-005`; approved
for Implementation Planning by `HD-FAL-006`

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
and have no correction or closure authority. The normative review is named “fresh read-only
Standard-Assurance review with adversarial instructions.” It must not be called independent High
Assurance unless separate execution and provenance are actually established by a future accepted
profile.

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
- at most 8 attributed production modules and 1,800 new counted production lines; unchanged
  attributed baseline lines are reported separately and do not consume the new-line envelope;
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
use and the complete exemption decision in section 13.4 returns `EXEMPT`. Every other reached path
counts unless this section explicitly requires `awaiting_human`. Splitting, moving or wrapping code
does not change attribution or the total.

A counted production line is a physical line in an attributed production source file that is neither
empty nor solely a comment. Docstrings and multiline literals count. Tests and documentation do not.
For generated behavior, the generator, template and canonical model count as production code, and
generated runtime behavior counts toward the line limit. Purely derivative schemas may be excluded
from the line count but count toward schema surfaces. One schema surface is one authoritative
persisted or external boundary root; splitting it among files or nested definitions does not create
an exclusion or change the surface count.

### 13.1 Frozen inventory inputs

Before implementation, an Engineering Brief may only freeze the concrete inputs to this algorithm:

- exactly one repository-relative canonical FAL-002 entrypoint;
- baseline commit and first-party source roots;
- the executor adapter and reviewer adapter, if present;
- persisted and external boundary roots;
- proposed general repository-tool exemptions, each with path and baseline hash; and
- expected generated runtime artifacts; and
- exact Python major/minor version used for standard-library parsing and import resolution.

Paths use `/` separators, contain no `.` or `..` segments and are relative to the repository root.
Content hashes are lowercase SHA-256 of the file bytes. A missing, ambiguous or multiple canonical
entrypoint stops as `awaiting_human`; no local default is permitted. The Engineering Brief may not
define or change traversal, import resolution, exclusions, stop conditions, attribution, module or
line counting, adapter classification or schema-surface semantics.

### 13.2 Deterministic traversal and attribution

The inventory shall execute this algorithm without a new dependency:

1. Initialize a queue with the frozen canonical entrypoint file.
2. Normalize every candidate to its unique repository-relative canonical path. Reject a candidate
   outside the repository or the frozen first-party source roots.
3. Process the queue in stable lexicographic canonical-path order.
4. Parse every reached first-party Python production source file with the Python standard library
   AST and inspect every syntactic import and executable first-party reference.
5. Resolve relative imports from the importing package and absolute first-party imports against the
   frozen source roots, using source-root order only when exactly one file resolves. Include package
   `__init__.py` files executed along the resolved import chain.
6. Include every uniquely resolved module file and executable reference, add it to the queue and
   continue until no new first-party production file remains.
7. Count each unique canonical file path exactly once. Every syntactically present first-party
   import or first-party executable reference is included and traversed regardless of whether it
   occurs inside a conditional, platform-specific, version-specific, exception-handling or
   `TYPE_CHECKING` branch. FAL-002 inventory performs no branch-feasibility analysis and never
   excludes an edge based on a frozen runtime variant. A statically resolved target counts; a
   computed or incompletely enumerable target stops as `awaiting_human` under section 13.3.
8. If resolution has zero or multiple plausible first-party targets, preserve the edge and stop as
   `awaiting_human`; do not select or exclude a target locally.

For every included file, output its canonical path, SHA-256 content hash, first lexicographic parent
edge, all additional inbound edges, attribution reason, classification and counted LOC. All
transitively reachable first-party production files count regardless of directory, name, package,
shared/common/internal/reusable label or FAL-001 origin. A thin wrapper counts as a production module
and, when it performs an adapter role, as that adapter; traversal continues through its delegated
runtime path.

An executor adapter is an attributed first-party file that translates between the canonical
executor request/result boundary and an executor implementation. A reviewer adapter is an attributed
first-party file that translates between the canonical reviewer packet/result boundary and a
reviewer implementation. Count each unique file satisfying a role once for that role, including a
delegating wrapper. A file satisfying both roles counts once as a production module and once against
each adapter limit. Unclear role classification stops as `awaiting_human`; the Engineering Brief
cannot relabel it.

### 13.3 Dynamic execution and subprocesses

The inventory must inspect `importlib.import_module`, `__import__`, `runpy`, import hooks, `exec`,
`eval`, path-based module loading, reflection or registries selecting runtime code, and first-party
scripts started by subprocess. A literal, statically resolvable first-party target is included and
traversed. A computed, configuration-selected or otherwise incompletely enumerable target is
recorded with its source edge and stops as `awaiting_human`. It may never be ignored, exempted or
counted as zero. Syntax or analysis failure also stops as `awaiting_human`.

### 13.4 General repository-tool exemption

For every transitively reached tool proposed for exemption, the inventory evaluates these mandatory
predicates in order:

1. exact repository-relative path and baseline identity are frozen;
2. acceptable repository provenance proves an independent use before FAL-002;
3. current content SHA-256 equals the content SHA-256 at the frozen baseline;
4. tool-owned configuration and every file in its frozen exemption closure are unchanged from the
   baseline;
5. no new or changed FAL-002 specialization exists in the proposed exemption closure;
6. new wrappers, adapters and FAL-002-specific runtime artifacts are outside the exemption and count
   normally; and
7. the exemption and its evidence are explicit in inventory output.

Each predicate status is exactly `VERIFIED_TRUE`, `VERIFIED_FALSE`, `UNKNOWN` or `NOT_EVALUATED`.
`NOT_EVALUATED` is permitted only after an earlier predicate is `VERIFIED_FALSE`. Acceptable
provenance for predicate 2 is mechanically verified by at least one statically resolved first-party
caller or entrypoint outside FAL-001 and FAL-002 at the baseline commit, or by a human decision record
that existed no later than that commit and explicitly names the tool path and independent use.
Absence of positive evidence is `UNKNOWN`, not `VERIFIED_FALSE`.

The only permitted decision tree is:

1. The tool must first be transitively reachable from the frozen FAL-002 entrypoint. Unresolved
   reachability follows the ordinary rule and returns `AWAITING_HUMAN`.
2. If every mandatory predicate is `VERIFIED_TRUE`, classify the tool `EXEMPT`.
3. If any mandatory predicate is `VERIFIED_FALSE`, classify the tool `COUNT`; remaining predicates
   may be `NOT_EVALUATED`.
4. If no predicate is `VERIFIED_FALSE` and at least one is `UNKNOWN`, return `AWAITING_HUMAN`.
5. No other classification or disposition is permitted.

A changed baseline content hash or verified FAL-002 specialization is `VERIFIED_FALSE` and therefore
`COUNT`. A missing or unverifiable baseline, provenance item or exemption closure is `UNKNOWN` and
therefore `AWAITING_HUMAN` unless another predicate is already `VERIFIED_FALSE`. A counted wrapper
does not disqualify an otherwise qualifying unchanged tool. No local choice between `COUNT` and
`AWAITING_HUMAN` is permitted, and no other reached-file exemption exists.

For each exemption candidate, inventory output contains its path, baseline commit, baseline and
current hashes, provenance reference, frozen exemption closure, every predicate status and its
evidence, and final classification.

### 13.5 Generated code and line counting

Generators, templates and the canonical model count as production code. Materialized generated
runtime code counts under the same module and LOC rules. If generated runtime behavior cannot be
materialized deterministically from frozen inputs, inventory stops as `awaiting_human`. Generation
cannot move runtime scope outside the limits. Purely derivative schemas may be excluded from LOC but
remain subject to schema-surface counting.

For each attributed production source file, LOC is the number of physical non-empty lines except
lines whose non-whitespace content is solely a comment. Code with a trailing comment, docstrings,
multiline string literals, generators, templates and materialized generated runtime code count. The
inventory reports LOC per file and the summed total.

### 13.6 Schema surfaces and dependencies

A schema surface is one independently persisted or externally exchanged top-level payload or
boundary versioned or validated as a unit. File splitting does not alter the count. Nested
definitions under the same real boundary root do not automatically add surfaces. Independent
payload types in one file are separate surfaces, and placing independent boundaries beneath a
synthetic wrapper does not reduce the count. Each surface has a stable identifier and canonical-model
reference in the inventory.

The inventory reports standard-library imports, existing third-party dependencies, dependency
manifest or lockfile changes and new direct or transitive dependency surfaces. A new dependency
without a human decision stops as `awaiting_human`.

### 13.7 Deterministic output and stop result

Output is sorted by canonical path and stable identifier and contains the frozen inputs and baseline
commit; entrypoint; every attributed file with hashes and edges; every inclusion or exemption reason;
module count; per-file and total LOC; executor- and reviewer-adapter counts; schema surfaces;
dependency changes; unresolved dynamic targets; and final `PASS` or `AWAITING_HUMAN` against every
hard limit. An unclassified or unresolved runtime edge, a limit breach or a prohibited complexity
feature stops as `awaiting_human`, never implicit exclusion. Reclassification, movement, splitting,
wrapping or abstraction cannot cure a breach.

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
8. reviewer execution satisfies the fresh read-only Standard-Assurance review with adversarial
   instructions contract;
9. the append-only history retains adverse reviews and corrections;
10. human decision cards block without defaults;
11. human-only closure passes role, eligibility, pending-decision, atomicity, interruption and repeat tests;
12. forbidden operations and allowed file/command boundaries pass adversarial fixtures;
13. the hard size/complexity limits are satisfied;
14. full Forge tests, lint, format, diff check and Project Memory Health pass;
15. a fresh read-only Standard-Assurance review with adversarial instructions of the implementation
    has been completed and returns PASS;
16. a human separately authorizes closure.

An implementation PASS is not release authorization and cannot start an adjacent product gate.

## 16. Required implementation evidence

A future Engineering Brief must define the canonical model technology, generated-schema check,
storage layout, exact collector commands/parsers, adapter interface, schema fixtures, interruption
fixtures, criterion coverage table and rollback. For the section 13 inventory it may freeze only the
inputs listed in section 13.1 and select an implementation of the already normative algorithm; it
may not alter that algorithm or its semantics. No implementation is authorized by this
specification.

## 17. First real measurement trial

FAL-002 requires two separate review events: a fresh read-only Standard-Assurance review with
adversarial instructions whose review object is the specification, and a separate fresh read-only
Standard-Assurance review with adversarial instructions whose review object is the implementation.
After both events and human closure, Manual Digital Album Authoring and Export is intended as the
first real before/after trial. Its capability specification is not created here. The trial follows
the separate measurement plan and must not claim improvement before measured evidence exists.
