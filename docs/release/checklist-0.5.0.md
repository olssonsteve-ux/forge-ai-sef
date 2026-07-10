# Forge 0.5.0 Release Plan And Checklist

Status: Planned

Release Authority decision date: 2026-07-10

Target version: `v0.5.0`

Release classification: pre-`1.0` minor release

## Release Objective

Publish the reviewed EB-004 Universal Bootstrap Output Contract implementation as the release that
introduces `forge-bootstrap/2.0.0`.

## Intended Scope

- exactly eight universal bootstrap directories
- exactly eight generated files
- removal of only the historical generated `forge/` placeholder
- no replacement source-code directory
- generated README and AI handoff architecture-discovery guidance
- language-neutral generated `.gitignore`
- dry-run and success reporting of `forge-bootstrap/2.0.0`
- three changed template versions `1.0.0` and complete bootstrap-template compatibility
  `>=0.5,<0.6`
- runtime and package version metadata `0.5.0`

## Excluded Scope

- project profiles
- source-layout selection
- migration tooling or automatic migration
- existing-project inspection or modification
- new CLI commands or flags
- package publication
- release automation

## Compatibility Decision

Release Authority rejects the previous compatibility proposal. All three changed templates use
`>=0.5,<0.6`, the narrowest range that includes the implementing release without claiming
unverified compatibility with Forge 0.3 or 0.4. DAR-EB-0003 preserves the previous range as
historical review evidence. The other five bootstrap templates receive only the same compatibility
metadata alignment so the complete template set validates under Forge 0.5; their generated content
and template versions are unchanged.

Historical generated projects are not migrated. Populated directories remain project-owned,
existing layouts may remain indefinitely, and empty placeholders require deliberate manual action.

## Release Dependencies

- DAR-EB-0003 condition-closure review returned `PASS`.
- EB-004 implementation was committed after review approval as
  `5c926759591f617a8245526cdc27cdfd10dbb8e5` and the Engineering Brief is closed.
- Final candidate validation and version consistency must pass.
- Known limitations and rollback instructions must remain current.
- Release Authority must separately authorize `Release Candidate` and `Released` transitions.

## Test And Validation Expectations

```text
python -m pytest tests/test_init.py
python -m pytest
python -m ruff check .
python -m ruff format --check .
git diff --check
```

Manual validation must compare dry-run and actual output path-by-path, confirm exact counts, inspect
generated guidance, verify no unresolved variables, and confirm no generated `forge/` or `src/`.

## Known Limitations

- Unexpected filesystem failures may leave partial output, consistent with existing behavior.
- No automatic migration or migration tooling exists.
- Template compatibility is intentionally limited to Forge `0.5.x` until broader compatibility is
  separately verified and governed.
- Formal condition closure, commit, release-candidate approval, and release approval remain pending.

## Packaging Decision

Forge `0.5.0` remains local editable only. Package-index publication is not authorized.

## Rollback Readiness

Rollback may restore the previous folder plan, identity plumbing, CLI reporting, three template
versions and contents, tests, documentation, and version metadata. Rollback must not modify any
generated project or rewrite accepted ADR and contract history.

## Planned Checklist

- [x] Release classification selected.
- [x] Target version selected.
- [x] Template compatibility range selected.
- [x] Runtime and package version metadata aligned.
- [x] Focused DAR-EB-0003 condition-closure review passes.
- [x] Implementation commit is created after review approval.
- [x] EB-004 implementation closeout is recorded.
- [ ] Final release-candidate validation passes.
- [ ] Version consistency evidence is accepted.
- [ ] Release notes and changelog are finalized.
- [ ] Release Authority authorizes tagging.

## Tagging Decision

Ready to tag v0.5.0: NO
