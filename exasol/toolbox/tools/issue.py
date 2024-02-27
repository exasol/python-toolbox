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
        name, _ = name.split(".")
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


@CLI.command(name="show")
def show_issue(
    issue: str = typer.Argument(..., help="Issue which shall be shown."),
) -> None:
    """Shows a specific issue."""
    issues = _issues()
    if issue not in issues:
        stdout.print(f"Unknown issue <{issue}>.", style="red")
        raise typer.Exit(code=1)

    issue = issues[issue]
    stdout.print(Syntax.from_path(path=issue, encoding="utf-8", lexer="markdown"))  # type: ignore


@CLI.command(name="diff")
def diff_issue(
    issue: str = typer.Argument(..., help="issue which shall be diffed."),
    dest: Path = typer.Argument(
        Path("./.github/ISSUE_TEMPLATE"),
        help="target directory to diff the issue against.",
    ),
) -> None:
    """Diff a specific issue against the installed one."""
    issues = _issues()
    if issue not in issues:
        stdout.print(f"Unknown issue <{issue}>.", style="red")
        raise typer.Exit(code=1)

    # Use Any type to enable reuse of the variable/binding name
    old: Any = dest / f"{issue}.md"
    new: Any = Path(_issues()[issue])
    with ExitStack() as stack:
        old = stack.enter_context(open(old, encoding="utf-8") if old.exists() else io.StringIO(""))
        new = stack.enter_context(open(new, encoding="utf-8"))
        old = old.read().split("\n")
        new = new.read().split("\n")

    diff = difflib.unified_diff(old, new, fromfile="old", tofile="new")
    stdout.print(Syntax("\n".join(diff), "diff"))


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
        raise ValueError(f"Issue <{issue}> is unknown")
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

    for name, path in issues.items():
        destination = dest / f"{name}.md"
        _install_issue(path, destination, exists_ok=True)
        stderr.print(f"Installed {name} in {destination}")


@CLI.command(name="update")
def update_issue(
    issue: str = typer.Argument("all", help="name of the issue to install."),
    dest: Path = typer.Argument(
        Path("./.github/ISSUE_TEMPLATE"), help="target directory to install the issue to."
    ),
    confirm: bool = typer.Option(
        False, help="Automatically confirm overwritting exsisting issue(s)"
    ),
) -> None:
    """Similar to install but checks for existing issues and shows diff"""
    if not dest.exists():
        dest.mkdir()

    try:
        issues = _select_issues(issue)
    except Exception as ex:
        stderr.print(f"[red]{ex}[/red]")
        raise typer.Exit(-1)

    if confirm:
        install_issue(issue, dest)
        raise typer.Exit(0)

    for name, path in issues.items():
        destination = dest / f"{name}.md"
        try:
            _install_issue(path, destination, exists_ok=False)
            stderr.print(f"Updated {name} in {destination}")
        except Exception:
            show_diff = typer.confirm(
                f"issue <{name}> already exists, show diff?"
            )
            if show_diff:
                diff_issue(name, dest)

            overwrite = typer.confirm(f"Overwrite existing issue?")
            if overwrite:
                _install_issue(path, destination, exists_ok=True)
                stderr.print(f"Updated {name} in {destination}")


if __name__ == "__main__":
    CLI()
