# Forge 1.0 — delivery proposal from Audio Recorder lessons

Date: 2026-10-11. Status: proposal and researched delivery plan, not implementation/release acceptance.
Authority: owner requested using Audio Recorder lessons and current agents/LLMs to finish Forge 1.0.
This adds a concrete proposed direction to the existing repository; it does not bootstrap a project,
commit, change a version, retire a finding, or silently replace accepted FAL contracts.

## Verified starting point

Forge main at e8d8ed05d23e5229109139836101d036fb27a7e1, with the prior authorized uncommitted
CORR-003 repair and ADR0018 documentation changes retained. Current release documentation names
0.4.1, package metadata targets 0.5.0, and ROADMAP defines 1.0 as a stable platform contract.
The last independently recorded suite has 183 passes; it was not rerun for this planning-only work.
IR-FAL-004 still reports FAIL for FAL-002 despite those tests. Audio Recorder has a separate
616-test implementation baseline and outstanding native interactive acceptance. Neither result
is renamed into complete system acceptance.

## Product outcome

A person or coding agent can enter an existing repository, establish its true state, receive a
bounded task with durable authority, implement it using a supported agent tool, run the project's
actual checks, obtain an independent review, and resume after interruption without losing work or
inventing success. Ordinary work should require one working record and no repeated permission for
actions already authorized. Release remains an explicit decision on concrete verified artifacts.

The stable boundary should cover bootstrap compatibility, project memory, task/authority and
verification contracts, command behavior, errors, and migrations. It should not depend on one
model name, provider, document count, or an unverified autonomous-loop claim.

## Lessons applied

| Observed problem | Required improvement | Observable acceptance |
| --- | --- | --- |
| User-supplied path and FAL baseline belonged to different repositories | Establish repository root, HEAD, index and scope before work | Wrong-repository fixture rejects without writes |
| Many green tests missed authority/publication defects | Reproductions become negative integration cases independent of implementation claims | Missing authority, sealed publication and forged evidence cannot yield acceptance |
| Duplicate current-state histories drift | One status owner, one work record, links from handoff | A status change needs no manually synchronized narrative copies |
| A C# project is reported as missing Python packaging | Language-neutral core checks plus explicit project verification configuration | Python and .NET fixtures both report applicable checks accurately |
| UI access denial was discovered late | Preflight required tools, permissions and environment | Missing desktop/system capability is visible before claiming a complete verification plan |
| Adapter exceptions and recovery failed | Durable interruption and bounded failure outcomes | Restart tests preserve work, findings, authority and correction history |
| Reviewer freshness/offline authority was asserted rather than enforced | Observe execution identity and validate actual grants before invocation | No callback can manufacture independence or approval |

## Proposed technical direction

Keep the deterministic Forge core small: inspect state, assemble scoped context, validate authority,
record evidence, and evaluate explicit readiness criteria. Reuse a maintained coding-agent runtime
for execution rather than writing another complete LLM runner. Preserve provider-neutral contracts;
a first concrete Codex integration is a candidate, not a mandate for every user or a new dependency
added by this plan. A later provider must pass the same behavioral conformance suite.

Implementation and independent review use distinct fresh sessions with observed boundaries. A
second model can supplement review but does not itself establish independence. Parallel agents
are used only for separable work with clear write ownership and explicit resource limits.

Record provider/model identifier, runtime version, applicable configuration, input baseline,
permissions, commands and evidence for each actual run. Treat model changes as evaluated upgrades,
not automatic latest-version selection. Prefer account-configured defaults until measured task
quality, cost and latency justify another choice. No unverified claim of account/API availability.

## Current external evidence, checked 2026-10-11

- Codex SDK documentation provides local thread start/continue/resume and a stable Python SDK
  controlling the app server. This is relevant to Forge's existing Python implementation.
  https://learn.chatgpt.com/docs/codex-sdk
- OpenAI distinguishes managed Agents API, application-controlled Agents SDK and direct Responses
  integration. Runtime state ownership must be chosen deliberately; their session types differ.
  https://developers.openai.com/api/docs/guides/agents
- The current model catalog identifies GPT-6 Astra, GPT-6.1 Sol and GPT-6 Luna for different
  capability/cost trade-offs. These are candidates to evaluate, not pinned Forge requirements or
  evidence that a particular account has access.
  https://developers.openai.com/api/docs/models

No paid model execution, SDK installation or provider comparison was performed in this assessment.
Other providers remain possible but have not been researched or certified here.

## Delivery sequence and gates

1. **Define the stable 1.0 boundary.** Reconcile README, roadmap and current status; inventory public
   contracts and select supported environments. Produce one reviewed architecture decision that
   compares repairing the current FAL runtime against an SDK-backed implementation of the same
   required invariants. Preserve FAL-001 termination and all open FAL-002 evidence. A replacement
   must not hide failures by renaming or dropping required behavior. If FAL-002 is excluded from
   stable distribution, that must be an explicit reviewed disposition and visible packaging boundary.
2. **Make the ordinary workflow small and truthful.** Apply ADR0018 to runtime guidance and versioned
   templates, preserving compatibility/migration. Add project-specific verification configuration,
   environment preflight and concise actionable status. Distinguish PASS, FAIL, not run and blocked.
3. **Enforce the execution/review contract.** Validate permission and offline/network authority before
   any agent invocation; use genuinely fresh review context; preserve immutable observations;
   redact failure evidence; safely interrupt/resume; deny sealed predecessor writes. Add no optional
   agent platform feature until these end-to-end cases pass.
4. **Qualify real agent integrations.** Use the first supported runtime against isolated repositories
   and explicit budgets. Test malformed output, timeout, cancellation, stale baseline, partial writes,
   pending permissions, altered reviewer provenance and restart. Capture real results separately from
   mocks; SDK availability is not conformance evidence.
5. **Dogfood and package.** Run a bounded maintenance task against Audio Recorder and a separate small
   repository, checking useful deliverables and administrative effort. Verify installation, CLI,
   migration, documentation and the selected OS/runtime matrix. Independently review the actual
   release candidate; reconcile versions only when the release scope is accepted.

Each step uses one linked work record containing scope, implementation, tests, findings and status.
Additional documents are reserved for durable decisions or separately required contracts.

## Definition of done for 1.0

- Stable public repository/memory/template/CLI contracts with migration guidance and compatibility tests.
- No material open defect in the included release scope; excluded experiments clearly identified.
- Required checks execute against fresh candidate artifacts; missing system verification blocks claims.
- Real agent execution and independent review satisfy the declared authority/freshness contract.
- Interruption/restart, malformed inputs and unauthorized actions are adversarially verified.
- Existing project files and uncommitted work survive all supported workflows.
- Model/provider upgrades pass the same evaluation set before becoming defaults.
- One canonical current-status owner and measured reduction in duplicated records/repeated approvals.
- Clean installation/upgrade evidence, coherent version metadata, release notes and independent review.
- An explicit release decision; no tag, publication or commit inferred from this planning document.

## Current disposition

Feasible direction; Forge 1.0 is not implemented or release-ready by this assessment. The immediate
next deliverable is the reviewed stable-boundary/architecture decision and its first bounded
implementation slice. Existing FAL limits (3,400 LOC, four modules, two adapters, five surfaces,
zero added dependencies) stay effective for that runtime until explicitly superseded through the
applicable governance. They must not be silently applied to, or discarded by, a new SDK architecture.
