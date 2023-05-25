import typer

from exasol.toolbox.tools import workflow

CLI = typer.Typer(rich_markup_mode=None, rich_help_panel=False)
CLI.add_typer(workflow.CLI, name="workflow")

if __name__ == "__main__":
    CLI()
