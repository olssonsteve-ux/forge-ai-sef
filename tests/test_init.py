import tomllib
from pathlib import Path

import pytest
from typer.testing import CliRunner

from forge import __version__
from forge.bootstrap import (
    BOOTSTRAP_OUTPUT_CONTRACT,
    ForgeInitError,
    default_variables,
    is_version_compatible,
    load_bootstrap_templates,
    render_template,
    validate_template,
)
from forge.cli import app

runner = CliRunner()

EXPECTED_DIRECTORIES = (
    "docs",
    "docs/architecture",
    "docs/contracts",
    "docs/decisions",
    "docs/vision",
    "standards",
    "templates",
    "tests",
)

EXPECTED_FILES = (
    "README.md",
    "PROJECT_STATE.md",
    "PROJECT_BRAIN.md",
    "AI_HANDOFF.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "LICENSE",
    ".gitignore",
)

EXPECTED_NEXT_STEP = (
    "Next step: review PROJECT_STATE.md and select source layout through architecture discovery."
)


def relative_generated_directories(root: Path) -> tuple[str, ...]:
    return tuple(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_dir())


def relative_generated_files(root: Path) -> tuple[str, ...]:
    return tuple(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())


def dry_run_paths(output: str, root: Path, start: str, end: str) -> tuple[str, ...]:
    lines = output.splitlines()
    start_index = lines.index(start) + 1
    end_index = lines.index(end)
    return tuple(
        Path(line.strip()).relative_to(root).as_posix() for line in lines[start_index:end_index]
    )


def test_valid_project_creation_in_isolated_filesystem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, ["init", "demo-project"])

    assert result.exit_code == 0
    root = tmp_path / "demo-project"
    assert len(relative_generated_directories(root)) == 8
    assert set(relative_generated_directories(root)) == set(EXPECTED_DIRECTORIES)
    assert len(relative_generated_files(root)) == 8
    assert set(relative_generated_files(root)) == set(EXPECTED_FILES)
    assert not (root / "forge").exists()
    assert not (root / "src").exists()
    assert "Forge project initialized: demo-project" in result.stdout
    assert "Created folders: 8" in result.stdout
    assert "Created files: 8" in result.stdout
    assert f"Bootstrap output contract: {BOOTSTRAP_OUTPUT_CONTRACT}" in result.stdout
    assert "Source layout: not selected" in result.stdout
    assert EXPECTED_NEXT_STEP in result.stdout


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
    assert "Folders to create: 8" in result.stdout
    assert "Files to create: 8" in result.stdout
    assert f"Bootstrap output contract: {BOOTSTRAP_OUTPUT_CONTRACT}" in result.stdout
    assert "Source layout: not selected" in result.stdout
    assert not (tmp_path / "demo-project").exists()


def test_dry_run_plan_matches_actual_generated_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    dry_root = tmp_path / "dry-project"
    dry_result = runner.invoke(app, ["init", dry_root.name, "--dry-run"])
    actual_root = tmp_path / "actual-project"
    actual_result = runner.invoke(app, ["init", actual_root.name])

    assert dry_result.exit_code == 0
    assert actual_result.exit_code == 0
    dry_directories = dry_run_paths(
        dry_result.stdout,
        dry_root,
        "Folders to create: 8",
        "Files to create: 8",
    )
    dry_files = dry_run_paths(
        dry_result.stdout,
        dry_root,
        "Files to create: 8",
        f"Bootstrap output contract: {BOOTSTRAP_OUTPUT_CONTRACT}",
    )

    assert dry_directories == EXPECTED_DIRECTORIES
    assert set(dry_directories) == set(relative_generated_directories(actual_root))
    assert dry_files == EXPECTED_FILES
    assert set(dry_files) == set(relative_generated_files(actual_root))
    assert f"Bootstrap output contract: {BOOTSTRAP_OUTPUT_CONTRACT}" in actual_result.stdout


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
    assert __version__ == "1.0.0rc1"
    assert "Forge `1.0.0rc1`" in readme
    assert f"Bootstrap output contract: `{BOOTSTRAP_OUTPUT_CONTRACT}`" in readme
    assert "No source-code directory was generated intentionally." in readme
    assert "architecture discovery" in readme
    assert "template_name:" not in readme
    assert "{{PROJECT_NAME}}" not in readme
    assert "{{BOOTSTRAP_OUTPUT_CONTRACT}}" not in readme

    handoff = (tmp_path / "demo-project" / "AI_HANDOFF.md").read_text(encoding="utf-8")
    assert f"Bootstrap output contract: `{BOOTSTRAP_OUTPUT_CONTRACT}`" in handoff
    assert "No source layout has been accepted." in handoff
    assert "Do not invent or create source structure" in handoff
    assert "architecture discovery" in handoff
    assert "{{BOOTSTRAP_OUTPUT_CONTRACT}}" not in handoff

    gitignore = (tmp_path / "demo-project" / ".gitignore").read_text(encoding="utf-8")
    assert gitignore.splitlines() == [
        ".DS_Store",
        "Thumbs.db",
        ".env",
        ".env.*",
        "dist/",
        "build/",
    ]


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


def test_bootstrap_identity_is_required_and_distinct_from_forge_version() -> None:
    templates = load_bootstrap_templates()
    readme = next(template for template in templates if template.output_name == "README.md")
    variables = default_variables("demo-project")

    assert variables["BOOTSTRAP_OUTPUT_CONTRACT"] == "forge-bootstrap/2.0.0"
    assert BOOTSTRAP_OUTPUT_CONTRACT != __version__
    variables.pop("BOOTSTRAP_OUTPUT_CONTRACT")
    with pytest.raises(ForgeInitError, match="Missing required variables"):
        render_template(readme, variables)


def test_unknown_template_variable_is_rejected() -> None:
    templates = load_bootstrap_templates()
    readme = next(template for template in templates if template.output_name == "README.md")

    with pytest.raises(ForgeInitError, match="Template uses undeclared variables"):
        validate_template(
            source=readme.source,
            metadata=readme.metadata,
            body=f"{readme.body}\n{{{{UNKNOWN_VARIABLE}}}}\n",
        )


def test_changed_template_versions_and_compatibility() -> None:
    templates = {template.output_name: template for template in load_bootstrap_templates()}

    assert {template.metadata["compatible_forge_versions"] for template in templates.values()} == {
        ">=1.0.0rc1,<2.0"
    }
    for output_name in ("README.md", "AI_HANDOFF.md", ".gitignore"):
        assert templates[output_name].metadata["version"] == "1.0.0"
        assert templates[output_name].metadata["compatible_forge_versions"] == ">=1.0.0rc1,<2.0"


def test_release_target_version_metadata_is_aligned() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    package_metadata = tomllib.loads(
        (repository_root / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert __version__ == "1.0.0rc1"
    assert package_metadata["project"]["version"] == "1.0.0rc1"
    assert default_variables("demo-project")["FORGE_VERSION"] == "1.0.0rc1"


def test_forge_internal_package_remains_present() -> None:
    repository_root = Path(__file__).resolve().parents[1]

    assert (repository_root / "forge").is_dir()
    assert (repository_root / "forge" / "bootstrap.py").is_file()


def test_template_compatibility_validation() -> None:
    assert is_version_compatible("0.2.0", ">=0.2,<0.3")
    assert not is_version_compatible("0.1.0", ">=0.2,<0.3")
    assert not is_version_compatible("0.3.0", ">=0.2,<0.3")


@pytest.mark.parametrize(
    ("version", "constraint", "expected"),
    [
        ("1.0.0rc1", ">=1.0.0rc1,<2.0", True),
        ("1.0.0rc1", ">=1.0", False),
        ("1.0.0rc1", "<1.0", True),
        ("1.0.0", ">1.0.0rc99", True),
        ("1.0.0rc10", ">1.0.0rc2", True),
        ("1.0.0rc1", "==1.0.0", False),
        ("1.0", "==1.0.0", True),
        ("2.0", ">=1.0.0rc1,<2.0", False),
    ],
)
def test_candidate_template_compatibility(version, constraint, expected):
    assert is_version_compatible(version, constraint) is expected


@pytest.mark.parametrize("version", ["", "1..0", "-1.0", "1.0.0.1", "1.0.0rc", "1.0.0bad"])
def test_malformed_versions_fail_with_domain_error(version):
    with pytest.raises(ForgeInitError, match="Unsupported version format"):
        is_version_compatible(version, ">=1.0.0rc1")
    with pytest.raises(ForgeInitError, match="Unsupported version format"):
        is_version_compatible("1.0.0rc1", ">=" + version)
