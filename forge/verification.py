"""Explicit, language-neutral verification; configuration is trusted operator policy."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import time
import tomllib
from pathlib import Path

from forge.evidence import WorkflowError, relative_path, safe_path

OUTPUT_LIMIT = 1024 * 1024
DEFAULT_ARTIFACTS = [
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "bin",
    "obj",
    "build",
    "dist",
    "node_modules",
    ".venv",
]
SECRET = re.compile(r"(?i)(bearer\s+\S+|(?:token|password|secret|api[_-]?key)\s*[=:]\s*\S+)")


def redacted(text: str) -> str:
    text = SECRET.sub("[REDACTED]", text)
    for key, value in os.environ.items():
        if any(word in key.upper() for word in ("TOKEN", "SECRET", "PASSWORD", "API_KEY")):
            if len(value) >= 8:
                text = text.replace(value, "[REDACTED]")
    return text


def validate_config(value: dict) -> dict:
    allowed = {"schema_version", "required_tools", "checks", "excluded_paths", "artifact_dirs"}
    if (
        not isinstance(value, dict)
        or set(value) - allowed
        or type(value.get("schema_version")) is not int
        or value.get("schema_version") != 1
    ):
        raise WorkflowError("Unsupported verification configuration.")
    result = dict(value)
    for key, default in (
        ("required_tools", []),
        ("excluded_paths", []),
        ("artifact_dirs", DEFAULT_ARTIFACTS),
    ):
        items = result.setdefault(key, list(default))
        if (
            not isinstance(items, list)
            or len(items) > 128
            or any(not isinstance(s, str) or not s for s in items)
            or len(set(items)) != len(items)
        ):
            raise WorkflowError(f"Invalid {key}.")
    for item in result["excluded_paths"]:
        relative_path(item)
    if any("/" in s or "\\" in s or s in {".", ".."} for s in result["artifact_dirs"]):
        raise WorkflowError("Artifact directories must be single directory names.")
    checks = result.get("checks")
    if not isinstance(checks, list) or not 1 <= len(checks) <= 32:
        raise WorkflowError("At least one and at most 32 checks are required.")
    ids = set()
    normalized = []
    for item in checks:
        if not isinstance(item, dict) or set(item) - {"id", "argv", "cwd", "timeout_seconds"}:
            raise WorkflowError("Unknown verification check field.")
        entry = dict(item)
        name = entry.get("id")
        if (
            not isinstance(name, str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", name)
            or name in ids
        ):
            raise WorkflowError("Invalid or duplicate check ID.")
        ids.add(name)
        argv = entry.get("argv")
        if (
            not isinstance(argv, list)
            or not 1 <= len(argv) <= 64
            or any(not isinstance(s, str) or not s or "\0" in s or len(s) > 8192 for s in argv)
        ):
            raise WorkflowError("Check argv must be a bounded string array.")
        entry.setdefault("cwd", ".")
        relative_path(entry["cwd"], dot=True)
        timeout = entry.setdefault("timeout_seconds", 300)
        if type(timeout) is not int or not 1 <= timeout <= 3600:
            raise WorkflowError("Check timeout must be 1â€“3600 seconds.")
        normalized.append(entry)
    result["checks"] = normalized
    return result


def load_config(root: Path, path: str = "forge.toml") -> dict:
    source = safe_path(root, relative_path(path))
    if not source.is_file() or source.stat().st_size > 128 * 1024:
        raise WorkflowError("Verification configuration is absent or oversized.")
    try:
        return validate_config(tomllib.loads(source.read_text(encoding="utf-8")))
    except (ValueError, UnicodeError) as exc:
        raise WorkflowError("Malformed verification TOML.") from exc


def preflight(root: Path, config: dict) -> list[str]:
    missing = [name for name in config["required_tools"] if shutil.which(name) is None]
    for check in config["checks"]:
        cwd = safe_path(root, check["cwd"])
        if not cwd.is_dir():
            missing.append(f"working directory for {check['id']}")
        program = check["argv"][0]
        if "/" in program or "\\" in program:
            relative_path(program)
            present = safe_path(cwd, program).is_file()
        else:
            present = shutil.which(program) is not None
        if not present:
            missing.append(f"executable for {check['id']}")
    return sorted(set(missing))


def run_process(
    argv: list[str], cwd: Path, timeout: int, *, stdin: str = "", env: dict | None = None
) -> dict:
    # Disk streams avoid a blocked pipe defeating timeout or child cleanup.
    from forge.process_guard import ProcessGuard

    started = time.monotonic()
    reason = "EXITED"
    code = None
    with (
        tempfile.TemporaryFile() as incoming,
        tempfile.TemporaryFile() as outgoing,
        tempfile.TemporaryFile() as errors,
    ):
        incoming.write(stdin.encode("utf-8"))
        incoming.seek(0)
        try:
            with ProcessGuard() as guard:
                process = subprocess.Popen(
                    argv,
                    cwd=cwd,
                    stdin=incoming,
                    stdout=outgoing,
                    stderr=errors,
                    shell=False,
                    creationflags=0x4 if os.name == "nt" else 0,  # CREATE_SUSPENDED
                    start_new_session=os.name != "nt",
                    env=env,
                )
                guard.attach(process)
                try:
                    while process.poll() is None:
                        if (
                            max(
                                os.fstat(outgoing.fileno()).st_size,
                                os.fstat(errors.fileno()).st_size,
                            )
                            > OUTPUT_LIMIT
                        ):
                            reason = "OUTPUT_LIMIT"
                            break
                        if time.monotonic() - started > timeout:
                            reason = "TIMEOUT"
                            break
                        time.sleep(0.03)
                except KeyboardInterrupt:
                    reason = "INTERRUPTED"
                finally:
                    guard.stop()
                    process.wait(timeout=10)
                code = process.returncode
        except (OSError, subprocess.SubprocessError):
            reason = "SPAWN_OR_CLEANUP_ERROR"
        outgoing.seek(0)
        errors.seek(0)
        raw = [stream.read(OUTPUT_LIMIT + 1) for stream in (outgoing, errors)]
    if any(len(value) > OUTPUT_LIMIT for value in raw):
        reason = "OUTPUT_LIMIT"
    return {
        "status": "PASS"
        if reason == "EXITED" and code == 0
        else "FAIL"
        if reason == "EXITED"
        else "BLOCKED",
        "reason": reason,
        "exit_code": code,
        "stdout": raw[0][:OUTPUT_LIMIT].decode("utf-8", "replace"),
        "stderr": raw[1][:OUTPUT_LIMIT].decode("utf-8", "replace"),
        "seconds": round(time.monotonic() - started, 3),
    }


def verify(root: Path, config: dict) -> dict:
    config = validate_config(config)
    missing = preflight(root, config)
    if missing:
        return {"status": "BLOCKED", "missing": missing, "checks": []}
    results = []
    for check in config["checks"]:
        result = run_process(
            check["argv"],
            safe_path(root, check["cwd"]),
            check["timeout_seconds"],
            env={**os.environ, "GIT_CEILING_DIRECTORIES": str(root.parent)},
        )
        result["stdout"] = redacted(result["stdout"])
        result["stderr"] = redacted(result["stderr"])
        results.append({"id": check["id"], **result})
        if result["status"] != "PASS":
            break
    status = (
        "PASS"
        if len(results) == len(config["checks"])
        and all(item["status"] == "PASS" for item in results)
        else results[-1]["status"]
    )
    return {"status": status, "checks": results, "missing": []}
