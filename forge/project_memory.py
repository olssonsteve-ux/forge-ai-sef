from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


class ProjectMemoryError(Exception):
    """An expected project-memory read or parse failure."""


@dataclass(frozen=True)
class SectionFact:
    heading: str
    content: str


@dataclass(frozen=True)
class DocumentFact:
    relative_path: str
    content: str
    sections: dict[str, tuple[SectionFact, ...]]


@dataclass(frozen=True)
class ReferenceFact:
    identifier: str
    directory: str
    prefix: str
    artifact_type: str


@dataclass(frozen=True)
class ResolutionFact:
    reference: ReferenceFact
    matches: tuple[Path, ...]


@dataclass(frozen=True)
class StatusEvidence:
    values: tuple[str, ...]


HEADING_PATTERN = re.compile(r"^## ([^\r\n]+)$", re.MULTILINE)
COMMIT_PATTERN = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{40}(?![0-9A-Fa-f])")

REFERENCE_PATTERNS: tuple[tuple[re.Pattern[str], str, str, str], ...] = (
    (re.compile(r"(?<![A-Z0-9-])ADR(?: |-)\d{4}(?![A-Z0-9-])"), "docs/decisions", "", "ADR"),
    (re.compile(r"(?<![A-Z0-9-])FCS-\d{3}(?![A-Z0-9-])"), "docs/capabilities", "", "FCS"),
    (
        re.compile(r"(?<![A-Z0-9-])CS-\d{3}\.\d+(?![A-Z0-9-]|\.\d)"),
        "docs/capabilities",
        "",
        "Capability Slice",
    ),
    (
        re.compile(r"(?<![A-Z0-9-])EB-\d{3}(?:\.\d+)?(?![A-Z0-9-]|\.\d)"),
        "docs/engineering",
        "",
        "Engineering Brief",
    ),
    (
        re.compile(r"(?<![A-Z0-9-])DAR-(?:CS|EB|AR)-\d{4}(?![A-Z0-9-])"),
        "docs/reviews",
        "",
        "Review",
    ),
    (re.compile(r"(?<![A-Z0-9-])PRR-\d{4}(?![A-Z0-9-])"), "docs/reviews", "", "Review"),
)


def load_document(root: Path, relative_path: str) -> DocumentFact:
    path = root / relative_path
    try:
        content = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    except (OSError, UnicodeError) as exc:
        raise ProjectMemoryError(f"Could not read {relative_path} as UTF-8.") from exc
    return DocumentFact(relative_path, content, extract_sections(content))


def extract_sections(content: str) -> dict[str, tuple[SectionFact, ...]]:
    matches = list(HEADING_PATTERN.finditer(content))
    sections: dict[str, list[SectionFact]] = {}
    for index, match in enumerate(matches):
        start = match.end()
        if start < len(content) and content[start] == "\n":
            start += 1
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        heading = match.group(1)
        sections.setdefault(heading, []).append(SectionFact(heading, content[start:end]))
    return {heading: tuple(values) for heading, values in sections.items()}


def has_structural_content(content: str) -> bool:
    without_comments = _remove_html_comments(content)
    return any(
        line.strip() and not line.lstrip().startswith("#") for line in without_comments.splitlines()
    )


def first_nonempty_list_item(content: str) -> str | None:
    for line in content.splitlines():
        match = re.match(r"^\s*(?:[-*+] |\d+[.)] )(.*)$", line)
        if match and match.group(1).strip():
            return match.group(1).strip()
    return None


def claim_units(content: str) -> tuple[str, ...]:
    units: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--"):
            continue
        stripped = re.sub(r"^(?:[-*+] |\d+[.)] )", "", stripped)
        units.extend(part.strip() for part in re.split(r"(?<=[.!?])\s+", stripped) if part.strip())
    return tuple(units)


def parse_references(content: str) -> tuple[ReferenceFact, ...]:
    content = _reference_text(content)
    found: list[tuple[int, ReferenceFact]] = []
    for pattern, directory, _, artifact_type in REFERENCE_PATTERNS:
        for match in pattern.finditer(content):
            identifier = match.group(0)
            if artifact_type == "ADR":
                number = identifier.replace("ADR", "", 1).lstrip(" -")
                prefix = f"{number}-"
            else:
                prefix = f"{identifier}-"
            found.append(
                (match.start(), ReferenceFact(identifier, directory, prefix, artifact_type))
            )
    unique: dict[tuple[str, str], tuple[int, ReferenceFact]] = {}
    for position, fact in found:
        unique.setdefault((fact.identifier, fact.directory), (position, fact))
    return tuple(fact for _, fact in sorted(unique.values(), key=lambda value: value[0]))


def parse_commit_hashes(content: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(match.group(0) for match in COMMIT_PATTERN.finditer(content)))


def resolve_reference(root: Path, reference: ReferenceFact) -> ResolutionFact:
    directory = root / reference.directory
    try:
        if not directory.is_dir():
            return ResolutionFact(reference, ())
        matches = tuple(
            sorted(
                (
                    path
                    for path in directory.iterdir()
                    if path.is_file()
                    and path.suffix == ".md"
                    and path.name.startswith(reference.prefix)
                ),
                key=lambda path: path.name,
            )
        )
    except OSError as exc:
        raise ProjectMemoryError(f"Could not inspect {reference.directory}/.") from exc
    return ResolutionFact(reference, matches)


def explicit_status_evidence(document: DocumentFact) -> StatusEvidence:
    values: list[str] = []
    for line in document.content.splitlines():
        if line.startswith("Status:"):
            value = line.removeprefix("Status:").strip()
            if value:
                values.append(normalize_label(value))
            break
        if line.startswith("## "):
            break
    for section in document.sections.get("Status", ()):
        for line in section.content.splitlines():
            if line.strip() and not line.lstrip().startswith("#"):
                values.append(normalize_label(line))
                break
    return StatusEvidence(tuple(value for value in values if value))


def normalize_label(value: str) -> str:
    value = value.replace("`", "").strip().rstrip(".,;:")
    return " ".join(value.split()).casefold()


def contains_exact_phrase(content: str, phrase: str) -> bool:
    return (
        re.search(rf"(?<![A-Za-z]){re.escape(phrase)}(?![A-Za-z])", content, re.IGNORECASE)
        is not None
    )


def _remove_html_comments(content: str) -> str:
    result: list[str] = []
    cursor = 0
    while cursor < len(content):
        start = content.find("<!--", cursor)
        if start == -1:
            result.append(content[cursor:])
            break
        result.append(content[cursor:start])
        end = content.find("-->", start + 4)
        if end == -1:
            break
        cursor = end + 3
    return "".join(result)


def _reference_text(content: str) -> str:
    content = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", content)
    content = re.sub(r"https?://\S+", "", content, flags=re.IGNORECASE)
    content = re.sub(r"(?<!\S)(?:[A-Za-z]:[\\/]|\.{1,2}[\\/]|docs[\\/])\S+", "", content)
    return content
