from pathlib import Path

import typer

from exasol.toolbox.tools import template

CLI = typer.Typer()
PKG = "exasol.toolbox.templates.github.workflows"
TEMPLATE_TYPE = "workflow"
LEXER = "yaml"


@CLI.command(name="list")
def list_workflows(
    columns: bool = typer.Option(
        False, "--columns", "-c", help="use column style presentation like `ls`"
    )
) -> None:
    """List all available workflows."""
    template.list_templates(columns=columns, pkg=PKG)


@CLI.command(name="show")
def show_workflow(
    workflow: str = typer.Argument(..., help="Workflow which shall be shown."),
) -> None:
    """Shows a specific workflow."""
    template.show_templates(
        template=workflow, pkg=PKG, template_type=TEMPLATE_TYPE, lexer=LEXER
    )


@CLI.command(name="diff")
def diff_workflow(
    workflow: str = typer.Argument(..., help="workflow which shall be diffed."),
    dest: Path = typer.Argument(
        Path("./.github/workflows"),
        help="target directory to diff the workflow against.",
    ),
) -> None:
    """Diff a specific workflow against the installed one."""
    template.diff_template(
        template=workflow, dest=dest, pkg=PKG, template_type=TEMPLATE_TYPE
    )


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
    template.install_template(
        template=workflow, dest=dest, pkg=PKG, template_type=TEMPLATE_TYPE
    )


@CLI.command(name="update")
def update_workflow(
    workflow: str = typer.Argument("all", help="name of the workflow to install."),
    dest: Path = typer.Argument(
        Path("./.github/workflows"), help="target directory to install the workflow to."
    ),
    confirm: bool = typer.Option(
        False, help="Automatically confirm overwriting the existing workflow(s)"
    ),
) -> None:
    """Similar to install but checks for existing workflows and shows diff"""
    template.update_template(
        template=workflow,
        dest=dest,
        confirm=confirm,
        pkg=PKG,
        template_type=TEMPLATE_TYPE,
    )


if __name__ == "__main__":
    CLI()
