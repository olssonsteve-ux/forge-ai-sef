# ruff: noqa: E501
"""Deterministic FAL-002 production inventory and hard-limit accounting."""
# fmt: off

from __future__ import annotations

import ast
import io
import tokenize
from pathlib import Path
from typing import Any

from forge.fal002_model import HB, FAL002Error

AUTHORIZED_MODULES = tuple("forge/fal002.py forge/fal002_model.py forge/fal002_inventory.py forge/fal002_io.py".split())
AUTHORIZED_SURFACES = tuple("fal002.gate-record.v1 fal002.executor-exchange.v1 fal002.run-record.v1 fal002.reviewer-exchange.v1 fal002.human-decision.v1".split())
CORRECTION_BASELINE = "23b398eeac46ad19226c4f0fae42713887a39a29"
STDLIB = set("__future__ argparse ast collections copy dataclasses datetime hashlib io json os pathlib re shutil subprocess sys tokenize typing uuid".split())


def counted_loc(path: Path) -> int:
    """Count physical code lines, excluding blanks, comments, and standalone docstrings."""
    text = path.read_text(encoding="utf-8")
    ignored: set[int] = set()
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise FAL002Error("AWAITING_HUMAN", f"invalid Python at {path}") from exc
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            ignored.update(range(body[0].lineno, (body[0].end_lineno or body[0].lineno) + 1))
    comment_only: set[int] = set()
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type == tokenize.COMMENT and not text.splitlines()[token.start[0] - 1][: token.start[1]].strip():
            comment_only.add(token.start[0])
    return sum(1 for number, line in enumerate(text.splitlines(), 1) if line.strip() and number not in ignored and number not in comment_only)


def _module_path(name: str) -> str:
    return name.replace(".", "/") + ".py"


def _imports(path: Path, relative: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
    edges: list[dict[str, str]] = []
    unresolved: list[dict[str, str]] = []
    package = relative.removesuffix(".py").split("/")[:-1]
    for node in ast.walk(tree):
        targets: list[tuple[str, str]] = []
        if isinstance(node, ast.Import):
            targets = [(alias.name, "IMPORT") for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            prefix = package[: max(0, len(package) - node.level + 1)] if node.level else []
            base = ".".join(prefix + ([node.module] if node.module else []))
            targets = [(base, "IMPORT")]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"import_module", "run_module"}:
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                targets = [(node.args[0].value, "DYNAMIC")]
            else:
                unresolved.append(
                    {
                        "source": relative,
                        "locator": f"line:{node.lineno}",
                        "expression": ast.unparse(node),
                        "kind": "DYNAMIC",
                        "reason": "computed target",
                    }
                )
        for name, kind in targets:
            root = name.split(".")[0]
            if root == "forge":
                target = _module_path(name)
                edges.append(
                    {
                        "source": relative,
                        "target": target,
                        "kind": kind,
                        "locator": f"line:{node.lineno}",
                    }
                )
            elif root not in STDLIB:
                unresolved.append(
                    {
                        "source": relative,
                        "locator": f"line:{node.lineno}",
                        "expression": name,
                        "kind": kind,
                        "reason": "non-stdlib import",
                    }
                )
    return edges, unresolved


def inventory(root: Path) -> dict[str, Any]:
    root = root.resolve(strict=True)
    files: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    unresolved: list[dict[str, str]] = []
    for relative in AUTHORIZED_MODULES:
        path = root / relative
        if not path.is_file():
            unresolved.append(
                {
                    "source": relative,
                    "locator": "file",
                    "expression": relative,
                    "kind": "IMPORT",
                    "reason": "authorized module missing",
                }
            )
            continue
        module_edges, module_unresolved = _imports(path, relative)
        edges.extend(module_edges)
        unresolved.extend(module_unresolved)
        roles = []
        classes = {node.name for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))) if isinstance(node, ast.ClassDef)}
        if "FAL002ExecutorAdapter" in classes:
            roles.append("EXECUTOR_ADAPTER")
        if "FAL002ReviewerAdapter" in classes:
            roles.append("REVIEWER_ADAPTER")
        inbound = [f"{edge['source']}:{edge['locator']}" for edge in edges if edge["target"] == relative]
        files.append(
            {
                "path": relative,
                "content_hash": HB(path.read_bytes()),
                "inbound_edges": sorted(inbound),
                "reason": "ENTRYPOINT" if relative == "forge/fal002.py" else "STATIC_IMPORT",
                "counted_loc": counted_loc(path),
                "roles": roles,
                "classification": "COUNT",
            }
        )
    unauthorized = [edge for edge in edges if edge["target"].startswith("forge/fal002") and edge["target"] not in AUTHORIZED_MODULES]
    unresolved.extend({**edge, "expression": edge["target"], "reason": "unauthorized FAL-002 module"} for edge in unauthorized)
    counts = {
        "modules": len(files),
        "new_production_loc": sum(item["counted_loc"] for item in files),
        "executor_adapters": sum("EXECUTOR_ADAPTER" in item["roles"] for item in files),
        "reviewer_adapters": sum("REVIEWER_ADAPTER" in item["roles"] for item in files),
        "schema_surfaces": len(AUTHORIZED_SURFACES),
    }
    if counts["modules"] > 4 or counts["new_production_loc"] > 3000 or counts["executor_adapters"] != 1 or counts["reviewer_adapters"] != 1 or counts["schema_surfaces"] != 5:
        disposition = "AWAITING_HUMAN"
    else:
        disposition = "PASS" if not unresolved else "AWAITING_HUMAN"
    exact_edges = [
        {
            **edge,
            "edge_id": HB(f"{edge['source']}|{edge['target']}|{edge['kind']}|{edge['locator']}".encode())[:24],
        }
        for edge in edges
    ]
    return {
        "entrypoint": "forge/fal002.py",
        "baseline_commit": CORRECTION_BASELINE,
        "python_version": "3.14",
        "files": sorted(files, key=lambda item: item["path"]),
        "edges": sorted(exact_edges, key=lambda item: (item["source"], item["target"], item["locator"])),
        "exemptions": [],
        "counts": counts,
        "dependencies": {
            "stdlib": sorted(STDLIB),
            "existing_third_party": [],
            "new_direct": [],
            "new_transitive": [],
            "manifest_hash": HB((root / "pyproject.toml").read_bytes()),
        },
        "unresolved_targets": sorted(unresolved, key=lambda item: (item["source"], item["locator"])),
        "disposition": disposition,
    }


def enforce_limits(result: dict[str, Any]) -> None:
    if result["disposition"] != "PASS":
        raise FAL002Error("BUDGET_AUTHORITY_REQUIRED", "inventory is outside authorized limits")
# fmt: on
