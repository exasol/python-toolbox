from __future__ import annotations

from typing import Iterable
import argparse
from pathlib import Path

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
            *files)


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


def _import_lint(session: Session, path: Path) -> None:
    session.run(
        "poetry",
        "run",
        "lint-imports",
        "--config",
        path
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


@nox.session(name="security", python=False)
def security_lint(session: Session) -> None:
    """Runs the security linter on the project"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _security_lint(session, list(filter(lambda file: "test" not in file, py_files)))


@nox.session(name="import-lint", python=False)
def import_lint(session: Session) -> None:
    """(experimental) Runs import linter on the project"""
    parser = argparse.ArgumentParser(
        usage="nox -s import-lint -- [options]",
        description="Runs the import linter on the project"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="path to the configuration file for the importlinter",
        metavar="TEXT"
    )

    args: argparse.Namespace = parser.parse_args(args=session.posargs)
    file: str = args.config
    path: Path | None = None
    if file is None:
        path = getattr(PROJECT_CONFIG, "import_linter_config", Path(".import_linter_config"))
    else:
        path = Path(file)
    if not path.exists():
        session.error(
            "Please make sure you have a configuration file for the importlinter"
        )
    _import_lint(session=session, path=path)

