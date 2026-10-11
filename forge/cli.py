from pathlib import Path
from typing import Annotated

import typer

from .bootstrap import ForgeInitError, init_project
from .status import StatusServiceError, evaluate_status, render_status_report

app = typer.Typer(
    name="forge",
    help="Forge AI Software Engineering Framework.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Forge AI Software Engineering Framework."""


@app.command("init")
def init(
    project_name: Annotated[str, typer.Argument(help="Project directory name to create.")],
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Show planned initialization without writing files."),
    ] = False,
) -> None:
    """Create a new Forge-governed project from bootstrap templates."""
    try:
        result = init_project(project_name=project_name, base_dir=Path.cwd(), dry_run=dry_run)
    except ForgeInitError as error:
        typer.secho(f"Error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from error

    if dry_run:
        typer.echo(f"Forge init dry run: {result.target}")
        typer.echo("Validation: OK")
        typer.echo(f"Folders to create: {len(result.folders)}")
        for folder in result.folders:
            typer.echo(f"  {folder}")
        typer.echo(f"Files to create: {len(result.files)}")
        for file_path in result.files:
            typer.echo(f"  {file_path}")
        typer.echo(f"Bootstrap output contract: {result.output_contract}")
        typer.echo("Source layout: not selected")
        return

    typer.echo(f"Forge project initialized: {project_name}")
    typer.echo(f"Created folders: {len(result.folders)}")
    typer.echo(f"Created files: {len(result.files)}")
    typer.echo(f"Bootstrap output contract: {result.output_contract}")
    typer.echo("Source layout: not selected")
    typer.echo(
        "Next step: review PROJECT_STATE.md and select source layout through "
        "architecture discovery."
    )


@app.command("status")
def status() -> None:
    """Report read-only Forge governance status for the current repository."""
    try:
        report = evaluate_status(Path.cwd())
    except StatusServiceError as error:
        typer.secho(f"Error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from error

    typer.echo(render_status_report(report))


# Stable commands deliberately import no experimental FAL modules.
task_app = typer.Typer(help="Isolated tasks with explicit verification, review and apply.")
app.add_typer(task_app, name="task")


def _report_action(action) -> None:
    import json

    from forge.evidence import WorkflowError
    from forge.verification import redacted

    try:
        result = action()
    except (WorkflowError, OSError, ValueError, KeyError, TypeError) as error:
        typer.echo(json.dumps({"status": "BLOCKED", "error": redacted(str(error))[:4000]}))
        raise typer.Exit(2) from error
    typer.echo(json.dumps(result, ensure_ascii=False, sort_keys=True))
    state = result.get("status", result.get("state"))
    if state in {"FAIL", "NEEDS_CHANGES"}:
        raise typer.Exit(1)
    if state == "BLOCKED":
        raise typer.Exit(2)


@app.command("verify")
def verify_command(
    config: Annotated[
        str, typer.Option("--config", help="Trusted relative TOML policy.")
    ] = "forge.toml",
) -> None:
    """Run explicitly configured checks; commands are trusted operator code."""
    from forge.verification import load_config, verify

    _report_action(lambda: verify(Path.cwd(), load_config(Path.cwd(), config)))


@task_app.command("create")
def task_create(
    identifier: str,
    spec: Annotated[Path, typer.Option("--spec", help="Explicit task JSON specification.")],
) -> None:
    """Capture repository authority and create an isolated workspace."""
    from forge.evidence import MAX_RECORD, WorkflowError, parse_json
    from forge.workflow import create

    def action():
        if spec.stat().st_size > MAX_RECORD:
            raise WorkflowError("Task specification exceeds size limit.")
        return create(Path.cwd(), identifier, parse_json(spec.read_bytes()))

    _report_action(action)


@task_app.command("show")
def task_show(identifier: str) -> None:
    """Read validated evidence without executing anything."""
    from forge.workflow import show

    _report_action(lambda: show(Path.cwd(), identifier))


@task_app.command("run")
def task_run(identifier: str) -> None:
    """Execute, verify and review a READY task once."""
    from forge.workflow import run

    _report_action(lambda: run(Path.cwd(), identifier))


@task_app.command("resume")
def task_resume(
    identifier: str,
    reason: Annotated[
        str, typer.Option("--reason", help="Why another full attempt is authorized.")
    ],
) -> None:
    """Invalidate prior readiness and explicitly authorize a new attempt."""
    from forge.workflow import resume

    _report_action(lambda: resume(Path.cwd(), identifier, reason))


@task_app.command("apply")
def task_apply(identifier: str) -> None:
    """Apply only the verified candidate, or resume its existing apply journal."""
    from forge.workflow import apply

    _report_action(lambda: apply(Path.cwd(), identifier))
