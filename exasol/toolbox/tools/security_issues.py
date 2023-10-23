import typer
from rich.console import Console

stdout = Console()
stderr = Console(stderr=True)

CLI = typer.Typer()


@CLI.command(name="convert")
def convert() -> None:
    pass


@CLI.command(name="filter")
def filter() -> None:
    pass


@CLI.command(name="create")
def create() -> None:
    pass


if __name__ == "__main__":
    CLI()
