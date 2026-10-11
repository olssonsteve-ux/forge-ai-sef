# Forge: statement of intent

> Build software with intention.

## Why Forge exists

Forge exists to help people turn an idea into working, verified and maintainable software with
AI agents, with as little unnecessary manual work and administration as possible.

A person should be able to explain what they want, set meaningful boundaries and remain in control
of important decisions. Agents should carry the engineering work forward: clarify the problem,
implement the agreed behavior, test it, review it and resolve defects. The result should be
supported by evidence that another person or agent can inspect.

Forge is an AI-Native Software Engineering Platform. Its foundation is a practical engineering
concept: preserve intent, give agents clear authority, make changes reviewable and establish what
actually works. The software in this repository implements part of that concept.

## What we want to make possible

- Move from an idea to a usable result through one coherent engineering workflow.
- Keep goals, requirements, decisions and project knowledge available across sessions and agents.
- Let agents complete authorized work without repeatedly asking for the same permission.
- Use independent review and meaningful tests to expose mistakes, including mistakes in the tests.
- Resume interrupted work without silently losing decisions or accepting incomplete results.
- Bring the human back when a consequential decision needs human judgment.
- Improve the method through evidence from real projects and advances in agents and language models.

Forge should be useful for building software and for maintaining it months or years later.
People should be able to understand what changed, why it changed and what evidence supports it.

## Administration must earn its place

Governance should help work move forward. Each rule and record should protect a concrete outcome:
clarity, correctness, safety, continuity or maintainability.

One work item should have one authoritative evidence record, linked from concise project memory.
Existing authorization should carry through ordinary work within its scope. A minor correction
should not create a new administrative campaign. We will judge simplification by better engineering
outcomes, not just fewer documents or more generated code.

Lessons from building Audio Recorder informed this approach. They revealed both the value of
durable project memory and the cost of duplicated records and repeated approvals. This is evidence
for improving the method, not a claim that its productivity benefits have already been measured.

## Human authority and agent responsibility

Humans set purpose, acceptable risk and important boundaries. Agents work within that authority.
An agent's statement that a task succeeded is not enough: tests, observable behavior and review
must support it. Failures and uncertainty remain visible.

The concept is intended to evolve with different agents and models. The current implementation
uses one Codex CLI integration. Other providers and environments are future qualification work,
not capabilities we claim to support today.

## What version 1 means

The [Forge Concept v1.0 baseline](docs/Forge-Concept-v1.0.md) fixes the purpose, principles and
initial scope. It gives contributors a common foundation for testing and improving Forge.

The first public implementation is **1.0.0rc1**, tagged **v1.0.0-rc.1**. It is a testing prerelease.
Its automated tests, bounded code review and package checks have passed, but actual agent execution,
independent runtime review and apply have not completed end to end in the qualification environment.
A tool-policy rejection remains unresolved. We do not call this implementation a stable 1.0 release.

Freezing the concept does not erase defects or freeze learning. Corrections remain welcome;
material changes to the agreed purpose or boundaries require an explicit, reviewable decision.

## Open participation and cost

Forge is available under the [MIT License](LICENSE). Anyone may use, study, modify and redistribute
it, including commercially, while preserving the required copyright and license notices.

Forge itself has no license fee. AI accounts, model usage, hosting and other third-party services
may have their own costs and terms. The MIT license also permits others to sell modified versions;
it does not require all downstream copies to remain free of charge.

We welcome practical trials, reproducible bug reports, thoughtful criticism and improvements.
Start with a disposable repository or a backup, follow the [testing guide](docs/Forge-1.0-guide.md),
and share what worked, what failed and what caused unnecessary effort through
[GitHub Issues](https://github.com/olssonsteve-ux/forge-ai-sef/issues).

Our ambition is simple: make AI-assisted engineering easier to carry through, easier to trust
and easier to continue.
