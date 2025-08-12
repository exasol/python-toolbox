from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import nox
from nox import Session

from exasol.toolbox.nox._shared import (
    Mode,
    _version,
    python_files,
)
from noxconfig import (
    PROJECT_CONFIG,
    Config,
)

_PYUPGRADE_ARGS = ("--py39-plus",)


def _code_format(session: Session, mode: Mode, directory: Path) -> None:
    def command(*args: str) -> Iterable[str]:
        return args if mode == Mode.Fix else list(args) + ["--check"]

    session.run(*command("isort"), directory)
    session.run(*command("black"), directory)


def _pyupgrade(session: Session, config: Config, files: Iterable[str]) -> None:
    pyupgrade_args = getattr(config, "pyupgrade_args", _PYUPGRADE_ARGS)
    session.run(
        "pyupgrade",
        *pyupgrade_args,
        "--exit-zero-even-if-changed",
        *files,
    )


@nox.session(name="project:fix", python=False)
def fix(session: Session) -> None:
    """Runs all automated fixes on the code base"""
    py_files = python_files(PROJECT_CONFIG.root)
    _version(session, Mode.Fix)
    _pyupgrade(session, config=PROJECT_CONFIG, files=py_files)
    _code_format(session, Mode.Fix, PROJECT_CONFIG.root)


@nox.session(name="project:format", python=False)
def fmt_check(session: Session) -> None:
    """Checks the project for correct formatting_code"""
    _code_format(session=session, mode=Mode.Check, directory=PROJECT_CONFIG.root)
