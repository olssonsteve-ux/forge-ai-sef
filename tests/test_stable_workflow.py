"""Independent observable failures for the v1 contract (no live model required)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from forge import workflow
from forge.codex_runtime import validate_result
from forge.evidence import (
    WorkflowError,
    append_event,
    canonical,
    load_events,
    lock,
    parse_json,
    relative_path,
    task_path,
)
from forge.verification import run_process, validate_config, verify


@pytest.fixture
def repository(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    for argv in (
        ["init"],
        ["config", "user.email", "fixture@example.invalid"],
        ["config", "user.name", "Fixture"],
    ):
        subprocess.run(["git", "-C", str(root), *argv], check=True, capture_output=True)
    (root / "hello.txt").write_text("before\n")
    (root / "other.txt").write_text("preserve\n")
    (root / "forge.toml").write_text(
        'schema_version=1\n[[checks]]\nid="acceptance"\nargv=["python","-c",'
        + json.dumps("from pathlib import Path; assert Path('hello.txt').read_text()=='after\\n'")
        + "]\n"
    )
    subprocess.run(["git", "-C", str(root), "add", "."], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", "fixture"], check=True, capture_output=True
    )
    return root


def spec(**updates):
    result = {
        "schema_version": 1,
        "objective": "Change greeting",
        "scope": ["hello.txt", "new.txt"],
        "criteria": [{"id": "greeting", "text": "hello.txt contains after plus newline"}],
        "config": "forge.toml",
        "allow_dirty": False,
        "authorization": {"execute": True, "review": True, "tool_network": False},
    }
    result.update(updates)
    return result


class Runtime:
    def __init__(self, mutate=None, review_mutate=None, session="review-session", decision="PASS"):
        self.mutate = mutate
        self.review_mutate = review_mutate
        self.session = session
        self.decision = decision
        self.calls = []

    def preflight(self, cwd):
        pass

    def invoke(self, workspace, task, task_spec, *, review, attempt, evidence=None):
        self.calls.append(review)
        if review:
            if self.review_mutate:
                self.review_mutate(workspace)
            return {
                "session_id": self.session,
                "result": {
                    "summary": "Inspected actual greeting",
                    "decision": self.decision,
                    "criteria": [
                        {
                            "id": "greeting",
                            "verdict": "PASS",
                            "rationale": "Observed after and newline",
                        }
                    ],
                },
            }
        (workspace / "hello.txt").write_text("after\n")
        if self.mutate:
            self.mutate(workspace)
        return {"session_id": "executor-session", "result": {"summary": "Changed greeting"}}


def ready(root, runtime=None):
    workflow.create(root, "task", spec())
    return workflow.run(root, "task", runtime or Runtime())


def test_roundtrip_preserves_original_until_explicit_apply(repository):
    root = repository
    runtime = Runtime(lambda ws: (ws / "new.txt").write_text("new"))
    result = ready(root, runtime)
    assert result["state"] == "READY_FOR_APPLY", result
    assert runtime.calls == [False, True]
    assert (root / "hello.txt").read_text() == "before\n"
    assert not (root / "new.txt").exists()
    assert workflow.apply(root, "task")["state"] == "APPLIED"
    assert (root / "hello.txt").read_text() == "after\n"
    assert (root / "other.txt").read_text() == "preserve\n"
    assert (root / "new.txt").read_text() == "new"
    assert (task_path(root, "task") / "backups/00000000").read_text() == "before\n"
    assert workflow.apply(root, "task")["state"] == "APPLIED"
    assert subprocess.check_output(["git", "-C", str(root), "diff", "--cached"]) == b""


@pytest.mark.parametrize("mutation", ["dirty", "index", "head", "root", "config", "spec"])
def test_stale_authority_stops_before_agent(repository, tmp_path, mutation):
    root = repository
    workflow.create(root, "task", spec())
    if mutation == "dirty":
        (root / "other.txt").write_text("different")
    elif mutation == "index":
        subprocess.run(
            ["git", "-C", str(root), "update-index", "--assume-unchanged", "other.txt"], check=True
        )
        # A real staged change must alter the index evidence, not only filesystem stat cache.
        (root / "other.txt").write_text("staged")
        subprocess.run(
            ["git", "-C", str(root), "update-index", "--no-assume-unchanged", "other.txt"],
            check=True,
        )
        subprocess.run(["git", "-C", str(root), "add", "other.txt"], check=True)
    elif mutation == "head":
        subprocess.run(
            ["git", "-C", str(root), "commit", "--allow-empty", "-qm", "later"], check=True
        )
    elif mutation == "root":
        import shutil

        copied = tmp_path / "copy"
        shutil.copytree(root, copied)
        root = copied
    else:
        path = task_path(root, "task") / (mutation + ".json")
        value = parse_json(path.read_bytes())
        value["objective" if mutation == "spec" else "required_tools"] = (
            "different" if mutation == "spec" else ["absent-tool"]
        )
        path.write_bytes(canonical(value))
    runtime = Runtime()
    with pytest.raises(WorkflowError):
        workflow.run(root, "task", runtime)
    assert runtime.calls == []


def test_dirty_requires_explicit_authorization(repository):
    (repository / "hello.txt").write_text("uncommitted")
    with pytest.raises(WorkflowError, match="Dirty"):
        workflow.create(repository, "task", spec())
    workflow.create(repository, "task", spec(allow_dirty=True))
    assert (task_path(repository, "task") / "workspace/hello.txt").read_text() == "uncommitted"


@pytest.mark.parametrize(
    "mutation",
    [
        lambda ws: (ws / "other.txt").write_text("out of scope"),
        lambda ws: (ws / "unknown.txt").write_text("out of scope"),
        lambda ws: (ws / "forge.toml").write_text("schema_version=999"),
        lambda ws: (ws / ".env").write_text("secret"),
    ],
)
def test_scope_and_configuration_are_not_model_authority(repository, mutation):
    result = ready(repository, Runtime(mutation))
    assert result["state"] == "BLOCKED"
    assert (repository / "hello.txt").read_text() == "before\n"


def test_failed_verification_cannot_reach_reviewer(repository):
    runtime = Runtime(lambda ws: (ws / "hello.txt").write_text("wrong"))
    result = ready(repository, runtime)
    assert result["state"] == "BLOCKED"
    assert result["evidence"]["verification"]["status"] == "FAIL"
    assert runtime.calls == [False]


@pytest.mark.parametrize(
    "runtime",
    [
        Runtime(session="executor-session"),
        Runtime(review_mutate=lambda ws: (ws / "hello.txt").write_text("review mutation")),
        Runtime(decision="NEEDS_CHANGES"),
    ],
)
def test_review_is_fresh_readonly_and_must_pass(repository, runtime):
    result = ready(repository, runtime)
    assert result["state"] in {"BLOCKED", "NEEDS_CHANGES"}
    with pytest.raises(WorkflowError):
        workflow.apply(repository, "task")


def test_stale_candidate_refuses_apply(repository):
    assert ready(repository)["state"] == "READY_FOR_APPLY"
    (task_path(repository, "task") / "workspace/hello.txt").write_text("after review")
    with pytest.raises(WorkflowError, match="workspace changed"):
        workflow.apply(repository, "task")
    assert (repository / "hello.txt").read_text() == "before\n"


def test_unknown_execution_needs_explicit_retry_and_rechecks(repository):
    workflow.create(repository, "task", spec())
    task = task_path(repository, "task")
    append_event(task, "EXECUTING", {"attempt": 1})
    runtime = Runtime()
    with pytest.raises(WorkflowError, match="not READY"):
        workflow.run(repository, "task", runtime)
    assert not runtime.calls
    with pytest.raises(WorkflowError):
        workflow.resume(repository, "task", "")
    assert workflow.resume(repository, "task", "Inspected interrupted execution")["attempt"] == 2
    assert workflow.run(repository, "task", runtime)["state"] == "READY_FOR_APPLY"
    assert runtime.calls == [False, True]


def test_partial_apply_retry_preserves_backup_and_accepts_only_own_values(repository, monkeypatch):
    root = repository
    assert (
        ready(root, Runtime(lambda ws: (ws / "new.txt").write_text("new")))["state"]
        == "READY_FOR_APPLY"
    )
    original = workflow.write_new

    def crash(path, content):
        if path.name.startswith("apply-00000001-"):
            raise OSError("Injected crash after first replacement")
        original(path, content)

    monkeypatch.setattr(workflow, "write_new", crash)
    with pytest.raises(OSError):
        workflow.apply(root, "task")
    assert workflow.show(root, "task")["state"] == "APPLYING"
    assert (root / "hello.txt").read_text() == "after\n"
    assert not (root / "new.txt").exists()
    monkeypatch.setattr(workflow, "write_new", original)
    (root / "hello.txt").write_text("third-party edit")
    with pytest.raises(WorkflowError, match="third-party"):
        workflow.apply(root, "task")
    assert (root / "hello.txt").read_text() == "third-party edit"
    (root / "hello.txt").write_text("after\n")
    assert workflow.apply(root, "task")["state"] == "APPLIED"
    assert (task_path(root, "task") / "backups/00000000").read_text() == "before\n"


def test_protected_secrets_not_copied_or_read(repository, monkeypatch):
    (repository / ".env").write_text("do-not-copy")
    original = Path.read_bytes

    def guarded(path):
        assert path.name != ".env"
        return original(path)

    monkeypatch.setattr(Path, "read_bytes", guarded)
    workflow.create(repository, "task", spec(allow_dirty=True))
    task = task_path(repository, "task")
    assert not (task / "workspace/.env").exists()
    assert ".env" in load_events(task)[0]["payload"]["baseline"]["excluded"]


@pytest.mark.parametrize(
    "path", ["../x", "/x", "a/../b", "a\\b", "C:x", "nul", "foo.", "a?", "x//y"]
)
def test_unsafe_paths_rejected(path):
    with pytest.raises(WorkflowError):
        relative_path(path)


@pytest.mark.parametrize("data", [b'{"a":1,"a":2}', b'{"n":NaN}', b'{"a":', b"\xff"])
def test_noncanonical_input_cannot_hide_ambiguity(data):
    with pytest.raises(WorkflowError):
        parse_json(data)


@pytest.mark.parametrize("corruption", ["partial", "gap", "modified"])
def test_event_corruption_blocks(repository, corruption):
    workflow.create(repository, "task", spec())
    events = task_path(repository, "task") / "events"
    if corruption == "partial":
        (events / "00000001.json").write_text("{")
    elif corruption == "gap":
        (events / "00000002.json").write_text("{}")
    else:
        path = events / "00000000.json"
        path.write_bytes(path.read_bytes().replace(b'"attempt":1', b'"attempt":2'))
    with pytest.raises(WorkflowError):
        workflow.show(repository, "task")


def test_os_lock_blocks_second_owner_and_releases(tmp_path):
    path = tmp_path / "lock"
    with lock(path):
        with pytest.raises(WorkflowError):
            with lock(path):
                pytest.fail("Two owners acquired same lock")
    with lock(path):
        pass


def test_verification_timeout_output_limit_missing_and_nonzero(tmp_path):
    timed = run_process([sys.executable, "-c", "import time; time.sleep(30)"], tmp_path, 1)
    assert timed["status"] == "BLOCKED" and timed["reason"] == "TIMEOUT"
    assert timed["seconds"] < 10
    failed = run_process([sys.executable, "-c", "raise SystemExit(7)"], tmp_path, 10)
    assert failed["status"] == "FAIL" and failed["exit_code"] == 7
    flooded = run_process([sys.executable, "-c", "print('x'*2000000)"], tmp_path, 10)
    assert flooded["status"] == "BLOCKED" and flooded["reason"] == "OUTPUT_LIMIT"
    missing = verify(
        tmp_path,
        {
            "schema_version": 1,
            "checks": [{"id": "missing", "argv": ["forge-absolutely-nonexistent-executable"]}],
        },
    )
    assert missing["status"] == "BLOCKED" and not missing["checks"]


def test_checks_cannot_modify_sources_and_reuse_pass(repository):
    config = repository / "forge.toml"
    config.write_text(
        'schema_version=1\n[[checks]]\nid="bad"\nargv=["python","-c",'
        + json.dumps("from pathlib import Path; Path('hello.txt').write_text('mutated')")
        + "]\n"
    )
    workflow.create(repository, "task", spec(allow_dirty=True))
    runtime = Runtime()
    result = workflow.run(repository, "task", runtime)
    assert result["state"] == "BLOCKED"
    assert "Verification modified" in result["evidence"]["error"]
    assert runtime.calls == [False]


def test_artifacts_are_excluded_but_initial_files_are_authoritative(repository):
    def build(ws):
        (ws / "build").mkdir()
        (ws / "build/log.txt").write_text("build output")

    assert ready(repository, Runtime(build))["state"] == "READY_FOR_APPLY"
    workflow.apply(repository, "task")
    assert not (repository / "build").exists()


@pytest.mark.parametrize("value", [True, 0, 2, "1"])
def test_config_version_is_strict(value):
    with pytest.raises(WorkflowError):
        validate_config({"schema_version": value, "checks": [{"id": "a", "argv": ["python"]}]})


def test_review_cannot_omit_or_forge_criteria():
    criteria = [{"id": "real", "text": "required"}]
    for items in (
        [],
        [{"id": "fake", "verdict": "PASS", "rationale": "claimed"}],
        [{"id": "real", "verdict": "FAIL", "rationale": "broken"}],
    ):
        with pytest.raises(WorkflowError):
            validate_result(
                {"summary": "claimed", "decision": "PASS", "criteria": items}, criteria, review=True
            )


def test_case_alias_cannot_bypass_secrets_or_configuration(repository):
    from forge.evidence import excluded

    assert excluded("Credentials.JSON", ["credentials.json"])
    (repository / "forge.toml").rename(repository / "FORGE.TOML")
    with pytest.raises(WorkflowError, match="configuration"):
        workflow.create(repository, "task", spec(scope=["FORGE.TOML"], allow_dirty=True))
    with pytest.raises(WorkflowError, match="scope"):
        workflow.check_scope(
            {"FORGE.TOML": "old"},
            {"FORGE.TOML": "new"},
            spec(scope=["FORGE.TOML"]),
            validate_config({"schema_version": 1, "checks": [{"id": "a", "argv": ["python"]}]}),
        )


def test_partial_staging_never_creates_partial_original(repository, monkeypatch):
    root = repository
    assert (
        ready(root, Runtime(lambda ws: (ws / "new.txt").write_text("complete new content")))[
            "state"
        ]
        == "READY_FOR_APPLY"
    )
    original = workflow.write_new

    def fail_staging(path, content):
        if path.name.startswith("apply-00000001-"):
            original(path, content[:3])
            raise OSError("Power loss simulation during staging")
        original(path, content)

    monkeypatch.setattr(workflow, "write_new", fail_staging)
    with pytest.raises(OSError):
        workflow.apply(root, "task")
    assert not (root / "new.txt").exists()
    monkeypatch.setattr(workflow, "write_new", original)
    assert workflow.apply(root, "task")["state"] == "APPLIED"
    assert (root / "new.txt").read_text() == "complete new content"


def test_process_descendants_die_with_parent_and_timeout(tmp_path):
    import time

    marker = tmp_path / "orphan.txt"
    child = (
        "import time,pathlib;time.sleep(2);pathlib.Path("
        + repr(str(marker))
        + ").write_text('BAD')"
    )
    for parent_tail, timeout in (("", 10), (";import time;time.sleep(30)", 1)):
        parent = "import subprocess,sys;subprocess.Popen([sys.executable,'-c'," + repr(child) + "])"
        result = run_process([sys.executable, "-c", parent + parent_tail], tmp_path, timeout)
        assert result["status"] == ("PASS" if not parent_tail else "BLOCKED")
        time.sleep(2.2)
        assert not marker.exists()


def test_process_is_suspended_until_job_assignment(monkeypatch, tmp_path):
    import os

    import forge.verification as module

    original = module.subprocess.Popen
    observed = []

    def capture(*args, **kwargs):
        observed.append(kwargs.get("creationflags"))
        return original(*args, **kwargs)

    monkeypatch.setattr(module.subprocess, "Popen", capture)
    assert run_process([sys.executable, "-c", "pass"], tmp_path, 10)["status"] == "PASS"
    assert observed == [4 if os.name == "nt" else 0]


def test_runtime_environment_does_not_inherit_sessions_or_keys(monkeypatch):
    from forge.codex_runtime import runtime_environment

    monkeypatch.setenv("CODEX_PERMISSION_PROFILE", "host-session-policy")
    monkeypatch.setenv("CODEX_APP_TOOLS_PIPE_PATH", "host-ipc")
    monkeypatch.setenv("OPENAI_API_KEY", "should-not-copy")
    values = runtime_environment()
    assert "CODEX_PERMISSION_PROFILE" not in values
    assert "CODEX_APP_TOOLS_PIPE_PATH" not in values
    assert "OPENAI_API_KEY" not in values


@pytest.mark.parametrize("failure", ["no-thread", "no-completion", "malformed", "turn-failed"])
def test_adapter_requires_observed_runtime_completion(tmp_path, monkeypatch, failure):
    import forge.codex_runtime as module

    instance = module.CodexRuntime()
    instance.executable = "codex"
    events = [
        {"type": "thread.started", "thread_id": "real-thread"},
        {"type": "item.completed", "item": {"type": "agent_message", "text": '{"summary":"done"}'}},
        {"type": "turn.completed", "usage": {}},
    ]
    if failure == "no-thread":
        events.pop(0)
    elif failure == "no-completion":
        events.pop()
    elif failure == "malformed":
        events[1]["item"]["text"] = '{"summary":"fake","session_id":"invented"}'
    else:
        events.append({"type": "turn.failed"})
    monkeypatch.setattr(
        module,
        "run_process",
        lambda *args, **kwargs: {
            "status": "PASS",
            "stdout": "\n".join(json.dumps(item) for item in events),
            "stderr": "",
            "seconds": 1,
            "exit_code": 0,
        },
    )
    with pytest.raises(WorkflowError):
        instance.invoke(tmp_path, tmp_path, workflow.validate_spec(spec()), review=False, attempt=1)


def test_verification_can_only_generate_declared_artifacts(repository):
    (repository / "build").mkdir()
    (repository / "build/owned.txt").write_text("authoritative")
    workflow.create(repository, "task", spec(allow_dirty=True))
    result = workflow.run(
        repository,
        "task",
        Runtime(lambda ws: (ws / "build/owned.txt").write_text("not an artifact")),
    )
    assert result["state"] == "BLOCKED"


def test_symlink_and_junction_paths_block(tmp_path):
    import os

    from forge.evidence import safe_path

    target = tmp_path / "target"
    target.mkdir()
    alias = tmp_path / "alias"
    if os.name == "nt":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(alias), str(target)], check=True, capture_output=True
        )
    else:
        alias.symlink_to(target, target_is_directory=True)
    with pytest.raises(WorkflowError, match="reparse"):
        safe_path(tmp_path, "alias/file")


def test_deletion_is_journaled_and_backup_survives(repository):
    root = repository
    workflow.create(root, "task", spec(scope=["hello.txt", "other.txt"]))
    result = workflow.run(root, "task", Runtime(lambda ws: (ws / "other.txt").unlink()))
    assert result["state"] == "READY_FOR_APPLY"
    workflow.apply(root, "task")
    assert not (root / "other.txt").exists()
    assert (task_path(root, "task") / "backups/00000001").read_text() == "preserve\n"


def test_windows_extended_root_alias_uses_same_identity(repository):
    import os

    if os.name != "nt":
        pytest.skip("Native Windows path alias")
    extended = Path("\\\\?\\" + str(repository))
    assert workflow.root_identity(extended) == workflow.root_identity(repository)
    workflow.create(extended, "task", spec())
    assert workflow.run(repository, "task", Runtime())["state"] == "READY_FOR_APPLY"
    assert workflow.apply(extended, "task")["state"] == "APPLIED"


def test_checks_do_not_discover_original_git_above_snapshot(repository):
    from forge.verification import verify

    workflow.create(repository, "task", spec())
    workspace = task_path(repository, "task") / "workspace"
    result = verify(
        workspace,
        {
            "schema_version": 1,
            "checks": [
                {
                    "id": "no-parent-git",
                    "argv": [
                        "python",
                        "-c",
                        "import subprocess; p=subprocess.run(['git','rev-parse','--show-toplevel'],"
                        "capture_output=True); assert p.returncode != 0",
                    ],
                }
            ],
        },
    )
    assert result["status"] == "PASS"


def test_status_accepts_dotnet_without_python_configuration(tmp_path):
    from forge.status import StatusState, _testing_status

    (tmp_path / "tests").mkdir()
    (tmp_path / "Application.sln").write_text("")
    report = _testing_status(tmp_path)
    assert report.state == StatusState.OK
    assert not (tmp_path / "pyproject.toml").exists()


def test_cli_verify_and_task_errors_are_structured(tmp_path, monkeypatch):
    from typer.testing import CliRunner

    from forge.cli import app

    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(app, ["verify"])
    assert result.exit_code == 2
    assert json.loads(result.stdout)["status"] == "BLOCKED"
    result = runner.invoke(app, ["task", "show", "../escape"])
    assert result.exit_code == 2
    assert json.loads(result.stdout)["status"] == "BLOCKED"
    for command in (["--help"], ["task", "--help"], ["status"]):
        assert runner.invoke(app, command).exit_code == 0
