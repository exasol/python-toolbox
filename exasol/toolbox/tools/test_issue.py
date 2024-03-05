import typer
from pathlib import Path
from rich.columns import Columns
import exasol.toolbox.tools.template as template

CLI = typer.Typer()
pkg = "exasol.toolbox.templates.github.ISSUE_TEMPLATE"


@CLI.command(name="list")
def list_issues(
    columns: bool = typer.Option(
        False, "--columns", "-c", help="use column style presentation like `ls`"
    )
) -> None:
    """List all available issues."""
    template.list_templates(columns, pkg) 



@CLI.command(name="show")
def show_issue(
    issue: str = typer.Argument(..., help="Issue which shall be shown."),
) -> None:
    """Shows a specific issue."""
    template.show_templates(issue, pkg, "issue", "makedown")


@CLI.command(name="diff")
def diff_issue(
    issue: str = typer.Argument(..., help="issue which shall be diffed."),
    dest: Path = typer.Argument(
        Path("./.github/ISSUE_TEMPLATE"),
        help="target directory to diff the issue against.",
    ),
) -> None:
    """Diff a specific issue against the installed one."""
    template.diff_template(issue, dest, pkg, "isssue", "markdown")


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
    template.install_template(issue, dest, pkg, "issue")


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
    template.update_template(issue, dest, confirm, pkg, "issue")


if __name__ == "__main__":
    CLI()
