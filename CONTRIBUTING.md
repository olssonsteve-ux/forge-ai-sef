# Contributing to Forge

Forge is open for testing, bug reports and contributions under the [MIT License](LICENSE).
Read the [statement of intent](INTENT.md) and [v1 concept baseline](docs/Forge-Concept-v1.0.md).

## Try it and report what happened

Follow the [user guide](docs/Forge-1.0-guide.md). Use a disposable project or a backup for the
candidate. Report issues at https://github.com/olssonsteve-ux/forge-ai-sef/issues with:

- Forge version, operating system, Python version and Codex CLI version if used.
- The smallest reproducible example and the exact command.
- Expected and actual behavior, including the exit status.
- Relevant sanitized output and whether the issue reproduces in a clean project.

Do not upload credentials, private source code, audio recordings, task workspaces or raw session
logs. Use synthetic examples. Runtime qualification V1-Q-01 is a known blocker; reports from
other environments are welcome, but do not bypass sandbox or approval policies.

## Propose a change

Open an issue for a substantial scope or contract change before implementing it. Small fixes can
arrive as a pull request with the problem, intended behavior and verification. Keep changes focused.
One concise record is enough unless the governing contract requires more.

Run:

```text
python -m pip install -e ".[dev]"
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
git diff --check
```

CI targets Windows and Python 3.14. Checks do not prove real agent permissions or end-to-end runtime
qualification. Separate evidence is required for those claims. Never close historical findings
solely because tests are green.

Contributions are reviewed against the Constitution and accepted scope. By submitting a contribution,
you agree that it may be distributed under this project's MIT License and confirm that you have
the right to contribute it. Third-party dependencies retain their own licenses.
