import hashlib
import json
import uuid

import pytest

from forge.fal002 import make_gate
from forge.fal002_model import (
    CF,
    CJ,
    HB,
    FAL002Error,
    H,
    decision_binding,
    decision_identity,
    decision_requirement,
    empty_finding_checkpoint,
    generate_schemas,
    parse_cf,
    pass_eligible,
    seal_record,
    validate_record,
    validate_schema_instance,
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


def origin_gate():
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


def test_cj_cf_and_hash_literals_are_independent():
    value = {"z": "å", "a": [True, None, -2]}
    literal = '{"a":[true,null,-2],"z":"å"}'.encode()
    assert CJ(value) == literal
    assert CF(value) == literal + b"\n"
    expected = hashlib.sha256(b'{"domain":"fal002-json-content-v1","value":"x"}').hexdigest()
    assert H("fal002-json-content-v1", "x") == expected
    assert HB(b"x\n") == hashlib.sha256(b"x\n").hexdigest()
    assert HB(CF(value)) != hashlib.sha256(CJ(value)).hexdigest()


@pytest.mark.parametrize("value", [1.2, float("nan"), "\ud800"])
def test_cj_rejects_values_outside_frozen_json_domain(value):
    with pytest.raises(FAL002Error, match="MALFORMED_BOUNDARY"):
        CJ(value)


@pytest.mark.parametrize(
    "raw",
    [
        b'{"b":1,"a":2}\n',
        b'{"a":1,"a":1}\n',
        b'{"a":1.0}\n',
        b'{"a":1}',
        b'{"a":1}\n\n',
        b'\xef\xbb\xbf{"a":1}\n',
    ],
)
def test_parse_cf_rejects_noncanonical_or_malformed_files(raw):
    with pytest.raises(FAL002Error, match="MALFORMED_BOUNDARY"):
        parse_cf(raw)


def test_gate_is_closed_and_hash_validated():
    gate = origin_gate()
    assert validate_record(gate) is gate
    unknown = {**gate, "surprise": True}
    with pytest.raises(FAL002Error, match="MALFORMED_BOUNDARY"):
        validate_record(unknown)
    corrupt = {**gate, "record_hash": "f" * 64}
    with pytest.raises(FAL002Error, match="HASH_MISMATCH"):
        validate_record(corrupt)
    nested = json.loads(json.dumps(gate))
    nested["payload"]["manifest"]["surprise"] = True
    with pytest.raises(FAL002Error, match="MALFORMED_BOUNDARY"):
        seal_record(
            {
                key: value
                for key, value in nested.items()
                if key not in {"payload_hash", "record_hash"}
            }
        )


def test_decision_identity_requirement_and_binding_stay_semantic():
    semantic = {
        "domain": "RECOVERY",
        "question": "Resume?",
        "allowed_choices": ["AUTHORIZE_RECOVERY_RESUME", "ABANDON_LINEAGE"],
        "original_target": {
            "target_kind": "RECOVERY_ROOT",
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
    assert requirement["decision_identity"] == decision_identity(semantic)
    binding = decision_binding(
        {
            "decision_identity": requirement["decision_identity"],
            "decision_requirement_hash": requirement["decision_requirement_hash"],
            "binding_generation": 0,
            "binding_series_id": SERIES,
            "pending_card_record_id": f"{requirement['decision_identity']}-pending-b0000",
            "pending_card_locator": "decisions/pending.json",
            "pending_card_record_hash": "4" * 64,
            "previous_binding_key": None,
            "obstruction_evidence_hash": None,
        }
    )
    relocated = decision_binding({**binding, "pending_card_record_hash": "5" * 64})
    assert relocated["binding_key"] == binding["binding_key"]


def test_pass_eligibility_never_clears_addressed_or_critical_blocker():
    addressed = {
        "state": "ADDRESSED_AWAITING_REVIEW",
        "current_blocking": True,
        "current_severity": "HIGH",
    }
    critical = {"state": "OPEN", "current_blocking": True, "current_severity": "CRITICAL"}
    assert not pass_eligible([addressed], pending_decisions=False, criteria_complete=True)
    assert not pass_eligible([critical], pending_decisions=False, criteria_complete=True)
    assert not pass_eligible([], pending_decisions=True, criteria_complete=True)
    assert pass_eligible([], pending_decisions=False, criteria_complete=True)


def test_schema_generation_is_exact_and_only_five(tmp_path):
    first = generate_schemas(tmp_path)
    second = generate_schemas(tmp_path, check=True)
    assert first == second
    assert len(first) == 5
    assert {item.schema_id for item in first} == {
        "fal002.gate-record.v1",
        "fal002.executor-exchange.v1",
        "fal002.run-record.v1",
        "fal002.reviewer-exchange.v1",
        "fal002.human-decision.v1",
    }
    schemas = [json.loads(item.path.read_text()) for item in first]
    assert all(
        schema.get("additionalProperties") is False or "oneOf" in schema for schema in schemas
    )
    assert all("$defs" in schema for schema in schemas)
    assert uuid.UUID(SERIES) == uuid.UUID(SERIES)


def test_runtime_and_generated_schema_accept_and_reject_same_gate(tmp_path):
    generated = {item.schema_id: item for item in generate_schemas(tmp_path)}
    schema = json.loads(generated["fal002.gate-record.v1"].path.read_text())
    valid = origin_gate()
    validate_record(valid)
    validate_schema_instance(valid, schema)
    invalid = json.loads(json.dumps(valid))
    invalid["payload"]["manifest"]["unexpected"] = True
    for validator in (validate_record, lambda value: validate_schema_instance(value, schema)):
        with pytest.raises(FAL002Error, match="MALFORMED_BOUNDARY"):
            validator(invalid)
