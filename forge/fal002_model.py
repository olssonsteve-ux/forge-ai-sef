# ruff: noqa: E501
"""Canonical boundary model for the FAL-002 Standard-Assurance loop."""
# fmt: off

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
SCHEMA_FILES = {key: f"{key.removeprefix('fal002.').removesuffix('.v1').replace('.', '-')}-v1.schema.json" for key in SURFACE_MODELS}
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

STATES = set("draft ready executing evidence_ready reviewing correction_required blocked awaiting_human accepted closed".split())
SEVERITIES = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
UNRESOLVED_STATES = {"OPEN", "ADDRESSED_AWAITING_REVIEW"}
GATE_VARIANTS = set("MANIFEST INVENTORY EXECUTION EVIDENCE REVIEW CONTROL CHECKPOINT ELIGIBILITY CLOSURE RECOVERY_ROOT PUBLICATION_INTENT".split())
COMMAND_IDS = [
    "GIT-ROOT",
    "PYTHON-VERSION",
    "GIT-VERSION",
    "PYTEST-VERSION",
    "RUFF-VERSION",
    "GIT-HEAD-BASELINE",
    "GIT-BRANCH",
    "INVENTORY",
    "GIT-HEAD-FINAL",
    "GIT-STATUS",
    "GIT-DIFF",
    "GIT-NUMSTAT",
    "SCHEMA-CHECK",
    "PYTEST",
    "RUFF-LINT",
    "RUFF-FORMAT",
    "FORGE-STATUS",
]
EVIDENCE_KINDS = {
    "REPOSITORY_STATE",
    "DIFF",
    "COMMAND_RESULT",
    "TEST_RESULT",
    "BUILD_RESULT",
    "INVENTORY",
    "SCHEMA",
    "REVIEW_FINDING",
    "HUMAN_DECISION",
}
DECISION_DOMAINS = {
    "SCOPE",
    "CRITERIA",
    "BUDGET",
    "AUTHORITY_CONFLICT",
    "EXECUTOR_RETRY",
    "REVIEWER_RETRY",
    "RECOVERY",
    "OFFLINE_EXECUTION",
    "FINDING_DISPOSITION",
    "FINDING_RECLASSIFICATION",
}
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
    if path.is_absolute() or str(path) != value or any(part in {"", ".", ".."} for part in path.parts):
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
        return {key: record[key] for key in ("repository", "runtime", "tools", "commands", "diff", "build")}
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


def _obj(required: dict[str, Any], optional: dict[str, Any] | None = None) -> dict[str, Any]:
    properties = {**required, **(optional or {})}
    return {
        "type": "object",
        "properties": properties,
        "required": list(required),
        "additionalProperties": False,
    }


def _arr(item: dict[str, Any], minimum: int = 0, maximum: int = 65_535) -> dict[str, Any]:
    return {"type": "array", "items": item, "minItems": minimum, "maxItems": maximum}


def _ref(name: str) -> dict[str, str]:
    return {"$ref": f"#/$defs/{name}"}


S = {"type": "string"}
B = {"type": "boolean"}
NNI = {"type": "integer", "minimum": 0}
SHA = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
UUID = {
    "type": "string",
    "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
}
TIMESTAMP = {
    "type": "string",
    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$",
}
NONEMPTY = {
    "type": "string",
    "minLength": 1,
    "pattern": r"^[^ \t\r\n](?:[\s\S]*[^ \t\r\n])?$",
}
PATH_REL = {
    "type": "string",
    "minLength": 1,
    "pattern": r"^(?!/)(?!.*(?:^|/)\.\.?(/|$))(?!.*\\)(?!.*//).+$",
}
PATH_ABS = {"type": "string", "pattern": r"^(?:[A-Z]:/|/).+"}
HEAD = {"type": "string", "pattern": "^(?:[0-9a-f]{40}|[0-9a-f]{64})$"}
SEMVER3 = {"type": "string", "pattern": r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$"}
JSON_POINTER = {"type": "string", "pattern": r"^(?:|(?:/(?:[^~/]|~[01])*)+)$"}
GATE_ID = {"type": "string", "pattern": r"^gate-[0-9]{8}$"}
RUN_ID = {"type": "string", "pattern": r"^run-[0-9]{4}-[0-9a-f]{12}$"}
EXECUTION_ID = {"type": "string", "pattern": r"^exec-[0-9]{4}-[0-9a-f]{12}$"}
REVIEW_ID = {"type": "string", "pattern": r"^review-[0-9]{4}-[0-9a-f]{12}$"}
FINDING_ID = {"type": "string", "pattern": r"^F-[0-9a-f]{20}$"}
CRITERION_ID = {"type": "string", "pattern": r"^FAL2-CC-[0-9]{2}$"}
SURFACE = {"enum": sorted(SURFACE_MODELS)}
COMMAND = {"enum": COMMAND_IDS}
SEVERITY = {"enum": list(SEVERITIES)}

MODEL_DEFS: dict[str, dict[str, Any]] = {
    "Provenance": _obj({"source": NONEMPTY, "locator": NONEMPTY, "content_hash": SHA}),
    "EvidenceProvenance": _obj({"authority": {"enum": ["COLLECTOR", "REVIEWER", "HUMAN"]}, "record_id": NONEMPTY, "record_hash": SHA}, {"collector_id": COMMAND}),
    "EvidenceBinding": _obj({"criterion_id": CRITERION_ID, "evidence_kind": {"enum": sorted(EVIDENCE_KINDS)}, "source_surface": SURFACE, "source_record_id": NONEMPTY, "locator": JSON_POINTER, "assertion": NONEMPTY, "content_hash": SHA, "provenance": _ref("EvidenceProvenance")}),
    "InvocationGrant": _obj({"grant_id": SHA, "role": {"enum": ["EXECUTOR", "REVIEWER"]}, "principal_id": NONEMPTY, "adapter_id": NONEMPTY, "context_id": NONEMPTY, "input_record_id": NONEMPTY, "input_hash": SHA, "issued_by": {"const": "FORGE_CORE"}, "issued_at": TIMESTAMP, "allowed_effect": {"enum": ["RETURN_EXECUTOR_RESULT", "RETURN_REVIEW_RESULT"]}}, {"prior_context_id": NONEMPTY}),
    "ObservedInvocation": _obj({"grant_id": SHA, "resolved_adapter_path": PATH_REL, "adapter_content_hash": SHA, "process_id": {"type": "integer", "minimum": 1}, "thread_id": {"type": "integer", "minimum": 1}, "object_identity": {"type": "integer", "minimum": 1}, "started_at": TIMESTAMP, "input_hash": SHA, "termination": {"enum": ["RETURNED", "TIMEOUT", "INTERRUPTED", "ERROR"]}}, {"ended_at": TIMESTAMP, "output_hash": SHA}),
    "ExecutorRequest": _obj({"frozen_hash": SHA, "scope": _arr(PATH_REL), "criteria": _arr(CRITERION_ID, 1), "allowed_paths": _arr(PATH_REL, 1), "command_ids": _arr(COMMAND, 17, 17), "correction_count": {"type": "integer", "minimum": 0, "maximum": 2}, "work_packet_hash": SHA, "request_kind": {"enum": ["INITIAL", "CORRECTION"]}}),
    "ExecutorResult": _obj({"status": {"enum": ["COMPLETED", "FAILED"]}, "changed_paths": _arr(PATH_REL), "summary": NONEMPTY}, {"error_code": NONEMPTY}),
    "ExecutorInvocation": _obj({"grant": _ref("InvocationGrant"), "observed": _ref("ObservedInvocation")}),
    "InventoryCounts": _obj({name: NNI for name in ("modules", "new_production_loc", "executor_adapters", "reviewer_adapters", "schema_surfaces")}),
    "InventoryEdge": _obj({"edge_id": NONEMPTY, "source": PATH_REL, "target": PATH_REL, "kind": {"enum": ["IMPORT", "DYNAMIC", "SUBPROCESS", "PACKAGE_INIT"]}, "locator": NONEMPTY}),
    "InventoryFile": _obj({"path": PATH_REL, "content_hash": SHA, "inbound_edges": _arr(NONEMPTY), "reason": {"enum": ["ENTRYPOINT", "STATIC_IMPORT", "DYNAMIC_LITERAL", "SUBPROCESS_LITERAL", "PACKAGE_INIT"]}, "classification": {"enum": ["COUNT", "EXEMPT"]}, "counted_loc": NNI, "roles": _arr({"enum": ["EXECUTOR_ADAPTER", "REVIEWER_ADAPTER"]}, 0, 2)}, {"parent_edge": NONEMPTY}),
    "EvidencePredicate": _obj({"name": NONEMPTY, "status": {"enum": ["VERIFIED_TRUE", "VERIFIED_FALSE", "UNKNOWN", "NOT_EVALUATED"]}, "evidence_ref": NONEMPTY}),
    "Exemption": _obj({"path": PATH_REL, "baseline_hash": SHA, "current_hash": SHA, "provenance_ref": NONEMPTY, "closure": _arr(PATH_REL), "predicates": _arr(_ref("EvidencePredicate")), "classification": {"enum": ["EXEMPT", "COUNT", "AWAITING_HUMAN"]}}),
    "DependencyInventory": _obj({"stdlib": _arr(NONEMPTY), "existing_third_party": _arr(NONEMPTY), "new_direct": _arr(NONEMPTY), "new_transitive": _arr(NONEMPTY), "manifest_hash": SHA}, {"lock_hash": SHA}),
    "UnresolvedTarget": _obj({"source": PATH_REL, "locator": NONEMPTY, "expression": NONEMPTY, "kind": {"enum": ["DYNAMIC", "SUBPROCESS", "IMPORT"]}, "reason": NONEMPTY}),
    "Inventory": _obj({"entrypoint": PATH_REL, "baseline_commit": HEAD, "python_version": {"const": "3.14"}, "files": _arr(_ref("InventoryFile"), 1, 8), "edges": _arr(_ref("InventoryEdge")), "exemptions": _arr(_ref("Exemption")), "counts": _ref("InventoryCounts"), "dependencies": _ref("DependencyInventory"), "unresolved_targets": _arr(_ref("UnresolvedTarget")), "disposition": {"enum": ["PASS", "AWAITING_HUMAN"]}}),
    "StatusEntry": _obj({"xy": {"type": "string", "minLength": 2, "maxLength": 2}, "path": PATH_REL}, {"original_path": PATH_REL}),
    "NumstatEntry": _obj({"path": PATH_REL, "added": {"type": ["integer", "null"], "minimum": 0}, "deleted": {"type": ["integer", "null"], "minimum": 0}}),
    "SchemaDigest": _obj({"schema_id": SURFACE, "sha256": SHA}),
    "StatusCategory": _obj({"name": NONEMPTY, "status": {"enum": ["OK", "WARNING", "NOT_APPLICABLE"]}, "evidence_lines": _arr(NONEMPTY)}),
}

PARSED_SUCCESS = [
    _obj({"available": {"const": True}, "root": {"const": "."}}),
    _obj({"available": {"const": True}, "implementation": {"const": "CPython"}, "version": SEMVER3}),
    _obj({"available": {"const": True}, "version": NONEMPTY}),
    _obj({"available": {"const": True}, "head": HEAD, "kind": {"enum": ["BASELINE", "FINAL"]}}),
    _obj({"available": {"const": True}, "branch": NONEMPTY}),
    _obj({"available": {"const": True}, "inventory_hash": SHA, "disposition": {"enum": ["PASS", "AWAITING_HUMAN"]}, "counts": _ref("InventoryCounts")}),
    _obj({"available": {"const": True}, "entries": _arr(_ref("StatusEntry")), "changed_paths": _arr(PATH_REL)}),
    _obj({"available": {"const": True}, "redacted_content_hash": SHA, "byte_count": NNI}),
    _obj({"available": {"const": True}, "entries": _arr(_ref("NumstatEntry"))}),
    _obj({"available": {"const": True}, "schemas": _arr(_ref("SchemaDigest"), 5, 5)}),
    _obj({"available": {"const": True}, "passed": NNI, "failed": NNI, "skipped": NNI, "xfailed": NNI, "xpassed": NNI, "errors": NNI, "warnings": NNI, "duration_seconds_decimal": NONEMPTY}),
    _obj({"available": {"const": True}, "status": {"enum": ["PASS", "FAIL"]}}),
    _obj({"available": {"const": True}, "categories": _arr(_ref("StatusCategory"))}),
]
MODEL_DEFS.update(
    {
        "CommandParsed": {"anyOf": [*PARSED_SUCCESS, _obj({"available": {"const": False}, "failure_reason": NONEMPTY})]},
        "CommandEntry": _obj({"command_id": COMMAND, "phase": {"enum": ["preflight", "pre-execution", "post-executor", "verification"]}, "argv": _arr(NONEMPTY, 1), "cwd": {"const": "."}, "environment_keys": _arr(NONEMPTY, 6, 6), "started_at": TIMESTAMP, "ended_at": TIMESTAMP, "exit_code": {"type": ["integer", "null"]}, "termination": {"enum": ["EXITED", "TIMEOUT", "INTERRUPTED", "SPAWN_ERROR"]}, "stdout_sha256": SHA, "stderr_sha256": SHA, "stdout_text": S, "stderr_text": S, "redaction_count": NNI, "parser_version": {"const": 1}, "parsed": _ref("CommandParsed"), "classification": {"enum": ["PASS", "FAIL", "NOT_AVAILABLE", "BLOCKED", "AWAITING_HUMAN"]}}),
        "Repository": _obj({"root": {"const": "."}, "branch": NONEMPTY, "baseline_head": HEAD, "final_head": HEAD, "status": _arr(NONEMPTY), "changed_paths": _arr(PATH_REL), "offline_evidence_id": SHA, "offline_evidence_record_hash": SHA}),
        "Runtime": _obj({"python_implementation": {"const": "CPython"}, "python_version": SEMVER3, "python_executable": PATH_ABS, "python_executable_sha256": SHA}),
        "Tool": _obj({"name": {"enum": ["git", "python", "pytest", "ruff"]}, "version": NONEMPTY, "executable": PATH_ABS, "executable_sha256": SHA, "version_command_id": COMMAND}),
        "Diff": _obj({"redacted_text": S, "sha256": SHA, "numstat": _arr(_ref("NumstatEntry"))}),
        "Build": _obj({"status": {"const": "not_available"}, "reason": {"const": "packaging_forbidden"}}),
        "ReviewerPacket": _obj(
            {
                "frozen_hash": SHA,
                "run_record_id": RUN_ID,
                "run_record_hash": SHA,
                "criterion_ids": _arr(CRITERION_ID, 1),
                "evidence_index": _arr(_ref("EvidenceBinding"), 1),
                "instructions_hash": SHA,
            }
        ),
        "FindingObservation": _obj(
            {
                "finding_id": FINDING_ID,
                "finding_key": SHA,
                "assurance_property": {
                    "enum": [
                        "BOUNDARY",
                        "EVIDENCE",
                        "INDEPENDENCE",
                        "RECOVERY",
                        "AUTHORITY",
                        "CLOSURE",
                        "DETERMINISM",
                        "SCOPE",
                        "BUDGET",
                    ]
                },
                "defect_locator": NONEMPTY,
                "severity": SEVERITY,
                "blocking": B,
                "criterion_ids": _arr(CRITERION_ID, 1),
                "statement": NONEMPTY,
                "observation": {"enum": ["NEW", "STILL_PRESENT", "ABSENT_AFTER_CORRECTION"]},
            }
        ),
        "SemanticRationale": _obj({"criterion_id": CRITERION_ID, "rationale": NONEMPTY}),
        "ReviewResult": _obj(
            {
                "outcome": {"enum": ["PASS", "CORRECTION_REQUIRED", "BLOCKED", "INCONCLUSIVE"]},
                "findings": _arr(_ref("FindingObservation")),
                "criterion_evidence": _arr(_ref("EvidenceBinding")),
                "semantic_rationale": _arr(_ref("SemanticRationale")),
            }
        ),
        "ReviewerExecution": _obj(
            {
                "grant": _ref("InvocationGrant"),
                "observed": _ref("ObservedInvocation"),
                "fresh_context_verified": {"const": True},
                "read_only_packet_verified": {"const": True},
                "separation_checks": _arr(NONEMPTY, 7, 7),
            }
        ),
    }
)

GATE_VARIANT_MODELS = {
    "MANIFEST": "Manifest",
    "INVENTORY": "Inventory",
    "EXECUTION": "Execution",
    "EVIDENCE": "Evidence",
    "REVIEW": "Review",
    "CONTROL": "Control",
    "CHECKPOINT": "Checkpoint",
    "ELIGIBILITY": "Eligibility",
    "CLOSURE": "Closure",
    "RECOVERY_ROOT": "RecoveryRoot",
    "PUBLICATION_INTENT": "PublicationIntent",
}
MODEL_DEFS["GatePayload"] = {
    "oneOf": [
        _obj(
            {
                "frozen_hash": SHA,
                "correction_count": {"type": "integer", "minimum": 0, "maximum": 2},
                "variant_kind": {"const": variant},
                variant.lower(): _ref(model),
            }
        )
        for variant, model in GATE_VARIANT_MODELS.items()
    ]
}


def _surface_schema(surface: str, *, include_defs: bool) -> dict[str, Any]:
    common = {
        "schema_id": {"const": surface},
        "schema_version": {"const": 1},
        "series_id": UUID,
        "created_at": TIMESTAMP,
        "payload_hash": SHA,
        "record_hash": SHA,
    }
    if surface == "fal002.gate-record.v1":
        fields = {
            **common,
            "record_id": GATE_ID,
            "sequence": {"type": "integer", "minimum": 0, "maximum": 99_999_999},
            "predecessor": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
            "state": {"enum": sorted(STATES)},
            "actor": {"enum": ["human", "core", "collector", "executor", "reviewer", "recovery"]},
            "event": NONEMPTY,
            "payload": _ref("GatePayload"),
        }
        schema = _obj(fields)
    elif surface == "fal002.executor-exchange.v1":
        schema = _obj(
            {
                **common,
                "record_id": EXECUTION_ID,
                "run_id": RUN_ID,
                "ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "request": _ref("ExecutorRequest"),
                "result": {"anyOf": [{"type": "null"}, _ref("ExecutorResult")]},
                "invocation": _ref("ExecutorInvocation"),
            }
        )
    elif surface == "fal002.run-record.v1":
        schema = _obj(
            {
                **common,
                "record_id": RUN_ID,
                "execution_id": EXECUTION_ID,
                "ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "repository": _ref("Repository"),
                "runtime": _ref("Runtime"),
                "tools": _arr(_ref("Tool"), 4, 4),
                "commands": _arr(_ref("CommandEntry"), 17, 17),
                "diff": _ref("Diff"),
                "build": _ref("Build"),
            }
        )
    elif surface == "fal002.reviewer-exchange.v1":
        schema = _obj(
            {
                **common,
                "record_id": REVIEW_ID,
                "run_id": RUN_ID,
                "ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "packet": _ref("ReviewerPacket"),
                "result": {"anyOf": [{"type": "null"}, _ref("ReviewResult")]},
                "reviewer_execution": _ref("ReviewerExecution"),
            }
        )
    else:
        envelope = {
            **common,
            "record_id": NONEMPTY,
            "decision_identity": NONEMPTY,
            "binding_generation": {"type": "integer", "minimum": 0, "maximum": 9999},
            "owner": NONEMPTY,
            "provenance": _ref("Provenance"),
        }
        pending = _obj(
            {
                **envelope,
                "decision_kind": {"const": "PENDING_CARD"},
                "status": {"const": "PENDING"},
                "payload": _obj(
                    {
                        "decision_requirement_hash": SHA,
                        "binding_key": SHA,
                        "semantic_input": _ref("DecisionSemanticInput"),
                    }
                ),
            }
        )
        resolution = _obj(
            {
                **envelope,
                "decision_kind": {"const": "RESOLUTION"},
                "status": {"enum": ["ACCEPTED", "DECLINED"]},
                "payload": _obj(
                    {
                        "resolution_semantic_input": _ref("ResolutionSemanticInput"),
                        "resolution_semantic_hash": SHA,
                        "presentation_evidence": _ref("PresentationEvidence"),
                    }
                ),
            }
        )
        closure = _obj(
            {
                **envelope,
                "decision_kind": {"const": "CLOSURE"},
                "status": {"const": "ACCEPTED"},
                "payload": _obj(
                    {
                        "eligible_gate_id": GATE_ID,
                        "eligible_gate_hash": SHA,
                        "review_id": REVIEW_ID,
                        "review_hash": SHA,
                        "finding_ledger_hash": SHA,
                    }
                ),
            }
        )
        schema = {"oneOf": [pending, resolution, closure]}
    if include_defs:
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": surface,
            "title": SURFACE_MODELS[surface],
            **schema,
            "$defs": deepcopy(MODEL_DEFS),
        }
    return schema


def _check(value: Any, schema: dict[str, Any], location: str = "$", *, defs: dict[str, Any] | None = None) -> None:
    defs = defs or MODEL_DEFS
    if "$ref" in schema:
        return _check(value, defs[schema["$ref"].rsplit("/", 1)[-1]], location, defs=defs)
    for union in ("oneOf", "anyOf"):
        if union in schema:
            matches = 0
            for option in schema[union]:
                try:
                    _check(value, option, location, defs=defs)
                    matches += 1
                except FAL002Error:
                    pass
            invalid = matches != 1 if union == "oneOf" else matches == 0
            if invalid:
                raise FAL002Error("MALFORMED_BOUNDARY", f"{union} mismatch at {location}")
            return
    if "const" in schema and value != schema["const"]:
        raise FAL002Error("MALFORMED_BOUNDARY", f"const mismatch at {location}")
    if "enum" in schema and value not in schema["enum"]:
        raise FAL002Error("MALFORMED_BOUNDARY", f"enum mismatch at {location}")
    expected = schema.get("type")
    allowed = expected if isinstance(expected, list) else [expected] if expected else []
    if allowed:
        actual = "null" if value is None else "boolean" if isinstance(value, bool) else "integer" if isinstance(value, int) else "string" if isinstance(value, str) else "array" if isinstance(value, list) else "object" if isinstance(value, dict) else "invalid"
        if actual not in allowed:
            raise FAL002Error("MALFORMED_BOUNDARY", f"{allowed} required at {location}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", 2**31):
            raise FAL002Error("MALFORMED_BOUNDARY", f"string length at {location}")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise FAL002Error("MALFORMED_BOUNDARY", f"string pattern at {location}")
    if isinstance(value, int) and not isinstance(value, bool):
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            raise FAL002Error("MALFORMED_BOUNDARY", f"integer range at {location}")
    if isinstance(value, list):
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", 2**31):
            raise FAL002Error("MALFORMED_BOUNDARY", f"array length at {location}")
        for index, item in enumerate(value):
            _check(item, schema.get("items", {}), f"{location}/{index}", defs=defs)
    if isinstance(value, dict) and schema.get("type") == "object":
        required = set(schema.get("required", []))
        properties = schema.get("properties", {})
        missing = required - value.keys()
        extra = value.keys() - properties.keys()
        if missing or (schema.get("additionalProperties") is False and extra):
            raise FAL002Error(
                "MALFORMED_BOUNDARY",
                f"closed model mismatch at {location}; missing={sorted(missing)} extra={sorted(extra)}",
            )
        for key, item in value.items():
            if key in properties:
                _check(item, properties[key], f"{location}/{key}", defs=defs)


MODEL_DEFS.update(
    {
        "DecisionOriginalTarget": _obj(
            {
                "target_kind": {"enum": ["GATE", "SERIES_INTENT", "RECOVERY_ROOT"]},
                "origin_series_id": UUID,
                "target_record_id": NONEMPTY,
                "target_semantic_hash": SHA,
            }
        ),
        "DecisionSemanticSource": _obj(
            {
                "authority": {
                    "enum": [
                        "HUMAN",
                        "COLLECTOR",
                        "CANONICAL_MODEL",
                        "REVIEWER",
                        "STATE_SERIES",
                        "REPOSITORY_HISTORY",
                    ]
                },
                "record_id": NONEMPTY,
                "record_hash": SHA,
                "locator": JSON_POINTER,
            }
        ),
        "DecisionSemanticInput": _obj(
            {
                "domain": {"enum": sorted(DECISION_DOMAINS)},
                "question": NONEMPTY,
                "allowed_choices": _arr(NONEMPTY, 2, 16),
                "original_target": _ref("DecisionOriginalTarget"),
                "semantic_sources": _arr(_ref("DecisionSemanticSource")),
            }
        ),
        "DecisionRequirement": _obj(
            {
                "decision_identity": NONEMPTY,
                "semantic_input": _ref("DecisionSemanticInput"),
                "semantic_payload_hash": SHA,
                "required_authority": {"const": "HUMAN"},
                "originating_series_id": UUID,
                "originating_gate_id": GATE_ID,
                "originating_gate_hash": SHA,
                "created_at": TIMESTAMP,
                "decision_requirement_hash": SHA,
            }
        ),
        "DecisionBinding": _obj(
            {
                "decision_identity": NONEMPTY,
                "decision_requirement_hash": SHA,
                "binding_generation": {"type": "integer", "minimum": 0, "maximum": 9999},
                "binding_series_id": UUID,
                "pending_card_record_id": NONEMPTY,
                "pending_card_locator": PATH_REL,
                "pending_card_record_hash": SHA,
                "binding_key": SHA,
            },
            {"previous_binding_key": SHA, "obstruction_evidence_hash": SHA},
        ),
        "ResolutionSemanticInput": _obj(
            {
                "decision_identity": NONEMPTY,
                "answered_requirement_hash": SHA,
                "answered_semantic_payload_hash": SHA,
                "selected_choice": NONEMPTY,
                "rationale": NONEMPTY,
                "human_owner": NONEMPTY,
                "human_provenance": _ref("Provenance"),
                "decided_at": TIMESTAMP,
            }
        ),
        "PresentationEvidence": _obj(
            {
                "answered_pending_card_record_id": NONEMPTY,
                "answered_pending_card_record_hash": SHA,
                "answered_binding_generation": {"type": "integer", "minimum": 0, "maximum": 9999},
                "answered_binding_key": SHA,
                "presented_at": TIMESTAMP,
                "presentation_evidence_hash": SHA,
            }
        ),
        "DecisionApplication": _obj(
            {
                "decision_identity": NONEMPTY,
                "decision_requirement_hash": SHA,
                "binding_generation": {"type": "integer", "minimum": 0, "maximum": 9999},
                "binding_key": SHA,
                "pending_card_record_id": NONEMPTY,
                "pending_card_record_hash": SHA,
                "resolution_record_id": NONEMPTY,
                "resolution_locator": PATH_REL,
                "resolution_record_hash": SHA,
                "resolution_semantic_hash": SHA,
                "presentation_evidence_hash": SHA,
                "selected_choice": NONEMPTY,
                "application_ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "application_key": SHA,
            },
            {"previous_application_key": SHA},
        ),
        "OfflineEvidence": _obj(
            {
                "evidence_id": SHA,
                "decision_identity": NONEMPTY,
                "decision_requirement_hash": SHA,
                "binding_generation": {"type": "integer", "minimum": 0, "maximum": 9999},
                "binding_key": SHA,
                "pending_card_record_id": NONEMPTY,
                "pending_card_record_hash": SHA,
                "resolution_record_id": NONEMPTY,
                "resolution_record_hash": SHA,
                "resolution_locator": PATH_REL,
                "resolution_semantic_hash": SHA,
                "presentation_evidence_hash": SHA,
                "locator": {"const": "/payload/resolution_semantic_input/selected_choice"},
                "content_hash": SHA,
                "collected_at": TIMESTAMP,
                "valid_until": TIMESTAMP,
                "command_policy_hash": SHA,
            }
        ),
        "RemediationEvidence": _obj(
            {
                "finding_id": FINDING_ID,
                "finding_key": SHA,
                "occurrence": NNI,
                "correction_objective_id": NONEMPTY,
                "authorization_decision_id": NONEMPTY,
                "authorization_decision_hash": SHA,
                "corrected_artifact_path": PATH_REL,
                "corrected_locator": NONEMPTY,
                "corrected_content_hash": SHA,
                "correction_baseline_head": HEAD,
                "correction_actor": {"const": "CORRECTION_AGENT"},
                "claim": {"const": "ADDRESSED_AWAITING_REVIEW"},
                "created_at": TIMESTAMP,
                "source_run_id": RUN_ID,
                "source_run_hash": SHA,
                "remediation_evidence_hash": SHA,
            },
            {"correction_result_head": HEAD},
        ),
        "ReviewEventPayload": _obj(
            {
                "observation": {"enum": ["NEW", "STILL_PRESENT", "ABSENT_AFTER_CORRECTION"]},
                "observed_severity": SEVERITY,
                "observed_blocking": B,
                "statement": NONEMPTY,
                "criterion_ids": _arr(CRITERION_ID, 1),
                "evidence_bindings": _arr(_ref("EvidenceBinding"), 1),
                "rationale": NONEMPTY,
            },
            {"recurs_after_event_hash": SHA},
        ),
        "RemediationEventPayload": _obj({"remediation": _ref("RemediationEvidence")}),
        "ReclassificationEventPayload": _obj(
            {
                "new_effective_severity": SEVERITY,
                "new_blocking": B,
                "rationale": NONEMPTY,
                "decision_application_key": SHA,
            }
        ),
        "DispositionEventPayload": _obj(
            {
                "disposition": {"enum": ["CLOSE_VERIFIED", "SUPERSEDE"]},
                "rationale": NONEMPTY,
                "decision_application_key": SHA,
            },
            {"replacement_finding_key": SHA},
        ),
        "FindingEvent": _obj(
            {
                "event_id": NONEMPTY,
                "event_ordinal": {"type": "integer", "minimum": 0, "maximum": 99_999_999},
                "event_kind": {
                    "enum": [
                        "REVIEW_OBSERVATION",
                        "REMEDIATION_CLAIM",
                        "HUMAN_RECLASSIFICATION",
                        "HUMAN_DISPOSITION",
                    ]
                },
                "finding_id": FINDING_ID,
                "finding_key": SHA,
                "occurrence": NNI,
                "created_at": TIMESTAMP,
                "source_authority": {"enum": ["REVIEWER", "CORRECTION_AGENT", "HUMAN"]},
                "source_record_id": NONEMPTY,
                "source_record_hash": SHA,
                "payload": {
                    "oneOf": [
                        _ref("ReviewEventPayload"),
                        _ref("RemediationEventPayload"),
                        _ref("ReclassificationEventPayload"),
                        _ref("DispositionEventPayload"),
                    ]
                },
                "event_hash": SHA,
            },
            {"previous_event_hash": SHA},
        ),
        "CurrentFindingState": _obj(
            {
                "finding_id": FINDING_ID,
                "finding_key": SHA,
                "occurrence": NNI,
                "state": {
                    "enum": [
                        "OPEN",
                        "ADDRESSED_AWAITING_REVIEW",
                        "INDEPENDENTLY_VERIFIED",
                        "CLOSED",
                        "SUPERSEDED",
                    ]
                },
                "severity_epoch": NNI,
                "epoch_baseline_severity": SEVERITY,
                "current_severity": SEVERITY,
                "current_blocking": B,
                "latest_statement": NONEMPTY,
                "criterion_ids": _arr(CRITERION_ID, 1),
                "last_event_hash": SHA,
            },
            {"remediation_evidence_hash": SHA, "replacement_finding_key": SHA},
        ),
        "FindingCheckpoint": _obj(
            {
                "event_count": NNI,
                "finding_history_hash": SHA,
                "current_findings": _arr(_ref("CurrentFindingState")),
                "finding_ledger_hash": SHA,
            }
        ),
        "ProgressSnapshot": _obj(
            {
                "run_id": RUN_ID,
                "diff_hash": SHA,
                "progress_evidence_hash": SHA,
                "unresolved_finding_set_hash": SHA,
                "correction_count": {"type": "integer", "minimum": 0, "maximum": 2},
            }
        ),
        "PublicationSlot": _obj(
            {
                "slot_id": SHA,
                "origin_series_id": UUID,
                "predecessor_series_id": UUID,
                "predecessor_gate_id": GATE_ID,
                "predecessor_gate_hash": SHA,
                "target_surface": SURFACE,
                "target_record_id": NONEMPTY,
                "target_path": PATH_REL,
                "reconstruction": {"enum": ["RECONSTRUCTABLE", "COMMITTED"]},
            }
        ),
        "RecoveryDiscoveryMaterial": _obj(
            {
                "origin_series_id": UUID,
                "predecessor_series_id": UUID,
                "predecessor_gate_id": GATE_ID,
                "predecessor_gate_hash": SHA,
                "publication_slot": _obj(
                    {
                        "slot_id": SHA,
                        "target_surface": SURFACE,
                        "target_record_id": NONEMPTY,
                        "target_path": PATH_REL,
                    }
                ),
            }
        ),
        "ObstructionDescriptor": _obj(
            {
                "origin_series_id": UUID,
                "predecessor_series_id": UUID,
                "predecessor_gate_id": GATE_ID,
                "predecessor_gate_hash": SHA,
                "publication_slot": _ref("PublicationSlot"),
                "intended_record_hash": SHA,
                "intended_file_hash": SHA,
                "target_path": PATH_REL,
                "obstruction_kind": {
                    "enum": [
                        "CONFLICTING_FILE",
                        "MALFORMED_FILE",
                        "NONREGULAR_PATH",
                        "UNREADABLE_PATH",
                    ]
                },
                "path_object_kind": {"enum": ["REGULAR", "SYMLINK", "DIRECTORY", "OTHER"]},
                "frozen_hash": SHA,
            },
            {"intent_gate_id": GATE_ID, "intent_gate_hash": SHA, "observed_content_hash": SHA},
        ),
    }
)

MODEL_DEFS.update(
    {
        "Manifest": _obj(
            {
                "scope_hash": SHA,
                "criteria_hash": SHA,
                "allowed_paths": _arr(PATH_REL, 1),
                "command_policy_hash": SHA,
                "executor_principal_id": NONEMPTY,
                "reviewer_principal_id": NONEMPTY,
                "executor_adapter_id": NONEMPTY,
                "reviewer_adapter_id": NONEMPTY,
                "decision_requirements": _arr(_ref("DecisionRequirement"), 0, 16),
                "decision_bindings": _arr(_ref("DecisionBinding"), 0, 16),
                "decision_applications": _arr(_ref("DecisionApplication"), 0, 16),
                "finding_checkpoint": _ref("FindingCheckpoint"),
            },
            {"offline_evidence": _ref("OfflineEvidence")},
        ),
        "Execution": _obj(
            {
                "execution_id": EXECUTION_ID,
                "run_id": RUN_ID,
                "ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "request_kind": {"enum": ["INITIAL", "CORRECTION"]},
                "request": _ref("ExecutorRequest"),
                "request_hash": SHA,
                "invocation_grant": _ref("InvocationGrant"),
            }
        ),
        "Evidence": _obj(
            {
                "run_id": RUN_ID,
                "run_record_hash": SHA,
                "execution_id": EXECUTION_ID,
                "command_ids": _arr(COMMAND, 17, 17),
                "evidence_hash": SHA,
            }
        ),
        "Review": _obj(
            {
                "review_id": REVIEW_ID,
                "run_id": RUN_ID,
                "ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "packet": _ref("ReviewerPacket"),
                "packet_hash": SHA,
                "invocation_grant": _ref("InvocationGrant"),
            }
        ),
        "Control": _obj(
            {
                "ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "correction_count": {"type": "integer", "minimum": 0, "maximum": 2},
                "diff_hash": SHA,
                "evidence_hash": SHA,
                "finding_ids": _arr(FINDING_ID),
                "progress": {"enum": ["MATERIAL", "NONE", "CEILING"]},
                "decision_requirements": _arr(_ref("DecisionRequirement")),
                "decision_bindings": _arr(_ref("DecisionBinding")),
                "decision_applications": _arr(_ref("DecisionApplication")),
                "finding_events": _arr(_ref("FindingEvent")),
                "finding_checkpoint": _ref("FindingCheckpoint"),
            }
        ),
        "Checkpoint": _obj(
            {
                "reason_code": NONEMPTY,
                "source_record_ids": _arr(NONEMPTY),
                "source_hashes": _arr(SHA),
            },
            {
                "interruption_id": NONEMPTY,
                "decision_id": NONEMPTY,
                "resume_state": {"enum": ["ready", "evidence_ready", "correction_required"]},
                "staging_path": PATH_REL,
            },
        ),
        "Eligibility": _obj(
            {
                "review_id": REVIEW_ID,
                "review_hash": SHA,
                "criterion_ids": _arr(CRITERION_ID, 1),
                "finding_ids": _arr(FINDING_ID),
                "eligible": B,
            }
        ),
        "Closure": _obj(
            {
                "decision_id": NONEMPTY,
                "decision_hash": SHA,
                "eligible_gate_id": GATE_ID,
                "eligible_gate_hash": SHA,
            }
        ),
        "PublicationIntent": _obj(
            {
                "slot": _ref("PublicationSlot"),
                "retained_state": {"enum": sorted(STATES - {"closed"})},
                "intended_record_hash": SHA,
                "intended_file_hash": SHA,
                "stage_locator": PATH_REL,
                "stage_attempt": {"type": "integer", "minimum": 0, "maximum": 9999},
                "stage_file_hash": SHA,
                "source_authority": {
                    "enum": [
                        "FORGE_CORE",
                        "COLLECTOR",
                        "EXECUTOR_ADAPTER",
                        "REVIEWER_ADAPTER",
                        "HUMAN_BOUNDARY",
                    ]
                },
                "source_record_id": NONEMPTY,
                "source_record_hash": SHA,
                "intent_commitment_hash": SHA,
            }
        ),
        "RecoveryRoot": _obj(
            {
                "origin_series_id": UUID,
                "predecessor_series_id": UUID,
                "predecessor_gate_id": GATE_ID,
                "predecessor_gate_hash": SHA,
                "publication_slot": _ref("PublicationSlot"),
                "recovery_discovery_material": _ref("RecoveryDiscoveryMaterial"),
                "recovery_discovery_key": SHA,
                "obstruction": _ref("ObstructionDescriptor"),
                "recovery_condition_hash": SHA,
                "successor_series_id": UUID,
                "recovery_ordinal": NNI,
                "predecessor_sealed": {"const": True},
                "retained_state": {"enum": sorted(STATES)},
                "scope_hash": SHA,
                "criteria_hash": SHA,
                "allowed_paths_hash": SHA,
                "command_policy_hash": SHA,
                "frozen_hash": SHA,
                "correction_count": {"type": "integer", "minimum": 0, "maximum": 2},
                "max_prior_ordinal": {"type": "integer", "minimum": 0, "maximum": 9999},
                "finding_checkpoint": _ref("FindingCheckpoint"),
                "pending_decisions": _arr(_ref("DecisionRequirement")),
                "active_decision_bindings": _arr(_ref("DecisionBinding")),
                "applied_decisions": _arr(_ref("DecisionApplication")),
                "no_progress_history": _arr(_ref("ProgressSnapshot")),
                "intended_decision_record_id": NONEMPTY,
                "intended_decision_record_hash": SHA,
            }
        ),
    }
)


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
    _check(record, _surface_schema(surface, include_defs=False))
    _validate_surface(record)
    expected_payload = H(f"fal002-payload-v1:{surface}", _payload_input(record))
    if record["payload_hash"] != expected_payload:
        raise FAL002Error("HASH_MISMATCH", "payload_hash mismatch")
    unsigned = {key: value for key, value in record.items() if key != "record_hash"}
    expected_record = H(f"fal002-record-v1:{surface}", unsigned)
    if record["record_hash"] != expected_record:
        raise FAL002Error("HASH_MISMATCH", "record_hash mismatch")
    return record


def validate_schema_instance(value: Any, schema: dict[str, Any]) -> None:
    """Validate with the same exact model interpreter used by runtime boundaries."""
    _check(value, schema, defs=schema.get("$defs", MODEL_DEFS))


def resolve_json_pointer(value: Any, pointer: str) -> Any:
    _check(pointer, JSON_POINTER, "/locator")
    current = value
    if not pointer:
        return current
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        try:
            current = current[int(token)] if isinstance(current, list) else current[token]
        except (KeyError, IndexError, ValueError, TypeError) as exc:
            raise FAL002Error("MISSING_EVIDENCE", f"unresolvable locator {pointer}") from exc
    return current


def validate_evidence_binding(binding: dict[str, Any], source_record: dict[str, Any]) -> None:
    _validate_evidence_binding(binding)
    validate_record(source_record)
    provenance = binding["provenance"]
    if binding["source_surface"] != source_record["schema_id"] or binding["source_record_id"] != source_record["record_id"] or provenance["record_id"] != source_record["record_id"] or provenance["record_hash"] != source_record["record_hash"]:
        raise FAL002Error("AUTHORITY_CONFLICT", "evidence source identity mismatch")
    resolved = resolve_json_pointer(source_record, binding["locator"])
    if binding["content_hash"] != H("fal002-json-content-v1", resolved):
        raise FAL002Error("HASH_MISMATCH", "criterion evidence content mismatch")
    if provenance["authority"] == "COLLECTOR":
        if source_record["schema_id"] != "fal002.run-record.v1":
            raise FAL002Error("AUTHORITY_CONFLICT", "collector evidence must resolve to RunRecord")
        command = next(
            (item for item in source_record["commands"] if item["command_id"] == provenance["collector_id"]),
            None,
        )
        if command is None:
            raise FAL002Error("MISSING_EVIDENCE", "collector command absent")


def validate_reviewer_run(review: dict[str, Any], run: dict[str, Any]) -> None:
    validate_record(review)
    validate_record(run)
    packet = review["packet"]
    if run["schema_id"] != "fal002.run-record.v1" or review["run_id"] != run["record_id"] or packet["run_record_id"] != run["record_id"] or packet["run_record_hash"] != run["record_hash"] or review["series_id"] != run["series_id"] or review["ordinal"] != run["ordinal"]:
        raise FAL002Error("AUTHORITY_CONFLICT", "review does not target authoritative RunRecord")


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
    if not isinstance(sequence, int) or isinstance(sequence, bool) or not 0 <= sequence <= 99_999_999:
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
    if not isinstance(payload["correction_count"], int) or not 0 <= payload["correction_count"] <= 2:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid correction_count")
    variant = payload["variant_kind"]
    if variant not in GATE_VARIANTS or variant.lower() not in payload:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid gate variant")
    if sequence == 0 and variant not in {"MANIFEST", "RECOVERY_ROOT"}:
        raise FAL002Error("FORBIDDEN_TRANSITION", "invalid sequence-zero variant")
    _validate_gate_variant(variant, payload[variant.lower()])
    if variant == "RECOVERY_ROOT":
        root = payload["recovery_root"]
        if record["series_id"] != root["successor_series_id"] or record["state"] != "awaiting_human" or record["actor"] != "recovery" or record["event"] != "RECOVERY_SUCCESSOR" or payload["correction_count"] != root["correction_count"] or payload["frozen_hash"] != root["frozen_hash"]:
            raise FAL002Error("HASH_MISMATCH", "recovery root envelope mismatch")
    if variant == "PUBLICATION_INTENT":
        intent = payload["publication_intent"]
        if record["state"] != intent["retained_state"] or record["actor"] != "core" or record["event"] != "PUBLICATION_INTENT_COMMITTED":
            raise FAL002Error("FORBIDDEN_TRANSITION", "publication intent envelope mismatch")


def _validate_grant(grant: dict[str, Any], input_hash: str, role: str) -> None:
    if grant["role"] != role or grant["input_hash"] != input_hash:
        raise FAL002Error("INDEPENDENCE_FAILURE", "invocation grant mismatch")
    effect = "RETURN_EXECUTOR_RESULT" if role == "EXECUTOR" else "RETURN_REVIEW_RESULT"
    if grant["allowed_effect"] != effect or (role == "REVIEWER" and "prior_context_id" in grant):
        raise FAL002Error("INDEPENDENCE_FAILURE", "invocation authority mismatch")


def _validate_evidence_binding(binding: dict[str, Any]) -> None:
    _check(binding, _ref("EvidenceBinding"), "/evidence_binding")
    provenance = binding["provenance"]
    if binding["source_record_id"] != provenance["record_id"]:
        raise FAL002Error("HASH_MISMATCH", "evidence record identity mismatch")
    pairs = {
        "COLLECTOR": {"fal002.run-record.v1", "fal002.gate-record.v1"},
        "REVIEWER": {"fal002.reviewer-exchange.v1"},
        "HUMAN": {"fal002.human-decision.v1"},
    }
    if binding["source_surface"] not in pairs[provenance["authority"]]:
        raise FAL002Error("MALFORMED_BOUNDARY", "evidence authority/surface mismatch")
    if (provenance["authority"] == "COLLECTOR") != ("collector_id" in provenance):
        raise FAL002Error("MALFORMED_BOUNDARY", "collector provenance mismatch")


def _validate_binding_array(bindings: list[dict[str, Any]]) -> None:
    for binding in bindings:
        _validate_evidence_binding(binding)
    keys = [(item["criterion_id"], item["evidence_kind"], item["source_record_id"], item["locator"]) for item in bindings]
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise FAL002Error("MALFORMED_BOUNDARY", "evidence bindings must be sorted and unique")


def _validate_semantic_input(value: dict[str, Any]) -> None:
    _check(value, _ref("DecisionSemanticInput"), "/semantic_input")
    sources = value["semantic_sources"]
    keys = [(item["authority"], item["record_id"], item["record_hash"], item["locator"]) for item in sources]
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise FAL002Error("MALFORMED_BOUNDARY", "decision sources must be sorted and unique")


def _validate_requirement(value: dict[str, Any]) -> None:
    _check(value, _ref("DecisionRequirement"), "/decision_requirement")
    _validate_semantic_input(value["semantic_input"])
    if value["decision_identity"] != decision_identity(value["semantic_input"]) or value["semantic_payload_hash"] != H("fal002-json-content-v1", value["semantic_input"]):
        raise FAL002Error("HASH_MISMATCH", "decision requirement semantic identity mismatch")
    expected = H(
        "fal002-decision-requirement-v1",
        {key: item for key, item in value.items() if key != "decision_requirement_hash"},
    )
    if value["decision_requirement_hash"] != expected:
        raise FAL002Error("HASH_MISMATCH", "decision requirement hash mismatch")


def _validate_binding(value: dict[str, Any]) -> None:
    _check(value, _ref("DecisionBinding"), "/decision_binding")
    generation = value["binding_generation"]
    if (generation == 0 and ({"previous_binding_key", "obstruction_evidence_hash"} & value.keys())) or (generation > 0 and "previous_binding_key" not in value):
        raise FAL002Error("MALFORMED_BOUNDARY", "decision binding generation mismatch")
    expected_id = f"{value['decision_identity']}-pending-b{generation:04d}"
    expected_path = f".forge/fal002/series/{value['binding_series_id']}/decisions/{expected_id}.json"
    if value["pending_card_record_id"] != expected_id or value["pending_card_locator"] != expected_path or decision_binding({key: item for key, item in value.items() if key != "binding_key"}) != value:
        raise FAL002Error("HASH_MISMATCH", "decision binding mismatch")


def _validate_application(value: dict[str, Any]) -> None:
    _check(value, _ref("DecisionApplication"), "/decision_application")
    ordinal = value["application_ordinal"]
    if (ordinal == 0) != ("previous_application_key" not in value):
        raise FAL002Error("MALFORMED_BOUNDARY", "decision application ordinal mismatch")
    if decision_application({key: item for key, item in value.items() if key != "application_key"}) != value:
        raise FAL002Error("HASH_MISMATCH", "decision application mismatch")


def _validate_decision_arrays(value: dict[str, Any]) -> None:
    for requirement in value["decision_requirements"]:
        _validate_requirement(requirement)
    for binding in value["decision_bindings"]:
        _validate_binding(binding)
    for application in value["decision_applications"]:
        _validate_application(application)


def _validate_recovery_root(value: dict[str, Any]) -> None:
    slot = value["publication_slot"]
    _validate_publication_slot(slot)
    material = recovery_discovery_material(slot)
    if value["recovery_discovery_material"] != material or value["recovery_discovery_key"] != recovery_discovery_key(material):
        raise FAL002Error("HASH_MISMATCH", "recovery discovery mismatch")
    for key in (
        "origin_series_id",
        "predecessor_series_id",
        "predecessor_gate_id",
        "predecessor_gate_hash",
    ):
        if value[key] != slot[key] or value["obstruction"][key] != slot[key]:
            raise FAL002Error("HASH_MISMATCH", "recovery predecessor mismatch")
    obstruction = value["obstruction"]
    if obstruction["publication_slot"] != slot or obstruction["target_path"] != slot["target_path"]:
        raise FAL002Error("HASH_MISMATCH", "recovery obstruction mismatch")
    if value["recovery_condition_hash"] != H("fal002-recovery-condition-v1", obstruction):
        raise FAL002Error("HASH_MISMATCH", "recovery condition mismatch")
    if value["successor_series_id"] != recovery_candidate_uuid(value["recovery_discovery_key"], value["recovery_ordinal"]):
        raise FAL002Error("HASH_MISMATCH", "recovery successor UUID mismatch")
    _validate_decision_arrays(
        {
            "decision_requirements": value["pending_decisions"],
            "decision_bindings": value["active_decision_bindings"],
            "decision_applications": value["applied_decisions"],
        }
    )
    _validate_checkpoint(value["finding_checkpoint"])


def _validate_gate_variant(variant: str, value: Any) -> None:
    _check(value, _ref(GATE_VARIANT_MODELS[variant]), f"/payload/{variant.lower()}")
    if variant == "MANIFEST":
        _sorted_unique(value["allowed_paths"], "/payload/manifest/allowed_paths", allow_empty=False)
        if value["executor_principal_id"] == value["reviewer_principal_id"] or value["executor_adapter_id"] == value["reviewer_adapter_id"]:
            raise FAL002Error("INDEPENDENCE_FAILURE", "executor/reviewer identities must differ")
        _validate_decision_arrays(value)
        _validate_checkpoint(value["finding_checkpoint"])
    elif variant == "INVENTORY":
        if value["counts"]["modules"] > 4 or value["counts"]["new_production_loc"] > 3000 or value["counts"]["executor_adapters"] != 1 or value["counts"]["reviewer_adapters"] != 1 or value["counts"]["schema_surfaces"] != 5:
            if value["disposition"] != "AWAITING_HUMAN":
                raise FAL002Error("BUDGET_AUTHORITY_REQUIRED", "inventory limit mismatch")
    elif variant == "EXECUTION":
        if value["request_kind"] != value["request"]["request_kind"] or value["request_hash"] != H("fal002-json-content-v1", value["request"]):
            raise FAL002Error("HASH_MISMATCH", "execution request mismatch")
        if value["request"]["command_ids"] != COMMAND_IDS:
            raise FAL002Error("MISSING_EVIDENCE", "execution requires exact command inventory")
        _validate_grant(value["invocation_grant"], value["request_hash"], "EXECUTOR")
    elif variant == "EVIDENCE":
        if value["command_ids"] != COMMAND_IDS:
            raise FAL002Error("MISSING_EVIDENCE", "evidence requires exact command inventory")
    elif variant == "REVIEW":
        if value["packet_hash"] != H("fal002-json-content-v1", value["packet"]):
            raise FAL002Error("HASH_MISMATCH", "review packet mismatch")
        _validate_grant(value["invocation_grant"], value["packet_hash"], "REVIEWER")
        _validate_binding_array(value["packet"]["evidence_index"])
    elif variant == "CONTROL":
        _validate_decision_arrays(value)
        for event in value["finding_events"]:
            _validate_finding_event(event)
        _validate_checkpoint(value["finding_checkpoint"])
    elif variant == "PUBLICATION_INTENT":
        _validate_publication_slot(value["slot"])
        if value["slot"]["reconstruction"] != "COMMITTED":
            raise FAL002Error("FORBIDDEN_TRANSITION", "intent requires COMMITTED slot")
        expected_stage = f".forge/fal002/series/{value['slot']['predecessor_series_id']}/.staging/{value['slot']['slot_id']}/attempt-{value['stage_attempt']:04d}.json.part"
        if value["stage_locator"] != expected_stage or value["intended_file_hash"] != value["stage_file_hash"]:
            raise FAL002Error("HASH_MISMATCH", "publication stage binding mismatch")
        expected = H(
            "fal002-publication-intent-v1",
            {key: item for key, item in value.items() if key != "intent_commitment_hash"},
        )
        if value["intent_commitment_hash"] != expected:
            raise FAL002Error("HASH_MISMATCH", "publication intent commitment mismatch")
    elif variant == "RECOVERY_ROOT":
        _validate_recovery_root(value)


def _validate_publication_slot(slot: Any) -> None:
    _check(slot, _ref("PublicationSlot"), "/publication_slot")
    unsigned = {key: value for key, value in slot.items() if key != "slot_id"}
    if slot["slot_id"] != H("fal002-publication-slot-v1", unsigned):
        raise FAL002Error("HASH_MISMATCH", "publication slot_id mismatch")
    folders = {
        "fal002.gate-record.v1": "gate",
        "fal002.executor-exchange.v1": "executor",
        "fal002.run-record.v1": "runs",
        "fal002.reviewer-exchange.v1": "reviewer",
        "fal002.human-decision.v1": "decisions",
    }
    filename = f"{int(slot['target_record_id'].removeprefix('gate-')):08d}.json" if slot["target_surface"] == "fal002.gate-record.v1" else f"{slot['target_record_id']}.json"
    expected = f".forge/fal002/series/{slot['predecessor_series_id']}/{folders[slot['target_surface']]}/{filename}"
    if slot["target_path"] != expected:
        raise FAL002Error("HASH_MISMATCH", "publication target path mismatch")


def _validate_checkpoint(checkpoint: Any) -> None:
    _check(checkpoint, _ref("FindingCheckpoint"), "/finding_checkpoint")
    current = checkpoint["current_findings"]
    if current != sorted(current, key=lambda item: (item["finding_id"], item["occurrence"])):
        raise FAL002Error("MALFORMED_BOUNDARY", "finding checkpoint order mismatch")


def _validate_executor(record: dict[str, Any]) -> None:
    if not record["record_id"].startswith(f"exec-{record['ordinal']:04d}-") or not record["run_id"].startswith(f"run-{record['ordinal']:04d}-"):
        raise FAL002Error("MALFORMED_BOUNDARY", "execution ordinal identity mismatch")
    if record["request"]["command_ids"] != COMMAND_IDS:
        raise FAL002Error("MISSING_EVIDENCE", "executor request command inventory mismatch")
    if record["result"] is not None:
        _sorted_unique(record["result"]["changed_paths"], "/result/changed_paths")
        if record["result"]["status"] == "COMPLETED" and "error_code" in record["result"]:
            raise FAL002Error("MALFORMED_BOUNDARY", "completed executor has error code")
    _validate_invocation(record["invocation"], reviewer=False)
    request_hash = H("fal002-json-content-v1", record["request"])
    _validate_grant(record["invocation"]["grant"], request_hash, "EXECUTOR")
    observed = record["invocation"]["observed"]
    if observed["grant_id"] != record["invocation"]["grant"]["grant_id"] or observed["input_hash"] != request_hash:
        raise FAL002Error("INDEPENDENCE_FAILURE", "executor observation mismatch")
    expected_output = None if record["result"] is None else H("fal002-json-content-v1", record["result"])
    _validate_observation(observed, expected_output)


def _validate_invocation(value: Any, *, reviewer: bool) -> None:
    _check(
        value,
        _ref("ReviewerExecution" if reviewer else "ExecutorInvocation"),
        "/reviewer_execution" if reviewer else "/invocation",
    )
    if reviewer and value["separation_checks"] != [
        "MANIFEST_ROLE_DISTINCT",
        "PRINCIPAL_DISTINCT",
        "ADAPTER_ENTRYPOINT_DISTINCT",
        "GRANT_MATCH",
        "CONTEXT_FRESH",
        "PACKET_MINIMAL",
        "NO_WRITE_CALLBACK",
    ]:
        raise FAL002Error("INDEPENDENCE_FAILURE", "reviewer separation checks mismatch")


def _validate_observation(observed: dict[str, Any], expected_output: str | None) -> None:
    termination = observed["termination"]
    ended = "ended_at" in observed
    output = observed.get("output_hash")
    valid = termination == "RETURNED" and ended and output == expected_output or termination in {"TIMEOUT", "ERROR"} and ended and output is None or termination == "INTERRUPTED" and not ended and output is None
    if not valid or (ended and observed["ended_at"] < observed["started_at"]):
        raise FAL002Error("MALFORMED_BOUNDARY", "invocation observation mismatch")


def _validate_run(record: dict[str, Any]) -> None:
    ordinal = record["ordinal"]
    if not record["record_id"].startswith(f"run-{ordinal:04d}-") or not record["execution_id"].startswith(f"exec-{ordinal:04d}-"):
        raise FAL002Error("MALFORMED_BOUNDARY", "run identity mismatch")
    if not record["runtime"]["python_version"].startswith("3.14."):
        raise FAL002Error("UNSUPPORTED_VERSION", "Python 3.14 required")
    names = [item["name"] for item in record["tools"]]
    if names != ["git", "pytest", "python", "ruff"]:
        raise FAL002Error("MALFORMED_BOUNDARY", "tool order mismatch")
    version_ids = {
        "git": "GIT-VERSION",
        "pytest": "PYTEST-VERSION",
        "python": "PYTHON-VERSION",
        "ruff": "RUFF-VERSION",
    }
    if any(item["version_command_id"] != version_ids[item["name"]] for item in record["tools"]):
        raise FAL002Error("MALFORMED_BOUNDARY", "tool command mismatch")
    if [item["command_id"] for item in record["commands"]] != COMMAND_IDS:
        raise FAL002Error("MISSING_EVIDENCE", "RunRecord requires 17 ordered commands")
    expected_env = ["PATH", "PYTHONIOENCODING", "PYTHONUTF8", "SYSTEMROOT", "TEMP", "TMP"]
    for command in record["commands"]:
        if command["environment_keys"] != expected_env or (command["termination"] == "EXITED") != (command["exit_code"] is not None):
            raise FAL002Error("MALFORMED_BOUNDARY", "command execution mismatch")
        _validate_command_parsed(command)
    _sorted_unique(record["repository"]["changed_paths"], "/repository/changed_paths")
    if record["diff"]["sha256"] != HB(record["diff"]["redacted_text"].encode("utf-8")):
        raise FAL002Error("HASH_MISMATCH", "diff hash mismatch")
    if record["diff"]["numstat"] != sorted(record["diff"]["numstat"], key=lambda item: item["path"]):
        raise FAL002Error("MALFORMED_BOUNDARY", "numstat order mismatch")


def _validate_command_parsed(command: dict[str, Any]) -> None:
    parsed = command["parsed"]
    if not parsed["available"]:
        return
    keys = set(parsed) - {"available"}
    expected = {
        "GIT-ROOT": {"root"},
        "PYTHON-VERSION": {"implementation", "version"},
        "GIT-VERSION": {"version"},
        "PYTEST-VERSION": {"version"},
        "RUFF-VERSION": {"version"},
        "GIT-HEAD-BASELINE": {"head", "kind"},
        "GIT-BRANCH": {"branch"},
        "INVENTORY": {"inventory_hash", "disposition", "counts"},
        "GIT-HEAD-FINAL": {"head", "kind"},
        "GIT-STATUS": {"entries", "changed_paths"},
        "GIT-DIFF": {"redacted_content_hash", "byte_count"},
        "GIT-NUMSTAT": {"entries"},
        "SCHEMA-CHECK": {"schemas"},
        "PYTEST": {
            "passed",
            "failed",
            "skipped",
            "xfailed",
            "xpassed",
            "errors",
            "warnings",
            "duration_seconds_decimal",
        },
        "RUFF-LINT": {"status"},
        "RUFF-FORMAT": {"status"},
        "FORGE-STATUS": {"categories"},
    }[command["command_id"]]
    if keys != expected:
        raise FAL002Error("MALFORMED_BOUNDARY", "command parsed discriminator mismatch")


def _validate_reviewer(record: dict[str, Any]) -> None:
    if not record["record_id"].startswith(f"review-{record['ordinal']:04d}-") or not record["run_id"].startswith(f"run-{record['ordinal']:04d}-"):
        raise FAL002Error("MALFORMED_BOUNDARY", "review identity mismatch")
    _sorted_unique(record["packet"]["criterion_ids"], "/packet/criterion_ids", allow_empty=False)
    _validate_binding_array(record["packet"]["evidence_index"])
    if record["result"] is not None:
        _validate_binding_array(record["result"]["criterion_evidence"])
        if any(binding not in record["packet"]["evidence_index"] for binding in record["result"]["criterion_evidence"]):
            raise FAL002Error("AUTHORITY_CONFLICT", "reviewer rewrote evidence binding")
        for finding in record["result"]["findings"]:
            identity = H(
                "fal002-finding-key-v1",
                {
                    "assurance_property": finding["assurance_property"],
                    "defect_locator": finding["defect_locator"],
                    "criterion_ids": finding["criterion_ids"],
                },
            )
            if finding["finding_key"] != identity or finding["finding_id"] != "F-" + identity[:20]:
                raise FAL002Error("HASH_MISMATCH", "finding identity mismatch")
        if record["result"]["outcome"] == "PASS":
            criterion_ids = record["packet"]["criterion_ids"]
            rationale_ids = [item["criterion_id"] for item in record["result"]["semantic_rationale"]]
            evidence_ids = {item["criterion_id"] for item in record["result"]["criterion_evidence"]}
            if rationale_ids != criterion_ids or set(criterion_ids) - evidence_ids:
                raise FAL002Error("MISSING_EVIDENCE", "PASS lacks semantic rationale")
            if any(item["blocking"] or item["severity"] == "CRITICAL" for item in record["result"]["findings"]):
                raise FAL002Error("FORBIDDEN_TRANSITION", "PASS contains blocker")
    _validate_invocation(record["reviewer_execution"], reviewer=True)
    packet_hash = H("fal002-json-content-v1", record["packet"])
    _validate_grant(record["reviewer_execution"]["grant"], packet_hash, "REVIEWER")
    observed = record["reviewer_execution"]["observed"]
    if observed["grant_id"] != record["reviewer_execution"]["grant"]["grant_id"] or observed["input_hash"] != packet_hash:
        raise FAL002Error("INDEPENDENCE_FAILURE", "reviewer observation mismatch")
    _validate_observation(
        observed,
        None if record["result"] is None else H("fal002-json-content-v1", record["result"]),
    )


def _validate_decision_record(record: dict[str, Any]) -> None:
    kind = record["decision_kind"]
    if kind == "PENDING_CARD":
        _validate_semantic_input(record["payload"]["semantic_input"])
        expected = f"{record['decision_identity']}-pending-b{record['binding_generation']:04d}"
        if record["record_id"] != expected or record["decision_identity"] != decision_identity(record["payload"]["semantic_input"]):
            raise FAL002Error("HASH_MISMATCH", "pending decision identity mismatch")
    elif kind == "RESOLUTION":
        payload = record["payload"]
        expected_id = f"{record['decision_identity']}-resolution-b{record['binding_generation']:04d}"
        expected = H("fal002-json-content-v1", payload["resolution_semantic_input"])
        presentation = payload["presentation_evidence"]
        presentation_hash = H(
            "fal002-json-content-v1",
            {key: item for key, item in presentation.items() if key != "presentation_evidence_hash"},
        )
        if record["record_id"] != expected_id or payload["resolution_semantic_input"]["decision_identity"] != record["decision_identity"] or payload["resolution_semantic_hash"] != expected or presentation["presentation_evidence_hash"] != presentation_hash or presentation["presented_at"] > payload["resolution_semantic_input"]["decided_at"]:
            raise FAL002Error("HASH_MISMATCH", "resolution semantic hash mismatch")


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
        "publication_slot": {key: slot[key] for key in ("slot_id", "target_surface", "target_record_id", "target_path")},
    }


def recovery_discovery_key(material: dict[str, Any]) -> str:
    return H("fal002-recovery-discovery-v1", material)


def recovery_candidate_uuid(discovery_key: str, ordinal: int) -> str:
    _sha(discovery_key, "/recovery_discovery_key")
    if not isinstance(ordinal, int) or ordinal < 0:
        raise FAL002Error("MALFORMED_BOUNDARY", "invalid recovery ordinal")
    return str(uuid.uuid5(RECOVERY_NAMESPACE, f"fal002-recovery-discovery-v1:{discovery_key}:{ordinal}"))


def empty_finding_checkpoint() -> dict[str, Any]:
    return {
        "event_count": 0,
        "finding_history_hash": H("fal002-finding-history-v1", []),
        "current_findings": [],
        "finding_ledger_hash": H("fal002-finding-ledger-v1", []),
    }


def _validate_finding_event(event: dict[str, Any]) -> None:
    _check(event, _ref("FindingEvent"), "/finding_event")
    expected_authority = {
        "REVIEW_OBSERVATION": "REVIEWER",
        "REMEDIATION_CLAIM": "CORRECTION_AGENT",
        "HUMAN_RECLASSIFICATION": "HUMAN",
        "HUMAN_DISPOSITION": "HUMAN",
    }[event["event_kind"]]
    if event["source_authority"] != expected_authority:
        raise FAL002Error("AUTHORITY_CONFLICT", "finding event authority mismatch")
    expected = H(
        "fal002-finding-observation-v1",
        {key: value for key, value in event.items() if key not in {"event_id", "event_hash"}},
    )
    if event["event_hash"] != expected or event["event_id"] != "FE-" + expected[:20]:
        raise FAL002Error("HASH_MISMATCH", "finding event identity mismatch")
    payload = event["payload"]
    kind = event["event_kind"]
    if kind == "REVIEW_OBSERVATION":
        _validate_binding_array(payload["evidence_bindings"])
    elif kind == "REMEDIATION_CLAIM":
        remediation = payload["remediation"]
        if any(remediation[key] != event[key] for key in ("finding_id", "finding_key", "occurrence")):
            raise FAL002Error("HASH_MISMATCH", "remediation finding mismatch")
        expected_hash = H(
            "fal002-remediation-evidence-v1",
            {key: value for key, value in remediation.items() if key != "remediation_evidence_hash"},
        )
        if remediation["remediation_evidence_hash"] != expected_hash:
            raise FAL002Error("HASH_MISMATCH", "remediation evidence mismatch")
    elif kind == "HUMAN_DISPOSITION":
        if (payload["disposition"] == "SUPERSEDE") != ("replacement_finding_key" in payload):
            raise FAL002Error("MALFORMED_BOUNDARY", "disposition replacement mismatch")


def fold_finding_events(
    events: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    states: dict[tuple[str, int], dict[str, Any]] = {}
    latest: dict[str, dict[str, Any]] = {}
    previous_global = -1
    ordered: list[dict[str, Any]] = []
    for event in events:
        _validate_finding_event(event)
        if event.get("event_ordinal") != previous_global + 1:
            raise FAL002Error("HASH_MISMATCH", "noncontiguous finding event ordinal")
        key = (event["finding_id"], event["occurrence"])
        current = states.get(key)
        if (current is None) != (event.get("previous_event_hash") is None):
            raise FAL002Error("FORBIDDEN_TRANSITION", "finding predecessor mismatch")
        if current and event["previous_event_hash"] != current["last_event_hash"]:
            raise FAL002Error("HASH_MISMATCH", "finding previous hash mismatch")
        kind = event["event_kind"]
        payload = event["payload"]
        if current is None:
            prior = latest.get(event["finding_id"])
            if kind != "REVIEW_OBSERVATION" or payload.get("observation") not in {
                "NEW",
                "STILL_PRESENT",
            }:
                raise FAL002Error("FORBIDDEN_TRANSITION", "finding occurrence must begin NEW")
            if event["occurrence"] == 0:
                if prior is not None or "recurs_after_event_hash" in payload:
                    raise FAL002Error("FORBIDDEN_TRANSITION", "initial finding cannot recur")
            elif prior is None or event["occurrence"] != prior["occurrence"] + 1 or prior["state"] not in {"CLOSED", "SUPERSEDED"} or payload.get("recurs_after_event_hash") != prior["last_event_hash"]:
                raise FAL002Error("FORBIDDEN_TRANSITION", "invalid prior-terminal recurrence")
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
            }
            states[key] = current
            latest[event["finding_id"]] = current
        else:
            state = current["state"]
            if kind == "REMEDIATION_CLAIM" and state == "OPEN":
                current["state"] = "ADDRESSED_AWAITING_REVIEW"
                current["remediation_evidence_hash"] = payload["remediation"]["remediation_evidence_hash"]
            elif kind == "REVIEW_OBSERVATION":
                observation = payload["observation"]
                if state == "ADDRESSED_AWAITING_REVIEW" and observation == "ABSENT_AFTER_CORRECTION":
                    current["state"] = "INDEPENDENTLY_VERIFIED"
                elif observation in {"NEW", "STILL_PRESENT"} and state in {
                    "OPEN",
                    "ADDRESSED_AWAITING_REVIEW",
                    "INDEPENDENTLY_VERIFIED",
                }:
                    current["state"] = "OPEN"
                else:
                    raise FAL002Error("FORBIDDEN_TRANSITION", "invalid review finding transition")
                if SEVERITIES.index(payload["observed_severity"]) > SEVERITIES.index(current["current_severity"]):
                    current["current_severity"] = payload["observed_severity"]
                current["current_blocking"] = current["current_blocking"] or payload["observed_blocking"] or current["current_severity"] == "CRITICAL"
                current["latest_statement"] = payload["statement"]
                current["criterion_ids"] = payload["criterion_ids"]
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
    current_values = sorted(states.values(), key=lambda item: (item["finding_id"], item["occurrence"]))
    checkpoint = {
        "event_count": len(ordered),
        "finding_history_hash": H("fal002-finding-history-v1", ordered),
        "current_findings": current_values,
        "finding_ledger_hash": H("fal002-finding-ledger-v1", current_values),
    }
    return current_values, checkpoint


def pass_eligible(current_findings: list[dict[str, Any]], *, pending_decisions: bool, criteria_complete: bool) -> bool:
    if pending_decisions or not criteria_complete:
        return False
    return not any(item["state"] in UNRESOLVED_STATES and (item["current_blocking"] or item["current_severity"] == "CRITICAL") for item in current_findings)


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
    return _surface_schema(surface, include_defs=True)


def generate_schemas(output_root: Path, *, check: bool = False) -> tuple[GeneratedSchema, ...]:
    generated: list[GeneratedSchema] = []
    for surface in sorted(SURFACE_MODELS):
        path = output_root / SCHEMA_FILES[surface]
        raw = json.dumps(_schema_for(surface), ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
        if check:
            if not path.is_file() or path.read_bytes() != raw:
                raise FAL002Error("SCHEMA_MISMATCH", str(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        generated.append(GeneratedSchema(surface, path, HB(raw)))
    return tuple(generated)
# fmt: on
