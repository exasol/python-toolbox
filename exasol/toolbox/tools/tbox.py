import typer

from exasol.toolbox.tools import workflow

CLI = typer.Typer()
CLI.add_typer(workflow.CLI, name="workflow")

if __name__ == "__main__":
    CLI()
