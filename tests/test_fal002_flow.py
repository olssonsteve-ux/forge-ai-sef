from copy import deepcopy
from pathlib import Path

import pytest

from forge.fal002 import (
    correction_disposition,
    decisions_pending,
    evaluate_review,
    make_gate,
    publish_committed,
    resolve_decision,
    run_engineering_loop,
    transition,
)
from forge.fal002_inventory import inventory
from forge.fal002_io import (
    FAL002ExecutorAdapter,
    FAL002ReviewerAdapter,
    canonical_record_path,
    load_gate_chain,
    publish_create_only,
)
from forge.fal002_model import (
    COMMAND_IDS,
    HB,
    FAL002Error,
    H,
    decision_application,
    decision_binding,
    decision_identity,
    decision_requirement,
    empty_finding_checkpoint,
    seal_record,
    validate_evidence_binding,
    validate_record,
    validate_reviewer_run,
)

SERIES = "11111111-1111-4111-8111-111111111111"
STAMP = "2026-08-09T12:00:00.000000Z"
SHA = "0" * 64


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


def test_exact_inventory_transition_and_correction_ceiling():
    value = inventory(Path(__file__).parents[1])
    ready = transition(
        origin(), event="MARK_READY", created_at=STAMP, variant_kind="INVENTORY", variant=value
    )
    assert ready["state"] == "ready"
    correction = make_gate(
        series_id=SERIES,
        sequence=2,
        predecessor=ready["record_hash"],
        state="correction_required",
        actor="reviewer",
        event="REVIEW_CORRECTION",
        created_at=STAMP,
        frozen_hash="3" * 64,
        correction_count=2,
        variant_kind="INVENTORY",
        variant=value,
    )
    with pytest.raises(FAL002Error, match="CORRECTION_CEILING"):
        transition(
            correction,
            event="START_CORRECTION",
            created_at=STAMP,
            variant_kind="INVENTORY",
            variant=value,
        )


def test_malformed_run_record_rejected_exactly():
    malformed = {
        "schema_id": "fal002.run-record.v1",
        "schema_version": 1,
        "record_id": "not-a-uuid",
        "series_id": SERIES,
        "created_at": STAMP,
        "execution_id": 17,
        "ordinal": "not-an-int",
        "repository": {"unexpected": True},
        "runtime": {},
        "tools": [],
        "commands": [],
        "diff": {},
        "build": {},
        "payload_hash": SHA,
        "record_hash": SHA,
    }
    with pytest.raises(FAL002Error, match="MALFORMED_BOUNDARY"):
        validate_record(malformed)


def binding(run, content="PASS"):
    return {
        "criterion_id": "FAL2-CC-01",
        "evidence_kind": "TEST_RESULT",
        "source_surface": "fal002.run-record.v1",
        "source_record_id": run["record_id"],
        "locator": "/commands/13/classification",
        "assertion": "Test command passed.",
        "content_hash": H("fal002-json-content-v1", content),
        "provenance": {
            "authority": "COLLECTOR",
            "record_id": run["record_id"],
            "record_hash": run["record_hash"],
            "collector_id": "PYTEST",
        },
    }


def test_bare_and_fabricated_criterion_evidence_cannot_count():
    with pytest.raises(FAL002Error, match="MALFORMED_BOUNDARY"):
        validate_record(
            {
                "schema_id": "fal002.reviewer-exchange.v1",
                "criterion_evidence": [{"criterion_id": "FAL2-CC-01"}],
            }
        )
    fake = binding({"record_id": "run-0000-aaaaaaaaaaaa", "record_hash": "1" * 64})
    with pytest.raises(FAL002Error):
        validate_evidence_binding(fake, origin())


def test_pass_requires_resolver_even_for_structurally_complete_review(monkeypatch):
    review = {
        "result": {"outcome": "PASS", "criterion_evidence": [], "semantic_rationale": []},
        "packet": {"criterion_ids": ["FAL2-CC-01"]},
    }
    monkeypatch.setattr("forge.fal002.validate_record", lambda value: value)
    assert not evaluate_review(review, [], pending_decisions=False)
    assert COMMAND_IDS[7:12] == [
        "INVENTORY",
        "GIT-HEAD-FINAL",
        "GIT-STATUS",
        "GIT-DIFF",
        "GIT-NUMSTAT",
    ]


def _decision_chain(label="A"):
    semantic = {
        "domain": "SCOPE",
        "question": f"Approve {label}?",
        "allowed_choices": ["APPROVE", "REJECT"],
        "original_target": {
            "target_kind": "GATE",
            "origin_series_id": SERIES,
            "target_record_id": "gate-00000000",
            "target_semantic_hash": SHA,
        },
        "semantic_sources": [],
    }
    requirement = decision_requirement(
        {
            "semantic_input": semantic,
            "required_authority": "HUMAN",
            "originating_series_id": SERIES,
            "originating_gate_id": "gate-00000000",
            "originating_gate_hash": SHA,
            "created_at": STAMP,
        }
    )
    identity = decision_identity(semantic)
    pending_id = f"{identity}-pending-b0000"
    binding = decision_binding(
        {
            "decision_identity": identity,
            "decision_requirement_hash": requirement["decision_requirement_hash"],
            "binding_generation": 0,
            "binding_series_id": SERIES,
            "pending_card_record_id": pending_id,
            "pending_card_locator": f".forge/fal002/series/{SERIES}/decisions/{pending_id}.json",
            "pending_card_record_hash": SHA,
        }
    )
    pending = seal_record(
        {
            "schema_id": "fal002.human-decision.v1",
            "schema_version": 1,
            "record_id": pending_id,
            "series_id": SERIES,
            "created_at": STAMP,
            "decision_identity": identity,
            "binding_generation": 0,
            "decision_kind": "PENDING_CARD",
            "status": "PENDING",
            "owner": "human",
            "provenance": {"source": "test", "locator": label, "content_hash": SHA},
            "payload": {
                "decision_requirement_hash": requirement["decision_requirement_hash"],
                "binding_key": binding["binding_key"],
                "semantic_input": semantic,
            },
        }
    )
    binding = decision_binding({**binding, "pending_card_record_hash": pending["record_hash"]})
    resolution_input = {
        "decision_identity": identity,
        "answered_requirement_hash": requirement["decision_requirement_hash"],
        "answered_semantic_payload_hash": requirement["semantic_payload_hash"],
        "selected_choice": "APPROVE",
        "rationale": f"Approve decision {label}.",
        "human_owner": "human",
        "human_provenance": {"source": "test", "locator": label, "content_hash": SHA},
        "decided_at": STAMP,
    }
    presentation = {
        "answered_pending_card_record_id": pending["record_id"],
        "answered_pending_card_record_hash": pending["record_hash"],
        "answered_binding_generation": 0,
        "answered_binding_key": binding["binding_key"],
        "presented_at": STAMP,
    }
    presentation["presentation_evidence_hash"] = H("fal002-json-content-v1", presentation)
    resolution = seal_record(
        {
            "schema_id": "fal002.human-decision.v1",
            "schema_version": 1,
            "record_id": f"{identity}-resolution-b0000",
            "series_id": SERIES,
            "created_at": STAMP,
            "decision_identity": identity,
            "binding_generation": 0,
            "decision_kind": "RESOLUTION",
            "status": "ACCEPTED",
            "owner": "human",
            "provenance": {"source": "test", "locator": label, "content_hash": SHA},
            "payload": {
                "resolution_semantic_input": resolution_input,
                "resolution_semantic_hash": H("fal002-json-content-v1", resolution_input),
                "presentation_evidence": presentation,
            },
        }
    )
    application = decision_application(
        {
            "decision_identity": identity,
            "decision_requirement_hash": requirement["decision_requirement_hash"],
            "binding_generation": 0,
            "binding_key": binding["binding_key"],
            "pending_card_record_id": pending["record_id"],
            "pending_card_record_hash": pending["record_hash"],
            "resolution_record_id": resolution["record_id"],
            "resolution_locator": (
                f".forge/fal002/series/{SERIES}/decisions/{resolution['record_id']}.json"
            ),
            "resolution_record_hash": resolution["record_hash"],
            "resolution_semantic_hash": resolution["payload"]["resolution_semantic_hash"],
            "presentation_evidence_hash": presentation["presentation_evidence_hash"],
            "selected_choice": "APPROVE",
            "application_ordinal": 0,
        }
    )
    return requirement, binding, pending, resolution, application


def test_no_progress_and_online_offline_semantic_resolution():
    unresolved = [
        {
            "finding_id": "F-a",
            "occurrence": 0,
            "state": "OPEN",
            "current_blocking": True,
            "current_severity": "HIGH",
        }
    ]
    snapshot = {"diff_hash": SHA, "progress_evidence_hash": SHA}
    assert correction_disposition(snapshot, snapshot, unresolved, unresolved, 1) == "NONE"
    assert correction_disposition(snapshot, snapshot, unresolved, unresolved, 2) == "CEILING"

    requirement, binding, pending, resolution, application = _decision_chain()
    identity = requirement["decision_identity"]
    records = {
        binding["pending_card_locator"]: pending,
        application["resolution_locator"]: resolution,
    }
    online = resolve_decision(
        identity, [requirement], [binding], [application], records.__getitem__
    )
    offline = resolve_decision(
        identity,
        [requirement],
        [binding],
        [application],
        lambda locator: deepcopy(records)[locator],
    )
    assert online == offline
    other = _decision_chain("B")[3]
    cross_application = decision_application(
        {
            **{
                key: value
                for key, value in application.items()
                if key
                not in {
                    "application_key",
                    "resolution_record_id",
                    "resolution_locator",
                    "resolution_record_hash",
                    "resolution_semantic_hash",
                    "presentation_evidence_hash",
                    "selected_choice",
                }
            },
            "resolution_record_id": other["record_id"],
            "resolution_locator": (
                f".forge/fal002/series/{SERIES}/decisions/{other['record_id']}.json"
            ),
            "resolution_record_hash": other["record_hash"],
            "resolution_semantic_hash": other["payload"]["resolution_semantic_hash"],
            "presentation_evidence_hash": other["payload"]["presentation_evidence"][
                "presentation_evidence_hash"
            ],
            "selected_choice": other["payload"]["resolution_semantic_input"]["selected_choice"],
        }
    )
    records[cross_application["resolution_locator"]] = other
    with pytest.raises(FAL002Error, match="resolution application mismatch"):
        resolve_decision(
            identity, [requirement], [binding], [cross_application], records.__getitem__
        )


def test_persisted_decision_state_distinguishes_pending_and_applied(tmp_path):
    requirement, binding, pending, resolution, application = _decision_chain()
    for applied in (False, True):
        root = tmp_path / ("applied" if applied else "pending")
        root.mkdir()
        value = manifest()
        value["decision_requirements"] = [requirement]
        value["decision_bindings"] = [binding]
        value["decision_applications"] = [application] if applied else []
        gate = make_gate(
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
            variant=value,
        )
        publish_create_only(canonical_record_path(root, gate), gate)
        tip = publish_committed(
            root, gate, pending, created_at=STAMP, source_authority="FORGE_CORE", source_record=gate
        )
        if applied:
            publish_committed(
                root,
                tip,
                resolution,
                created_at=STAMP,
                source_authority="HUMAN_BOUNDARY",
                source_record=tip,
            )
        assert decisions_pending(root, load_gate_chain(root, SERIES))[0] is (not applied)


def _command(_root, command_id, *, timeout_seconds):
    index = COMMAND_IDS.index(command_id)
    parsed = {
        "GIT-ROOT": {"available": True, "root": "."},
        "PYTHON-VERSION": {"available": True, "implementation": "CPython", "version": "3.14.0"},
        "GIT-VERSION": {"available": True, "version": "2.50.0"},
        "PYTEST-VERSION": {"available": True, "version": "9.0.0"},
        "RUFF-VERSION": {"available": True, "version": "0.12.0"},
        "GIT-HEAD-BASELINE": {"available": True, "head": "a" * 40, "kind": "BASELINE"},
        "GIT-BRANCH": {"available": True, "branch": "main"},
        "INVENTORY": {
            "available": True,
            "inventory_hash": "b" * 64,
            "disposition": "PASS",
            "counts": {
                "modules": 4,
                "new_production_loc": 2999,
                "executor_adapters": 1,
                "reviewer_adapters": 1,
                "schema_surfaces": 5,
            },
        },
        "GIT-HEAD-FINAL": {"available": True, "head": "a" * 40, "kind": "FINAL"},
        "GIT-STATUS": {"available": True, "entries": [], "changed_paths": []},
        "GIT-DIFF": {"available": True, "redacted_content_hash": HB(b""), "byte_count": 0},
        "GIT-NUMSTAT": {"available": True, "entries": []},
        "SCHEMA-CHECK": {
            "available": True,
            "schemas": [
                {"schema_id": surface, "sha256": "c" * 64}
                for surface in [
                    "fal002.executor-exchange.v1",
                    "fal002.gate-record.v1",
                    "fal002.human-decision.v1",
                    "fal002.reviewer-exchange.v1",
                    "fal002.run-record.v1",
                ]
            ],
        },
        "PYTEST": {
            "available": True,
            "passed": 1,
            "failed": 0,
            "skipped": 0,
            "xfailed": 0,
            "xpassed": 0,
            "errors": 0,
            "warnings": 0,
            "duration_seconds_decimal": "0.1",
        },
        "RUFF-LINT": {"available": True, "status": "PASS"},
        "RUFF-FORMAT": {"available": True, "status": "PASS"},
        "FORGE-STATUS": {"available": True, "categories": []},
    }[command_id]
    return {
        "command_id": command_id,
        "phase": "preflight"
        if index < 5
        else "pre-execution"
        if index < 8
        else "post-executor"
        if index < 12
        else "verification",
        "argv": ["fake", command_id],
        "cwd": ".",
        "environment_keys": ["PATH", "PYTHONIOENCODING", "PYTHONUTF8", "SYSTEMROOT", "TEMP", "TMP"],
        "started_at": STAMP,
        "ended_at": STAMP,
        "exit_code": 0,
        "termination": "EXITED",
        "stdout_sha256": HB(b""),
        "stderr_sha256": HB(b""),
        "stdout_text": "",
        "stderr_text": "",
        "redaction_count": 0,
        "parser_version": 1,
        "parsed": parsed,
        "classification": "PASS",
    }


def _returned(exchange, result, execution_key):
    exchange["result"] = result
    observed = exchange[execution_key]["observed"]
    observed.update(
        {
            "termination": "RETURNED",
            "ended_at": STAMP,
            "output_hash": H("fal002-json-content-v1", result),
        }
    )
    return seal_record(
        {
            key: value
            for key, value in exchange.items()
            if key not in {"payload_hash", "record_hash"}
        }
    )


def _ready_runtime_root(tmp_path, value=None):
    value = deepcopy(value) if value is not None else manifest()
    value["offline_evidence"] = {
        "evidence_id": "4" * 64,
        "decision_identity": "D-offline",
        "decision_requirement_hash": "5" * 64,
        "binding_generation": 0,
        "binding_key": "6" * 64,
        "pending_card_record_id": "D-offline-pending-b0000",
        "pending_card_record_hash": "7" * 64,
        "resolution_record_id": "D-offline-resolution-b0000",
        "resolution_record_hash": "8" * 64,
        "resolution_locator": "decisions/offline.json",
        "resolution_semantic_hash": "9" * 64,
        "presentation_evidence_hash": "a" * 64,
        "locator": "/payload/resolution_semantic_input/selected_choice",
        "content_hash": "b" * 64,
        "collected_at": STAMP,
        "valid_until": "2026-08-10T12:00:00.000000Z",
        "command_policy_hash": "2" * 64,
    }
    gate0 = make_gate(
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
        variant=value,
    )
    publish_create_only(canonical_record_path(tmp_path, gate0), gate0)
    ready = transition(
        gate0,
        event="MARK_READY",
        created_at=STAMP,
        variant_kind="INVENTORY",
        variant=inventory(Path(__file__).parents[1]),
    )
    publish_create_only(canonical_record_path(tmp_path, ready), ready)
    return ready


def test_real_orchestrator_persists_executor_run_reviewer_and_gate(tmp_path):
    ready = _ready_runtime_root(tmp_path)

    executor = FAL002ExecutorAdapter(
        lambda exchange, **_: _returned(
            exchange, {"status": "COMPLETED", "changed_paths": [], "summary": "done"}, "invocation"
        )
    )

    def review_handler(exchange, **_):
        result = {
            "outcome": "PASS",
            "findings": [],
            "criterion_evidence": exchange["packet"]["evidence_index"],
            "semantic_rationale": [
                {"criterion_id": "FAL2-CC-01", "rationale": "Bound test evidence is relevant."}
            ],
        }
        returned = _returned(exchange, result, "reviewer_execution")
        returned["reviewer_execution"]["observed"]["process_id"] = 999999
        return seal_record(
            {
                key: value
                for key, value in returned.items()
                if key not in {"payload_hash", "record_hash"}
            }
        )

    result = run_engineering_loop(
        tmp_path,
        ready,
        executor,
        FAL002ReviewerAdapter(review_handler),
        created_at=STAMP,
        criterion_ids=["FAL2-CC-01"],
        command_runner=_command,
    )
    assert result["eligible"] is True
    assert all(
        canonical_record_path(tmp_path, result[key]).is_file()
        for key in ("executor_exchange", "run_record", "reviewer_exchange", "gate_record")
    )
    assert result["reviewer_exchange"]["reviewer_execution"]["observed"]["process_id"] != 999999
    chain = load_gate_chain(tmp_path, SERIES)
    assert sum(gate["payload"]["variant_kind"] == "PUBLICATION_INTENT" for gate in chain) == 3
    pending = _decision_chain()[2]
    for record in (
        pending,
        result["executor_exchange"],
        result["run_record"],
        result["reviewer_exchange"],
    ):
        bypass_root = tmp_path / record["schema_id"]
        bypass_root.mkdir()
        target = canonical_record_path(bypass_root, record)
        with pytest.raises(FAL002Error, match="PUBLICATION_INTENT"):
            publish_create_only(target, record)
        assert not target.exists()
    fabricated = deepcopy(result["reviewer_exchange"])
    fabricated["packet"]["run_record_hash"] = "f" * 64
    with pytest.raises(FAL002Error):
        validate_reviewer_run(fabricated, result["run_record"])


def test_orchestrator_uses_applied_decision_and_rejects_cross_decision(tmp_path):
    executor = FAL002ExecutorAdapter(
        lambda exchange, **_: _returned(
            exchange, {"status": "COMPLETED", "changed_paths": [], "summary": "done"}, "invocation"
        )
    )

    def pass_review(exchange, **_):
        return _returned(
            exchange,
            {
                "outcome": "PASS",
                "findings": [],
                "criterion_evidence": exchange["packet"]["evidence_index"],
                "semantic_rationale": [
                    {"criterion_id": "FAL2-CC-01", "rationale": "Evidence is relevant."}
                ],
            },
            "reviewer_execution",
        )

    reviewer = FAL002ReviewerAdapter(pass_review)
    requirement, binding, pending, resolution, application = _decision_chain("A")
    for mode in ("pending", "applied"):
        root = tmp_path / mode
        root.mkdir()
        value = manifest()
        value["decision_requirements"] = [requirement]
        value["decision_bindings"] = [binding]
        value["decision_applications"] = [application] if mode == "applied" else []
        ready = _ready_runtime_root(root, value)
        tip = publish_committed(
            root,
            ready,
            pending,
            created_at=STAMP,
            source_authority="FORGE_CORE",
            source_record=ready,
        )
        if mode == "applied":
            predecessor = tip
            tip = publish_committed(
                root,
                predecessor,
                resolution,
                created_at=STAMP,
                source_authority="HUMAN_BOUNDARY",
                source_record=predecessor,
            )
        result = run_engineering_loop(
            root,
            tip,
            executor,
            reviewer,
            created_at=STAMP,
            criterion_ids=["FAL2-CC-01"],
            command_runner=_command,
        )
        assert result["eligible"] is (mode == "applied")

    other_resolution = _decision_chain("B")[3]
    cross_application = decision_application(
        {
            **{key: value for key, value in application.items() if key != "application_key"},
            "resolution_record_id": other_resolution["record_id"],
            "resolution_locator": (
                f".forge/fal002/series/{SERIES}/decisions/{other_resolution['record_id']}.json"
            ),
            "resolution_record_hash": other_resolution["record_hash"],
            "resolution_semantic_hash": other_resolution["payload"]["resolution_semantic_hash"],
            "presentation_evidence_hash": other_resolution["payload"]["presentation_evidence"][
                "presentation_evidence_hash"
            ],
            "selected_choice": other_resolution["payload"]["resolution_semantic_input"][
                "selected_choice"
            ],
        }
    )
    root = tmp_path / "cross"
    root.mkdir()
    value = manifest()
    value["decision_requirements"] = [requirement]
    value["decision_bindings"] = [binding]
    value["decision_applications"] = [cross_application]
    ready = _ready_runtime_root(root, value)
    tip = publish_committed(
        root,
        ready,
        pending,
        created_at=STAMP,
        source_authority="FORGE_CORE",
        source_record=ready,
    )
    tip = publish_committed(
        root,
        tip,
        other_resolution,
        created_at=STAMP,
        source_authority="HUMAN_BOUNDARY",
        source_record=tip,
    )
    with pytest.raises(FAL002Error, match="resolution application mismatch"):
        run_engineering_loop(
            root,
            tip,
            executor,
            reviewer,
            created_at=STAMP,
            criterion_ids=["FAL2-CC-01"],
            command_runner=_command,
        )


def test_orchestrator_derives_no_progress_and_stops_before_retry(tmp_path):
    ready = _ready_runtime_root(tmp_path)
    executor = FAL002ExecutorAdapter(
        lambda exchange, **_: _returned(
            exchange,
            {"status": "COMPLETED", "changed_paths": [], "summary": "unchanged"},
            "invocation",
        )
    )

    def correction_review(exchange, **_):
        return _returned(
            exchange,
            {
                "outcome": "CORRECTION_REQUIRED",
                "findings": [],
                "criterion_evidence": [],
                "semantic_rationale": [],
            },
            "reviewer_execution",
        )

    reviewer = FAL002ReviewerAdapter(correction_review)
    first = run_engineering_loop(
        tmp_path,
        ready,
        executor,
        reviewer,
        created_at=STAMP,
        criterion_ids=["FAL2-CC-01"],
        command_runner=_command,
    )
    second = run_engineering_loop(
        tmp_path,
        first["gate_record"],
        executor,
        reviewer,
        created_at=STAMP,
        criterion_ids=["FAL2-CC-01"],
        command_runner=_command,
    )
    assert second["gate_record"]["payload"]["control"]["progress"] == "NONE"
    stopped = run_engineering_loop(
        tmp_path,
        second["gate_record"],
        executor,
        reviewer,
        created_at=STAMP,
        criterion_ids=["FAL2-CC-01"],
        command_runner=lambda *_args, **_kwargs: pytest.fail("no-progress retry executed"),
    )
    assert stopped["stop_reason"] == "NONE"
    assert stopped["gate_record"]["state"] == "blocked"
