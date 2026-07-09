import subprocess
from pathlib import Path

from typer.testing import CliRunner

from forge.cli import app
from forge.status import StatusState, evaluate_status

runner = CliRunner()


def create_forge_project(root: Path, version: str = "0.4.0") -> None:
    root_docs = {
        "CONSTITUTION.md": "# Constitution\n",
        "AI_ENGINEERING_CONDUCT.md": "# AI Engineering Conduct\n",
        "PROJECT_STATE.md": (f"# Project State\n\n## Current Version\n\n`v{version}`\n"),
        "PROJECT_BRAIN.md": "# Project Brain\n",
        "AI_HANDOFF.md": (
            "# AI Handoff\n\n"
            "## Current Repository State\n\n"
            f"The repository is released as Forge `v{version}`.\n"
        ),
        "CHANGELOG.md": (
            "# Changelog\n\n"
            "## [Unreleased]\n\n"
            "No unreleased changes.\n\n"
            f"## [{version}] - 2026-07-09\n\n"
            "### Added\n\n"
            "- Test release.\n\n"
            "## [0.1.0] - 2026-01-01\n\n"
            "- Historical release.\n"
        ),
        "README.md": (
            "# Test Forge Project\n\n"
            "## Current State\n\n"
            f"This repository is released as Forge `v{version}`.\n"
        ),
        "pyproject.toml": f'[project]\nname = "test-forge-project"\nversion = "{version}"\n',
    }
    for file_name, content in root_docs.items():
        (root / file_name).write_text(content, encoding="utf-8")

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


def create_git_repo(root: Path, tag: str | None = "v0.4.0") -> None:
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "config", "user.email", "forge-tests@example.com"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Forge Tests"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", "initial"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    if tag is not None:
        subprocess.run(["git", "tag", tag], cwd=root, check=True, capture_output=True, text=True)


def snapshot_files(root: Path) -> dict[Path, str]:
    return {
        path.relative_to(root): path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def category(report_name: str, root: Path):
    report = evaluate_status(root)
    return next(item for item in report.categories if item.name == report_name)


def status_item(report_name: str, label: str, root: Path):
    status_category = category(report_name, root)
    return next(item for item in status_category.items if item.label == label)


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
        "Version Consistency Status",
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

    assert len(report.categories) == 10
    assert all(category.name for category in report.categories)
    assert all(category.items for category in report.categories)


def test_version_consistency_reports_matching_versions(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    create_git_repo(tmp_path)

    version_status = category("Version Consistency Status", tmp_path)

    assert version_status.state == StatusState.OK
    assert all(item.state == StatusState.OK for item in version_status.items)


def test_version_consistency_reports_readme_mismatch(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    (tmp_path / "README.md").write_text(
        "# Test Forge Project\n\n"
        "## Current State\n\n"
        "This repository still references Forge `v0.3.3`.\n",
        encoding="utf-8",
    )
    create_git_repo(tmp_path)

    item = status_item("Version Consistency Status", "README current state", tmp_path)

    assert item.state == StatusState.WARNING
    assert "expected v0.4.0" in item.message


def test_version_consistency_reports_changelog_mismatch(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n"
        "## [Unreleased]\n\n"
        "No unreleased changes.\n\n"
        "## [0.3.3] - 2026-07-09\n\n"
        "- Previous release.\n",
        encoding="utf-8",
    )
    create_git_repo(tmp_path)

    item = status_item("Version Consistency Status", "Changelog latest release", tmp_path)

    assert item.state == StatusState.WARNING
    assert "expected v0.4.0" in item.message


def test_version_consistency_reports_project_state_mismatch(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    (tmp_path / "PROJECT_STATE.md").write_text(
        "# Project State\n\n## Current Version\n\n`v0.3.3`\n",
        encoding="utf-8",
    )
    create_git_repo(tmp_path)

    item = status_item("Version Consistency Status", "Project State current version", tmp_path)

    assert item.state == StatusState.WARNING
    assert "expected v0.4.0" in item.message


def test_version_consistency_reports_missing_git_tag(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    create_git_repo(tmp_path, tag=None)

    item = status_item("Version Consistency Status", "Latest release tag", tmp_path)

    assert item.state == StatusState.MISSING


def test_version_consistency_treats_missing_pyproject_as_not_applicable(
    tmp_path: Path,
) -> None:
    create_forge_project(tmp_path)
    (tmp_path / "pyproject.toml").unlink()
    create_git_repo(tmp_path)

    item = status_item("Version Consistency Status", "pyproject project version", tmp_path)

    assert item.state == StatusState.NOT_APPLICABLE


def test_dirty_working_tree_still_reported_separately(tmp_path: Path) -> None:
    create_forge_project(tmp_path)
    create_git_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "# Test Forge Project\n\n"
        "## Current State\n\n"
        "This repository is released as Forge `v0.4.0`.\n\n"
        "Uncommitted note.\n",
        encoding="utf-8",
    )

    version_status = category("Version Consistency Status", tmp_path)
    repository = category("Repository Status", tmp_path)

    assert version_status.state == StatusState.WARNING
    assert repository.state == StatusState.WARNING
    assert status_item("Repository Status", "Git working tree", tmp_path).state == (
        StatusState.WARNING
    )
