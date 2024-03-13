from __future__ import annotations

__all__ = [
    "Mode",
    "build_docs",
    "check",
    "clean_docs",
    "coverage",
    "fix",
    "integration_tests",
    "lint",
    "open_docs",
    "prepare_release",
    "type_check",
    "unit_tests",
]


import argparse
import shutil
import webbrowser
from typing import Iterable

import nox
from nox import Session

from exasol.toolbox.metrics import (
    Format,
    create_report,
    format_report,
)
from exasol.toolbox.nox._release import prepare_release
from exasol.toolbox.nox._shared import (
    DOCS_OUTPUT_DIR,
    Mode,
    _context,
    _version,
    python_files,
)
from exasol.toolbox.nox._test import (
    _coverage,
    coverage,
    integration_tests,
    unit_tests,
)
from noxconfig import (
    PROJECT_CONFIG,
    Config,
)


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
def fix(session: Session) -> None:
    """Runs all automated fixes on the code base"""
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _version(session, Mode.Fix, PROJECT_CONFIG.version_file)
    _pyupgrade(session, py_files)
    _code_format(session, Mode.Fix, py_files)


@nox.session(name="check", python=False)
def check(session: Session) -> None:
    """Runs all available checks on the project"""
    context = _context(session, coverage=True)
    py_files = [f"{file}" for file in python_files(PROJECT_CONFIG.root)]
    _version(session, Mode.Check, PROJECT_CONFIG.version_file)
    _pyupgrade(session, py_files)
    _code_format(session, Mode.Check, py_files)
    _pylint(session, py_files)
    _type_check(session, py_files)
    _coverage(session, PROJECT_CONFIG, context)


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


@nox.session(name="build-docs", python=False)
def build_docs(session: Session) -> None:
    """Builds the project documentation"""
    _build_docs(session, PROJECT_CONFIG)


def _build_docs(session: nox.Session, config: Config) -> None:
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-W",
        "-b",
        "html",
        f"{config.doc}",
        DOCS_OUTPUT_DIR,
    )


@nox.session(name="open-docs", python=False)
def open_docs(session: Session) -> None:
    """Opens the built project documentation"""
    docs_folder = PROJECT_CONFIG.root / DOCS_OUTPUT_DIR
    if not docs_folder.exists():
        session.error(f"No documentation could be found. {docs_folder} is missing")
    index = docs_folder / "index.html"
    webbrowser.open_new_tab(index.as_uri())


@nox.session(name="clean-docs", python=False)
def clean_docs(_session: Session) -> None:
    """Removes the documentations build folder"""
    docs_folder = PROJECT_CONFIG.root / DOCS_OUTPUT_DIR
    if docs_folder.exists():
        shutil.rmtree(docs_folder)


@nox.session(name="report", python=False)
def report(session: Session) -> None:
    """
    Collects and generates metrics summary for the workspace

    Attention:

        Pre-requisites:

        * Make sure you remove old and outdated artifacts
            - e.g. by running one of the following commands
                * :code:`git clean -xdf`
                * :code:`rm .coverage .lint.txt`

        * Run the following targets:
            - :code:`nox -s coverage`
            - :code:`nox -s lint`
    """
    formats = tuple(fmt.name.lower() for fmt in Format)
    usage = "nox -s report -- [options]"
    parser = argparse.ArgumentParser(
        description="Generates status report for the project", usage=usage
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default=formats[0],
        help="Output format to produce.",
        choices=formats,
    )
    required_files = (
        PROJECT_CONFIG.root / ".coverage",
        PROJECT_CONFIG.root / ".lint.txt",
    )
    if not all(file.exists() for file in required_files):
        session.error(
            "Please make sure you run the `coverage` and the `lint` target first"
        )
    sha1 = str(
        session.run("git", "rev-parse", "HEAD", external=True, silent=True)
    ).strip()
    args: argparse.Namespace = parser.parse_args(args=session.posargs)
    project_report = create_report(commit=sha1)
    fmt = Format.from_string(args.format)

    print(format_report(project_report, fmt))
