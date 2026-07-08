from pathlib import Path

from typer.testing import CliRunner

from forge.cli import app
from forge.status import StatusState, evaluate_status

runner = CliRunner()


def create_forge_project(root: Path) -> None:
    for file_name in (
        "CONSTITUTION.md",
        "AI_ENGINEERING_CONDUCT.md",
        "PROJECT_STATE.md",
        "PROJECT_BRAIN.md",
        "AI_HANDOFF.md",
        "CHANGELOG.md",
        "README.md",
        "pyproject.toml",
    ):
        (root / file_name).write_text(f"# {file_name}\n", encoding="utf-8")

    for directory in (
        "docs/decisions",
        "docs/capabilities",
        "docs/engineering",
        "docs/reviews",
        "docs/release",
        "templates",
        "standards",
        "tests",
        ".github/workflows",
    ):
        (root / directory).mkdir(parents=True, exist_ok=True)

    (root / "docs/capabilities/FCS-001-Test.md").write_text("# FCS test\n", encoding="utf-8")
    (root / "docs/capabilities/CS-001.1-Test.md").write_text("# CS test\n", encoding="utf-8")
    (root / "docs/engineering/EB-001-Test.md").write_text("# EB test\n", encoding="utf-8")


def snapshot_files(root: Path) -> dict[Path, str]:
    return {
        path.relative_to(root): path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def category(report_name: str, root: Path):
    report = evaluate_status(root)
    return next(item for item in report.categories if item.name == report_name)


def test_status_works_in_complete_forge_repository(tmp_path: Path) -> None:
    create_forge_project(tmp_path)

    report = evaluate_status(tmp_path)

    assert {item.name for item in report.categories} == {
        "Constitutional Status",
        "Governance Status",
        "Documentation Status",
        "Capability Status",
        "Engineering Workflow Status",
        "Testing Status",
        "Release Status",
        "Runtime Memory Status",
        "Repository Status",
    }
    assert report.categories[0].state == StatusState.OK


def test_missing_constitution_reports_missing(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    (tmp_path / "CONSTITUTION.md").unlink()

    constitutional = category("Constitutional Status", tmp_path)

    assert constitutional.state == StatusState.MISSING
    assert any(
        item.label == "Constitution" and item.state == StatusState.MISSING
        for item in constitutional.items
    )


def test_missing_project_state_reports_missing(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    (tmp_path / "PROJECT_STATE.md").unlink()

    memory = category("Runtime Memory Status", tmp_path)

    assert memory.state == StatusState.MISSING
    assert any(
        item.label == "Project State" and item.state == StatusState.MISSING for item in memory.items
    )


def test_no_git_repository_still_evaluates(tmp_path: Path) -> None:
    create_forge_project(tmp_path)

    repository = category("Repository Status", tmp_path)

    assert any(
        item.label == "Git repository" and item.state == StatusState.NOT_APPLICABLE
        for item in repository.items
    )


def test_service_is_read_only(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    before = snapshot_files(tmp_path)

    evaluate_status(tmp_path)

    assert snapshot_files(tmp_path) == before


def test_cli_status_is_read_only(tmp_path: Path, monkeypatch) -> None:
    create_forge_project(tmp_path)
    before = snapshot_files(tmp_path)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Forge status" in result.stdout
    assert "This is informational status only" in result.stdout
    assert snapshot_files(tmp_path) == before


def test_status_category_generation(tmp_path: Path) -> None:
    create_forge_project(tmp_path)

    report = evaluate_status(tmp_path)

    assert len(report.categories) == 9
    assert all(category.name for category in report.categories)
    assert all(category.items for category in report.categories)
