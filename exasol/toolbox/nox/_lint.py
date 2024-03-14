from __future__ import annotations

from typing import Iterable

import nox
from nox import Session

from exasol.toolbox.nox._shared import python_files
from noxconfig import PROJECT_CONFIG


def _pylint(session: Session, files: Iterable[str]) -> None:
    session.run("poetry", "run", "python", "-m", "pylint", *files)


def _type_check(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
        "mypy",
        "--explicit-package-bases",
        "--namespace-packages",
        "--show-error-codes",
        "--pretty",
        "--show-column-numbers",
        "--show-error-context",
        "--scripts-are-modules",
        *files,
    )


@nox.session(python=False)
def lint(session: Session) -> None:
    """Runs the linter on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _pylint(session, py_files)


@nox.session(name="type-check", python=False)
def type_check(session: Session) -> None:
    """Runs the type checker on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _type_check(session, py_files)
