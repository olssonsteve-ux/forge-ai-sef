from __future__ import annotations

import re
import subprocess
import tomllib
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from forge.project_memory import (
    DocumentFact,
    ProjectMemoryError,
    ReferenceFact,
    claim_units,
    contains_exact_phrase,
    explicit_status_evidence,
    first_nonempty_list_item,
    has_structural_content,
    load_document,
    normalize_label,
    parse_commit_hashes,
    parse_references,
    resolve_reference,
)


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

VERSION_TAG_PATTERN = re.compile(r"^v(\d+\.\d+\.\d+)$")
VERSION_PATTERN = re.compile(r"\bv?(\d+\.\d+\.\d+)\b")
CHANGELOG_HEADING_PATTERN = re.compile(r"^## \[(v?\d+\.\d+\.\d+)\]", re.MULTILINE)


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
        _project_memory_health_status(root),
        _version_consistency_status(root),
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
            _project_configuration_item(root),
        ),
    )


def _project_configuration_item(root: Path) -> StatusItem:
    for name in ("forge.toml", "pyproject.toml", "package.json", "Cargo.toml", "go.mod"):
        if (root / name).is_file():
            return _file_item(root, name, "Project verification configuration")
    for pattern in ("*.sln", "*.slnx", "*.csproj"):
        if any(root.glob(pattern)):
            return StatusItem(
                label="Project verification configuration",
                state=StatusState.OK,
                message=f"Found {pattern}; use forge.toml for explicit checks.",
            )
    return StatusItem(
        label="Project verification configuration",
        state=StatusState.MISSING,
        message="No supported project configuration found; add forge.toml.",
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


PRIMARY_MEMORY_FILES = ("PROJECT_STATE.md", "PROJECT_BRAIN.md", "AI_HANDOFF.md")
REQUIRED_MEMORY_SECTIONS = {
    "PROJECT_STATE.md": (
        "Status",
        "Current Version",
        "Current Objective",
        "What Exists",
        "What Does Not Exist",
        "Architectural Posture",
        "Next Recommended Work",
    ),
    "PROJECT_BRAIN.md": (
        "Core Identity",
        "Guiding Beliefs",
        "Product Shape",
        "Important Boundaries",
        "Current Decisions",
        "Open Questions",
    ),
    "AI_HANDOFF.md": (
        "Role Context",
        "Current Repository State",
        "Current Architectural Intent",
        "Instructions For Future AI Agents",
        "Immediate Next Step",
    ),
}
REFERENCE_SECTIONS = {
    "PROJECT_STATE.md": ("Status", "Current Objective", "Next Recommended Work"),
    "AI_HANDOFF.md": ("Current Repository State", "Immediate Next Step"),
}

LIFECYCLE_LABELS = {
    "Capability Slice": {
        "draft": "draft",
        "specified": "specified",
        "approved": "dar approved",
        "reviewed": "implementation reviewed",
        "dar approved": "dar approved",
        "implementation ready": "implementation ready",
        "implemented": "implemented",
        "implementation reviewed": "implementation reviewed",
        "closed": "closed",
        "rejected": "rejected",
        "withdrawn": "withdrawn",
        "archived": "archived",
        "superseded": "superseded",
        "deprecated": "deprecated",
    },
    "Engineering Brief": {
        label: label
        for label in (
            "draft",
            "approved",
            "implementation ready",
            "implemented",
            "implementation reviewed",
            "closed",
            "rejected",
            "withdrawn",
            "archived",
            "superseded",
            "deprecated",
        )
    },
    "ADR": {
        "proposed": "proposed",
        "accepted": "approved",
        "rejected": "rejected",
        "deprecated": "deprecated",
        "superseded": "superseded",
    },
    "Review": {
        "completed": "completed",
        "pass": "pass",
        "pass with conditions": "pass with conditions",
        "fail": "fail",
    },
}
RELEASE_LABELS = (
    "planned",
    "release candidate",
    "released",
    "post release reviewed",
    "deprecated",
)


def _project_memory_health_status(root: Path) -> StatusCategory:
    if not _has_forge_memory_signal(root):
        return _category_from_items(
            "Project Memory Health",
            (
                StatusItem(
                    label="PMH-001 required memory files",
                    state=StatusState.NOT_APPLICABLE,
                    message="No Forge project-memory or root governance signal was found.",
                ),
            ),
        )

    documents: dict[str, DocumentFact] = {}
    read_errors: dict[str, str] = {}
    items: list[StatusItem] = []
    items.extend(_pmh_required_files(root, documents, read_errors))
    items.extend(_pmh_required_sections(documents))
    items.extend(_pmh_current_content(documents))
    items.extend(_pmh_reference_integrity(root, documents))
    items.extend(_pmh_active_work_coherence(documents))
    items.extend(_pmh_lifecycle_coherence(root, documents))
    items.extend(_pmh_stale_handoff_gates(root, documents))
    items.extend(_pmh_release_lifecycle(root, documents))
    items.extend(_pmh_current_adr_authority(root, documents))
    return _category_from_items("Project Memory Health", tuple(items))


def _has_forge_memory_signal(root: Path) -> bool:
    return any(
        (root / path).exists()
        for path in (*PRIMARY_MEMORY_FILES, "CONSTITUTION.md", "AI_ENGINEERING_CONDUCT.md")
    )


def _pmh_required_files(
    root: Path,
    documents: dict[str, DocumentFact],
    read_errors: dict[str, str],
) -> list[StatusItem]:
    items: list[StatusItem] = []
    for relative_path in PRIMARY_MEMORY_FILES:
        path = root / relative_path
        if not path.is_file():
            items.append(_pmh_item("PMH-001", StatusState.MISSING, f"Missing {relative_path}."))
            continue
        try:
            documents[relative_path] = load_document(root, relative_path)
        except ProjectMemoryError as exc:
            read_errors[relative_path] = str(exc)
            items.append(_pmh_item("PMH-001", StatusState.BLOCKED, str(exc)))
        else:
            items.append(_pmh_item("PMH-001", StatusState.OK, f"Read {relative_path}."))
    return items


def _pmh_required_sections(documents: dict[str, DocumentFact]) -> list[StatusItem]:
    findings: list[StatusItem] = []
    checked = 0
    for relative_path, headings in REQUIRED_MEMORY_SECTIONS.items():
        document = documents.get(relative_path)
        if document is None:
            continue
        for heading in headings:
            checked += 1
            sections = document.sections.get(heading, ())
            if not sections:
                findings.append(
                    _pmh_item(
                        "PMH-002", StatusState.MISSING, f"{relative_path} is missing ## {heading}."
                    )
                )
            elif len(sections) > 1:
                findings.append(
                    _pmh_item(
                        "PMH-002",
                        StatusState.WARNING,
                        f"{relative_path} contains duplicate ## {heading} headings.",
                    )
                )
            elif not has_structural_content(sections[0].content):
                findings.append(
                    _pmh_item(
                        "PMH-002",
                        StatusState.MISSING,
                        f"{relative_path} ## {heading} is structurally empty.",
                    )
                )
    if findings:
        return findings
    state = StatusState.OK if checked else StatusState.NOT_APPLICABLE
    message = (
        f"Validated {checked} required project-memory sections."
        if checked
        else "No readable primary file was available for section checks."
    )
    return [_pmh_item("PMH-002", state, message)]


def _pmh_current_content(documents: dict[str, DocumentFact]) -> list[StatusItem]:
    targets = (
        ("PROJECT_STATE.md", "Status"),
        ("PROJECT_STATE.md", "Current Objective"),
        ("AI_HANDOFF.md", "Immediate Next Step"),
    )
    findings: list[StatusItem] = []
    checked = 0
    for relative_path, heading in targets:
        document = documents.get(relative_path)
        if document is None:
            continue
        sections = document.sections.get(heading, ())
        if len(sections) != 1:
            continue
        checked += 1
        if not has_structural_content(sections[0].content):
            findings.append(
                _pmh_item(
                    "PMH-003",
                    StatusState.MISSING,
                    f"{relative_path} ## {heading} has no explicit structural value.",
                )
            )
    if findings:
        return findings
    state = StatusState.OK if checked else StatusState.NOT_APPLICABLE
    message = (
        f"Validated {checked} current status/objective sections."
        if checked
        else "No eligible current section was available."
    )
    return [_pmh_item("PMH-003", state, message)]


def _pmh_reference_integrity(root: Path, documents: dict[str, DocumentFact]) -> list[StatusItem]:
    references = _active_references(documents)
    hashes = _active_commit_hashes(documents)
    findings: list[StatusItem] = []
    for reference in references:
        try:
            resolution = resolve_reference(root, reference)
        except ProjectMemoryError as exc:
            findings.append(_pmh_item("PMH-004", StatusState.BLOCKED, str(exc)))
            continue
        if not resolution.matches:
            findings.append(
                _pmh_item(
                    "PMH-004",
                    StatusState.MISSING,
                    f"{reference.identifier} did not resolve under {reference.directory}/.",
                )
            )
        elif len(resolution.matches) > 1:
            names = ", ".join(path.name for path in resolution.matches)
            findings.append(
                _pmh_item(
                    "PMH-004", StatusState.WARNING, f"{reference.identifier} is ambiguous: {names}."
                )
            )
        else:
            try:
                load_document(root, resolution.matches[0].relative_to(root).as_posix())
            except ProjectMemoryError:
                findings.append(
                    _pmh_item(
                        "PMH-004",
                        StatusState.BLOCKED,
                        f"Could not read {resolution.matches[0].relative_to(root).as_posix()}.",
                    )
                )
    for commit_hash in hashes:
        state = _commit_exists(root, commit_hash)
        if state is False:
            findings.append(
                _pmh_item(
                    "PMH-004",
                    StatusState.MISSING,
                    f"Commit {commit_hash} does not resolve locally.",
                )
            )
        elif state is None:
            findings.append(
                _pmh_item(
                    "PMH-004",
                    StatusState.NOT_APPLICABLE,
                    f"Commit {commit_hash} was not checked because Git metadata is unavailable.",
                )
            )
    if findings:
        return findings
    count = len(references) + len(hashes)
    state = StatusState.OK if count else StatusState.NOT_APPLICABLE
    message = (
        f"Resolved {count} explicit active reference(s)."
        if count
        else "No supported active artifact reference was present."
    )
    return [_pmh_item("PMH-004", state, message)]


def _pmh_active_work_coherence(documents: dict[str, DocumentFact]) -> list[StatusItem]:
    state_document = documents.get("PROJECT_STATE.md")
    handoff_document = documents.get("AI_HANDOFF.md")
    if state_document is None or handoff_document is None:
        return [
            _pmh_item(
                "PMH-005",
                StatusState.NOT_APPLICABLE,
                "Both Project State and AI Handoff are required for active-work comparison.",
            )
        ]
    state_text = _single_section_content(state_document, "Current Objective")
    next_text = _single_section_content(state_document, "Next Recommended Work")
    handoff_text = _single_section_content(handoff_document, "Immediate Next Step")
    first_next = first_nonempty_list_item(next_text or "") or ""
    state_ids = {ref.identifier for ref in parse_references(f"{state_text or ''}\n{first_next}")}
    handoff_ids = {ref.identifier for ref in parse_references(handoff_text or "")}
    if not state_ids or not handoff_ids:
        return [
            _pmh_item(
                "PMH-005",
                StatusState.NOT_APPLICABLE,
                "One active-work side contains no governed identifier.",
            )
        ]
    if state_ids.isdisjoint(handoff_ids):
        return [
            _pmh_item(
                "PMH-005",
                StatusState.WARNING,
                "Project State identifiers "
                f"{sorted(state_ids)} and AI Handoff identifiers "
                f"{sorted(handoff_ids)} are disjoint.",
            )
        ]
    return [
        _pmh_item(
            "PMH-005",
            StatusState.OK,
            f"Active-work identifiers overlap: {sorted(state_ids & handoff_ids)}.",
        )
    ]


def _pmh_lifecycle_coherence(root: Path, documents: dict[str, DocumentFact]) -> list[StatusItem]:
    findings: list[StatusItem] = []
    checked = 0
    for unit in _active_claim_units(documents):
        for reference in parse_references(unit):
            claimed = _lifecycle_claim(unit, reference)
            if claimed is None:
                continue
            checked += 1
            try:
                resolution = resolve_reference(root, reference)
            except ProjectMemoryError as exc:
                findings.append(_pmh_item("PMH-006", StatusState.BLOCKED, str(exc)))
                continue
            if not resolution.matches:
                findings.append(
                    _pmh_item(
                        "PMH-006",
                        StatusState.MISSING,
                        f"Lifecycle claim target {reference.identifier} is missing.",
                    )
                )
            elif len(resolution.matches) > 1:
                findings.append(
                    _pmh_item(
                        "PMH-006",
                        StatusState.WARNING,
                        f"Lifecycle claim target {reference.identifier} is ambiguous.",
                    )
                )
            else:
                try:
                    document = load_document(
                        root, resolution.matches[0].relative_to(root).as_posix()
                    )
                    evidence = explicit_status_evidence(document)
                except ProjectMemoryError as exc:
                    findings.append(_pmh_item("PMH-006", StatusState.BLOCKED, str(exc)))
                    continue
                evidence_values = list(evidence.values)
                if reference.artifact_type == "Review":
                    evidence_values.extend(_review_result_values(document))
                normalized = {
                    _normalize_artifact_state(value, reference.artifact_type)
                    for value in evidence_values
                }
                normalized.discard(None)
                if len(normalized) > 1:
                    findings.append(
                        _pmh_item(
                            "PMH-006",
                            StatusState.WARNING,
                            f"{reference.identifier} has conflicting explicit lifecycle evidence.",
                        )
                    )
                elif not normalized:
                    continue
                elif claimed not in normalized:
                    findings.append(
                        _pmh_item(
                            "PMH-006",
                            StatusState.WARNING,
                            f"{reference.identifier} is claimed as {claimed}; authoritative "
                            f"evidence is {next(iter(normalized))}.",
                        )
                    )
    if findings:
        return findings
    state = StatusState.OK if checked else StatusState.NOT_APPLICABLE
    message = (
        f"Validated {checked} explicit lifecycle claim(s)."
        if checked
        else "No supported explicit lifecycle claim was present."
    )
    return [_pmh_item("PMH-006", state, message)]


def _pmh_stale_handoff_gates(root: Path, documents: dict[str, DocumentFact]) -> list[StatusItem]:
    document = documents.get("AI_HANDOFF.md")
    content = _single_section_content(document, "Immediate Next Step") if document else None
    if not content:
        return [
            _pmh_item(
                "PMH-007",
                StatusState.NOT_APPLICABLE,
                "No eligible Immediate Next Step was available.",
            )
        ]
    findings: list[StatusItem] = []
    checked = 0
    for unit in claim_units(content):
        references = parse_references(unit)
        if not references:
            continue
        phrase = next(
            (
                value
                for value in (
                    "pending review",
                    "awaiting review",
                    "ready to commit",
                    "commit pending",
                    "implementation ready",
                )
                if contains_exact_phrase(unit, value)
            ),
            None,
        )
        if phrase is None:
            continue
        checked += 1
        stale = False
        if phrase in {"pending review", "awaiting review"}:
            try:
                review_refs = [ref for ref in references if ref.artifact_type == "Review"]
                for reference in references:
                    if reference.artifact_type != "Review":
                        review_refs.extend(_linked_review_references(root, reference))
                stale = any(_review_records_pass(root, ref) for ref in review_refs)
            except ProjectMemoryError as exc:
                findings.append(_pmh_item("PMH-007", StatusState.BLOCKED, str(exc)))
                continue
        elif phrase in {"ready to commit", "commit pending"}:
            stale = any(_commit_exists(root, value) is True for value in parse_commit_hashes(unit))
        else:
            try:
                stale = any(
                    _artifact_has_state(
                        root, ref, {"implemented", "implementation reviewed", "closed"}
                    )
                    for ref in references
                )
            except ProjectMemoryError as exc:
                findings.append(_pmh_item("PMH-007", StatusState.BLOCKED, str(exc)))
                continue
        if stale:
            findings.append(
                _pmh_item(
                    "PMH-007",
                    StatusState.WARNING,
                    f"The `{phrase}` gate for {references[0].identifier} has positive "
                    "completion evidence.",
                )
            )
    if findings:
        return findings
    state = StatusState.OK if checked else StatusState.NOT_APPLICABLE
    message = (
        f"Validated {checked} recognized handoff gate(s) as legitimately pending."
        if checked
        else "No recognized handoff gate claim was present."
    )
    return [_pmh_item("PMH-007", state, message)]


def _pmh_release_lifecycle(root: Path, documents: dict[str, DocumentFact]) -> list[StatusItem]:
    state_text = _section_from_documents(documents, "PROJECT_STATE.md", "Planned Release")
    handoff_text = _section_from_documents(documents, "AI_HANDOFF.md", "Current Repository State")
    state_claims = _release_claims(state_text or "")
    handoff_claims = _release_claims(handoff_text or "")
    shared = set(state_claims) & set(handoff_claims)
    if not shared:
        return [
            _pmh_item(
                "PMH-008",
                StatusState.NOT_APPLICABLE,
                "No shared explicit release identifier was present in both active sections.",
            )
        ]
    findings: list[StatusItem] = []
    checked = 0
    for version in sorted(shared):
        checked += 1
        checklist = root / f"docs/release/checklist-{version}.md"
        if not checklist.is_file():
            findings.append(
                _pmh_item(
                    "PMH-008", StatusState.MISSING, f"Missing docs/release/checklist-{version}.md."
                )
            )
            continue
        try:
            evidence = explicit_status_evidence(
                load_document(root, checklist.relative_to(root).as_posix())
            )
        except ProjectMemoryError as exc:
            findings.append(_pmh_item("PMH-008", StatusState.BLOCKED, str(exc)))
            continue
        values = [value for value in evidence.values if value in RELEASE_LABELS]
        if len(values) != 1:
            findings.append(
                _pmh_item(
                    "PMH-008",
                    StatusState.BLOCKED,
                    f"Release checklist {version} lacks one unambiguous lifecycle status.",
                )
            )
            continue
        expected = values[0]
        observed = state_claims[version] | handoff_claims[version]
        if observed != {expected}:
            findings.append(
                _pmh_item(
                    "PMH-008",
                    StatusState.WARNING,
                    f"Release {version} active labels {sorted(observed)} disagree with "
                    f"checklist status {expected}.",
                )
            )
    if findings:
        return findings
    return [
        _pmh_item(
            "PMH-008", StatusState.OK, f"Validated {checked} active release lifecycle label set(s)."
        )
    ]


def _pmh_current_adr_authority(root: Path, documents: dict[str, DocumentFact]) -> list[StatusItem]:
    content = _section_from_documents(documents, "PROJECT_BRAIN.md", "Current Decisions")
    if not content:
        return [
            _pmh_item(
                "PMH-009",
                StatusState.NOT_APPLICABLE,
                "No eligible Current Decisions section was available.",
            )
        ]
    findings: list[StatusItem] = []
    checked = 0
    for unit in claim_units(content):
        references = [ref for ref in parse_references(unit) if ref.artifact_type == "ADR"]
        for reference in references:
            checked += 1
            try:
                resolution = resolve_reference(root, reference)
            except ProjectMemoryError as exc:
                findings.append(_pmh_item("PMH-009", StatusState.BLOCKED, str(exc)))
                continue
            if not resolution.matches:
                findings.append(
                    _pmh_item(
                        "PMH-009",
                        StatusState.MISSING,
                        f"Current decision {reference.identifier} is missing.",
                    )
                )
                continue
            if len(resolution.matches) > 1:
                findings.append(
                    _pmh_item(
                        "PMH-009",
                        StatusState.WARNING,
                        f"Current decision {reference.identifier} is ambiguous.",
                    )
                )
                continue
            try:
                evidence = explicit_status_evidence(
                    load_document(root, resolution.matches[0].relative_to(root).as_posix())
                )
            except ProjectMemoryError as exc:
                findings.append(_pmh_item("PMH-009", StatusState.BLOCKED, str(exc)))
                continue
            states = {_normalize_artifact_state(value, "ADR") for value in evidence.values}
            states.discard(None)
            noncurrent = states & {"rejected", "superseded", "deprecated"}
            try:
                historical = _historical_adr_qualifier_valid(root, unit)
            except ProjectMemoryError as exc:
                findings.append(_pmh_item("PMH-009", StatusState.BLOCKED, str(exc)))
                continue
            if noncurrent and not historical:
                findings.append(
                    _pmh_item(
                        "PMH-009",
                        StatusState.WARNING,
                        f"{reference.identifier} is listed as current but is explicitly "
                        f"{next(iter(noncurrent))}.",
                    )
                )
    if findings:
        return findings
    state = StatusState.OK if checked else StatusState.NOT_APPLICABLE
    message = (
        f"Validated {checked} current ADR reference(s)."
        if checked
        else "No ADR is explicitly listed as current authority."
    )
    return [_pmh_item("PMH-009", state, message)]


def _pmh_item(rule: str, state: StatusState, message: str) -> StatusItem:
    return StatusItem(label=rule, state=state, message=message)


def _single_section_content(document: DocumentFact | None, heading: str) -> str | None:
    if document is None:
        return None
    sections = document.sections.get(heading, ())
    return sections[0].content if len(sections) == 1 else None


def _section_from_documents(
    documents: dict[str, DocumentFact], path: str, heading: str
) -> str | None:
    return _single_section_content(documents.get(path), heading)


def _active_references(documents: dict[str, DocumentFact]) -> tuple[ReferenceFact, ...]:
    references: dict[tuple[str, str], ReferenceFact] = {}
    for path, headings in REFERENCE_SECTIONS.items():
        document = documents.get(path)
        if document is None:
            continue
        for heading in headings:
            content = _single_section_content(document, heading)
            for reference in parse_references(content or ""):
                references.setdefault((reference.identifier, reference.directory), reference)
    return tuple(references.values())


def _active_commit_hashes(documents: dict[str, DocumentFact]) -> tuple[str, ...]:
    values: dict[str, None] = {}
    for path, headings in REFERENCE_SECTIONS.items():
        document = documents.get(path)
        if document is None:
            continue
        for heading in headings:
            for value in parse_commit_hashes(_single_section_content(document, heading) or ""):
                values.setdefault(value, None)
    return tuple(values)


def _active_claim_units(documents: dict[str, DocumentFact]) -> tuple[str, ...]:
    values: list[str] = []
    for path, headings in REFERENCE_SECTIONS.items():
        document = documents.get(path)
        if document is None:
            continue
        for heading in headings:
            values.extend(claim_units(_single_section_content(document, heading) or ""))
    return tuple(values)


def _lifecycle_claim(unit: str, reference: ReferenceFact) -> str | None:
    labels = LIFECYCLE_LABELS.get(reference.artifact_type, {})
    identifier = re.escape(reference.identifier)
    matches = []
    for source, normalized in labels.items():
        label = re.escape(source)
        pattern = (
            rf"{identifier}[^.!?]{{0,80}}\b"
            rf"(?:is|remains|returned|records?|recorded|"
            rf"status(?:\s+is|:)?|result(?:\s+is|:)?)\s+`?{label}`?\b"
        )
        if re.search(pattern, unit, re.IGNORECASE):
            matches.append(normalized)
    if not matches:
        return None
    return sorted(matches, key=len, reverse=True)[0]


def _normalize_artifact_state(value: str, artifact_type: str) -> str | None:
    labels = LIFECYCLE_LABELS.get(artifact_type, {})
    return labels.get(normalize_label(value))


def _commit_exists(root: Path, commit_hash: str) -> bool | None:
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", f"{commit_hash}^{{commit}}"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.returncode == 0


def _review_records_pass(root: Path, reference: ReferenceFact) -> bool:
    resolution = resolve_reference(root, reference)
    if len(resolution.matches) != 1:
        return False
    document = load_document(root, resolution.matches[0].relative_to(root).as_posix())
    return "pass" in _review_result_values(document)


def _review_result_values(document: DocumentFact) -> tuple[str, ...]:
    values: list[str] = []
    for heading in ("Review Status", "Decision", "Review Result"):
        content = _single_section_content(document, heading)
        if content:
            values.extend(normalize_label(line) for line in content.splitlines() if line.strip())
    for line in document.content.splitlines():
        match = re.match(
            r"^(?:Final review status|Review result):\s*`?([^`]+?)`?\s*$",
            line,
            re.IGNORECASE,
        )
        if match:
            values.append(normalize_label(match.group(1)))
    return tuple(dict.fromkeys(values))


def _linked_review_references(root: Path, reference: ReferenceFact) -> list[ReferenceFact]:
    resolution = resolve_reference(root, reference)
    if len(resolution.matches) != 1:
        return []
    document = load_document(root, resolution.matches[0].relative_to(root).as_posix())
    return [ref for ref in parse_references(document.content) if ref.artifact_type == "Review"]


def _artifact_has_state(root: Path, reference: ReferenceFact, states: set[str]) -> bool:
    resolution = resolve_reference(root, reference)
    if len(resolution.matches) != 1:
        return False
    document = load_document(root, resolution.matches[0].relative_to(root).as_posix())
    return bool(
        {
            _normalize_artifact_state(value, reference.artifact_type)
            for value in explicit_status_evidence(document).values
        }
        & states
    )


def _release_claims(content: str) -> dict[str, set[str]]:
    claims: dict[str, set[str]] = {}
    for unit in claim_units(content):
        versions = re.findall(r"(?<![\d.])v?(\d+\.\d+\.\d+)(?![\d.])", unit)
        labels = {label for label in RELEASE_LABELS if _explicit_release_label(unit, label)}
        for version in versions:
            if labels:
                claims.setdefault(version, set()).update(labels)
    return claims


def _explicit_release_label(unit: str, label: str) -> bool:
    escaped = re.escape(label)
    backticked = re.search(rf"`{escaped}`", unit, re.IGNORECASE)
    attributed = re.search(
        rf"\b(?:is|remains|status(?:\s+is|:)?|state(?:\s+is|:)?)\s+`?{escaped}`?\b",
        unit,
        re.IGNORECASE,
    )
    return backticked is not None or attributed is not None


def _historical_adr_qualifier_valid(root: Path, unit: str) -> bool:
    lowered = unit.casefold()
    if any(
        contains_exact_phrase(lowered, value) for value in ("historical", "rejected", "deprecated")
    ):
        return True
    match = re.search(r"superseded by (ADR(?: |-)\d{4})", unit, re.IGNORECASE)
    if match is None:
        return False
    references = [
        ref for ref in parse_references(match.group(1).upper()) if ref.artifact_type == "ADR"
    ]
    return bool(references and len(resolve_reference(root, references[0]).matches) == 1)


def _repository_status(root: Path) -> StatusCategory:
    workflow_item = _directory_item(
        root,
        ".github/workflows",
        DIRECTORY_ARTIFACTS[".github/workflows"],
    )
    git_item = _git_status_item(root)
    return _category_from_items("Repository Status", (workflow_item, git_item))


def _version_consistency_status(root: Path) -> StatusCategory:
    target = _latest_release_tag_version(root)
    items = [
        _latest_release_tag_item(root, target),
        _readme_version_item(root, target),
        _changelog_version_item(root, target),
        _project_state_version_item(root, target),
        _ai_handoff_version_item(root, target),
        _pyproject_version_item(root, target),
        _version_working_tree_item(root),
    ]
    return _category_from_items("Version Consistency Status", tuple(items))


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


def _latest_release_tag_item(root: Path, target: str | None) -> StatusItem:
    if not (root / ".git").exists():
        return StatusItem(
            label="Latest release tag",
            state=StatusState.NOT_APPLICABLE,
            message="No .git metadata found; tag consistency was not evaluated.",
        )
    if target is None:
        return StatusItem(
            label="Latest release tag",
            state=StatusState.MISSING,
            message="No local release tag matching vMAJOR.MINOR.PATCH was found.",
        )
    return StatusItem(
        label="Latest release tag",
        state=StatusState.OK,
        message=f"Latest local release tag is v{target}.",
    )


def _latest_release_tag_version(root: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "tag", "--list", "v*"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None

    versions = []
    for line in result.stdout.splitlines():
        match = VERSION_TAG_PATTERN.match(line.strip())
        if match:
            versions.append(match.group(1))
    if not versions:
        return None
    return sorted(versions, key=_version_key)[-1]


def _version_key(version: str) -> tuple[int, int, int]:
    major, minor, patch = version.split(".")
    return (int(major), int(minor), int(patch))


def _readme_version_item(root: Path, target: str | None) -> StatusItem:
    return _document_version_item(
        root=root,
        relative_path="README.md",
        label="README current state",
        target=target,
        section_heading="## Current State",
    )


def _project_state_version_item(root: Path, target: str | None) -> StatusItem:
    return _document_version_item(
        root=root,
        relative_path="PROJECT_STATE.md",
        label="Project State current version",
        target=target,
        section_heading="## Current Version",
    )


def _ai_handoff_version_item(root: Path, target: str | None) -> StatusItem:
    return _document_version_item(
        root=root,
        relative_path="AI_HANDOFF.md",
        label="AI Handoff current state",
        target=target,
        section_heading="## Current Repository State",
    )


def _document_version_item(
    root: Path,
    relative_path: str,
    label: str,
    target: str | None,
    section_heading: str,
) -> StatusItem:
    path = root / relative_path
    if not path.is_file():
        return StatusItem(
            label=label,
            state=StatusState.MISSING,
            message=f"Missing {relative_path}.",
        )
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return StatusItem(
            label=label,
            state=StatusState.WARNING,
            message=f"Could not read {relative_path}.",
        )

    # Keep this intentionally narrow: only inspect the active section that describes
    # current repository state, avoiding historical version references elsewhere.
    section = _markdown_section(content, section_heading)
    if section is None:
        return StatusItem(
            label=label,
            state=StatusState.MISSING,
            message=f"No {section_heading} section found in {relative_path}.",
        )
    version = _first_version(section)
    if version is None:
        return StatusItem(
            label=label,
            state=StatusState.MISSING,
            message=f"No active version reference found in {relative_path}.",
        )
    if target is None:
        return StatusItem(
            label=label,
            state=StatusState.NOT_APPLICABLE,
            message=f"Found {version}, but no release tag is available for comparison.",
        )
    if version == target:
        return StatusItem(label=label, state=StatusState.OK, message=f"Matches v{target}.")
    return StatusItem(
        label=label,
        state=StatusState.WARNING,
        message=f"Found {version}; expected v{target}.",
    )


def _changelog_version_item(root: Path, target: str | None) -> StatusItem:
    path = root / "CHANGELOG.md"
    if not path.is_file():
        return StatusItem(
            label="Changelog latest release",
            state=StatusState.MISSING,
            message="Missing CHANGELOG.md.",
        )
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return StatusItem(
            label="Changelog latest release",
            state=StatusState.WARNING,
            message="Could not read CHANGELOG.md.",
        )

    headings = [
        match.group(1).removeprefix("v") for match in CHANGELOG_HEADING_PATTERN.finditer(content)
    ]
    if not headings:
        return StatusItem(
            label="Changelog latest release",
            state=StatusState.MISSING,
            message="No changelog release heading was found.",
        )
    latest_heading = headings[0]
    if target is None:
        return StatusItem(
            label="Changelog latest release",
            state=StatusState.NOT_APPLICABLE,
            message=(
                f"Latest changelog heading is {latest_heading}, but no release tag is available."
            ),
        )
    if latest_heading == target:
        return StatusItem(
            label="Changelog latest release",
            state=StatusState.OK,
            message=f"Latest changelog heading matches v{target}.",
        )
    return StatusItem(
        label="Changelog latest release",
        state=StatusState.WARNING,
        message=f"Latest changelog heading is {latest_heading}; expected v{target}.",
    )


def _pyproject_version_item(root: Path, target: str | None) -> StatusItem:
    path = root / "pyproject.toml"
    if not path.is_file():
        return StatusItem(
            label="pyproject project version",
            state=StatusState.NOT_APPLICABLE,
            message="pyproject.toml is not present.",
        )
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return StatusItem(
            label="pyproject project version",
            state=StatusState.WARNING,
            message="Could not read pyproject.toml project version.",
        )
    version = data.get("project", {}).get("version")
    if not isinstance(version, str):
        return StatusItem(
            label="pyproject project version",
            state=StatusState.MISSING,
            message="No [project].version value was found.",
        )
    normalized = version.removeprefix("v")
    if target is None:
        return StatusItem(
            label="pyproject project version",
            state=StatusState.NOT_APPLICABLE,
            message=f"Found {version}, but no release tag is available for comparison.",
        )
    if normalized == target:
        return StatusItem(
            label="pyproject project version",
            state=StatusState.OK,
            message=f"Matches v{target}.",
        )
    return StatusItem(
        label="pyproject project version",
        state=StatusState.WARNING,
        message=f"Found {version}; expected v{target}.",
    )


def _version_working_tree_item(root: Path) -> StatusItem:
    git_item = _git_status_item(root)
    if git_item.label == "Git repository":
        return StatusItem(
            label="Version check working tree context",
            state=StatusState.NOT_APPLICABLE,
            message="No Git working tree context is available.",
        )
    return StatusItem(
        label="Version check working tree context",
        state=git_item.state,
        message=git_item.message,
    )


def _markdown_section(content: str, heading: str) -> str | None:
    start = content.find(heading)
    if start == -1:
        return None
    rest = content[start + len(heading) :]
    next_heading = re.search(r"\n## ", rest)
    if next_heading:
        return rest[: next_heading.start()]
    return rest


def _first_version(content: str) -> str | None:
    match = VERSION_PATTERN.search(content)
    if match:
        return match.group(1)
    return None


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
