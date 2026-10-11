# Forge Lifecycle Standard

Status: Accepted

Owner: Forge Design Authority

Last updated: 2026-07-10

## Purpose

Forge uses many durable artifacts: Capability Specifications, Capability Slices, Engineering Briefs, ADRs, reviews, standards, templates, and releases.

Those artifacts need clear lifecycle language. Without a shared lifecycle model, statuses drift across documents, review outcomes become ambiguous, and AI agents can mistake "reviewed", "implemented", "closed", and "released" for the same state.

The Forge Lifecycle Standard defines consistent lifecycle states, transition expectations, ownership, and required evidence.

## Scope

This standard applies to:

- Capability Specifications
- Capability Slices
- Engineering Briefs
- ADRs
- Design Authority Reviews
- Post Release Reviews
- Releases
- Standards
- Templates
- runtime outputs where applicable

Runtime outputs may use lifecycle language only when the output describes an artifact lifecycle. Runtime command results must otherwise use their own status model. Runtime outputs are not durable governed artifacts and must not enter `Withdrawn` or `Archived` under this standard.

## Normative Language

`MUST`, `MUST NOT`, `SHOULD`, and `MAY` are normative. A transition is valid only when its entry criteria, required evidence, and authorizing authority are recorded. A status label without that record does not establish the state.

## Lifecycle State Classes

Forge distinguishes three state classes:

- **Common lifecycle states** describe reusable governance conditions that may apply to multiple artifact types.
- **Artifact-specific lifecycle states** describe a condition local to one artifact type or workflow. They must not be imposed on unrelated artifacts.
- **Release lifecycle states** describe a versioned release and must not be used as a substitute for implementation or closure state on other artifacts.

The Forge Method remains:

```text
Capability -> DAR -> Engineering Brief -> Implementation -> Implementation Review -> Commit -> Close
```

Artifact-specific and release states refine this method; they do not reorder it or transfer authority between roles.

## Record size and ceremony (ADR 0018)

Lifecycle states describe decisions, not document count. Where the governing capability or brief
does not require separate files, one linked assurance record MAY hold scope, design review,
implementation evidence, independent findings and their dispositions. The role, date, decision and
evidence for each transition MUST remain explicit. Independent review MUST remain independent.
Current status belongs in PROJECT_STATE; other memory artifacts link rather than duplicate it.
This consolidation MUST NOT waive a contract-specific gate, budget, stop condition, authority or
required record, and MUST NOT retroactively rewrite historical outcomes.

## Core Lifecycle Principles

- Status MUST be explicit and traceable to evidence.
- Status SHOULD appear near the top of the artifact.
- Status changes MUST update project memory when they change current work or durable direction.
- Every transition MUST identify the authorizing authority, transition date, rationale, and evidence.
- The Implementation Agent MAY supply implementation evidence but MUST NOT approve its own implementation review or closure.
- Review Authority owns review outcomes; Quality Authority owns the sufficiency of quality and validation evidence; Release Authority owns release transitions.
- `Reviewed`, `Completed`, `Closed`, `Withdrawn`, `Archived`, `Deprecated`, and `Superseded` are not synonyms.
- Lifecycle history MUST be append-only or otherwise preserved through version-control history and explicit status-history records.
- Lifecycle states MUST NOT hide uncertainty, unfinished work, or missing evidence.

## Semantic Distinctions for End and Retention States

### Closed

`Closed` means the authorized scope of a finite work artifact is complete, its required review has been accepted, and no further work is expected under that artifact. Closure is a substantive completion decision. It does not mean that the artifact is obsolete or stored outside the active record.

### Withdrawn

`Withdrawn` means the sponsor or governing authority intentionally stopped an artifact before its approved objective was completed. Withdrawal is not successful completion, rejection by a reviewing authority, deprecation, or deletion.

### Archived

`Archived` means a durable artifact is retained as a non-active record after its substantive disposition. Archival is a records-retention state, not a new decision on the artifact's merits. The immediately preceding disposition, such as `Closed`, `Withdrawn`, `Rejected`, `Superseded`, or `Deprecated`, MUST remain recorded in the artifact's status history.

### Deprecated

`Deprecated` means an artifact, template, behavior, or release line remains historically valid but MUST NOT guide new work. Deprecation communicates intentional retirement and MUST identify replacement guidance or state explicitly that no replacement exists.

### Superseded

`Superseded` means a named newer artifact or version has replaced the artifact as current authority. Supersession MUST identify the replacement. A superseded artifact may remain historically valid for decisions made while it was current.

These distinctions are mandatory:

- `Closed` records completed finite work.
- `Withdrawn` records intentionally stopped, incomplete work.
- `Archived` records non-active retention and preserves the prior disposition.
- `Deprecated` warns against new use without necessarily naming a direct successor.
- `Superseded` names the successor that now carries authority.

### Withdrawn and Archived Applicability

| Artifact type | `Withdrawn` | `Archived` |
| --- | --- | --- |
| Capability Specification | Permitted before completion of the approved objective | Permitted after `Withdrawn`, `Rejected`, `Superseded`, or `Deprecated` |
| Capability Slice | Permitted before implementation begins | Permitted after `Closed`, `Withdrawn`, `Rejected`, `Superseded`, or `Deprecated` |
| Engineering Brief | Permitted before implementation begins | Permitted after `Closed`, `Withdrawn`, `Rejected`, `Superseded`, or `Deprecated` |
| ADR | Not supported; `docs/contracts/adr-lifecycle.md` governs the complete ADR status set | Not supported as an ADR status; repository retention preserves the record |
| Design Authority Review or implementation review | Permitted only before a decision is issued | Permitted after `Closed` or `Superseded` |
| Post Release Review | Permitted only before findings or a decision are issued | Permitted after `Closed` or `Superseded` |
| Release | Permitted only from `Planned` or `Release Candidate`, before publication | Permitted only after `Superseded` or `Deprecated` |
| Standard | Permitted before approval, or after approval only before any governed reliance | Permitted after `Withdrawn`, `Rejected`, `Superseded`, or `Deprecated` |
| Template | Permitted before publication | Permitted after `Withdrawn`, `Rejected`, `Superseded`, or `Deprecated` |
| Runtime output | Not supported | Not supported |

The applicability table controls if a broader state description could otherwise be read to permit a transition.

## Common Lifecycle States

The responsible authority named for each state authorizes entry into that state. Where multiple authorities are named, all named authorities MUST approve the transition.

### Draft

- Applies to: Capability Specifications, Capability Slices, Engineering Briefs, ADRs, Design Authority Reviews, Post Release Reviews, standards, and templates.
- Entry criteria: An owner, purpose, and initial scope are recorded.
- Required evidence: Initial artifact content and authorship or ownership record.
- Responsible authority: The artifact owner; the Implementation Agent MAY create a draft only within authorized scope.
- Exit criteria: The artifact is sufficiently formed for a permitted next state, or work is intentionally stopped.
- Permitted next states: `Proposed`, `Specified`, `Approved`, `Completed`, `Withdrawn`, or `Rejected`, but only where the target state applies to that artifact's defined flow.

### Proposed

- Applies to: Capability Specifications, ADRs, standards, templates, and other artifacts whose defined flow explicitly includes proposal review.
- Entry criteria: The problem, proposed content, owner, scope, and review request are recorded.
- Required evidence: Reviewable proposal and traceability to the governing need.
- Responsible authority: Product Owner for product intent and release goals; Chief Architect for architecture, ADRs, standards, and templates.
- Exit criteria: The appropriate authority decides the proposal or returns it for revision.
- Permitted next states: `Approved`, `Specified`, `Rejected`, `Draft`, or `Withdrawn` where the artifact flow permits them.

### Specified

- Applies to: Capability Specifications, Capability Slices, Engineering Briefs, standards, and templates.
- Entry criteria: Scope, non-goals, acceptance criteria, risks, dependencies, and traceability are complete enough for evaluation.
- Required evidence: The reviewable specification and its acceptance criteria.
- Responsible authority: Chief Architect, with Product Owner approval when product intent or capability scope is established or changed.
- Exit criteria: The required approval or review records acceptance, rejection, withdrawal, or replacement.
- Permitted next states: `Approved`, `DAR Approved`, `Implementation Ready`, `Rejected`, `Withdrawn`, or `Superseded` where the artifact flow permits them.

### Approved

- Applies to: Capability Specifications, Engineering Briefs, standards, templates, plans, and ADRs through the ADR-local `Accepted` label.
- Entry criteria: The artifact meets its review criteria and the responsible authority records acceptance.
- Required evidence: Approval record, accepted ADR, review decision, or explicit project-memory decision.
- Responsible authority: Chief Architect for architecture, Engineering Briefs, standards, templates, and ADR alignment; Product Owner additionally approves product intent, capability scope, priority, and release goals.
- Exit criteria: The artifact advances to authorized execution or publication, or a governed retirement/replacement decision occurs.
- Permitted next states: `Implementation Ready`, `Released` for a versioned template only, `Withdrawn` only before execution begins, `Superseded`, or `Deprecated`.

### Implementation Ready

- Applies to: Capability Slices and Engineering Briefs.
- Entry criteria: Required specification and architecture approval are complete; implementation scope, acceptance criteria, constraints, and verification obligations are explicit.
- Required evidence: Accepted specification, applicable DAR or brief approval, implementation scope, and acceptance criteria.
- Responsible authority: Chief Architect. Review Authority MUST have recorded the required DAR outcome for a Capability Slice.
- Exit criteria: Authorized implementation is completed, the work is withdrawn before implementation begins, or the artifact is replaced.
- Permitted next states: `Implemented`, `Withdrawn`, `Rejected` only when a newly discovered blocking issue invalidates readiness, or `Superseded`.

### Implemented

- Applies to: Capability Slices and Engineering Briefs.
- Entry criteria: All authorized changes are complete and the acceptance criteria have been exercised.
- Required evidence: Changed-file inventory, tests, documentation updates, verification results, and known deviations.
- Responsible authority: Implementation Agent attests completion; this attestation does not constitute review approval.
- Exit criteria: Review Authority records the implementation-review outcome or the governing artifact is superseded.
- Permitted next states: `Implementation Reviewed`, `Implementation Ready` when review requires rework, or `Superseded`.

### Implementation Reviewed

- Applies to: Capability Slices and Engineering Briefs after their implementation has undergone formal review.
- Entry criteria: The implementation review is complete and its outcome permits closure or release progression.
- Required evidence: Implementation review report, decision, verification evidence, known limitations, and remaining risks.
- Responsible authority: Review Authority; Quality Authority MUST accept the sufficiency of required quality evidence.
- Exit criteria: Closure is recorded or a replacement is identified. Inclusion in a governed release is recorded as traceability and does not change the slice or brief state.
- Permitted next states: `Closed` or `Superseded`.

### Closed

- Applies to: Capability Slices, Engineering Briefs, completed Design Authority Reviews, and completed Post Release Reviews. A standard MAY be closed only when it governed a finite, explicitly bounded activity rather than durable guidance.
- Entry criteria: Authorized scope is complete, required review outcomes are accepted, follow-up items are separately tracked, and no further work is expected under the artifact.
- Required evidence: Closure decision, final review outcome, unresolved-risk disposition, and project-memory or release evidence when relevant.
- Responsible authority: Review Authority for reviews, Capability Slices, and Engineering Briefs; Chief Architect MUST concur for architecture-governed scope. Release Authority MUST accept release-specific findings before the release record enters `Post Release Reviewed`, but Review Authority closes the Post Release Review artifact.
- Exit criteria: None in the ordinary flow. Any request to resume work MUST follow Reopening Governance.
- Permitted next states: `Archived`, or `Superseded` or `Deprecated` where those states apply to the artifact type. An exceptional transition back to active work is permitted only under Reopening Governance.

`Closed` is intentionally not supported as a normal state for Capability Specifications, ADRs, durable standards, templates, or releases. Those artifacts remain current until they are `Superseded`, `Deprecated`, or, before completion, `Withdrawn` or `Rejected` as applicable.

### Withdrawn

- Applies to: Draft, proposed, specified, or approved Capability Specifications; Capability Slices; Engineering Briefs; standards; templates; and `Planned` or `Release Candidate` releases. It MAY apply to an uncompleted review artifact only when the review was formally cancelled before any decision was issued.
- Entry criteria: Work will stop before its objective is completed; the authority records why completion is no longer intended and disposes of dependencies and follow-up obligations.
- Required evidence: Withdrawal decision, rationale, current-state summary, dependency impact, known downstream artifacts, and replacement link when one exists.
- Responsible authority: Chief Architect authorizes withdrawal of Capability Specifications, Capability Slices, Engineering Briefs, standards, and templates. Product Owner MUST concur when product intent, capability priority, or release goals are affected. Review Authority authorizes withdrawal of an uncompleted review. Release Authority authorizes withdrawal of a `Planned` or `Release Candidate` release.
- Exit criteria: The artifact remains withdrawn unless a governed reopening is authorized or it is archived.
- Permitted next states: `Draft` only under Reopening Governance and only before implementation or a review decision occurred; `Superseded`; or `Archived`.

`Withdrawn` is intentionally not supported for an implementation review or other review after a decision has been issued, for a `Released` release, or for an artifact already `Closed`, `Superseded`, `Deprecated`, or `Archived`. Corrections to an issued review require a new review record or an appended correction; released versions require a new release.

### Superseded

- Applies to: Capability Specifications, Capability Slices, Engineering Briefs, ADRs, Design Authority Reviews, Post Release Reviews, standards, templates, and releases.
- Entry criteria: A named replacement is approved or released and assumes current authority.
- Required evidence: Replacement artifact, relationship and effective date, approval or review record, and migration guidance when needed.
- Responsible authority: The authority responsible for the artifact type; Release Authority for releases; Chief Architect for architecture and governance artifacts; Product Owner MUST concur when product intent changes.
- Exit criteria: The artifact remains non-current and may be archived or explicitly deprecated.
- Permitted next states: `Deprecated` where deprecation applies to the artifact type, or `Archived` where archival is supported. A superseded ADR has no next state under `docs/contracts/adr-lifecycle.md`.

### Deprecated

- Applies to: Capability Specifications, ADRs, standards, templates, behaviors represented by governed artifacts, and release lines. It MAY apply to a Capability Slice or Engineering Brief only when the artifact itself has ongoing reuse value that must be discouraged.
- Entry criteria: New use is no longer permitted or recommended, impact has been assessed, and replacement guidance or the absence of a replacement is explicit.
- Required evidence: Deprecation decision, reason, effective date, affected consumers, migration or retirement guidance, and known limitations.
- Responsible authority: Chief Architect for architecture and governance artifacts; Release Authority for releases and release lines; Product Owner MUST concur when supported product behavior is retired.
- Exit criteria: The artifact remains deprecated until archived. Reactivation MUST use a new or superseding artifact under Reopening Governance.
- Permitted next states: `Archived` where archival is supported. A deprecated ADR has no next state under `docs/contracts/adr-lifecycle.md`.

### Rejected

- Applies to: Proposed or specified Capability Specifications, Capability Slices, Engineering Briefs, ADRs, standards, templates, and planned releases when evaluated and declined.
- Entry criteria: The responsible authority has considered the artifact and declined it.
- Required evidence: Decision, rationale, review record, and downstream impact.
- Responsible authority: The authority that would have approved the artifact; Review Authority records review-based rejection; Release Authority rejects a release proposal.
- Exit criteria: The rejected record remains unchanged; materially revised work is represented by a new version or new artifact.
- Permitted next states: `Archived` or `Superseded` where supported for the artifact type. A rejected ADR has no next state under `docs/contracts/adr-lifecycle.md`. A return to `Draft` is permitted only under Reopening Governance and only when the revised work retains the same identity and scope.

### Archived

- Applies to: Durable governed artifact types permitted by the applicability table after a substantive disposition. A release MAY enter `Archived` only from `Superseded` or `Deprecated`. An uncompleted active artifact MUST NOT move directly to `Archived`; it must first be `Withdrawn` or `Rejected`.
- Entry criteria: The artifact is no longer active, retention obligations are satisfied, dependencies and references have been updated, and its prior substantive disposition is recorded.
- Required evidence: Archive decision, prior status, archive date, retention location, authority, and links to replacements or follow-up records.
- Responsible authority: The authority responsible for the artifact type; Release Authority for releases; Review Authority for review records; Chief Architect for architecture and governance artifacts.
- Exit criteria: None. Retrieval from archival storage does not change lifecycle state.
- Permitted next states: None. Any renewed work MUST create a new version or new artifact linked to the archived record.

## Artifact-Specific Lifecycle States

Artifact-specific states are valid only for the artifact types named below.

### DAR Approved

- Applies to: Capability Slices only.
- Entry criteria: A Design Authority Review has evaluated the specified slice and issued an outcome that authorizes Engineering Brief preparation and implementation planning.
- Required evidence: DAR identifier, review outcome, accepted constraints, risks, and required follow-up.
- Responsible authority: Review Authority. Chief Architect accepts any architecture constraints; Product Owner accepts any product-scope conditions.
- Exit criteria: The slice and its Engineering Brief satisfy implementation-readiness criteria, or the approval is invalidated by a material change.
- Permitted next states: `Implementation Ready`, `Specified` when re-review is required, `Withdrawn`, or `Superseded`.

`DAR Approved` MUST NOT be used for the DAR artifact itself. The DAR artifact uses `Completed` after its review decision is issued.

### Completed

- Applies to: Design Authority Review and Post Release Review artifacts only.
- Entry criteria: The review activities are finished, a decision or findings have been recorded, evidence and dissent are captured, and required follow-up has an owner.
- Required evidence: Signed or attributable review result, reviewed scope, evidence considered, findings, risks, and follow-up actions.
- Responsible authority: Review Authority. Quality Authority owns conclusions about quality evidence; Release Authority accepts release-specific findings.
- Exit criteria: The review record is accepted as complete and its follow-up actions are tracked independently.
- Permitted next states: `Closed`. If the review record is replaced because it is invalid, it may become `Superseded`; it MUST NOT be silently edited back to `Draft`.

`Completed` is intentionally not a common synonym for `Implemented`, `Implementation Reviewed`, `Closed`, or `Released`.

## Artifact Lifecycle Flows

### Capability Specification

```text
Draft -> Proposed -> Specified -> Approved -> Superseded/Deprecated -> Archived
                     |           |
                     v           v
                 Rejected     Withdrawn
```

Capability Specifications define durable platform capabilities. They are not normally `Implemented` or `Closed` because a capability may produce many slices over time.

### Capability Slice

```text
Draft -> Specified -> DAR Approved -> Implementation Ready
  -> Implemented -> Implementation Reviewed -> Closed -> Archived
```

At pre-implementation stages a slice may become `Withdrawn`, `Rejected`, or `Superseded` as permitted by the relevant state. A closed slice may later become `Superseded` or, where ongoing reuse must be discouraged, `Deprecated`.

`Released` is not a Capability Slice state. A release record may identify the slice as included content.

For compatibility with `docs/standards/capability-slice-standard.md`, that standard's slice-local `Approved` and `Reviewed` labels map to `DAR Approved` and `Implementation Reviewed` respectively. Its reference to a slice as `Released` is release-inclusion metadata evidenced by a release record; it does not replace the slice's `Closed` lifecycle state.

### Engineering Brief

```text
Draft -> Approved -> Implementation Ready -> Implemented
  -> Implementation Reviewed -> Closed -> Archived
```

An Engineering Brief may become `Withdrawn` before implementation begins or `Superseded` when replacement work is approved. Engineering Briefs close only after the implementation they authorize has passed implementation review.

### ADR

```text
Proposed -> Accepted/Rejected -> Superseded/Deprecated
```

ADR status MUST follow `docs/contracts/adr-lifecycle.md`. ADR-local `Accepted` maps semantically to common `Approved`. `Withdrawn` and `Archived` are intentionally not supported as ADR statuses under the current ADR lifecycle. ADRs are not `Closed` or `Completed` under this standard.

### Design Authority Review

```text
Draft -> Completed -> Closed -> Archived
```

Review decisions use their own decision labels, such as `PASS`, `PASS WITH COMMENTS`, `REQUIRES REWORK`, or `FAIL`. A review may be `Withdrawn` only before any decision is issued and only with a recorded cancellation.

### Post Release Review

```text
Draft -> Completed -> Closed -> Archived
```

The review artifact's `Completed` and `Closed` states are distinct from the release record's `Post Release Reviewed` state.

### Standard

```text
Draft -> Proposed -> Approved -> Superseded/Deprecated -> Archived
```

Standards are durable guidance and are not normally `Closed`. A pre-approval standard may be `Withdrawn` or `Rejected`.

### Template

```text
Draft -> Approved -> Released -> Superseded/Deprecated -> Archived
```

For templates, `Released` indicates a versioned template publication governed by an associated release record. Templates SHOULD carry version metadata when used by generation workflows. A pre-release template may be `Withdrawn` or `Rejected`.

## Capability Slice Lifecycle

Capability Slices use this explicit lifecycle:

```text
Draft
  |
  v
Specified
  |
  v
DAR Approved
  |
  v
Implementation Ready
  |
  v
Implemented
  |
  v
Implementation Reviewed
  |
  v
Closed
```

This lifecycle preserves the Forge Method from capability definition through DAR, Engineering Brief, implementation, implementation review, commit, and close. Committing changes is a required workflow action supported by repository evidence; it is not a lifecycle status.

## Release Lifecycle States and Evidence

Release states apply only to a versioned release record, except that a versioned template may state that it has been published through that release. Product Owner defines release goals, Quality Authority determines whether validation evidence satisfies the required quality gate, and Release Authority alone authorizes `Release Candidate`, `Released`, `Post Release Reviewed`, release `Superseded`, and release `Deprecated` transitions.

### Planned

- Applies to: Release records only.
- Entry criteria: Release objective, intended scope, target version or identifier, owner, dependencies, and target timing are recorded.
- Required evidence: Release plan linked to approved product goals and candidate content.
- Responsible authority: Release Authority, with Product Owner approval of release goals.
- Exit criteria: Candidate scope is frozen and readiness evidence is assembled, or the plan is declined or stopped.
- Permitted next states: `Release Candidate`, `Withdrawn`, or `Rejected`.

### Release Candidate

- Applies to: Release records only.
- Entry criteria: Intended content is identified and frozen; included implementation has passed required implementation review; candidate validation has completed; known limitations are recorded; rollback or recovery readiness has been demonstrated or explicitly accepted as not applicable.
- Required evidence: Candidate identifier, included-artifact manifest, implementation-review results, validation record, version-consistency result, known limitations, unresolved-risk disposition, and rollback or recovery readiness record.
- Responsible authority: Release Authority authorizes entry after Quality Authority accepts validation sufficiency and Review Authority confirms required implementation reviews.
- Exit criteria: Release readiness is approved, verification requires candidate rework, or the candidate is withdrawn in favor of a new candidate record.
- Permitted next states: `Released`, `Planned` when scope or evidence must be reworked, or `Withdrawn` before publication.

### Released

- Applies to: Release records and, by reference to a release record, versioned template publications.
- Entry criteria: Release Candidate criteria remain satisfied; the release decision is affirmative; the version is tagged or published; required notes and recovery information are available.
- Required evidence: Release decision, immutable tag or publication identifier, changelog entry, release notes, final validation record, included-artifact manifest, known limitations, and rollback or recovery instructions.
- Responsible authority: Release Authority. Quality Authority MUST confirm the final validation evidence; Product Owner MUST accept any product-facing limitations that alter approved release goals.
- Exit criteria: A Post Release Review is completed and accepted, a later release supersedes it, or the release line is deprecated.
- Permitted next states: `Post Release Reviewed`, `Superseded`, or `Deprecated`.

A published release MUST NOT transition to `Withdrawn`, `Draft`, `Planned`, or `Release Candidate`. Correction requires a new release or superseding release record.

### Post Release Reviewed

- Applies to: Release records only.
- Entry criteria: A separate Post Release Review artifact has reached `Completed`; observed behavior, incidents, user or operator findings, version consistency, limitations, and follow-up actions have been evaluated.
- Required evidence: Post Release Review identifier and result, post-release validation or observation record, findings, incident and limitation summary, follow-up owners, and the Release Authority's acceptance.
- Responsible authority: Release Authority authorizes the release-state transition after Review Authority completes the Post Release Review; Quality Authority owns quality findings.
- Exit criteria: The release remains historically reviewed until it is superseded or deprecated.
- Permitted next states: `Superseded` or `Deprecated`.

### Release Superseded

- Applies to: Release records only, using the common `Superseded` label.
- Entry criteria: A named later release is published and designated as the current replacement.
- Required evidence: Replacement release identifier, supersession decision, effective date, compatibility or migration guidance, and known limitations.
- Responsible authority: Release Authority; Product Owner MUST concur if supported product behavior changes.
- Exit criteria: The release may be deprecated or archived.
- Permitted next states: `Deprecated` or `Archived`.

### Release Deprecated

- Applies to: Release records or release lines, using the common `Deprecated` label.
- Entry criteria: Continued use is no longer supported or recommended; affected consumers and recovery or migration paths have been assessed.
- Required evidence: Deprecation decision, rationale, effective date, affected versions, replacement or no-replacement statement, migration guidance, known limitations, and support or recovery disposition.
- Responsible authority: Release Authority, with Product Owner approval for product-facing retirement and Quality Authority input on safety or quality risk.
- Exit criteria: The release may be archived after retention and reference requirements are satisfied.
- Permitted next states: `Archived` only.

## Reopening Governance

Reopening means resuming work that would otherwise alter the disposition of a `Closed`, `Completed`, `Withdrawn`, `Rejected`, `Deprecated`, or `Archived` artifact. Reopening MUST NOT erase, overwrite, backdate, or silently revise the original decision.

### Acceptable Reasons

A reopening request MUST cite at least one of:

- material new evidence showing that the recorded closure or completion criteria were not actually satisfied
- a defect, safety issue, or governance breach within the original scope
- an external requirement change that must be evaluated against the original decision
- a clerical or factual error that materially affects the recorded decision
- resumption of previously withdrawn work whose identity and scope remain materially unchanged

Convenience, stylistic preference, or unscoped enhancement is not sufficient. New scope MUST use a new Capability Slice, Engineering Brief, ADR, review, standard version, template version, or release as applicable.

### Authorization

- Capability Specifications, Capability Slices, Engineering Briefs, ADRs, standards, and templates require Chief Architect authorization. Product Owner MUST also authorize when product intent, priority, or approved scope is affected.
- Design Authority Reviews and implementation reviews require Review Authority authorization. An issued decision is not reopened in place; a new review record MUST be created and linked.
- Post Release Reviews require Review Authority and Release Authority authorization. A completed review is not reopened in place; a new review or addendum MUST be created and linked.
- Release records require Release Authority authorization. A published release MUST never be reopened in place.
- Quality Authority MUST identify the validation evidence that must be repeated when quality conclusions may be affected.
- The Implementation Agent MAY request reopening and provide evidence but MUST NOT authorize it.

### Required Reopening Record

Before work resumes, the authorizing authority MUST record:

- the artifact identifier and status being challenged
- the original closure, completion, withdrawal, rejection, deprecation, or archive decision and date
- the acceptable reason and new evidence
- the affected scope and downstream artifacts
- the decision to create a new version, new artifact, review addendum, or exceptional same-artifact resumption
- the required revalidation plan and responsible authorities
- links in both directions between the original and replacement or reopening record

### Original Artifact or Replacement

The default and mandatory rule for ADRs, `Completed` reviews, issued review decisions, `Deprecated` artifacts, `Archived` artifacts, and published releases is to preserve the original and create a new version, new artifact, or explicit addendum. Their original status MUST remain unchanged.

A `Closed`, `Withdrawn`, or `Rejected` Capability Slice, Engineering Brief, specification, standard, or template MAY exceptionally resume in the same artifact only when all of the following are true:

- identity and scope remain materially unchanged
- no published release or downstream approval relies on the prior disposition, or every such dependency is included in revalidation
- the reopening authorities approve the same-artifact approach
- a status-history entry preserves the original decision, date, rationale, and evidence
- the artifact version is incremented when its contract or approved content changes

The permitted same-artifact target is `Draft`, `Specified`, or `Implementation Ready`, whichever is the earliest state whose entry criteria remain valid. No intermediate approval or review state may be skipped.

### History and Auditability

The original decision text MUST remain accessible. Reopening changes MUST be additive through a status-history section, linked decision or review record, version-control history, and project-memory update where the disposition affects current or durable direction. The current status MUST link to the prior disposition and reopening authorization.

### Downstream Revalidation

The reopening record MUST inventory downstream artifacts and assign revalidation as follows:

- Product Owner revalidates affected product intent, capability priority, acceptance criteria, and release goals.
- Chief Architect revalidates affected Capability Specifications, Capability Slices, ADRs, standards, architecture constraints, and Engineering Briefs.
- Review Authority repeats any DAR or implementation review whose assumptions, scope, evidence, or outcome changed.
- Quality Authority repeats or explicitly waives, with rationale, affected tests, validation, quality gates, and risk conclusions.
- Release Authority revalidates affected release plans, candidate evidence, release decisions, notes, limitations, and recovery readiness.

An artifact MUST NOT return to `Closed`, `Completed`, `Release Candidate`, `Released`, or `Post Release Reviewed` until all assigned downstream revalidation is complete and evidenced.

## Status Ownership

Authority remains separated by role:

- Product Owner owns product intent, roadmap, capability priority, acceptance of product-facing limitations, and release goals.
- Chief Architect owns architecture state, Capability Specifications, Capability Slices, standards, ADR alignment, and Engineering Brief authorization.
- Implementation Agent owns implementation progress evidence and implementation-complete attestations, but not review, closure, or release approval.
- Review Authority owns DAR outcomes, implementation review outcomes, review completion, and review closure.
- Quality Authority owns testing and validation sufficiency, quality gates, and quality-risk conclusions.
- Release Authority owns release planning, candidate authorization, release decisions, post-release state, supersession, deprecation, and release archival.

AI agents MAY update lifecycle status only when explicitly instructed or when the accepted workflow requires it, all required evidence is present, and the responsible authority's decision is recorded.

## Transition Record Requirements

Every lifecycle transition MUST record, in the artifact or a linked durable decision record:

- previous state and new state
- effective date
- authorizing authority
- entry criteria satisfied
- evidence references
- rationale and known limitations
- affected downstream artifacts and required follow-up

Relevant evidence includes ADRs, DARs, implementation reviews, test and validation records, changed-file inventories, release decisions, tags, changelog entries, recovery-readiness records, Post Release Reviews, and project-memory updates. Evidence MUST be concrete enough for an independent reviewer to reproduce why the transition was allowed.

## Anti-Patterns

The following are prohibited:

- marking `Implemented` work as `Closed` without implementation review
- using `Released` for every artifact
- hiding unfinished work in `Closed` artifacts
- changing lifecycle state without the required authority and evidence
- using ambiguous labels such as "done-ish", "final", "ready", or "complete" without a governed definition
- treating `Reviewed` or review `Completed` as equivalent to `Closed`
- treating `Withdrawn`, `Archived`, `Deprecated`, or `Superseded` as equivalent to `Closed`
- archiving active work without first recording its substantive disposition
- reopening or rewriting an issued decision without a reopening record and downstream revalidation
- allowing an Implementation Agent to approve its own review, closure, or release

## Documentation Requirements

Lifecycle status SHOULD appear near the top of the artifact, usually after the title.

Recommended format:

```text
## Status

Closed.
```

or:

```text
Status: Accepted
```

Status changes MUST be reflected in:

- the artifact itself
- `PROJECT_STATE.md` when current work changes
- `PROJECT_BRAIN.md` when durable guidance changes
- `AI_HANDOFF.md` when future agents need the status to orient correctly
- `CHANGELOG.md` when the status change is release-facing

## Relationship To Existing Standards

### CONSTITUTION.md

The Constitution defines Forge's highest principles. Lifecycle discipline supports intentional software, review before release, and durable project memory.

### AI_ENGINEERING_CONDUCT.md

AI Engineering Conduct requires agents to read, understand, test, review, document, and escalate uncertainty. Lifecycle status gives agents a clear way to know what state an artifact is actually in.

### AI Implementation Protocol

`docs/standards/ai-implementation-protocol.md` defines how Engineering Briefs are implemented. This standard defines how lifecycle state is represented before, during, and after implementation.

### Capability Slice Standard

`docs/standards/capability-slice-standard.md` defines Capability Slice content and lifecycle. This standard clarifies the shared lifecycle model and makes the Capability Slice lifecycle consistent with other artifact types.

### ADR Lifecycle

`docs/contracts/adr-lifecycle.md` governs ADR-local status labels. This standard preserves that lifecycle and maps ADR `Accepted` to the shared meaning of `Approved` without renaming existing ADRs.

### Release Standard

`docs/release/release-standard.md` governs releases. This standard defines auditable release-state transitions and preserves `Released` primarily for project versions and release records.
