# ADR 0011 - Forge Constitutional Governance And Product Identity

Status: Accepted

Date: 2026-07-08

## Context

Forge has reached `0.3.0`. The bootstrap capability, project memory, Developer Platform, review specification, standards, and release workflow now need a permanent source of identity and governance.

Before adding new capabilities, Forge needs one highest governing document that future decisions derive from.

The governing document name must be selected deliberately.

Options considered:

- `CONSTITUTION.md`
- `CHARTER.md`
- `MANIFEST.md`
- another alternative

Forge also needs one official product positioning.

Options considered:

- Framework
- Toolkit
- Platform
- Engineering System
- Engineering Platform
- AI-Native Software Engineering Platform

## Evaluation Of Governing Document Names

### `CONSTITUTION.md`

Advantages:

- strongest signal of highest authority
- clearly supports hierarchy, rights, responsibilities, and amendment rules
- familiar in governance-heavy systems and open source communities
- durable enough for long-term product identity
- suitable for deriving strategy, roadmap, capabilities, briefs, implementation, review, and release

Disadvantages:

- can feel formal or heavy for a young project
- may imply rigidity if amendment rules are unclear
- requires discipline to avoid ceremonial wording without operational force

Long-term implications:

- best supports constitutional review and Design Authority Review
- makes governance clarity explicit
- scales well as Forge adds capabilities, plugins, and enterprise governance

Maintainability:

- maintainable if kept short, principle-based, and rarely amended

Governance clarity:

- highest among the options

Future scalability:

- strong fit for a platform expected to govern many future engineering decisions

### `CHARTER.md`

Advantages:

- strong open source and organizational precedent
- friendlier than Constitution
- good for describing purpose, scope, and authority

Disadvantages:

- less clearly supreme than Constitution
- can read as team-operating guidance rather than permanent governing law
- weaker for constitutional hierarchy and amendment expectations

Long-term implications:

- useful for organizational governance, but less forceful as the root of all future decisions

Maintainability:

- easy to maintain, but may need companion documents for deeper governance

Governance clarity:

- good, but not maximal

Future scalability:

- adequate for community governance, weaker for platform-wide engineering doctrine

### `MANIFEST.md`

Advantages:

- strong expression of values and beliefs
- memorable and motivating
- good for communicating philosophy

Disadvantages:

- weak as an authority document
- does not naturally define roles, hierarchy, amendment rules, or release governance
- may become inspirational rather than operational

Long-term implications:

- helpful as a cultural artifact, but insufficient as the source of engineering authority

Maintainability:

- easy to maintain because it is value-oriented

Governance clarity:

- low compared with Constitution or Charter

Future scalability:

- weak fit for enterprise governance and capability authority

### Other Alternative

Alternatives such as `GOVERNANCE.md`, `FOUNDATION.md`, or `DOCTRINE.md` were considered.

These names either narrow the scope too much, lack product resonance, or create ambiguity about whether they are higher than roadmap, architecture, or standards documents.

## Decision

Forge will use `CONSTITUTION.md` as its highest governing document.

Forge will officially describe itself as:

```text
Forge is an AI-Native Software Engineering Platform.
```

The official one-sentence product definition is:

```text
Forge provides a disciplined engineering environment where humans and AI collaborate to design, build, review, govern and evolve software.
```

## Rationale

`CONSTITUTION.md` is selected because Forge needs more than a statement of values. It needs a durable authority model that can govern product identity, capabilities, standards, implementation, reviews, releases, and future extension.

The Constitution name is intentionally formal because Forge is designed to make engineering decisions explainable and governable over time.

## Evaluation Of Product Identity

### Framework

Advantages:

- familiar to developers
- suggests reusable structure and conventions
- accurately described Forge's earliest foundation stage

Disadvantages:

- too narrow for governance, memory, review, release, and human-AI collaboration
- may imply application framework behavior that Forge explicitly rejects
- does not communicate product-level platform responsibility

Long-term implication: useful as historical context, but too small for Forge's permanent identity.

### Toolkit

Advantages:

- practical and approachable
- suggests useful commands and utilities
- avoids excessive formality

Disadvantages:

- implies loosely related tools rather than a coherent governing model
- weakens constitutional hierarchy
- does not express architecture, standards, or release authority

Long-term implication: would make Forge easier to understand initially but harder to govern as capabilities grow.

### Platform

Advantages:

- communicates a durable foundation
- supports capabilities, workflows, standards, and extension
- scales better than Framework or Toolkit

Disadvantages:

- broad without additional qualifiers
- may imply hosted infrastructure unless scoped carefully

Long-term implication: strong foundation, but incomplete without the AI-native and software engineering qualifiers.

### Engineering System

Advantages:

- emphasizes operational coherence
- describes connected engineering practices
- avoids implying an application framework

Disadvantages:

- less product-oriented
- less familiar as an open source product category
- weaker for ecosystem and extension positioning

Long-term implication: accurate internally, but less effective as the public identity of Forge.

### Engineering Platform

Advantages:

- strong, scalable, and product-oriented
- supports governance, standards, tooling, and extension
- clear fit for platform engineering principles

Disadvantages:

- does not explicitly communicate human-AI collaboration
- could describe traditional engineering tooling without AI-native assumptions

Long-term implication: close to correct, but missing the distinctive collaboration model Forge is built around.

### AI-Native Software Engineering Platform

Advantages:

- captures human-AI collaboration as a first-class design premise
- communicates durable platform scope
- remains broad enough for governance, memory, review, bootstrap, standards, and release discipline
- scales to plugin ecosystems and enterprise governance

Disadvantages:

- longer than the alternatives
- requires clear boundaries to avoid sounding like a hosted AI product

Long-term implication: best fit for a platform intended to govern AI-assisted engineering across many future capabilities.

Maintainability: strong, because it gives future docs a clear identity test.

Governance clarity: strong, because it aligns with constitutional authority and platform hierarchy.

Future scalability: strong, because it can include bootstrap, reviews, knowledge, runtime, orchestration, plugins, and enterprise governance without renaming the product.

## Consequences

- `CONSTITUTION.md` becomes the highest authority in Forge.
- README, project memory, vision, and architecture documents must derive from it.
- Future ADRs, FCS documents, engineering briefs, reviews, and release decisions should be evaluated for constitutional alignment.
- The motto `Build software with intention.` becomes the guiding principle of Forge.
- Existing "framework" language should be treated as historical or supporting language unless it conflicts with the official platform identity.

## Rejected Alternatives

`CHARTER.md` is rejected because it is strong but not sufficiently supreme for the desired constitutional hierarchy.

`MANIFEST.md` is rejected because it expresses philosophy but does not provide enough governance authority.

`GOVERNANCE.md` is rejected because it sounds procedural rather than foundational.
