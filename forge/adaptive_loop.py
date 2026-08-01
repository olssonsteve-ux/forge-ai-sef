"""Bounded, deterministic Forge Adaptive Loop V1.

The module owns policy and evidence state. Executors and reviewers are adapters; neither can
accept a gate or mutate its frozen contract.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import subprocess
import time
import uuid
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Protocol

SCHEMA_VERSION = "forge-adaptive-loop/1.0"
FORGE_VERSION = "0.5.0"
PROMPT_VERSION = "forge-executor-prompt/1.0"
TEMPLATE_VERSION = "1.0"

STATES = {
    "draft",
    "awaiting_human",
    "ready",
    "executing",
    "evidence_ready",
    "reviewing",
    "correction_required",
    "blocked",
    "accepted",
    "closed",
}
TRANSITIONS = {
    "draft": {"awaiting_human", "ready", "blocked"},
    "awaiting_human": {"ready", "blocked"},
    "ready": {"executing", "awaiting_human", "blocked"},
    "executing": {"evidence_ready", "awaiting_human", "blocked"},
    "evidence_ready": {"reviewing", "blocked"},
    "reviewing": {"correction_required", "awaiting_human", "blocked", "accepted"},
    "correction_required": {"executing", "awaiting_human", "blocked"},
    "accepted": {"closed"},
    "blocked": set(),
    "closed": set(),
}
REVIEW_RESULTS = {"PASS", "CORRECTION_REQUIRED", "BLOCKED", "INCONCLUSIVE"}
HUMAN_DECISIONS = {
    "product_goal",
    "priority",
    "scope",
    "closure_criteria",
    "residual_risk",
    "architecture_lock_in",
    "release",
    "destructive_action",
    "external_action",
    "os_restart",
    "budget_exceeded",
}
FORBIDDEN_OPERATIONS = {
    "push",
    "tag",
    "merge",
    "release",
    "packaging",
    "distribution",
    "version_change",
    "history_rewrite",
    "destructive_git",
    "os_restart",
    "os_shutdown",
    "external_message",
    "credential_reuse",
}
FROZEN_FIELDS = (
    "capability_id",
    "gate",
    "gate_id",
    "scope",
    "non_goals",
    "criteria",
    "allowed_paths",
    "baseline_commit",
    "evidence_requirements",
    "max_corrections",
    "decision_owners",
    "forbidden_operations",
    "command_policy",
    "risk",
    "process_level",
    "reviewer_identity",
    "next_allowed_gate",
)
SECRET_PATTERN = re.compile(
    r"(?i)(bearer\s+\S+|(?:token|password|secret|api[_-]?key|aws_access_key_id)\s*[=:]\s*\S+)"
)
SECRET_KEYS = re.compile(r"(?i)(authorization|password|secret|token|api[_-]?key|aws_access_key_id)")
_COLLECTOR_KEY = uuid.uuid4().bytes
ACTOR_TARGETS = {
    "executor": {"executing", "evidence_ready", "awaiting_human", "blocked"},
    "collector": {"evidence_ready", "blocked"},
    "reviewer": {"correction_required", "awaiting_human", "blocked", "accepted"},
    "forge": STATES - {"closed", "accepted"},
    "human": {"ready", "blocked", "closed"},
}


class ContractError(ValueError):
    """The manifest or a requested transition violates Forge policy."""


class StateStore:
    """Append-only local snapshot ledger; current is a derived, recoverable cache."""

    def __init__(self, path: Path):
        self.path = path
        self.ledger = path.with_suffix(path.suffix + ".ledger")

    def initialize(self, manifest: dict[str, Any]) -> None:
        validate_manifest(manifest)
        if self.path.exists() or self.ledger.exists():
            raise ContractError("authoritative state already exists")
        self.ledger.mkdir(parents=True)
        self._append(manifest, None)
        self._write_cache(manifest, 0)

    def load(self) -> dict[str, Any]:
        records = self._records()
        state = records[-1]["payload"]
        if self.path.exists():
            cache = json.loads(self.path.read_text(encoding="utf-8"))
            if cache["sequence"] > records[-1]["sequence"]:
                raise ContractError("derived cache is ahead of authoritative ledger")
            if cache["sequence"] == records[-1]["sequence"] and cache["payload_hash"] != sha256(
                state
            ):
                raise ContractError("derived cache contradicts authoritative ledger")
        validate_manifest(state)
        return state

    def update(self, manifest: dict[str, Any], fail_after_append: bool = False) -> None:
        records = self._records()
        previous = records[-1]["payload"]
        validate_successor(previous, manifest)
        self._append(manifest, records[-1])
        if fail_after_append:
            raise OSError("injected persistence interruption after authoritative append")
        self._write_cache(manifest, records[-1]["sequence"] + 1)

    def _append(self, manifest: dict[str, Any], predecessor: dict[str, Any] | None) -> None:
        sequence = 0 if predecessor is None else predecessor["sequence"] + 1
        record = {
            "series_id": manifest["run"]["series_id"],
            "sequence": sequence,
            "predecessor": None if predecessor is None else predecessor["record_hash"],
            "payload_hash": sha256(manifest),
            "payload": manifest,
        }
        record["record_hash"] = sha256(record)
        target = self.ledger / f"{sequence:08d}.json"
        with target.open("x", encoding="utf-8") as stream:
            json.dump(record, stream, sort_keys=True, indent=2, ensure_ascii=False)
            stream.write("\n")

    def _records(self) -> list[dict[str, Any]]:
        paths = sorted(self.ledger.glob("*.json"))
        if not paths:
            raise ContractError("authoritative ledger is empty")
        records = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
        previous_hash = None
        for sequence, record in enumerate(records):
            unsigned = {key: value for key, value in record.items() if key != "record_hash"}
            if record.get("sequence") != sequence or record.get("predecessor") != previous_hash:
                raise ContractError("ledger sequence or predecessor mismatch")
            if record.get("payload_hash") != sha256(record.get("payload")):
                raise ContractError("ledger payload hash mismatch")
            if record.get("record_hash") != sha256(unsigned):
                raise ContractError("ledger record hash mismatch")
            if sequence and record.get("series_id") != records[0].get("series_id"):
                raise ContractError("ledger series identity mismatch")
            validate_manifest(record["payload"])
            previous_hash = record["record_hash"]
        return records

    def _write_cache(self, manifest: dict[str, Any], sequence: int) -> None:
        payload = {"sequence": sequence, "payload_hash": sha256(manifest)}
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)


class ExecutorAdapter(Protocol):
    def execute(self, prompt: str, packet: dict[str, Any]) -> dict[str, Any]: ...


class ReviewerAdapter(Protocol):
    def review(self, packet: dict[str, Any]) -> dict[str, Any]: ...


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(value: Any) -> str:
    data = value if isinstance(value, bytes) else canonical_bytes(value)
    return hashlib.sha256(data).hexdigest()


def validate_schema_boundary(value: Any, schema_name: str) -> None:
    """Execute the repository-owned closed JSON schema subset at runtime boundaries."""
    path = Path(__file__).parents[1] / "schemas" / schema_name
    schema = json.loads(path.read_text(encoding="utf-8"))

    def resolve(reference: str) -> dict[str, Any]:
        node: Any = schema
        for part in reference.removeprefix("#/").split("/"):
            node = node[part]
        return node

    def check(data: Any, rule: dict[str, Any], location: str) -> None:
        if "$ref" in rule:
            check(data, resolve(rule["$ref"]), location)
            return
        if "const" in rule and data != rule["const"]:
            raise ContractError(f"schema const mismatch at {location}")
        if "enum" in rule and data not in rule["enum"]:
            raise ContractError(f"schema enum mismatch at {location}")
        expected = rule.get("type")
        allowed = expected if isinstance(expected, list) else [expected] if expected else []
        type_map = {
            "object": dict,
            "array": list,
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "null": type(None),
        }
        if allowed and not any(isinstance(data, type_map[item]) for item in allowed):
            raise ContractError(f"schema type mismatch at {location}")
        if isinstance(data, dict):
            required = set(rule.get("required", []))
            if missing := required - data.keys():
                raise ContractError(
                    f"schema required fields missing at {location}: {sorted(missing)}"
                )
            properties = rule.get("properties", {})
            extra = set(data) - properties.keys()
            if rule.get("additionalProperties") is False and extra:
                raise ContractError(f"schema unknown fields at {location}: {sorted(extra)}")
            for key, item in data.items():
                if key in properties:
                    check(item, properties[key], f"{location}/{key}")
        if isinstance(data, list) and "items" in rule:
            for index, item in enumerate(data):
                check(item, rule["items"], f"{location}/{index}")
        if isinstance(data, int):
            if "minimum" in rule and data < rule["minimum"]:
                raise ContractError(f"schema minimum violated at {location}")
            if "maximum" in rule and data > rule["maximum"]:
                raise ContractError(f"schema maximum violated at {location}")
        if isinstance(data, str) and len(data) < rule.get("minLength", 0):
            raise ContractError(f"schema minLength violated at {location}")

    check(value, schema, "$")


def redact(value: Any) -> Any:
    if isinstance(value, str):
        return SECRET_PATTERN.sub("[REDACTED]", value)
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if SECRET_KEYS.search(str(key)) else redact(item)
            for key, item in value.items()
        }
    return value


def validate_manifest(manifest: dict[str, Any]) -> None:
    validate_schema_boundary(manifest, "forge-adaptive-loop-v1.schema.json")
    required = {
        "schema_version",
        "forge_version",
        "project",
        "repository",
        "capability_id",
        "gate",
        "gate_id",
        "capability_status",
        "process_level",
        "risk",
        "decision_owners",
        "scope",
        "non_goals",
        "criteria",
        "allowed_paths",
        "forbidden_operations",
        "evidence_requirements",
        "command_policy",
        "state",
        "previous_state",
        "history",
        "run",
        "baseline_commit",
        "correction_count",
        "max_corrections",
        "pending_decisions",
        "reviewer_identity",
        "next_allowed_gate",
    }
    missing = sorted(required - manifest.keys())
    if missing:
        raise ContractError(f"missing required fields: {', '.join(missing)}")
    if manifest["schema_version"] != SCHEMA_VERSION:
        raise ContractError("unsupported schema_version")
    if manifest["state"] not in STATES:
        raise ContractError("unknown state")
    if manifest["process_level"] not in {"lite", "standard", "high_assurance"}:
        raise ContractError("unknown process level")
    if manifest["capability_status"] not in {"authorized", "closed"}:
        raise ContractError("invalid capability status")
    if (manifest["capability_status"] == "closed") != (manifest["state"] == "closed"):
        raise ContractError("capability closure must match closed state")
    if (
        manifest["gate_id"] == "GATE-FAL-001"
        and manifest["next_allowed_gate"] != "human-acceptance"
    ):
        raise ContractError("unexpected next gate for Adaptive Loop V1")
    if manifest["run"].get("executor_identity") == manifest["reviewer_identity"]:
        raise ContractError("reviewer identity must be distinct from executor identity")
    if not 0 <= manifest["correction_count"] <= manifest["max_corrections"] <= 2:
        raise ContractError("invalid correction budget")
    if not manifest["criteria"] or any(
        not {"id", "text", "truth_authority", "risk"} <= criterion.keys()
        for criterion in manifest["criteria"]
    ):
        raise ContractError("criteria must include id, text, truth_authority and risk")
    ids = [criterion["id"] for criterion in manifest["criteria"]]
    if len(ids) != len(set(ids)):
        raise ContractError("criterion ids must be unique")
    if not set(manifest["forbidden_operations"]) >= FORBIDDEN_OPERATIONS:
        raise ContractError("mandatory forbidden operations are missing")
    validate_risk(manifest["risk"])
    for criterion in manifest["criteria"]:
        validate_risk(criterion["risk"])
    validate_history(manifest)
    if manifest["run"].get("frozen_hash"):
        assert_frozen(manifest)


def validate_risk(risk: dict[str, Any]) -> None:
    dimensions = {
        "consequence",
        "uncertainty",
        "irreversibility",
        "evidence_difficulty",
        "external_impact",
        "security_data_integrity",
    }
    if set(risk.get("dimensions", {})) != dimensions:
        raise ContractError("risk dimensions are incomplete")
    if any(not isinstance(v, int) or not 1 <= v <= 5 for v in risk["dimensions"].values()):
        raise ContractError("risk dimensions must be integers from 1 to 5")
    if risk.get("level") not in {"lite", "standard", "high_assurance"}:
        raise ContractError("invalid risk level")
    score = sum(risk["dimensions"].values()) / len(risk["dimensions"])
    derived = "high_assurance" if score >= 3.5 else "standard" if score >= 2 else "lite"
    if not risk.get("human_override") and risk.get("level") != derived:
        raise ContractError(f"risk level must match deterministic classification: {derived}")
    if risk.get("human_override") and not risk.get("override_rationale"):
        raise ContractError("human risk override requires rationale")


def validate_history(manifest: dict[str, Any]) -> None:
    history = manifest["history"]
    if manifest["state"] not in {"draft", "ready", "awaiting_human"} and not history:
        raise ContractError("non-initial state requires append-only history")
    previous_hash = "GENESIS"
    for index, event in enumerate(history):
        if event.get("sequence") != index + 1:
            raise ContractError("history sequence is not append-only")
        if index and event.get("from") != history[index - 1].get("to"):
            raise ContractError("history chain is broken")
        if event.get("to") not in TRANSITIONS.get(event.get("from"), set()):
            raise ContractError("history contains invalid transition")
        if event.get("previous_event_hash") != previous_hash:
            raise ContractError("history hash chain is broken")
        unsigned = {key: value for key, value in event.items() if key != "event_hash"}
        if event.get("event_hash") != sha256(unsigned):
            raise ContractError("history event hash is invalid")
        previous_hash = event["event_hash"]
    if history and history[-1]["to"] != manifest["state"]:
        raise ContractError("history does not reach current state")
    expected_head = history[-1]["event_hash"] if history else "GENESIS"
    if manifest["run"].get("history_head", "GENESIS") != expected_head:
        raise ContractError("history head does not match append-only ledger")


def validate_successor(previous: dict[str, Any], current: dict[str, Any]) -> None:
    """Validate a new authoritative record against its retained predecessor."""
    validate_manifest(previous)
    validate_manifest(current)
    if previous["run"]["series_id"] != current["run"]["series_id"]:
        raise ContractError("correction series identity changed")
    if current["correction_count"] < previous["correction_count"]:
        raise ContractError("correction budget cannot reset")
    prefix = current["history"][: len(previous["history"])]
    if prefix != previous["history"]:
        raise ContractError("append-only history was truncated or replaced")


def frozen_payload(manifest: dict[str, Any], prompt_hash: str | None = None) -> dict[str, Any]:
    payload = {field: manifest[field] for field in FROZEN_FIELDS}
    payload["prompt_hash"] = prompt_hash or manifest["run"].get("prompt_hash")
    payload["series_id"] = manifest["run"].get("series_id")
    return payload


def assert_frozen(manifest: dict[str, Any]) -> None:
    if sha256(frozen_payload(manifest)) != manifest["run"]["frozen_hash"]:
        raise ContractError("frozen contract changed")


def transition(manifest: dict[str, Any], target: str, actor: str, reason: str) -> dict[str, Any]:
    validate_manifest(manifest)
    source = manifest["state"]
    if target not in TRANSITIONS[source]:
        raise ContractError(f"invalid transition: {source} -> {target}")
    actor_role = actor.split(":", 1)[0]
    if target not in ACTOR_TARGETS.get(actor_role, set()):
        raise ContractError(f"actor {actor_role} cannot authorize state {target}")
    result = deepcopy(manifest)
    result["previous_state"] = source
    result["state"] = target
    event = {
        "sequence": len(result["history"]) + 1,
        "from": source,
        "to": target,
        "actor": actor,
        "reason": reason,
        "at": utc_now(),
        "previous_event_hash": result["history"][-1]["event_hash"]
        if result["history"]
        else "GENESIS",
    }
    event["event_hash"] = sha256(event)
    result["history"].append(event)
    result["run"]["history_head"] = event["event_hash"]
    validate_manifest(result)
    return result


def human_close(
    store: StateStore,
    decision: dict[str, Any],
    actor_role: str = "human",
    fail_after_append: bool = False,
) -> dict[str, Any]:
    """Atomically append an explicitly human-authorized closure snapshot."""
    validate_schema_boundary(decision, "forge-decision-record-v1.schema.json")
    required = {"decision_id", "decision", "owner", "provenance", "gate_id", "status"}
    if set(decision) != required or not required <= decision.keys():
        raise ContractError("malformed closure decision record")
    if actor_role != "human" or decision["decision"] != "AUTHORIZE_CLOSE":
        raise ContractError("closure requires explicit human authorization")
    if decision["status"] != "accepted" or not decision["provenance"]:
        raise ContractError("closure decision lacks accepted provenance")
    current = store.load()
    if current["state"] == "closed":
        raise ContractError("gate is already closed")
    if current["state"] != "accepted" or current["capability_status"] != "authorized":
        raise ContractError("gate is not technically eligible for closure")
    if decision["gate_id"] != current["gate_id"]:
        raise ContractError("closure decision targets another gate")
    if current["pending_decisions"]:
        raise ContractError("pending human decisions block closure")
    result = deepcopy(current)
    result["previous_state"] = "accepted"
    result["state"] = "closed"
    result["capability_status"] = "closed"
    event = {
        "sequence": len(result["history"]) + 1,
        "from": "accepted",
        "to": "closed",
        "actor": f"human:{decision['owner']}",
        "reason": f"closure authorized by {decision['decision_id']}",
        "at": utc_now(),
        "decision_id": decision["decision_id"],
        "decision_provenance": decision["provenance"],
        "previous_event_hash": result["history"][-1]["event_hash"],
    }
    event["event_hash"] = sha256(event)
    result["history"].append(event)
    result["run"]["history_head"] = event["event_hash"]
    validate_manifest(result)
    store.update(result, fail_after_append=fail_after_append)
    return result


def compile_prompt(manifest: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    validate_manifest(manifest)
    source = deepcopy(manifest)
    source["history"] = []
    source["previous_state"] = None
    source_hash = sha256(source)
    body = {
        "role": "bounded_executor",
        "capability_id": manifest["capability_id"],
        "gate_id": manifest["gate_id"],
        "scope": manifest["scope"],
        "non_goals": manifest["non_goals"],
        "criteria": manifest["criteria"],
        "allowed_paths": manifest["allowed_paths"],
        "forbidden_operations": manifest["forbidden_operations"],
        "evidence_plan": manifest["evidence_requirements"],
        "command_policy": manifest["command_policy"],
        "report_format": {"status": "string", "changed_files": "array", "claims": "array"},
        "correction_budget": {
            "used": manifest["correction_count"],
            "maximum": manifest["max_corrections"],
        },
        "policy": "Do not change frozen state, scope, criteria or policy. Do not accept the gate.",
    }
    prompt = json.dumps(body, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    metadata = {
        "prompt_version": PROMPT_VERSION,
        "source_state_hash": source_hash,
        "template_version": TEMPLATE_VERSION,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
        "created_at": "deterministic-from-run-start:" + manifest["run"]["started_at"],
        "executor_role": "bounded_executor",
    }
    return prompt, metadata


def begin_run(manifest: dict[str, Any], prompt_metadata: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(manifest)
    result["run"]["prompt_hash"] = prompt_metadata["prompt_hash"]
    result["run"]["source_state_hash"] = prompt_metadata["source_state_hash"]
    result["run"]["frozen_hash"] = sha256(frozen_payload(result, prompt_metadata["prompt_hash"]))
    validate_manifest(result)
    return result


def validate_changed_files(manifest: dict[str, Any], changed_files: list[str]) -> None:
    allowed = tuple(path.rstrip("/") + "/" for path in manifest["allowed_paths"])
    repository_root = Path(manifest["run"].get("working_directory", ".")).resolve()
    for path in changed_files:
        pure = PurePosixPath(path.replace("\\", "/"))
        if pure.is_absolute() or ".." in pure.parts:
            raise ContractError(f"forbidden file changed: {path}")
        normalized = pure.as_posix().removeprefix("./")
        candidate = (repository_root / Path(*pure.parts)).resolve()
        try:
            candidate.relative_to(repository_root)
        except ValueError as exc:
            raise ContractError(f"forbidden file changed: {path}") from exc
        if not any(
            normalized == prefix[:-1] or normalized.startswith(prefix) for prefix in allowed
        ):
            raise ContractError(f"forbidden file changed: {path}")


def collect_command(
    command: list[str],
    cwd: Path,
    timeout: float = 60,
    command_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if command_policy is not None:
        rendered = " ".join(command)
        if not any(
            rendered == item or rendered.startswith(item + " ")
            for item in command_policy.get("allow", [])
        ):
            raise ContractError(f"command is not allowed: {rendered}")
    forbidden_tokens = {"push", "tag", "merge", "release", "shutdown", "restart"}
    if any(token.lower() in forbidden_tokens for token in command):
        raise ContractError("command contains a forbidden operation")
    started = utc_now()
    monotonic_start = time.monotonic()
    try:
        completed = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False
        )
        status = "completed"
        exit_code: int | str = completed.returncode
        stdout, stderr = completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as exc:
        status, exit_code = "timeout", "not available"
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
    result = redact(
        {
            "command": command,
            "started_at": started,
            "finished_at": utc_now(),
            "elapsed_seconds": round(time.monotonic() - monotonic_start, 6),
            "status": status,
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "provenance": "subprocess.run",
        }
    )
    rendered = " ".join(command).lower()
    if "pytest" in rendered and "--version" not in rendered and "--help" not in rendered:
        match = re.search(r"(\d+) passed(?:, (\d+) skipped)?", result["stdout"])
        if result["exit_code"] == 0 and match:
            result["derived_tests"] = {
                "status": "passed",
                "passed": int(match.group(1)),
                "failed": 0,
                "skipped": int(match.group(2) or 0),
                "evidence": "command_record_hash",
            }
    result["command_record_hash"] = hmac.new(
        _COLLECTOR_KEY, canonical_bytes(result), hashlib.sha256
    ).hexdigest()
    return result


def create_run_record(
    manifest: dict[str, Any], commands: list[dict[str, Any]], executor_result: dict[str, Any]
) -> dict[str, Any]:
    validate_schema_boundary(executor_result, "forge-executor-result-v1.schema.json")
    validate_changed_files(manifest, executor_result.get("changed_files", []))
    tests = executor_result.get("tests", "unknown")
    if isinstance(tests, dict) and tests.get("status") == "passed":
        if not any(
            c.get("exit_code") == 0
            and "test" in " ".join(c["command"]).lower()
            and c.get("provenance") == "subprocess.run"
            and c.get("command_record_hash")
            == hmac.new(
                _COLLECTOR_KEY,
                canonical_bytes(
                    {key: value for key, value in c.items() if key != "command_record_hash"}
                ),
                hashlib.sha256,
            ).hexdigest()
            and c.get("derived_tests") == tests
            for c in commands
        ):
            raise ContractError("green test claim lacks command evidence")
    finished_at = utc_now()
    try:
        started_dt = datetime.fromisoformat(manifest["run"]["started_at"].replace("Z", "+00:00"))
        finished_dt = datetime.fromisoformat(finished_at.replace("Z", "+00:00"))
        elapsed: float | str = max(0.0, (finished_dt - started_dt).total_seconds())
    except (TypeError, ValueError):
        elapsed = "not available"
    record = redact(
        {
            "schema_version": "forge-run-record/1.0",
            "run_id": manifest["run"]["id"],
            "started_at": manifest["run"]["started_at"],
            "finished_at": finished_at,
            "elapsed_seconds": elapsed,
            "active_execution_seconds": sum(float(c.get("elapsed_seconds", 0)) for c in commands),
            "human_wait_seconds": "unknown",
            "repository": manifest["repository"],
            "working_directory": manifest["run"].get("working_directory", "unknown"),
            "branch": executor_result.get("branch", "unknown"),
            "baseline_head": manifest["baseline_commit"],
            "final_head": executor_result.get("final_head", "unknown"),
            "staging_status": executor_result.get("staging_status", "unknown"),
            "working_tree_status": executor_result.get("working_tree_status", "unknown"),
            "changed_files": executor_result.get("changed_files", []),
            "diff": executor_result.get("diff", {"status": "not available"}),
            "commands": commands,
            "runtime_versions": executor_result.get("runtime_versions", "not available"),
            "build": executor_result.get("build", "unknown"),
            "tests": tests,
            "warnings": executor_result.get("warnings", "unknown"),
            "errors": executor_result.get("errors", "unknown"),
            "skipped": executor_result.get("skipped", "unknown"),
            "raw_logs": executor_result.get("raw_logs", "not available"),
            "artifact_hashes": executor_result.get("artifact_hashes", {}),
            "review_results": [],
            "correction_count": manifest["correction_count"],
            "decisions": manifest["pending_decisions"],
            "escalations": [],
            "token_usage": executor_result.get("token_usage", "not available"),
            "api_usage": executor_result.get("api_usage", "not available"),
            "cost": executor_result.get("cost", "not available"),
            "provenance": {
                "git_fields": executor_result.get("git_provenance", "executor adapter"),
                "commands": "raw command result and exit code",
                "summary": "executor adapter",
            },
        }
    )
    record["record_hash"] = sha256(record)
    validate_schema_boundary(record, "forge-run-record-v1.schema.json")
    return record


def reviewer_packet(
    manifest: dict[str, Any],
    run_record: dict[str, Any],
    diff: str,
    prior_findings: list[dict[str, Any]],
) -> dict[str, Any]:
    assert_frozen(manifest)
    history_artifact = {
        "kind": "transition_history",
        "content": manifest["history"],
        "content_hash": sha256(manifest["history"]),
        "provenance": "authoritative-state-ledger",
    }
    run_artifact = {
        "kind": "run_record",
        "content": run_record,
        "content_hash": run_record["record_hash"],
        "provenance": "deterministic-evidence-collector",
    }
    started = manifest["run"]["started_at"]
    packet = {
        "schema_version": "forge-reviewer-packet/1.0",
        "mode": "read_only_adversarial",
        "criteria": manifest["criteria"],
        "baseline": manifest["baseline_commit"],
        "truth_authority": {c["id"]: c["truth_authority"] for c in manifest["criteria"]},
        "diff": diff,
        "changed_files": run_record["changed_files"],
        "run_record": run_record,
        "evidence_references": run_record.get("raw_logs", "not available"),
        "allowed_paths": manifest["allowed_paths"],
        "forbidden_operations": manifest["forbidden_operations"],
        "prior_findings": prior_findings,
        "reviewer_identity": manifest["reviewer_identity"],
        "artifacts": {"state-history": history_artifact, "run-record": run_artifact},
        "reviewer_execution": {
            "execution_id": f"REV-{manifest['run']['id']}",
            "adapter": "reviewer-adapter",
            "adapter_version": "1.0",
            "started_at": started,
            "finished_at": None,
            "repository": manifest["repository"],
            "baseline": manifest["baseline_commit"],
            "read_only": True,
            "source": "orchestrator",
        },
    }
    packet["packet_hash"] = sha256(packet)
    validate_schema_boundary(packet, "forge-reviewer-packet-v1.schema.json")
    return packet


def bind_review_packet(manifest: dict[str, Any], packet: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(manifest)
    result["run"]["review_packet_hash"] = packet["packet_hash"]
    result["run"]["review_record_hash"] = packet["run_record"]["record_hash"]
    result["run"]["review_artifacts"] = packet["artifacts"]
    result["run"]["reviewer_execution"] = packet["reviewer_execution"]
    return result


def resolve_evidence(reference: dict[str, Any], manifest: dict[str, Any]) -> Any:
    required = {
        "criterion_id",
        "evidence_kind",
        "artifact_id",
        "pointer",
        "assertion",
        "content_hash",
        "provenance",
    }
    if set(reference) != required or not reference["pointer"].startswith("/"):
        raise ContractError("malformed criterion evidence reference")
    artifact = manifest["run"].get("review_artifacts", {}).get(reference["artifact_id"])
    if not artifact or reference["content_hash"] != artifact["content_hash"]:
        raise ContractError("evidence artifact is missing or hash mismatched")
    if (
        reference["evidence_kind"] != artifact["kind"]
        or reference["provenance"] != artifact["provenance"]
    ):
        raise ContractError("evidence kind or provenance mismatch")
    value: Any = artifact
    for raw_part in reference["pointer"].lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        try:
            value = value[int(part)] if isinstance(value, list) else value[part]
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise ContractError("criterion evidence pointer cannot be resolved") from exc
    if value in (None, [], {}, "") or not reference["assertion"].strip():
        raise ContractError("criterion evidence is empty or has no assertion")
    return value


def validate_review(review: dict[str, Any], manifest: dict[str, Any]) -> None:
    validate_schema_boundary(review, "forge-review-result-v1.schema.json")
    unsigned_review = {key: value for key, value in review.items() if key != "review_result_hash"}
    if review.get("review_result_hash") != sha256(unsigned_review):
        raise ContractError("review result hash mismatch")
    if review.get("result") not in REVIEW_RESULTS:
        raise ContractError("invalid review result")
    if review.get("reviewer_identity") != manifest["reviewer_identity"]:
        raise ContractError("review identity does not match packet authority")
    if review.get("execution_identity") != manifest["run"].get("executor_identity"):
        raise ContractError("review execution identity is missing or incorrect")
    if review["reviewer_identity"] == review["execution_identity"]:
        raise ContractError("reviewer is not independent from executor")
    if review.get("packet_hash") != manifest["run"].get("review_packet_hash"):
        raise ContractError("review is not bound to the reviewer packet")
    criterion_ids = {c["id"] for c in manifest["criteria"]}
    for finding in review.get("findings", []):
        required = {
            "id",
            "criterion_id",
            "severity",
            "observation",
            "evidence_reference",
            "claim_status",
            "minimum_remediation",
            "human_decision_required",
        }
        if not required <= finding.keys() or finding["criterion_id"] not in criterion_ids:
            raise ContractError("invalid review finding")
    if review["result"] == "PASS":
        coverage = set(review.get("criterion_coverage", []))
        if coverage != criterion_ids:
            raise ContractError("PASS requires complete criterion-to-evidence coverage")
        evidence = review.get("criterion_evidence", {})
        if set(evidence) != criterion_ids or any(not refs for refs in evidence.values()):
            raise ContractError("PASS requires evidence references for every criterion")
        for criterion_id, references in evidence.items():
            for reference in references:
                if reference.get("criterion_id") != criterion_id:
                    raise ContractError("evidence reference belongs to another criterion")
                resolve_evidence(reference, manifest)
        provenance = review.get("reviewer_execution", {})
        expected_execution = manifest["run"].get("reviewer_execution", {})
        if (
            provenance.get("execution_id") != expected_execution.get("execution_id")
            or provenance.get("read_only") is not True
            or provenance.get("source") not in {"collector", "orchestrator"}
            or provenance.get("adapter") == "self-declared"
        ):
            raise ContractError("reviewer independence lacks orchestrator provenance")


def apply_review(manifest: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    validate_review(review, manifest)
    result = review["result"]
    if result == "PASS":
        return transition(manifest, "accepted", "reviewer", "technical eligibility established")
    if result in {"BLOCKED", "INCONCLUSIVE"}:
        return transition(manifest, "blocked", "reviewer", result.lower())
    if any(f["human_decision_required"] for f in review.get("findings", [])):
        return transition(manifest, "awaiting_human", "forge", "finding requires human decision")
    if manifest["correction_count"] >= manifest["max_corrections"]:
        return transition(manifest, "blocked", "forge", "correction budget exhausted")
    return transition(manifest, "correction_required", "reviewer", "bounded correction required")


def start_correction(
    manifest: dict[str, Any], finding_ids: list[str], previous_diff_hash: str, new_diff_hash: str
) -> dict[str, Any]:
    assert_frozen(manifest)
    if manifest["state"] != "correction_required":
        raise ContractError("correction is not authorized in current state")
    if manifest["correction_count"] >= manifest["max_corrections"]:
        return transition(manifest, "blocked", "forge", "correction budget exhausted")
    result = deepcopy(manifest)
    if previous_diff_hash == new_diff_hash:
        return transition(result, "blocked", "forge", "no progress: diff hash unchanged")
    previous = result["run"].get("last_finding_ids", [])
    if previous == finding_ids and result["run"].get("last_diff_hash") == new_diff_hash:
        return transition(result, "blocked", "forge", "same finding without material progress")
    result["correction_count"] += 1
    result["run"]["last_finding_ids"] = finding_ids
    result["run"]["last_diff_hash"] = new_diff_hash
    # Correction count is mutable control state and deliberately excluded from the frozen payload.
    return transition(result, "executing", "forge", "bounded correction started")


def decision_card(
    decision_id: str,
    question: str,
    decision_type: str,
    owner: str,
    options: list[dict[str, str]],
    recommendation: str,
    blocked: str,
    needed_by: str,
) -> dict[str, Any]:
    option_ids = {option.get("id") for option in options}
    if (
        decision_type not in HUMAN_DECISIONS
        or len(options) < 2
        or recommendation not in option_ids
        or any(not {"id", "consequence", "reversibility"} <= option.keys() for option in options)
        or not owner.strip()
    ):
        raise ContractError("decision card requires a human-owned type and realistic alternatives")
    return {
        "decision_id": decision_id,
        "question": question,
        "why_needed": decision_type,
        "decision_owner": owner,
        "options": options,
        "recommendation": recommendation,
        "reversibility": {option["id"]: option["reversibility"] for option in options},
        "blocked_work": blocked,
        "needed_by": needed_by,
        "status": "pending",
    }


def request_human_decision(manifest: dict[str, Any], card: dict[str, Any]) -> dict[str, Any]:
    """Atomically persist a pending card and move an active run to awaiting human."""
    if card.get("status") != "pending":
        raise ContractError("only pending decision cards may be requested")
    result = deepcopy(manifest)
    result["pending_decisions"].append(card)
    return transition(
        result, "awaiting_human", "forge", f"decision required: {card['decision_id']}"
    )


def resolve_human_decision(
    manifest: dict[str, Any], decision_id: str, selected_option: str, actor: str = "human"
) -> dict[str, Any]:
    result = deepcopy(manifest)
    cards = [card for card in result["pending_decisions"] if card["decision_id"] == decision_id]
    if len(cards) != 1 or selected_option not in {o["id"] for o in cards[0]["options"]}:
        raise ContractError("invalid human decision resolution")
    cards[0]["status"] = "resolved"
    cards[0]["selected_option"] = selected_option
    return transition(result, "ready", actor, f"decision resolved: {decision_id}")


@dataclass
class FakeExecutor:
    result: dict[str, Any]

    def execute(self, prompt: str, packet: dict[str, Any]) -> dict[str, Any]:
        del prompt, packet
        return deepcopy(self.result)


@dataclass
class FakeReviewer:
    results: list[dict[str, Any]]

    def review(self, packet: dict[str, Any]) -> dict[str, Any]:
        if not self.results:
            raise ContractError("fake reviewer exhausted")
        result = deepcopy(self.results.pop(0))
        result["packet_hash"] = packet["packet_hash"]
        result["reviewer_execution"] = deepcopy(packet["reviewer_execution"])
        result["reviewer_execution"]["finished_at"] = utc_now()
        if result["result"] == "PASS":
            result["criterion_evidence"] = {}
            for criterion in result["criterion_coverage"]:
                artifact_id = "state-history" if criterion == "FAL-01" else "run-record"
                artifact = packet["artifacts"][artifact_id]
                pointer = "/content" if criterion == "FAL-01" else "/content/provenance/commands"
                result["criterion_evidence"][criterion] = [
                    {
                        "criterion_id": criterion,
                        "evidence_kind": artifact["kind"],
                        "artifact_id": artifact_id,
                        "pointer": pointer,
                        "assertion": "Resolved evidence satisfies the criterion truth authority.",
                        "content_hash": artifact["content_hash"],
                        "provenance": artifact["provenance"],
                    }
                ]
        result["review_result_hash"] = sha256(
            {key: value for key, value in result.items() if key != "review_result_hash"}
        )
        return result


def run_controlled_fixture(
    manifest: dict[str, Any],
    executor: ExecutorAdapter,
    reviewer: ReviewerAdapter,
    cwd: Path,
) -> dict[str, Any]:
    """Run the bounded fake-adapter journey used by the executable V1 demonstration."""
    prompt, metadata = compile_prompt(manifest)
    store = StateStore(cwd / "forge-adaptive-loop-state.json")
    store.initialize(manifest)
    state = begin_run(manifest, metadata)
    store.update(state)
    records: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    prior_diff_hash = manifest["baseline_commit"]
    prior_findings: list[dict[str, Any]] = []
    while True:
        if state["state"] == "ready":
            state = transition(state, "executing", "executor", "fixture execution")
            store.update(state)
        execution = executor.execute(prompt, {"manifest_hash": state["run"]["frozen_hash"]})
        command = collect_command(
            ["python", "-m", "pytest", str(ROOT_FIXTURE), "-q"],
            cwd,
            command_policy=state["command_policy"],
        )
        execution["tests"] = command.get("derived_tests", "unknown")
        record = create_run_record(state, [command], execution)
        records.append(record)
        state = transition(state, "evidence_ready", "collector", "run record sealed")
        store.update(state)
        state = transition(state, "reviewing", "forge", "review packet sealed")
        store.update(state)
        packet = reviewer_packet(
            state, record, execution.get("diff", {}).get("text", ""), prior_findings
        )
        state = bind_review_packet(state, packet)
        store.update(state)
        review_result = reviewer.review(packet)
        reviews.append(review_result)
        state = apply_review(state, review_result)
        store.update(state)
        if state["state"] != "correction_required":
            break
        new_diff_hash = sha256(execution.get("diff", {}))
        state = start_correction(
            state,
            [item["id"] for item in review_result.get("findings", [])],
            prior_diff_hash,
            new_diff_hash,
        )
        store.update(state)
        prior_diff_hash = new_diff_hash
        prior_findings.extend(review_result.get("findings", []))
        if state["state"] == "blocked":
            break
    return {"state": state, "records": records, "reviews": reviews, "prompt": metadata}


def new_run_id() -> str:
    return str(uuid.uuid4())


ROOT_FIXTURE = Path(__file__).parents[1] / "fixtures" / "adaptive-loop-v1" / "demo_check.py"
