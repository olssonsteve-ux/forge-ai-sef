"""Sequential FAL-002 Standard-Assurance bounded engineering loop."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from forge.fal002_inventory import enforce_limits, inventory
from forge.fal002_io import (
    canonical_record_path,
    publish_create_only,
    write_current,
)
from forge.fal002_model import (
    FAL002Error,
    decision_application,
    empty_finding_checkpoint,
    fold_finding_events,
    generate_schemas,
    pass_eligible,
    seal_record,
    validate_record,
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


def evaluate_review(
    review: dict[str, Any],
    current_findings: list[dict[str, Any]],
    *,
    pending_decisions: bool,
) -> bool:
    validate_record(review)
    result = review["result"]
    if result is None or result["outcome"] != "PASS":
        return False
    criterion_ids = review["packet"]["criterion_ids"]
    bound = {binding["criterion_id"] for binding in result["criterion_evidence"]}
    rationales = {
        item["criterion_id"] for item in result["semantic_rationale"] if item.get("rationale")
    }
    criteria_complete = set(criterion_ids) <= bound and set(criterion_ids) <= rationales
    return pass_eligible(
        current_findings, pending_decisions=pending_decisions, criteria_complete=criteria_complete
    )


def correction_disposition(
    previous_snapshot: dict[str, Any],
    current_snapshot: dict[str, Any],
    previous_findings: list[dict[str, Any]],
    current_findings: list[dict[str, Any]],
    correction_count: int,
) -> str:
    if correction_count >= 2:
        return "CEILING"
    previous_unresolved = {
        (item["finding_id"], item["occurrence"]): item
        for item in previous_findings
        if item["state"] in {"OPEN", "ADDRESSED_AWAITING_REVIEW"}
    }
    current_by_key = {(item["finding_id"], item["occurrence"]): item for item in current_findings}
    resolved_any = any(
        current_by_key.get(key, {}).get("state")
        in {"INDEPENDENTLY_VERIFIED", "CLOSED", "SUPERSEDED"}
        for key in previous_unresolved
    )
    changed = (
        previous_snapshot["diff_hash"] != current_snapshot["diff_hash"]
        or previous_snapshot["progress_evidence_hash"] != current_snapshot["progress_evidence_hash"]
    )
    introduced = any(
        key not in previous_unresolved
        and item["state"] in {"OPEN", "ADDRESSED_AWAITING_REVIEW"}
        and (item["current_blocking"] or item["current_severity"] == "CRITICAL")
        for key, item in current_by_key.items()
    )
    return "MATERIAL" if changed and resolved_any and not introduced else "NONE"


def resolve_decision(
    decision_identity: str,
    requirements: list[dict[str, Any]],
    bindings: list[dict[str, Any]],
    applications: list[dict[str, Any]],
    record_loader: Callable[[str], dict[str, Any]],
) -> tuple[str, dict[str, Any] | None]:
    matching_requirements = [
        item for item in requirements if item["decision_identity"] == decision_identity
    ]
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
        if (
            index
            and binding.get("previous_binding_key") != ordered_bindings[index - 1]["binding_key"]
        ):
            raise FAL002Error("HASH_MISMATCH", "binding predecessor mismatch")
    if not ordered_bindings:
        return "PENDING", None
    latest_binding = ordered_bindings[-1]
    pending = record_loader(latest_binding["pending_card_locator"])
    validate_record(pending)
    if pending["record_hash"] != latest_binding["pending_card_record_hash"]:
        raise FAL002Error("HASH_MISMATCH", "pending binding mismatch")
    ordered_applications = sorted(
        (item for item in applications if item["decision_identity"] == decision_identity),
        key=lambda item: item["application_ordinal"],
    )
    if not ordered_applications:
        return "PENDING", None
    semantic_hashes = {item["resolution_semantic_hash"] for item in ordered_applications}
    choices = {item["selected_choice"] for item in ordered_applications}
    if len(semantic_hashes) != 1 or len(choices) != 1:
        raise FAL002Error("AUTHORITY_CONFLICT", "conflicting semantic answers")
    application = ordered_applications[-1]
    expected_application = decision_application(
        {key: value for key, value in application.items() if key != "application_key"}
    )
    if application != expected_application:
        raise FAL002Error("HASH_MISMATCH", "decision application key mismatch")
    if application["binding_key"] != latest_binding["binding_key"]:
        raise FAL002Error("STALE_RECORD", "application uses stale binding")
    resolution = record_loader(application["resolution_locator"])
    validate_record(resolution)
    if (
        resolution["record_hash"] != application["resolution_record_hash"]
        or resolution["payload"]["resolution_semantic_hash"]
        != application["resolution_semantic_hash"]
    ):
        raise FAL002Error("HASH_MISMATCH", "resolution application mismatch")
    return resolution["status"], resolution


def human_close(
    accepted_gate: dict[str, Any], decision: dict[str, Any], *, created_at: str
) -> dict[str, Any]:
    validate_record(accepted_gate)
    validate_record(decision)
    if (
        accepted_gate["state"] != "accepted"
        or decision["decision_kind"] != "CLOSURE"
        or decision["status"] != "ACCEPTED"
    ):
        raise FAL002Error("FORBIDDEN_TRANSITION", "human closure authority required")
    payload = decision["payload"]
    if (
        payload["eligible_gate_id"] != accepted_gate["record_id"]
        or payload["eligible_gate_hash"] != accepted_gate["record_hash"]
    ):
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
        output = (
            json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        )
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
