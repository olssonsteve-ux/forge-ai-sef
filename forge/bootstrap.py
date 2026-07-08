from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import __version__

FOLDER_PATHS = (
    "docs",
    "docs/architecture",
    "docs/contracts",
    "docs/decisions",
    "docs/vision",
    "forge",
    "standards",
    "templates",
    "tests",
)

TEMPLATE_OUTPUTS = {
    "README.template.md": "README.md",
    "PROJECT_STATE.template.md": "PROJECT_STATE.md",
    "PROJECT_BRAIN.template.md": "PROJECT_BRAIN.md",
    "AI_HANDOFF.template.md": "AI_HANDOFF.md",
    "CHANGELOG.template.md": "CHANGELOG.md",
    "ROADMAP.template.md": "ROADMAP.md",
    "LICENSE.template": "LICENSE",
    "gitignore.template": ".gitignore",
}

SUPPORTED_VARIABLES = {
    "PROJECT_NAME",
    "PROJECT_DESCRIPTION",
    "AUTHOR",
    "LICENSE",
    "YEAR",
    "FORGE_VERSION",
    "CREATED_DATE",
}

VARIABLE_PATTERN = re.compile(r"{{([A-Z0-9_]+)}}")
PROJECT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ForgeInitError(Exception):
    """Raised when project initialization cannot continue."""


@dataclass(frozen=True)
class InitResult:
    target: Path
    folders: tuple[Path, ...]
    files: tuple[Path, ...]


@dataclass(frozen=True)
class Template:
    source: Path
    output_name: str
    metadata: dict[str, object]
    body: str


def init_project(project_name: str, base_dir: Path, dry_run: bool = False) -> InitResult:
    target = (base_dir / project_name).resolve()
    validate_project_name(project_name)
    validate_target(target=target, base_dir=base_dir.resolve())

    templates = load_bootstrap_templates()
    variables = default_variables(project_name)
    rendered_files = [
        (template.output_name, render_template(template, variables)) for template in templates
    ]

    output_names = [output_name for output_name, _ in rendered_files]
    if len(output_names) != len(set(output_names)):
        raise ForgeInitError("Generated file plan contains duplicate output paths.")

    folders = tuple(target / folder for folder in FOLDER_PATHS)
    files = tuple(target / output_name for output_name, _ in rendered_files)

    if dry_run:
        return InitResult(target=target, folders=folders, files=files)

    try:
        target.mkdir(parents=True, exist_ok=True)
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
        for output_name, content in rendered_files:
            destination = target / output_name
            with destination.open("x", encoding="utf-8") as file:
                file.write(content)
    except OSError as error:
        raise ForgeInitError(f"Failed while writing '{target}': {error}") from error

    return InitResult(target=target, folders=folders, files=files)


def validate_project_name(project_name: str) -> None:
    if not project_name or not project_name.strip():
        raise ForgeInitError("Project name is required.")
    if project_name in {".", ".."}:
        raise ForgeInitError("Project name must not be '.' or '..'.")
    if any(separator in project_name for separator in ("/", "\\")):
        raise ForgeInitError("Project name must not contain path separators.")
    if ".." in project_name:
        raise ForgeInitError("Project name must not contain path traversal.")
    if not PROJECT_NAME_PATTERN.match(project_name):
        raise ForgeInitError(
            "Project name must use letters, numbers, dots, hyphens, or underscores."
        )


def validate_target(target: Path, base_dir: Path) -> None:
    try:
        target.relative_to(base_dir)
    except ValueError as error:
        raise ForgeInitError("Target path must stay within the current directory.") from error

    if target.exists() and any(target.iterdir()):
        raise ForgeInitError(f"Target directory already exists and is not empty: {target}")

    parent = target.parent
    if not parent.exists():
        raise ForgeInitError(f"Target parent directory does not exist: {parent}")
    if not parent.is_dir():
        raise ForgeInitError(f"Target parent is not a directory: {parent}")


def load_bootstrap_templates() -> tuple[Template, ...]:
    template_dir = repository_root() / "templates" / "bootstrap"
    if not template_dir.is_dir():
        raise ForgeInitError(f"Bootstrap template directory is missing: {template_dir}")

    templates: list[Template] = []
    for template_name, output_name in TEMPLATE_OUTPUTS.items():
        source = template_dir / template_name
        if not source.is_file():
            raise ForgeInitError(f"Required bootstrap template is missing: {source}")
        metadata, body = parse_template(source)
        validate_template(source=source, metadata=metadata, body=body)
        templates.append(
            Template(source=source, output_name=output_name, metadata=metadata, body=body)
        )
    return tuple(templates)


def parse_template(source: Path) -> tuple[dict[str, object], str]:
    content = source.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ForgeInitError(f"Template metadata block is missing: {source}")

    try:
        _, metadata_text, body = content.split("---\n", 2)
    except ValueError as error:
        raise ForgeInitError(f"Template metadata block is invalid: {source}") from error

    return parse_metadata(metadata_text), body


def parse_metadata(metadata_text: str) -> dict[str, object]:
    metadata: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in metadata_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - "):
            if current_list_key is None:
                raise ForgeInitError("Template metadata list item has no parent key.")
            value = line[4:].strip().strip('"')
            list_value = metadata.setdefault(current_list_key, [])
            if not isinstance(list_value, list):
                raise ForgeInitError(f"Template metadata key is not a list: {current_list_key}")
            list_value.append(value)
            continue

        current_list_key = None
        if ":" not in line:
            raise ForgeInitError(f"Template metadata line is invalid: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            metadata[key] = []
            current_list_key = key
        elif value == "[]":
            metadata[key] = []
        else:
            metadata[key] = value.strip('"')

    return metadata


def validate_template(source: Path, metadata: dict[str, object], body: str) -> None:
    required_fields = {
        "template_name",
        "version",
        "compatible_forge_versions",
        "description",
        "variables",
        "required_variables",
        "optional_variables",
    }
    missing_fields = sorted(required_fields - metadata.keys())
    if missing_fields:
        raise ForgeInitError(
            f"Template metadata missing fields in {source}: {', '.join(missing_fields)}"
        )

    variables = metadata_list(metadata, "variables")
    required_variables = metadata_list(metadata, "required_variables")
    optional_variables = metadata_list(metadata, "optional_variables")

    declared = set(variables)
    if declared != set(required_variables) | set(optional_variables):
        raise ForgeInitError(f"Template variable lists disagree in {source}")
    if not declared <= SUPPORTED_VARIABLES:
        unknown = ", ".join(sorted(declared - SUPPORTED_VARIABLES))
        raise ForgeInitError(f"Template declares unsupported variables in {source}: {unknown}")

    used = set(VARIABLE_PATTERN.findall(body))
    if not used <= declared:
        unknown = ", ".join(sorted(used - declared))
        raise ForgeInitError(f"Template uses undeclared variables in {source}: {unknown}")

    compatibility = metadata["compatible_forge_versions"]
    if not isinstance(compatibility, str) or not is_version_compatible(__version__, compatibility):
        raise ForgeInitError(f"Template is not compatible with Forge {__version__}: {source}")

    malformed = re.search(r"{{[^}]*$|^[^{]*}}", body)
    if malformed:
        raise ForgeInitError(f"Template variable syntax is malformed in {source}")


def metadata_list(metadata: dict[str, object], key: str) -> list[str]:
    value = metadata[key]
    if not isinstance(value, list):
        raise ForgeInitError(f"Template metadata field must be a list: {key}")
    return value


def render_template(template: Template, variables: dict[str, str]) -> str:
    required = metadata_list(template.metadata, "required_variables")
    missing = [name for name in required if not variables.get(name)]
    if missing:
        raise ForgeInitError(
            f"Missing required variables for {template.source.name}: {', '.join(missing)}"
        )

    used = set(VARIABLE_PATTERN.findall(template.body))
    unknown = used - variables.keys()
    if unknown:
        raise ForgeInitError(
            f"Unknown variables in {template.source.name}: {', '.join(sorted(unknown))}"
        )

    def replace(match: re.Match[str]) -> str:
        return variables.get(match.group(1), "")

    return VARIABLE_PATTERN.sub(replace, template.body).lstrip("\n")


def default_variables(project_name: str) -> dict[str, str]:
    today = date.today()
    return {
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": "A Forge-governed software project.",
        "AUTHOR": "",
        "LICENSE": "License TBD",
        "YEAR": str(today.year),
        "FORGE_VERSION": __version__,
        "CREATED_DATE": today.isoformat(),
    }


def is_version_compatible(version: str, compatibility: str) -> bool:
    version_tuple = parse_version(version)
    for raw_part in compatibility.split(","):
        part = raw_part.strip()
        if part.startswith(">="):
            if version_tuple < parse_version(part[2:]):
                return False
        elif part.startswith(">"):
            if version_tuple <= parse_version(part[1:]):
                return False
        elif part.startswith("<="):
            if version_tuple > parse_version(part[2:]):
                return False
        elif part.startswith("<"):
            if version_tuple >= parse_version(part[1:]):
                return False
        elif part.startswith("=="):
            if version_tuple != parse_version(part[2:]):
                return False
        else:
            raise ForgeInitError(f"Unsupported template compatibility constraint: {part}")
    return True


def parse_version(version: str) -> tuple[int, int, int]:
    parts = version.strip().split(".")
    if len(parts) > 3:
        raise ForgeInitError(f"Unsupported version format: {version}")
    numbers = [int(part) for part in parts]
    while len(numbers) < 3:
        numbers.append(0)
    return tuple(numbers)


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]
