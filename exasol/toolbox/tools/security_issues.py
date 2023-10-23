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
