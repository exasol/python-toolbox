from __future__ import annotations

from collections.abc import Iterable

import nox
from nox import Session

from exasol.toolbox.nox._shared import get_filtered_python_files
from noxconfig import PROJECT_CONFIG


def _pylint(session: Session, files: Iterable[str]) -> None:
    json_file = PROJECT_CONFIG.root_path / ".lint.json"

    session.run(
        "pylint",
        "--output-format",
        f"colorized,json:{json_file}",
        *files,
    )


def _type_check(session: Session, files: Iterable[str]) -> None:
    session.run(
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
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--format",
        "json",
        "--output",
        PROJECT_CONFIG.root_path / ".security.json",
        "--exit-zero",
        *files,
    )
    session.run(
        "bandit",
        "--severity-level",
        "low",
        "--quiet",
        "--exit-zero",
        *files,
    )


@nox.session(name="lint:code", python=False)
def lint(session: Session) -> None:
    """Runs the static code analyzer on the project"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.source_code_path)
    _pylint(session=session, files=py_files)


@nox.session(name="lint:typing", python=False)
def type_check(session: Session) -> None:
    """Runs the type checker on the project"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.root_path)
    _type_check(session=session, files=py_files)


@nox.session(name="lint:security", python=False)
def security_lint(session: Session) -> None:
    """Runs the security linter on the project"""
    py_files = get_filtered_python_files(PROJECT_CONFIG.source_code_path)
    _security_lint(session=session, files=py_files)
