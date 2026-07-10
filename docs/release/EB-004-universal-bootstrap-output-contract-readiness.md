# EB-004 Universal Bootstrap Output Contract Implementation Readiness

Status: DAR-EB-0003 condition-closure review `PASS` — implementation ready to commit

Date: 2026-07-10

Owner: Implementation Agent

Governing brief: `docs/engineering/EB-004-Implement-Universal-Bootstrap-Output-Contract.md`

Bootstrap output contract: `forge-bootstrap/2.0.0`

## Release Classification And Target

Release Authority decision: `ACCEPTED` on 2026-07-10.

- Release classification: pre-`1.0` minor release
- Target Forge version: `v0.5.0`
- Accepted template compatibility range: `>=0.5,<0.6`

The change is user-visible and contract-level: universal output moves from nine directories to
eight, removes the historical generated `forge/` placeholder, adopts `forge-bootstrap/2.0.0`, and
publishes three major template versions. A minor release provides the clearest pre-`1.0` boundary.

The previous compatibility proposal is rejected because it excludes `v0.5.0` and compatibility
with Forge 0.3 was not verified for the new required rendering variable. `>=0.5,<0.6` is the
narrowest verified claim: it includes the implementing release and avoids unsupported backward
compatibility. DAR-EB-0003 preserves the previous range as historical review evidence.

No release, tag, publication, or packaging change is authorized by this implementation record.

## Included Change

The implementation removes only the historical generated `forge/` placeholder from universal
bootstrap output. It does not replace that directory with `src/` or any other source-code layout.
Forge's repository-internal `forge/` Python package remains present.

The generated directory plan is exactly:

```text
docs/
docs/architecture/
docs/contracts/
docs/decisions/
docs/vision/
standards/
templates/
tests/
```

The generated file plan is exactly:

```text
README.md
PROJECT_STATE.md
PROJECT_BRAIN.md
AI_HANDOFF.md
CHANGELOG.md
ROADMAP.md
LICENSE
.gitignore
```

## Output Identity And Guidance

`forge/bootstrap.py` defines the single runtime identity
`BOOTSTRAP_OUTPUT_CONTRACT = "forge-bootstrap/2.0.0"`. The value is supplied through
`default_variables()`, required by the generated README and AI handoff templates, carried by
`InitResult.output_contract`, and reported by dry-run and successful generation.

Generated README and AI handoff content state that no source-code directory was created
intentionally and direct language, packaging, deployment architecture, and source-layout selection
to project architecture discovery.

## Compatibility Statement

- No existing project is inspected or modified.
- No automatic migration, rename, removal, movement, or rewriting exists.
- Populated directories remain project-owned.
- Existing layouts may remain indefinitely.
- Empty historical placeholders require deliberate manual action under project governance.
- No migration tooling or project-profile behavior is included.

All three changed template compatibility ranges are `>=0.5,<0.6`. The five otherwise unchanged
bootstrap templates use the same range as a compatibility-only metadata alignment required for the
complete template set to validate under Forge `0.5.0`; their content, variables, mappings, and
template versions are unchanged. Runtime and package version metadata are aligned to `0.5.0`. The
range refers to Forge release compatibility, not `forge-bootstrap/2.0.0` or template versions.

## Known Limitations And Unresolved Risks

- Commit, implementation closeout, release-candidate validation, and release approval remain
  pending.
- Forge product version, template version, and bootstrap output-contract identity remain separate
  namespaces; maintainers must preserve that separation.
- Unexpected filesystem failures can still leave partial output, consistent with existing
  `forge init` behavior and outside EB-004 scope.

## Validation Evidence

Automated verification on 2026-07-10:

- `python -m pytest tests/test_init.py`: `13 passed`
- `python -m pytest`: `27 passed`
- `python -m ruff check .`: passed
- `python -m ruff format --check .`: passed; `7 files already formatted`
- `git diff --check`: passed

Manual verification used separate `dry-project` and `actual-project` targets under a unique system
temporary directory outside the repository:

- dry-run target created: no
- dry-run directory count: `8`
- actual directory count: `8`
- dry-run versus actual versus contracted directory differences: `0`
- dry-run file count: `8`
- actual file count: `8`
- dry-run versus actual versus contracted file differences: `0`
- generated `forge/` present: no
- generated `src/` present: no
- generated README identity and guidance present: yes
- generated AI handoff identity and guidance present: yes
- unresolved `BOOTSTRAP_OUTPUT_CONTRACT` token present: no
- temporary verification directory removed after comparison: yes

The final code-diff audit found no existing-project inspection, migration, profile selection,
rename, removal, move, or rewrite behavior. Forge's internal `forge/` package remains present.
EB-004 changes `forge/bootstrap.py` and `forge/cli.py`; Release Authority condition resolution also
aligns only `forge/__init__.py` version metadata to `0.5.0` within that package.

Release Authority condition-resolution verification on 2026-07-10:

- `python -m pytest tests/test_init.py`: `12 passed`
- `python -m pytest`: `26 passed`
- `python -m ruff check .`: passed
- `python -m ruff format --check .`: passed
- `git diff --check`: passed
- all eight bootstrap templates validate with `compatible_forge_versions: ">=0.5,<0.6"`
- runtime version: `0.5.0`
- package version: `0.5.0`
- rejected range in active implementation, project memory, and readiness documentation: absent
- output-contract identity, folder plan, file plan, CLI scope, and migration policy: unchanged
- manual dry-run reported `8` directories and `8` files without writing a target
- manual generation produced `8` directories and `8` files, no `forge/` or `src/`, rendered Forge
  `0.5.0`, and retained `forge-bootstrap/2.0.0`

## Rollback Readiness

A rollback can restore the prior `FOLDER_PATHS` entry, remove output-contract rendering and result
plumbing, restore prior CLI reporting, restore the three affected template versions and content,
and revert the focused tests and implementation documentation. Rollback MUST NOT modify any
generated project and MUST leave ADR 0017 and the accepted contracts unchanged unless later
governance supersedes them.

## Implementation Review

Implementation-review artifact:
`docs/reviews/DAR-EB-0003-EB-004-Universal-Bootstrap-Implementation.md`

Original implementation-review result: `PASS WITH CONDITIONS`

Focused condition-closure result: `PASS`

Release Authority resolution:

1. Release classification and target resolved as pre-`1.0` minor release `v0.5.0`.
2. Template compatibility resolved as `>=0.5,<0.6`; the prior proposal is rejected and retained
   only in DAR-EB-0003 as historical review evidence.

Review Authority verified traceability, exact output, identity separation, template behavior,
safeguards, compatibility boundaries, verification evidence, and absence of migration, profile, or
replacement-source behavior. Both original conditions are closed. The implementation is ready to
commit but remains unclosed and unreleased; release-candidate and release transitions require
separate evidence and authority.
