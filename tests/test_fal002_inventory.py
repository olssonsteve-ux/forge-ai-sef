from pathlib import Path

import pytest

from forge.fal002_inventory import AUTHORIZED_MODULES, counted_loc, enforce_limits, inventory
from forge.fal002_model import FAL002Error


def test_self_inventory_is_deterministic_and_within_hard_limits():
    root = Path(__file__).parents[1]
    first = inventory(root)
    second = inventory(root)
    assert first == second
    assert first["disposition"] == "PASS"
    assert first["counts"]["modules"] == 4
    assert first["counts"]["new_production_loc"] <= 3000
    assert first["counts"]["executor_adapters"] == 1
    assert first["counts"]["reviewer_adapters"] == 1
    assert first["counts"]["schema_surfaces"] == 5
    assert first["dependencies"]["new_direct"] == []
    assert first["dependencies"]["new_transitive"] == []
    assert first["unresolved_targets"] == []


def test_inventory_has_exact_authorized_module_set():
    result = inventory(Path(__file__).parents[1])
    assert tuple(item["path"] for item in result["files"]) == tuple(sorted(AUTHORIZED_MODULES))
    assert all(edge["target"] != "forge/adaptive_loop.py" for edge in result["edges"])


def test_counted_loc_excludes_blank_comment_and_docstring(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text('"""module"""\n\n# comment\nx = 1  # inline\n', encoding="utf-8")
    assert counted_loc(source) == 1


def test_hard_limit_failure_requires_budget_authority():
    result = inventory(Path(__file__).parents[1])
    result["disposition"] = "AWAITING_HUMAN"
    result["counts"]["new_production_loc"] = 1801
    with pytest.raises(FAL002Error, match="BUDGET_AUTHORITY_REQUIRED"):
        enforce_limits(result)
