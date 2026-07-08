from pathlib import Path
from typing import Annotated

import typer

from .bootstrap import ForgeInitError, init_project

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
        return

    typer.echo(f"Forge project initialized: {project_name}")
    typer.echo(f"Created folders: {len(result.folders)}")
    typer.echo(f"Created files: {len(result.files)}")
    typer.echo("Next step: review PROJECT_STATE.md and begin architecture discovery.")
