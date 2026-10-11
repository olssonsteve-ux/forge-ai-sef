# Project State

## Status

Forge Concept v1.0 is frozen; public testing publication 1.0.0rc1 is in preparation.
Bounded independent code review PASS; stable release acceptance remains BLOCKED
by real Codex runtime qualification (V1-Q-01). Full 258 tests, lint and format pass. Public-candidate package checks and independent review pass.
The current work is governed by ADR 0019 and the consolidated
[assurance record](docs/engineering/Forge-1.0-assurance.md). This file owns current status.

## Current Version

Latest completed release: v0.4.1. Public testing package: 1.0.0rc1, tag v1.0.0-rc.1.
Publication state is recorded in docs/release/checklist-1.0.0-rc.1.md.

## Planned Release

1.0.0 â€” packaged locally after all acceptance evidence and independent review pass.
The owner authorized commit, push, public GitHub access and MIT licensing on 2026-10-11.
[Public testing checklist](docs/release/checklist-1.0.0-rc.1.md).
[Stable acceptance checklist](docs/release/checklist-1.0.0.md) remains blocked.

## Current Objective

Resolve the host runtime policy/profile mismatch, qualify real execution and fresh read-only
review/apply, finish the bounded Audio maintenance task, then independently accept 1.0.

## What Exists

- Bootstrap with eight output paths and 1.x template compatibility; read-only project status.
- Explicit language-neutral verification with bounded subprocess lifetime/output.
- Isolated task snapshots, immutable authority, hash-linked events, explicit retry and apply.
- Codex CLI adapter with separate execution/review sessions and explicit sandbox policy requests.
- Proportionate record ownership under ADR 0018.
- Historical FAL source and all review/correction evidence retained.

## What Does Not Exist

- Accepted stable 1.0 implementation, automatic commits, release automation or cloud service.
- Qualified alternative providers, CLI versions or platforms.
- Accepted autonomous FAL correction loop; this is outside stable distribution scope.

## Architectural Posture

Use the deterministic stable kernel and one qualified external runtime. Agent outputs are evidence,
not authority. Preserve original files until verified explicit apply. No new Python runtime
dependencies. See ADR 0019 and the assurance record for precise contracts and qualification.

## Next Recommended Work

Run the saved real qualification script in a supported environment that permits the bounded
workspace action. Both tested CLI versions currently receive read-only/tool-policy rejection.
See V1-Q-01 in the assurance record; do not bypass policy or weaken checks.
Public testing publication is explicitly authorized. Do not infer stable acceptance from it.

## Preserved experimental disposition

FAL-001 remains TERMINATED BLOCKED, unaccepted and unclosed under HD-FAL-002 / DISP-FAL-001.
FAL-002 remains implemented, failing acceptance and unclosed. IR-FAL-004 preserves concrete residuals:
IR1-01/05 OPEN, IR1-04 partially addressed; IR1-03 original no-intent bypass eliminated.
Frozen IR1-02/06/07 remain verified, not reopened. CORR-003 repaired sealed COMMITTED publication.
Structural evidence remains 3,318/3,400 LOC, four modules, two adapters, five surfaces, no new
dependencies for FAL. These limits apply to that experimental scope, not the new stable kernel.
See [IR-FAL-004](docs/reviews/IR-FAL-004-CORR-003-targeted-re-review.md) and linked prior records.
No finding was renamed or closed to obtain stable-release scope.

## Repository baseline

Existing repository C:/Users/olsso/Documents/forge-ai-sef, main,
e8d8ed05d23e5229109139836101d036fb27a7e1. Authorized uncommitted changes retained; no reset.
Audio Recorder is a separate repository; its implementation evidence is not Forge release evidence.
