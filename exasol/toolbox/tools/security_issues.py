import sys

import typer
from rich.console import Console

stdout = Console()
stderr = Console(stderr=True)

CLI = typer.Typer()


@CLI.command(name="convert")
def convert(
        format: str = typer.Argument(..., help="input format to be converted."),
) -> None:
    for line in sys.stdin:
        stdout.print(line)


@CLI.command(name="filter")
def filter(
        type: str = typer.Argument(..., help="filter type to apply"),
) -> None:
    for line in sys.stdin:
        stdout.print(line)


@CLI.command(name="create")
def create() -> None:
    for line in sys.stdin:
        stdout.print(line)


if __name__ == "__main__":
    CLI()
