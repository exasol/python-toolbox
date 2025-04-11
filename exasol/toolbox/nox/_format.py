from __future__ import annotations

from typing import Iterable

import nox
from nox import Session

from exasol.toolbox.nox._shared import (
    Mode,
    _version,
    python_files,
)
from noxconfig import PROJECT_CONFIG


def _code_format(session: Session, mode: Mode, files: Iterable[str]) -> None:
    def command(*args: str) -> Iterable[str]:
        return args if mode == Mode.Fix else list(args) + ["--check"]

    session.run(*command("isort"), *files)
    session.run(*command("black"), *files)


def _pyupgrade(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
        "pyupgrade",
        "--py38-plus",
        "--exit-zero-even-if-changed",
        *files,
    )


@nox.session(name="project:fix", python=False)
def fix(session: Session) -> None:
    """Runs all automated fixes on the code base"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _version(session, Mode.Fix, PROJECT_CONFIG.version_file)
    _pyupgrade(session, py_files)
    _code_format(session, Mode.Fix, py_files)


@nox.session(name="project:format", python=False)
def fmt_check(session: Session) -> None:
    """Checks the project for correct formatting"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _code_format(session=session, mode=Mode.Check, files=py_files)
