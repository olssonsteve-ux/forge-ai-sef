# Forge 1.0.0-rc.1 public testing publication

Date: 2026-10-11.
Purpose: freeze Forge Concept v1.0 and open the existing implementation for public testing.
Package version: 1.0.0rc1. Tag: v1.0.0-rc.1. GitHub release: prerelease, not latest stable.
Distribution: public GitHub repository, wheel and sdist assets; no PyPI publication.

## Authority and baseline

The owner explicitly requested v1 freeze, GitHub push and public testing, and selected the MIT
License. This supersedes earlier no-commit/tag/push restrictions for Forge. Audio Recorder is
a separate repository and is not included in this publication.

Verified local repository: C:/Users/olsso/Documents/forge-ai-sef, main,
HEAD e8d8ed05d23e5229109139836101d036fb27a7e1. Index was empty; existing uncommitted work preserved.
GitHub main f596eebe251f0a77eb2525c91ae123a602e5f0bb is an ancestor, 51 commits behind.
Publication uses ordinary fast-forward push; no reset, force push or history rewriting.

## Scope and review

The [concept baseline](../Forge-Concept-v1.0.md) and [intent](../../INTENT.md) define the public promise.
Existing candidate implementation and independent code-review evidence remain governed by ADR0019
and the [assurance record](../engineering/Forge-1.0-assurance.md).

Publication preparation adds the MIT license, public intent, contribution guidance, an honest
prerelease identity and installable archives. Runtime changes are limited to the reported version and bootstrap compatibility parsing:
rcN versions now compare before final releases and malformed versions raise a domain error.
Fourteen regression cases cover ordering and rejection. The task runtime is unchanged. Bootstrap template revision remains 1.0.0; compatibility includes 1.0.0rc1 explicitly.
No historical finding is closed. No stable v1.0.0 tag is authorized by this checklist.

## Known limitations

V1-Q-01 remains OPEN: actual bounded agent execution, fresh read-only review and apply did not
complete in the build environment. The observed tool-policy rejection reproduced with the target
CLI 0.160.0 and a separate 0.162.1 probe; root cause is unresolved. Package checks do not qualify it.
Windows x64 / CPython3.14 is the qualification target; cross-platform support is not claimed.
Verification commands are trusted operator code. No multi-file atomic apply guarantee is offered.
FAL experiments remain excluded from installed runtime code and retain all existing dispositions.

## Publication gates

- [x] Owner publication authority and MIT license choice.
- [x] Concept scope frozen; stable acceptance failure remains visible.
- [x] Repository/history credential-pattern and private-artifact inspection.
- [x] Final automated suite, lint, format and whitespace checks.
- [x] Wheel/sdist built; license included; clean installed CLI smoke.
- [x] Final publication consistency review and recorded checksums.
- [ ] Commit and clean working tree.
- [ ] Fast-forward push, public visibility and prerelease assets verified.
- [ ] Hosted CI result inspected.

Technical publication gates: PASS. Commit, hosted CI and publication confirmation follow below.
Ready to tag v1.0.0-rc.1: YES after the reviewed commit is clean and hosted CI is green.
Ready to tag stable v1.0.0: NO (V1-Q-01).

## Verification evidence

- Full suite: 258 passed in 58.53 seconds; lint PASS; format PASS (29 files).
- Focused bootstrap suite: 27 passed, including 14 new prerelease/invalid-version cases.
- Independent publication reviewer: PASS; 16 independently executed focused checks passed.
  Scope: intent, concept, license, public claims, prerelease parsing and packaging instructions.
  This review did not independently scan history or inspect final binary archives.
- Installed package: 16 CLI/archive checks PASS; isolated environment pip check PASS.
- Targeted credential-pattern scan: 191 current files and 556 historical blobs, no matches or
  suspicious credential filenames. This is a bounded inspection, not a guarantee of no secrets.
  Ignored build directories, task workspaces, caches and credentials are outside the commit.
- Default git diff --check PASS. Project memory/status checks retain all 18 required sections.
- Final hashes and limitations: [machine evidence](evidence-1.0.0-rc.1.json).
- A failed first packaging check caught numeric-only version parsing; rcN support and negative
  regression tests corrected it before publication. No failed artifact is uploaded.
- Stable V1-Q-01 qualification was not rerun or accepted. Existing FAL findings are unchanged.

## Hosted CI toolchain correction

The first hosted run (38144008372, commit 77396c9) passed all 258 tests and lint but failed format:
unbounded ruff>=0.8 installed Ruff 0.17.0, which also formats Markdown code blocks and requested
rewriting the frozen EB-006 oracle. Local verification used Ruff 0.15.20.
Pin the existing development dependency to 0.15.20 so local and hosted checks use the same reviewed
formatter. This adds no runtime dependency and changes no frozen record. The candidate packages
are rebuilt with the corrected development metadata; old draft assets are replaced before publication.
