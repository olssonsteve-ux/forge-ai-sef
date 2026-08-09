# ruff: noqa: E501
"""Create-only persistence, collection, and the two FAL-002 adapters."""
# fmt: off

from __future__ import annotations

import os
import re
import subprocess
import sys
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from forge.fal002_model import (
    CF,
    HB,
    FAL002Error,
    parse_cf,
    recovery_candidate_uuid,
    validate_record,
    validate_reviewer_run,
)

SECRET_PATTERN = re.compile(rb"(?i)(bearer\s+\S+|(?:token|password|secret|api[_-]?key)\s*[=:]\s*\S+)")
KINDS = {
    "fal002.gate-record.v1": "gate",
    "fal002.executor-exchange.v1": "executor",
    "fal002.run-record.v1": "runs",
    "fal002.reviewer-exchange.v1": "reviewer",
    "fal002.human-decision.v1": "decisions",
}
COMMANDS = {
    "GIT-ROOT": ("git", "rev-parse", "--show-toplevel"),
    "PYTHON-VERSION": (sys.executable, "--version"),
    "GIT-VERSION": ("git", "--version"),
    "PYTEST-VERSION": (sys.executable, "-m", "pytest", "--version"),
    "RUFF-VERSION": (sys.executable, "-m", "ruff", "--version"),
    "GIT-HEAD-BASELINE": ("git", "rev-parse", "HEAD"),
    "GIT-BRANCH": ("git", "branch", "--show-current"),
    "INVENTORY": (sys.executable, "-m", "forge.fal002", "inventory", "--output", "-"),
    "GIT-HEAD-FINAL": ("git", "rev-parse", "HEAD"),
    "GIT-STATUS": ("git", "status", "--porcelain=v1", "-z", "--untracked-files=all"),
    "GIT-DIFF": ("git", "diff", "--no-ext-diff", "--binary", "HEAD"),
    "GIT-NUMSTAT": ("git", "diff", "--numstat", "HEAD"),
    "SCHEMA-CHECK": (
        sys.executable,
        "-m",
        "forge.fal002",
        "schemas",
        "--output-root",
        "schemas/fal002",
        "--check",
    ),
    "PYTEST": (sys.executable, "-m", "pytest", "-q"),
    "RUFF-LINT": (sys.executable, "-m", "ruff", "check", "."),
    "RUFF-FORMAT": (sys.executable, "-m", "ruff", "format", "--check", "."),
    "FORGE-STATUS": (sys.executable, "-m", "forge", "status"),
}


class FAL002ExecutorAdapter:
    """The sole executable adapter for executor-authority callbacks."""

    def __init__(self, handler: Any) -> None:
        self._handler = handler

    def execute(self, exchange: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
        return self._handler(deepcopy(exchange), timeout_seconds=timeout_seconds)


class FAL002ReviewerAdapter:
    """The sole executable adapter for fresh, read-only reviewer callbacks."""

    def __init__(self, handler: Any) -> None:
        self._handler = handler

    def review(self, exchange: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
        return self._handler(deepcopy(exchange), timeout_seconds=timeout_seconds)


def canonical_record_path(root: Path, record: dict[str, Any]) -> Path:
    validate_record(record)
    series = record["series_id"]
    surface = record["schema_id"]
    folder = KINDS[surface]
    if surface == "fal002.gate-record.v1":
        filename = f"{record['sequence']:08d}.json"
    else:
        filename = f"{record['record_id']}.json"
    target = root / ".forge" / "fal002" / "series" / series / folder / filename
    _beneath(root, target)
    return target


def _beneath(root: Path, target: Path) -> None:
    resolved_root = root.resolve(strict=True)
    existing = target
    while not existing.exists():
        existing = existing.parent
    if existing.resolve(strict=True) != resolved_root:
        try:
            existing.resolve(strict=True).relative_to(resolved_root)
        except ValueError as exc:
            raise FAL002Error("AWAITING_HUMAN", "path escapes repository root") from exc


def publish_create_only(path: Path, record: dict[str, Any]) -> str:
    """Create canonical authoritative bytes; identical replay is idempotent."""
    validate_record(record)
    root = _repository_root_from_target(path)
    if path.resolve(strict=False) != canonical_record_path(root, record).resolve(strict=False):
        raise FAL002Error("AUTHORITY_CONFLICT", "noncanonical authoritative target")
    if record["schema_id"] == "fal002.reviewer-exchange.v1":
        run_path = root / ".forge" / "fal002" / "series" / record["series_id"] / "runs" / f"{record['run_id']}.json"
        validate_reviewer_run(record, load_record(run_path))
    if record["schema_id"] != "fal002.gate-record.v1" or record["payload"]["variant_kind"] != "RECOVERY_ROOT":
        _assert_series_unsealed(root, record["series_id"])
    raw = CF(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        if not path.is_file():
            raise FAL002Error("AUTHORITY_CONFLICT", f"nonregular target {path}") from None
        if path.read_bytes() != raw:
            raise FAL002Error("AUTHORITY_CONFLICT", f"different bytes at {path}") from None
        return "ADOPTED"
    observed = path.read_bytes()
    if observed != raw or HB(observed) != HB(raw):
        raise FAL002Error("HASH_MISMATCH", f"durability reread mismatch at {path}")
    return "CREATED"


def load_record(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FAL002Error("MISSING_EVIDENCE", str(path))
    value = parse_cf(path.read_bytes())
    return validate_record(value)


def load_gate_chain(root: Path, series_id: str) -> list[dict[str, Any]]:
    gate_root = root / ".forge" / "fal002" / "series" / series_id / "gate"
    if not gate_root.is_dir():
        raise FAL002Error("MISSING_EVIDENCE", "gate series absent")
    paths = sorted(gate_root.glob("*.json"))
    records = [load_record(path) for path in paths]
    previous = None
    for sequence, record in enumerate(records):
        if record["sequence"] != sequence or record["predecessor"] != previous:
            raise FAL002Error("HASH_MISMATCH", "gate chain discontinuity")
        if record["series_id"] != series_id:
            raise FAL002Error("AUTHORITY_CONFLICT", "gate series mismatch")
        previous = record["record_hash"]
    if not records:
        raise FAL002Error("MISSING_EVIDENCE", "empty gate series")
    return records


def write_current(root: Path, record: dict[str, Any]) -> None:
    """Replaceable exact GateRecord cache; never consulted as authority."""
    if record["schema_id"] != "fal002.gate-record.v1":
        raise FAL002Error("MALFORMED_BOUNDARY", "current cache requires GateRecord")
    target = root / ".forge" / "fal002" / "series" / record["series_id"] / "current.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name("current.json.tmp")
    raw = CF(record)
    with temporary.open("wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != raw:
        raise FAL002Error("HASH_MISMATCH", "current cache reread mismatch")
    os.replace(temporary, target)


def stage_committed_record(root: Path, predecessor_series_id: str, slot_id: str, record: dict[str, Any]) -> tuple[Path, int, str]:
    validate_record(record)
    raw = CF(record)
    stage_root = root / ".forge" / "fal002" / "series" / predecessor_series_id / ".staging" / slot_id
    for attempt in range(10_000):
        path = stage_root / f"attempt-{attempt:04d}.json.part"
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError:
            continue
        if path.read_bytes() != raw:
            raise FAL002Error("HASH_MISMATCH", "stage reread mismatch")
        return path, attempt, HB(raw)
    raise FAL002Error("AWAITING_HUMAN_EXTERNAL_REPAIR", "stage attempts exhausted")


def publish_staged(
    root: Path,
    staged_path: Path,
    intent_gate: dict[str, Any],
    target_record: dict[str, Any],
) -> str:
    """Publish committed bytes only through an authoritative PUBLICATION_INTENT."""
    validate_record(intent_gate)
    validate_record(target_record)
    if intent_gate["payload"]["variant_kind"] != "PUBLICATION_INTENT":
        raise FAL002Error("MISSING_EVIDENCE", "PUBLICATION_INTENT required")
    intent = intent_gate["payload"]["publication_intent"]
    slot = intent["slot"]
    expected_stage = root / intent["stage_locator"]
    if staged_path.resolve(strict=False) != expected_stage.resolve(strict=False):
        raise FAL002Error("AUTHORITY_CONFLICT", "staging locator mismatch")
    raw = staged_path.read_bytes()
    if HB(raw) != intent["intended_file_hash"] or HB(raw) != intent["stage_file_hash"]:
        raise FAL002Error("HASH_MISMATCH", "staged target mismatch")
    record = parse_cf(raw)
    if record != target_record or record["record_hash"] != intent["intended_record_hash"]:
        raise FAL002Error("HASH_MISMATCH", "intent record mismatch")
    if record["schema_id"] != slot["target_surface"] or record["record_id"] != slot["target_record_id"]:
        raise FAL002Error("AUTHORITY_CONFLICT", "publication identity mismatch")
    target = canonical_record_path(root, record)
    if target.relative_to(root).as_posix() != slot["target_path"]:
        raise FAL002Error("AUTHORITY_CONFLICT", "publication target mismatch")
    return publish_create_only(target, record)


def _repository_root_from_target(path: Path) -> Path:
    parts = path.resolve(strict=False).parts
    try:
        index = parts.index(".forge")
    except ValueError as exc:
        raise FAL002Error("AUTHORITY_CONFLICT", "target outside FAL-002 authority") from exc
    return Path(*parts[:index])


def _assert_series_unsealed(root: Path, series_id: str) -> None:
    series_root = root / ".forge" / "fal002" / "series"
    if not series_root.exists():
        return
    for candidate in series_root.glob("*/gate/00000000.json"):
        try:
            gate = load_record(candidate)
        except (FAL002Error, OSError):
            continue
        if (
            gate["payload"]["variant_kind"] == "RECOVERY_ROOT"
            and gate["payload"]["recovery_root"]["predecessor_series_id"] == series_id
        ):
            raise FAL002Error("STALE_RECORD", "predecessor physical series is sealed")


def discover_recovery_root(root: Path, discovery_key: str, *, max_ordinal: int = 9999) -> dict[str, Any] | None:
    """Probe deterministic candidates without enumerating the series directory."""
    for ordinal in range(max_ordinal + 1):
        candidate = recovery_candidate_uuid(discovery_key, ordinal)
        path = root / ".forge" / "fal002" / "series" / candidate / "gate" / "00000000.json"
        try:
            if not path.exists():
                return None
            record = load_record(path)
            recovery = record["payload"]["recovery_root"]
            if record["series_id"] == candidate and recovery["recovery_discovery_key"] == discovery_key and recovery["recovery_ordinal"] == ordinal:
                return record
        except FAL002Error:
            continue
        except OSError as exc:
            raise FAL002Error("AWAITING_HUMAN", "transient recovery authority uncertainty") from exc
    raise FAL002Error("AWAITING_HUMAN_EXTERNAL_REPAIR", "recovery candidates exhausted")


def invoke_executor(adapter: FAL002ExecutorAdapter, exchange: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    before = deepcopy(exchange)
    validate_record(exchange)
    output = adapter.execute(deepcopy(exchange), timeout_seconds=timeout_seconds)
    validate_record(output)
    for key in before:
        if key not in {"result", "invocation", "payload_hash", "record_hash"} and output[key] != before[key]:
            raise FAL002Error("AUTHORITY_CONFLICT", f"executor changed {key}")
    if output["invocation"]["grant"] != before["invocation"]["grant"]:
        raise FAL002Error("AUTHORITY_CONFLICT", "executor changed invocation grant")
    if output["result"] is None:
        raise FAL002Error("MISSING_EVIDENCE", "executor returned no result")
    return output


def invoke_reviewer(adapter: FAL002ReviewerAdapter, exchange: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    before = deepcopy(exchange)
    validate_record(exchange)
    output = adapter.review(deepcopy(exchange), timeout_seconds=timeout_seconds)
    validate_record(output)
    for key in before:
        if key not in {"result", "reviewer_execution", "payload_hash", "record_hash"} and output[key] != before[key]:
            raise FAL002Error("AUTHORITY_CONFLICT", f"reviewer changed {key}")
    if output["result"] is None:
        raise FAL002Error("MISSING_EVIDENCE", "reviewer returned no result")
    if output["reviewer_execution"]["grant"] != before["reviewer_execution"]["grant"]:
        raise FAL002Error("AUTHORITY_CONFLICT", "reviewer changed invocation grant")
    return output


def redact(raw: bytes) -> tuple[bytes, int]:
    count = 0

    def replacement(_: re.Match[bytes]) -> bytes:
        nonlocal count
        count += 1
        return b"[REDACTED]"

    return SECRET_PATTERN.sub(replacement, raw), count


def _timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _parsed(command_id: str, text: str, root: Path) -> dict[str, Any]:
    value = text.strip()
    try:
        if command_id == "GIT-ROOT":
            return {"available": True, "root": "."}
        if command_id == "PYTHON-VERSION":
            return {"available": True, "implementation": "CPython", "version": value.split()[-1]}
        if command_id in {"GIT-VERSION", "PYTEST-VERSION", "RUFF-VERSION"}:
            return {"available": True, "version": value.split()[-1]}
        if command_id in {"GIT-HEAD-BASELINE", "GIT-HEAD-FINAL"}:
            return {"available": True, "head": value, "kind": command_id.rsplit("-", 1)[-1]}
        if command_id == "GIT-BRANCH":
            return {"available": True, "branch": value}
        if command_id == "INVENTORY":
            data = __import__("json").loads(value)
            return {
                "available": True,
                "inventory_hash": HB(value.encode()),
                "disposition": data["disposition"],
                "counts": data["counts"],
            }
        if command_id == "GIT-STATUS":
            entries = []
            for item in text.rstrip("\0").split("\0") if text else []:
                entries.append({"xy": item[:2], "path": item[3:]})
            return {
                "available": True,
                "entries": entries,
                "changed_paths": sorted(item["path"] for item in entries),
            }
        if command_id == "GIT-DIFF":
            return {
                "available": True,
                "redacted_content_hash": HB(text.encode()),
                "byte_count": len(text.encode()),
            }
        if command_id == "GIT-NUMSTAT":
            entries = []
            for line in value.splitlines():
                added, deleted, path = line.split("\t", 2)
                entries.append(
                    {
                        "path": path,
                        "added": None if added == "-" else int(added),
                        "deleted": None if deleted == "-" else int(deleted),
                    }
                )
            return {"available": True, "entries": sorted(entries, key=lambda item: item["path"])}
        if command_id in {"RUFF-LINT", "RUFF-FORMAT"}:
            return {"available": True, "status": "PASS"}
    except (ValueError, KeyError, IndexError):
        pass
    return {"available": False, "failure_reason": f"parser unavailable for {command_id}"}


def run_command(root: Path, command_id: str, *, timeout_seconds: float = 30) -> dict[str, Any]:
    if command_id not in COMMANDS:
        raise FAL002Error("FORBIDDEN_OPERATION", f"command {command_id}")
    argv = COMMANDS[command_id]
    started_at = _timestamp()
    environment = {key: os.environ.get(key, "") for key in ("PATH", "SYSTEMROOT", "TEMP", "TMP")}
    environment.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    try:
        completed = subprocess.run(
            argv,
            cwd=root,
            env=environment,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            shell=False,
            timeout=timeout_seconds,
            check=False,
        )
        termination = "EXITED"
        exit_code = completed.returncode
        stdout, stdout_redactions = redact(completed.stdout)
        stderr, stderr_redactions = redact(completed.stderr)
    except subprocess.TimeoutExpired as exc:
        termination = "TIMEOUT"
        exit_code = None
        stdout, stdout_redactions = redact(exc.stdout or b"")
        stderr, stderr_redactions = redact(exc.stderr or b"")
    ended_at = _timestamp()
    stdout_text = stdout.decode("utf-8", "strict")
    parsed = _parsed(command_id, stdout_text, root) if termination == "EXITED" and exit_code == 0 else {"available": False, "failure_reason": "command did not pass"}
    phase = "preflight" if command_id in COMMANDS and list(COMMANDS).index(command_id) < 5 else "pre-execution" if list(COMMANDS).index(command_id) < 8 else "post-executor" if list(COMMANDS).index(command_id) < 12 else "verification"
    return {
        "command_id": command_id,
        "argv": list(argv),
        "cwd": ".",
        "environment_keys": sorted(environment),
        "phase": phase,
        "started_at": started_at,
        "ended_at": ended_at,
        "exit_code": exit_code,
        "termination": termination,
        "stdout_sha256": HB(stdout),
        "stderr_sha256": HB(stderr),
        "stdout_text": stdout_text,
        "stderr_text": stderr.decode("utf-8", "strict"),
        "redaction_count": stdout_redactions + stderr_redactions,
        "parser_version": 1,
        "parsed": parsed,
        "classification": "PASS" if termination == "EXITED" and exit_code == 0 else "BLOCKED",
    }
# fmt: on
