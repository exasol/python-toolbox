import json
import sys
from typing import (
    Iterable,
)

import typer
from rich.console import Console

stdout = Console()
stderr = Console(stderr=True)

CLI = typer.Typer()

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Issue:
    cve: str
    cwe: str
    description: str
    coordinates: str
    references: tuple
    # Note: Add support additional (custom) information e.g. dependency tree etc.


def from_maven(report: str) -> Iterable[Issue]:
    # Notes:
    # * Consider adding warnings if there is the same cve with multiple cooardinates
    report = json.loads(report)
    dependencies = report["vulnerable"]  # type: ignore
    for _, dependency in dependencies.items():  # type: ignore
        for v in dependency["vulnerabilities"]:  # type: ignore
            references = [v["reference"]] + v["externalReferences"]
            yield Issue(
                cve=v["cve"],
                cwe=v["cwe"],
                description=v["description"],
                coordinates=dependency["coordinates"],
                references=tuple(references),
            )


@CLI.command(name="convert")
def convert(
        format: str = typer.Argument(..., help="input format to be converted."),
) -> None:
    if format == 'maven':
        issues = from_maven(sys.stdin.read())
        for issue in issues:
            issue = asdict(issue)  # type: ignore
            stdout.print(json.dumps(issue))
    else:
        stderr.print("Unsupported format")
        sys.exit(-1)


@CLI.command(name="filter")
def filter(
        _: str = typer.Argument(..., help="filter type to apply"),
) -> None:
    for line in sys.stdin:
        stdout.print(line, end='')


@CLI.command(name="create")
def create() -> None:
    for line in sys.stdin:
        stdout.print(line, end='')

    title = 'test'
    body = 'another test'
    command = [
        'gh',
        'issue',
        'create',
        '--label',
        'security',
        '--title',
        title,
        '--body',
        body
    ]

    import subprocess
    result = subprocess.run(command, check=True)
    print(result)


if __name__ == "__main__":
    CLI()
