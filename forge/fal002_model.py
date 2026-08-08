"""Canonical boundary model for the FAL-002 Standard-Assurance loop."""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

Json = None | bool | int | str | list["Json"] | dict[str, "Json"]

SURFACE_MODELS = {
    "fal002.gate-record.v1": "GateRecord",
    "fal002.executor-exchange.v1": "ExecutorExchange",
    "fal002.run-record.v1": "RunRecord",
    "fal002.reviewer-exchange.v1": "ReviewerExchange",
    "fal002.human-decision.v1": "HumanDecisionRecord",
}
SCHEMA_FILES = {
    key: f"{key.removeprefix('fal002.').removesuffix('.v1').replace('.', '-')}-v1.schema.json"
    for key in SURFACE_MODELS
}
HASH_DOMAINS = set(
    """fal002-json-content-v1 fal002-allowed-paths-v1 fal002-scope-v1 fal002-criteria-v1
    fal002-command-policy-v1 fal002-work-packet-v1 fal002-invocation-grant-v1
    fal002-publication-slot-v1 fal002-publication-intent-v1 fal002-recovery-condition-v1
    fal002-recovery-discovery-v1 fal002-conflict-card-v1 fal002-decision-identity-v1
    fal002-decision-requirement-v1 fal002-decision-binding-v1 fal002-offline-evidence-v1
    fal002-finding-key-v1 fal002-remediation-evidence-v1 fal002-finding-observation-v1
    fal002-finding-history-v1 fal002-finding-ledger-v1 fal002-progress-evidence-v1
    fal002-unresolved-findings-v1""".split()
)
HASH_DOMAINS |= {f"fal002-payload-v1:{surface}" for surface in SURFACE_MODELS}
HASH_DOMAINS |= {f"fal002-record-v1:{surface}" for surface in SURFACE_MODELS}

STATES = set(
    "draft ready executing evidence_ready reviewing correction_required blocked awaiting_human "
    "accepted closed".split()
)
SEVERITIES = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
UNRESOLVED_STATES = {"OPEN", "ADDRESSED_AWAITING_REVIEW"}
GATE_VARIANTS = set(
    "MANIFEST INVENTORY EXECUTION EVIDENCE REVIEW CONTROL CHECKPOINT ELIGIBILITY CLOSURE "
    "RECOVERY_ROOT PUBLICATION_INTENT".split()
)
RECOVERY_NAMESPACE = uuid.UUID("6f1b8e9e-6a37-5e3a-9d9e-50dc93295943")
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
HEX_HEAD_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z\Z")
NONEMPTY_RE = re.compile(r"[^ \t\r\n](?:[\s\S]*[^ \t\r\n])?\Z")


class FAL002Error(ValueError):
    """Fail-closed contract error with a stable category."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True)
class GeneratedSchema:
    schema_id: str
    path: Path
    sha256: str


def _json_value(value: Any, location: str = "$", *, keys: bool = True) -> None:
    if value is None or isinstance(value, (bool, int, str)):
        if isinstance(value, str) and any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise FAL002Error("MALFORMED_BOUNDARY", f"lone surrogate at {location}")
        return
    if isinstance(value, float):
        raise FAL002Error("MALFORMED_BOUNDARY", f"float forbidden at {location}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _json_value(item, f"{location}/{index}")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if keys and not isinstance(key, str):
                raise FAL002Error("MALFORMED_BOUNDARY", f"non-string key at {location}")
            _json_value(item, f"{location}/{key}")
        return
    raise FAL002Error("MALFORMED_BOUNDARY", f"non-JSON value at {location}")


def CJ(value: Json) -> bytes:
    """Canonical JSON value bytes without a terminal LF."""
    _json_value(value)
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8", "strict")
    except (UnicodeEncodeError, ValueError, TypeError) as exc:
        raise FAL002Error("MALFORMED_BOUNDARY", "canonical JSON encoding failed") from exc


def CF(value: Json) -> bytes:
    """Canonical persisted JSON bytes with exactly one terminal LF."""
    return CJ(value) + b"\n"


def H(domain: str, value: Json) -> str:
    if domain not in HASH_DOMAINS:
        raise FAL002Error("MALFORMED_BOUNDARY", f"unknown hash domain {domain!r}")
    return hashlib.sha256(CJ({"domain": domain, "value": value})).hexdigest()


def HB(value: bytes) -> str:
    if not isinstance(value, bytes):
        raise FAL002Error("MALFORMED_BOUNDARY", "HB requires exact bytes")
    return hashlib.sha256(value).hexdigest()


def parse_cf(raw: bytes) -> Json:
    if raw.startswith(b"\xef\xbb\xbf") or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid canonical file framing")
    body = raw[:-1]
    try:
        text = body.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid UTF-8") from exc

    def pairs(items: list[tuple[str, Json]]) -> dict[str, Json]:
        result: dict[str, Json] = {}
        for key, value in items:
            if key in result:
                raise FAL002Error("MALFORMED_BOUNDARY", f"duplicate key {key!r}")
            result[key] = value
        return result

    def reject_float(_: str) -> None:
        raise FAL002Error("MALFORMED_BOUNDARY", "decimal/exponent values forbidden")

    try:
        value = json.loads(text, object_pairs_hook=pairs, parse_float=reject_float)
    except FAL002Error:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid JSON") from exc
    _json_value(value)
    if CF(value) != raw:
        raise FAL002Error("MALFORMED_BOUNDARY", "non-canonical persisted bytes")
    return value


def _exact(value: Any, required: set[str], location: str, optional: set[str] | None = None) -> None:
    if not isinstance(value, dict):
        raise FAL002Error("MALFORMED_BOUNDARY", f"object required at {location}")
    optional = optional or set()
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing or extra:
        raise FAL002Error(
            "MALFORMED_BOUNDARY",
            f"closed model mismatch at {location}; missing={sorted(missing)} extra={sorted(extra)}",
        )


def _nonempty(value: Any, location: str) -> str:
    if not isinstance(value, str) or not NONEMPTY_RE.fullmatch(value):
        raise FAL002Error("MALFORMED_BOUNDARY", f"NonEmpty required at {location}")
    return value


def _sha(value: Any, location: str) -> str:
    if not isinstance(value, str) or not SHA_RE.fullmatch(value):
        raise FAL002Error("MALFORMED_BOUNDARY", f"Sha256 required at {location}")
    return value


def _uuid(value: Any, location: str) -> str:
    try:
        parsed = uuid.UUID(str(value))
    except (ValueError, AttributeError) as exc:
        raise FAL002Error("MALFORMED_BOUNDARY", f"UUID required at {location}") from exc
    if str(parsed) != value:
        raise FAL002Error("MALFORMED_BOUNDARY", f"non-canonical UUID at {location}")
    return value


def _timestamp(value: Any, location: str) -> str:
    if not isinstance(value, str) or not TIMESTAMP_RE.fullmatch(value):
        raise FAL002Error("MALFORMED_BOUNDARY", f"Timestamp required at {location}")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise FAL002Error("MALFORMED_BOUNDARY", f"invalid Timestamp at {location}") from exc
    return value


def _path_rel(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise FAL002Error("MALFORMED_BOUNDARY", f"PathRel required at {location}")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or str(path) != value
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise FAL002Error("MALFORMED_BOUNDARY", f"non-canonical PathRel at {location}")
    return value


def _sorted_unique(values: Any, location: str, *, allow_empty: bool = True) -> list[Any]:
    if not isinstance(values, list) or (not allow_empty and not values):
        raise FAL002Error("MALFORMED_BOUNDARY", f"array required at {location}")
    encoded = [CJ(value) for value in values]
    if encoded != sorted(encoded) or len(encoded) != len(set(encoded)):
        raise FAL002Error("MALFORMED_BOUNDARY", f"sorted unique array required at {location}")
    return values


def _payload_input(record: dict[str, Any]) -> dict[str, Any] | Json:
    surface = record["schema_id"]
    if surface == "fal002.gate-record.v1":
        return record["payload"]
    if surface == "fal002.executor-exchange.v1":
        return {key: record[key] for key in ("request", "result", "invocation")}
    if surface == "fal002.run-record.v1":
        return {
            key: record[key]
            for key in ("repository", "runtime", "tools", "commands", "diff", "build")
        }
    if surface == "fal002.reviewer-exchange.v1":
        return {key: record[key] for key in ("packet", "result", "reviewer_execution")}
    return {
        key: record[key]
        for key in (
            "decision_identity",
            "binding_generation",
            "decision_kind",
            "status",
            "owner",
            "provenance",
            "payload",
        )
    }


TOP_LEVEL_FIELDS = {
    "fal002.gate-record.v1": {
        "schema_id",
        "schema_version",
        "record_id",
        "series_id",
        "sequence",
        "predecessor",
        "state",
        "actor",
        "event",
        "created_at",
        "payload",
        "payload_hash",
        "record_hash",
    },
    "fal002.executor-exchange.v1": {
        "schema_id",
        "schema_version",
        "record_id",
        "series_id",
        "created_at",
        "payload_hash",
        "record_hash",
        "run_id",
        "ordinal",
        "request",
        "result",
        "invocation",
    },
    "fal002.run-record.v1": {
        "schema_id",
        "schema_version",
        "record_id",
        "series_id",
        "created_at",
        "payload_hash",
        "record_hash",
        "execution_id",
        "ordinal",
        "repository",
        "runtime",
        "tools",
        "commands",
        "diff",
        "build",
    },
    "fal002.reviewer-exchange.v1": {
        "schema_id",
        "schema_version",
        "record_id",
        "series_id",
        "created_at",
        "payload_hash",
        "record_hash",
        "run_id",
        "ordinal",
        "packet",
        "result",
        "reviewer_execution",
    },
    "fal002.human-decision.v1": {
        "schema_id",
        "schema_version",
        "record_id",
        "series_id",
        "created_at",
        "payload_hash",
        "record_hash",
        "decision_identity",
        "binding_generation",
        "decision_kind",
        "status",
        "owner",
        "provenance",
        "payload",
    },
}


def seal_record(record: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(record)
    surface = result.get("schema_id")
    if surface not in SURFACE_MODELS:
        raise FAL002Error("MALFORMED_BOUNDARY", "unknown surface")
    result.pop("record_hash", None)
    result["payload_hash"] = H(f"fal002-payload-v1:{surface}", _payload_input(result))
    result["record_hash"] = H(f"fal002-record-v1:{surface}", result)
    validate_record(result)
    return result


def validate_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise FAL002Error("MALFORMED_BOUNDARY", "record object required")
    surface = record.get("schema_id")
    if surface not in SURFACE_MODELS:
        raise FAL002Error("MALFORMED_BOUNDARY", "unknown schema_id")
    _exact(record, TOP_LEVEL_FIELDS[surface], "$")
    if record["schema_version"] != 1:
        raise FAL002Error("MALFORMED_BOUNDARY", "schema_version must be 1")
    _nonempty(record["record_id"], "/record_id")
    _uuid(record["series_id"], "/series_id")
    _timestamp(record["created_at"], "/created_at")
    _validate_surface(record)
    expected_payload = H(f"fal002-payload-v1:{surface}", _payload_input(record))
    if record["payload_hash"] != expected_payload:
        raise FAL002Error("HASH_MISMATCH", "payload_hash mismatch")
    unsigned = {key: value for key, value in record.items() if key != "record_hash"}
    expected_record = H(f"fal002-record-v1:{surface}", unsigned)
    if record["record_hash"] != expected_record:
        raise FAL002Error("HASH_MISMATCH", "record_hash mismatch")
    return record


def _validate_surface(record: dict[str, Any]) -> None:
    surface = record["schema_id"]
    if surface == "fal002.gate-record.v1":
        _validate_gate(record)
    elif surface == "fal002.executor-exchange.v1":
        _validate_executor(record)
    elif surface == "fal002.run-record.v1":
        _validate_run(record)
    elif surface == "fal002.reviewer-exchange.v1":
        _validate_reviewer(record)
    else:
        _validate_decision_record(record)


def _validate_gate(record: dict[str, Any]) -> None:
    sequence = record["sequence"]
    if (
        not isinstance(sequence, int)
        or isinstance(sequence, bool)
        or not 0 <= sequence <= 99_999_999
    ):
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid gate sequence")
    if record["record_id"] != f"gate-{sequence:08d}":
        raise FAL002Error("MALFORMED_BOUNDARY", "gate record_id mismatch")
    if (sequence == 0) != (record["predecessor"] is None):
        raise FAL002Error("MALFORMED_BOUNDARY", "predecessor/sequence mismatch")
    if record["predecessor"] is not None:
        _sha(record["predecessor"], "/predecessor")
    if record["state"] not in STATES or record["actor"] not in {
        "human",
        "core",
        "collector",
        "executor",
        "reviewer",
        "recovery",
    }:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid state or actor")
    payload = record["payload"]
    _exact(
        payload,
        {
            "frozen_hash",
            "correction_count",
            "variant_kind",
            payload.get("variant_kind", "").lower(),
        },
        "/payload",
    )
    _sha(payload["frozen_hash"], "/payload/frozen_hash")
    if (
        not isinstance(payload["correction_count"], int)
        or not 0 <= payload["correction_count"] <= 2
    ):
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid correction_count")
    variant = payload["variant_kind"]
    if variant not in GATE_VARIANTS or variant.lower() not in payload:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid gate variant")
    if sequence == 0 and variant not in {"MANIFEST", "RECOVERY_ROOT"}:
        raise FAL002Error("FORBIDDEN_TRANSITION", "invalid sequence-zero variant")
    _validate_gate_variant(variant, payload[variant.lower()])


def _validate_gate_variant(variant: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise FAL002Error("MALFORMED_BOUNDARY", f"{variant} object required")
    if variant == "MANIFEST":
        required = {
            "scope_hash",
            "criteria_hash",
            "allowed_paths",
            "command_policy_hash",
            "executor_principal_id",
            "reviewer_principal_id",
            "executor_adapter_id",
            "reviewer_adapter_id",
            "decision_requirements",
            "decision_bindings",
            "decision_applications",
            "finding_checkpoint",
        }
        _exact(value, required, "/payload/manifest", {"offline_evidence"})
        for key in ("scope_hash", "criteria_hash", "command_policy_hash"):
            _sha(value[key], f"/payload/manifest/{key}")
        for path in value["allowed_paths"]:
            _path_rel(path, "/payload/manifest/allowed_paths")
        _sorted_unique(value["allowed_paths"], "/payload/manifest/allowed_paths", allow_empty=False)
        if (
            value["executor_principal_id"] == value["reviewer_principal_id"]
            or value["executor_adapter_id"] == value["reviewer_adapter_id"]
        ):
            raise FAL002Error("INDEPENDENCE_FAILURE", "executor/reviewer identities must differ")
        _validate_checkpoint(value["finding_checkpoint"])
    elif variant == "CONTROL":
        required = {
            "ordinal",
            "correction_count",
            "diff_hash",
            "evidence_hash",
            "finding_ids",
            "progress",
            "decision_requirements",
            "decision_bindings",
            "decision_applications",
            "finding_events",
            "finding_checkpoint",
        }
        _exact(value, required, "/payload/control")
        if value["progress"] not in {"MATERIAL", "NONE", "CEILING"}:
            raise FAL002Error("MALFORMED_BOUNDARY", "invalid progress")
        _validate_checkpoint(value["finding_checkpoint"])
    elif variant == "PUBLICATION_INTENT":
        _exact(
            value,
            {
                "slot",
                "retained_state",
                "intended_record_hash",
                "intended_file_hash",
                "stage_locator",
                "stage_attempt",
                "stage_file_hash",
                "source_authority",
                "source_record_id",
                "source_record_hash",
                "intent_commitment_hash",
            },
            "/payload/publication_intent",
        )
        _validate_publication_slot(value["slot"])
        if value["slot"]["reconstruction"] != "COMMITTED":
            raise FAL002Error("FORBIDDEN_TRANSITION", "intent requires COMMITTED slot")
        for key in (
            "intended_record_hash",
            "intended_file_hash",
            "stage_file_hash",
            "source_record_hash",
            "intent_commitment_hash",
        ):
            _sha(value[key], f"/payload/publication_intent/{key}")
    elif variant == "RECOVERY_ROOT":
        required = {
            "origin_series_id",
            "predecessor_series_id",
            "predecessor_gate_id",
            "predecessor_gate_hash",
            "publication_slot",
            "recovery_discovery_material",
            "recovery_discovery_key",
            "obstruction",
            "recovery_condition_hash",
            "successor_series_id",
            "recovery_ordinal",
            "predecessor_sealed",
            "retained_state",
            "scope_hash",
            "criteria_hash",
            "allowed_paths_hash",
            "command_policy_hash",
            "frozen_hash",
            "correction_count",
            "max_prior_ordinal",
            "finding_checkpoint",
            "pending_decisions",
            "active_decision_bindings",
            "applied_decisions",
            "no_progress_history",
            "intended_decision_record_id",
            "intended_decision_record_hash",
        }
        _exact(value, required, "/payload/recovery_root")
        _validate_publication_slot(value["publication_slot"])
        _validate_checkpoint(value["finding_checkpoint"])
        if value["predecessor_sealed"] is not True:
            raise FAL002Error("MALFORMED_BOUNDARY", "recovery predecessor must be sealed")
        expected = recovery_candidate_uuid(
            value["recovery_discovery_key"], value["recovery_ordinal"]
        )
        if value["successor_series_id"] != expected:
            raise FAL002Error("HASH_MISMATCH", "recovery successor UUID mismatch")
    elif variant == "ELIGIBILITY":
        _exact(
            value,
            {"review_id", "review_hash", "criterion_ids", "finding_ids", "eligible"},
            "/payload/eligibility",
        )
    elif variant == "CLOSURE":
        _exact(
            value,
            {"decision_id", "decision_hash", "eligible_gate_id", "eligible_gate_hash"},
            "/payload/closure",
        )


def _validate_publication_slot(slot: Any) -> None:
    required = {
        "slot_id",
        "origin_series_id",
        "predecessor_series_id",
        "predecessor_gate_id",
        "predecessor_gate_hash",
        "target_surface",
        "target_record_id",
        "target_path",
        "reconstruction",
    }
    _exact(slot, required, "/publication_slot")
    if slot["target_surface"] not in SURFACE_MODELS or slot["reconstruction"] not in {
        "RECONSTRUCTABLE",
        "COMMITTED",
    }:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid publication slot")
    unsigned = {key: value for key, value in slot.items() if key != "slot_id"}
    if slot["slot_id"] != H("fal002-publication-slot-v1", unsigned):
        raise FAL002Error("HASH_MISMATCH", "publication slot_id mismatch")


def _validate_checkpoint(checkpoint: Any) -> None:
    _exact(
        checkpoint,
        {"event_count", "finding_history_hash", "current_findings", "finding_ledger_hash"},
        "/finding_checkpoint",
    )
    if not isinstance(checkpoint["event_count"], int) or checkpoint["event_count"] < 0:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid event_count")
    _sha(checkpoint["finding_history_hash"], "/finding_checkpoint/finding_history_hash")
    _sha(checkpoint["finding_ledger_hash"], "/finding_checkpoint/finding_ledger_hash")


def _validate_executor(record: dict[str, Any]) -> None:
    if record["record_id"] != record["request"].get("execution_id", record["record_id"]):
        raise FAL002Error("MALFORMED_BOUNDARY", "execution identity mismatch")
    _exact(
        record["request"],
        {
            "execution_id",
            "frozen_hash",
            "scope",
            "criteria",
            "allowed_paths",
            "command_ids",
            "correction_count",
            "work_packet_hash",
            "request_kind",
        },
        "/request",
    )
    if record["result"] is not None:
        _exact(record["result"], {"status", "changed_paths", "summary"}, "/result", {"error_code"})
        if record["result"]["status"] not in {"COMPLETED", "FAILED"}:
            raise FAL002Error("MALFORMED_BOUNDARY", "invalid executor status")
    _validate_invocation(record["invocation"], reviewer=False)


def _validate_invocation(value: Any, *, reviewer: bool) -> None:
    if reviewer:
        _exact(
            value,
            {
                "grant",
                "observed",
                "fresh_context_verified",
                "read_only_packet_verified",
                "separation_checks",
            },
            "/reviewer_execution",
        )
        if (
            value["fresh_context_verified"] is not True
            or value["read_only_packet_verified"] is not True
        ):
            raise FAL002Error("INDEPENDENCE_FAILURE", "reviewer separation false")
        expected = [
            "MANIFEST_ROLE_DISTINCT",
            "PRINCIPAL_DISTINCT",
            "ADAPTER_ENTRYPOINT_DISTINCT",
            "GRANT_MATCH",
            "CONTEXT_FRESH",
            "PACKET_MINIMAL",
            "NO_WRITE_CALLBACK",
        ]
        if value["separation_checks"] != expected:
            raise FAL002Error("INDEPENDENCE_FAILURE", "reviewer separation checks mismatch")
    else:
        _exact(value, {"grant", "observed"}, "/invocation")


def _validate_run(record: dict[str, Any]) -> None:
    if record["record_id"] != record.get("record_id") or not isinstance(record["commands"], list):
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid run")
    _exact(record["build"], {"status", "reason"}, "/build")
    if record["build"] != {"status": "not_available", "reason": "packaging_forbidden"}:
        raise FAL002Error("MALFORMED_BOUNDARY", "build contract mismatch")


def _validate_reviewer(record: dict[str, Any]) -> None:
    _exact(
        record["packet"],
        {
            "frozen_hash",
            "run_record_id",
            "run_record_hash",
            "criterion_ids",
            "evidence_index",
            "instructions_hash",
        },
        "/packet",
    )
    if record["result"] is not None:
        _exact(
            record["result"],
            {"outcome", "findings", "criterion_evidence", "semantic_rationale"},
            "/result",
        )
        if record["result"]["outcome"] not in {
            "PASS",
            "CORRECTION_REQUIRED",
            "BLOCKED",
            "INCONCLUSIVE",
        }:
            raise FAL002Error("MALFORMED_BOUNDARY", "invalid review outcome")
        if record["result"]["outcome"] == "PASS":
            criterion_ids = record["packet"]["criterion_ids"]
            rationale_ids = [
                item.get("criterion_id") for item in record["result"]["semantic_rationale"]
            ]
            if sorted(rationale_ids) != sorted(criterion_ids):
                raise FAL002Error("MISSING_EVIDENCE", "PASS lacks semantic rationale")
            if any(
                item.get("blocking") or item.get("severity") == "CRITICAL"
                for item in record["result"]["findings"]
            ):
                raise FAL002Error("FORBIDDEN_TRANSITION", "PASS contains blocker")
    _validate_invocation(record["reviewer_execution"], reviewer=True)


def _validate_decision_record(record: dict[str, Any]) -> None:
    if (
        not isinstance(record["binding_generation"], int)
        or not 0 <= record["binding_generation"] <= 9999
    ):
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid binding generation")
    _exact(record["provenance"], {"source", "locator", "content_hash"}, "/provenance")
    kind = record["decision_kind"]
    if kind == "PENDING_CARD":
        if record["status"] != "PENDING":
            raise FAL002Error("MALFORMED_BOUNDARY", "pending card status mismatch")
        _exact(
            record["payload"],
            {"decision_requirement_hash", "binding_key", "semantic_input"},
            "/payload",
        )
    elif kind == "RESOLUTION":
        if record["status"] not in {"ACCEPTED", "DECLINED"}:
            raise FAL002Error("MALFORMED_BOUNDARY", "resolution status mismatch")
        _exact(
            record["payload"],
            {"resolution_semantic_input", "resolution_semantic_hash", "presentation_evidence"},
            "/payload",
        )
        expected = H("fal002-json-content-v1", record["payload"]["resolution_semantic_input"])
        if record["payload"]["resolution_semantic_hash"] != expected:
            raise FAL002Error("HASH_MISMATCH", "resolution semantic hash mismatch")
    elif kind == "CLOSURE":
        if record["status"] != "ACCEPTED":
            raise FAL002Error("MALFORMED_BOUNDARY", "closure status mismatch")
        _exact(
            record["payload"],
            {
                "eligible_gate_id",
                "eligible_gate_hash",
                "review_id",
                "review_hash",
                "finding_ledger_hash",
            },
            "/payload",
        )
    else:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid decision kind")


def decision_identity(semantic_input: dict[str, Any]) -> str:
    return "D-" + H("fal002-decision-identity-v1", semantic_input)[:32]


def decision_requirement(value: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(value)
    result["decision_identity"] = decision_identity(result["semantic_input"])
    result["semantic_payload_hash"] = H("fal002-json-content-v1", result["semantic_input"])
    result.pop("decision_requirement_hash", None)
    result["decision_requirement_hash"] = H("fal002-decision-requirement-v1", result)
    return result


def decision_binding(value: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(value)
    result.pop("binding_key", None)
    projection = {key: item for key, item in result.items() if key != "pending_card_record_hash"}
    result["binding_key"] = H(
        "fal002-decision-binding-v1",
        {"binding_object_kind": "PENDING_BINDING", "value": projection},
    )
    return result


def decision_application(value: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(value)
    result.pop("application_key", None)
    result["application_key"] = H(
        "fal002-decision-binding-v1",
        {"binding_object_kind": "RESOLUTION_APPLICATION", "value": result},
    )
    return result


def publication_slot(value: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(value)
    result.pop("slot_id", None)
    result["slot_id"] = H("fal002-publication-slot-v1", result)
    _validate_publication_slot(result)
    return result


def recovery_discovery_material(slot: dict[str, Any]) -> dict[str, Any]:
    return {
        "origin_series_id": slot["origin_series_id"],
        "predecessor_series_id": slot["predecessor_series_id"],
        "predecessor_gate_id": slot["predecessor_gate_id"],
        "predecessor_gate_hash": slot["predecessor_gate_hash"],
        "publication_slot": {
            key: slot[key]
            for key in ("slot_id", "target_surface", "target_record_id", "target_path")
        },
    }


def recovery_discovery_key(material: dict[str, Any]) -> str:
    return H("fal002-recovery-discovery-v1", material)


def recovery_candidate_uuid(discovery_key: str, ordinal: int) -> str:
    _sha(discovery_key, "/recovery_discovery_key")
    if not isinstance(ordinal, int) or ordinal < 0:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid recovery ordinal")
    return str(
        uuid.uuid5(RECOVERY_NAMESPACE, f"fal002-recovery-discovery-v1:{discovery_key}:{ordinal}")
    )


def empty_finding_checkpoint() -> dict[str, Any]:
    return {
        "event_count": 0,
        "finding_history_hash": H("fal002-finding-history-v1", []),
        "current_findings": [],
        "finding_ledger_hash": H("fal002-finding-ledger-v1", []),
    }


def fold_finding_events(
    events: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    states: dict[tuple[str, int], dict[str, Any]] = {}
    previous_global = -1
    ordered: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_ordinal") != previous_global + 1:
            raise FAL002Error("HASH_MISMATCH", "noncontiguous finding event ordinal")
        expected = H(
            "fal002-finding-observation-v1",
            {key: value for key, value in event.items() if key not in {"event_id", "event_hash"}},
        )
        if event.get("event_hash") != expected or event.get("event_id") != "FE-" + expected[:20]:
            raise FAL002Error("HASH_MISMATCH", "finding event identity mismatch")
        key = (event["finding_id"], event["occurrence"])
        current = states.get(key)
        if (current is None) != (event.get("previous_event_hash") is None):
            raise FAL002Error("FORBIDDEN_TRANSITION", "finding predecessor mismatch")
        if current and event["previous_event_hash"] != current["last_event_hash"]:
            raise FAL002Error("HASH_MISMATCH", "finding previous hash mismatch")
        kind = event["event_kind"]
        payload = event["payload"]
        if current is None:
            if kind != "REVIEW_OBSERVATION" or payload.get("observation") != "NEW":
                raise FAL002Error("FORBIDDEN_TRANSITION", "finding occurrence must begin NEW")
            severity = payload["observed_severity"]
            current = {
                "finding_id": event["finding_id"],
                "finding_key": event["finding_key"],
                "occurrence": event["occurrence"],
                "state": "OPEN",
                "severity_epoch": 0,
                "epoch_baseline_severity": severity,
                "current_severity": severity,
                "current_blocking": severity == "CRITICAL" or payload["observed_blocking"],
                "latest_statement": payload["statement"],
                "criterion_ids": payload["criterion_ids"],
                "last_event_hash": event["event_hash"],
                "remediation_evidence_hash": None,
                "replacement_finding_key": None,
            }
            states[key] = current
        else:
            state = current["state"]
            if kind == "REMEDIATION_CLAIM" and state == "OPEN":
                current["state"] = "ADDRESSED_AWAITING_REVIEW"
                current["remediation_evidence_hash"] = payload["remediation"][
                    "remediation_evidence_hash"
                ]
            elif kind == "REVIEW_OBSERVATION":
                observation = payload["observation"]
                if (
                    state == "ADDRESSED_AWAITING_REVIEW"
                    and observation == "ABSENT_AFTER_CORRECTION"
                ):
                    current["state"] = "INDEPENDENTLY_VERIFIED"
                elif observation in {"NEW", "STILL_PRESENT"} and state in {
                    "OPEN",
                    "ADDRESSED_AWAITING_REVIEW",
                    "INDEPENDENTLY_VERIFIED",
                }:
                    current["state"] = "OPEN"
                else:
                    raise FAL002Error("FORBIDDEN_TRANSITION", "invalid review finding transition")
                if SEVERITIES.index(payload["observed_severity"]) > SEVERITIES.index(
                    current["current_severity"]
                ):
                    current["current_severity"] = payload["observed_severity"]
                current["current_blocking"] = (
                    current["current_blocking"]
                    or payload["observed_blocking"]
                    or current["current_severity"] == "CRITICAL"
                )
                current["latest_statement"] = payload["statement"]
            elif kind == "HUMAN_RECLASSIFICATION":
                severity = payload["new_effective_severity"]
                if severity == "CRITICAL" and payload["new_blocking"] is False:
                    raise FAL002Error("FORBIDDEN_TRANSITION", "CRITICAL cannot be nonblocking")
                current["severity_epoch"] += 1
                current["epoch_baseline_severity"] = severity
                current["current_severity"] = severity
                current["current_blocking"] = severity == "CRITICAL" or payload["new_blocking"]
            elif kind == "HUMAN_DISPOSITION":
                disposition = payload["disposition"]
                if disposition == "CLOSE_VERIFIED" and state == "INDEPENDENTLY_VERIFIED":
                    current["state"] = "CLOSED"
                elif disposition == "SUPERSEDE" and state in {
                    "OPEN",
                    "ADDRESSED_AWAITING_REVIEW",
                    "INDEPENDENTLY_VERIFIED",
                }:
                    current["state"] = "SUPERSEDED"
                    current["replacement_finding_key"] = payload.get("replacement_finding_key")
                else:
                    raise FAL002Error("FORBIDDEN_TRANSITION", "invalid human finding disposition")
            else:
                raise FAL002Error("FORBIDDEN_TRANSITION", "invalid finding event")
            current["last_event_hash"] = event["event_hash"]
        previous_global += 1
        ordered.append(event)
    current_values = sorted(
        states.values(), key=lambda item: (item["finding_id"], item["occurrence"])
    )
    checkpoint = {
        "event_count": len(ordered),
        "finding_history_hash": H("fal002-finding-history-v1", ordered),
        "current_findings": current_values,
        "finding_ledger_hash": H("fal002-finding-ledger-v1", current_values),
    }
    return current_values, checkpoint


def pass_eligible(
    current_findings: list[dict[str, Any]], *, pending_decisions: bool, criteria_complete: bool
) -> bool:
    if pending_decisions or not criteria_complete:
        return False
    return not any(
        item["state"] in UNRESOLVED_STATES
        and (item["current_blocking"] or item["current_severity"] == "CRITICAL")
        for item in current_findings
    )


def progress_fingerprint(progress: dict[str, Any]) -> str:
    return H("fal002-progress-evidence-v1", progress)


def unresolved_fingerprint(current: list[dict[str, Any]]) -> str:
    projection = [
        {
            "finding_id": item["finding_id"],
            "occurrence": item["occurrence"],
            "state": item["state"],
            "severity_epoch": item["severity_epoch"],
            "epoch_baseline_severity": item["epoch_baseline_severity"],
            "current_severity": item["current_severity"],
            "current_blocking": item["current_blocking"],
            "last_event_hash": item["last_event_hash"],
            "remediation_evidence_hash_or_absent": item.get("remediation_evidence_hash"),
        }
        for item in current
        if item["state"] in UNRESOLVED_STATES
    ]
    return H("fal002-unresolved-findings-v1", projection)


def _schema_for(surface: str) -> dict[str, Any]:
    required = sorted(TOP_LEVEL_FIELDS[surface])
    properties: dict[str, Any] = {key: {} for key in required}
    properties.update(
        {
            "schema_id": {"const": surface},
            "schema_version": {"const": 1},
            "record_id": {"type": "string", "minLength": 1},
            "series_id": {"type": "string", "format": "uuid"},
            "created_at": {
                "type": "string",
                "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$",
            },
            "payload_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "record_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        }
    )

    def closed(keys: list[str]) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {key: {} for key in keys},
            "additionalProperties": False,
        }

    if surface == "fal002.gate-record.v1":
        variants = {
            "manifest": "scope_hash criteria_hash allowed_paths command_policy_hash executor_principal_id reviewer_principal_id executor_adapter_id reviewer_adapter_id decision_requirements decision_bindings decision_applications finding_checkpoint offline_evidence",  # noqa: E501
            "inventory": "entrypoint baseline_commit python_version files edges exemptions counts dependencies unresolved_targets disposition",  # noqa: E501
            "execution": "execution_id run_id ordinal request_kind request request_hash invocation_grant",  # noqa: E501
            "evidence": "run_id run_record_hash execution_id command_ids evidence_hash",
            "review": "review_id run_id ordinal packet packet_hash invocation_grant",
            "control": "ordinal correction_count diff_hash evidence_hash finding_ids progress decision_requirements decision_bindings decision_applications finding_events finding_checkpoint",  # noqa: E501
            "checkpoint": "reason_code source_record_ids source_hashes interruption_id decision_id resume_state staging_path",  # noqa: E501
            "eligibility": "review_id review_hash criterion_ids finding_ids eligible",
            "closure": "decision_id decision_hash eligible_gate_id eligible_gate_hash",
            "publication_intent": "slot retained_state intended_record_hash intended_file_hash stage_locator stage_attempt stage_file_hash source_authority source_record_id source_record_hash intent_commitment_hash",  # noqa: E501
            "recovery_root": "origin_series_id predecessor_series_id predecessor_gate_id predecessor_gate_hash publication_slot recovery_discovery_material recovery_discovery_key obstruction recovery_condition_hash successor_series_id recovery_ordinal predecessor_sealed retained_state scope_hash criteria_hash allowed_paths_hash command_policy_hash frozen_hash correction_count max_prior_ordinal finding_checkpoint pending_decisions active_decision_bindings applied_decisions no_progress_history intended_decision_record_id intended_decision_record_hash",  # noqa: E501
        }
        properties["payload"] = closed(
            ["frozen_hash", "correction_count", "variant_kind", *variants]
        )
        for name, keys in variants.items():
            properties["payload"]["properties"][name] = closed(keys.split())
    elif surface == "fal002.executor-exchange.v1":
        properties["request"] = closed(
            "execution_id frozen_hash scope criteria allowed_paths command_ids correction_count work_packet_hash request_kind".split()  # noqa: E501
        )
        properties["result"] = {
            "oneOf": [{"type": "null"}, closed("status changed_paths summary error_code".split())]
        }
        properties["invocation"] = closed(["grant", "observed"])
    elif surface == "fal002.run-record.v1":
        properties["repository"] = closed(
            "root branch baseline_head final_head status changed_paths offline_evidence_id offline_evidence_record_hash".split()  # noqa: E501
        )
        properties["runtime"] = closed(
            "python_implementation python_version python_executable python_executable_sha256".split()  # noqa: E501
        )
        properties["build"] = closed(["status", "reason"])
    elif surface == "fal002.reviewer-exchange.v1":
        properties["packet"] = closed(
            "frozen_hash run_record_id run_record_hash criterion_ids evidence_index instructions_hash".split()  # noqa: E501
        )
        properties["result"] = {
            "oneOf": [
                {"type": "null"},
                closed("outcome findings criterion_evidence semantic_rationale".split()),
            ]
        }
        properties["reviewer_execution"] = closed(
            "grant observed fresh_context_verified read_only_packet_verified separation_checks".split()  # noqa: E501
        )
    else:
        properties["provenance"] = closed(["source", "locator", "content_hash"])
        properties["payload"] = closed(
            "decision_requirement_hash binding_key semantic_input resolution_semantic_input resolution_semantic_hash presentation_evidence eligible_gate_id eligible_gate_hash review_id review_hash finding_ledger_hash".split()  # noqa: E501
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": surface,
        "title": SURFACE_MODELS[surface],
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": False,
    }


def generate_schemas(output_root: Path, *, check: bool = False) -> tuple[GeneratedSchema, ...]:
    generated: list[GeneratedSchema] = []
    for surface in sorted(SURFACE_MODELS):
        path = output_root / SCHEMA_FILES[surface]
        raw = (
            json.dumps(_schema_for(surface), ensure_ascii=False, sort_keys=True, indent=2).encode()
            + b"\n"
        )
        if check:
            if not path.is_file() or path.read_bytes() != raw:
                raise FAL002Error("SCHEMA_MISMATCH", str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        generated.append(GeneratedSchema(surface, path, HB(raw)))
    return tuple(generated)
