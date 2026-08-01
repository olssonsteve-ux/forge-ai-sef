"""Bounded, deterministic Forge Adaptive Loop V1.

The module owns policy and evidence state. Executors and reviewers are adapters; neither can
accept a gate or mutate its frozen contract.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
import uuid
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
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
    "ready": {"executing", "blocked"},
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
)
SECRET_PATTERN = re.compile(
    r"(?i)(bearer\s+\S+|(?:token|password|secret|api[_-]?key)\s*[=:]\s*\S+)"
)


class ContractError(ValueError):
    """The manifest or a requested transition violates Forge policy."""


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


def redact(value: Any) -> Any:
    if isinstance(value, str):
        return SECRET_PATTERN.sub("[REDACTED]", value)
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    return value


def validate_manifest(manifest: dict[str, Any]) -> None:
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
    if risk.get("human_override") and not risk.get("override_rationale"):
        raise ContractError("human risk override requires rationale")


def validate_history(manifest: dict[str, Any]) -> None:
    history = manifest["history"]
    for index, event in enumerate(history):
        if event.get("sequence") != index + 1:
            raise ContractError("history sequence is not append-only")
        if index and event.get("from") != history[index - 1].get("to"):
            raise ContractError("history chain is broken")
        if event.get("to") not in TRANSITIONS.get(event.get("from"), set()):
            raise ContractError("history contains invalid transition")
    if history and history[-1]["to"] != manifest["state"]:
        raise ContractError("history does not reach current state")


def frozen_payload(manifest: dict[str, Any], prompt_hash: str | None = None) -> dict[str, Any]:
    payload = {field: manifest[field] for field in FROZEN_FIELDS}
    payload["prompt_hash"] = prompt_hash or manifest["run"].get("prompt_hash")
    return payload


def assert_frozen(manifest: dict[str, Any]) -> None:
    if sha256(frozen_payload(manifest)) != manifest["run"]["frozen_hash"]:
        raise ContractError("frozen contract changed")


def transition(manifest: dict[str, Any], target: str, actor: str, reason: str) -> dict[str, Any]:
    validate_manifest(manifest)
    source = manifest["state"]
    if target not in TRANSITIONS[source]:
        raise ContractError(f"invalid transition: {source} -> {target}")
    result = deepcopy(manifest)
    result["previous_state"] = source
    result["state"] = target
    result["history"].append(
        {
            "sequence": len(result["history"]) + 1,
            "from": source,
            "to": target,
            "actor": actor,
            "reason": reason,
            "at": utc_now(),
        }
    )
    validate_manifest(result)
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
    for path in changed_files:
        normalized = path.replace("\\", "/").lstrip("./")
        if not any(
            normalized == prefix[:-1] or normalized.startswith(prefix) for prefix in allowed
        ):
            raise ContractError(f"forbidden file changed: {path}")


def collect_command(command: list[str], cwd: Path, timeout: float = 60) -> dict[str, Any]:
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
    return redact(
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


def create_run_record(
    manifest: dict[str, Any], commands: list[dict[str, Any]], executor_result: dict[str, Any]
) -> dict[str, Any]:
    validate_changed_files(manifest, executor_result.get("changed_files", []))
    tests = executor_result.get("tests", "unknown")
    if isinstance(tests, dict) and tests.get("status") == "passed":
        if not any(
            c.get("exit_code") == 0 and "test" in " ".join(c["command"]).lower() for c in commands
        ):
            raise ContractError("green test claim lacks command evidence")
    record = redact(
        {
            "schema_version": "forge-run-record/1.0",
            "run_id": manifest["run"]["id"],
            "started_at": manifest["run"]["started_at"],
            "finished_at": utc_now(),
            "elapsed_seconds": "not available",
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
    return record


def reviewer_packet(
    manifest: dict[str, Any],
    run_record: dict[str, Any],
    diff: str,
    prior_findings: list[dict[str, Any]],
) -> dict[str, Any]:
    assert_frozen(manifest)
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
    }
    packet["packet_hash"] = sha256(packet)
    return packet


def validate_review(review: dict[str, Any], manifest: dict[str, Any]) -> None:
    if review.get("result") not in REVIEW_RESULTS:
        raise ContractError("invalid review result")
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
    if decision_type not in HUMAN_DECISIONS or len(options) < 2:
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
        del packet
        if not self.results:
            raise ContractError("fake reviewer exhausted")
        return deepcopy(self.results.pop(0))


def new_run_id() -> str:
    return str(uuid.uuid4())
