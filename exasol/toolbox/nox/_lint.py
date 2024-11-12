from __future__ import annotations

from typing import Iterable

import nox
from nox import Session

from exasol.toolbox.nox._shared import python_files
from noxconfig import PROJECT_CONFIG


def _pylint(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
        "python",
        "-m",
        "pylint",
        "--output-format",
        "colorized,json:.lint.json,text:.lint.txt",
        *files,
    )


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


def _security_lint(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--format",
        "json",
        "--output",
        ".security.json",
        "--exit-zero",
        *files,
    )
    session.run(
        "poetry",
        "run",
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--exit-zero",
        *files,
    )


@nox.session(python=False)
def lint(session: Session) -> None:
    """Runs the linter on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _pylint(session, py_files)


@nox.session(name="lint:typing", python=False)
def type_check(session: Session) -> None:
    """Runs the type checker on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _type_check(session, py_files)


@nox.session(name="lint:security", python=False)
def security_lint(session: Session) -> None:
    """Runs the security linter on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _security_lint(session, list(
        filter(lambda file: "test" not in file, py_files)))
