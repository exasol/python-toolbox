import difflib
import io
from contextlib import ExitStack
from pathlib import Path
from typing import (
    Any,
    Mapping,
    Union,
)

import importlib_resources as resources
import typer
from rich.columns import Columns
from rich.console import Console
from rich.syntax import Syntax

stdout = Console()
stderr = Console(stderr=True)

CLI = typer.Typer()


def _workflows() -> Mapping[str, Any]:
    pkg = "exasol.toolbox.templates.github.workflows"

    def _normalize(name: str) -> str:
        name, ext = name.split(".")
        return name

    return {_normalize(w.name): w for w in resources.files(pkg).iterdir()}  # type: ignore


@CLI.command(name="list")
def list_workflows(
    columns: bool = typer.Option(
        False, "--columns", "-c", help="use column style presentation like `ls`"
    )
) -> None:
    """List all available workflows."""

    class List:
        def __init__(self, items: Any):
            self.items = items

        def __rich__(self) -> str:
            return "\n".join(self.items)

    output = List(_workflows()) if not columns else Columns(_workflows(), expand=True)
    stdout.print(output)


@CLI.command(name="show")
def show_workflow(
    workflow: str = typer.Argument(..., help="Workflow which shall be shown."),
) -> None:
    """Shows a specific workflow."""
    workflows = _workflows()
    if workflow not in workflows:
        stdout.print(f"Unknown workflow <{workflow}>.", style="red")
        raise typer.Exit(code=1)

    workflow = workflows[workflow]
    stdout.print(Syntax(workflow.read_text(), "yaml"))  # type: ignore


@CLI.command(name="diff")
def diff_workflow(
    workflow: str = typer.Argument(..., help="Workflow which shall be diffed."),
    dest: Path = typer.Argument(
        Path("./.github/workflows"),
        help="target directory to diff the workflow against.",
    ),
) -> None:
    """Diff a specific workflow against the installed one."""
    workflows = _workflows()
    if workflow not in workflows:
        stdout.print(f"Unknown workflow <{workflow}>.", style="red")
        raise typer.Exit(code=1)

    # Use Any type to enable reuse of the variable/binding name
    old: Any = dest / f"{workflow}.yml"
    new: Any = Path(_workflows()[workflow])
    with ExitStack() as stack:
        old = stack.enter_context(open(old) if old.exists() else io.StringIO(""))
        new = stack.enter_context(open(new))
        old = old.read().split("\n")
        new = new.read().split("\n")

    diff = difflib.unified_diff(old, new, fromfile="old", tofile="new")
    stdout.print(Syntax("\n".join(diff), "diff"))


def _install_workflow(
    src: Union[str, Path], dest: Union[str, Path], exists_ok: bool = False
) -> None:
    src, dest = Path(src), Path(dest)

    if dest.exists() and not exists_ok:
        raise FileExistsError("Workflow already exists")

    with ExitStack() as stack:
        input_file = stack.enter_context(open(src))
        output_file = stack.enter_context(open(dest, "w"))
        output_file.write(input_file.read())


def _select_workflows(workflow: str) -> Mapping[str, Any]:
    workflows = _workflows()
    if workflow != "all" and workflow not in workflows:
        raise Exception(f"Workflow <{workflow}> is unknown")
    workflows = (
        workflows
        if workflow == "all"
        else {name: path for name, path in workflows.items() if workflow == name}
    )
    return workflows


@CLI.command(name="install")
def install_workflow(
    workflow: str = typer.Argument("all", help="name of the workflow to install."),
    dest: Path = typer.Argument(
        Path("./.github/workflows"), help="target directory to install the workflow to."
    ),
) -> None:
    """
    Installs the requested workflow into the target directory.

    Attention: If there is an existing workflow with the same name it will be overwritten!
    """
    if not dest.exists():
        dest.mkdir()

    try:
        workflows = _select_workflows(workflow)
    except Exception as ex:
        stderr.print(f"[red]{ex}[/red]")
        raise typer.Exit(-1)

    for workflow, path in workflows.items():
        destination = dest / f"{workflow}.yml"
        _install_workflow(path, destination, exists_ok=True)
        stderr.print(f"Installed {workflow} in {destination}")


@CLI.command(name="update")
def update_workflow(
    workflow: str = typer.Argument("all", help="name of the workflow to install."),
    dest: Path = typer.Argument(
        Path("./.github/workflows"), help="target directory to install the workflow to."
    ),
    confirm: bool = typer.Option(
        False, help="Automatically confirm overwritting exsisting workflow(s)"
    ),
) -> None:
    """Similar to install but checks for existing workflows and shows diff"""
    if not dest.exists():
        dest.mkdir()

    try:
        workflows = _select_workflows(workflow)
    except Exception as ex:
        stderr.print(f"[red]{ex}[/red]")
        raise typer.Exit(-1)

    if confirm:
        install_workflow(workflow, dest)
        raise typer.Exit(0)

    for workflow, path in workflows.items():
        destination = dest / f"{workflow}.yml"
        try:
            _install_workflow(path, destination, exists_ok=False)
            stderr.print(f"Updated {workflow} in {destination}")
        except Exception:
            show_diff = typer.confirm(
                f"Workflow <{workflow}> already exists, show diff?"
            )
            if show_diff:
                diff_workflow(workflow, dest)

            overwrite = typer.confirm(f"Overwrite existing workflow?")
            if overwrite:
                _install_workflow(path, destination, exists_ok=True)
                stderr.print(f"Updated {workflow} in {destination}")


if __name__ == "__main__":
    CLI()
