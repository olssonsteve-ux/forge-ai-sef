"""Bounded operator-driven tasks: snapshot, execute, verify, fresh review, explicit apply."""

from __future__ import annotations

import hashlib
import os
import re
import uuid
from pathlib import Path

from forge.codex_runtime import CodexRuntime, validate_result
from forge.evidence import (
    WorkflowError,
    append_event,
    canonical,
    digest,
    excluded,
    file_hash,
    hash_paths,
    load_events,
    lock,
    parse_json,
    relative_path,
    safe_path,
    task_path,
    write_new,
)
from forge.verification import load_config, redacted, run_process, validate_config, verify


def git(root: Path, *args: str) -> str:
    result = run_process(["git", "-C", str(root), *args], root, 30)
    if result["status"] != "PASS":
        raise WorkflowError("Cannot establish Git evidence: " + " ".join(args[:2]))
    return result["stdout"]


def validate_spec(value: dict) -> dict:
    fields = {
        "schema_version",
        "objective",
        "scope",
        "criteria",
        "config",
        "allow_dirty",
        "authorization",
        "agent_timeout_seconds",
    }
    if not isinstance(value, dict) or set(value) - fields:
        raise WorkflowError("Unknown task specification field.")
    spec = dict(value)
    if type(spec.get("schema_version")) is not int or spec["schema_version"] != 1:
        raise WorkflowError("Unsupported task specification version.")
    if not isinstance(spec.get("objective"), str) or not 1 <= len(spec["objective"]) <= 16000:
        raise WorkflowError("A bounded task objective is required.")
    scope = spec.get("scope")
    if not isinstance(scope, list) or not 1 <= len(scope) <= 128:
        raise WorkflowError("Explicit nonempty task scope is required.")
    for item in scope:
        relative_path(item)
    if len(set(scope)) != len(scope):
        raise WorkflowError("Duplicate scope entry.")
    criteria = spec.get("criteria")
    if not isinstance(criteria, list) or not 1 <= len(criteria) <= 64:
        raise WorkflowError("Explicit acceptance criteria are required.")
    ids = set()
    for item in criteria:
        if (
            not isinstance(item, dict)
            or set(item) != {"id", "text"}
            or not isinstance(item["id"], str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", item["id"])
            or item["id"] in ids
            or not isinstance(item["text"], str)
            or not 1 <= len(item["text"]) <= 4000
        ):
            raise WorkflowError("Invalid acceptance criterion.")
        ids.add(item["id"])
    authorization = spec.get("authorization")
    if (
        not isinstance(authorization, dict)
        or set(authorization) != {"execute", "review", "tool_network"}
        or authorization["execute"] is not True
        or authorization["review"] is not True
        or type(authorization["tool_network"]) is not bool
    ):
        raise WorkflowError("Explicit execution, review and network authorization is required.")
    if type(spec.get("allow_dirty")) is not bool:
        raise WorkflowError("allow_dirty must be explicit.")
    spec.setdefault("config", "forge.toml")
    relative_path(spec["config"])
    timeout = spec.setdefault("agent_timeout_seconds", 600)
    if type(timeout) is not int or not 1 <= timeout <= 3600:
        raise WorkflowError("Agent timeout must be 1â€“3600 seconds.")
    return spec


def in_scope(path: str, scope: list[str]) -> bool:
    return any(
        path.casefold() == item.casefold() or path.casefold().startswith(item.casefold() + "/")
        for item in scope
    )


def root_identity(root: Path) -> str:
    value = str(root.resolve())
    if os.name == "nt":
        if value.startswith("\\\\?\\UNC\\"):
            value = "\\\\" + value[8:]
        elif value.startswith("\\\\?\\"):
            value = value[4:]
        value = os.path.normcase(value)
    return value


def baseline(root: Path, config: dict) -> dict:
    root = safe_path(root)
    actual = Path(git(root, "rev-parse", "--show-toplevel").strip()).resolve()
    if not root.samefile(actual):
        raise WorkflowError("Run Forge from the repository root.")
    names = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split("\0")
    names = sorted(set(name for name in names if name))
    excluded_names = [name for name in names if excluded(name, config["excluded_paths"])]
    accepted = [name for name in names if name not in set(excluded_names)]
    return {
        "root": root_identity(root),
        "head": git(root, "rev-parse", "HEAD").strip(),
        "index": hashlib.sha256(git(root, "ls-files", "--stage", "-z").encode()).hexdigest(),
        "files": hash_paths(root, accepted),
        "excluded": excluded_names,
    }


def comparable(value: dict) -> dict:
    return {key: value[key] for key in ("root", "head", "index", "files")}


def candidate(workspace: Path, initial: dict, config: dict) -> dict:
    safe_path(workspace)
    names = set(initial)
    count = 0
    for directory, dirs, files in os.walk(workspace, followlinks=False):
        for name in dirs + files:
            count += 1
            if count > 100000:
                raise WorkflowError("Workspace entry limit exceeded.")
            path = Path(directory) / name
            relative = path.relative_to(workspace).as_posix()
            safe_path(workspace, relative)
            if excluded(relative, config["excluded_paths"]):
                raise WorkflowError("Protected or excluded content appeared in workspace.")
        for name in files:
            relative = (Path(directory) / name).relative_to(workspace).as_posix()
            if relative in initial or not any(
                part.casefold() in {entry.casefold() for entry in config["artifact_dirs"]}
                for part in relative.split("/")[:-1]
            ):
                names.add(relative)
    return hash_paths(workspace, sorted(names))


def changes(initial: dict, current: dict) -> list[str]:
    return sorted(
        name for name in initial.keys() | current.keys() if initial.get(name) != current.get(name)
    )


def check_scope(initial: dict, current: dict, spec: dict, config: dict) -> None:
    for name in changes(initial, current):
        if (
            not in_scope(name, spec["scope"])
            or name.casefold() in {"forge.toml", spec["config"].casefold()}
            or excluded(name, config["excluded_paths"])
        ):
            raise WorkflowError("Workspace change is outside authorized scope: " + name)


def create(root: Path, identifier: str, raw_spec: dict) -> dict:
    root = safe_path(root)
    task = task_path(root, identifier)
    spec = validate_spec(raw_spec)
    config = load_config(root, spec["config"])
    for path in spec["scope"]:
        if (
            excluded(path, config["excluded_paths"])
            or path.casefold() in {"forge.toml", spec["config"].casefold()}
            or in_scope(spec["config"], [path])
            or in_scope("forge.toml", [path])
        ):
            raise WorkflowError("Scope overlaps operator configuration or protected paths.")
    with lock(root / ".forge" / "tasks" / (identifier + ".lock")):
        if task.exists():
            raise WorkflowError("Task already exists; create never overwrites evidence.")
        initial = baseline(root, config)
        dirty = git(
            root, "status", "--porcelain", "--untracked-files=all", "--", ".", ":(exclude).forge"
        )
        if dirty.strip() and not spec["allow_dirty"]:
            raise WorkflowError("Dirty repository requires explicit allow_dirty.")
        task.mkdir()
        workspace = task / "workspace"
        workspace.mkdir()
        write_new(task / "spec.json", canonical(spec))
        write_new(task / "config.json", canonical(config))
        for name, expected in initial["files"].items():
            if expected is None:
                continue
            source = safe_path(root, name)
            destination = safe_path(workspace, name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            write_new(destination, source.read_bytes())
        if candidate(workspace, initial["files"], config) != initial["files"]:
            raise WorkflowError("Snapshot copy did not match captured baseline.")
        if comparable(baseline(root, config)) != comparable(initial):
            raise WorkflowError("Original changed during snapshot creation.")
        event = append_event(
            task,
            "READY",
            {
                "spec_hash": digest(spec),
                "config_hash": digest(config),
                "baseline": initial,
                "attempt": 1,
            },
        )
        return {"id": identifier, "state": event["state"], "attempt": 1}


def load(root: Path, identifier: str):
    task = task_path(root, identifier)
    events = load_events(task)
    first = events[0]["payload"]
    spec = validate_spec(parse_json(safe_path(task, "spec.json").read_bytes()))
    config = validate_config(parse_json(safe_path(task, "config.json").read_bytes()))
    if first.get("spec_hash") != digest(spec) or first.get("config_hash") != digest(config):
        raise WorkflowError("Task authority/configuration digest changed.")
    initial = first.get("baseline")
    if not isinstance(initial, dict) or initial.get("root") != root_identity(root):
        raise WorkflowError("Task belongs to a different repository.")
    attempt = [event["payload"].get("attempt") for event in events if event["state"] == "READY"]
    if attempt != list(range(1, len(attempt) + 1)):
        raise WorkflowError("Invalid task attempt sequence.")
    return task, events, spec, config, initial, attempt[-1]


def show(root: Path, identifier: str) -> dict:
    _, events, _, _, _, attempt = load(root, identifier)
    return {
        "id": identifier,
        "state": events[-1]["state"],
        "attempt": attempt,
        "last_event_hash": events[-1]["hash"],
        "evidence": events[-1]["payload"],
    }


def unchanged(root: Path, initial: dict, config: dict) -> None:
    if comparable(baseline(root, config)) != comparable(initial):
        raise WorkflowError("Original repository baseline changed; task cannot proceed.")


def run(root: Path, identifier: str, runtime=None) -> dict:
    task = task_path(root, identifier)
    with lock(root / ".forge" / "tasks" / (identifier + ".lock")):
        task, events, spec, config, initial, attempt = load(root, identifier)
        if events[-1]["state"] != "READY":
            raise WorkflowError(
                "Task is not READY. Inspect evidence; explicitly resume if appropriate."
            )
        unchanged(root, initial, config)
        workspace = safe_path(task, "workspace")
        check_scope(initial["files"], candidate(workspace, initial["files"], config), spec, config)
        append_event(task, "EXECUTING", {"attempt": attempt})
        runtime = runtime or CodexRuntime()
        try:
            runtime.preflight(workspace)
            execution = runtime.invoke(workspace, task, spec, review=False, attempt=attempt)
            validate_result(execution["result"], spec["criteria"], review=False)
            if not isinstance(execution.get("session_id"), str) or not execution["session_id"]:
                raise WorkflowError("Executor session evidence is absent.")
            task, _, spec, config, initial, _ = load(root, identifier)
            unchanged(root, initial, config)
            snapshot = candidate(workspace, initial["files"], config)
            check_scope(initial["files"], snapshot, spec, config)
            append_event(task, "EXECUTED", {"runtime": execution, "candidate": snapshot})
            append_event(task, "VERIFYING", {"candidate_hash": digest(snapshot)})
            verification = verify(workspace, config)
            task, _, spec, config, initial, _ = load(root, identifier)
            unchanged(root, initial, config)
            if candidate(workspace, initial["files"], config) != snapshot:
                raise WorkflowError("Verification modified authoritative workspace files.")
            if verification["status"] != "PASS":
                append_event(task, "BLOCKED", {"verification": verification})
                return show(root, identifier)
            append_event(
                task, "VERIFIED", {"verification": verification, "candidate_hash": digest(snapshot)}
            )
            append_event(task, "REVIEWING", {"candidate_hash": digest(snapshot)})
            # Bounded evidence summary; reviewers inspect actual files independently.
            review = runtime.invoke(
                workspace,
                task,
                spec,
                review=True,
                attempt=attempt,
                evidence={
                    "checks": [
                        {"id": item["id"], "status": item["status"]}
                        for item in verification["checks"]
                    ],
                    "candidate_hash": digest(snapshot),
                },
            )
            validate_result(review["result"], spec["criteria"], review=True)
            task, _, spec, config, initial, _ = load(root, identifier)
            unchanged(root, initial, config)
            if not review.get("session_id") or review["session_id"] == execution["session_id"]:
                raise WorkflowError("Reviewer session is not independently fresh.")
            if candidate(workspace, initial["files"], config) != snapshot:
                raise WorkflowError("Reviewer modified authoritative workspace files.")
            decision = review["result"]["decision"]
            state = "READY_FOR_APPLY" if decision == "PASS" else decision
            append_event(
                task,
                state,
                {"runtime": review, "candidate": snapshot, "candidate_hash": digest(snapshot)},
            )
        except (WorkflowError, OSError, ValueError, KeyError, TypeError) as error:
            append_event(task, "BLOCKED", {"error": redacted(str(error))[:4000]})
        return show(root, identifier)


def resume(root: Path, identifier: str, reason: str) -> dict:
    if not isinstance(reason, str) or not reason.strip() or len(reason) > 2000:
        raise WorkflowError("An explicit bounded retry reason is required.")
    with lock(root / ".forge" / "tasks" / (identifier + ".lock")):
        task, events, _, config, initial, attempt = load(root, identifier)
        if events[-1]["state"] in {"READY", "APPLIED", "APPLYING", "READY_FOR_APPLY"}:
            raise WorkflowError(
                "This state cannot restart; APPLYING requires explicit apply retry."
            )
        unchanged(root, initial, config)
        append_event(task, "READY", {"attempt": attempt + 1, "reason": reason})
    return show(root, identifier)


def validate_journal(root: Path, initial: dict, config: dict, operations: list[dict]) -> None:
    now = baseline(root, config)
    if any(now[key] != initial[key] for key in ("root", "head", "index")):
        raise WorkflowError("Repository identity/HEAD/index changed during apply.")
    operations_by_path = {item["path"]: item for item in operations}
    for name in now["files"].keys() | initial["files"].keys() | operations_by_path.keys():
        value = now["files"].get(name)
        if name in operations_by_path:
            operation = operations_by_path[name]
            if value not in {operation["old"], operation["new"]}:
                raise WorkflowError("Conflicting third-party edit during apply: " + name)
        elif value != initial["files"].get(name):
            raise WorkflowError("Unrelated original change during apply: " + name)


def apply(root: Path, identifier: str) -> dict:
    with (
        lock(root / ".forge" / "apply.lock"),
        lock(root / ".forge" / "tasks" / (identifier + ".lock")),
    ):
        task, events, spec, config, initial, _ = load(root, identifier)
        state = events[-1]["state"]
        if state == "APPLIED":
            return show(root, identifier)
        if state not in {"READY_FOR_APPLY", "APPLYING"}:
            raise WorkflowError("Task has no verified candidate ready for apply.")
        ready = next(event for event in reversed(events) if event["state"] == "READY_FOR_APPLY")
        snapshot = ready["payload"]["candidate"]
        workspace = safe_path(task, "workspace")
        if digest(snapshot) != ready["payload"]["candidate_hash"]:
            raise WorkflowError("Candidate evidence digest changed.")
        if candidate(workspace, initial["files"], config) != snapshot:
            raise WorkflowError("Verified workspace changed; apply refused.")
        check_scope(initial["files"], snapshot, spec, config)
        names = changes(initial["files"], snapshot)
        if state == "READY_FOR_APPLY":
            unchanged(root, initial, config)
            backups = safe_path(task, "backups")
            backups.mkdir(exist_ok=True)
            operations = []
            for index, name in enumerate(names):
                old = initial["files"].get(name)
                backup = f"backups/{index:08d}"
                if old is not None:
                    content = safe_path(root, name).read_bytes()
                    if hashlib.sha256(content).hexdigest() != old:
                        raise WorkflowError("Original changed while preparing apply.")
                    destination = safe_path(task, backup)
                    if destination.exists():
                        if destination.read_bytes() != content:
                            raise WorkflowError("Conflicting retained apply backup.")
                    else:
                        write_new(destination, content)
                operations.append(
                    {
                        "path": name,
                        "old": old,
                        "new": snapshot.get(name),
                        "backup": backup if old is not None else None,
                    }
                )
            append_event(
                task, "APPLYING", {"operations": operations, "candidate_hash": digest(snapshot)}
            )
        else:
            operations = events[-1]["payload"]["operations"]
        if [op["path"] for op in operations] != names:
            raise WorkflowError("Apply journal does not match candidate changes.")
        for operation in operations:
            name = operation["path"]
            if operation["old"] != initial["files"].get(name) or operation["new"] != snapshot.get(
                name
            ):
                raise WorkflowError("Apply journal digest mismatch.")
            if operation["old"] is not None:
                if file_hash(safe_path(task, operation["backup"])) != operation["old"]:
                    raise WorkflowError("Apply backup is absent or corrupt.")
        validate_journal(root, initial, config, operations)
        for index, operation in enumerate(operations):
            name = operation["path"]
            destination = safe_path(root, name)
            current = file_hash(destination)
            if current == operation["new"]:
                continue
            if current != operation["old"]:
                raise WorkflowError("Destination changed immediately before apply: " + name)
            if operation["new"] is None:
                destination.unlink()
            else:
                content = safe_path(workspace, name).read_bytes()
                if hashlib.sha256(content).hexdigest() != operation["new"]:
                    raise WorkflowError("Candidate changed during apply.")
                destination.parent.mkdir(parents=True, exist_ok=True)
                safe_path(root, name)
                # Publish complete bytes atomically, including no-overwrite creation.
                staging = safe_path(task, f"apply-{index:08d}-{uuid.uuid4().hex}.tmp")
                write_new(staging, content)
                safe_path(root, name)
                if file_hash(destination) != operation["old"]:
                    raise WorkflowError("Destination changed before atomic publication.")
                if current is None:
                    os.link(staging, destination)  # Atomic, fails if another writer created it.
                    staging.unlink()
                else:
                    os.replace(staging, destination)
            if file_hash(safe_path(root, name)) != operation["new"]:
                raise WorkflowError("Applied file verification failed.")
        validate_journal(root, initial, config, operations)
        if any(file_hash(safe_path(root, op["path"])) != op["new"] for op in operations):
            raise WorkflowError("Apply incomplete.")
        append_event(task, "APPLIED", {"candidate_hash": digest(snapshot), "changed_files": names})
    return show(root, identifier)
