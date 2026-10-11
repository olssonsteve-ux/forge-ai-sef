"""Inspect distribution contents and smoke every installed CLI command without model calls."""

from __future__ import annotations

import argparse
import json
import subprocess
import tarfile
import uuid
import zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--wheel", required=True)
    parser.add_argument("--sdist", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()
    python = str(Path(args.python).resolve())
    wheel, sdist = Path(args.wheel).resolve(), Path(args.sdist).resolve()
    forbidden = {
        "adaptive_loop.py",
        "fal002.py",
        "fal002_model.py",
        "fal002_io.py",
        "fal002_inventory.py",
    }
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert not any(Path(name).name in forbidden for name in names)
        assert len([name for name in names if name.startswith("forge/data/bootstrap/")]) == 8
        assert "forge/data/Forge-1.0-guide.md" in names
        assert "forge/data/INTENT.md" in names
        assert "forge/data/Forge-Concept-v1.0.md" in names
        assert any(name.endswith("/LICENSE") and ".dist-info/" in name for name in names)
        for name in names:
            if name.startswith("forge/") and name.endswith(".py"):
                assert archive.read(name) == Path(name).read_bytes(), name
    with tarfile.open(sdist) as archive:
        names = archive.getnames()
        assert not any(Path(name).name in forbidden for name in names)
        assert len([name for name in names if "/templates/bootstrap/" in name]) == 8
        assert any(name.endswith("/LICENSE") for name in names)
    root = Path(args.output_root).resolve() / ("package-smoke-" + uuid.uuid4().hex)
    root.mkdir(parents=True)
    results = []

    def command(argv, cwd=root, expected=0):
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=60)
        assert result.returncode == expected, (argv, result.stdout, result.stderr)
        results.append({"argv": argv, "exit_code": result.returncode})
        return result.stdout

    command(
        [
            python,
            "-I",
            "-c",
            "import forge,forge.cli,importlib.util,sys;"
            "assert 'site-packages' in forge.__file__;"
            "assert not any('fal002' in n or 'adaptive_loop' in n for n in sys.modules);"
            "assert importlib.util.find_spec('forge.fal002') is None",
        ]
    )
    command([python, "-I", "-m", "forge", "--help"])
    command([python, "-I", "-m", "forge", "init", "demo", "--dry-run"])
    assert not (root / "demo").exists()
    command([python, "-I", "-m", "forge", "init", "demo"])
    project = root / "demo"
    assert len([path for path in project.iterdir() if path.is_file()]) == 8
    command([python, "-I", "-m", "forge", "status"], cwd=project)
    (project / "forge.toml").write_text(
        'schema_version=1\n[[checks]]\nid="smoke"\nargv=["python","-c","print(123)"]\n',
        encoding="utf-8",
    )
    assert (
        json.loads(command([python, "-I", "-m", "forge", "verify"], cwd=project))["status"]
        == "PASS"
    )
    for argv in (
        ["init"],
        ["config", "user.email", "fixture@example.invalid"],
        ["config", "user.name", "Package fixture"],
        ["add", "."],
        ["commit", "-qm", "isolated package fixture"],
    ):
        command(["git", *argv], cwd=project)
    spec = {
        "schema_version": 1,
        "objective": "Bounded package smoke",
        "scope": ["README.md"],
        "criteria": [{"id": "smoke", "text": "Readme remains useful"}],
        "allow_dirty": False,
        "authorization": {"execute": True, "review": True, "tool_network": False},
    }
    spec_path = root / "task.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    base = [python, "-I", "-m", "forge", "task"]
    assert (
        json.loads(command([*base, "create", "smoke", "--spec", str(spec_path)], cwd=project))[
            "state"
        ]
        == "READY"
    )
    assert json.loads(command([*base, "show", "smoke"], cwd=project))["state"] == "READY"
    # Negative run/apply/resume paths must fail closed without invoking a model.
    for argv in (
        ["run", "missing"],
        ["apply", "smoke"],
        ["resume", "smoke", "--reason", "Already ready"],
    ):
        assert json.loads(command([*base, *argv], cwd=project, expected=2))["status"] == "BLOCKED"
    report = {
        "status": "PASS",
        "wheel": str(wheel),
        "sdist": str(sdist),
        "fixture": str(root),
        "checks": results,
        "limitation": "No live model call. Actual runtime qualification is separate.",
    }
    (root / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        json.dumps({"status": "PASS", "checks": len(results), "report": str(root / "report.json")})
    )


if __name__ == "__main__":
    main()
