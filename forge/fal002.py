# ruff: noqa: E501
"""Sequential FAL-002 Standard-Assurance bounded engineering loop."""
# fmt: off

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from forge.fal002_inventory import enforce_limits, inventory
from forge.fal002_io import (
    FAL002ExecutorAdapter,
    FAL002ReviewerAdapter,
    canonical_record_path,
    load_record,
    publish_create_only,
    publish_staged,
    run_command,
    stage_committed_record,
    write_current,
)
from forge.fal002_model import (
    COMMAND_IDS,
    HB,
    FAL002Error,
    H,
    decision_application,
    empty_finding_checkpoint,
    fold_finding_events,
    generate_schemas,
    pass_eligible,
    progress_snapshot,
    publication_slot,
    seal_record,
    validate_record,
    validate_reviewer_run,
)

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
TRANSITIONS = {
    (None, "INITIALIZE"): "draft",
    ("draft", "MARK_READY"): "ready",
    ("draft", "ESCALATE"): "awaiting_human",
    ("ready", "START_EXECUTION"): "executing",
    ("executing", "COLLECT_COMPLETE"): "evidence_ready",
    ("evidence_ready", "START_REVIEW"): "reviewing",
    ("reviewing", "REVIEW_PASS"): "accepted",
    ("reviewing", "REVIEW_CORRECTION"): "correction_required",
    ("reviewing", "REVIEW_BLOCKED"): "blocked",
    ("correction_required", "START_CORRECTION"): "executing",
    ("correction_required", "NO_PROGRESS"): "blocked",
    ("correction_required", "CEILING_REACHED"): "awaiting_human",
    ("accepted", "HUMAN_CLOSE"): "closed",
}
EVENT_ACTORS = {
    "INITIALIZE": "human",
    "MARK_READY": "core",
    "ESCALATE": "core",
    "START_EXECUTION": "core",
    "START_CORRECTION": "core",
    "COLLECT_COMPLETE": "collector",
    "START_REVIEW": "core",
    "REVIEW_PASS": "reviewer",
    "REVIEW_CORRECTION": "reviewer",
    "REVIEW_BLOCKED": "reviewer",
    "NO_PROGRESS": "core",
    "CEILING_REACHED": "core",
    "HUMAN_CLOSE": "human",
    "PUBLICATION_INTENT_COMMITTED": "core",
    "RECOVERY_SUCCESSOR": "recovery",
}


def make_gate(
    *,
    series_id: str,
    sequence: int,
    predecessor: str | None,
    state: str,
    actor: str,
    event: str,
    created_at: str,
    frozen_hash: str,
    correction_count: int,
    variant_kind: str,
    variant: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "frozen_hash": frozen_hash,
        "correction_count": correction_count,
        "variant_kind": variant_kind,
        variant_kind.lower(): variant,
    }
    return seal_record(
        {
            "schema_id": "fal002.gate-record.v1",
            "schema_version": 1,
            "record_id": f"gate-{sequence:08d}",
            "series_id": series_id,
            "sequence": sequence,
            "predecessor": predecessor,
            "state": state,
            "actor": actor,
            "event": event,
            "created_at": created_at,
            "payload": payload,
        }
    )


def transition(
    previous: dict[str, Any] | None,
    *,
    event: str,
    created_at: str,
    variant_kind: str,
    variant: dict[str, Any],
    series_id: str | None = None,
    frozen_hash: str | None = None,
) -> dict[str, Any]:
    previous_state = None if previous is None else previous["state"]
    if event == "PUBLICATION_INTENT_COMMITTED":
        if previous is None:
            raise FAL002Error("FORBIDDEN_TRANSITION", "intent needs predecessor")
        next_state = previous_state
    elif event == "RECOVERY_SUCCESSOR":
        next_state = "awaiting_human"
    else:
        try:
            next_state = TRANSITIONS[(previous_state, event)]
        except KeyError as exc:
            raise FAL002Error("FORBIDDEN_TRANSITION", f"{previous_state} + {event}") from exc
    if previous is None:
        if series_id is None or frozen_hash is None:
            raise FAL002Error("MALFORMED_BOUNDARY", "origin identity required")
        sequence, predecessor, corrections = 0, None, 0
    elif event == "RECOVERY_SUCCESSOR":
        sequence, predecessor, corrections = 0, None, previous["payload"]["correction_count"]
        series_id = variant["successor_series_id"]
        frozen_hash = previous["payload"]["frozen_hash"]
    else:
        sequence, predecessor = previous["sequence"] + 1, previous["record_hash"]
        corrections = previous["payload"]["correction_count"]
        series_id, frozen_hash = previous["series_id"], previous["payload"]["frozen_hash"]
        if event == "START_CORRECTION":
            if corrections >= 2:
                raise FAL002Error("CORRECTION_CEILING", "two corrections consumed")
            corrections += 1
    return make_gate(
        series_id=series_id,
        sequence=sequence,
        predecessor=predecessor,
        state=next_state,
        actor=EVENT_ACTORS[event],
        event=event,
        created_at=created_at,
        frozen_hash=frozen_hash,
        correction_count=corrections,
        variant_kind=variant_kind,
        variant=variant,
    )


def persist_transition(root: Path, gate: dict[str, Any]) -> str:
    status = publish_create_only(canonical_record_path(root, gate), gate)
    write_current(root, gate)
    return status


def publish_committed(
    root: Path,
    predecessor: dict[str, Any],
    record: dict[str, Any],
    *,
    created_at: str,
    source_authority: str,
    source_record: dict[str, Any],
) -> dict[str, Any]:
    """Stage and final-publish one COMMITTED record through its authoritative intent."""
    target_path = canonical_record_path(root, record).relative_to(root).as_posix()
    origin = predecessor["payload"].get("recovery_root", {}).get("origin_series_id", predecessor["series_id"])
    slot = publication_slot(
        {
            "origin_series_id": origin,
            "predecessor_series_id": predecessor["series_id"],
            "predecessor_gate_id": predecessor["record_id"],
            "predecessor_gate_hash": predecessor["record_hash"],
            "target_surface": record["schema_id"],
            "target_record_id": record["record_id"],
            "target_path": target_path,
            "reconstruction": "COMMITTED",
        }
    )
    staged, attempt, file_hash = stage_committed_record(root, predecessor["series_id"], slot["slot_id"], record)
    intent = {
        "slot": slot,
        "retained_state": predecessor["state"],
        "intended_record_hash": record["record_hash"],
        "intended_file_hash": file_hash,
        "stage_locator": staged.relative_to(root).as_posix(),
        "stage_attempt": attempt,
        "stage_file_hash": file_hash,
        "source_authority": source_authority,
        "source_record_id": source_record["record_id"],
        "source_record_hash": source_record["record_hash"],
    }
    intent["intent_commitment_hash"] = H("fal002-publication-intent-v1", intent)
    intent_gate = transition(
        predecessor,
        event="PUBLICATION_INTENT_COMMITTED",
        created_at=created_at,
        variant_kind="PUBLICATION_INTENT",
        variant=intent,
    )
    persist_transition(root, intent_gate)
    publish_staged(root, staged, intent_gate, record)
    return intent_gate


def reconstruct_findings(
    gates: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    events: list[dict[str, Any]] = []
    expected_checkpoint = empty_finding_checkpoint()
    for gate in gates:
        variant = gate["payload"]["variant_kind"]
        value = gate["payload"][variant.lower()]
        if variant == "MANIFEST":
            expected_checkpoint = value["finding_checkpoint"]
            if expected_checkpoint != empty_finding_checkpoint():
                raise FAL002Error("HASH_MISMATCH", "origin checkpoint must be empty")
        elif variant == "CONTROL":
            events.extend(value["finding_events"])
            _, computed = fold_finding_events(events)
            if value["finding_checkpoint"] != computed:
                raise FAL002Error("HASH_MISMATCH", "CONTROL finding checkpoint mismatch")
            expected_checkpoint = computed
        elif variant == "RECOVERY_ROOT":
            if value["finding_checkpoint"] != expected_checkpoint:
                raise FAL002Error("HASH_MISMATCH", "recovery finding checkpoint mismatch")
    return fold_finding_events(events)


def reconstruct_decisions(gates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    requirements: list[dict[str, Any]] = []
    bindings: list[dict[str, Any]] = []
    applications: list[dict[str, Any]] = []
    for gate in gates:
        variant = gate["payload"]["variant_kind"]
        value = gate["payload"][variant.lower()]
        if variant in {"MANIFEST", "CONTROL"}:
            requirements = value["decision_requirements"]
            bindings = value["decision_bindings"]
            applications = value["decision_applications"]
        elif variant == "RECOVERY_ROOT":
            requirements = value["pending_decisions"]
            bindings = value["active_decision_bindings"]
            applications = value["applied_decisions"]
    return requirements, bindings, applications


def decisions_pending(root: Path, gates: list[dict[str, Any]]) -> tuple[bool, tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]]:
    authority = reconstruct_decisions(gates)
    requirements, bindings, applications = authority
    pending = False
    for requirement in requirements:
        status, _ = resolve_decision(
            requirement["decision_identity"],
            requirements,
            bindings,
            applications,
            lambda locator: load_record(root / locator),
        )
        pending = pending or status != "ACCEPTED"
    return pending, authority


def evaluate_review(
    review: dict[str, Any],
    current_findings: list[dict[str, Any]],
    *,
    pending_decisions: bool,
    evidence_loader: Callable[[str, str], dict[str, Any]] | None = None,
) -> bool:
    validate_record(review)
    result = review["result"]
    if result is None or result["outcome"] != "PASS":
        return False
    criterion_ids = review["packet"]["criterion_ids"]
    bound: set[str] = set()
    if evidence_loader is not None:
        from forge.fal002_model import validate_evidence_binding

        for binding in result["criterion_evidence"]:
            source = evidence_loader(binding["source_surface"], binding["source_record_id"])
            validate_evidence_binding(binding, source)
            bound.add(binding["criterion_id"])
    rationales = {item["criterion_id"] for item in result["semantic_rationale"] if item.get("rationale")}
    criteria_complete = set(criterion_ids) <= bound and set(criterion_ids) <= rationales
    return pass_eligible(current_findings, pending_decisions=pending_decisions, criteria_complete=criteria_complete)


def correction_disposition(
    previous_snapshot: dict[str, Any] | None,
    current_snapshot: dict[str, Any],
    previous_findings: list[dict[str, Any]],
    current_findings: list[dict[str, Any]],
    correction_count: int,
) -> str:
    if previous_snapshot is None:
        return "MATERIAL"
    if correction_count >= 2:
        return "CEILING"
    previous_unresolved = {(item["finding_id"], item["occurrence"]): item for item in previous_findings if item["state"] in {"OPEN", "ADDRESSED_AWAITING_REVIEW"}}
    current_by_key = {(item["finding_id"], item["occurrence"]): item for item in current_findings}
    resolved_any = any(current_by_key.get(key, {}).get("state") in {"INDEPENDENTLY_VERIFIED", "CLOSED", "SUPERSEDED"} for key in previous_unresolved)
    changed = previous_snapshot["diff_hash"] != current_snapshot["diff_hash"] or previous_snapshot["progress_evidence_hash"] != current_snapshot["progress_evidence_hash"]
    introduced = any(key not in previous_unresolved and item["state"] in {"OPEN", "ADDRESSED_AWAITING_REVIEW"} and (item["current_blocking"] or item["current_severity"] == "CRITICAL") for key, item in current_by_key.items())
    return "MATERIAL" if changed and resolved_any and not introduced else "NONE"


def _grant(
    role: str,
    principal: str,
    adapter: str,
    context: str,
    record_id: str,
    input_hash: str,
    created_at: str,
    prior: str | None = None,
) -> dict[str, Any]:
    value = {
        "role": role,
        "principal_id": principal,
        "adapter_id": adapter,
        "context_id": context,
        "input_record_id": record_id,
        "input_hash": input_hash,
        "issued_by": "FORGE_CORE",
        "issued_at": created_at,
        "allowed_effect": "RETURN_REVIEW_RESULT" if role == "REVIEWER" else "RETURN_EXECUTOR_RESULT",
    }
    if prior is not None:
        value["prior_context_id"] = prior
    value["grant_id"] = H("fal002-invocation-grant-v1", value)
    return value


def _tool(name: str, command_id: str, version: str) -> dict[str, Any]:
    executable = sys.executable if name in {"python", "pytest", "ruff"} else shutil.which("git")
    if not executable:
        raise FAL002Error("MISSING_EVIDENCE", f"{name} executable unavailable")
    path = Path(executable).resolve(strict=True)
    return {
        "name": name,
        "version": version,
        "executable": path.as_posix(),
        "executable_sha256": HB(path.read_bytes()),
        "version_command_id": command_id,
    }


def _finding_events(review: dict[str, Any], existing_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    current, checkpoint = fold_finding_events(existing_events)
    by_id = {item["finding_id"]: item for item in current}
    created: list[dict[str, Any]] = []
    for finding in review["result"]["findings"]:
        prior = by_id.get(finding["finding_id"])
        terminal = prior and prior["state"] in {"CLOSED", "SUPERSEDED"}
        occurrence = prior["occurrence"] + 1 if terminal else prior["occurrence"] if prior else 0
        payload = {
            "observation": "NEW" if not prior or terminal else "STILL_PRESENT",
            "observed_severity": finding["severity"],
            "observed_blocking": finding["blocking"],
            "statement": finding["statement"],
            "criterion_ids": finding["criterion_ids"],
            "evidence_bindings": review["result"]["criterion_evidence"],
            "rationale": "Independent reviewer observation.",
        }
        if terminal:
            payload["recurs_after_event_hash"] = prior["last_event_hash"]
        event = {
            "event_ordinal": checkpoint["event_count"] + len(created),
            "event_kind": "REVIEW_OBSERVATION",
            "finding_id": finding["finding_id"],
            "finding_key": finding["finding_key"],
            "occurrence": occurrence,
            "created_at": review["created_at"],
            "source_authority": "REVIEWER",
            "source_record_id": review["record_id"],
            "source_record_hash": review["record_hash"],
            "payload": payload,
        }
        if prior and not terminal:
            event["previous_event_hash"] = prior["last_event_hash"]
        event_hash = H("fal002-finding-observation-v1", event)
        event.update({"event_id": "FE-" + event_hash[:20], "event_hash": event_hash})
        created.append(event)
    return created


def run_engineering_loop(
    root: Path,
    current_gate: dict[str, Any],
    executor: FAL002ExecutorAdapter,
    reviewer: FAL002ReviewerAdapter,
    *,
    created_at: str,
    criterion_ids: list[str],
    command_runner: Callable[..., dict[str, Any]] = run_command,
    timeout_seconds: float = 120,
) -> dict[str, Any]:
    """Execute one explicit sequential EB-006 engineering-loop cycle."""
    validate_record(current_gate)
    root = root.resolve(strict=True)
    chain = __import__("forge.fal002_io", fromlist=["load_gate_chain"]).load_gate_chain(root, current_gate["series_id"])
    if chain[-1] != current_gate:
        raise FAL002Error("STALE_RECORD", "current GateRecord is not authoritative tip")
    if current_gate["state"] == "correction_required" and current_gate["payload"]["variant_kind"] == "CONTROL":
        control = current_gate["payload"]["control"]
        stop_event = "CEILING_REACHED" if current_gate["payload"]["correction_count"] >= 2 else "NO_PROGRESS" if control["progress"] == "NONE" else None
        if stop_event:
            stopped_control = {**control, "progress": "CEILING" if stop_event == "CEILING_REACHED" else "NONE"}
            stopped = transition(
                current_gate,
                event=stop_event,
                created_at=created_at,
                variant_kind="CONTROL",
                variant=stopped_control,
            )
            persist_transition(root, stopped)
            return {"gate_record": stopped, "eligible": False, "stop_reason": stopped_control["progress"]}
    manifest = chain[0]["payload"]["manifest"]
    ordinal = max((gate["payload"].get("control", {}).get("ordinal", -1) for gate in chain), default=-1) + 1
    suffix = H("fal002-json-content-v1", {"series": current_gate["series_id"], "ordinal": ordinal})[:12]
    execution_id, run_id = f"exec-{ordinal:04d}-{suffix}", f"run-{ordinal:04d}-{suffix}"
    request = {
        "frozen_hash": current_gate["payload"]["frozen_hash"],
        "scope": manifest["allowed_paths"],
        "criteria": criterion_ids,
        "allowed_paths": manifest["allowed_paths"],
        "command_ids": COMMAND_IDS,
        "correction_count": current_gate["payload"]["correction_count"],
        "work_packet_hash": manifest["scope_hash"],
        "request_kind": "INITIAL" if ordinal == 0 else "CORRECTION",
    }
    request_hash = H("fal002-json-content-v1", request)
    exec_grant = _grant(
        "EXECUTOR",
        manifest["executor_principal_id"],
        manifest["executor_adapter_id"],
        f"executor-{suffix}",
        execution_id,
        request_hash,
        created_at,
    )
    execution_gate = transition(
        current_gate,
        event="START_EXECUTION" if current_gate["state"] == "ready" else "START_CORRECTION",
        created_at=created_at,
        variant_kind="EXECUTION",
        variant={
            "execution_id": execution_id,
            "run_id": run_id,
            "ordinal": ordinal,
            "request_kind": request["request_kind"],
            "request": request,
            "request_hash": request_hash,
            "invocation_grant": exec_grant,
        },
    )
    persist_transition(root, execution_gate)
    exchange = seal_record(
        {
            "schema_id": "fal002.executor-exchange.v1",
            "schema_version": 1,
            "record_id": execution_id,
            "series_id": current_gate["series_id"],
            "created_at": created_at,
            "run_id": run_id,
            "ordinal": ordinal,
            "request": request,
            "result": None,
            "invocation": {
                "grant": exec_grant,
                "observed": {
                    "grant_id": exec_grant["grant_id"],
                    "resolved_adapter_path": "forge/fal002_io.py",
                    "adapter_content_hash": HB(Path(__import__("forge.fal002_io", fromlist=["x"]).__file__).read_bytes()),
                    "process_id": os.getpid(),
                    "thread_id": 1,
                    "object_identity": id(executor),
                    "started_at": created_at,
                    "input_hash": request_hash,
                    "termination": "INTERRUPTED",
                },
            },
        }
    )
    exchange = __import__("forge.fal002_io", fromlist=["invoke_executor"]).invoke_executor(executor, exchange, timeout_seconds=timeout_seconds)
    execution_tip = publish_committed(
        root,
        execution_gate,
        exchange,
        created_at=created_at,
        source_authority="EXECUTOR_ADAPTER",
        source_record=execution_gate,
    )
    commands = [command_runner(root, command_id, timeout_seconds=timeout_seconds) for command_id in COMMAND_IDS]
    parsed = {item["command_id"]: item["parsed"] for item in commands}
    offline = manifest.get("offline_evidence")
    if offline is None:
        raise FAL002Error("MISSING_EVIDENCE", "manifest offline evidence required")
    versions = {key: parsed[key].get("version", "not-available") for key in ("GIT-VERSION", "PYTEST-VERSION", "PYTHON-VERSION", "RUFF-VERSION")}
    run = seal_record(
        {
            "schema_id": "fal002.run-record.v1",
            "schema_version": 1,
            "record_id": run_id,
            "series_id": current_gate["series_id"],
            "created_at": created_at,
            "execution_id": execution_id,
            "ordinal": ordinal,
            "repository": {
                "root": ".",
                "branch": parsed["GIT-BRANCH"]["branch"],
                "baseline_head": parsed["GIT-HEAD-BASELINE"]["head"],
                "final_head": parsed["GIT-HEAD-FINAL"]["head"],
                "status": [item["path"] for item in parsed["GIT-STATUS"]["entries"]],
                "changed_paths": parsed["GIT-STATUS"]["changed_paths"],
                "offline_evidence_id": offline["evidence_id"],
                "offline_evidence_record_hash": offline["resolution_record_hash"],
            },
            "runtime": {
                "python_implementation": "CPython",
                "python_version": versions["PYTHON-VERSION"],
                "python_executable": Path(sys.executable).resolve().as_posix(),
                "python_executable_sha256": HB(Path(sys.executable).read_bytes()),
            },
            "tools": [
                _tool("git", "GIT-VERSION", versions["GIT-VERSION"]),
                _tool("pytest", "PYTEST-VERSION", versions["PYTEST-VERSION"]),
                _tool("python", "PYTHON-VERSION", versions["PYTHON-VERSION"]),
                _tool("ruff", "RUFF-VERSION", versions["RUFF-VERSION"]),
            ],
            "commands": commands,
            "diff": {
                "redacted_text": next(item for item in commands if item["command_id"] == "GIT-DIFF")["stdout_text"],
                "sha256": parsed["GIT-DIFF"]["redacted_content_hash"],
                "numstat": parsed["GIT-NUMSTAT"]["entries"],
            },
            "build": {"status": "not_available", "reason": "packaging_forbidden"},
        }
    )
    run_tip = publish_committed(
        root,
        execution_tip,
        run,
        created_at=created_at,
        source_authority="COLLECTOR",
        source_record=execution_gate,
    )
    evidence_gate = transition(
        run_tip,
        event="COLLECT_COMPLETE",
        created_at=created_at,
        variant_kind="EVIDENCE",
        variant={
            "run_id": run_id,
            "run_record_hash": run["record_hash"],
            "execution_id": execution_id,
            "command_ids": COMMAND_IDS,
            "evidence_hash": H("fal002-json-content-v1", commands),
        },
    )
    persist_transition(root, evidence_gate)
    bindings = [
        {
            "criterion_id": criterion,
            "evidence_kind": "TEST_RESULT",
            "source_surface": run["schema_id"],
            "source_record_id": run_id,
            "locator": "/commands/13/classification",
            "assertion": "Authoritative pytest result is bound for reviewer assessment.",
            "content_hash": H("fal002-json-content-v1", commands[13]["classification"]),
            "provenance": {
                "authority": "COLLECTOR",
                "record_id": run_id,
                "record_hash": run["record_hash"],
                "collector_id": "PYTEST",
            },
        }
        for criterion in criterion_ids
    ]
    review_id = f"review-{ordinal:04d}-{suffix}"
    packet = {
        "frozen_hash": request["frozen_hash"],
        "run_record_id": run_id,
        "run_record_hash": run["record_hash"],
        "criterion_ids": criterion_ids,
        "evidence_index": bindings,
        "instructions_hash": manifest["criteria_hash"],
    }
    packet_hash = H("fal002-json-content-v1", packet)
    review_grant = _grant(
        "REVIEWER",
        manifest["reviewer_principal_id"],
        manifest["reviewer_adapter_id"],
        f"reviewer-{suffix}",
        review_id,
        packet_hash,
        created_at,
    )
    review_exchange = seal_record(
        {
            "schema_id": "fal002.reviewer-exchange.v1",
            "schema_version": 1,
            "record_id": review_id,
            "series_id": run["series_id"],
            "created_at": created_at,
            "run_id": run_id,
            "ordinal": ordinal,
            "packet": packet,
            "result": None,
            "reviewer_execution": {
                "grant": review_grant,
                "observed": {
                    "grant_id": review_grant["grant_id"],
                    "resolved_adapter_path": "forge/fal002_io.py",
                    "adapter_content_hash": HB(Path(__import__("forge.fal002_io", fromlist=["x"]).__file__).read_bytes()),
                    "process_id": os.getpid(),
                    "thread_id": 1,
                    "object_identity": id(reviewer),
                    "started_at": created_at,
                    "input_hash": packet_hash,
                    "termination": "INTERRUPTED",
                },
                "fresh_context_verified": True,
                "read_only_packet_verified": True,
                "separation_checks": [
                    "MANIFEST_ROLE_DISTINCT",
                    "PRINCIPAL_DISTINCT",
                    "ADAPTER_ENTRYPOINT_DISTINCT",
                    "GRANT_MATCH",
                    "CONTEXT_FRESH",
                    "PACKET_MINIMAL",
                    "NO_WRITE_CALLBACK",
                ],
            },
        }
    )
    review_gate = transition(
        evidence_gate,
        event="START_REVIEW",
        created_at=created_at,
        variant_kind="REVIEW",
        variant={
            "review_id": review_id,
            "run_id": run_id,
            "ordinal": ordinal,
            "packet": packet,
            "packet_hash": packet_hash,
            "invocation_grant": review_grant,
        },
    )
    persist_transition(root, review_gate)
    review_exchange = __import__("forge.fal002_io", fromlist=["invoke_reviewer"]).invoke_reviewer(reviewer, review_exchange, timeout_seconds=timeout_seconds)
    if executor is reviewer or review_exchange["reviewer_execution"]["grant"]["context_id"] == exec_grant["context_id"] or review_exchange["reviewer_execution"]["observed"]["object_identity"] == exchange["invocation"]["observed"]["object_identity"]:
        raise FAL002Error("INDEPENDENCE_FAILURE", "reviewer execution context is not fresh")
    validate_reviewer_run(review_exchange, run)
    review_tip = publish_committed(
        root,
        review_gate,
        review_exchange,
        created_at=created_at,
        source_authority="REVIEWER_ADAPTER",
        source_record=review_gate,
    )
    prior_events = [event for gate in chain for event in gate["payload"].get("control", {}).get("finding_events", [])]
    events = _finding_events(review_exchange, prior_events)
    findings, checkpoint = fold_finding_events(prior_events + events)
    pending, decision_authority = decisions_pending(root, chain)
    requirements, decision_bindings, decision_applications = decision_authority
    eligible = evaluate_review(
        review_exchange,
        findings,
        pending_decisions=pending,
        evidence_loader=lambda _surface, _id: run,
    )
    current_snapshot = progress_snapshot(run, findings, execution_gate["payload"]["correction_count"])
    previous_snapshot = None
    previous_findings: list[dict[str, Any]] = []
    if request["request_kind"] == "CORRECTION":
        previous_control = next(
            (gate["payload"]["control"] for gate in reversed(chain) if gate["payload"]["variant_kind"] == "CONTROL"),
            None,
        )
        if previous_control is None:
            raise FAL002Error("MISSING_EVIDENCE", "correction requires prior control state")
        previous_findings, _ = reconstruct_findings(chain)
        previous_run_id = next(
            gate["payload"]["evidence"]["run_id"]
            for gate in reversed(chain)
            if gate["payload"]["variant_kind"] == "EVIDENCE"
        )
        previous_run = load_record(root / ".forge" / "fal002" / "series" / current_gate["series_id"] / "runs" / f"{previous_run_id}.json")
        previous_snapshot = progress_snapshot(previous_run, previous_findings, previous_control["correction_count"])
    progress = correction_disposition(
        previous_snapshot,
        current_snapshot,
        previous_findings,
        findings,
        execution_gate["payload"]["correction_count"],
    )
    outcome_event = "REVIEW_PASS" if eligible else "REVIEW_CORRECTION" if review_exchange["result"]["outcome"] == "CORRECTION_REQUIRED" else "REVIEW_BLOCKED"
    variant_kind = "ELIGIBILITY" if eligible else "CONTROL"
    variant = (
        {
            "review_id": review_id,
            "review_hash": review_exchange["record_hash"],
            "criterion_ids": criterion_ids,
            "finding_ids": [item["finding_id"] for item in findings],
            "eligible": True,
        }
        if eligible
        else {
            "ordinal": ordinal,
            "correction_count": execution_gate["payload"]["correction_count"],
            "diff_hash": run["diff"]["sha256"],
            "evidence_hash": current_snapshot["progress_evidence_hash"],
            "finding_ids": [item["finding_id"] for item in findings],
            "progress": progress,
            "decision_requirements": requirements,
            "decision_bindings": decision_bindings,
            "decision_applications": decision_applications,
            "finding_events": events,
            "finding_checkpoint": checkpoint,
        }
    )
    final_gate = transition(
        review_tip,
        event=outcome_event,
        created_at=created_at,
        variant_kind=variant_kind,
        variant=variant,
    )
    persist_transition(root, final_gate)
    return {
        "executor_exchange": exchange,
        "run_record": run,
        "reviewer_exchange": review_exchange,
        "gate_record": final_gate,
        "eligible": eligible,
    }


def resolve_decision(
    decision_identity: str,
    requirements: list[dict[str, Any]],
    bindings: list[dict[str, Any]],
    applications: list[dict[str, Any]],
    record_loader: Callable[[str], dict[str, Any]],
) -> tuple[str, dict[str, Any] | None]:
    matching_requirements = [item for item in requirements if item["decision_identity"] == decision_identity]
    if not matching_requirements:
        raise FAL002Error("MISSING_EVIDENCE", "decision requirement absent")
    canonical = matching_requirements[0]
    if any(item != canonical for item in matching_requirements[1:]):
        raise FAL002Error("AUTHORITY_CONFLICT", "decision requirement changed")
    ordered_bindings = sorted(
        (item for item in bindings if item["decision_identity"] == decision_identity),
        key=lambda item: item["binding_generation"],
    )
    for index, binding in enumerate(ordered_bindings):
        if binding["binding_generation"] != index:
            raise FAL002Error("STALE_RECORD", "binding generation gap")
        if index and binding.get("previous_binding_key") != ordered_bindings[index - 1]["binding_key"]:
            raise FAL002Error("HASH_MISMATCH", "binding predecessor mismatch")
    if not ordered_bindings:
        return "PENDING", None
    latest_binding = ordered_bindings[-1]
    if latest_binding["decision_requirement_hash"] != canonical["decision_requirement_hash"]:
        raise FAL002Error("AUTHORITY_CONFLICT", "binding targets another decision requirement")
    pending = record_loader(latest_binding["pending_card_locator"])
    validate_record(pending)
    if (
        pending["record_hash"] != latest_binding["pending_card_record_hash"]
        or pending["record_id"] != latest_binding["pending_card_record_id"]
        or pending["decision_identity"] != decision_identity
        or pending["binding_generation"] != latest_binding["binding_generation"]
        or pending["payload"]["decision_requirement_hash"] != canonical["decision_requirement_hash"]
        or pending["payload"]["binding_key"] != latest_binding["binding_key"]
        or pending["payload"]["semantic_input"] != canonical["semantic_input"]
    ):
        raise FAL002Error("HASH_MISMATCH", "pending binding mismatch")
    ordered_applications = sorted(
        (item for item in applications if item["decision_identity"] == decision_identity),
        key=lambda item: item["application_ordinal"],
    )
    if not ordered_applications:
        return "PENDING", None
    for index, item in enumerate(ordered_applications):
        if item["application_ordinal"] != index or (index and item.get("previous_application_key") != ordered_applications[index - 1]["application_key"]):
            raise FAL002Error("STALE_RECORD", "decision application lineage gap")
    semantic_hashes = {item["resolution_semantic_hash"] for item in ordered_applications}
    choices = {item["selected_choice"] for item in ordered_applications}
    if len(semantic_hashes) != 1 or len(choices) != 1:
        raise FAL002Error("AUTHORITY_CONFLICT", "conflicting semantic answers")
    application = ordered_applications[-1]
    expected_application = decision_application({key: value for key, value in application.items() if key != "application_key"})
    if application != expected_application:
        raise FAL002Error("HASH_MISMATCH", "decision application key mismatch")
    if (
        application["decision_requirement_hash"] != canonical["decision_requirement_hash"]
        or application["binding_key"] != latest_binding["binding_key"]
        or application["binding_generation"] != latest_binding["binding_generation"]
        or application["pending_card_record_id"] != pending["record_id"]
        or application["pending_card_record_hash"] != pending["record_hash"]
    ):
        raise FAL002Error("STALE_RECORD", "application uses stale binding")
    resolution = record_loader(application["resolution_locator"])
    validate_record(resolution)
    semantic = resolution["payload"]["resolution_semantic_input"]
    presentation = resolution["payload"]["presentation_evidence"]
    if (
        resolution["decision_identity"] != decision_identity
        or resolution["binding_generation"] != latest_binding["binding_generation"]
        or resolution["record_id"] != application["resolution_record_id"]
        or resolution["record_hash"] != application["resolution_record_hash"]
        or resolution["payload"]["resolution_semantic_hash"] != application["resolution_semantic_hash"]
        or semantic["decision_identity"] != decision_identity
        or semantic["answered_requirement_hash"] != canonical["decision_requirement_hash"]
        or semantic["answered_semantic_payload_hash"] != canonical["semantic_payload_hash"]
        or semantic["selected_choice"] not in canonical["semantic_input"]["allowed_choices"]
        or semantic["selected_choice"] != application["selected_choice"]
        or presentation["answered_pending_card_record_id"] != pending["record_id"]
        or presentation["answered_pending_card_record_hash"] != pending["record_hash"]
        or presentation["answered_binding_generation"] != latest_binding["binding_generation"]
        or presentation["answered_binding_key"] != latest_binding["binding_key"]
        or presentation["presentation_evidence_hash"] != application["presentation_evidence_hash"]
    ):
        raise FAL002Error("HASH_MISMATCH", "resolution application mismatch")
    return resolution["status"], resolution


def human_close(accepted_gate: dict[str, Any], decision: dict[str, Any], *, created_at: str) -> dict[str, Any]:
    validate_record(accepted_gate)
    validate_record(decision)
    if accepted_gate["state"] != "accepted" or decision["decision_kind"] != "CLOSURE" or decision["status"] != "ACCEPTED":
        raise FAL002Error("FORBIDDEN_TRANSITION", "human closure authority required")
    payload = decision["payload"]
    if payload["eligible_gate_id"] != accepted_gate["record_id"] or payload["eligible_gate_hash"] != accepted_gate["record_hash"]:
        raise FAL002Error("HASH_MISMATCH", "closure eligibility mismatch")
    return transition(
        accepted_gate,
        event="HUMAN_CLOSE",
        created_at=created_at,
        variant_kind="CLOSURE",
        variant={
            "decision_id": decision["record_id"],
            "decision_hash": decision["record_hash"],
            "eligible_gate_id": accepted_gate["record_id"],
            "eligible_gate_hash": accepted_gate["record_hash"],
        },
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m forge.fal002")
    subcommands = parser.add_subparsers(dest="command", required=True)
    schemas = subcommands.add_parser("schemas")
    schemas.add_argument("--output-root", required=True, type=Path)
    schemas.add_argument("--check", action="store_true")
    inv = subcommands.add_parser("inventory")
    inv.add_argument("--manifest", type=Path)
    inv.add_argument("--output", default="-")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "schemas":
            generated = generate_schemas(args.output_root, check=args.check)
            for item in generated:
                print(f"{item.schema_id} {item.sha256}")
            return 0
        result = inventory(Path.cwd())
        output = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        if args.output == "-":
            sys.stdout.write(output)
        else:
            Path(args.output).write_text(output, encoding="utf-8")
        enforce_limits(result)
        return 0
    except FAL002Error as exc:
        print(str(exc), file=sys.stderr)
        return 3 if exc.code in {"AWAITING_HUMAN", "BUDGET_AUTHORITY_REQUIRED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
# fmt: on
