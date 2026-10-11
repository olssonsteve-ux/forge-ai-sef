# Forge 1.0 — stable workflow assurance record

Date: 2026-10-11. Status: bounded code review PASS; overall 1.0 acceptance FAIL (runtime qualification BLOCKED). Owner request: complete every step
of the researched delivery plan to stable 1.0. This single record owns capability, engineering
brief, design/implementation reviews, tests and remaining work under ADR0018. No commit/tag/push.

## Capability and architecture decision (ADR 0019)

Stable Forge consists of compatible init/status, explicit verification configuration, and a bounded
local task workflow. An implementation agent works only in an isolated snapshot; a new read-only
Codex process reviews the verified result. Forge owns the authoritative task/event state and apply
checks. The local Codex CLI is an optional external prerequisite, not an imported SDK dependency.
Provider-neutral task/result contracts permit later qualified adapters, but 1.0 supports only Codex.

The previous FAL-001/adaptive_loop and FAL-002 modules remain unchanged in source with their failed
or terminated dispositions. Exclude them from wheel and sdist code; stable CLI must not import them.
This is explicit stable-release scope quarantine, not repaired FAL acceptance or disappearance of
its findings. Existing FAL limits stay binding for those source modules. New task code does not
reuse their schemas or claim their autonomous correction/recovery contract. It provides the safety
outcomes below with explicit operator-driven retry/apply instead of automatic correction loops.

Alternative rejected: squeeze remaining FAL fixes into 82 LOC and certify a 5,000-line historical
oracle quickly. Independent architecture assessment identified missing authority/freshness/error/
recovery behavior and recommends a smaller separately reviewed stable kernel. Building another LLM
SDK is also rejected: reuse the locally installed and authenticated Codex runtime.

## Public contracts

Keep forge init <name> [--dry-run] and read-only forge status. Add forge verify [--config PATH]
with explicit shell-free argv commands, IDs, relative working directories, timeout and required
programs. Configuration is operator-authored trusted executable policy, never downloaded or authored
by an agent into effect. Version-1 TOML has schema_version=1, required_tools=[...], [[checks]] with
id, argv, cwd='.', timeout_seconds (1..3600). At least one check, bounded count/size; unknown fields,
duplicate IDs and malformed entries reject. Missing required tools or executable return BLOCKED;
nonzero status is FAIL; timeout/interruption is BLOCKED. Output is bounded and redacted. No command
runs during status or preflight. Verification runs only on an explicit verify/run invocation.

Task commands: create ID --spec PATH, show ID, run ID, resume ID --reason TEXT, apply ID.
ID is ASCII [a-z0-9][a-z0-9-]{0,47}; no path traversal. Spec version 1 binds objective, scope (exact
relative files or directory prefixes), criteria [{id,text}], config path, allow_dirty, and explicit
authorization {execute:true, review:true, tool_network:bool}. Scope cannot include .git, .forge,
forge.toml or the selected configuration, which remain operator authority. No secret files or
symlinks/reparse points are copied. Model output cannot alter the task/configuration/authorization.

Creation records real repository root, Git HEAD, index digest and full tracked/nonignored file
hash map (excluding .forge/tasks), plus canonical spec/config digest. Dirty roots require explicit
allow_dirty. Snapshot copy must exactly match the captured map before READY, including uncommitted
bytes. Existing original files remain untouched until explicit apply. Copy constraints are bounded:
20,000 files, 256 MiB per file, 1 GiB total; a larger project blocks rather than truncates.

Task storage: .forge/tasks/ID/{events,workspace,config.json}. A single OS advisory lock prevents
concurrent commands for a task and releases after process death. Events are create-only, numbered
canonical UTF-8 JSON with previous hash and record hash; flushed and reread. Reject malformed,
noncanonical, gapped, unknown or conflicting records. No summary pointer conveys authority. OS user
and repository owner are trusted; hashes detect corruption, not malicious full-history replacement.
A partial write blocks and is retained for inspection. Never recursively delete user trees.

Exact task states: READY -> EXECUTING -> EXECUTED -> VERIFYING -> VERIFIED -> REVIEWING ->
READY_FOR_APPLY -> APPLYING -> APPLIED. Agent/check/contract failure appends BLOCKED or
NEEDS_CHANGES. Every external action has a flushed start event before invocation. Unknown outcome
(EXECUTING, VERIFYING, REVIEWING, APPLYING after process death) cannot silently rerun. Explicit
resume with reason authorizes revalidation/retry; retain workspace and original snapshot. Resume
may return READY for execution/check/review failures; APPLYING can only resume validated apply,
never execute again. APPLIED is terminal; it does not mean committed/released/human-closed.

Before each external action, validate chain, spec/config hashes, original repository HEAD/index/
file snapshot and workspace containment. Recheck original immediately before apply. Changes outside
scope, changes to copied configuration, symlinks, unknown files and review-time mutation block.
Snapshots compare hashes rather than timestamps. Verification must pass on the same candidate that
is reviewed/applied; any post-verification workspace change invalidates readiness.

Codex adapter uses explicit process argv, stdin prompt, no shell, no user config/rules, ephemeral
fresh sessions, sandbox workspace-write for execution / read-only for review, never approval bypass,
no extra writable directories, and explicit sandbox tool-network policy. Existing ChatGPT login is
used; no credentials are copied. Capture real thread.started ID, completed turn, usage, runtime
version, selected model policy, process termination, prompt digest and structured last message.
Version qualification initially targets CLI 0.160.0; incompatible versions fail preflight.
A run starts a separate reviewer after execution and deterministic verification. Session IDs must
differ. Process timeout/cancel/output limit terminates the process tree; no unknown outcome is PASS.
Any interruption leaves durable non-success state. No automatic retries or provider fallbacks.

Executor result is a bounded summary, not approval. Reviewer result is PASS/NEEDS_CHANGES/BLOCKED,
with per-criterion verdict/rationale; exact criterion coverage is required for PASS. Forge controls
source hash, command results and observed session identities; returned metadata cannot replace them.
Review is advisory evidence, not release authority. Missing or malformed output cannot yield readiness.

Apply operates only on the recorded verified candidate, only scoped changed files, and only while
original baseline is unchanged. Retain per-file original bytes before replacement. Write an apply
manifest before changes; atomic per-file replace, no-overwrite creation and explicit file deletion
are journaled. This is not a multi-file filesystem transaction. On interruption, retain backups and
manifest; explicit apply retry checks each path is either its old or intended value, rejecting a
third-party edit. No Git reset, staging, commit, tag, merge, push, or release is performed.

## Engineering brief and acceptance

Implementation files: new forge/workflow.py, forge/evidence.py, forge/verification.py,
forge/codex_runtime.py, forge/process_guard.py; CLI/status/bootstrap/packaging/templates and dedicated tests. No new runtime
Python dependencies. Stable artifact must include bootstrap templates and exclude experimental code.
Template compatibility is versioned for >=1.0,<2.0; eight existing output paths remain. Existing
projects are never automatically migrated. Documentation explains task records and optional Codex.

Required tests: wrong root/HEAD/index/dirty snapshot, malformed/duplicate data, authority missing,
config mutation, scope escape, symlink/reparse, concurrent lock, partial/gapped records, timeout,
interrupt, malformed agent response, forged session/criteria, review mutation, stale candidate,
crash before/after stage/apply, refusal to replay uncertain work, preserved originals and safe retry.
Real CLI execution+fresh review in an isolated small repository; Audio Recorder snapshot verification
and bounded maintenance dogfood. Mock tests never substitute for the real agent qualification.

Packaging: build wheel/sdist, inspect contents, install wheel in a clean environment, run init/status/
verify/task CLI smoke, verify template availability and absence of experimental imports. Supported
release baseline initially Windows x64/Python 3.11–3.14; portability tests/CI may cover Linux but
unexecuted platform claims must be labelled. Unit/lint/format/diff and project memory checks required.

Release candidate can be locally packaged without commits. Tag/publication readiness remains NO
under the user's no-commit constraint and release standard. Do not describe a candidate as published.

## Design review

Independent reviewer forge_review: PASS on 2026-10-11 after the six conditions below were resolved. Implementation review remains pending.

## Implementation evidence and findings

Pending. Prior evidence: 183 Forge tests and concrete FAL defects in IR-FAL-004. Current runtime
preflight: Codex CLI0.160.0, existing ChatGPT login; real read-only ephemeral invocation returned
FORGE_RUNTIME_PROBE_OK with observed thread.started and turn.completed events on 2026-10-11.
No new key or provider SDK was installed.

## Design conditions resolved — 2026-10-11

These clarifications supersede ambiguous shorthand above:

- Acquire per-task OS lock for every mutating task command AND repository-wide apply lock before
  original validation/mutation. Recheck every destination ancestor for symlink/reparse and current
  bytes immediately before replacing. External non-Forge writers are not locked out: detectable
  interference blocks, and no general concurrent-writer transaction guarantee is claimed.
- Before first apply mutation, persist operation/path/old digest or ABSENT/new digest or ABSENT/
  backup locator in one APPLYING event. Durably save/reread required backups first. Retry accepts
  only old/new values for that journal's paths and unchanged values elsewhere, with identical
  HEAD/index. A third value blocks. Reuse the journal, never rebaseline ambiguous partial apply.
- Snapshot exactly Git tracked plus nonignored files except protected .git/.forge/.codex/.agents/
  .aws/.ssh directories, any .env or .env.* filename, and operator-declared excluded_paths in the
  version-1 config. Record excluded names, never read/copy those bytes. Do not claim arbitrary
  remaining content is secret-free: operator must classify project-specific secrets through
  excluded_paths. Scope cannot authorize excluded paths. Ignored inputs/dependencies are not copied;
  checks requiring them must provision explicitly or fail. No ambient credentials copied to snapshot.
- Config also declares artifact_dirs, defaulting to __pycache__, .pytest_cache, .ruff_cache, bin,
  obj, build, dist, node_modules and .venv. Newly generated files under these directory names are
  excluded from candidate authority/publication. Files present in the initial snapshot remain
  authoritative even under those names. Artifacts never enter apply; mutable config is rejected.
- Scoped new files are allowed. Unknown OUT-OF-SCOPE files or modifications reject. Compare candidate
  hash maps before/after verification and review; verification may produce only excluded artifacts,
  otherwise readiness fails. Capture final authoritative candidate before review and require exact
  identity before apply. Every retry increments an attempt number, retains workspace bytes, appends
  explicit reason, and discards previous readiness. Re-execution/reverification/fresh review are
  mandatory for a new attempt; no previous PASS is reusable. APPLIED never restarts.
- Runtime flags are qualified in a real write/read-only roundtrip before acceptance. Ignore user
  config and rules, disable project instruction discovery when supported by qualified CLI, use no
  additional writable directories, explicit sandbox and never-approval policy. The prompt carries
  selected project context. Credential ownership remains with installed Codex. Provider network
  needed for authenticated model calls is distinct from the explicitly configured tool-network
  policy. Verification commands are trusted operator code, not sandboxed untrusted commands.
- Qualified release platform is Windows x64 with CPython 3.14 initially. Earlier Python versions
  may be syntactically compatible but are not declared tested; CI must earn additional claims.

Independent design review before these clarifications: PASS WITH CONDITIONS (forge_review agent).
The six explicit conditions are resolved by the contract above and require implementation tests.

Task schema additionally permits agent_timeout_seconds (integer 1–3600, default 600).
Scope entries match exact files and descendants. APPLYING is resumed with explicit task apply,
not task resume. Protected/excluded content newly created in a workspace blocks.

## Final verification and independent implementation review â€” 2026-10-11

**Overall 1.0 acceptance decision: FAIL â€” live-runtime qualification BLOCKED.**
**Bounded deterministic implementation review: PASS.** This is a local, uncommitted candidate,
not a stable release. No human closure, commit, tag or publication has occurred.

### Verified baseline and retained boundaries

Repository: C:/Users/olsso/Documents/forge-ai-sef; branch main; HEAD
e8d8ed05d23e5229109139836101d036fb27a7e1, equal to the recorded starting HEAD.
Index remains empty. Authorized prior uncommitted CORR-003/ADR0018 work and subsequent v1 work
remain in the working tree. No reset/discard or implementation commit was performed.
Fixture commits exist only in disposable, explicitly isolated test repositories.

Governing authority: owner request to finish Forge 1.0 using Audio Recorder lessons; Constitution,
engineering conduct, implementation/lifecycle standards, ADR 0018, ADR 0019, the accepted design
and clarifications in this record, and docs/release/release-standard.md. Prior FAL reviews and
HD-FAL-023 remain authority for their separate frozen scope. Their failed disposition is preserved.

Five new modules own evidence, process lifetime, verification, Codex transport and orchestration.
The installed package has 11 Python files including __init__/__main__ (nine substantive modules).
There is one Codex transport and one existing direct runtime Python dependency, Typer; no new
runtime Python dependency was added. See the generated candidate manifest for exact source hashes.
FAL remains 3,318/3,400 counted LOC, four modules, two adapters, five surfaces and no new dependency.
Stable modules do not enter the experimental FAL import graph; experimental modules are absent
from both wheel and sdist. Their acceptance has not been repaired by quarantine.

### Independent findings and closure

Reviewer: separate forge_review agent; no implementation edits by reviewer.

| Finding | Original failure | Correction and independent verification | Status |
| --- | --- | --- | --- |
| V1-IR-01 | Partial creation wrote incomplete bytes directly into an original path, preventing safe retry | Unique durable same-volume staging; atomic no-overwrite hard-link publication; fault injection confirms destination remains absent after partial staging and retry completes | CLOSED |
| V1-IR-02 | Windows mixed-case names bypassed exclusion/config protection | Casefold comparisons for scope, exclusions, configuration and artifact policy; negative alias tests | CLOSED |
| V1-IR-03 | A process could spawn children before Job Object assignment | CREATE_SUSPENDED, assign job, NtResumeProcess; kill-on-close ownership; actual delayed-child write and timeout tests | CLOSED |
| V1-IR-04 | Extended Windows path aliases were mistaken for another repository | samefile root check plus normalized stored identity; create/run/apply across aliases | CLOSED |
| V1-Q-01 | Real Codex exec cannot perform the required workspace action in this host environment | Explicit settings, isolated environment and official newer CLI compatibility probe still yield read-only/tool-policy rejection; deterministic tests correctly reject unchanged result | OPEN â€” qualification blocker |

Initial independent implementation review was FAIL for IR-01/02/03. Re-review independently ran
57 stable tests, including the process cleanup failures, and confirmed all three corrected.
Final bounded re-review independently ran four further cases for extended paths, ancestor Git
discovery, .NET status and structured CLI errors. Verdict: PASS for reviewed deterministic code;
no further material code defect established. Targeted lint and whitespace passed. Packaging and
Audio results below are coordinator evidence; reviewer did not independently rerun those.

Git ceiling configuration prevents accidental discovery of the original ancestor repository from
snapshot commands. It is not a security sandbox. Tests check that an unqualified git rev-parse
inside a snapshot cannot find the original. Windows sandbox permission enforcement is a separate
live qualification requirement.

### Tests and package verification

- python -m forge verify: PASS; full pytest 244 passed, lint PASS, format PASS (28 Python files
  at the full-suite run). Additional qualification-script lint/format checks pass.
- New stable tests: 61, covering external state, dirty/staged/HEAD changes, missing authority,
  corrupted/gapped records, scope/config mutation, secret exclusion, Windows case aliases,
  junctions, concurrent locks, interruption and explicit retry, failing/side-effecting checks,
  reviewer freshness/criteria/mutation, stale candidate, partial apply, preserved backups,
  process timeout/output limits/descendant cleanup, and installed-command error contracts.
- Historical suite retained. Previously frozen FAL invariants not redesigned/reopened.
- Build wheel and sdist from source; rebuild wheel from sdist via python -m build. PASS.
- Inspect both archives: no experimental FAL runtime code; eight bootstrap templates and user
  guide included. Wheel Python bytes match current source.
- Clean venv install with no system-site packages; pip check PASS. Installed Typer 0.27.3 and its
  transitive dependencies resolved under the unchanged Typer requirement.
- scripts/verify_package.py: 16 installed checks PASS, including isolated import origin, absent
  FAL modules, dry-run nonmutation, eight bootstrap outputs, status, explicit verification,
  task create/show and negative run/resume/apply paths. No model call is claimed by this smoke.
- Repository whitespace and project-memory schema checks PASS. Version-status warnings correctly
  disclose package target 1.0.0 versus last tag v0.4.1 and an uncommitted working tree.
- CI configuration now targets Windows/Python3.14. No hosted CI run is claimed without push.

### Audio Recorder application of the workflow

Separate original baseline: main/ae09df414060664de85daf8d5b394bb7d7744f9f.
Added explicit forge.toml with locked restore, full .NET tests and check-only formatting; ignore
local .forge task storage. First snapshot correctly failed formatting on four pre-existing
WHITESPACE diagnostics. Applied formatter only to those four files; verified non-whitespace
character streams unchanged. No audio behavior or dependency changed.

Second isolated snapshot: locked restore PASS (1.559s); full tests PASS (616 tests, 27.188s);
format --verify-no-changes PASS (14.562s). Evidence: build/audio-snapshot-verification-2.json.
Snapshot files and original baseline are separately preserved. Hardware tests remain opt-in and
were not rerun for whitespace-only changes. Prior real-audio evidence and native-UI limitation
remain in Audio Recorder's own record.

The bounded maintenance task was created, but actual agent maintenance/review/apply is NOT claimed
complete: V1-Q-01 blocks that gate. No forged reviewer result or test double substitutes for it.

### Live runtime observations and remaining gate

Codex CLI 0.160.0 login/preflight and fresh ephemeral session creation work. Actual exec attempts
with workspace-write, never-approval, explicit working root, ignored user config/rules, native
Windows sandbox and isolated environment nevertheless report read-only and reject a shell read
with "blocked by policy". Debug prompt rendering reports workspace-write, so the root cause is
not conclusively established. Do not call it a confirmed upstream defect or weaken policy.

Official npm @openai/codex latest was checked (0.162.1), installed only under build/codex-0.162.1,
and probed with the same constrained read. It exhibits the same rejection. Global app/config/auth
were not changed. This probe does not qualify 0.162.1 or add it to accepted adapter versions.

The final reproducible script is python -m scripts.qualify_runtime. Its final-code run recorded
BLOCKED under build/runtime-qualification-55f287e5077a48959efd3db0aec8fc12/qualification.json,
session 01a12ae5-9bdd-78f3-b710-4aa30783ab4b. The original greeting remains unchanged; deterministic
verification failed as expected, no reviewer ran and no apply occurred. Earlier probes remain
preserved under build/real-roundtrip-1. Model claims never override command failure.

To finish 1.0: resolve the host runtime policy/profile mismatch through supported configuration in
an environment authorized for the bounded workspace action; rerun real execution, checks, fresh
read-only review and apply; demonstrate write/read/network boundaries; complete Audio maintenance
dogfood; obtain independent acceptance of that evidence; rebuild and freeze package hashes.
Do not use bypass flags, alter global policy, copy credentials or weaken checks to obtain PASS.

### Administration, commit and closure readiness

Current project-memory files decreased from 1,055 baseline lines to 133 lines, preserving their
18 required sections and links to durable decisions/reviews. This measures removed repetition,
not a claimed productivity improvement. One assurance record owns this work item's detailed evidence.

Implementation ready to commit as stable 1.0: NO â€” qualification remains incomplete.
Ready to tag/publish/close: NO. FAL-002 remains unaccepted and unclosed.
Recommended next governance step: resolve V1-Q-01 and finish real qualification, then independent
release acceptance. Only after separate commit authorization: "feat: add verified isolated Forge
task workflow and streamline assurance records". No commit was made.

Final package/source hashes and baseline: [candidate evidence](../release/evidence-1.0.0.json).
Final archive inspection and clean installed smoke: 16 checks PASS; lint PASS; format 29 files PASS;
normal repository git diff --check PASS. Nonstandard core.autocrlf=false falsely treated existing
CRLF as added trailing whitespace; repository-configured normalization is the applicable check.

## Subsequent public testing authorization - 2026-10-11

The owner subsequently authorized freezing the v1 concept, committing/pushing Forge and opening
GitHub for everyone to test, and explicitly selected the MIT License. Prior no-publication statements
above describe the earlier review baseline. This new authority permits a clearly labelled prerelease;
it does not convert V1-Q-01 to PASS or authorize a stable v1.0.0 implementation claim.
The public version is 1.0.0rc1 / v1.0.0-rc.1. Publication evidence and new artifact hashes are owned
by [the public testing checklist](../release/checklist-1.0.0-rc.1.md). Historical candidate hashes
remain evidence for their earlier baseline. FAL dispositions and acceptance gates are unchanged.
