import hashlib
import os
import stat
import subprocess
from pathlib import Path

import pytest

from forge.project_memory import (
    extract_sections,
    has_structural_content,
    parse_commit_hashes,
    parse_references,
)
from forge.status import StatusItem, StatusState, _rollup_state, evaluate_status


def write_healthy_memory(root: Path) -> None:
    files = {
        "PROJECT_STATE.md": (
            "# Project State\n\n"
            "## Status\n\nCS-001.1 is Implementation Ready.\n\n"
            "## Current Version\n\n`v0.5.0`\n\n"
            "## Planned Release\n\n`v0.5.0` is `Planned`.\n\n"
            "## Current Objective\n\nImplement CS-001.1.\n\n"
            "## What Exists\n\n- Governance.\n\n"
            "## What Does Not Exist\n\n- Release automation.\n\n"
            "## Architectural Posture\n\nKeep changes bounded.\n\n"
            "## Next Recommended Work\n\n1. Implement CS-001.1.\n"
        ),
        "PROJECT_BRAIN.md": (
            "# Project Brain\n\n"
            "## Core Identity\n\nForge fixture.\n\n"
            "## Guiding Beliefs\n\n- Determinism.\n\n"
            "## Product Shape\n\nGoverned tooling.\n\n"
            "## Important Boundaries\n\n- Read-only status.\n\n"
            "## Current Decisions\n\nADR 0001 is current authority.\n\n"
            "## Open Questions\n\n- What comes next?\n"
        ),
        "AI_HANDOFF.md": (
            "# AI Handoff\n\n"
            "## Role Context\n\nMaintain Forge.\n\n"
            "## Current Repository State\n\nRelease `v0.5.0` is `Planned`.\n\n"
            "## Current Architectural Intent\n\nKeep status read-only.\n\n"
            "## Instructions For Future AI Agents\n\nFollow governance.\n\n"
            "## Immediate Next Step\n\nImplement CS-001.1.\n"
        ),
    }
    for name, content in files.items():
        (root / name).write_text(content, encoding="utf-8")
    for directory in (
        "docs/decisions",
        "docs/capabilities",
        "docs/engineering",
        "docs/reviews",
        "docs/release",
    ):
        (root / directory).mkdir(parents=True, exist_ok=True)
    (root / "docs/capabilities/CS-001.1-Test.md").write_text(
        "# CS\n\nStatus: Implementation Ready\n", encoding="utf-8"
    )
    (root / "docs/decisions/0001-Test.md").write_text(
        "# ADR\n\nStatus: Accepted\n", encoding="utf-8"
    )
    (root / "docs/release/checklist-0.5.0.md").write_text(
        "# Release\n\nStatus: Planned\n", encoding="utf-8"
    )


def project_memory(root: Path):
    return next(
        category
        for category in evaluate_status(root).categories
        if category.name == "Project Memory Health"
    )


def rule_items(root: Path, rule: str):
    return [item for item in project_memory(root).items if item.label == rule]


def tree_snapshot(root: Path) -> dict[str, tuple[str, int]]:
    snapshot = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            snapshot[path.relative_to(root).as_posix()] = (
                digest,
                stat.S_IMODE(path.stat().st_mode),
            )
    return snapshot


def test_exact_section_extraction_and_duplicate_facts() -> None:
    sections = extract_sections("# X\n\n## Status\n\nOne\n\n## Status\n\nTwo\n")

    assert [section.content.strip() for section in sections["Status"]] == ["One", "Two"]
    assert "status" not in sections


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("\n \t\n", False),
        ("<!-- only -->\n", False),
        ("<!-- unterminated\ntext", False),
        ("<!-- comment -->\nValue\n", True),
        ("TBD\n", True),
    ],
)
def test_structural_content_is_literal(content: str, expected: bool) -> None:
    assert has_structural_content(content) is expected


def test_reference_parsing_is_finite_and_ignores_paths() -> None:
    content = (
        "ADR 0001 FCS-002 CS-002.3 EB-005 EB-002.2 DAR-CS-0003 "
        "DAR-EB-0004 DAR-AR-0002 PRR-0001 "
        "[CS-003.1](docs/capabilities/CS-999.1-Missing.md) "
        "https://example.com/EB-997 C:/EB-996.md ../CS-995.1.md"
    )

    assert [value.identifier for value in parse_references(content)] == [
        "ADR 0001",
        "FCS-002",
        "CS-002.3",
        "EB-005",
        "EB-002.2",
        "DAR-CS-0003",
        "DAR-EB-0004",
        "DAR-AR-0002",
        "PRR-0001",
        "CS-003.1",
    ]


def test_only_full_commit_hashes_are_parsed() -> None:
    full_hash = "a" * 40
    assert parse_commit_hashes(f"short abc1234 full {full_hash}") == (full_hash,)


def test_healthy_project_memory_is_ok(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)

    health = project_memory(tmp_path)

    assert health.state == StatusState.OK
    assert {item.label for item in health.items} == {
        "PMH-001",
        "PMH-002",
        "PMH-003",
        "PMH-004",
        "PMH-005",
        "PMH-006",
        "PMH-007",
        "PMH-008",
        "PMH-009",
    }


@pytest.mark.parametrize("missing", ["PROJECT_STATE.md", "PROJECT_BRAIN.md", "AI_HANDOFF.md"])
def test_each_missing_primary_file_is_reported_and_other_files_continue(
    tmp_path: Path, missing: str
) -> None:
    write_healthy_memory(tmp_path)
    (tmp_path / missing).unlink()

    health = project_memory(tmp_path)

    assert health.state == StatusState.MISSING
    assert any(
        item.state == StatusState.MISSING and missing in item.message for item in health.items
    )
    assert len(rule_items(tmp_path, "PMH-001")) == 3


def test_missing_duplicate_and_comment_only_required_sections(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    state_path = tmp_path / "PROJECT_STATE.md"
    content = state_path.read_text(encoding="utf-8")
    content = content.replace("## What Exists\n\n- Governance.\n\n", "")
    content += "\n## Status\n\nDuplicate.\n"
    content = content.replace(
        "## Current Objective\n\nImplement CS-001.1.", "## Current Objective\n\n<!-- empty -->"
    )
    state_path.write_text(content, encoding="utf-8")

    items = rule_items(tmp_path, "PMH-002")

    assert {item.state for item in items} == {StatusState.MISSING, StatusState.WARNING}
    assert any("What Exists" in item.message for item in items)
    assert any("duplicate ## Status" in item.message for item in items)
    assert any("Current Objective" in item.message for item in items)


@pytest.mark.parametrize("replacement", ["## open questions", "### Open Questions"])
def test_different_case_and_third_level_headings_are_not_aliases(
    tmp_path: Path, replacement: str
) -> None:
    write_healthy_memory(tmp_path)
    brain = tmp_path / "PROJECT_BRAIN.md"
    brain.write_text(
        brain.read_text(encoding="utf-8").replace("## Open Questions", replacement),
        encoding="utf-8",
    )

    item = next(
        item for item in rule_items(tmp_path, "PMH-002") if "Open Questions" in item.message
    )
    assert item.state == StatusState.MISSING


def test_placeholder_looking_current_value_is_structurally_present(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    state = tmp_path / "PROJECT_STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace("Implement CS-001.1.", "TBD", 1),
        encoding="utf-8",
    )

    assert rule_items(tmp_path, "PMH-003")[0].state == StatusState.OK


def test_missing_and_ambiguous_active_references_are_distinct(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    state = tmp_path / "PROJECT_STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace(
            "Implement CS-001.1.", "Implement EB-999 and CS-001.1.", 1
        ),
        encoding="utf-8",
    )
    (tmp_path / "docs/capabilities/CS-001.1-Duplicate.md").write_text(
        "# duplicate\n", encoding="utf-8"
    )

    items = rule_items(tmp_path, "PMH-004")

    assert any(item.state == StatusState.MISSING and "EB-999" in item.message for item in items)
    assert any(item.state == StatusState.WARNING and "CS-001.1" in item.message for item in items)


def test_unreadable_supporting_artifact_is_blocked(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    (tmp_path / "docs/capabilities/CS-001.1-Test.md").write_bytes(b"\xff\xfe")

    assert rule_items(tmp_path, "PMH-004")[0].state == StatusState.BLOCKED


def test_links_external_urls_and_historical_sections_are_ignored(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    state = tmp_path / "PROJECT_STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8")
        + "\n## Recently Completed\n\nHistorical EB-999.\n"
        + "\n[missing](docs/engineering/EB-998-Missing.md) https://example.com/EB-997\n",
        encoding="utf-8",
    )

    assert all("EB-99" not in item.message for item in rule_items(tmp_path, "PMH-004"))


def test_active_work_contradiction_and_different_detail(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    handoff = tmp_path / "AI_HANDOFF.md"
    original = handoff.read_text(encoding="utf-8")
    handoff.write_text(
        original.replace("Implement CS-001.1.", "Implement EB-005."), encoding="utf-8"
    )

    assert rule_items(tmp_path, "PMH-005")[0].state == StatusState.WARNING

    handoff.write_text(
        original.replace("Implement CS-001.1.", "Implement detailed tests for CS-001.1."),
        encoding="utf-8",
    )
    assert rule_items(tmp_path, "PMH-005")[0].state == StatusState.OK


def test_explicit_lifecycle_contradiction_and_conflicting_evidence(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    state = tmp_path / "PROJECT_STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace(
            "CS-001.1 is Implementation Ready.", "CS-001.1 is Closed."
        ),
        encoding="utf-8",
    )
    artifact = tmp_path / "docs/capabilities/CS-001.1-Test.md"
    artifact.write_text(
        "# CS\n\nStatus: Implementation Ready\n\n## Status\n\nClosed\n",
        encoding="utf-8",
    )

    item = rule_items(tmp_path, "PMH-006")[0]

    assert item.state == StatusState.WARNING
    assert "conflicting explicit lifecycle evidence" in item.message


def test_lifecycle_prohibition_is_not_an_affirmative_claim(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    state = tmp_path / "PROJECT_STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace(
            "## Current Objective\n\nImplement CS-001.1.",
            "## Current Objective\n\nDo not mark CS-001.1 Closed before review.",
        ),
        encoding="utf-8",
    )

    assert rule_items(tmp_path, "PMH-006")[0].state == StatusState.OK


def test_formal_review_result_is_lifecycle_evidence(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    review = tmp_path / "docs/reviews/DAR-CS-0003-Test.md"
    review.write_text("# Review\n\n## Review Status\n\nPASS\n", encoding="utf-8")
    state = tmp_path / "PROJECT_STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace(
            "CS-001.1 is Implementation Ready.", "DAR-CS-0003 returned PASS."
        ),
        encoding="utf-8",
    )

    assert rule_items(tmp_path, "PMH-006")[0].state == StatusState.OK


@pytest.mark.parametrize(
    ("next_step", "artifact_name", "artifact_content"),
    [
        (
            "DAR-CS-0003 is pending review.",
            "docs/reviews/DAR-CS-0003-Test.md",
            "# Review\n\n## Review Status\n\nPASS\n",
        ),
        (
            "DAR-CS-0003 is awaiting review.",
            "docs/reviews/DAR-CS-0003-Test.md",
            "# Review\n\n## Review Status\n\nPASS\n",
        ),
        (
            f"EB-005 is ready to commit at {'a' * 40}.",
            "docs/engineering/EB-005-Test.md",
            "# EB\n\nStatus: Implementation Ready\n",
        ),
        (
            f"EB-005 is commit pending at {'a' * 40}.",
            "docs/engineering/EB-005-Test.md",
            "# EB\n\nStatus: Implementation Ready\n",
        ),
        (
            "CS-001.1 is implementation ready.",
            "docs/capabilities/CS-001.1-Test.md",
            "# CS\n\nStatus: Implemented\n",
        ),
    ],
)
def test_supported_stale_gate_requires_positive_proof(
    tmp_path: Path, next_step: str, artifact_name: str, artifact_content: str
) -> None:
    write_healthy_memory(tmp_path)
    path = tmp_path / artifact_name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(artifact_content, encoding="utf-8")
    if "ready to commit" in next_step or "commit pending" in next_step:
        subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True
        )
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
        subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "initial"], cwd=tmp_path, check=True, capture_output=True
        )
        commit_hash = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True, capture_output=True, text=True
        ).stdout.strip()
        next_step = next_step.replace("a" * 40, commit_hash)
    handoff = tmp_path / "AI_HANDOFF.md"
    content = handoff.read_text(encoding="utf-8")
    content = content.replace("Implement CS-001.1.", next_step)
    handoff.write_text(content, encoding="utf-8")

    assert rule_items(tmp_path, "PMH-007")[0].state == StatusState.WARNING


def test_legitimately_pending_gate_is_ok(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    review = tmp_path / "docs/reviews/DAR-CS-0003-Test.md"
    review.write_text("# Review\n\nStatus: Draft\n", encoding="utf-8")
    handoff = tmp_path / "AI_HANDOFF.md"
    handoff.write_text(
        handoff.read_text(encoding="utf-8").replace(
            "Implement CS-001.1.", "DAR-CS-0003 is pending review."
        ),
        encoding="utf-8",
    )

    assert rule_items(tmp_path, "PMH-007")[0].state == StatusState.OK


def test_pending_artifact_review_uses_explicit_linked_review(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    (tmp_path / "docs/engineering/EB-005-Test.md").write_text(
        "# EB\n\nStatus: Implemented\n\nReview: DAR-EB-0004\n", encoding="utf-8"
    )
    (tmp_path / "docs/reviews/DAR-EB-0004-Test.md").write_text(
        "# Review\n\n## Review Status\n\nPASS\n", encoding="utf-8"
    )
    handoff = tmp_path / "AI_HANDOFF.md"
    handoff.write_text(
        handoff.read_text(encoding="utf-8").replace(
            "Implement CS-001.1.", "EB-005 is pending review."
        ),
        encoding="utf-8",
    )

    assert rule_items(tmp_path, "PMH-007")[0].state == StatusState.WARNING


@pytest.mark.parametrize(
    "unsupported",
    [
        "EB-005 implementation pending.",
        "EB-005 implementation review pending.",
        "EB-005 condition closure pending.",
        "EB-005 closeout pending.",
    ],
)
def test_unapproved_gate_phrases_are_not_inferred(tmp_path: Path, unsupported: str) -> None:
    write_healthy_memory(tmp_path)
    (tmp_path / "docs/engineering/EB-005-Test.md").write_text(
        "# EB\n\nStatus: Closed\n", encoding="utf-8"
    )
    handoff = tmp_path / "AI_HANDOFF.md"
    handoff.write_text(
        handoff.read_text(encoding="utf-8").replace("Implement CS-001.1.", unsupported),
        encoding="utf-8",
    )

    assert rule_items(tmp_path, "PMH-007")[0].state == StatusState.NOT_APPLICABLE


def test_release_state_disagreement_without_version_comparison(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    handoff = tmp_path / "AI_HANDOFF.md"
    handoff.write_text(
        handoff.read_text(encoding="utf-8").replace("is `Planned`", "is `Released`"),
        encoding="utf-8",
    )

    item = rule_items(tmp_path, "PMH-008")[0]

    assert item.state == StatusState.WARNING
    assert "checklist status planned" in item.message


def test_multiple_release_status_locations_are_blocked(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    checklist = tmp_path / "docs/release/checklist-0.5.0.md"
    checklist.write_text("# Release\n\nStatus: Planned\n\n## Status\n\nPlanned\n", encoding="utf-8")

    assert rule_items(tmp_path, "PMH-008")[0].state == StatusState.BLOCKED


def test_superseded_current_adr_warns_but_historical_qualifier_is_ok(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    adr = tmp_path / "docs/decisions/0001-Test.md"
    adr.write_text("# ADR\n\nStatus: Superseded\n", encoding="utf-8")

    assert rule_items(tmp_path, "PMH-009")[0].state == StatusState.WARNING

    brain = tmp_path / "PROJECT_BRAIN.md"
    brain.write_text(
        brain.read_text(encoding="utf-8").replace(
            "ADR 0001 is current authority.", "ADR 0001 is retained as historical evidence."
        ),
        encoding="utf-8",
    )
    assert rule_items(tmp_path, "PMH-009")[0].state == StatusState.OK


def test_non_forge_repository_is_not_applicable(tmp_path: Path) -> None:
    health = project_memory(tmp_path)

    assert health.state == StatusState.NOT_APPLICABLE


def test_evaluation_is_completely_read_only(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    before = tree_snapshot(tmp_path)

    evaluate_status(tmp_path)

    assert tree_snapshot(tmp_path) == before
    assert not (tmp_path / ".git").exists()


def test_category_order_and_existing_category_states(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)

    report = evaluate_status(tmp_path)
    names = [category.name for category in report.categories]

    assert names.index("Runtime Memory Status") + 1 == names.index("Project Memory Health")
    assert names.index("Project Memory Health") + 1 == names.index("Version Consistency Status")
    assert (
        next(
            category for category in report.categories if category.name == "Runtime Memory Status"
        ).state
        == StatusState.OK
    )


def test_no_git_commit_reference_is_not_applicable(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    state = tmp_path / "PROJECT_STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace(
            "Implement CS-001.1.", f"Implement CS-001.1 from {'a' * 40}.", 1
        ),
        encoding="utf-8",
    )

    assert any(item.state == StatusState.NOT_APPLICABLE for item in rule_items(tmp_path, "PMH-004"))


def test_invalid_utf8_blocks_only_dependent_memory_checks(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    (tmp_path / "PROJECT_BRAIN.md").write_bytes(b"\xff\xfe")

    health = project_memory(tmp_path)

    assert health.state == StatusState.BLOCKED
    assert any(
        item.label == "PMH-001" and item.state == StatusState.BLOCKED for item in health.items
    )
    assert any(item.label == "PMH-002" for item in health.items)


@pytest.mark.parametrize(
    ("states", "expected"),
    [
        ((StatusState.OK, StatusState.BLOCKED, StatusState.MISSING), StatusState.BLOCKED),
        ((StatusState.OK, StatusState.MISSING, StatusState.WARNING), StatusState.MISSING),
        ((StatusState.OK, StatusState.WARNING), StatusState.WARNING),
        ((StatusState.NOT_APPLICABLE,), StatusState.NOT_APPLICABLE),
        ((StatusState.OK, StatusState.NOT_APPLICABLE), StatusState.OK),
    ],
)
def test_literal_category_aggregation_precedence(
    states: tuple[StatusState, ...], expected: StatusState
) -> None:
    items = tuple(
        StatusItem(f"item-{index}", state, "literal") for index, state in enumerate(states)
    )

    assert _rollup_state(items) == expected


def test_file_permissions_are_not_changed(tmp_path: Path) -> None:
    write_healthy_memory(tmp_path)
    path = tmp_path / "PROJECT_STATE.md"
    before = stat.S_IMODE(path.stat().st_mode)

    evaluate_status(tmp_path)

    assert stat.S_IMODE(path.stat().st_mode) == before
    assert os.access(path, os.R_OK)
