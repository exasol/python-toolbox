import typer

from exasol.toolbox.tools import (
    issue,
    security,
)

CLI = typer.Typer()
CLI.add_typer(security.CLI, name="security", help="Security related helpers")
CLI.add_typer(issue.CLI, name="issue", help="Manage issue templates")

if __name__ == "__main__":
    CLI()
