# Project Brain

This file captures durable project knowledge that future human and AI contributors should preserve.

## Core Identity

Forge is an AI-Native Software Engineering Platform.

Forge provides a disciplined engineering environment where humans and AI collaborate to design, build, review, govern, and evolve software.

Forge is not an application. It is a constitutional foundation for creating and governing future applications and software projects.

## Guiding Beliefs

- Good AI engineering starts with context quality.
- Project memory must live in the repository, not only in chat history.
- Architecture decisions should be explicit, dated, and reviewable.
- Automation should follow documented contracts.
- Human control should remain visible at key decision points.
- A platform should make good defaults easy without making exceptions impossible.
- Documentation needs clear authority so repeated summaries do not drift.
- Architecture review gates protect Forge from premature automation.
- Project memory files are contracts, not casual notes.
- CLI behavior must be specified before it is implemented.
- Bootstrap generation must be template-driven, not hardcoded in CLI code.
- Templates are versioned architecture assets.
- Permanent Forge capabilities are specified through FCS documents before implementation.
- Reviews must produce scores and narrative findings, not scores alone.
- The first implementation must stay narrow and prove the template-driven bootstrap path.
- Dogfooding is a release gate: generated projects must be judged for real usefulness, not only successful file creation.
- Forge must have a reliable developer platform before new capabilities are added.
- Forge's permanent motto is: Build software with intention.
- Every future engineering decision should ultimately derive from `CONSTITUTION.md`.
- AI agents must follow `AI_ENGINEERING_CONDUCT.md` when working in Forge-governed projects.
- Governance Runtime is the future operational layer that interprets Forge governance and evaluates engineering health.
- Capability Slices keep large capabilities traceable and implementation-sized without weakening capability-first governance.
- Capability Slices are first-class Forge artifacts governed by `docs/standards/capability-slice-standard.md`.
- Governance Runtime should begin with a read-only Status Service before any scoring, enforcement, release approval, or memory mutation.
- Capability Slice Design Authority Reviews should verify slice readiness before Engineering Briefs are created for major runtime capabilities.
- Engineering Brief implementation must follow a standard protocol so AI implementation behavior remains repeatable, reviewable, and scope-controlled.
- Lifecycle language must be governed consistently so artifact state remains explicit, traceable, and reviewable.

## Product Shape

Forge may eventually include:

- project bootstrap
- AI development workflow
- project memory
- engineering standards
- templates
- documentation governance
- architecture governance
- testing standards
- Git workflow
- release management

## Important Boundaries

- Forge should not become a hosted SaaS by default.
- Forge should not require a specific AI vendor.
- Forge should not hide architectural decisions in generated output.
- Forge should not generate production code before project intent is captured.
- Adaptive automation must not claim append-only state, independent review or criterion coverage
  without executable integrity and provenance boundaries.

## Current Decisions

- Preserve `IR-FAL-001`, the two exhausted automatic correction rounds and the resolved
  `DC-FAL-001`/`HD-FAL-001` authorization as immutable correction-series history.
- Preserve `IR-FAL-002` as the result of the consumed `HD-FAL-001` human-bounded correction. The
  local append-only ledger finding closed, but closure authority, nested schema semantics and
  criterion/reviewer proof remained blocking and led to resolved `DC-FAL-002`/`HD-FAL-002`.
- Treat FAL-001 as permanently `TERMINATED BLOCKED` under `HD-FAL-002`; never reuse a run identity or
  correction to imply acceptance or closure.
- Treat FAL-002 as a new Standard-Assurance design: small bounded engineering core, canonical
  boundary model, criterion-bound evidence with reviewer semantic rationale, honest fresh read-only
  review, and High Assurance deferred to a separate future profile.
- Treat the FAL-002 specification as approved for Implementation Planning under `HD-FAL-006`; all
  four specification findings are closed. `EB-006` is the bounded implementation plan and must pass
  human review before a separate decision may authorize implementation.
- Treat `EB006-R1`–`EB006-R3` as addressed under `HD-FAL-007` but not closed. The revised brief freezes
  storage, collector/parser, adapter, schema/fixture, recovery and criterion-evidence contracts and
  must receive a new independent review before Implementation Authorization can be considered.
- Treat the latest independent EB-006 verdict as `NOT READY FOR IMPLEMENTATION AUTHORIZATION`.
  `HD-FAL-008` authorizes documentation-only correction of `EB006-FR-01`–`EB006-FR-07`; it does not
  close or verify those findings or `EB006-R1`–`EB006-R3`. Stop if the correction requires changed
  specification, scope, criteria, authority, budget, dependencies or implementation experiments.
- Treat `HD-FAL-009` as the sole budget reconciliation for the unchanged FAL-002 scope: approximately
  1,660 expected and at most 1,800 new production LOC. The ceiling is a maximum envelope, not a
  target; every non-LOC limit, assurance requirement and finding remains unchanged. The bounded
  `HD-FAL-008` correction is documentation-complete, but FAL-002 implementation remains unauthorized.
- Treat the resumed `HD-FAL-008` correction as documentation-complete but unverified. EB-006 sections
  21–27 are the implementation-complete refinements for boundary models, state transitions,
  fixtures, adapters, reviewer separation, collectors, recovery, budget and control coverage. All
  ten findings await fresh independent review; no implementation authority follows.
- Treat the latest independent review as superseding that completeness claim: it returned `NOT READY
  FOR IMPLEMENTATION AUTHORIZATION` with `EB006-IR2-01`–`EB006-IR2-07`. `HD-FAL-010` authorizes only
  their bounded documentation correction. It cannot change the FAL-002 specification, 1,800-LOC
  ceiling, dependencies or implementation state and must stop on higher-order authority needs.
- Treat EB-006 sections 28–33 as the completed `HD-FAL-010` refinements: exact nested variants,
  command parsed unions, decision vocabulary, Forge-owned grants, unified staged publication,
  independent fixture oracle, collector representations and corrected control mapping. They await
  independent review and confer no implementation authority.
- Treat the independent IR3 verdict as `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED` with
  all eight findings `EB006-IR3-01`–`EB006-IR3-08` open. `HD-FAL-011` authorizes no CORR-011 work;
  it requires a separate recovery/state architecture decision because an occupied canonical gate
  path cannot record authoritative fail-closed state under the current single-series contract and
  total conflict-card recovery depends on that choice. Keep the 1,660 expected / 1,800 maximum LOC
  envelope unchanged and FAL-002 `NOT AUTHORIZED`.
- Treat `HD-FAL-012` as the binding recovery/state architecture: deterministic successor physical
  series segments form one logical append-only lineage; a `RECOVERY_ROOT` GateRecord is the sole
  authority transition; HumanDecision conflict cards explain/resolve but never establish state;
  discovery is derived and pointer-free. The five surfaces and budget remain unchanged. IR3-04 and
  IR3-05 remain open; HD-FAL-013 subsequently supplies the separate CORR-011 authorization.
- Treat `HD-FAL-013` as authorization for one coherent bounded documentation campaign containing
  `CORR-011-01`–`CORR-011-08`. It may change EB-006 and only necessary project-memory/index text,
  must implement `HD-FAL-012` without redesign, and must stop on specification, architecture,
  surface, dependency or budget authority needs. Findings may become only `ADDRESSED — AWAITING
  INDEPENDENT REVIEW`; FAL-002 remains `NOT AUTHORIZED`.
- Treat EB-006 sections 34–42 as the completed CORR-011 correction-agent contract claim. They were
  submitted for independent review with all eight IR3 findings still unverified. Independent IR4
  now supersedes any implication that these sections are implementation-ready; no implementation
  authority follows.
- Treat Independent IR4's canonical outcome as `FAIL — IMPLEMENTATION AUTHORIZATION NOT
  RECOMMENDED`; its abbreviated final `FAIL` is a non-material formatting deviation. Preserve all
  five findings `EB006-IR4-01`–`EB006-IR4-05` as open.
- Treat `HD-FAL-014` as the binding narrow clarification of `HD-FAL-012`: semantic recovery identity
  retains intended/obstruction evidence, while pointer-free physical discovery derives only from an
  authoritative predecessor and publication slot. Non-reconstructable intended bytes require a
  GateRecord publication-intent commitment before final publication. Exact ordinal candidate lookup
  is authoritative only through a valid RECOVERY_ROOT; directory presence is never authority.
- Preserve one stable semantic `decision_identity` across physical recovery. A successor may rebind
  its HumanDecisionRecord locator/hash with an incremented binding generation, but may not mint a
  new governance question merely to escape a collision. Complete-lineage lookup uses only validated
  GateRecord bindings. IR4-03 remains open with architecture authority provided; IR4-04 remains open
  with its architecture dependency removed. HD-FAL-014 itself authorized neither CORR-012 nor
  FAL-002 implementation; HD-FAL-015 subsequently authorizes only the bounded correction.
- Treat `HD-FAL-015` as authorization for exactly one coherent bounded EB-006 documentation campaign
  mapping `CORR-012-01`–`CORR-012-05` one-to-one to `EB006-IR4-01`–`EB006-IR4-05`. The campaign must
  reconcile one universal hash contract, a total independent oracle, HD-FAL-014 publication-intent/
  discovery/decision continuity, complete-lineage decision lookup and deterministic finding
  evolution as one model. It may change only EB-006 and necessary index/project-memory text.
- Treat EB-006 sections 43–50 as the completed integrated CORR-012 correction claim. The final model
  uses domain-separated canonical hashing, predecessor/slot-derived recovery discovery, acyclic
  decision bindings, explicit immutable finding events plus derived current state, an executable
  stdlib-only fixture oracle, and five-surface systemic audits. All five IR4 findings were submitted
  as `ADDRESSED — AWAITING INDEPENDENT REVIEW` for IR5; the later IR5 disposition governs their
  verification state. FAL-002 implementation remains `NOT AUTHORIZED`.
- Treat Independent IR5's canonical outcome as `FAIL — IMPLEMENTATION AUTHORIZATION NOT
  RECOMMENDED`. Preserve its verification of the narrow CORR-012-01/IR4-01 canonical-hash correction
  and CORR-012-03/IR4-03 publication-intent/recovery-discovery correction without treating either as
  finding closure. Preserve `EB006-IR5-01`–`EB006-IR5-04` as open blocking residuals.
- Treat `HD-FAL-016` as authorization for exactly one coherent bounded EB-006 documentation campaign
  mapping `CORR-013-01`–`CORR-013-04` one-to-one to `EB006-IR5-01`–`EB006-IR5-04`. It must replace or
  consolidate the affected final sections into total fixture, decision-resolution, persisted finding
  event and severity-fold contracts, not add another avoidable precedence layer. HD-FAL-012/014,
  five surfaces, verified hash/recovery contracts and the 1,800-LOC ceiling remain unchanged.
  At that gate FAL-002 implementation remained `NOT AUTHORIZED` and only IR6 could verify the correction.
- Treat EB-006 §§44–50 as the completed CORR-013 remediation claim. The final consolidated model
  separates pending cards from accepted resolutions and GateRecord application, persists finding
  deltas/checkpoints in GateRecord, folds severity/blocking with human epochs, and provides a
  stdlib-only executable fixture/VFS oracle. These changes preserve the independently verified
  CORR-012-01 hash and CORR-012-03 recovery/discovery contracts. All four CORR-013 objectives were
  submitted as `ADDRESSED — AWAITING INDEPENDENT REVIEW`; the later IR6 disposition governs them.
- Treat Independent IR6's canonical outcome as `FAIL — IMPLEMENTATION AUTHORIZATION NOT
  RECOMMENDED`. Preserve its VERIFIED dispositions for CORR-013-03/IR5-03 and CORR-013-04/IR5-04,
  PARTIALLY VERIFIED disposition for CORR-013-02/IR5-02 and NOT VERIFIED disposition for
  CORR-013-01/IR5-01 without treating any as finding closure. Preserve `EB006-IR6-01` and
  `EB006-IR6-02` as open blocking residuals.
- Treat `HD-FAL-017` as authorization for exactly one coherent bounded EB-006 documentation campaign
  mapping `CORR-014-01` to `EB006-IR6-01` and `CORR-014-02` to `EB006-IR6-02`. It may correct only
  stable semantic-answer versus physical-binding semantics and the total lineage-aware independent
  oracle. It must directly consolidate §§46 and 48, preserve every IR6-verified contract, keep five
  surfaces and the 1,800-LOC ceiling, and leave FAL-002 implementation `NOT AUTHORIZED`.
- Treat EB-006 §§44–50 as the completed CORR-014 remediation claim. Stable ResolutionSemanticInput
  binds DecisionRequirement rather than a relocatable pending-card hash; PresentationEvidence is
  separate; DecisionApplication and offline authority independently validate semantic answer and
  current physical lineage. The stdlib-only OracleLineageState, CONTROL, RECOVERY_ROOT,
  review-event and mutation/VFS scenarios execute without production imports. Both objectives were
  submitted as `ADDRESSED — AWAITING INDEPENDENT REVIEW`; the later IR7 disposition governs them.
- Treat Independent IR7's canonical outcome as `FAIL — IMPLEMENTATION AUTHORIZATION NOT
  RECOMMENDED`. Preserve `CORR-014-01`/`EB006-IR6-01` as independently `VERIFIED` but not closed.
  Preserve `CORR-014-02`/`EB006-IR6-02` as `NOT VERIFIED`, open and blocking; IR7 created no new
  finding. The residual is limited to active-series propagation, recovery-N/successor run-review
  construction, complete REHASH dependency closure and total executable matrix rows.
- Treat `HD-FAL-018` as authorization for exactly one final bounded EB-006 documentation campaign:
  `CORR-015-01` → `EB006-IR6-02`. The correction must make §48's oracle follow the frozen production
  model, preserve §46 decision semantics and all verified recovery/finding/hash contracts, keep five
  surfaces and the 1,800-LOC ceiling, and leave FAL-002 implementation `NOT AUTHORIZED`.
- Treat `CORR-015-01` as documentation-complete and only `ADDRESSED — AWAITING INDEPENDENT REVIEW`.
  Final §48 now takes current lineage for all successor construction, executes recovery-N and
  successor Run/Review/FindingEvent chains, recomputes DecisionRequirement dependencies
  inner-to-outer, preserves stale hashes under NO_REHASH, and exercises create-only VFS behavior.
  `EB006-IR6-02` remains open and blocking until a fresh independent read-only review; no finding is
  closed and `EB006-IR6-01` remains independently verified.
- Treat IR8's canonical outcome as `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
  `CORR-015-01` is `PARTIALLY VERIFIED`; `EB006-IR6-02` is `NOT VERIFIED`, open and blocking; no
  new finding was created. Preserve IR8's verified recovery depth-three, successor Run/Review,
  review-event binding, DecisionRequirement REHASH/NO_REHASH, semantic relocation and five-surface
  results.
- Treat `HD-FAL-019` as authorization for exactly one bounded `CORR-016-01` → `EB006-IR6-02`
  documentation correction. It may correct only final §48's executable REHASH policy/closure,
  affected matrix rows and eligibility-oracle fidelity to frozen §47. It may not change production
  semantics, specification, architecture, runtime, five surfaces, dependencies or budget, and it
  leaves FAL-002 `NOT AUTHORIZED`.
- Treat CORR-016 as documentation-complete and only `ADDRESSED — AWAITING INDEPENDENT REVIEW`.
  Final §48 now executes an exhaustive REHASH policy with supported/context/prohibited dispatch,
  dependency-cycle/context validation, coherent binding and publication identities, a 24-row
  affected-matrix gate, and eligibility derived from carried finding history/checkpoint. Empty
  review never verifies an addressed blocker; CRITICAL blocks; exact independent absence clears
  only that finding blocker. Recovery depth three, successor execution and semantic answer
  relocation remain regression-green. `EB006-IR6-02` remains open pending independent review.
- Treat IR9's canonical outcome as `FAIL — IMPLEMENTATION AUTHORIZATION NOT RECOMMENDED`.
  `CORR-016-01` is `PARTIALLY VERIFIED`; `EB006-IR6-02` is `NOT VERIFIED`, open and blocking; IR9
  created no new finding. Preserve its verified matrix, eligibility, recovery depth-three,
  successor Run/Review, semantic-answer, finding/governance and five-surface results. The sole
  residual is standalone PublicationSlot REHASH accepting key-complete wrong context and returning
  stale target path/slot identity, plus a self-check that misses the absent executable handler.
- Treat `HD-FAL-020` as authorization for exactly one bounded `CORR-017-01` → `EB006-IR6-02`
  documentation correction. Normative caller audit selected Option B: direct standalone
  PublicationSlot REHASH is unnecessary and must be prohibited, while the verified GateRecord
  publication-intent path remains supported. Dispatch/dependency self-checks must detect missing
  handlers and unauthorized fallback. FAL-002 remains `NOT AUTHORIZED`; no architecture, production
  semantic, surface, dependency or budget change is authorized.

- Use documentation-first development for `0.1`.
- Use Python as the expected implementation language.
- Defer CLI implementation.
- Evaluate Typer before implementation, but do not introduce it yet.
- Keep empty implementation and test directories to establish future structure.
- Use `docs/README.md` as the documentation authority map.
- Require explicit architecture review gates before major implementation milestones.
- Accept Forge 0.1 RC1 as the architecture foundation.
- Define project memory schemas under `docs/contracts/`.
- Use ADR lifecycle and status rules from `docs/contracts/adr-lifecycle.md`.
- Govern standards through categories and acceptance criteria before automation.
- Govern templates through ownership, versioning, and change rules before generation.
- Specify `forge init <project-name>` before implementation.
- Use `templates/bootstrap/` as the source for generated project files.
- Require every template to define metadata, variables, required variables, and optional variables.
- Reject unknown or missing template variables before writing files.
- Verify first CLI behavior against the `forge init` specification before expanding scope.
- Use `docs/capabilities/` for Forge Capability Specifications.
- Accept FCS-001 as the Review Capability specification.
- Implement Forge `0.2.0` as a Typer-based Python CLI.
- Implement only `forge init <project-name>` for the first MVP.
- Keep generated file content in `templates/bootstrap/`, not in Python code.
- Use tests to protect dry-run, validation, overwrite protection, and template rendering.
- Release Forge `0.2.0` as local editable only.
- Use tag format `vX.Y.Z`, starting with `v0.2.0`.
- Do not publish Forge `0.2.0` to a package index.
- Use DAR-0001 as the baseline for Forge `0.3` planning.
- Treat roadmap drift, CI, testing standard, review persistence, and template provenance as known governance work.
- Accept Gate 1 dogfooding for `ForgePlayground` as `PASS WITH COMMENTS`.
- Treat the generated project source-layout question as resolved by ADR 0017: the universal bootstrap will generate no source-code directory after contract and implementation gates pass.
- Treat release tag, package version, and generated `FORGE_VERSION` alignment as required traceability work before future release confidence increases.
- Fix generated Forge version traceability for `v0.2.1` before starting Forge `0.3`.
- Strengthen first-session architecture discovery guidance in bootstrap templates without expanding `forge init` scope.
- Preserve the historical `0.2.x` output until the ADR 0017 contract revision and bounded implementation pass their required gates.
- Establish Forge `0.3` as the Developer Platform milestone.
- Use `pytest` as the required test runner.
- Use Ruff for lightweight lint and format checks.
- Run tests, lint, and format checks in GitHub Actions on push and pull request.
- Do not implement `forge review` until after the Developer Platform baseline is accepted.
- Use `CONSTITUTION.md` as Forge's highest governing document.
- Officially position Forge as an AI-Native Software Engineering Platform.
- Use ADR 0011 as the decision record for constitutional governance and product identity.
- Treat "framework" language as historical or supporting language unless it conflicts with the official platform identity.
- Use `AI_ENGINEERING_CONDUCT.md` as the root AI behavior contract.
- Use ADR 0012 as the decision record for AI Engineering Conduct.
- Require AI agents to escalate uncertainty instead of inventing certainty.
- Accept FCS-002 as the Governance Runtime capability specification.
- Use ADR 0013 as the decision record for Governance Runtime as a permanent capability.
- Do not implement Governance Runtime until first service, inputs, outputs, persistence, scoring policy, and failure behavior are specified.
- Introduce Capability Slice between Capability Specification and Engineering Brief.
- Use ADR 0014 as the decision record for Capability Slices.
- Use AR-0001 as the architecture review baseline for the engineering hierarchy.
- Do not create Engineering Briefs for large multi-service capabilities until the relevant Capability Slice is accepted.
- Use `templates/capability-slices/CS-template.md` as the starting point for new Capability Slices.
- Name Capability Slices with `CS-NNN.S-descriptive-name.md`.
- Accept CS-002.1 as the first Governance Runtime Capability Slice.
- Scope CS-002.1 to read-only status evaluation for Forge governance and engineering artifacts.
- Use CS-002.1 as the boundary for the future `forge status` Engineering Brief.
- Do not add automatic writes, review generation, release approval, or complex code-quality scoring to the first Status Service implementation.
- Accept DAR-CS-0001 as `PASS WITH COMMENTS` for CS-002.1.
- Require EB-002.1 to resolve output shape, strict mode behavior or deferral, repository validity detection, module boundaries, and read-only verification tests.
- Accept EB-002.1 as the implementation brief for the read-only Governance Runtime Status Service.
- Implement `forge status` through a service boundary, with CLI wiring separate from repository inspection.
- Defer strict mode, JSON output, persisted reports, Governance Score, and policy packs beyond EB-002.1.
- Treat runtime project memory writes as explicitly forbidden for the first Status Service.
- Implement the first Status Service in `forge/status.py` with CLI wiring in `forge/cli.py`.
- Keep `forge status` human-readable and informational; it must not imply release approval or governance certification.
- Represent first status results with simple categories and the states `OK`, `WARNING`, `MISSING`, `BLOCKED`, and `NOT_APPLICABLE`.
- Version consistency is a Governance Runtime concern because release identity spans Git tags, package metadata, documentation, project memory, changelog, and handoff context.
- CI cannot be assumed to catch governance drift unless explicit checks exist.
- `forge status` should evolve through slices from artifact presence toward semantic governance consistency checks.
- Version consistency should extend `forge status` as a read-only status category or item group, not as a separate command.
- Accept CS-002.2 as the specified Capability Slice for Governance Runtime Version Consistency Check.
- Treat historical version references as valid context unless they conflict with active release-facing version identity.
- Do not implement version consistency checks until CS-002.2 passes DAR-CS and an Engineering Brief is accepted.
- Accept DAR-CS-0002 as `PASS WITH COMMENTS` for CS-002.2.
- Require EB-002.2 to define exact version parsing, active versus historical reference handling, latest tag selection, package metadata policy, output placement, fixtures, and read-only tests.
- Keep version consistency informational; it must not become release approval or automatic remediation.
- Accept EB-002.2 as the implementation brief for adding Version Consistency Status to `forge status`.
- Implement version consistency with conservative parsing, local Git-only inspection, and explicit historical-reference exclusions.
- Keep `pyproject.toml` version mismatches as warnings until Forge has a package publishing policy.
- Implement Version Consistency Status as one additional read-only `forge status` category, not a new command.
- Use the latest local `vMAJOR.MINOR.PATCH` Git tag as the comparison target when available.
- Compare only active release-facing document sections, not every historical version reference in a file.
- Treat missing `pyproject.toml` as `NOT_APPLICABLE` because Forge-generated projects may not be Python packages.
- Report version mismatches as `WARNING`; do not automatically fix files, approve releases, create tags, or persist reports.
- Use `docs/standards/ai-implementation-protocol.md` as the default implementation process for future Engineering Briefs.
- Use ADR 0015 as the decision record for the AI Implementation Protocol.
- Require implementation agents to read governing documents, implement only approved scope, run required verification, update required documentation, report risks, and prepare review handoff.
- Let Engineering Briefs define stricter verification or process requirements, but not silently bypass the protocol.
- Accept DAR-EB-0002 as the implementation review for EB-002.2.
- Treat CS-002.2 as closed after passing implementation review.
- Keep future Version Consistency enhancements in separate Capability Slices rather than expanding the current implementation opportunistically.
- Use `docs/standards/lifecycle-standard.md` as the shared lifecycle model for Forge artifacts.
- Use ADR 0016 as the decision record for the Forge Lifecycle Standard.
- Treat `Closed`, `Withdrawn`, `Archived`, `Released`, `Deprecated`, `Superseded`, and `Implementation Reviewed` as distinct states with distinct authority and evidence requirements.
- Use ADR 0017 as the durable generated project source-layout decision.
- Keep the universal bootstrap language-neutral and generate no source-code directory after the affected contracts and bounded implementation are accepted.
- Keep Forge's own `forge/` Python package separate from generated project source layout.
- Require generated projects to choose source layout during architecture discovery unless a future accepted profile governs the choice.
- Do not automatically migrate existing generated projects or alter populated project-owned directories.
- Treat project-profile-dependent layouts and Python-specific `src/<package_name>/` generation as separate future capability work.
- Use `forge-bootstrap/2.0.0` as the accepted universal bootstrap output-contract identity, distinct from Forge release versions and owned by the Chief Architect.
- Treat the ADR 0017 bootstrap contract revisions and manual compatibility guidance as accepted after focused contract review `PASS`.
- Implement `forge-bootstrap/2.0.0` through one authoritative runtime identity shared by template
  rendering, dry-run reporting, successful generation reporting, and verification.
- Keep the universal bootstrap output fixed at eight contracted directories and eight generated
  files until a separately accepted output-contract revision changes it.
- Keep generated README and AI handoff guidance explicit that source layout is selected during
  architecture discovery, and keep universal `.gitignore` defaults language-neutral.
- Select Project Memory Health as CS-002.3, the next Governance Runtime increment after the closed
  Status Service and Version Consistency slices.
- Extend `forge status` through deterministic, read-only project-memory checks before pursuing JSON
  output, persistence, release readiness evaluation, or further Version Consistency enhancement.
- Reuse the existing Governance Runtime status result model for CS-002.3; do not create a shared
  result-model prerequisite without concrete evidence from Design Authority Review or a bounded
  Engineering Brief.
- Accept DAR-CS-0003's `PASS` decision for CS-002.3 and its bounded architecture: use one private
  `forge/project_memory.py` helper for deterministic parsing and reference resolution while status
  types, rule evaluation, aggregation, and CLI-facing composition remain in `forge/status.py`.
- Treat CS-002.3 as `DAR Approved`: a bounded Engineering Brief may be created and reviewed, but
  implementation remains unauthorized until that brief is accepted and `Implementation Ready`.

## Open Questions

- What project profiles should Forge support first?
- Should Forge generate files directly or produce plans for human approval?
- How strict should Forge be when a project violates standards?
- Should Forge support plugin-style extensions before `1.0`?
- What scoring model should future architecture reviews use?
- What migration metadata should generated projects store after Forge `0.2`?
- Where should Forge Review Reports be stored?
- Should review project memory updates be automatic, suggested, or manual?
- Should `forge init` eventually write template provenance metadata into generated projects?
- What packaging channel should Forge use after local editable releases?
- Should Forge `0.3` prioritize testing/CI governance or FCS-001 review persistence?
- Should `forge init` generate an architecture discovery starter or only point to one?
- Should Forge add type checking before `1.0`?
- What test coverage threshold should Forge require before review automation exists?
- What constitutional review cadence should Forge use after major milestones?
- How should Governance Runtime enforce AI Engineering Conduct without becoming brittle?
- Should a future slice add JSON output for `forge status`?
- Should a future slice persist status reports, and if so where?
- Should package metadata version match release tags before Forge publishes packages, or only after a package distribution strategy is accepted?
- Should future release policy require package metadata to match release tags before package publishing exists?
