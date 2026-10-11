"""Run one real isolated Codex roundtrip. No retries, original-project edits or releases."""

from __future__ import annotations

import json
import subprocess
import uuid
from pathlib import Path

from forge.evidence import canonical, load_events
from forge.workflow import apply, create, run


def main():
    root = Path("build").resolve() / ("runtime-qualification-" + uuid.uuid4().hex)
    root.mkdir(parents=True)
    for args in (
        ["init"],
        ["config", "user.email", "fixture@example.invalid"],
        ["config", "user.name", "Forge qualification"],
    ):
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)
    (root / "greeting.py").write_text('def greeting():\n    return "hello"\n', encoding="utf-8")
    (root / "forge.toml").write_text(
        'schema_version=1\n[[checks]]\nid="behavior"\n'
        'argv=["python","-c","from greeting import greeting; assert greeting() == \'hej\'"]\n',
        encoding="utf-8",
    )
    for args in (["add", "."], ["commit", "-qm", "isolated runtime qualification fixture"]):
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)
    spec = {
        "schema_version": 1,
        "objective": "Change greeting() to return exactly hej. Preserve the function API.",
        "scope": ["greeting.py"],
        "criteria": [{"id": "greeting", "text": "Calling greeting() returns exactly hej."}],
        "allow_dirty": False,
        "authorization": {"execute": True, "review": True, "tool_network": False},
    }
    create(root, "roundtrip", spec)
    result = run(root, "roundtrip")
    assert (root / "greeting.py").read_text(encoding="utf-8") == (
        'def greeting():\n    return "hello"\n'
    )
    if result["state"] == "READY_FOR_APPLY":
        result = apply(root, "roundtrip")
        subprocess.run(
            ["python", "-c", "from greeting import greeting; assert greeting()=='hej'"],
            cwd=root,
            check=True,
        )
    events = load_events(root / ".forge/tasks/roundtrip")
    sessions = [
        event["payload"]["runtime"]["session_id"]
        for event in events
        if "runtime" in event["payload"]
    ]
    report = {
        "status": "PASS" if result["state"] == "APPLIED" else "BLOCKED",
        "fixture": str(root),
        "result": result,
        "observed_sessions": sessions,
        "release_acceptance": False,
        "note": "Roundtrip evidence only; permission/network conformance is a separate gate.",
    }
    (root / "qualification.json").write_bytes(canonical(report))
    print(json.dumps(report, ensure_ascii=True))
    raise SystemExit(0 if report["status"] == "PASS" else 2)


if __name__ == "__main__":
    main()
