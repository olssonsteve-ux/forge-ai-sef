# ADR 0019 â€” Stable isolated task kernel

Date: 2026-10-11
Status: Accepted for implementation under the owner's request to complete Forge 1.0 and the
independent design review recorded in [the assurance record](../engineering/Forge-1.0-assurance.md).

Forge 1.0 adds explicit language-neutral verification and operator-driven isolated tasks with
fresh review and journaled apply. Use the existing authenticated Codex CLI rather than adding a
provider SDK dependency. Runtime authority belongs to Forge's task specification and evidence;
model responses cannot grant permissions, close work or release software.

The linked assurance record owns the specification, engineering brief, acceptance evidence and
review findings. Do not duplicate these in handoff documents. Five small runtime modules separate
filesystem evidence, process lifetime, verification policy, Codex transport and orchestration.
There is no arbitrary LOC ceiling for this kernel; independently review its bounded responsibilities.

Quarantine the failed/terminated FAL runtime experiments from installed wheel and sdist code,
preserving their repository source and all unresolved findings. Their acceptance and budgets are
unchanged. The new task contract does not implement their autonomous correction-loop capability.

Bootstrap templates keep the eight-output contract and gain explicit 1.x compatibility. Projects
are never migrated automatically. Qualification starts with Windows x64, CPython 3.14 and
Codex CLI 0.160.0. Other runtime versions fail closed until qualified.

A locally verified 1.0 candidate is allowed. Commit, tag, publication and human closure remain
separate authority; the owner's no-commit instruction is still active.
