"""Create-only persistence, collection, and the two FAL-002 adapters."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Protocol

from forge.fal002_model import (
    CF,
    HB,
    FAL002Error,
    parse_cf,
    recovery_candidate_uuid,
    validate_record,
)

SECRET_PATTERN = re.compile(
    rb"(?i)(bearer\s+\S+|(?:token|password|secret|api[_-]?key)\s*[=:]\s*\S+)"
)
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
    "GIT-HEAD-FINAL": ("git", "rev-parse", "HEAD"),
    "GIT-STATUS": ("git", "status", "--porcelain=v1", "-z", "--untracked-files=all"),
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


class FAL002ExecutorAdapter(Protocol):
    def execute(self, exchange: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]: ...


class FAL002ReviewerAdapter(Protocol):
    def review(self, exchange: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]: ...


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


def stage_committed_record(
    root: Path, predecessor_series_id: str, slot_id: str, record: dict[str, Any]
) -> tuple[Path, int, str]:
    validate_record(record)
    raw = CF(record)
    stage_root = (
        root / ".forge" / "fal002" / "series" / predecessor_series_id / ".staging" / slot_id
    )
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


def publish_staged(path: Path, target: Path, intended_file_hash: str) -> str:
    raw = path.read_bytes()
    if HB(raw) != intended_file_hash:
        raise FAL002Error("HASH_MISMATCH", "staged target mismatch")
    record = parse_cf(raw)
    validate_record(record)
    return publish_create_only(target, record)


def discover_recovery_root(
    root: Path, discovery_key: str, *, max_ordinal: int = 9999
) -> dict[str, Any] | None:
    """Probe deterministic candidates without enumerating the series directory."""
    for ordinal in range(max_ordinal + 1):
        candidate = recovery_candidate_uuid(discovery_key, ordinal)
        path = root / ".forge" / "fal002" / "series" / candidate / "gate" / "00000000.json"
        if not path.exists():
            return None
        try:
            record = load_record(path)
            recovery = record["payload"]["recovery_root"]
            if (
                record["series_id"] == candidate
                and recovery["recovery_discovery_key"] == discovery_key
                and recovery["recovery_ordinal"] == ordinal
            ):
                return record
        except (FAL002Error, OSError):
            continue
    raise FAL002Error("AWAITING_HUMAN_EXTERNAL_REPAIR", "recovery candidates exhausted")


def invoke_executor(
    adapter: FAL002ExecutorAdapter, exchange: dict[str, Any], *, timeout_seconds: float
) -> dict[str, Any]:
    before = deepcopy(exchange)
    validate_record(exchange)
    output = adapter.execute(deepcopy(exchange), timeout_seconds=timeout_seconds)
    validate_record(output)
    for key in before:
        if key not in {"result", "payload_hash", "record_hash"} and output[key] != before[key]:
            raise FAL002Error("AUTHORITY_CONFLICT", f"executor changed {key}")
    if output["result"] is None:
        raise FAL002Error("MISSING_EVIDENCE", "executor returned no result")
    return output


def invoke_reviewer(
    adapter: FAL002ReviewerAdapter, exchange: dict[str, Any], *, timeout_seconds: float
) -> dict[str, Any]:
    before = deepcopy(exchange)
    validate_record(exchange)
    output = adapter.review(deepcopy(exchange), timeout_seconds=timeout_seconds)
    validate_record(output)
    for key in before:
        if (
            key not in {"result", "reviewer_execution", "payload_hash", "record_hash"}
            and output[key] != before[key]
        ):
            raise FAL002Error("AUTHORITY_CONFLICT", f"reviewer changed {key}")
    if output["result"] is None:
        raise FAL002Error("MISSING_EVIDENCE", "reviewer returned no result")
    return output


def redact(raw: bytes) -> tuple[bytes, int]:
    count = 0

    def replacement(_: re.Match[bytes]) -> bytes:
        nonlocal count
        count += 1
        return b"[REDACTED]"

    return SECRET_PATTERN.sub(replacement, raw), count


def run_command(root: Path, command_id: str, *, timeout_seconds: float = 30) -> dict[str, Any]:
    if command_id not in COMMANDS:
        raise FAL002Error("FORBIDDEN_OPERATION", f"command {command_id}")
    argv = COMMANDS[command_id]
    environment = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in {"PATH", "SYSTEMROOT", "TEMP", "TMP"}
    }
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
    return {
        "command_id": command_id,
        "argv": list(argv),
        "cwd": ".",
        "environment_keys": sorted(environment),
        "exit_code": exit_code,
        "termination": termination,
        "stdout_sha256": HB(stdout),
        "stderr_sha256": HB(stderr),
        "stdout_text": stdout.decode("utf-8", "strict"),
        "stderr_text": stderr.decode("utf-8", "strict"),
        "redaction_count": stdout_redactions + stderr_redactions,
        "classification": "PASS" if termination == "EXITED" and exit_code == 0 else "BLOCKED",
    }
