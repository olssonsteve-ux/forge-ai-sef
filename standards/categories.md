# Standard Categories

Forge standards define expected engineering behavior.

## Categories

### Architecture Standards

Define how architecture is discovered, reviewed, documented, and changed.

Required before:

- production code
- major module boundaries
- framework extension points

### Documentation Standards

Define how project documents are written, owned, updated, and reviewed.

Required before:

- generated documentation
- documentation validation
- AI handoff automation

### Project Memory Standards

Define how `PROJECT_STATE.md`, `PROJECT_BRAIN.md`, and `AI_HANDOFF.md` remain current.

Required before:

- memory validation
- AI context bundle generation
- automated handoff updates

### Testing Standards

Define expectations for unit tests, integration tests, regression tests, and quality gates.

Required before:

- production code
- release readiness checks
- validation automation

### Git Workflow Standards

Define branch, commit, review, and merge expectations.

Required before:

- automated commits
- release branches
- generated pull request workflows

### Template Standards

Define how templates are created, versioned, reviewed, and retired.

Required before:

- template rendering
- bootstrap generation
- migration tooling

### Release Standards

Define versioning, changelog, migration, release candidate, and final release expectations.

Required before:

- release automation
- published package versions
- compatibility guarantees

### AI Collaboration Standards

Define how AI agents plan, edit, verify, document, and hand off work.

Required before:

- agent workflow automation
- multi-agent handoffs
- AI-generated project changes

## Acceptance Criteria

Every standard must define:

- purpose
- scope
- required behavior
- prohibited behavior
- exception process
- examples
- whether it is advisory or required
- how compliance can be reviewed manually
- what future automation may check

## Change Rules

- Standards begin as `Draft`.
- Standards become `Accepted` after architecture review.
- Accepted standards require an ADR when they materially change project behavior.
- Validation automation must not exceed the accepted standard it checks.
