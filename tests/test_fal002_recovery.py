from copy import deepcopy

import pytest

from forge.fal002 import make_gate
from forge.fal002_io import (
    canonical_record_path,
    discover_recovery_root,
    load_gate_chain,
    publish_create_only,
    stage_committed_record,
)
from forge.fal002_model import (
    FAL002Error,
    H,
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


def origin_gate():
    return make_gate(
        series_id=ORIGIN,
        sequence=0,
        predecessor=None,
        state="draft",
        actor="human",
        event="INITIALIZE",
        created_at=STAMP,
        frozen_hash="3" * 64,
        correction_count=2,
        variant_kind="MANIFEST",
        variant=manifest(),
    )


def slot(predecessor_series, predecessor_hash, suffix):
    return publication_slot(
        {
            "origin_series_id": ORIGIN,
            "predecessor_series_id": predecessor_series,
            "predecessor_gate_id": "gate-00000000",
            "predecessor_gate_hash": predecessor_hash,
            "target_surface": "fal002.gate-record.v1",
            "target_record_id": "gate-00000001",
            "target_path": f".forge/fal002/series/{predecessor_series}/gate/00000001.json",
            "reconstruction": "RECONSTRUCTABLE",
        }
    )


def recovery_root(predecessor_series, predecessor_hash, suffix, ordinal=0):
    publication = slot(predecessor_series, predecessor_hash, suffix)
    material = recovery_discovery_material(publication)
    key = recovery_discovery_key(material)
    successor = recovery_candidate_uuid(key, ordinal)
    recovery = {
        "origin_series_id": ORIGIN,
        "predecessor_series_id": predecessor_series,
        "predecessor_gate_id": "gate-00000000",
        "predecessor_gate_hash": predecessor_hash,
        "publication_slot": publication,
        "recovery_discovery_material": material,
        "recovery_discovery_key": key,
        "obstruction": {"kind": "CONFLICTING_FILE", "suffix": suffix},
        "recovery_condition_hash": H("fal002-recovery-condition-v1", {"suffix": suffix}),
        "successor_series_id": successor,
        "recovery_ordinal": ordinal,
        "predecessor_sealed": True,
        "retained_state": "draft",
        "scope_hash": SHA,
        "criteria_hash": "1" * 64,
        "allowed_paths_hash": "2" * 64,
        "command_policy_hash": "3" * 64,
        "frozen_hash": "3" * 64,
        "correction_count": 2,
        "max_prior_ordinal": 4,
        "finding_checkpoint": empty_finding_checkpoint(),
        "pending_decisions": [],
        "active_decision_bindings": [],
        "applied_decisions": [],
        "no_progress_history": [{"diff_hash": SHA}],
        "intended_decision_record_id": "D-recovery-pending-b0000",
        "intended_decision_record_hash": "4" * 64,
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
        correction_count=2,
        variant_kind="RECOVERY_ROOT",
        variant=recovery,
    )


def finding_event(ordinal, kind, payload, previous=None):
    event = {
        "event_ordinal": ordinal,
        "event_kind": kind,
        "finding_id": "F-aaaaaaaaaaaaaaaaaaaa",
        "finding_key": "a" * 64,
        "occurrence": 0,
        "created_at": STAMP,
        "source_authority": "REVIEWER" if kind == "REVIEW_OBSERVATION" else "CORRECTION_AGENT",
        "source_record_id": f"source-{ordinal}",
        "source_record_hash": str(ordinal) * 64,
        "previous_event_hash": previous,
        "payload": payload,
    }
    event_hash = H("fal002-finding-observation-v1", event)
    return {"event_id": "FE-" + event_hash[:20], **event, "event_hash": event_hash}


def test_create_only_create_adopt_and_conflict(tmp_path):
    gate = origin_gate()
    path = canonical_record_path(tmp_path, gate)
    assert publish_create_only(path, gate) == "CREATED"
    original = path.read_bytes()
    assert publish_create_only(path, gate) == "ADOPTED"
    conflicting = deepcopy(gate)
    conflicting["created_at"] = "2026-08-09T12:00:01.000000Z"
    conflicting = seal_record(
        {
            key: value
            for key, value in conflicting.items()
            if key not in {"payload_hash", "record_hash"}
        }
    )
    with pytest.raises(FAL002Error, match="AUTHORITY_CONFLICT"):
        publish_create_only(path, conflicting)
    assert path.read_bytes() == original
    assert load_gate_chain(tmp_path, ORIGIN) == [gate]


def test_committed_stage_is_preserved_and_hash_bound(tmp_path):
    gate = origin_gate()
    path, attempt, file_hash = stage_committed_record(tmp_path, ORIGIN, "a" * 64, gate)
    assert attempt == 0
    assert path.exists()
    with pytest.raises(FAL002Error, match="HASH_MISMATCH"):
        from forge.fal002_io import publish_staged

        publish_staged(path, tmp_path / "wrong.json", "f" * 64)
    assert path.exists()
    assert len(file_hash) == 64


def test_pointer_free_recovery_n_preserves_lineage_and_correction_state(tmp_path):
    predecessor = origin_gate()
    roots = []
    for suffix in range(1, 4):
        root = recovery_root(predecessor["series_id"], predecessor["record_hash"], suffix)
        publish_create_only(canonical_record_path(tmp_path, root), root)
        discovered = discover_recovery_root(
            tmp_path, root["payload"]["recovery_root"]["recovery_discovery_key"]
        )
        assert discovered == root
        assert root["payload"]["recovery_root"]["origin_series_id"] == ORIGIN
        assert root["payload"]["correction_count"] == 2
        roots.append(root)
        predecessor = root
    assert len({root["series_id"] for root in roots}) == 3
    assert [root["payload"]["recovery_root"]["predecessor_series_id"] for root in roots] == [
        ORIGIN,
        roots[0]["series_id"],
        roots[1]["series_id"],
    ]


def test_recovery_probe_skips_stable_obstruction_without_directory_scan(tmp_path):
    valid = recovery_root(ORIGIN, origin_gate()["record_hash"], 9, ordinal=1)
    key = valid["payload"]["recovery_root"]["recovery_discovery_key"]
    obstructed_uuid = recovery_candidate_uuid(key, 0)
    obstruction = (
        tmp_path / ".forge" / "fal002" / "series" / obstructed_uuid / "gate" / "00000000.json"
    )
    obstruction.parent.mkdir(parents=True)
    obstruction.write_bytes(b"not canonical\n")
    publish_create_only(canonical_record_path(tmp_path, valid), valid)
    assert discover_recovery_root(tmp_path, key) == valid


def test_finding_remediation_empty_review_and_independent_absence():
    new = finding_event(
        0,
        "REVIEW_OBSERVATION",
        {
            "observation": "NEW",
            "observed_severity": "HIGH",
            "observed_blocking": True,
            "statement": "defect",
            "criterion_ids": ["FAL2-CC-06"],
            "evidence_bindings": [{}],
            "rationale": "evidence",
            "recurs_after_event_hash": None,
        },
    )
    remediation = finding_event(
        1,
        "REMEDIATION_CLAIM",
        {"remediation": {"remediation_evidence_hash": "b" * 64}},
        new["event_hash"],
    )
    current, checkpoint = fold_finding_events([new, remediation])
    assert current[0]["state"] == "ADDRESSED_AWAITING_REVIEW"
    assert checkpoint["event_count"] == 2
    assert fold_finding_events([new, remediation])[0] == current
    absence = finding_event(
        2,
        "REVIEW_OBSERVATION",
        {
            "observation": "ABSENT_AFTER_CORRECTION",
            "observed_severity": "HIGH",
            "observed_blocking": False,
            "statement": "independently absent",
            "criterion_ids": ["FAL2-CC-06"],
            "evidence_bindings": [{}],
            "rationale": "fresh review",
            "recurs_after_event_hash": None,
        },
        remediation["event_hash"],
    )
    verified, _ = fold_finding_events([new, remediation, absence])
    assert verified[0]["state"] == "INDEPENDENTLY_VERIFIED"


def test_finding_checkpoint_rejects_order_and_predecessor_corruption():
    new = finding_event(
        0,
        "REVIEW_OBSERVATION",
        {
            "observation": "NEW",
            "observed_severity": "CRITICAL",
            "observed_blocking": True,
            "statement": "critical",
            "criterion_ids": ["FAL2-CC-06"],
            "evidence_bindings": [{}],
            "rationale": "evidence",
            "recurs_after_event_hash": None,
        },
    )
    corrupt = deepcopy(new)
    corrupt["event_ordinal"] = 2
    with pytest.raises(FAL002Error, match="HASH_MISMATCH"):
        fold_finding_events([corrupt])
