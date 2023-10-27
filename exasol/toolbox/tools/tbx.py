import typer

from exasol.toolbox.tools import (
    security,
    workflow,
)

CLI = typer.Typer()
CLI.add_typer(workflow.CLI, name="workflow", help="Manage github workflows")
CLI.add_typer(security.CLI, name="security", help="Security related helpers")


if __name__ == "__main__":
    CLI()
