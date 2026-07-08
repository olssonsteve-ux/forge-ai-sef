from __future__ import annotations

import subprocess
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class StatusState(StrEnum):
    OK = "OK"
    WARNING = "WARNING"
    MISSING = "MISSING"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class StatusItem:
    label: str
    state: StatusState
    message: str


@dataclass(frozen=True)
class StatusCategory:
    name: str
    state: StatusState
    message: str
    items: tuple[StatusItem, ...]


@dataclass(frozen=True)
class StatusReport:
    repository: Path
    categories: tuple[StatusCategory, ...]


class StatusServiceError(Exception):
    """Raised when status evaluation cannot start."""


ROOT_ARTIFACTS = {
    "CONSTITUTION.md": "Constitution",
    "AI_ENGINEERING_CONDUCT.md": "AI Engineering Conduct",
    "PROJECT_STATE.md": "Project State",
    "PROJECT_BRAIN.md": "Project Brain",
    "AI_HANDOFF.md": "AI Handoff",
    "CHANGELOG.md": "Changelog",
    "README.md": "README",
}

DIRECTORY_ARTIFACTS = {
    "docs": "Documentation directory",
    "docs/decisions": "ADR directory",
    "docs/capabilities": "Capability directory",
    "docs/engineering": "Engineering Brief directory",
    "docs/reviews": "Review directory",
    "templates": "Template directory",
    "standards": "Standards directory",
    "tests": "Tests directory",
    ".github/workflows": "GitHub Actions workflow directory",
}


def evaluate_status(repository: Path) -> StatusReport:
    root = repository.resolve()
    if not root.exists():
        raise StatusServiceError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise StatusServiceError(f"Repository path is not a directory: {root}")

    categories = (
        _constitutional_status(root),
        _governance_status(root),
        _documentation_status(root),
        _capability_status(root),
        _engineering_workflow_status(root),
        _testing_status(root),
        _release_status(root),
        _runtime_memory_status(root),
        _repository_status(root),
    )
    return StatusReport(repository=root, categories=categories)


def render_status_report(report: StatusReport) -> str:
    lines = [
        "Forge status",
        f"Repository: {report.repository}",
        "",
        "This is informational status only. It does not approve releases or modify files.",
        "",
    ]
    for category in report.categories:
        lines.append(f"{category.name}: {category.state.value}")
        lines.append(f"  {category.message}")
        for item in category.items:
            lines.append(f"  - {item.label}: {item.state.value} - {item.message}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _constitutional_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Constitutional Status",
        (
            _file_item(root, "CONSTITUTION.md", ROOT_ARTIFACTS["CONSTITUTION.md"]),
            _file_item(
                root,
                "AI_ENGINEERING_CONDUCT.md",
                ROOT_ARTIFACTS["AI_ENGINEERING_CONDUCT.md"],
            ),
        ),
    )


def _governance_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Governance Status",
        (
            _directory_item(root, "docs/decisions", DIRECTORY_ARTIFACTS["docs/decisions"]),
            _directory_item(root, "standards", DIRECTORY_ARTIFACTS["standards"]),
            _directory_item(root, "templates", DIRECTORY_ARTIFACTS["templates"]),
        ),
    )


def _documentation_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Documentation Status",
        (
            _file_item(root, "README.md", ROOT_ARTIFACTS["README.md"]),
            _file_item(root, "CHANGELOG.md", ROOT_ARTIFACTS["CHANGELOG.md"]),
            _directory_item(root, "docs", DIRECTORY_ARTIFACTS["docs"]),
        ),
    )


def _capability_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Capability Status",
        (
            _directory_item(
                root,
                "docs/capabilities",
                DIRECTORY_ARTIFACTS["docs/capabilities"],
            ),
            _has_matching_file_item(
                root,
                "docs/capabilities",
                "FCS-*.md",
                "Capability Specifications",
            ),
            _has_matching_file_item(
                root,
                "docs/capabilities",
                "CS-*.md",
                "Capability Slices",
            ),
        ),
    )


def _engineering_workflow_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Engineering Workflow Status",
        (
            _directory_item(
                root,
                "docs/engineering",
                DIRECTORY_ARTIFACTS["docs/engineering"],
            ),
            _has_matching_file_item(
                root,
                "docs/engineering",
                "EB-*.md",
                "Engineering Briefs",
            ),
            _directory_item(root, "docs/reviews", DIRECTORY_ARTIFACTS["docs/reviews"]),
        ),
    )


def _testing_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Testing Status",
        (
            _directory_item(root, "tests", DIRECTORY_ARTIFACTS["tests"]),
            _file_item(root, "pyproject.toml", "Python project configuration"),
        ),
    )


def _release_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Release Status",
        (
            _file_item(root, "CHANGELOG.md", ROOT_ARTIFACTS["CHANGELOG.md"]),
            _directory_item(root, "docs/release", "Release documentation"),
        ),
    )


def _runtime_memory_status(root: Path) -> StatusCategory:
    return _category_from_items(
        "Runtime Memory Status",
        (
            _file_item(root, "PROJECT_STATE.md", ROOT_ARTIFACTS["PROJECT_STATE.md"]),
            _file_item(root, "PROJECT_BRAIN.md", ROOT_ARTIFACTS["PROJECT_BRAIN.md"]),
            _file_item(root, "AI_HANDOFF.md", ROOT_ARTIFACTS["AI_HANDOFF.md"]),
        ),
    )


def _repository_status(root: Path) -> StatusCategory:
    workflow_item = _directory_item(
        root,
        ".github/workflows",
        DIRECTORY_ARTIFACTS[".github/workflows"],
    )
    git_item = _git_status_item(root)
    return _category_from_items("Repository Status", (workflow_item, git_item))


def _file_item(root: Path, relative_path: str, label: str) -> StatusItem:
    path = root / relative_path
    if path.is_file():
        return StatusItem(label=label, state=StatusState.OK, message=f"Found {relative_path}.")
    return StatusItem(label=label, state=StatusState.MISSING, message=f"Missing {relative_path}.")


def _directory_item(root: Path, relative_path: str, label: str) -> StatusItem:
    path = root / relative_path
    if path.is_dir():
        return StatusItem(label=label, state=StatusState.OK, message=f"Found {relative_path}/.")
    return StatusItem(label=label, state=StatusState.MISSING, message=f"Missing {relative_path}/.")


def _has_matching_file_item(
    root: Path, relative_directory: str, pattern: str, label: str
) -> StatusItem:
    directory = root / relative_directory
    if not directory.is_dir():
        return StatusItem(
            label=label,
            state=StatusState.NOT_APPLICABLE,
            message=f"Cannot inspect {pattern}; {relative_directory}/ is missing.",
        )
    if any(directory.glob(pattern)):
        return StatusItem(label=label, state=StatusState.OK, message=f"Found {pattern}.")
    return StatusItem(label=label, state=StatusState.MISSING, message=f"Missing {pattern}.")


def _git_status_item(root: Path) -> StatusItem:
    if not (root / ".git").exists():
        return StatusItem(
            label="Git repository",
            state=StatusState.NOT_APPLICABLE,
            message="No .git metadata found; file-based status was still evaluated.",
        )

    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return StatusItem(
            label="Git working tree",
            state=StatusState.WARNING,
            message="Git metadata exists, but Git status could not be inspected.",
        )

    if result.returncode != 0:
        return StatusItem(
            label="Git working tree",
            state=StatusState.WARNING,
            message="Git status returned a non-zero exit code.",
        )
    if result.stdout.strip():
        return StatusItem(
            label="Git working tree",
            state=StatusState.WARNING,
            message="Working tree has uncommitted changes.",
        )
    return StatusItem(
        label="Git working tree",
        state=StatusState.OK,
        message="Working tree appears clean.",
    )


def _category_from_items(name: str, items: tuple[StatusItem, ...]) -> StatusCategory:
    state = _rollup_state(items)
    if state == StatusState.OK:
        message = "Expected artifacts were found."
    elif state == StatusState.MISSING:
        message = "One or more expected artifacts are missing."
    elif state == StatusState.WARNING:
        message = "Status was evaluated with warnings."
    elif state == StatusState.BLOCKED:
        message = "Status evaluation was blocked."
    else:
        message = "Status does not apply to this repository."
    return StatusCategory(name=name, state=state, message=message, items=items)


def _rollup_state(items: tuple[StatusItem, ...]) -> StatusState:
    states = {item.state for item in items}
    if StatusState.BLOCKED in states:
        return StatusState.BLOCKED
    if StatusState.MISSING in states:
        return StatusState.MISSING
    if StatusState.WARNING in states:
        return StatusState.WARNING
    if states == {StatusState.NOT_APPLICABLE}:
        return StatusState.NOT_APPLICABLE
    return StatusState.OK
