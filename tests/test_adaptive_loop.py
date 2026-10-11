import json
from copy import deepcopy
from pathlib import Path

import pytest

from forge.adaptive_loop import (
    ContractError,
    FakeExecutor,
    FakeReviewer,
    StateStore,
    apply_review,
    assert_frozen,
    begin_run,
    collect_command,
    compile_prompt,
    create_run_record,
    decision_card,
    human_close,
    redact,
    request_human_decision,
    reviewer_packet,
    run_controlled_fixture,
    sha256,
    start_correction,
    transition,
    validate_changed_files,
    validate_manifest,
    validate_review,
    validate_schema_boundary,
    validate_successor,
)

ROOT = Path(__file__).parents[1]


@pytest.fixture
def manifest():
    return json.loads((ROOT / "fixtures/adaptive-loop-v1/gate.json").read_text(encoding="utf-8"))


def frozen(manifest):
    prompt, metadata = compile_prompt(manifest)
    return begin_run(manifest, metadata), prompt, metadata


def review(result, findings=None, coverage=None):
    value = {
        "schema_version": "forge-review-result/1.0",
        "result": result,
        "findings": findings or [],
        "criterion_coverage": coverage or [],
        "reviewer_identity": "fresh-read-only-reviewer-fixture",
        "execution_identity": "fake-executor",
        "packet_hash": "PACKET",
        "reviewer_execution": {
            "execution_id": "REV-RUN-FAL-DEMO-001",
            "adapter": "fixture-reviewer",
            "adapter_version": "1.0",
            "started_at": "2026-08-01T12:00:00Z",
            "finished_at": "2026-08-01T12:00:01Z",
            "repository": "forge-ai-sef",
            "baseline": "21d3802df3e0f5a51ea692327fda3995f8d73eb0",
            "read_only": True,
            "source": "orchestrator",
        },
    }
    if result == "PASS" and coverage:
        value["criterion_evidence"] = {}
        for item in coverage:
            artifact_id = "state-history" if item == "FAL-01" else "run-record"
            artifact = dummy_artifacts()[artifact_id]
            value["criterion_evidence"][item] = [
                {
                    "criterion_id": item,
                    "evidence_kind": artifact["kind"],
                    "artifact_id": artifact_id,
                    "pointer": "/content",
                    "assertion": "fixture assertion",
                    "content_hash": artifact["content_hash"],
                    "provenance": artifact["provenance"],
                }
            ]
    value["review_result_hash"] = sha256(value)
    return value


def dummy_artifacts():
    history = [{"event": "transition"}]
    record = {"provenance": {"commands": "collector"}}
    return {
        "state-history": {
            "kind": "transition_history",
            "content": history,
            "content_hash": sha256(history),
            "provenance": "authoritative-state-ledger",
        },
        "run-record": {
            "kind": "run_record",
            "content": record,
            "content_hash": sha256(record),
            "provenance": "deterministic-evidence-collector",
        },
    }


def finding(human=False):
    return {
        "id": "F-001",
        "criterion_id": "FAL-01",
        "severity": "high",
        "observation": "transition was not proved",
        "evidence_reference": "run:test",
        "claim_status": "not_supported",
        "minimum_remediation": "add transition evidence",
        "human_decision_required": human,
    }


def to_reviewing(manifest):
    value, _, _ = frozen(manifest)
    value = transition(value, "executing", "executor", "begin")
    value = transition(value, "evidence_ready", "collector", "collected")
    value = transition(value, "reviewing", "forge", "packet ready")
    value["run"]["review_packet_hash"] = "PACKET"
    value["run"]["review_record_hash"] = "RECORD"
    value["run"]["review_artifacts"] = dummy_artifacts()
    value["run"]["reviewer_execution"] = review("BLOCKED")["reviewer_execution"]
    return value


def review_bound(manifest):
    value = deepcopy(manifest)
    value["run"]["review_packet_hash"] = "PACKET"
    value["run"]["review_record_hash"] = "RECORD"
    value["run"]["review_artifacts"] = dummy_artifacts()
    value["run"]["reviewer_execution"] = review("BLOCKED")["reviewer_execution"]
    return value


def test_fixture_schema_validates(manifest):
    validate_manifest(manifest)


def test_required_field_is_enforced(manifest):
    del manifest["scope"]
    with pytest.raises(ContractError, match="required fields missing"):
        validate_manifest(manifest)


def test_process_level_is_enforced(manifest):
    manifest["process_level"] = "extreme"
    with pytest.raises(ContractError, match="process_level"):
        validate_manifest(manifest)


def test_local_risk_dimensions_are_complete(manifest):
    del manifest["risk"]["dimensions"]["uncertainty"]
    with pytest.raises(ContractError, match="dimensions"):
        validate_manifest(manifest)


def test_risk_override_requires_human_rationale(manifest):
    manifest["risk"]["human_override"] = True
    with pytest.raises(ContractError, match="rationale"):
        validate_manifest(manifest)


def test_ready_can_enter_executing(manifest):
    result = transition(manifest, "executing", "executor", "authorized")
    assert result["state"] == "executing"
    assert result["history"][0]["sequence"] == 1


def test_invalid_transition_is_rejected(manifest):
    with pytest.raises(ContractError, match="invalid transition"):
        transition(manifest, "accepted", "executor", "self approval")


def test_append_only_history_chain_is_validated(manifest):
    value = transition(manifest, "executing", "executor", "begin")
    value["history"][0]["sequence"] = 2
    with pytest.raises(ContractError, match="append-only"):
        validate_manifest(value)


def test_deterministic_prompt_and_hash(manifest):
    p1, m1 = compile_prompt(manifest)
    p2, m2 = compile_prompt(deepcopy(manifest))
    assert p1 == p2
    assert m1 == m2
    assert m1["prompt_hash"] == sha256(p1.encode())


def test_frozen_criteria_cannot_change(manifest):
    value, _, _ = frozen(manifest)
    value["criteria"][0]["text"] = "new requirement"
    with pytest.raises(ContractError, match="frozen contract"):
        assert_frozen(value)


def test_frozen_scope_cannot_change(manifest):
    value, _, _ = frozen(manifest)
    value["scope"].append("src/audio")
    with pytest.raises(ContractError, match="frozen contract"):
        assert_frozen(value)


@pytest.mark.parametrize("field", ["forbidden_operations", "command_policy", "decision_owners"])
def test_all_policy_inputs_are_frozen(manifest, field):
    value, _, _ = frozen(manifest)
    if isinstance(value[field], list):
        value[field].append("changed")
    else:
        value[field]["changed"] = True
    with pytest.raises(ContractError, match="frozen contract"):
        assert_frozen(value)


def test_allowed_file_is_accepted(manifest):
    validate_changed_files(manifest, ["forge/adaptive_loop.py"])


def test_forbidden_file_blocks_progression(manifest):
    with pytest.raises(ContractError, match="forbidden file"):
        validate_changed_files(manifest, ["src/AudioRecorder/App.cs"])


def test_parent_traversal_cannot_bypass_allowed_paths(manifest):
    with pytest.raises(ContractError, match="forbidden file"):
        validate_changed_files(manifest, ["forge/../src/AudioRecorder/App.cs"])


def test_evidence_provenance_is_present(manifest, tmp_path):
    command = collect_command(
        ["python", "-m", "pytest", str(ROOT / "fixtures/adaptive-loop-v1/demo_check.py"), "-q"],
        tmp_path,
    )
    record = create_run_record(
        manifest, [command], {"changed_files": [], "tests": command["derived_tests"]}
    )
    assert record["provenance"]["commands"] == "raw command result and exit code"
    assert record["record_hash"]


def test_missing_fields_are_marked_not_invented(manifest):
    record = create_run_record(manifest, [], {"changed_files": []})
    assert record["tests"] == "unknown"
    assert record["cost"] == "not available"


def test_false_green_test_claim_is_rejected(manifest):
    with pytest.raises(ContractError, match="lacks command evidence"):
        create_run_record(manifest, [], {"changed_files": [], "tests": {"status": "passed"}})


def test_fabricated_command_record_is_rejected(manifest):
    fake = {"command": ["echo", "test"], "exit_code": 0, "provenance": "subprocess.run"}
    fake["command_record_hash"] = sha256(fake)
    with pytest.raises(ContractError, match="lacks command evidence"):
        create_run_record(manifest, [fake], {"changed_files": [], "tests": {"status": "passed"}})


def test_secret_redaction():
    assert redact("token=abc123") == "[REDACTED]"
    assert "secret" not in redact({"x": "Bearer secret"})["x"].lower()
    assert redact({"password": "hunter2"})["password"] == "[REDACTED]"
    assert redact({"Authorization": "Basic abc"})["Authorization"] == "[REDACTED]"


def test_reviewer_packet_is_reproducible(manifest):
    value, _, _ = frozen(manifest)
    record = create_run_record(value, [], {"changed_files": []})
    one = reviewer_packet(value, record, "diff", [])
    two = reviewer_packet(value, record, "diff", [])
    assert one == two
    assert one["mode"] == "read_only_adversarial"


@pytest.mark.parametrize("result", ["CORRECTION_REQUIRED", "BLOCKED", "INCONCLUSIVE"])
def test_review_results_validate(manifest, result):
    validate_review(review(result, [finding()]), review_bound(manifest))


def test_pass_needs_complete_criterion_coverage(manifest):
    with pytest.raises(ContractError, match="complete criterion"):
        validate_review(review("PASS", coverage=["FAL-01"]), review_bound(manifest))


def test_pass_needs_specific_evidence_links(manifest):
    value = review("PASS", coverage=["FAL-01", "FAL-02"])
    value["criterion_evidence"] = {}
    value["review_result_hash"] = sha256(
        {key: item for key, item in value.items() if key != "review_result_hash"}
    )
    with pytest.raises(ContractError, match="evidence references"):
        validate_review(value, review_bound(manifest))


def test_executor_cannot_accept(manifest):
    value = to_reviewing(manifest)
    with pytest.raises(ContractError, match="actor executor"):
        transition(value, "accepted", "executor", "self approval")


def test_history_content_mutation_breaks_hash_chain(manifest):
    value = transition(manifest, "executing", "executor", "begin")
    value["history"][0]["reason"] = "rewritten"
    with pytest.raises(ContractError, match="event hash"):
        validate_manifest(value)


def test_retained_predecessor_rejects_history_truncation(manifest):
    previous = transition(manifest, "executing", "executor", "begin")
    current = deepcopy(previous)
    current["history"] = []
    current["state"] = "ready"
    current["previous_state"] = None
    current["run"]["history_head"] = "GENESIS"
    with pytest.raises(ContractError, match="truncated or replaced"):
        validate_successor(previous, current)


def test_retained_predecessor_rejects_correction_reset(manifest):
    previous = to_reviewing(manifest)
    previous = apply_review(previous, review("CORRECTION_REQUIRED", [finding()]))
    previous = start_correction(previous, ["F-001"], "old", "new")
    current = deepcopy(previous)
    current["correction_count"] = 0
    with pytest.raises(ContractError, match="cannot reset"):
        validate_successor(previous, current)


def test_pass_makes_gate_eligible_but_not_closed(manifest):
    value = to_reviewing(manifest)
    result = apply_review(value, review("PASS", coverage=["FAL-01", "FAL-02"]))
    assert result["state"] == "accepted"
    assert result["state"] != "closed"


def test_reviewer_requests_bounded_correction(manifest):
    result = apply_review(to_reviewing(manifest), review("CORRECTION_REQUIRED", [finding()]))
    assert result["state"] == "correction_required"


def test_human_finding_escalates(manifest):
    result = apply_review(to_reviewing(manifest), review("CORRECTION_REQUIRED", [finding(True)]))
    assert result["state"] == "awaiting_human"


@pytest.mark.parametrize("outcome", ["BLOCKED", "INCONCLUSIVE"])
def test_adverse_result_never_becomes_pass(manifest, outcome):
    result = apply_review(to_reviewing(manifest), review(outcome, [finding()]))
    assert result["state"] == "blocked"


def test_correction_one_starts_without_changing_contract(manifest):
    value = apply_review(to_reviewing(manifest), review("CORRECTION_REQUIRED", [finding()]))
    result = start_correction(value, ["F-001"], "old", "new")
    assert result["state"] == "executing"
    assert result["correction_count"] == 1
    assert_frozen(result)


def test_third_correction_is_stopped(manifest):
    value = apply_review(to_reviewing(manifest), review("CORRECTION_REQUIRED", [finding()]))
    value["correction_count"] = 2
    result = start_correction(value, ["F-001"], "old", "new")
    assert result["state"] == "blocked"


def test_new_run_id_does_not_reset_budget(manifest):
    value = apply_review(to_reviewing(manifest), review("CORRECTION_REQUIRED", [finding()]))
    value["correction_count"] = 2
    value["run"]["id"] = "RUN-NEW"
    result = start_correction(value, ["F-001"], "old", "new")
    assert result["state"] == "blocked"


def test_unchanged_diff_stops_as_no_progress(manifest):
    value = apply_review(to_reviewing(manifest), review("CORRECTION_REQUIRED", [finding()]))
    result = start_correction(value, ["F-001"], "same", "same")
    assert result["state"] == "blocked"
    assert "no progress" in result["history"][-1]["reason"]


def test_decision_card_has_no_silent_default():
    card = decision_card(
        "DC-001",
        "Accept residual risk?",
        "residual_risk",
        "Product Owner",
        [
            {"id": "accept", "consequence": "risk retained", "reversibility": "medium"},
            {"id": "reject", "consequence": "work blocked", "reversibility": "high"},
        ],
        "reject",
        "acceptance",
        "before acceptance",
    )
    assert card["status"] == "pending"
    assert "selected" not in card


def test_ready_gate_persists_decision_and_awaits_human(manifest):
    card = decision_card(
        "DC-002",
        "Choose scope?",
        "scope",
        "Product Owner",
        [
            {"id": "a", "consequence": "narrow", "reversibility": "high"},
            {"id": "b", "consequence": "broad", "reversibility": "low"},
        ],
        "a",
        "execution",
        "before execution",
    )
    result = request_human_decision(manifest, card)
    assert result["state"] == "awaiting_human"
    assert result["pending_decisions"][0]["decision_id"] == "DC-002"


def test_state_store_makes_successor_validation_mandatory(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(manifest)
    progressed = transition(manifest, "executing", "executor", "begin")
    store.update(progressed)
    reset = deepcopy(progressed)
    reset["correction_count"] = 0
    reset["history"] = []
    reset["state"] = "ready"
    reset["previous_state"] = None
    reset["run"]["history_head"] = "GENESIS"
    with pytest.raises(ContractError):
        store.update(reset)


def test_non_human_decision_type_is_rejected():
    with pytest.raises(ContractError):
        decision_card("D", "Q", "formatting", "Codex", [{"id": "a"}, {"id": "b"}], "a", "x", "now")


def test_command_collector_records_exit_code_and_partial_result(tmp_path):
    result = collect_command(
        ["python", "-c", "import sys; print('partial'); sys.exit(3)"], tmp_path
    )
    assert result["exit_code"] == 3
    assert "partial" in result["stdout"]
    assert result["provenance"] == "subprocess.run"


def test_command_timeout_is_explicit(tmp_path):
    result = collect_command(["python", "-c", "import time; time.sleep(1)"], tmp_path, timeout=0.01)
    assert result["status"] == "timeout"
    assert result["exit_code"] == "not available"


def test_command_allowlist_is_enforced(manifest, tmp_path):
    with pytest.raises(ContractError, match="not allowed"):
        collect_command(["git", "push"], tmp_path, command_policy=manifest["command_policy"])


def test_interrupted_run_can_be_reopened_only_through_policy(manifest):
    manifest["state"] = "awaiting_human"
    assert transition(manifest, "ready", "human", "resume approved")["state"] == "ready"


def test_fixture_preserves_unrelated_sibling_repository(manifest, tmp_path):
    sibling = tmp_path / "Audio-Recorder"
    sibling.mkdir()
    source = sibling / "recording.bin"
    source.write_bytes(b"unrelated user recording")
    before = {p.relative_to(sibling): p.read_bytes() for p in sibling.rglob("*") if p.is_file()}
    evidence_root = tmp_path / "forge-evidence"
    result = run_controlled_fixture(
        manifest,
        FakeExecutor({"changed_files": [], "diff": {"text": "", "hash": "fixture"}}),
        FakeReviewer([review("PASS", coverage=["FAL-01", "FAL-02"])]),
        evidence_root,
    )
    assert result["state"]["state"] == "accepted"
    assert list(evidence_root.rglob("*.json"))
    after = {p.relative_to(sibling): p.read_bytes() for p in sibling.rglob("*") if p.is_file()}
    assert after == before


def test_end_to_end_fixture_corrects_then_passes(manifest, tmp_path):
    correction = review("CORRECTION_REQUIRED", [finding()])
    passed = review("PASS", coverage=["FAL-01", "FAL-02"])
    executor = FakeExecutor(
        {"changed_files": [], "diff": {"text": "bounded material change", "hash": "fixture"}}
    )
    result = run_controlled_fixture(
        manifest, executor, FakeReviewer([correction, passed]), tmp_path
    )
    assert result["state"]["state"] == "accepted"
    assert result["state"]["correction_count"] == 1
    assert len(result["records"]) == 2
    assert [item["result"] for item in result["reviews"]] == ["CORRECTION_REQUIRED", "PASS"]


def accepted_manifest(manifest):
    return apply_review(to_reviewing(manifest), review("PASS", coverage=["FAL-01", "FAL-02"]))


def close_decision():
    return {
        "decision_id": "HD-CLOSE-001",
        "decision": "AUTHORIZE_CLOSE",
        "owner": "Human Product Owner",
        "provenance": "signed task decision",
        "gate_id": "GATE-FAL-001",
        "status": "accepted",
    }


def test_human_close_is_atomic_and_coherent(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    eligible = accepted_manifest(manifest)
    store.initialize(eligible)
    closed = human_close(store, close_decision())
    assert closed["state"] == closed["capability_status"] == "closed"
    assert closed["history"][-1]["decision_id"] == "HD-CLOSE-001"
    assert store.load() == closed


@pytest.mark.parametrize("actor", ["executor", "reviewer", "forge"])
def test_non_human_cannot_close(manifest, tmp_path, actor):
    store = StateStore(tmp_path / f"{actor}.json")
    store.initialize(accepted_manifest(manifest))
    with pytest.raises(ContractError, match="human authorization"):
        human_close(store, close_decision(), actor_role=actor)


def test_close_interruption_reopens_authoritative_result(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(accepted_manifest(manifest))
    with pytest.raises(OSError, match="injected"):
        human_close(store, close_decision(), fail_after_append=True)
    assert store.load()["state"] == "closed"


def test_repeated_close_is_rejected(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(accepted_manifest(manifest))
    human_close(store, close_decision())
    with pytest.raises(ContractError, match="already closed"):
        human_close(store, close_decision())


def test_ledger_detects_old_snapshot_tamper(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(manifest)
    store.update(transition(manifest, "executing", "executor", "begin"))
    path = store.ledger / "00000000.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    record["payload"]["project"] = "tampered"
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ContractError, match="payload hash"):
        store.load()


def test_ledger_detects_latest_snapshot_tamper(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(manifest)
    path = store.ledger / "00000000.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    record["record_hash"] = "0" * 64
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ContractError, match="record hash"):
        store.load()


def test_replaced_cache_cannot_replace_ledger_truth(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(manifest)
    store.path.write_text(json.dumps({"sequence": 0, "payload_hash": "fake"}), encoding="utf-8")
    with pytest.raises(ContractError, match="contradicts"):
        store.load()


def test_ledger_detects_gap_and_missing_predecessor(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(manifest)
    store.update(transition(manifest, "executing", "executor", "begin"))
    (store.ledger / "00000000.json").unlink()
    with pytest.raises(ContractError, match="sequence or predecessor"):
        store.load()


def test_ledger_rejects_overwrite(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(manifest)
    with pytest.raises(FileExistsError):
        store._append(manifest, None)


def test_ledger_detects_forked_series(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    store.initialize(manifest)
    original = (store.ledger / "00000000.json").read_text(encoding="utf-8")
    (store.ledger / "00000001-fork.json").write_text(original, encoding="utf-8")
    with pytest.raises(ContractError, match="sequence or predecessor"):
        store.load()


def test_ledger_preserves_blocked_and_correction_history(manifest, tmp_path):
    store = StateStore(tmp_path / "state.json")
    correction = to_reviewing(manifest)
    correction = apply_review(correction, review("CORRECTION_REQUIRED", [finding()]))
    store.initialize(correction)
    loaded = store.load()
    assert any(event["to"] == "correction_required" for event in loaded["history"])


def test_schema_rejects_unknown_nested_criterion_field(manifest):
    manifest["criteria"][0]["unknown"] = True
    with pytest.raises(ContractError, match="unknown fields"):
        validate_manifest(manifest)


def test_decision_schema_rejects_unknown_field():
    value = close_decision()
    value["unknown"] = True
    with pytest.raises(ContractError, match="unknown fields"):
        validate_schema_boundary(value, "forge-decision-record-v1.schema.json")


def test_evidence_pointer_must_resolve(manifest):
    value = review("PASS", coverage=["FAL-01", "FAL-02"])
    value["criterion_evidence"]["FAL-01"][0]["pointer"] = "/content/missing"
    value["review_result_hash"] = sha256(
        {key: item for key, item in value.items() if key != "review_result_hash"}
    )
    with pytest.raises(ContractError, match="cannot be resolved"):
        validate_review(value, review_bound(manifest))
