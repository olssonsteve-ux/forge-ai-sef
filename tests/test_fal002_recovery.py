from copy import deepcopy

import pytest

from forge.fal002 import make_gate, transition
from forge.fal002_inventory import inventory
from forge.fal002_io import (
    canonical_record_path,
    discover_recovery_root,
    load_record,
    publish_create_only,
    publish_staged,
    stage_committed_record,
)
from forge.fal002_model import (
    FAL002Error,
    H,
    decision_identity,
    decision_requirement,
    empty_finding_checkpoint,
    fold_finding_events,
    publication_slot,
    recovery_candidate_uuid,
    recovery_discovery_key,
    recovery_discovery_material,
    seal_record,
)

ORIGIN = "11111111-1111-4111-8111-111111111111"
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


def origin_gate(series=ORIGIN, corrections=2):
    return make_gate(
        series_id=series,
        sequence=0,
        predecessor=None,
        state="draft",
        actor="human",
        event="INITIALIZE",
        created_at=STAMP,
        frozen_hash="3" * 64,
        correction_count=corrections,
        variant_kind="MANIFEST",
        variant=manifest(),
    )


def recovery_root(predecessor, ordinal=0, checkpoint=None, pending=None):
    slot = publication_slot(
        {
            "origin_series_id": ORIGIN,
            "predecessor_series_id": predecessor["series_id"],
            "predecessor_gate_id": predecessor["record_id"],
            "predecessor_gate_hash": predecessor["record_hash"],
            "target_surface": "fal002.gate-record.v1",
            "target_record_id": "gate-00000001",
            "target_path": f".forge/fal002/series/{predecessor['series_id']}/gate/00000001.json",
            "reconstruction": "RECONSTRUCTABLE",
        }
    )
    material = recovery_discovery_material(slot)
    key = recovery_discovery_key(material)
    successor = recovery_candidate_uuid(key, ordinal)
    obstruction = {
        "origin_series_id": ORIGIN,
        "predecessor_series_id": predecessor["series_id"],
        "predecessor_gate_id": predecessor["record_id"],
        "predecessor_gate_hash": predecessor["record_hash"],
        "publication_slot": slot,
        "intended_record_hash": "4" * 64,
        "intended_file_hash": "5" * 64,
        "target_path": slot["target_path"],
        "obstruction_kind": "CONFLICTING_FILE",
        "path_object_kind": "REGULAR",
        "frozen_hash": "3" * 64,
        "observed_content_hash": "6" * 64,
    }
    value = {
        "origin_series_id": ORIGIN,
        "predecessor_series_id": predecessor["series_id"],
        "predecessor_gate_id": predecessor["record_id"],
        "predecessor_gate_hash": predecessor["record_hash"],
        "publication_slot": slot,
        "recovery_discovery_material": material,
        "recovery_discovery_key": key,
        "obstruction": obstruction,
        "recovery_condition_hash": H("fal002-recovery-condition-v1", obstruction),
        "successor_series_id": successor,
        "recovery_ordinal": ordinal,
        "predecessor_sealed": True,
        "retained_state": predecessor["state"],
        "scope_hash": SHA,
        "criteria_hash": "1" * 64,
        "allowed_paths_hash": "2" * 64,
        "command_policy_hash": "2" * 64,
        "frozen_hash": "3" * 64,
        "correction_count": predecessor["payload"]["correction_count"],
        "max_prior_ordinal": 0,
        "finding_checkpoint": checkpoint or empty_finding_checkpoint(),
        "pending_decisions": pending or [],
        "active_decision_bindings": [],
        "applied_decisions": [],
        "no_progress_history": [],
        "intended_decision_record_id": "D-recovery-pending-b0000",
        "intended_decision_record_hash": "7" * 64,
    }
    return make_gate(
        series_id=successor,
        sequence=0,
        predecessor=None,
        state="awaiting_human",
        actor="recovery",
        event="RECOVERY_SUCCESSOR",
        created_at=STAMP,
        frozen_hash="3" * 64,
        correction_count=value["correction_count"],
        variant_kind="RECOVERY_ROOT",
        variant=value,
    )


def evidence_binding(record_id="review-0000-aaaaaaaaaaaa", record_hash="8" * 64):
    return {
        "criterion_id": "FAL2-CC-06",
        "evidence_kind": "REVIEW_FINDING",
        "source_surface": "fal002.reviewer-exchange.v1",
        "source_record_id": record_id,
        "locator": "/result/findings/0",
        "assertion": "Finding observation.",
        "content_hash": "9" * 64,
        "provenance": {"authority": "REVIEWER", "record_id": record_id, "record_hash": record_hash},
    }


def event(ordinal, kind, payload, *, occurrence=0, previous=None, authority=None):
    value = {
        "event_ordinal": ordinal,
        "event_kind": kind,
        "finding_id": "F-aaaaaaaaaaaaaaaaaaaa",
        "finding_key": "a" * 64,
        "occurrence": occurrence,
        "created_at": STAMP,
        "source_authority": authority
        or ("REVIEWER" if kind == "REVIEW_OBSERVATION" else "CORRECTION_AGENT"),
        "source_record_id": f"source-{ordinal}",
        "source_record_hash": f"{ordinal + 1}" * 64,
        "payload": payload,
    }
    if previous is not None:
        value["previous_event_hash"] = previous
    digest = H("fal002-finding-observation-v1", value)
    return {"event_id": "FE-" + digest[:20], **value, "event_hash": digest}


def review_payload(observation, *, recurrence=None):
    value = {
        "observation": observation,
        "observed_severity": "HIGH",
        "observed_blocking": True,
        "statement": "defect",
        "criterion_ids": ["FAL2-CC-06"],
        "evidence_bindings": [evidence_binding()],
        "rationale": "fresh independent evidence",
    }
    if recurrence is not None:
        value["recurs_after_event_hash"] = recurrence
    return value


def test_recovery_n_seals_each_predecessor(tmp_path):
    predecessor = origin_gate()
    publish_create_only(canonical_record_path(tmp_path, predecessor), predecessor)
    roots = []
    for _ in range(3):
        root = recovery_root(predecessor)
        publish_create_only(canonical_record_path(tmp_path, root), root)
        assert (
            discover_recovery_root(
                tmp_path, root["payload"]["recovery_root"]["recovery_discovery_key"]
            )
            == root
        )
        ordinary_append = make_gate(
            series_id=predecessor["series_id"],
            sequence=predecessor["sequence"] + 1,
            predecessor=predecessor["record_hash"],
            state=predecessor["state"],
            actor="core",
            event="ORDINARY_APPEND",
            created_at=STAMP,
            frozen_hash=predecessor["payload"]["frozen_hash"],
            correction_count=predecessor["payload"]["correction_count"],
            variant_kind="INVENTORY",
            variant=inventory(__import__("pathlib").Path(__file__).parents[1]),
        )
        with pytest.raises(FAL002Error, match="sealed"):
            publish_create_only(canonical_record_path(tmp_path, ordinary_append), ordinary_append)
        roots.append(root)
        predecessor = root
    assert len({item["series_id"] for item in roots}) == 3


def test_wrong_predecessor_and_transient_probe_fail_closed(tmp_path, monkeypatch):
    predecessor = origin_gate()
    root = recovery_root(predecessor)
    raw = {
        key: deepcopy(value)
        for key, value in root.items()
        if key not in {"payload_hash", "record_hash"}
    }
    raw["payload"]["recovery_root"]["predecessor_gate_hash"] = "f" * 64
    with pytest.raises(FAL002Error):
        seal_record(raw)
    monkeypatch.setattr(
        "pathlib.Path.exists", lambda self: (_ for _ in ()).throw(OSError("transient"))
    )
    with pytest.raises(FAL002Error, match="transient"):
        discover_recovery_root(tmp_path, "a" * 64)


def pending_decision():
    semantic = {
        "domain": "RECOVERY",
        "question": "Resume?",
        "allowed_choices": ["AUTHORIZE_RECOVERY_RESUME", "ABANDON_LINEAGE"],
        "original_target": {
            "target_kind": "RECOVERY_ROOT",
            "origin_series_id": ORIGIN,
            "target_record_id": "gate-00000000",
            "target_semantic_hash": SHA,
        },
        "semantic_sources": [],
    }
    identity = decision_identity(semantic)
    return seal_record(
        {
            "schema_id": "fal002.human-decision.v1",
            "schema_version": 1,
            "record_id": f"{identity}-pending-b0000",
            "series_id": ORIGIN,
            "created_at": STAMP,
            "decision_identity": identity,
            "binding_generation": 0,
            "decision_kind": "PENDING_CARD",
            "status": "PENDING",
            "owner": "human",
            "provenance": {"source": "test", "locator": "authority", "content_hash": SHA},
            "payload": {
                "decision_requirement_hash": "1" * 64,
                "binding_key": "2" * 64,
                "semantic_input": semantic,
            },
        }
    )


def test_publication_requires_exact_intent_and_target(tmp_path):
    predecessor = origin_gate(corrections=0)
    publish_create_only(canonical_record_path(tmp_path, predecessor), predecessor)
    target = pending_decision()
    slot = publication_slot(
        {
            "origin_series_id": ORIGIN,
            "predecessor_series_id": ORIGIN,
            "predecessor_gate_id": predecessor["record_id"],
            "predecessor_gate_hash": predecessor["record_hash"],
            "target_surface": target["schema_id"],
            "target_record_id": target["record_id"],
            "target_path": f".forge/fal002/series/{ORIGIN}/decisions/{target['record_id']}.json",
            "reconstruction": "COMMITTED",
        }
    )
    staged, attempt, file_hash = stage_committed_record(tmp_path, ORIGIN, slot["slot_id"], target)
    intent = {
        "slot": slot,
        "retained_state": "draft",
        "intended_record_hash": target["record_hash"],
        "intended_file_hash": file_hash,
        "stage_locator": staged.relative_to(tmp_path).as_posix(),
        "stage_attempt": attempt,
        "stage_file_hash": file_hash,
        "source_authority": "FORGE_CORE",
        "source_record_id": predecessor["record_id"],
        "source_record_hash": predecessor["record_hash"],
    }
    intent["intent_commitment_hash"] = H("fal002-publication-intent-v1", intent)
    intent_gate = transition(
        predecessor,
        event="PUBLICATION_INTENT_COMMITTED",
        created_at=STAMP,
        variant_kind="PUBLICATION_INTENT",
        variant=intent,
    )
    publish_create_only(canonical_record_path(tmp_path, intent_gate), intent_gate)
    assert publish_staged(tmp_path, staged, intent_gate, target) == "CREATED"
    staged.write_bytes(b"corrupt\n")
    with pytest.raises(FAL002Error, match="HASH_MISMATCH"):
        publish_staged(tmp_path, staged, intent_gate, target)


def test_exact_remediation_then_close_and_recurrence():
    first = event(0, "REVIEW_OBSERVATION", review_payload("NEW"))
    remediation = {
        "finding_id": first["finding_id"],
        "finding_key": first["finding_key"],
        "occurrence": 0,
        "correction_objective_id": "CORR-1",
        "authorization_decision_id": "HD-1",
        "authorization_decision_hash": "1" * 64,
        "corrected_artifact_path": "forge/fal002.py",
        "corrected_locator": "function",
        "corrected_content_hash": "2" * 64,
        "correction_baseline_head": "3" * 40,
        "correction_result_head": "4" * 40,
        "correction_actor": "CORRECTION_AGENT",
        "claim": "ADDRESSED_AWAITING_REVIEW",
        "created_at": STAMP,
        "source_run_id": "run-0000-aaaaaaaaaaaa",
        "source_run_hash": "5" * 64,
    }
    remediation["remediation_evidence_hash"] = H("fal002-remediation-evidence-v1", remediation)
    claim = event(
        1, "REMEDIATION_CLAIM", {"remediation": remediation}, previous=first["event_hash"]
    )
    absent = event(
        2,
        "REVIEW_OBSERVATION",
        review_payload("ABSENT_AFTER_CORRECTION"),
        previous=claim["event_hash"],
    )
    close = event(
        3,
        "HUMAN_DISPOSITION",
        {
            "disposition": "CLOSE_VERIFIED",
            "rationale": "human closure",
            "decision_application_key": "6" * 64,
        },
        previous=absent["event_hash"],
        authority="HUMAN",
    )
    recurrence = event(
        4, "REVIEW_OBSERVATION", review_payload("NEW", recurrence=close["event_hash"]), occurrence=1
    )
    current, checkpoint = fold_finding_events([first, claim, absent, close, recurrence])
    assert [item["state"] for item in current] == ["CLOSED", "OPEN"]
    assert checkpoint["event_count"] == 5
    bad = deepcopy(recurrence)
    bad["previous_event_hash"] = close["event_hash"]
    digest = H(
        "fal002-finding-observation-v1",
        {key: value for key, value in bad.items() if key not in {"event_id", "event_hash"}},
    )
    bad.update({"event_id": "FE-" + digest[:20], "event_hash": digest})
    with pytest.raises(FAL002Error, match="predecessor"):
        fold_finding_events([first, claim, absent, close, bad])


@pytest.mark.parametrize(
    ("initial", "human", "reviewer", "expected"),
    [
        ("MEDIUM", None, "HIGH", "HIGH"),
        ("HIGH", None, "MEDIUM", "HIGH"),
        ("HIGH", "MEDIUM", "HIGH", "HIGH"),
        ("HIGH", "MEDIUM", "LOW", "MEDIUM"),
        ("HIGH", None, "HIGH", "HIGH"),
    ],
)
def test_full_severity_epoch_matrix(initial, human, reviewer, expected):
    payload = review_payload("NEW")
    payload["observed_severity"] = initial
    events = [event(0, "REVIEW_OBSERVATION", payload)]
    if human:
        events.append(
            event(
                1,
                "HUMAN_RECLASSIFICATION",
                {
                    "new_effective_severity": human,
                    "new_blocking": False,
                    "rationale": "human epoch",
                    "decision_application_key": "d" * 64,
                },
                previous=events[-1]["event_hash"],
                authority="HUMAN",
            )
        )
    next_payload = review_payload("STILL_PRESENT")
    next_payload["observed_severity"] = reviewer
    events.append(
        event(len(events), "REVIEW_OBSERVATION", next_payload, previous=events[-1]["event_hash"])
    )
    current, _ = fold_finding_events(events)
    assert current[0]["current_severity"] == expected


def test_restart_recovery_carries_decisions_and_findings_together(tmp_path):
    predecessor = origin_gate()
    first = event(0, "REVIEW_OBSERVATION", review_payload("NEW"))
    _, checkpoint = fold_finding_events([first])
    semantic = {
        "domain": "RECOVERY",
        "question": "Resume recovered lineage?",
        "allowed_choices": ["AUTHORIZE_RECOVERY_RESUME", "ABANDON_LINEAGE"],
        "original_target": {
            "target_kind": "RECOVERY_ROOT",
            "origin_series_id": ORIGIN,
            "target_record_id": predecessor["record_id"],
            "target_semantic_hash": predecessor["record_hash"],
        },
        "semantic_sources": [],
    }
    requirement = decision_requirement(
        {
            "semantic_input": semantic,
            "required_authority": "HUMAN",
            "originating_series_id": ORIGIN,
            "originating_gate_id": predecessor["record_id"],
            "originating_gate_hash": predecessor["record_hash"],
            "created_at": STAMP,
        }
    )
    root = recovery_root(predecessor, checkpoint=checkpoint, pending=[requirement])
    publish_create_only(canonical_record_path(tmp_path, predecessor), predecessor)
    path = canonical_record_path(tmp_path, root)
    publish_create_only(path, root)
    del root, checkpoint, requirement
    recovered = load_record(path)["payload"]["recovery_root"]
    assert recovered["finding_checkpoint"]["current_findings"][0]["state"] == "OPEN"
    assert recovered["pending_decisions"][0]["semantic_input"]["domain"] == "RECOVERY"
    assert recovered["correction_count"] == 2
