# FAL-002 First-Trial Measurement Plan

Status: `AWAITING TARGETED HUMAN REVIEW`; trial not authorized or started

Decision basis: `HD-FAL-003`

Planned trial subject: Manual Digital Album Authoring and Export

The album capability specification is intentionally absent. This plan becomes executable only after
FAL-002 is separately reviewed, implemented, reviewed and human-closed, and after the album
capability gate is separately authorized.

## Baseline and comparison freeze

Only preserved, verifiable raw evidence may populate the Audio Recorder/FAL baseline. Historical
values must not be estimated or reconstructed. Missing values remain `UNKNOWN`. Before the album
trial starts, a human-approved comparison record must freeze the baseline artifacts and comparison
objects and document differences in scope, criteria, production-code change, test extent and risk
class. Normalization per criterion or comparable capability is permitted only when its formula and
inputs are frozen in that record.

If fewer than two primary friction measures have comparable baselines, no causal efficiency claim is
permitted and the efficiency result is `INCONCLUSIVE`.

## Operational definitions

- **Prompt:** a human- or machine-relayed instruction that starts or materially redirects a separate
  execution. Automatically generated internal calls are counted separately from human prompts.
- **Separate execution:** a separately started executor, collector, reviewer or recovery run with its
  own execution identity. Retries count and are labelled as retries.
- **Manual handoff:** manual copying, assembly or forwarding of state, evidence, prompt or decision
  between steps that the loop could technically transfer. A required human decision is not itself a
  handoff; decision waiting and any relay friction are recorded separately.
- **Defect escape:** a frozen-scope, criterion, authority-rule or closure-invariant violation that
  existed when a gate received PASS or closure eligibility, was not reported as blocking by the
  deciding review and was found after disposition. Its criterion, severity, detection phase and
  missed-control reason must be recorded.
- **Human decision time:** time in `awaiting_human` or an equivalent decision state. It is separate
  from active machine execution and technical waiting.

## Measure register

`UNKNOWN` is a required value, not a zero. Raw sources are provenance-bound records or artifacts;
the trial report must link their identities and hashes.

| Name | Definition | Unit | Raw source | Baseline | Collection method; start → end | Target / decision threshold | Comparability | Data-quality limit | Class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Calendar time | Elapsed gate duration, never worked time | hours | append-only transitions | UNKNOWN | subtract UTC timestamps; authorization → final disposition | diagnostic; lower is favorable | same transition semantics; disclose scope/risk differences | clock gaps make interval UNKNOWN | Secondary |
| Active execution time | Recorded active machine execution only | seconds | execution intervals | UNKNOWN | sum non-overlapping intervals; each execution start → end | diagnostic; lower is favorable | same adapter roles and interval rules | uninstrumented intervals remain UNKNOWN | Secondary |
| Human decision time | Time awaiting an identified human decision | hours | state series + decision cards | UNKNOWN | sum decision-state intervals; awaiting-human entry → decision disposition | excluded from machine inefficiency | same decision-state semantics | unavailable timestamps remain UNKNOWN | Diagnostic |
| Technical wait time | Non-human machine wait, queue or retry backoff | seconds | execution events | UNKNOWN | sum classified wait events; technical-wait start → end | diagnostic | same event taxonomy | mixed human wait invalidates value | Diagnostic |
| Manual handoffs | Manual transfers matching the definition above | count | handoff events + human confirmation | UNKNOWN | count qualified events; first work packet → disposition | primary 25% improvement candidate | same eligible step boundaries | unrecorded activity cannot be inferred | Primary |
| Human prompt count | Human prompts matching the prompt definition | count | prompt/work-packet events | UNKNOWN | count human-origin qualified events; authorization → disposition | primary 25% improvement candidate | same material-redirection rule | chat text without event identity is not counted | Primary |
| Machine-relayed prompt count | Machine-relayed external instructions, excluding internal calls | count | prompt events | UNKNOWN | count machine-relayed qualified events; authorization → disposition | report separately; no standalone success target | same execution boundary | cannot be merged with human prompts | Diagnostic |
| Internal call count | Automatically generated calls within one execution | count | adapter/runtime events | UNKNOWN | count internal-call events; execution start → end | diagnostic | same instrumentation boundary | unavailable instrumentation remains UNKNOWN | Diagnostic |
| Separate execution count | Executor, collector, reviewer or recovery starts with identities | count | execution records | UNKNOWN | count unique starts by identity; authorization → disposition | primary 25% improvement candidate | same role set; retries reported separately | missing identity invalidates count | Primary |
| Retry count | Separate executions explicitly caused by retry | count | execution records | UNKNOWN | count retry-labelled starts; authorization → disposition | no unexplained retries | same retry classification | inferred retries are prohibited | Secondary |
| Manually transcribed repository facts | Human-entered Git/build/test/diff facts | count | run records + provenance classification | UNKNOWN | classify and count human-origin fields; authorization → disposition | exactly 0 | same deterministic-fact field set | unclear provenance fails target | Primary |
| Correction rounds | Authorized automatic corrections in complete series | count | correction series | 2 for FAL-001; product-comparison baseline otherwise UNKNOWN | count linked correction transitions; first correction request → disposition | ≤2; no identity reset | same complete-series rule | missing predecessor link invalidates count | Secondary |
| No-progress stops | Stops caused by unchanged diff/evidence or repeated finding | count | state/review/correction records | UNKNOWN | count reason-coded stops; correction start → stop/disposition | all predefined fixtures detected; observed count diagnostic | same hash and recurrence rules | absent detector evidence is not zero | Secondary |
| Blocking review findings | CRITICAL or explicitly blocking findings before disposition | count by severity/criterion | reviewer results | UNKNOWN | aggregate structured findings; first review → disposition | quality guardrail, not minimized | same severity/blocking policy | reviewer rationale required | Diagnostic |
| Defect escapes | Escapes matching the definition above | count by criterion/severity/phase | post-disposition defect register | UNKNOWN | classify confirmed defects; disposition → album retrospective and before second capability evidence | 0 CRITICAL/HIGH | same observation window and taxonomy | open observation yields INCONCLUSIVE | Primary quality |
| Criterion evidence coverage | Criteria with resolvable binding and reviewer rationale / total | percent | manifest, run record, reviewer result | UNKNOWN | resolve and divide covered by total; evidence-ready → deciding review | exactly 100% | same accepted criterion set; normalized per criterion | test count is not evidence coverage | Primary quality |
| Test and verification result | Passed/failed/skipped plus required command outcomes | counts + exit codes | collector raw command records | UNKNOWN | parse bound raw outputs; command start → end | all required checks pass; skips/warnings reported | compare command set and test extent explicitly | missing raw output/hash is UNKNOWN | Primary quality |
| Time to runnable slice | Time to first committed artifact satisfying a predeclared runnable criterion | hours | Git history + frozen criterion | UNKNOWN | subtract verified timestamps; authorization → qualifying commit | diagnostic unless comparable baseline exists | identical runnable rule or documented normalization | post-hoc criterion prohibited | Secondary |

## Outcome rule

The trial produces one of `PASS`, `FAIL` or `INCONCLUSIVE` for practical value.

`PASS` requires all of the following:

1. manually transcribed deterministic repository facts equal zero;
2. at least one comparable primary friction measure improves by at least 25%;
3. no other comparable primary friction measure worsens by more than 10% without documented human
   justification;
4. human decision time is not counted as machine inefficiency;
5. 100% of closure criteria have resolvable evidence and reviewer rationale;
6. no open CRITICAL or blocking finding exists at PASS;
7. no review result is default-converted to PASS;
8. executor and reviewer cannot approve or close their own work, and closure remains human-only;
9. every predefined false-PASS, early-closure and blocking-finding fixture is detected; and
10. no CRITICAL or HIGH defect escape is found during the observation period.

`FAIL` results when comparable verified evidence demonstrates that any mandatory target or quality
condition is violated. `INCONCLUSIVE` results when a required baseline, raw source, comparability
record or observation period is insufficient to decide PASS or FAIL. Unknowns never default to PASS.

Defect-escape observation continues through the album capability retrospective and must finish
before a second product capability may be cited as evidence of FAL-002 effectiveness. Technical
operation alone is not improvement: FAL-002 must reduce measured friction or lead time without losing
the controls that prevented premature FCS-001 closure.

The final report must distinguish verified facts, derived measures, human observations, inferences
and unavailable information.
