from enum import (
    Enum,
    auto,
)
from pathlib import Path

from nox import Session


class Mode(Enum):
    Fix = auto()
    Check = auto()


def _version(session: Session, mode: Mode, version_file: Path) -> None:
    command = ["poetry", "run", "version-check"]
    command = command if mode == Mode.Check else command + ["--fix"]
    session.run(*command, f"{version_file}")
