from pathlib import Path

import pytest
from typer.testing import CliRunner

from forge.bootstrap import is_version_compatible, load_bootstrap_templates
from forge.cli import app


runner = CliRunner()


def test_valid_project_creation_in_isolated_filesystem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "demo-project"])

    assert result.exit_code == 0
    root = tmp_path / "demo-project"
    assert (root / "README.md").is_file()
    assert (root / "PROJECT_STATE.md").is_file()
    assert (root / ".gitignore").is_file()
    assert (root / "docs" / "architecture").is_dir()
    assert "Forge project initialized: demo-project" in result.stdout
    assert "Created folders: 9" in result.stdout
    assert "Created files: 8" in result.stdout


def test_invalid_project_name(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "../bad"])

    assert result.exit_code == 1
    assert "Error:" in result.stderr
    assert not (tmp_path / "bad").exists()


def test_dry_run_writes_nothing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "demo-project", "--dry-run"])

    assert result.exit_code == 0
    assert "Forge init dry run:" in result.stdout
    assert "Validation: OK" in result.stdout
    assert not (tmp_path / "demo-project").exists()


def test_existing_directory_overwrite_protection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "demo-project"
    root.mkdir()
    (root / "existing.txt").write_text("do not overwrite", encoding="utf-8")

    result = runner.invoke(app, ["init", "demo-project"])

    assert result.exit_code == 1
    assert "already exists and is not empty" in result.stderr
    assert (root / "existing.txt").read_text(encoding="utf-8") == "do not overwrite"


def test_template_rendering_strips_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "demo-project"])

    assert result.exit_code == 0
    readme = (tmp_path / "demo-project" / "README.md").read_text(encoding="utf-8")
    assert readme.startswith("# demo-project")
    assert "template_name:" not in readme
    assert "{{PROJECT_NAME}}" not in readme


def test_all_bootstrap_templates_are_discovered() -> None:
    templates = load_bootstrap_templates()

    assert len(templates) == 8
    assert {template.output_name for template in templates} == {
        "README.md",
        "PROJECT_STATE.md",
        "PROJECT_BRAIN.md",
        "AI_HANDOFF.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "LICENSE",
        ".gitignore",
    }


def test_template_compatibility_validation() -> None:
    assert is_version_compatible("0.2.0", ">=0.2,<0.3")
    assert not is_version_compatible("0.1.0", ">=0.2,<0.3")
    assert not is_version_compatible("0.3.0", ">=0.2,<0.3")
