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


def _issues() -> Mapping[str, Any]:
    pkg = "exasol.toolbox.templates.github.ISSUE_TEMPLATE"

    def _normalize(name: str) -> str:
        name, ext = name.split(".")
        return name

    return {_normalize(w.name): w for w in resources.files(pkg).iterdir()}  # type: ignore


@CLI.command(name="list")
def list_issues(
    columns: bool = typer.Option(
        False, "--columns", "-c", help="use column style presentation like `ls`"
    )
) -> None:
    """List all available issues."""

    class List:
        def __init__(self, items: Any):
            self.items = items

        def __rich__(self) -> str:
            return "\n".join(self.items)

    output = List(_issues()) if not columns else Columns(_issues(), expand=True)
    stdout.print(output)


def _install_issue(
    src: Union[str, Path], dest: Union[str, Path], exists_ok: bool = False
) -> None:
    src, dest = Path(src), Path(dest)

    if dest.exists() and not exists_ok:
        raise FileExistsError("Issue already exists")

    with ExitStack() as stack:
        input_file = stack.enter_context(open(src, "rb"))
        output_file = stack.enter_context(open(dest, "wb"))
        output_file.write(input_file.read())


def _select_issues(issue: str) -> Mapping[str, Any]:
    issues = _issues()
    if issue != "all" and issue not in issues:
        raise Exception(f"Issue <{issue}> is unknown")
    issues = (
        issues
        if issue == "all"
        else {name: path for name, path in issues.items() if issue == name}
    )
    return issues


@CLI.command(name="install")
def install_issue(
    issue: str = typer.Argument("all", help="name of the issue to install."),
    dest: Path = typer.Argument(
        Path("./.github/ISSUE_TEMPLATE"), help="target directory to install the issue to."
    ),
) -> None:
    """
    Installs the requested issue into the target directory.

    Attention: If there is an existing issue with the same name it will be overwritten!
    """
    if not dest.exists():
        dest.mkdir()

    try:
        issues = _select_issues(issue)
    except Exception as ex:
        stderr.print(f"[red]{ex}[/red]")
        raise typer.Exit(-1)

    for issue, path in issues.items():
        destination = dest / f"{issue}.md"
        _install_issue(path, destination, exists_ok=True)
        stderr.print(f"Installed {issue} in {destination}")