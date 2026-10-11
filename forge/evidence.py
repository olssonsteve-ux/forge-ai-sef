"""Bounded filesystem evidence and crash-releasing locks for the stable workflow."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

MAX_RECORD = 16 * 1024 * 1024
MAX_FILE = 256 * 1024 * 1024
MAX_TOTAL = 1024 * 1024 * 1024
MAX_FILES = 20000
PROTECTED = {".git", ".forge", ".codex", ".agents", ".aws", ".ssh"}
STATES = {
    "READY": {"EXECUTING"},
    "EXECUTING": {"EXECUTED", "BLOCKED", "READY"},
    "EXECUTED": {"VERIFYING", "BLOCKED", "READY"},
    "VERIFYING": {"VERIFIED", "BLOCKED", "READY"},
    "VERIFIED": {"REVIEWING", "BLOCKED", "READY"},
    "REVIEWING": {"READY_FOR_APPLY", "NEEDS_CHANGES", "BLOCKED", "READY"},
    "READY_FOR_APPLY": {"APPLYING"},
    "APPLYING": {"APPLIED"},
    "BLOCKED": {"READY"},
    "NEEDS_CHANGES": {"READY"},
    "APPLIED": set(),
}


class WorkflowError(Exception):
    """A bounded, user-visible refusal; never an implicit recovery instruction."""


def canonical(value: object) -> bytes:
    return (
        json.dumps(
            value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False
        )
        + "\n"
    ).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise WorkflowError("Duplicate JSON key.")
        result[key] = value
    return result


def parse_json(raw: bytes):
    if len(raw) > MAX_RECORD:
        raise WorkflowError("Record exceeds size limit.")
    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique_pairs,
            parse_constant=lambda _: (_ for _ in ()).throw(
                WorkflowError("Non-finite JSON number.")
            ),
        )
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise WorkflowError("Invalid JSON record.") from exc


def relative_path(value: str, *, dot: bool = False) -> str:
    if dot and value == ".":
        return value
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or any(c in value for c in ':*?<>|"')
    ):
        raise WorkflowError("Expected a portable relative path.")
    parts = value.split("/")
    if any(p in {"", ".", ".."} or p.endswith((" ", ".")) for p in parts):
        raise WorkflowError("Unsafe relative path.")
    if any(ord(c) < 32 for c in value):
        raise WorkflowError("Control character in path.")
    if any(
        p.split(".")[0].upper()
        in {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            *(f"COM{i}" for i in range(10)),
            *(f"LPT{i}" for i in range(10)),
        }
        for p in parts
    ):
        raise WorkflowError("Reserved device path.")
    return value


def safe_path(root: Path, relative: str = ".") -> Path:
    relative_path(relative, dot=True)
    root = root.absolute()
    target = root if relative == "." else root / relative
    # Check existing ancestors before resolve; junctions are not safe aliases.
    current = target
    while True:
        if current.exists() or current.is_symlink():
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise WorkflowError("Symlink/reparse paths are not allowed.")
        if current == current.parent:
            break
        current = current.parent
    if not target.resolve(strict=False).is_relative_to(root.resolve(strict=False)):
        raise WorkflowError("Path escapes the task root.")
    return target


def excluded(path: str, exclusions: list[str]) -> bool:
    parts = path.split("/")
    return any(
        p.lower() in PROTECTED or p.lower() == ".env" or p.lower().startswith(".env.")
        for p in parts
    ) or any(
        path.casefold() == item.casefold() or path.casefold().startswith(item.casefold() + "/")
        for item in exclusions
    )


def file_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    if not path.is_file() or path.stat().st_size > MAX_FILE:
        raise WorkflowError("Unsupported or oversized input file.")
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def hash_paths(root: Path, paths: list[str]) -> dict[str, str | None]:
    if len(paths) > MAX_FILES:
        raise WorkflowError("Snapshot file limit exceeded.")
    result = {}
    total = 0
    names = set()
    for name in sorted(set(paths)):
        relative_path(name)
        if name.casefold() in names:
            raise WorkflowError("Case-colliding snapshot paths.")
        names.add(name.casefold())
        path = safe_path(root, name)
        if path.exists():
            total += path.stat().st_size
        if total > MAX_TOTAL:
            raise WorkflowError("Snapshot byte limit exceeded.")
        result[name] = file_hash(path)
    return result


def write_new(path: Path, raw: bytes) -> None:
    safe_path(path.parent, path.name)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != raw:
        raise WorkflowError("Durability reread mismatch.")


@contextmanager
def lock(path: Path):
    safe_path(path.parent, path.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_path(path.parent, path.name)
    with path.open("a+b") as stream:
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise WorkflowError("Another Forge operation holds this lock.") from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def load_events(task: Path) -> list[dict]:
    directory = safe_path(task, "events")
    if not directory.is_dir():
        raise WorkflowError("Task event history is missing.")
    events = []
    for index, path in enumerate(sorted(directory.iterdir())):
        if path.name != f"{index:08d}.json":
            raise WorkflowError("Task event history has a gap or unknown file.")
        safe_path(directory, path.name)
        if path.stat().st_size > MAX_RECORD:
            raise WorkflowError("Record exceeds size limit.")
        raw = path.read_bytes()
        item = parse_json(raw)
        keys = {"version", "sequence", "previous", "state", "time", "payload", "hash"}
        if not isinstance(item, dict) or set(item) != keys:
            raise WorkflowError("Invalid event envelope.")
        unsigned = {k: v for k, v in item.items() if k != "hash"}
        if (
            canonical(item) != raw
            or type(item["version"]) is not int
            or item["version"] != 1
            or type(item["sequence"]) is not int
            or item["sequence"] != index
            or item["previous"] != (events[-1]["hash"] if events else None)
            or item["hash"] != digest(unsigned)
            or not isinstance(item["payload"], dict)
        ):
            raise WorkflowError("Task event integrity failure.")
        if not events:
            if item["state"] != "READY":
                raise WorkflowError("Task must begin READY.")
        elif item["state"] not in STATES.get(events[-1]["state"], set()):
            raise WorkflowError("Invalid task state transition.")
        if events and item["state"] == "READY" and not item["payload"].get("reason"):
            raise WorkflowError("Retry requires explicit reason.")
        events.append(item)
    if not events:
        raise WorkflowError("Empty task event history.")
    return events


def append_event(task: Path, state: str, payload: dict) -> dict:
    directory = task / "events"
    directory.mkdir(exist_ok=True)
    events = load_events(task) if any(directory.iterdir()) else []
    if (events and state not in STATES.get(events[-1]["state"], set())) or (
        not events and state != "READY"
    ):
        raise WorkflowError("Invalid task state transition.")
    item = {
        "version": 1,
        "sequence": len(events),
        "previous": events[-1]["hash"] if events else None,
        "state": state,
        "time": datetime.now(UTC).isoformat(),
        "payload": payload,
    }
    item["hash"] = digest(item)
    raw = canonical(item)
    if len(raw) > MAX_RECORD:
        raise WorkflowError("Record exceeds size limit.")
    write_new(directory / f"{len(events):08d}.json", raw)
    return item


def task_path(root: Path, identifier: str) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,47}", identifier):
        raise WorkflowError("Task ID must be 1â€“48 lowercase letters, digits or hyphens.")
    return safe_path(root, f".forge/tasks/{identifier}")
