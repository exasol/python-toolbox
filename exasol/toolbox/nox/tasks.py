from __future__ import annotations

__all__ = [
    "Mode",
    "fix",
    "check",
    "lint",
    "type_check",
    "unit_tests",
    "integration_tests",
    "coverage",
    "build_docs",
    "open_docs",
    "clean_docs",
]

import argparse
import shutil
import webbrowser
from collections import ChainMap
from enum import (
    Enum,
    auto,
)
from functools import partial
from pathlib import Path
from typing import (
    Any,
    Iterable,
    MutableMapping,
)

import nox
from nox import Session

from exasol.toolbox.metrics import (
    Format,
    create_report,
    format_report,
)
from exasol.toolbox.project import python_files as _python_files
from noxconfig import (
    PROJECT_CONFIG,
    Config,
)

_DOCS_OUTPUT_DIR = ".html-documentation"
_PATH_FILTER = tuple(["dist", ".eggs", "venv"] + list(Config.path_filters))

python_files = partial(_python_files, path_filters=_PATH_FILTER)


class Mode(Enum):
    Fix = auto()
    Check = auto()


def _context(session: Session, **kwargs: Any) -> MutableMapping[str, Any]:
    parser = _context_parser()
    namespace, _ = parser.parse_known_args(session.posargs)
    cli_context: MutableMapping[str, Any] = vars(namespace)
    default_context = {"db_version": "7.1.9", "coverage": False}
    # Note: ChainMap scans last to first
    return ChainMap(kwargs, cli_context, default_context)


def _context_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--db-version")
    parser.add_argument("--coverage", action="store_true")
    return parser


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


def _test_command(
    path: Path, config: Config, context: MutableMapping[str, Any]
) -> Iterable[str]:
    base_command = ["poetry", "run"]
    coverage_command = (
        ["coverage", "run", "-a", f"--rcfile={config.root / 'pyproject.toml'}", "-m"]
        if context["coverage"]
        else []
    )
    pytest_command = ["pytest", "-v", f"{path}"]
    return base_command + coverage_command + pytest_command


def _unit_tests(
    session: Session, config: Config, context: MutableMapping[str, Any]
) -> None:
    command = _test_command(config.root / "test" / "unit", config, context)
    session.run(*command)


def _integration_tests(
    session: Session, config: Config, context: MutableMapping[str, Any]
) -> None:
    _pre_integration_tests_hook = getattr(config, "pre_integration_tests_hook", _pass)
    _post_integration_tests_hook = getattr(config, "post_integration_tests_hook", _pass)

    success = _pre_integration_tests_hook(session, config, context)
    if not success:
        session.error("Failure during pre_integration_test_hook")

    command = _test_command(config.root / "test" / "integration", config, context)
    session.run(*command)

    success = _post_integration_tests_hook(session, config, context)
    if not success:
        session.error("Failure during post_integration_test_hook")


def _pass(
    _session: Session, _config: Config, _context: MutableMapping[str, Any]
) -> bool:
    """No operation"""
    return True


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


@nox.session(name="unit-tests", python=False)
def unit_tests(session: Session) -> None:
    """Runs all unit tests"""
    context = _context(session, coverage=False)
    _unit_tests(session, PROJECT_CONFIG, context)


@nox.session(name="integration-tests", python=False)
def integration_tests(session: Session) -> None:
    """
    Runs the all integration tests

    If a project needs to execute code pre-/post the test execution,
    it should provide appropriate hooks on their config object.
        * pre_integration_tests_hook(session: Session, config: Config, context: MutableMapping[str, Any]) -> bool:
        * post_integration_tests_hook(session: Session, config: Config, context: MutableMapping[str, Any]) -> bool:
    """
    context = _context(session, coverage=False)
    _integration_tests(session, PROJECT_CONFIG, context)


@nox.session(name="coverage", python=False)
def coverage(session: Session) -> None:
    """Runs all tests (unit + integration) and reports the code coverage"""
    context = _context(session, coverage=True)
    _coverage(session, PROJECT_CONFIG, context)


def _coverage(
    session: Session, config: Config, context: MutableMapping[str, Any]
) -> None:
    command = ["poetry", "run", "coverage", "report", "-m"]
    coverage_file = config.root / ".coverage"
    coverage_file.unlink(missing_ok=True)
    _unit_tests(session, config, context)
    _integration_tests(session, config, context)
    session.run(*command)


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
        _DOCS_OUTPUT_DIR,
    )


@nox.session(name="open-docs", python=False)
def open_docs(session: Session) -> None:
    """Opens the built project documentation"""
    docs_folder = PROJECT_CONFIG.root / _DOCS_OUTPUT_DIR
    if not docs_folder.exists():
        session.error(f"No documentation could be found. {docs_folder} is missing")
    index = docs_folder / "index.html"
    webbrowser.open_new_tab(index.as_uri())


@nox.session(name="clean-docs", python=False)
def clean_docs(_session: Session) -> None:
    """Removes the documentations build folder"""
    docs_folder = PROJECT_CONFIG.root / _DOCS_OUTPUT_DIR
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
