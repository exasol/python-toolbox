import typer

from exasol.toolbox.tools import (
    security,
    workflow,
)

CLI = typer.Typer()
CLI.add_typer(workflow.CLI, name="workflow")
CLI.add_typer(security.CLI, name="security")


if __name__ == "__main__":
    CLI()
