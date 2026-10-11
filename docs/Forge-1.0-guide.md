# Forge 1.0 user guide

Forge provides a local, explicit workflow for governed software changes. It runs on a repository
you already own. Stable commands are init, status, verify and task create/show/run/resume/apply.
The initial qualification target is Windows x64, CPython 3.14 and Codex CLI 0.160.0.

This public testing candidate (1.0.0rc1, tag v1.0.0-rc.1) has not passed live agent qualification. Both CLI 0.160.0 and a separate
0.162.1 probe received read-only/tool-policy rejection in the build environment. No stable release
is claimed; see V1-Q-01 in the repository assurance record.

## Install and inspect

Download the wheel from https://github.com/olssonsteve-ux/forge-ai-sef/releases and install it
with python -m pip install <path-to-wheel>. No package-index publication
is claimed. python -m forge --help works after installation; forge --help is its console entrypoint.
Use forge init <name> only for a new project. For existing work, enter its Git repository root and
run forge status. Status reads files/Git metadata and does not execute project checks.

Codex is optional for init/status/verify. Task run requires the qualified CLI on PATH and an
existing codex login session. Authentication is owned by Codex; Forge never asks for a key.
Authenticated model calls use network and account usage. tool_network controls agent shell-tool
network access separately. Agent execution and review are separate sessions.

## Configure project verification once

Create an operator-owned forge.toml in the repository:

```toml
schema_version = 1
required_tools = ["python"]
excluded_paths = ["local-credentials.json"]

[[checks]]
id = "tests"
argv = ["python", "-m", "pytest", "-q"]
timeout_seconds = 300
```

For .NET, use argv = ["dotnet", "test", "AudioRecorder.sln", "--configuration", "Release"] and
required_tools = ["dotnet"]. Use the real solution filename. Commands are argv arrays, never shell
strings. cwd defaults to "." and must remain in the snapshot; timeout_seconds is 1â€“3600.
At least one and at most 32 uniquely named checks are required. Unknown configuration fields fail.

Verification commands are trusted operator code and run with the caller's permissions. Review the
configuration before invoking it. Source-changing formatters are inappropriate for task checks:
use check-only options. Build artifacts may be generated under declared artifact_dirs. Defaults:
__pycache__, .pytest_cache, .ruff_cache, bin, obj, build, dist, node_modules, .venv.
Initially captured files stay authoritative even in those directories. New artifacts are never applied.

Run forge verify explicitly. PASS exits 0, failed assertions/commands exit 1, missing tools,
malformed policy, timeout and uncertain execution exit 2. Output is bounded and redacted.
A missing configuration is BLOCKED; Forge never guesses which test command to run.

## Authorize a bounded task

Save a JSON spec (prefer outside the repository or before capturing the task):

```json
{
  "schema_version": 1,
  "objective": "Correct the greeting without changing its API.",
  "scope": ["src/greeting.py", "tests/test_greeting.py"],
  "criteria": [
    {"id": "greeting", "text": "greeting() returns exactly hej."},
    {"id": "regression", "text": "Tests cover the corrected greeting and existing API."}
  ],
  "config": "forge.toml",
  "allow_dirty": false,
  "authorization": {"execute": true, "review": true, "tool_network": false},
  "agent_timeout_seconds": 600
}
```

Scope entries authorize that file or descendants of that directory, with case-insensitive matching.
They cannot cover operator configuration or excluded/protected paths. Authorization is explicit;
neither a callback nor model output can enlarge it. IDs are lowercase letters/digits/hyphens,
1â€“48 characters. Criteria IDs must be unique and every criterion needs reviewer evidence.

```text
forge task create greeting-fix --spec C:/tasks/greeting.json
forge task show greeting-fix
forge task run greeting-fix
forge task show greeting-fix
forge task apply greeting-fix
```

Creation captures root, HEAD, Git index, tracked/nonignored file bytes and spec/configuration hashes.
Uncommitted input requires allow_dirty=true. Agent changes happen in .forge/tasks/<id>/workspace.
The original remains untouched until apply. Snapshots contain no Git metadata, and a Git ceiling
prevents accidental discovery of the original ancestor repository; checks must not rely on it. Execution, deterministic tests and a fresh read-only
review must all pass on identical source bytes before READY_FOR_APPLY. Review is evidence, not
human closure. Apply does not stage or commit anything.

## Interruptions and conflicts

Each stage records a durable start event. A killed process never implies success. Inspect task show
and the numbered events. To retry execution/checks/review, use:
forge task resume <id> --reason "Inspected the failed attempt; retry is authorized".
Then run the task again. Workspace changes are retained, attempt number increments, and all tests
and a new review are mandatory. No automatic retry or fallback agent runs.

For an interrupted APPLYING state, run forge task apply <id> again. Its existing journal and original
backups authorize only old/intended byte values. A third-party edit blocks without overwriting it.
A changed HEAD, index or unrelated file also blocks. Resolve such conflicts deliberately; create a
new task after establishing a new baseline. APPLIED is terminal.

Per-task locks prevent concurrent mutation; a repository-wide apply lock prevents two Forge apply
operations. Other tools are not locked out. Apply is atomic per file, not a multi-file transaction.
Complete new files publish by same-volume hard link with no overwrite; unsupported filesystems fail
closed. Source/backups/events are flushed and reread. No universal power-loss filesystem guarantee
is claimed. Do not delete or edit event histories to bypass a blocked state.

## Secrets, limits and trust

Do not put secrets into objectives, criteria or source files supplied to a model. Protected path
components .git, .forge, .codex, .agents, .aws, .ssh and .env/.env.* are never copied. Add all
project-specific sensitive paths to excluded_paths. This is path exclusion, not content scanning.
Ignored dependencies and inputs are not copied; provision them through explicit trusted checks.

Symlinks, Windows junctions/reparse points, unsafe/device paths and case-colliding names fail closed.
Limits: 20,000 authoritative files, 256 MiB/file, 1 GiB total snapshot, 100,000 workspace entries,
16 MiB/event, 128 KiB configuration, 1 MiB retained stdout/stderr per command.
The OS user and repository owner are trusted. Hash chains detect corruption, not an owner rewriting
an entire history. The runtime sandbox constrains tools; review still requires human judgment.

## Migration and stable boundary

No automatic migration from 0.x. Existing governance documents remain yours. Add forge.toml and a
bounded spec when adopting tasks; one linked assurance record may own scope, checks, findings and
review under ADR 0018. PROJECT_STATE owns current status, PROJECT_BRAIN durable decisions, and
AI_HANDOFF links them. An ordinary bounded fix does not need repeated handoff/correction documents.

Version-1 task/configuration contracts reject unknown fields/versions. Future incompatible schemas
require an explicit migration tool or new task; no silent reinterpretation. A new CLI/model/runtime
version must pass qualification before the supported adapter changes. Model policy is recorded as
runtime-default because CLI events do not report a resolved model ID.

The legacy autonomous FAL experiments are preserved in repository history/source but excluded from
the installed distribution. Their failed findings remain open; stable tasks do not certify that
capability. No automatic correction loops, hidden provider fallback, release automation or cloud
service is included.
