from __future__ import annotations

from enum import (
    Enum,
    auto,
)
from pathlib import Path
from typing import Iterable

import nox
from nox import Session
from nox.sessions import SessionRunner

from exasol.toolbox.project import python_files
from noxconfig import (
    MIN_CODE_COVERAGE,
    PROJECT_ROOT,
    VERSION_FILE,
)


class Mode(Enum):
    Fix = auto()
    Check = auto()
    Report = auto()


def find_session_runner(session: Session, name: str) -> SessionRunner:
    """Helper function to find parameterized action by name"""
    for s, _ in session._runner.manifest.list_all_sessions():
        if name in s.signatures:
            return s
    session.error(f"Could not find a nox session by the name {name!r}")


def _code_format(session: Session, mode: Mode, files: Iterable[str]) -> None:
    isort = ["poetry", "run", "isort", "-v"]
    black = ["poetry", "run", "black"]
    isort = isort if mode == Mode.Fix else isort + ["--check"]
    black = black if mode == Mode.Fix else black + ["--check"]
    session.run(*isort, *files)
    session.run(*black, *files)


def _pyupgrade(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
        "pyupgrade",
        "--py38-plus",
        "--exit-zero-even-if-changed",
        *files,
    )


def _version(session: Session, mode: Mode, version_file: Path) -> None:
    command = ["poetry", "run", "version-check", "--fix"]
    command = command if mode == Mode.Check else command + ["--fix"]
    session.run(*command, f"{version_file}")


def _pylint(session: Session, files: Iterable[str]) -> None:
    session.run("poetry", "run", "python", "-m", "pylint", *files)


def _type_check(session: Session, files: Iterable[str]) -> None:
    session.run(
        "poetry",
        "run",
        "mypy",
        "--strict",
        "--explicit-package-bases",
        "--namespace-packages",
        "--show-error-codes",
        "--pretty",
        "--show-column-numbers",
        "--show-error-context",
        "--scripts-are-modules",
        *files,
    )


def _sources(project_root: Path) -> Iterable[Path]:
    exasol_ns = project_root / "exasol"
    sources = [project_root]
    if exasol_ns.exists():
        sources.append(exasol_ns)
    return sources


def _test_command(project_root: Path, path: Path) -> Iterable[str]:
    return [
        "poetry",
        "run",
        "coverage",
        "run",
        "-a",
        *[f"--source={src}" for src in _sources(project_root)],
        "-m",
        "pytest",
        f"{path}",
    ]


def _unit_tests(session: Session, project_root: Path) -> None:
    command = _test_command(project_root, project_root / "test" / "unit")
    session.run(*command)


def _integration_tests(session: Session, project_root: Path) -> None:
    command = _test_command(project_root, project_root / "test" / "integration")
    session.run(*command)


@nox.session(python=False)
def fix(session: Session) -> None:
    """Runs all automated fixes on the code base"""
    py_files = [f"{file}" for file in python_files(PROJECT_ROOT)]
    _version(session, Mode.Fix, VERSION_FILE)
    _pyupgrade(session, py_files)
    _code_format(session, Mode.Fix, py_files)


@nox.session(name="check", python=False)
def check(session: Session) -> None:
    py_files = [f"{file}" for file in python_files(PROJECT_ROOT)]
    _version(session, Mode.Check, VERSION_FILE)
    _pyupgrade(session, py_files)
    _code_format(session, Mode.Check, py_files)
    _pylint(session, py_files)
    _type_check(session, py_files)
    _coverage(session, PROJECT_ROOT, Mode.Check)


@nox.session(python=False)
def lint(session: Session) -> None:
    py_files = [f"{file}" for file in python_files(PROJECT_ROOT)]
    _pylint(session, py_files)


@nox.session(name="type-check", python=False)
def type_check(session: Session) -> None:
    py_files = [f"{file}" for file in python_files(PROJECT_ROOT)]
    _type_check(session, py_files)


@nox.session(name="unit-tests", python=False)
def unit_tests(session: Session) -> None:
    _unit_tests(session, PROJECT_ROOT)


def _coverage(session: Session, project_root: Path, mode: Mode) -> None:
    command = ["poetry", "run", "coverage", "report", "-m"]
    coverage_file = project_root / ".coverage"
    coverage_file.unlink(missing_ok=True)
    _unit_tests(session, PROJECT_ROOT)
    _integration_tests(session, PROJECT_ROOT)

    if mode == Mode.Check:
        command += [f"--fail-under={MIN_CODE_COVERAGE}"]
    elif mode == Mode.Report:
        pass  # default settings are just fine for report mode
    else:
        session.error(f"The mode [{mode}] is not supported by the coverage command")

    session.run(*command)


@nox.session(name="coverage", python=False)
def coverage(session: Session) -> None:
    _coverage(session, PROJECT_ROOT, Mode.Report)


# TODO: build docs [--check]
# TODO: build multi version docs [--check]
# TODO: open docs
# TODO: deploy docs to doc(s) branch
