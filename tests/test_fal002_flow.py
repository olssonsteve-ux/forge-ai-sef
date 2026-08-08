from copy import deepcopy

import pytest

from forge.fal002 import (
    correction_disposition,
    evaluate_review,
    human_close,
    make_gate,
    resolve_decision,
    transition,
)
from forge.fal002_io import invoke_executor, invoke_reviewer
from forge.fal002_model import (
    FAL002Error,
    H,
    decision_application,
    decision_binding,
    decision_requirement,
    empty_finding_checkpoint,
    seal_record,
)

SERIES = "11111111-1111-4111-8111-111111111111"
STAMP = "2026-08-09T12:00:00.000000Z"
SHA = "0" * 64
CHECKS = [
    "MANIFEST_ROLE_DISTINCT",
    "PRINCIPAL_DISTINCT",
    "ADAPTER_ENTRYPOINT_DISTINCT",
    "GRANT_MATCH",
    "CONTEXT_FRESH",
    "PACKET_MINIMAL",
    "NO_WRITE_CALLBACK",
]


def manifest():
    return {
        "scope_hash": SHA,
        "criteria_hash": "1" * 64,
        "allowed_paths": ["forge/fal002.py"],
        "command_policy_hash": "2" * 64,
        "executor_principal_id": "executor",
        "reviewer_principal_id": "reviewer",
        "executor_adapter_id": "executor-adapter",
        "reviewer_adapter_id": "reviewer-adapter",
        "decision_requirements": [],
        "decision_bindings": [],
        "decision_applications": [],
        "finding_checkpoint": empty_finding_checkpoint(),
    }


def origin():
    return make_gate(
        series_id=SERIES,
        sequence=0,
        predecessor=None,
        state="draft",
        actor="human",
        event="INITIALIZE",
        created_at=STAMP,
        frozen_hash="3" * 64,
        correction_count=0,
        variant_kind="MANIFEST",
        variant=manifest(),
    )


def grant(role):
    return {"role": role}


def observed():
    return {"termination": "RETURNED"}


def executor_exchange(result=None):
    execution_id = "exec-0-123456789abc"
    return seal_record(
        {
            "schema_id": "fal002.executor-exchange.v1",
            "schema_version": 1,
            "record_id": execution_id,
            "series_id": SERIES,
            "created_at": STAMP,
            "run_id": "run-0-123456789abc",
            "ordinal": 0,
            "request": {
                "execution_id": execution_id,
                "frozen_hash": "3" * 64,
                "scope": ["forge"],
                "criteria": ["FAL2-CC-01"],
                "allowed_paths": ["forge/fal002.py"],
                "command_ids": ["PYTEST"],
                "correction_count": 0,
                "work_packet_hash": "4" * 64,
                "request_kind": "INITIAL",
            },
            "result": result,
            "invocation": {"grant": grant("EXECUTOR"), "observed": observed()},
        }
    )


def reviewer_exchange(outcome="PASS", findings=None):
    result = {
        "outcome": outcome,
        "findings": findings or [],
        "criterion_evidence": [{"criterion_id": "FAL2-CC-01"}],
        "semantic_rationale": [{"criterion_id": "FAL2-CC-01", "rationale": "literal evidence"}],
    }
    return seal_record(
        {
            "schema_id": "fal002.reviewer-exchange.v1",
            "schema_version": 1,
            "record_id": "review-0-123456789abc",
            "series_id": SERIES,
            "created_at": STAMP,
            "run_id": "run-0-123456789abc",
            "ordinal": 0,
            "packet": {
                "frozen_hash": "3" * 64,
                "run_record_id": "run-0-123456789abc",
                "run_record_hash": "5" * 64,
                "criterion_ids": ["FAL2-CC-01"],
                "evidence_index": [{"criterion_id": "FAL2-CC-01"}],
                "instructions_hash": "6" * 64,
            },
            "result": result,
            "reviewer_execution": {
                "grant": grant("REVIEWER"),
                "observed": observed(),
                "fresh_context_verified": True,
                "read_only_packet_verified": True,
                "separation_checks": CHECKS,
            },
        }
    )


def closure_decision(accepted_gate):
    return seal_record(
        {
            "schema_id": "fal002.human-decision.v1",
            "schema_version": 1,
            "record_id": "HD-CLOSE-001",
            "series_id": SERIES,
            "created_at": STAMP,
            "decision_identity": "D-close",
            "binding_generation": 0,
            "decision_kind": "CLOSURE",
            "status": "ACCEPTED",
            "owner": "human",
            "provenance": {"source": "human", "locator": "task", "content_hash": SHA},
            "payload": {
                "eligible_gate_id": accepted_gate["record_id"],
                "eligible_gate_hash": accepted_gate["record_hash"],
                "review_id": "review-0-123456789abc",
                "review_hash": "7" * 64,
                "finding_ledger_hash": empty_finding_checkpoint()["finding_ledger_hash"],
            },
        }
    )


def test_state_flow_and_correction_ceiling_survive_series_identity():
    gate0 = origin()
    ready = transition(
        gate0, event="MARK_READY", created_at=STAMP, variant_kind="INVENTORY", variant={}
    )
    executing = transition(
        ready, event="START_EXECUTION", created_at=STAMP, variant_kind="EXECUTION", variant={}
    )
    evidence = transition(
        executing, event="COLLECT_COMPLETE", created_at=STAMP, variant_kind="EVIDENCE", variant={}
    )
    reviewing = transition(
        evidence, event="START_REVIEW", created_at=STAMP, variant_kind="REVIEW", variant={}
    )
    correction = transition(
        reviewing,
        event="REVIEW_CORRECTION",
        created_at=STAMP,
        variant_kind="CONTROL",
        variant={
            "ordinal": 0,
            "correction_count": 0,
            "diff_hash": SHA,
            "evidence_hash": SHA,
            "finding_ids": [],
            "progress": "MATERIAL",
            "decision_requirements": [],
            "decision_bindings": [],
            "decision_applications": [],
            "finding_events": [],
            "finding_checkpoint": empty_finding_checkpoint(),
        },
    )
    first = transition(
        correction, event="START_CORRECTION", created_at=STAMP, variant_kind="EXECUTION", variant={}
    )
    assert first["payload"]["correction_count"] == 1
    first["state"] = "correction_required"
    first = seal_record(
        {key: value for key, value in first.items() if key not in {"payload_hash", "record_hash"}}
    )
    second = transition(
        first, event="START_CORRECTION", created_at=STAMP, variant_kind="EXECUTION", variant={}
    )
    second["state"] = "correction_required"
    second = seal_record(
        {key: value for key, value in second.items() if key not in {"payload_hash", "record_hash"}}
    )
    with pytest.raises(FAL002Error, match="CORRECTION_CEILING"):
        transition(
            second, event="START_CORRECTION", created_at=STAMP, variant_kind="EXECUTION", variant={}
        )


def test_adapters_can_change_only_authorized_result_fields():
    class Executor:
        def execute(self, exchange, *, timeout_seconds):
            exchange["result"] = {"status": "COMPLETED", "changed_paths": [], "summary": "done"}
            return seal_record(
                {
                    key: value
                    for key, value in exchange.items()
                    if key not in {"payload_hash", "record_hash"}
                }
            )

    output = invoke_executor(Executor(), executor_exchange(), timeout_seconds=1)
    assert output["result"]["status"] == "COMPLETED"

    class BadExecutor:
        def execute(self, exchange, *, timeout_seconds):
            exchange["run_id"] = "run-altered"
            exchange["result"] = {"status": "COMPLETED", "changed_paths": [], "summary": "bad"}
            return seal_record(
                {
                    key: value
                    for key, value in exchange.items()
                    if key not in {"payload_hash", "record_hash"}
                }
            )

    with pytest.raises(FAL002Error, match="AUTHORITY_CONFLICT"):
        invoke_executor(BadExecutor(), executor_exchange(), timeout_seconds=1)


def test_reviewer_pass_is_not_default_and_blockers_deny_eligibility():
    review = reviewer_exchange()
    assert evaluate_review(review, [], pending_decisions=False)
    assert not evaluate_review(review, [], pending_decisions=True)
    addressed = {
        "state": "ADDRESSED_AWAITING_REVIEW",
        "current_blocking": True,
        "current_severity": "HIGH",
    }
    assert not evaluate_review(review, [addressed], pending_decisions=False)
    blocked = reviewer_exchange("BLOCKED")
    assert not evaluate_review(blocked, [], pending_decisions=False)

    class Reviewer:
        def review(self, exchange, *, timeout_seconds):
            return exchange

    assert invoke_reviewer(Reviewer(), review, timeout_seconds=1)["result"]["outcome"] == "PASS"


def test_only_human_closure_record_can_close():
    review_gate = make_gate(
        series_id=SERIES,
        sequence=1,
        predecessor=origin()["record_hash"],
        state="reviewing",
        actor="core",
        event="START_REVIEW",
        created_at=STAMP,
        frozen_hash="3" * 64,
        correction_count=0,
        variant_kind="REVIEW",
        variant={},
    )
    accepted = transition(
        review_gate,
        event="REVIEW_PASS",
        created_at=STAMP,
        variant_kind="ELIGIBILITY",
        variant={
            "review_id": "review-0-123456789abc",
            "review_hash": "7" * 64,
            "criterion_ids": ["FAL2-CC-01"],
            "finding_ids": [],
            "eligible": True,
        },
    )
    closed = human_close(accepted, closure_decision(accepted), created_at=STAMP)
    assert closed["state"] == "closed"


def test_no_progress_requires_resolution_not_remediation_only():
    prior = [
        {
            "finding_id": "F-1",
            "occurrence": 0,
            "state": "OPEN",
            "current_blocking": True,
            "current_severity": "HIGH",
        }
    ]
    remediated = [{**prior[0], "state": "ADDRESSED_AWAITING_REVIEW"}]
    before = {"diff_hash": SHA, "progress_evidence_hash": "1" * 64}
    after = {"diff_hash": "2" * 64, "progress_evidence_hash": "3" * 64}
    assert correction_disposition(before, after, prior, remediated, 0) == "NONE"
    verified = [{**prior[0], "state": "INDEPENDENTLY_VERIFIED"}]
    assert correction_disposition(before, after, prior, verified, 0) == "MATERIAL"
    assert correction_disposition(before, after, prior, verified, 2) == "CEILING"


def test_decision_application_and_semantic_relocation_use_current_binding():
    requirement = decision_requirement(
        {
            "semantic_input": {
                "domain": "OFFLINE_EXECUTION",
                "question": "Authorize offline execution?",
                "allowed_choices": ["AUTHORIZE_OFFLINE", "DECLINE"],
                "original_target": {
                    "target_kind": "SERIES_INTENT",
                    "origin_series_id": SERIES,
                    "target_record_id": "gate-00000000",
                    "target_semantic_hash": SHA,
                },
                "semantic_sources": [],
            },
            "required_authority": "HUMAN",
            "originating_series_id": SERIES,
            "originating_gate_id": "gate-00000000",
            "originating_gate_hash": SHA,
            "created_at": STAMP,
        }
    )
    decision_id = requirement["decision_identity"]
    pending_locator = f".forge/fal002/series/{SERIES}/decisions/{decision_id}-pending-b0000.json"
    pending = seal_record(
        {
            "schema_id": "fal002.human-decision.v1",
            "schema_version": 1,
            "record_id": f"{decision_id}-pending-b0000",
            "series_id": SERIES,
            "created_at": STAMP,
            "decision_identity": decision_id,
            "binding_generation": 0,
            "decision_kind": "PENDING_CARD",
            "status": "PENDING",
            "owner": "human",
            "provenance": {"source": "core", "locator": "gate", "content_hash": SHA},
            "payload": {
                "decision_requirement_hash": requirement["decision_requirement_hash"],
                "binding_key": "0" * 64,
                "semantic_input": requirement["semantic_input"],
            },
        }
    )
    binding = decision_binding(
        {
            "decision_identity": decision_id,
            "decision_requirement_hash": requirement["decision_requirement_hash"],
            "binding_generation": 0,
            "binding_series_id": SERIES,
            "pending_card_record_id": pending["record_id"],
            "pending_card_locator": pending_locator,
            "pending_card_record_hash": pending["record_hash"],
            "previous_binding_key": None,
            "obstruction_evidence_hash": None,
        }
    )
    pending["payload"]["binding_key"] = binding["binding_key"]
    pending = seal_record(
        {key: value for key, value in pending.items() if key not in {"payload_hash", "record_hash"}}
    )
    binding = decision_binding({**binding, "pending_card_record_hash": pending["record_hash"]})
    semantic_input = {
        "decision_identity": decision_id,
        "answered_requirement_hash": requirement["decision_requirement_hash"],
        "answered_semantic_payload_hash": requirement["semantic_payload_hash"],
        "selected_choice": "AUTHORIZE_OFFLINE",
        "rationale": "authorized",
        "human_owner": "human",
        "human_provenance": {"source": "task", "locator": "decision", "content_hash": SHA},
        "decided_at": STAMP,
    }
    semantic_hash = H("fal002-json-content-v1", semantic_input)
    resolution_locator = (
        f".forge/fal002/series/{SERIES}/decisions/{decision_id}-resolution-b0000.json"
    )
    resolution = seal_record(
        {
            "schema_id": "fal002.human-decision.v1",
            "schema_version": 1,
            "record_id": f"{decision_id}-resolution-b0000",
            "series_id": SERIES,
            "created_at": STAMP,
            "decision_identity": decision_id,
            "binding_generation": 0,
            "decision_kind": "RESOLUTION",
            "status": "ACCEPTED",
            "owner": "human",
            "provenance": {"source": "task", "locator": "decision", "content_hash": SHA},
            "payload": {
                "resolution_semantic_input": semantic_input,
                "resolution_semantic_hash": semantic_hash,
                "presentation_evidence": {"presentation_evidence_hash": "9" * 64},
            },
        }
    )
    application = decision_application(
        {
            "decision_identity": decision_id,
            "decision_requirement_hash": requirement["decision_requirement_hash"],
            "binding_generation": 0,
            "binding_key": binding["binding_key"],
            "pending_card_record_id": pending["record_id"],
            "pending_card_record_hash": pending["record_hash"],
            "resolution_record_id": resolution["record_id"],
            "resolution_locator": resolution_locator,
            "resolution_record_hash": resolution["record_hash"],
            "resolution_semantic_hash": semantic_hash,
            "presentation_evidence_hash": "9" * 64,
            "selected_choice": "AUTHORIZE_OFFLINE",
            "application_ordinal": 0,
            "previous_application_key": None,
        }
    )
    records = {pending_locator: pending, resolution_locator: resolution}
    status, applied = resolve_decision(
        decision_id, [requirement], [binding], [application], records.__getitem__
    )
    assert status == "ACCEPTED"
    assert applied["payload"]["resolution_semantic_hash"] == semantic_hash

    relocated = deepcopy(resolution)
    relocated["record_id"] = f"{decision_id}-resolution-b0001"
    relocated["binding_generation"] = 1
    relocated = seal_record(
        {
            key: value
            for key, value in relocated.items()
            if key not in {"payload_hash", "record_hash"}
        }
    )
    assert relocated["payload"]["resolution_semantic_hash"] == semantic_hash
    stale = decision_application(
        {
            **{key: value for key, value in application.items() if key != "application_key"},
            "binding_key": "f" * 64,
        }
    )
    with pytest.raises(FAL002Error, match="STALE_RECORD"):
        resolve_decision(decision_id, [requirement], [binding], [stale], records.__getitem__)
