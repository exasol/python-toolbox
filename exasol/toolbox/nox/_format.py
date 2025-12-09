from __future__ import annotations

from collections.abc import Iterable

import nox
from nox import Session

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.nox._shared import (
    Mode,
    _version,
    check_for_config_attribute,
    get_filtered_python_files,
)
from noxconfig import (
    PROJECT_CONFIG,
)


def _code_format(session: Session, mode: Mode, files: Iterable[str]) -> None:
    def command(*args: str) -> Iterable[str]:
        return args if mode == Mode.Fix else list(args) + ["--check"]

    session.run(*command("isort"), *files)
    session.run(*command("black"), *files)


def _pyupgrade(session: Session, config: BaseConfig, files: Iterable[str]) -> None:
    check_for_config_attribute(config, "pyupgrade_argument")
    session.run(
        "pyupgrade",
        *config.pyupgrade_argument,
        "--exit-zero-even-if-changed",
        *files,
    )


def _ruff(session: Session, mode: Mode, files: Iterable[str]):
    def command(*args: str) -> Iterable[str]:
        return args if mode == Mode.Check else list(args) + ["--fix"]

    session.run(*command("ruff", "check"), *files)


@nox.session(name="format:fix", python=False)
def fix_format(session: Session) -> None:
    """Runs all automated format fixes on the code base"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.root_path)
    _version(session, Mode.Fix)
    _pyupgrade(session, config=PROJECT_CONFIG, files=py_files)
    _ruff(session, mode=Mode.Fix, files=py_files)
    _code_format(session, Mode.Fix, py_files)


@nox.session(name="format:check", python=False)
def check_format(session: Session) -> None:
    """Checks the project for correct formatting"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.root_path)
    _ruff(session, mode=Mode.Check, files=py_files)
    _code_format(session=session, mode=Mode.Check, files=py_files)
