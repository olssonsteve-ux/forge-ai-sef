# DAR-EB-0003 - EB-004 Universal Bootstrap Implementation Review

## Review Status

Final status: PASS.

Original review result: PASS WITH CONDITIONS.

Focused condition-closure review: PASS on 2026-07-10.

Lifecycle status: Completed.

## Reviewed Implementation

EB-004 - Implement Universal Bootstrap Output Contract 2.0.0.

## Review Date

2026-07-10

## Reviewed Sources

- `docs/engineering/EB-004-Implement-Universal-Bootstrap-Output-Contract.md`
- `docs/architecture/AR-0002-Generated-Project-Source-Layout.md`
- `docs/reviews/DAR-AR-0002-Generated-Project-Source-Layout.md`
- `docs/decisions/0017-generated-project-source-layout.md`
- `docs/contracts/forge-init-spec.md`
- `docs/contracts/bootstrap-template-system.md`
- `templates/governance.md`
- `forge/bootstrap.py`
- `forge/cli.py`
- `tests/test_init.py`
- `templates/bootstrap/README.template.md`
- `templates/bootstrap/AI_HANDOFF.template.md`
- `templates/bootstrap/gitignore.template`
- `README.md`
- `PROJECT_STATE.md`
- `PROJECT_BRAIN.md`
- `AI_HANDOFF.md`
- `CHANGELOG.md`
- `docs/README.md`
- `docs/release/EB-004-universal-bootstrap-output-contract-readiness.md`

## Summary

The EB-004 implementation correctly realizes `forge-bootstrap/2.0.0`. Universal bootstrap now
plans and generates exactly eight contracted directories and eight generated files, creates no
source-code directory, reports one consistent output-contract identity, remains template-driven,
preserves existing safeguards, and adds no migration or project-profile behavior.

Automated and independent manual verification pass. One factual README overstatement was corrected
during review so the unreleased working-tree behavior is not attributed to released Forge `v0.4.1`.

The implementation cannot receive an unconditional `PASS` because EB-004 assigns the implementing
release target and template compatibility range to Release Authority. No recorded Release Authority
decision supports the exact `>=0.3,<0.5` bounds or selects the pre-`1.0` release target. The range is
mechanically valid and includes both runtime `0.3.0` and package baseline `0.4.1`, but that evidence
does not substitute for the required authority.

## Traceability Assessment

Every implementation change is authorized by EB-004, ADR 0017, or the accepted bootstrap contracts.
The implementation does not reopen the architecture decision, alter `forge-bootstrap/2.0.0`, add a
replacement source layout, introduce profiles or migration, or expand `forge init` beyond its
approved command and option surface.

## Exact Output And Output Plan

The single `FOLDER_PATHS` tuple contains the eight contracted directory paths. The existing ordered
`TEMPLATE_OUTPUTS` mapping remains the single file plan and maps exactly eight accepted templates to
the eight contracted files. Dry-run and write execution derive their paths from the same collections.
Counts are derived from `InitResult` collections rather than separately maintained numeric values.

Independent generation confirmed:

- directory count: `8`
- file count: `8`
- dry-run versus actual directory differences: `0`
- dry-run versus actual file differences: `0`
- generated `forge/`: absent
- generated `src/`: absent
- other source, package, framework, or profile directories: absent

The target root and temporary parent are not counted. Forge's internal `forge/` package remains
present; only the authorized `forge/bootstrap.py` and `forge/cli.py` files changed within it.

## Bootstrap Output Identity

`BOOTSTRAP_OUTPUT_CONTRACT = "forge-bootstrap/2.0.0"` is the single authoritative identity. It is
independent of `forge.__version__`, contains no `v` prefix, enters rendering through
`default_variables()`, and is copied into `InitResult.output_contract` for CLI presentation. The
result field carries the constant value and does not define a second authority.

README and AI handoff templates require the variable, generated output contains the exact identity,
both CLI modes report it, and tests prove missing or unknown variables fail validation. Independent
generation found no unresolved identity token.

## Template And `.gitignore` Assessment

Only the three EB-004-authorized templates changed. README and AI handoff template versions advance
to `1.0.0` because a required variable and governed meaning changed. Both remain language-neutral,
state that source omission is intentional, and direct language, packaging, deployment, and source
layout decisions to architecture discovery.

The `.gitignore` template advances to `1.0.0`. It removes exactly `__pycache__/`, `.pytest_cache/`,
and `.venv/`. It preserves `.DS_Store`, `Thumbs.db`, `.env`, `.env.*`, `dist/`, and `build/` in their
original order. No unrelated ignore redesign occurred.

## Compatibility Range Assessment

Under `docs/contracts/bootstrap-template-system.md`, `compatible_forge_versions` identifies Forge
releases that may render a template. It is not the bootstrap-contract version or template version.
Runtime validation currently evaluates the field against `forge.__version__`, which is `0.3.0`;
project package metadata and current release-facing documentation identify `0.4.1`.

The proposed `>=0.3,<0.5` range is objectively parseable, includes `0.3.0` and `0.4.1`, and does not
conflict mechanically with the current baseline. However, EB-004 explicitly makes the exact
template compatibility range a Release Authority decision before implementation completion. The
lower and upper bounds have no recorded Release Authority approval. The range therefore remains a
material open governance condition, not an implementation-code failure.

## CLI, Safeguard, And Test Assessment

Dry-run and success reporting use the result identity, derive counts from actual plan collections,
state `Source layout: not selected`, and provide the accepted architecture-discovery next step. No
command, flag, interaction, migration option, profile selection, or unrelated validation behavior
was added.

Project-name validation, target containment, non-empty target rejection, template discovery,
metadata validation, required-variable validation, unknown-variable rejection, deterministic
rendering, template-driven content, and dry-run no-write behavior remain intact.

The twelve focused tests use literal expected directory and file collections instead of importing
`FOLDER_PATHS` or `TEMPLATE_OUTPUTS`. They cover exact sets and counts, missing source directories,
dry-run equivalence, reporting, identity distinction, generated guidance, `.gitignore`, missing and
unknown variables, overwrite protection, compatibility parsing, and internal package presence. The
full relevant suite passes.

## Non-Migration Assessment

The runtime diff contains no historical-layout discovery, existing-project inspection, rename,
delete, move, rewrite, migration metadata, migration command, or profile logic. Compatibility
remains documentation-only and prospective.

## Documentation And Release Evidence Assessment

Project memory accurately records implementation pending review conditions. The changelog remains
under `Unreleased` and claims no release or closure. The README now distinguishes working-tree
behavior from released `v0.4.1`. The authority map links the governing decision, brief, evidence,
and this review.

The readiness record contains exact output, identity, compatibility, limitations, rollback,
automated verification, independent manual comparison, and implementation-review dependency. It
remains unaccepted while the Release Authority conditions are open.

## Changed-File Classification

| Classification | Files | Assessment |
| --- | --- | --- |
| Implementation | `forge/bootstrap.py`, `forge/cli.py` | Authorized |
| Tests | `tests/test_init.py` | Authorized |
| Templates | README, AI handoff, and `.gitignore` bootstrap templates | Authorized |
| Documentation | `README.md`, `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, `AI_HANDOFF.md`, `CHANGELOG.md`, `docs/README.md` | Authorized |
| Release evidence | EB-004 readiness record | Authorized |
| Unrelated | None | None detected |

## Findings

### Finding 1 - Template Compatibility Range Lacks Required Authority

Severity: Material condition.

The `>=0.3,<0.5` range is coherent with the versions it currently covers, but EB-004 assigns the
exact range to Release Authority. No durable Release Authority decision accepts those bounds.

Required action: Release Authority must accept the range for the selected implementing release or
authorize a corrected range. If metadata changes, rerun template, targeted, full-suite, lint,
format, whitespace, and manual-generation verification.

### Finding 2 - Implementing Release Target Is Not Selected

Severity: Material lifecycle condition, not a runtime defect.

EB-004 requires Release Authority to select and record the pre-`1.0` release classification and
target version before implementation completion or release-evidence acceptance. No target is
recorded.

Required action: Release Authority must record the classification and target before this
implementation can be committed as accepted implementation work or advance to `Implementation
Reviewed`.

### Corrected Finding - README Release Attribution

Severity before correction: Material documentation ambiguity.

The README described `forge-bootstrap/2.0.0` immediately after stating the repository is released as
`v0.4.1`, which could attribute unreleased behavior to that release. The review qualified the text
as uncommitted EB-004 behavior under review and explicitly excluded it from `v0.4.1`.

## Verification

Independent review verification:

```text
python -m pytest tests/test_init.py   -> 12 passed
python -m pytest                      -> 26 passed
python -m ruff check .                -> passed
python -m ruff format --check .       -> passed
git diff --check                      -> passed
```

Independent temporary dry-run and actual generation confirmed `8` directories, `8` files, zero
set differences, equal identity reporting, no writes from dry-run, resolved template tokens,
required generated guidance, exact `.gitignore` content, and no generated `forge/` or `src/`.

## Conditions

1. Release Authority must select and record the pre-`1.0` release classification and target version.
2. Release Authority must accept `>=0.3,<0.5` as the truthful template compatibility range for that
   release or authorize a corrected range and its required reverification.
3. Review Authority must perform a focused condition-closure review before the implementation is
   committed or marked `Implementation Reviewed`.

## Original Decision

PASS WITH CONDITIONS.

The runtime behavior, output contract, templates, CLI, tests, safeguards, non-migration boundary,
and verification satisfy EB-004. The implementation is not ready to commit, close, release, or
advance to `Implementation Reviewed` until all conditions are closed and recorded.

## Focused Condition-Closure Review

### Closure Scope

This focused review re-evaluated only the two original Release Authority conditions, the version
and compatibility metadata changes required to resolve them, resulting tests and release evidence,
and direct regressions that those corrections could introduce.

### Release Authority Evidence

Release Authority accepted a pre-`1.0` minor release with target `v0.5.0` and accepted
`>=0.5,<0.6` as the template-compatible Forge release range. The decision, date, rationale,
rejected prior proposal, compatibility boundary, and pending release gates are recorded in:

- `docs/release/EB-004-universal-bootstrap-output-contract-readiness.md`
- `docs/release/checklist-0.5.0.md`

The release remains `Planned`; it is not a Release Candidate, tagged, published, or completed.

### Version And Identity Assessment

- `forge.__version__`: `0.5.0`
- `pyproject.toml` project version: `0.5.0`
- planned release: `v0.5.0`
- bootstrap output contract: `forge-bootstrap/2.0.0`
- changed template versions: `1.0.0`
- compatible Forge range: `>=0.5,<0.6`

These identities remain distinct and consistent. Generated `FORGE_VERSION` is `0.5.0`; the
bootstrap output-contract identity remains unchanged.

### Complete Template-Set Assessment

All eight bootstrap templates declare exactly `>=0.5,<0.6`, include Forge `0.5.0`, and exclude
earlier and later minor series. The three EB-004 content templates retain their authorized content
and `1.0.0` versions. The other five templates changed only the
`compatible_forge_versions` metadata line; their bodies, variables, versions, ownership, output
mappings, and generated behavior are unchanged.

Complete template-set validation required the five metadata-only updates because template loading
validates every bootstrap asset against the active Forge version before rendering.

### Closure Review Correction

The review added one narrow independent test that pins runtime version, package version, and default
`FORGE_VERSION` rendering context to literal `0.5.0`. The generated README assertion now also checks
literal Forge `0.5.0`. This closes the evidence gap where generated content previously followed the
runtime constant without independently checking the accepted release target.

No production behavior or template content changed during condition-closure review.

### Closure Verification

```text
python -m pytest tests/test_init.py   -> 13 passed
python -m pytest                      -> 27 passed
python -m ruff check .                -> passed
python -m ruff format --check .       -> passed
git diff --check                      -> passed
```

Additional verification confirmed:

- all eight templates validate with `>=0.5,<0.6`
- runtime and package versions both equal `0.5.0`
- the rejected range is absent from active implementation, project memory, and readiness records
- manual generation creates exactly eight directories and eight files
- dry-run writes nothing
- generated `forge/` and `src/` remain absent
- generated README reports Forge `0.5.0` and `forge-bootstrap/2.0.0`
- generated README and AI handoff contain no unresolved output-contract token
- output plan, CLI surface, safeguards, source-layout policy, and migration policy are unchanged

### Condition Closure

1. Release classification and target Forge version: CLOSED.
2. Template compatibility range: CLOSED.

Remaining condition findings: none.

### Final Decision

PASS.

DAR-EB-0003 conditions are fully closed. The EB-004 implementation is ready to commit. It is not
closed or released, and `v0.5.0` is not ready to tag; commit, closeout, release-candidate validation,
and separate Release Authority transitions remain pending.

## Implementation Commit And Closure Eligibility

Implementation commit:
`5c926759591f617a8245526cdc27cdfd10dbb8e5`

The committed file set contains the complete reviewed EB-004 implementation, tests, bootstrap
templates, product-version metadata, project documentation, project memory, release evidence, and
this review record. The post-commit working tree was clean, and no unrelated files were included.

Closure eligibility: CONFIRMED.

- final implementation-review result: `PASS`
- original review conditions: closed
- unresolved implementation findings: none
- implementation commit: recorded
- release follow-up: separately tracked in `docs/release/checklist-0.5.0.md`

EB-004 may transition from `Implementation Reviewed` to `Closed` under the Forge Lifecycle
Standard. This eligibility record does not alter the review decision and does not authorize any
release transition.
