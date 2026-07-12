# EB-005 - Implement Governance Runtime Project Memory Health

Status: Implementation Reviewed

Date: 2026-07-11

Owner: Chief Architect

Review result: PASS

Implementation authorization: YES

Implementation date: 2026-07-12

Implementation review: `DAR-EB-0004` — `PASS`

Review date: 2026-07-11

Review Authority confirmed that EB-005 is deterministic, proportionate, traceable to CS-002.3 and
DAR-CS-0003, and safely implementable as one bounded change. Chief Architect accepts the corrected
implementation boundary.

Lifecycle history:

- `Proposed` on 2026-07-11 when the bounded brief was created for formal review.
- `Implementation Ready` on 2026-07-11 after formal Engineering Brief review returned `PASS`.
- `Implemented` on 2026-07-12 after the bounded code, tests, documentation, and required
  verification were completed under the AI Implementation Protocol.
- `Implementation Reviewed` on 2026-07-12 after DAR-EB-0004 returned `PASS` with no remaining
  conditions.

Next gate: commit the complete reviewed implementation and governance evidence.

## 1. Purpose

Implement the DAR-approved CS-002.3 Project Memory Health slice as one additional read-only
category in the existing human-readable `forge status` report.

The category evaluates only explicit, conservative, deterministic defects in active Forge project
memory. It does not certify correctness, interpret prose semantically, change governance state, or
authorize release activity. Formal review has accepted this brief as `Implementation Ready` and
authorizes only its bounded implementation.

## 2. Governing Capability, Review, Contracts, And Standards

Implementation MUST follow:

- `CONSTITUTION.md`
- `AI_ENGINEERING_CONDUCT.md`
- `docs/capabilities/FCS-002-Governance-Runtime.md`
- `docs/capabilities/CS-002.3-Governance-Runtime-Project-Memory-Health.md`
- `docs/reviews/DAR-CS-0003-CS-002.3-Project-Memory-Health.md`
- `docs/standards/ai-implementation-protocol.md`
- `docs/standards/testing-standard.md`
- `docs/standards/code-quality-standard.md`
- `docs/standards/lifecycle-standard.md`
- `docs/standards/capability-slice-standard.md`
- `docs/architecture/AR-0001-Engineering-Hierarchy.md`
- `docs/decisions/0005-project-memory-contracts.md`
- `docs/decisions/0013-governance-runtime-capability.md`
- `docs/decisions/0014-introduce-capability-slices.md`
- `docs/contracts/project-state-schema.md`
- `docs/contracts/project-brain-schema.md`
- `docs/contracts/ai-handoff-schema.md`
- closed CS-002.1 and CS-002.2 briefs and their implementation reviews

Where this brief is less specific than CS-002.3 or DAR-CS-0003, those accepted artifacts control.

## 3. Current Behavior

`forge/status.py` owns `StatusState`, `StatusItem`, `StatusCategory`, `StatusReport`, evaluation,
rendering, category construction, and deterministic rollup. `evaluate_status()` composes existing
governance, documentation, capability, engineering, testing, release, runtime-memory, version, and
repository categories. `_markdown_section()` supports current narrow consumers. CS-002.2 adds
Version Consistency Status and owns release-facing semantic-version comparison.

The CLI already renders every category through the common report renderer. There is no Project
Memory Health category, dedicated project-memory parser, or claim-driven reference resolver.

## 4. Target Behavior

`forge status` MUST include exactly one additional `Project Memory Health` category. It MUST:

- evaluate the three primary project-memory files
- apply exactly the nine rules in Section 11
- open supporting artifacts only for explicit active claims or references
- preserve existing categories, options, exit behavior, and human-readable rendering
- remain local, deterministic, advisory, and read-only
- coexist with Version Consistency Status without comparing semantic version values

## 5. Exact Implementation Scope

Expected implementation surfaces are:

- new private `forge/project_memory.py`
- `forge/status.py`
- `tests/test_status.py`, or the existing focused status-test file if differently named
- focused fixture files owned by the status tests
- user-facing documentation made inaccurate by the implementation
- project-memory, changelog, verification, and formal implementation-review handoff evidence

`forge/cli.py` SHOULD remain unchanged because the current renderer composes categories generically.
It MAY change only if implementation inspection proves a minimal category-presentation change is
necessary; no command, option, flag, exit policy, or interaction may change.

Existing status code MUST NOT be reorganized merely for style.

## 6. Explicit Exclusions

The implementation MUST NOT introduce:

- LLM or probabilistic interpretation
- writing-quality scoring or semantic similarity
- modification-time, Git-blame, or age-based freshness
- fuzzy, case-folded, edit-distance, or semantic reference matching
- automatic repair, synchronization, generated patches, or historical cleanup
- report persistence or status history
- JSON, strict mode, new flags, or new commands
- scoring, certification, release blocking, or release approval
- policy packs, remote inspection, or network calls
- generalized repository consistency or generalized Markdown parsing
- automatic lifecycle changes
- a public parser API, plugin architecture, policy engine, or registry
- project profiles or migration behavior
- semantic-version comparison owned by CS-002.2

## 7. Primary And Supporting Inputs

The primary inputs are exactly:

1. `PROJECT_STATE.md`
2. `PROJECT_BRAIN.md`
3. `AI_HANDOFF.md`

No other file is a primary input.

Supporting artifacts MAY be opened only when an explicit claim or reference in an approved active
section requires verification. Eligible targets are repository-relative Markdown artifacts under
`docs/decisions/`, `docs/capabilities/`, `docs/engineering/`, `docs/reviews/`, and `docs/release/`,
plus a full local Git commit hash. No supporting directory may be broadly scanned except the single
governed directory required to resolve one supported identifier prefix. `README.md`, `CHANGELOG.md`,
and arbitrary Markdown-link targets are not read by the nine approved rules because CS-002.3 and
DAR-CS-0003 define no link or path-token syntax that authorizes those reads.

A repository is Forge-signaled when at least one primary file, `CONSTITUTION.md`, or
`AI_ENGINEERING_CONDUCT.md` exists. With no signal, the category is `NOT_APPLICABLE`.

## 8. Exact Active And Historical Section Boundaries

Heading recognition is case-sensitive and exact after removal of an optional UTF-8 BOM and line
ending normalization to `\n`. A heading is active only when the complete line is `## ` followed by
the exact name below. Leading indentation, trailing text, alternate case, ATX closing hashes, and
Setext syntax are not aliases. There are no approved heading aliases.

Section content begins after its exact heading line and ends immediately before the next exact
second-level ATX heading or end of file. A required heading occurring zero times is `MISSING`; more
than once is `WARNING`. A section is empty when, after removing blank lines and HTML comment spans
beginning with literal `<!--` and ending with the next literal `-->` without nesting, it contains no
non-heading content line with non-whitespace characters. An unterminated comment consumes the
remainder of that section as comment content. Markdown formatting is not stripped or interpreted
for quality.

### PROJECT_STATE.md

Required and active:

- `## Status`
- `## Current Version`
- `## Current Objective`
- `## What Exists`
- `## What Does Not Exist`
- `## Architectural Posture`
- `## Next Recommended Work`

Optional and active when present:

- `## Planned Release`
- `## Active Risks`
- `## Blockers`

### PROJECT_BRAIN.md

Required and active:

- `## Core Identity`
- `## Guiding Beliefs`
- `## Product Shape`
- `## Important Boundaries`
- `## Current Decisions`
- `## Open Questions`

### AI_HANDOFF.md

Required and active:

- `## Role Context`
- `## Current Repository State`
- `## Current Architectural Intent`
- `## Instructions For Future AI Agents`
- `## Immediate Next Step`

Optional and active when present:

- `## Forbidden Actions`
- `## Required Reading`
- `## Handoff Notes`

Content outside these sections is historical or supporting context and MUST be ignored by active
checks unless an active section explicitly links to it. Optional sections are not required by Rule
2. Individual rules inspect only their narrower section lists in Section 11.

## 9. Exact Reference Syntax And Resolution

### Explicit Artifact Identifiers

Identifiers are case-sensitive ASCII tokens and map as follows:

| Accepted form | Governed directory and required filename prefix |
| --- | --- |
| `ADR NNNN`, `ADR-NNNN` | `docs/decisions/NNNN-` |
| `FCS-NNN` | `docs/capabilities/FCS-NNN-` |
| `CS-NNN.S` | `docs/capabilities/CS-NNN.S-` |
| `EB-NNN`, `EB-NNN.S` | `docs/engineering/EB-NNN-`, `docs/engineering/EB-NNN.S-` |
| `DAR-CS-NNNN`, `DAR-EB-NNNN`, `DAR-AR-NNNN` | identical prefix under `docs/reviews/` |
| `PRR-NNNN` | `docs/reviews/PRR-NNNN-` |

`N` represents an ASCII decimal digit in the exact widths shown. Resolution lists only `.md` files
whose basename begins with the required prefix in the one mapped directory. Exactly one match
resolves; zero is `MISSING`; multiple are `WARNING`. Matching MUST NOT recurse or use substrings,
topic names, case folding, edit distance, or prose meaning.

### Markdown Links And Path Tokens

CS-002.3 and DAR-CS-0003 authorize explicit identifier and full-commit-hash parsing, not a separate
Markdown-link or path-token reference format. Accordingly, repository-relative Markdown links,
exact `.md` path tokens, anchor fragments, reference-style links, images, autolinks, external URLs,
filesystem absolute paths, URI paths, and traversal paths are not reference inputs for PMH-4 and
are ignored as link/path syntax. Text inside a Markdown link label remains ordinary active-section
text and may independently contain a supported explicit identifier. A link destination MUST NOT
authorize a supporting-artifact read. No path normalization or anchor validation is performed.

Full 40-character hexadecimal commit hashes are recognized case-insensitively and checked only in
the local repository. With no Git metadata the commit sub-check is `NOT_APPLICABLE`; an unknown hash
is `MISSING`. No abbreviated hash is accepted.

## 10. Finite Lifecycle Normalization

Lifecycle claims are parsed only when an explicit supported identifier and accepted label occur in
the same sentence or Markdown list item. Source normalization may strip Markdown backticks, trim
whitespace and terminal punctuation, collapse internal whitespace, and compare ASCII
case-insensitively. It MUST NOT expand synonyms.

Accepted common and artifact-local labels are finite:

| Artifact applicability | Accepted source labels | Normalized comparison state |
| --- | --- | --- |
| Capability Slice | `Draft`, `Specified`, `Approved`, `Reviewed`, `DAR Approved`, `Implementation Ready`, `Implemented`, `Implementation Reviewed`, `Closed`, `Rejected`, `Withdrawn`, `Archived`, `Superseded`, `Deprecated` where ongoing reuse must be discouraged | slice-local `Approved` maps to `DAR Approved`; slice-local `Reviewed` maps to `Implementation Reviewed`; others remain canonical |
| Engineering Brief | `Draft`, `Approved`, `Implementation Ready`, `Implemented`, `Implementation Reviewed`, `Closed`, `Rejected`, `Withdrawn`, `Archived`, `Superseded`, `Deprecated` where ongoing reuse must be discouraged | same canonical label |
| ADR | `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded` | `Accepted` maps to common `Approved`; others remain canonical |
| DAR and formal review | `Completed`; final `PASS`, `PASS WITH CONDITIONS`, or `FAIL` | `Completed` plus the separate final result |
| Release | `Planned`, `Release Candidate`, `Released`, `Post Release Reviewed`, `Deprecated` | same canonical label |

Only labels applicable to the resolved artifact type are accepted. Unknown, inapplicable, or
unsupported labels make that claim `NOT_APPLICABLE`. Explicit lifecycle evidence is read only from
the resolved artifact's top-level `Status:` field and exact `## Status` section; both are examined
when both exist. One value is authoritative; two equal normalized values agree; different values
are conflicting evidence and produce `WARNING`. Formal reviews additionally use their explicit
final result as a separate decision value, never as a synonym for lifecycle status.
Unreadable evidence is `BLOCKED`; missing evidence is `NOT_APPLICABLE`. A contradictory accepted
claim is `WARNING`. State MUST NOT be inferred from prose tone, dates, filenames, directory
placement, or a commit alone.

## 11. Nine Evaluation Rules

Each evaluator returns one or more existing `StatusItem` values with a bounded label and evidence
message. Remediation MAY name the affected file, section, or artifact and advise human inspection;
it MUST NOT prescribe unaccepted wording, claim authority, or mutate anything.

### PMH-1 - Required Memory-File Presence

- Primary input: the three exact repository-root paths.
- Authoritative section: none; file scope only.
- Supporting evidence: none.
- Trigger and state: readable regular file `OK`; absent or non-file path `MISSING`; present but
  unreadable, invalid UTF-8, or I/O-failed file `BLOCKED`.
- Item/evidence: one item per file naming only its exact relative path and observed condition.
- Remediation boundary: advise restoring or making the named file readable.
- Controls/exclusions: optional artifacts and reasons for absence are not evaluated.
- Failure behavior: remaining available files continue; any item `BLOCKED` rolls up the category.
- Tests: healthy; each file missing; unreadable/invalid encoding; partial memory.

### PMH-2 - Required Section Presence And Non-Empty Content

- Primary input: every readable primary file.
- Authoritative section: required headings in Section 8 for that file.
- Supporting evidence: none.
- Trigger and state: each required heading exactly once with non-empty content `OK`; missing or
  empty `MISSING`; duplicated `WARNING`.
- Item/evidence: file and exact heading; content is not echoed.
- Remediation boundary: advise inspecting the named heading.
- Controls/exclusions: optional headings, order, prose quality, length, grammar, and tone excluded.
- Failure behavior: PMH-1 owns unreadable files; malformed near-headings are absent, not guessed;
  independent sections continue.
- Tests: missing, empty, duplicate, malformed heading, comment/whitespace-only content.

### PMH-3 - Current Status And Objective Usability

- Primary input: Project State `Status` and `Current Objective`; AI Handoff `Immediate Next Step`.
- Authoritative section: exactly those three sections.
- Supporting evidence: none.
- Trigger and state: at least one non-heading, non-comment content line is `OK`; otherwise `MISSING`.
- Item/evidence: file and section only.
- Remediation boundary: advise supplying an explicit current value without judging its content.
- Controls/exclusions: no writing-quality, strategic, detail, meaning, realism, or grammar test.
- Placeholder policy: CS-002.3 defines no rejected placeholder vocabulary; therefore no value such
  as `TBD`, `None`, or `N/A` is rejected merely by spelling. Only structural emptiness is tested.
- Failure behavior: missing/duplicate sections follow PMH-2; unreadable files follow PMH-1.
- Tests: populated, empty, comment-only, and literal placeholder text accepted as structurally
  present to prevent an invented semantic rule.

### PMH-4 - Active Artifact-Reference Integrity

- Primary input: Project State `Status`, `Current Objective`, `Next Recommended Work`; AI Handoff
  `Current Repository State`, `Immediate Next Step`.
- Authoritative section: exactly those five sections.
- Supporting evidence: only references parsed under Section 9.
- Trigger and state: one exact identifier match `OK`; zero target matches `MISSING`; multiple
  identifier matches `WARNING`; Git absence for a hash
  `NOT_APPLICABLE`; unreadable target/directory `BLOCKED`.
- Item/evidence: identifier or full commit hash plus resolved path or bounded candidates.
- Remediation boundary: advise correcting or disambiguating the explicit reference.
- Controls/exclusions: all link destinations and path tokens, historical sections, ordinary
  numbers, version strings, and filenames without governed identifiers are ignored.
- Failure behavior: no fuzzy fallback; dependent checks consume the explicit resolution result.
- Tests: every identifier family, repository-relative/external/absolute/traversal/fragment links
  ignored as destinations, identifiers in link labels, missing, ambiguous, unreadable, full hash,
  unknown hash, and no Git.

### PMH-5 - Project State And AI Handoff Active-Work Coherence

- Primary input: Project State `Current Objective`, the first non-empty list item in `Next
  Recommended Work`, and AI Handoff `Immediate Next Step`.
- Authoritative section: exactly those locations.
- Supporting evidence: valid governed work identifiers from PMH-4.
- Trigger and state: when both sides have identifiers, at least one shared identifier is `OK`; two
  disjoint explicit sets are `WARNING`; either side with no identifier is `NOT_APPLICABLE`.
- Item/evidence: both normalized identifier sets and section names.
- Remediation boundary: advise human reconciliation of the named active sections.
- Controls/exclusions: wording, detail, hierarchy, and semantic similarity are ignored. The slice
  defines no special phrases for `no active work`, `active capability`, `pending review`,
  `implementation pending`, or `closed work`; those concepts affect this rule only when expressed
  through supported identifiers. Gate phrases belong only to PMH-7.
- Exact contradiction pair: a non-empty Project State work-identifier set and a non-empty AI
  Handoff work-identifier set with an empty intersection. There are no other contradiction pairs.
- Failure behavior: unresolved identifiers follow PMH-4; absent identifiers never trigger prose
  inference.
- Tests: overlap, disjoint identifiers, different detail with overlap, and either side absent.

### PMH-6 - Explicit Lifecycle-Claim Coherence

- Primary input: all five PMH-4 sections.
- Authoritative section: same section containing the identifier/label pair.
- Supporting evidence: resolved artifact status and, for reviews, explicit final result.
- Evidence handling: inspect both the exact top-level `Status:` field and exact `## Status` section;
  one value controls, equal values agree, and different values conflict. For a formal review, the
  explicit final result is additionally authoritative and is not collapsed into status.
- Trigger and state: supported equal normalized claim `OK`; different authoritative state
  `WARNING`; no accepted pair or unknown label `NOT_APPLICABLE`; unresolved artifact `MISSING`;
  unreadable evidence `BLOCKED`; conflicting authoritative fields `WARNING`.
- Item/evidence: memory claim, normalized state, artifact path, and authoritative value.
- Remediation boundary: advise reviewing the claim and authoritative artifact.
- Controls/exclusions: finite labels only; no synonym, tone, date, filename, directory, or commit
  inference. A commit alone never proves closure.
- Failure behavior: ambiguity is never guessed; dependent evidence failure retains its state.
- Tests: agreement, contradiction, unknown/inapplicable label, missing/unreadable artifact,
  conflicting evidence, ADR `Accepted` mapping, and commit without lifecycle claim.

### PMH-7 - Proven Stale Handoff Gates

- Primary input: AI Handoff `Immediate Next Step`.
- Authoritative section: exactly that section.
- Supporting evidence: the named artifact, its explicitly linked review, and recorded full commit.
- Supported claims and positive proof: `pending review` or `awaiting review` is stale only when the
  linked review explicitly records final `PASS`; `ready to commit` or `commit pending` is stale only
  when a recorded full commit resolves locally; `implementation ready` is stale only when the named
  artifact explicitly records `Implemented`, `Implementation Reviewed`, or `Closed`.
- Trigger and state: recognized claim plus positive proof `WARNING`; recognized claim without proof
  `OK`; no explicit identifier and recognized phrase `NOT_APPLICABLE`; missing proof target
  `MISSING`; unreadable proof `BLOCKED`.
- Item/evidence: exact gate phrase and proving review, artifact, or commit.
- Remediation boundary: advise updating the handoff after human confirmation.
- Controls/exclusions: both identifier and phrase required. `DAR pending`, `Engineering Brief review
  pending`, `implementation review pending`, `condition closure pending`, and `closeout pending` are
  not additional aliases unless they contain an accepted exact phrase. Dates, timestamps, age, and
  absence of evidence never prove staleness.
- Failure behavior: Git absence makes commit proof `NOT_APPLICABLE`; it does not create staleness.
- Tests: each supported proof path, legitimately pending gate, no identifier, missing/unreadable
  evidence, unsupported phrase, and no Git.

### PMH-8 - Active Release Lifecycle-Label Coherence

- Primary input: Project State optional `Planned Release` and AI Handoff `Current Repository State`.
- Authoritative section: exactly those two sections.
- Supporting evidence: matching `docs/release/checklist-X.Y.Z.md` top-level `Status:` field, opened
  only for the explicit shared release identifier.
- Trigger and state: explicit `Planned`, `Release Candidate`, `Released`, `Post Release Reviewed`,
  or `Deprecated` labels for the same release agree with the checklist `OK`; disagreement
  `WARNING`; no shared release
  identifier `NOT_APPLICABLE`; missing checklist `MISSING`; unreadable or multiply defined status
  `BLOCKED`.
- Item/evidence: release identifier, explicit labels, and checklist path.
- Remediation boundary: advise human review of the conflicting lifecycle labels.
- Controls/exclusions: no semantic-version comparison, ordering, readiness, approval, or release
  blocking. No release lifecycle state is inferred from prose.
- Failure behavior: explicit evidence only; unsupported labels are `NOT_APPLICABLE`.
- Tests: agreement, disagreement, missing/unreadable checklist, valid historical release text
  ignored, and numeric version disagreement left exclusively to Version Consistency Status.

### PMH-9 - Current ADR Authority In Project Brain

- Primary input: Project Brain `Current Decisions`.
- Authoritative section: exactly that section.
- Supporting evidence: resolved ADR explicit status and an explicit replacement ADR when claimed.
- Trigger and state: current `Proposed` or `Accepted` ADR `OK`; `Rejected`, `Superseded`, or
  `Deprecated` presented as current `WARNING`; missing ADR/replacement `MISSING`; unreadable ADR
  `BLOCKED`; ambiguous identifier `WARNING`.
- Historical exception: the same list item may retain the ADR when it contains exactly
  `historical`, `rejected`, `deprecated`, `superseded by ADR NNNN`, or `superseded by ADR-NNNN`;
  replacement identifiers must resolve. Valid historical retention is `OK`.
- Item/evidence: Project Brain item location, ADR status, and resolved path.
- Remediation boundary: advise reviewing the current-decision entry; do not rewrite history.
- Controls/exclusions: no completeness requirement, topic comparison, conceptual supersession,
  inferred replacement, or scan outside `Current Decisions`.
- Failure behavior: unsupported qualifiers do not suppress the warning; resolution follows PMH-4.
- Tests: current accepted ADR, superseded/rejected/deprecated current ADR, each accepted historical
  qualifier, missing replacement, historical material outside the active section, and ambiguity.

## 12. Status Semantics And Aggregation

Only existing states are permitted:

- `OK`: the bounded check completed and found no defined defect; informational only
- `WARNING`: explicit non-blocking contradiction, duplication, ambiguity, or proven staleness
- `MISSING`: mandatory file/structure or explicit required target is absent
- `BLOCKED`: an existing required input cannot be safely read or evaluated
- `NOT_APPLICABLE`: the repository/check genuinely lacks eligible scope or optional context

Category aggregation MUST be:

1. any `BLOCKED` item -> `BLOCKED`
2. otherwise any `MISSING` item -> `MISSING`
3. otherwise any `WARNING` item -> `WARNING`
4. otherwise, if all items are `NOT_APPLICABLE` -> `NOT_APPLICABLE`
5. otherwise -> `OK`, including mixed `OK` and `NOT_APPLICABLE`

`OK` does not certify correctness, completeness, lifecycle approval, or release readiness. No state
changes command exit behavior beyond the existing status contract.

## 13. Module And Function Boundaries

`forge/project_memory.py` MUST remain private and project-memory-specific. It MAY own frozen private
parse-result/error types and functions equivalent to:

- UTF-8 document loading and line-ending normalization
- exact second-level section extraction with duplicate evidence
- non-empty content detection
- supported identifier, commit, lifecycle, and gate-phrase parsing
- deterministic identifier and commit resolution
- extraction of explicit top-level or section status evidence

Names are not prescribed, but responsibilities are. The helper MUST return facts, candidates,
paths, and bounded parse errors; it MUST NOT return `StatusItem`, `StatusCategory`, scores,
remediation, CLI text, or governance decisions.

`forge/status.py` MUST retain:

- `StatusState`, `StatusItem`, `StatusCategory`, `StatusReport`
- all nine rule evaluators and status mapping
- category aggregation and construction
- category composition in `evaluate_status()`
- CLI-facing report rendering

Existing `_rollup_state()` provides the accepted precedence and SHOULD be reused. CLI wiring remains
at the existing boundary.

## 14. Failure Behavior

- Invalid/unreadable target directory before evaluation: existing `StatusServiceError`.
- Non-Forge repository: category `NOT_APPLICABLE`; other categories continue.
- Missing primary file/required section/explicit target: `MISSING`.
- Duplicate required heading, ambiguous identifier, conflicting explicit evidence: `WARNING`.
- Unreadable file/target, invalid UTF-8, or I/O failure preventing a dependent check: `BLOCKED`.
- Malformed near-heading: treated as missing exact structure; no repair or alternate parse.
- Unknown lifecycle label or unsupported prose/link/gate: `NOT_APPLICABLE` for that check.
- Partial memory: available independent files and rules continue.
- No Git: commit-dependent sub-check `NOT_APPLICABLE`; file checks continue.
- Expected project-memory parse or evidence errors use bounded private errors that the Project
  Memory Health boundary converts to the rule-defined conservative state. Unexpected programming
  defects MUST propagate to the existing status-service invalid-execution handling; they MUST NOT
  be silently converted to `OK`, `NOT_APPLICABLE`, or an ordinary repository `BLOCKED` finding.
- Process-level failures that make initial repository evaluation impossible retain existing
  `StatusServiceError`; individual evidence failures MUST NOT crash the entire command when a safe
  informational result can be returned.

Messages MUST avoid unbounded file content, tracebacks, secrets, or claims that Forge fixed state.

## 15. Read-Only Guarantees

Automated tests and manual snapshots MUST prove that evaluation:

- creates, deletes, renames, modifies, or changes permissions on no file or directory
- updates no project memory and creates no review record
- changes no lifecycle or release state
- stages, commits, tags, checks out, or otherwise mutates no Git state
- performs no network call
- persists no report or cache

Advisory remediation text MAY identify a human action but has no authority to perform it.

## 16. Test And Fixture Requirements

Deterministic literal fixtures MUST cover at least:

1. healthy project memory
2. missing `PROJECT_STATE.md`
3. missing `PROJECT_BRAIN.md`
4. missing `AI_HANDOFF.md`
5. missing required section
6. duplicate required active heading
7. empty required current section
8. placeholder-looking text accepted because no placeholder vocabulary is governed
9. valid historical lifecycle statements
10. valid historical release statements
11. unresolved explicit active artifact reference
12. ambiguous explicit artifact identifier
13. external reference ignored
14. explicit active-work contradiction
15. different detail without contradiction
16. stale review gate proven passed
17. stale ready-to-commit gate proven committed
18. stale implementation-ready gate proven advanced
19. legitimately pending gate
20. explicit lifecycle contradiction
21. active release-state disagreement
22. semantic-version disagreement not handled by this category
23. superseded ADR presented as current authority
24. superseded ADR retained only as history
25. malformed Markdown
26. invalid encoding or unreadable file where feasible
27. non-Forge repository
28. repository without Git metadata
29. partial project memory
30. category aggregation precedence
31. coexistence with unchanged Version Consistency Status
32. complete read-only filesystem and Git-state behavior

Additional focused cases in Sections 9-11 are mandatory. Helper parsing/resolution and rule-level
fixtures SHOULD live in a focused new `tests/test_project_memory.py`; existing report composition,
CLI rendering, category order, exit behavior, and Version Consistency regression checks remain in
`tests/test_status.py`. No existing test file is reorganized merely for style. Expected outcomes and
fixture text MUST be literal and independently specified; tests MUST NOT derive all expectations
from implementation tables or constants or depend on the live Forge repository except for the
separately required manual integration run.

## 17. CLI And Output Requirements

Human-readable output MUST follow the existing category shape:

```text
Project Memory Health: <STATE>
  <bounded summary>
  - <rule label>: <STATE> - <evidence-based message>
```

The category MUST preserve existing categories, command name, options, renderer, informational
behavior, and exit policy. It MUST NOT use certification, compliance approval, release readiness,
or repair-authority wording. No JSON, strict mode, flag, command, persisted output, or new
exit-code enforcement is authorized.

User-visible category order MUST place `Project Memory Health` immediately after the existing
`Runtime Project Memory` category and immediately before `Version Consistency Status`. Existing
category relative order MUST remain unchanged. For concise output, each PMH rule emits one `OK`
summary item when all of its eligible instances succeed, one `NOT_APPLICABLE` summary item when it
has no eligible instance, and one item per distinct non-OK finding otherwise. PMH-1 retains one item
per primary file because each file has an independent mandatory result. This cardinality changes no
aggregation semantics.

## 18. Documentation Requirements

Implementation MUST update only documentation made inaccurate by actual behavior, as applicable:

- `README.md`
- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md` only for a genuinely durable implementation decision
- `AI_HANDOFF.md`
- `CHANGELOG.md`
- applicable documentation indexes
- implementation verification and formal review handoff evidence

Before formal implementation review, documentation MUST say implementation is complete but pending
formal review; it MUST NOT say the slice or brief is closed, released, or approved for release.

## 19. Implementation Sequence

1. Read governing documents, accepted slice/DAR, and current status implementation.
2. Run the existing status tests to record the regression baseline.
3. Inspect current project-memory contracts and real file structures.
4. Define literal mappings, fixture content, and independent expected outcomes.
5. Add focused parsing-contract tests and implement the private section/reference helper.
6. Add rule-level tests and implement individual evaluators in `forge/status.py`.
7. Reuse deterministic aggregation and compose the new category at the exact approved position.
8. Complete remaining deterministic fixtures and integration/regression tests.
9. Run manual healthy and inconsistent fixtures and verify filesystem and Git read-only behavior.
10. Update accurate project documentation and implementation evidence.
11. Run complete verification and inspect the complete diff and excluded surfaces.
12. Prepare formal implementation-review handoff.

Implementation MUST follow the AI Implementation Protocol and stop on any ambiguity that would
broaden these boundaries.

## 20. Verification Requirements

Required verification:

- targeted Project Memory Health tests
- existing `forge status` tests
- full `pytest` suite
- Ruff lint
- Ruff format check
- `git diff --check`
- manual `forge status` run against this Forge repository
- manual run against a healthy temporary fixture
- manual run against a deliberately inconsistent temporary fixture
- before/after filesystem comparison proving read-only behavior
- before/after Git status comparison proving no Git mutation
- confirmation that Version Consistency outcomes remain unchanged
- complete changed-file and exclusion-scope inspection

Exact commands and results MUST be recorded in the formal implementation-review handoff.

## 21. Completion Criteria

Implementation is complete only when:

- all nine rules are implemented exactly
- primary inputs remain limited to three files
- supporting reads remain explicit-claim-driven
- active and historical boundaries are preserved
- no semantic inference or excluded behavior exists
- aggregation uses the accepted precedence
- the private helper and status ownership boundaries are preserved
- `forge status` remains read-only and informational
- targeted, regression, full-suite, lint, formatting, manual, and read-only checks pass
- documentation accurately records implementation pending formal review
- the formal implementation-review handoff is ready

Completion does not itself authorize commit, closure, Release Candidate creation, tagging,
publication, or release.

## 22. Formal Review Handoff

The Implementation Agent MUST provide Review Authority with:

- accepted EB-005 identifier and implementation scope
- changed-file list and explicit exclusions confirmation
- rule-by-rule implementation traceability
- module-boundary evidence
- exact targeted and full verification results
- healthy, inconsistent, non-Forge, no-Git, and read-only manual evidence
- confirmation that Version Consistency behavior is unchanged
- known limitations and unresolved findings
- rollback readiness
- statement that no release transition is implied

Formal implementation review MUST occur before commit or closure under the Lifecycle Standard.

## 23. Risks And Rollback Considerations

- False positives: controlled through exact active sections, finite tokens, and positive proof.
- Parser growth: controlled through one private facts-only helper and status-owned evaluation.
- General-consistency creep: controlled through claim-driven single-target reads.
- Version-check duplication: controlled by excluding semantic-version comparison.
- Partial/corrupt input: controlled through per-rule conservative states and continued evaluation.
- False authority: controlled through informational wording and unchanged exit behavior.

Rollback is bounded: remove the category composition and its status evaluators, remove the private
helper and focused tests, and revert only documentation describing Project Memory Health. Rollback
MUST NOT change the three project-memory files being inspected, existing status categories, or
Version Consistency behavior.

## 24. Blocking Questions

None. Formal review resolved the narrow exactness findings without expanding CS-002.3 or
DAR-CS-0003.

## 25. Lifecycle And Authority

Current state: `Implementation Ready`.

- Product Owner selected CS-002.3.
- Design Authority approved the slice through DAR-CS-0003 `PASS`.
- Chief Architect owns and accepts this bounded implementation brief.
- Review Authority completed formal Engineering Brief review with `PASS`.
- Quality Authority retains verification authority.
- Implementation Agent is authorized only for the bounded scope in this brief and MUST follow the
  AI Implementation Protocol.
- Release Authority has no decision or transition in this work.

The next permitted state is `Implemented` only after all authorized changes, tests, documentation,
and verification are complete. Implementation review, commit, closure, and release gates remain
separate and MUST NOT be skipped.
