# FAL-002 First-Trial Measurement Plan

Status: Specified; trial not authorized or started

Planned trial subject: Manual Digital Album Authoring and Export

The album capability specification is intentionally absent. This plan becomes executable only after
FAL-002 is separately reviewed, implemented, reviewed and human-closed, and after the album
capability gate is separately authorized.

## Baseline

Use the Audio Recorder/FAL retrospective as historical baseline only where evidence is reliable:
elapsed calendar time, commit sequence/days, manually repeated deterministic facts that can be
counted, artifact/review counts and known evidence gaps. Do not infer worked hours, model-active time,
relay count or cost where they were not recorded.

## Measures

| Measure | Collection rule |
| --- | --- |
| Total elapsed time | UTC first authorized gate transition to final disposition; never label as worked time. |
| Active execution and human wait | Sum recorded intervals separately; unknown remains unknown. |
| Time to first runnable vertical slice | First committed artifact satisfying a predefined runnable criterion. |
| Human decisions and decision cards | Count IDs, owner, waiting interval and disposition. |
| Human relay/copy-paste steps | Count only explicitly recorded transfers. |
| Automatically collected evidence | Count distinct provenance-bound Git/build/test/diff fields. |
| Manually reported deterministic facts | Count human-entered branch/HEAD/diff/build/test/warning/skip/file facts. |
| Prompt/work-packet size | UTF-8 bytes and tokens only when actually exposed. |
| Corrections and no-progress stops | Count per complete series, including findings retained across identities. |
| Review findings | Count by severity, criterion, disposition and recurrence. |
| Criterion coverage | Covered/total with resolvable references; separate from test count. |
| Test count | Passed/failed/skipped, never used as a proxy for criterion coverage. |
| Duplicated governance statements | Count repeated authoritative facts outside references/generated views. |
| Token/API cost | Record only exposed usage and determinable cost. |
| Blocked time | UTC intervals in blocked/awaiting-human states. |
| Scope changes | Count human-authorized changes; loop-authored changes must remain zero. |
| Runtime size | Production modules, non-test logical lines, adapters, schemas and dependencies. |

## Initial targets

- zero manual copying of branch, HEAD, changed files, diffstat, build result, test totals, warnings,
  errors or skips;
- one run record as the authority for deterministic execution evidence;
- no more than two automatic corrections and zero correction-budget reset by run identity;
- zero loop-authored scope or criterion changes;
- every human question represented by a decision card;
- zero PASS outcomes containing an open CRITICAL/blocking finding;
- 100% accepted-criterion coverage by resolvable source/locator/hash/provenance references plus
  reviewer semantic rationale;
- explicit separation of Standard-Assurance fresh review from High-Assurance independence claims;
- FAL-002 implementation within its module/line/adapter/schema/dependency limits;
- no claimed speed or quality improvement until the trial is complete and compared.

No arbitrary lead-time reduction target is set because reliable worked-time baseline data does not
exist. The final trial report must distinguish verified facts, derived measures, user observations,
inferences and unavailable information.
