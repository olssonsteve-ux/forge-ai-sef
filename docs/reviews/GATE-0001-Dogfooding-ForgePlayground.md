# GATE-0001 - Dogfooding ForgePlayground

Date: 2026-07-08

Reviewed Forge version/tag: `v0.2.1`

Generated project: `ForgePlayground`

Command executed from outside the Forge repository:

```text
python -m forge init ForgePlayground
```

## Purpose

Gate 1 verifies that Forge can bootstrap a new project from outside its own repository and that the generated project is useful as the starting point for a real AI-assisted software project.

This is a dogfooding review, not a feature implementation milestone.

## Result

The command completed successfully and generated a usable Forge-governed project foundation.

Output:

```text
Forge project initialized: ForgePlayground
Created folders: 9
Created files: 8
Next step: review PROJECT_STATE.md and begin architecture discovery.
```

## Generated Structure

Observed generated structure:

```text
ForgePlayground/
+-- .gitignore
+-- AI_HANDOFF.md
+-- CHANGELOG.md
+-- LICENSE
+-- PROJECT_BRAIN.md
+-- PROJECT_STATE.md
+-- README.md
+-- ROADMAP.md
+-- docs/
|   +-- architecture/
|   +-- contracts/
|   +-- decisions/
|   +-- vision/
+-- forge/
+-- standards/
+-- templates/
+-- tests/
```

The generated project did not contain `src/`. It contained `forge/`, which matches the current `forge init` contract but may be confusing for generated projects that are not Forge itself.

## What Worked

- The CLI ran successfully from outside the Forge repository.
- The project name was accepted and used consistently in generated documents.
- The expected root memory documents were generated.
- The generated folders provide a clear documentation-first starting point.
- The output was concise and action-oriented.
- Generated file contents were visibly template-based and contained project-specific substitutions.
- The generated project gives future AI agents immediate orientation through `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, and `AI_HANDOFF.md`.

## What Was Confusing

- The generated project reports `Initialized with Forge 0.2.0` even though the dogfooding release tag is `v0.2.1`. This is traceability drift between package version and release tag.
- The generated implementation placeholder is named `forge/`. For a general bootstrap framework, `src/` would be less confusing and less likely to imply that every generated project is part of Forge itself.
- The generated `PROJECT_BRAIN.md` repeats the default description when no project description is supplied.
- Empty documentation directories are correct for a foundation, but new users may not know which document to create first.

## What Was Missing

- No generated `src/` directory, despite Gate 1 review expectations mentioning `src/`.
- No first architecture discovery document template is generated.
- No initial ADR placeholder is generated.
- No template provenance record is written into the generated project.
- No explicit generated-project checklist tells the maintainer how to move from bootstrap to architecture discovery.
- No generated testing standard or test strategy placeholder exists yet.

## Template Quality

The bootstrap templates are good enough for Forge `0.2.x`.

They establish:

- project identity
- project state
- project brain
- AI handoff context
- changelog
- roadmap
- license placeholder
- basic Git ignore rules

They are intentionally minimal, which is appropriate for `0.2.x`. Before Forge `0.3`, the templates should become more actionable without turning `forge init` into application generation.

## Project State Usefulness

`PROJECT_STATE.md` is useful. It tells a new maintainer what exists, what does not exist, and what to do next.

Improvement needed: it should include a clearer "first session checklist" for architecture discovery and should distinguish generated defaults from project-specific accepted facts.

## Project Brain Usefulness

`PROJECT_BRAIN.md` is useful as a durable project memory seed.

Improvement needed: it should avoid repeated generic descriptions and should better prompt the maintainer to record durable beliefs, constraints, and project-specific decisions.

## AI Handoff Usefulness

`AI_HANDOFF.md` is useful. It clearly tells future AI agents to read project memory before making changes and to avoid undocumented implementation assumptions.

Improvement needed: it should include the recommended first action sequence for a newly bootstrapped project.

## Folder Structure Assessment

The documentation folders are correct for a documentation-first project foundation.

The `tests/`, `templates/`, and `standards/` placeholders are reasonable.

The `forge/` placeholder should be reconsidered before Forge `0.3`. A neutral `src/` placeholder is more appropriate for arbitrary generated projects, while Forge itself can continue to use `forge/` as its package directory.

## Usefulness For A Real AI-Assisted Project

The generated project is useful as a starting foundation for a real AI-assisted software project, especially when the project is still in discovery.

It is not yet sufficient as a complete engineering starter. It lacks:

- a first architecture discovery template
- initial ADR scaffold
- testing strategy scaffold
- project-specific setup checklist
- template provenance metadata

These omissions are acceptable for Forge `0.2.x` but should shape Forge `0.3`.

## Recommended Improvements

Immediate:

- Document the version traceability issue between `v0.2.1` and generated `0.2.0` output.
- Treat the `forge/` versus `src/` mismatch as a Forge `0.3` design decision, not a silent implementation change.

Forge `0.3`:

- Decide whether generated projects should use `src/` instead of `forge/`.
- Add generated-project template provenance.
- Add an architecture discovery template or first-session checklist.
- Improve the default `PROJECT_BRAIN.md` wording when optional description is empty.
- Align package version, release tag, and generated `FORGE_VERSION` behavior.

Forge `0.4`:

- Add template migration guidance.
- Add stronger project profile support only after the bootstrap defaults are stable.

## Risks

Critical risks:

- None found during Gate 1.

Medium risks:

- Generated `forge/` folder may confuse users into thinking generated projects must be Forge packages.
- Release tag and generated Forge version can drift.
- Minimal templates may leave inexperienced users unsure how to begin architecture discovery.

Future risks:

- Without template provenance, future migration tooling will have limited evidence.
- If generated project structure changes without migration guidance, early Forge-created projects may diverge quickly.

## Gate 1 Decision

PASS WITH COMMENTS

## Recommendation

Proceed to Forge `0.3`.

Forge `0.3` should prioritize resolving bootstrap structure clarity, generated version traceability, and first-session guidance before adding new capabilities.
