# Forge Adaptive Loop V1 Contract

Status: Implemented, pending independent acceptance review

Owner: Forge Design Authority

## Purpose and scope

Adaptive Loop V1 replaces manual deterministic fact transfer with validated state, bounded adapter
execution, provenance-bound evidence, adversarial review and explicit human decisions. Its runtime
is `forge/adaptive_loop.py`; its machine contract is
`schemas/forge-adaptive-loop-v1.schema.json`; its controlled manifest is
`fixtures/adaptive-loop-v1/gate.json`.

V1 is a local library and fixture, not a new CLI command, SaaS, general workflow engine, model,
multi-agent platform, release service or Audio Recorder feature. It has no paid/live-model test
dependency. Forge policy always outranks adapter output.

## State authority

The authoritative state is a schema-versioned manifest plus its append-only transition history.
Allowed transitions are:

```text
draft -> awaiting_human | ready | blocked
awaiting_human -> ready | blocked
ready -> executing | blocked
executing -> evidence_ready | awaiting_human | blocked
evidence_ready -> reviewing | blocked
reviewing -> correction_required | awaiting_human | blocked | accepted
correction_required -> executing | awaiting_human | blocked
accepted -> closed
blocked, closed -> terminal
```

An executor cannot transition directly to `accepted` or `closed`. `accepted` means a schema-valid
PASS established technical eligibility; a separate human/governance act is required for `closed`.
`BLOCKED` and `INCONCLUSIVE` are terminal adverse outcomes and cannot be converted to PASS.
Transition sequence and from/to continuity are validated; an earlier adverse history item cannot be
removed without invalidating the authoritative record supplied for validation.

Natural-language adapter output is data. Only deterministic Forge functions validate and apply a
transition. Source comments, tests and prompts have no policy authority.

## Frozen contract and deterministic prompt

At run start Forge hash-freezes capability/gate identity, scope, non-goals, criteria, allowed paths,
baseline commit, evidence requirements, correction budget and generated prompt. Mutation produces a
`frozen contract changed` error. The correction count is mutable bounded control state, but its
maximum is frozen. A new run identity therefore cannot reset the gate's correction budget.

The prompt compiler serializes only the frozen execution contract, evidence/report format and
budget with sorted keys and a versioned template. Identical manifest and template inputs produce
identical UTF-8 bytes and SHA-256. `created_at` is a deterministic reference to the recorded run
start, not nondeterministic template content. The compiler does not call a model or synthesize
requirements.

## Decision and risk ownership

Humans own product goals/value, priority, scope/non-goals, criteria, residual risk, material
architecture lock-in, release/external publication, destructive/external actions, OS restart or
shutdown, and exceeded budgets. Decision cards contain the exact question, need, owner, at least
two realistic options with consequences/reversibility, recommendation, blocked work and deadline.
They remain pending; recommendations are never silent defaults.

Codex may choose reversible technical details inside frozen scope. Forge owns state, transition
policy, evidence policy, limits and measurement. A separate reviewer adapter receives only a
read-only packet and cannot write implementation or mutate criteria.

Risk is local to each criterion. Six 1–5 dimensions are mandatory: consequence, uncertainty,
irreversibility, evidence difficulty, external impact, and security/data-integrity exposure. The
declared Lite/Standard/High-Assurance level and rationale are visible. A human override requires
recorded rationale and cannot weaken frozen criteria.

## Evidence and adapter boundaries

`collect_command` records exact argv, UTC start/end, elapsed duration, status, exit code, stdout,
stderr and subprocess provenance, including timeout and partial output. `create_run_record` records
repository/run identity, baseline/final Git facts when supplied, cleanliness, files/diff, commands,
runtime/build/test facts, raw-log references/hashes, review/correction/decision data and available
usage/cost. Missing values remain `unknown` or `not available`. A green test claim without a
successful test command is rejected. Secrets matching credential/token patterns are redacted.

The executor adapter receives the frozen prompt and packet and returns structured data. It cannot
alter policy or accept a gate. Tests use controlled fakes. A future live adapter must add enforced
time/cost/command/scope limits without weakening this contract.

The reviewer packet contains frozen criteria and truth authority, baseline, relevant diff/files,
run record, raw-evidence references, allowed/forbidden policy, prior findings and a distinct reviewer
identity. Its hash makes reproduction testable. Review findings require ID, criterion, severity,
observation, evidence reference, falsified/unsupported claim, minimum remediation and human-decision
flag. PASS requires coverage of every criterion.

## Correction and escalation

The default and maximum automatic correction budget is two. Correction is allowed only from
`correction_required`, inside frozen criteria/path policy. Unchanged diff hashes stop as no progress.
Budget exhaustion, repeated non-progress, human decisions, frozen-contract changes, forbidden paths,
missing/contradictory evidence, or adverse/inconclusive review stop or escalate. No unbounded
AI-to-AI loop exists.

## Mandatory prohibitions

Every V1 manifest forbids push, tag, merge, release, packaging, distribution, version change,
history rewrite, destructive Git, restart/shutdown, external messages and credential reuse. The
fixture command policy is an allowlist and denies arbitrary shell interpretation.

## Controlled demonstration

The focused tests exercise the complete requested journey, including one executable fake-adapter
orchestrator path: ready/executing; deterministic prompt
and hashes; structured executor/evidence; bounded correction then PASS eligibility; third correction
rejection; frozen-criterion and forbidden-file rejection; false-green-test rejection; decision-card
escalation; no-progress stop; adverse-result preservation; append-only history; timeout, partial and
interrupted-run handling; redaction; and the unchanged Audio Recorder closure baseline.

## Read-only historical shadow replay

The replay maps the historical Audio Recorder closure sequence without changing it:

1. `64dbf6c` / review 001 maps to `reviewing -> correction_required` with two findings.
2. Both findings required product/evidence authority beyond the closure-only scope, so V1 would map
   to `awaiting_human`, not self-correct.
3. Human authorization produced bounded remediation `ba0b066`; the historical correction count is
   represented as one, never reset by a new execution identity.
4. Review 002 maps to PASS with a complete crosswalk and technical `accepted` eligibility.
5. Human closure `ae09df4` maps separately to `closed`; product release remains unauthorized.

The replay indicates that one generated run record and reviewer packet could have eliminated
repeated copying of Git/build/test facts. It cannot quantify chat relays or claim that V1 evidence
existed historically, and it does not replace either retained review.
