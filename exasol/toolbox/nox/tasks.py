from __future__ import annotations
from typing import Any, Callable, Dict

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
import json
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
    formats = ('text', 'json', 'markdown')
    usage = "nox -s report -- [options]"
    parser = argparse.ArgumentParser(description="Generates status report for the project", usage=usage)
    parser.add_argument(
        "-f", "--format",
        type=str,
        default=formats[0],
        help="Output format to produce.",
        choices=formats,
    )

    def _markdown(data: Any) -> str:
        from inspect import cleandoc
        return cleandoc("""
        # Status Report

        | Category | Status                                                          |
        | --- |-----------------------------------------------------------------|
        | Coverage | ![Coverage](https://img.shields.io/badge/-{coverage:.2f}%25-orange)         |
        | Static Code Analysis | ![Static Code Analysis](https://img.shields.io/badge/-{static_code_analysis}-green) |
        | Maintainability | ![Maintainability](https://img.shields.io/badge/-{maintainability}-black)      |
        | Reliability | ![Reliability](https://img.shields.io/badge/-{reliability}-black)          |
        | Security | ![Security](https://img.shields.io/badge/-{security}-black)             |
        | Technical Debt | ![Technical Debt](https://img.shields.io/badge/-{technical_debt}-black)       |
        """).format(**data)

    args: argparse.Namespace = parser.parse_args(args=session.posargs)
    formatter: Dict[str, Callable[..., Any]] = {'text': lambda data: data, 'json': lambda data: json.dumps(data),
                                                'markdown': _markdown}
    data = _report()
    print(formatter[args.format](data))


def _report() -> Any:
    coverage_file = Path(".coverage")
    lint_file = Path(".lint.txt")
    required_files = {coverage_file, lint_file}
    missing_files = {f"{f}" for f in required_files if not f.exists()}
    if missing_files:
        raise Exception(
            f"The following files are missing: {', '.join(missing_files)}, "
            "make sure you run the lint and coverage target first"
        )
    cov = _extract_coverage(coverage_file)
    static = _extract_static_analysis_score(lint_file)

    # TODO: Add sha1 and branch to report, maybe date
    return {
        "coverage": cov,
        "static_code_analysis": static,
        "maintainability": "n/a",
        "reliability": "n/a",
        "security": "n/a",
        "technical_debt": "n/a",
    }


def _extract_coverage(file: Path) -> Any:
    import json
    from subprocess import run
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as dir:
        tmp_dir = Path(dir)
        report = tmp_dir / "coverage.json"
        d = run(
            ["coverage", "json", f"--data-file={file}", "-o", f"{report}"],
            capture_output=True, check=True
        )
        with open(report, 'r') as r:
            coverage = json.load(r)
            return coverage["totals"]["percent_covered"]


class Interval:
    def __init__(self, start: Any, end: Any):
        self.start = start
        self.end = end

    def __contains__(self, item: Any) -> Any:
        return self.start <= item < self.end


def _score_to_rating(score: Any) -> Any:
    mapping = {
        Interval(8, 11): "A",
        Interval(6, 8): "B",
        Interval(4, 6): "C",
        Interval(3, 4): "D",
        Interval(1, 3): "E",
        Interval(0, 1): "F",
    }
    for interval, rating in mapping.items():
        if score in interval:
            return rating

    raise Exception("Uncategorized score")


def _extract_static_analysis_score(file: Path) -> Any:
    import re

    expr = re.compile(r"^Your code has been rated at (\d+.\d+)/.*", re.MULTILINE)
    with open(file) as results:
        data = results.read()

    matches = expr.search(data)
    if matches:
        groups = matches.groups()
    score: Any = None
    try:
        group = groups[0]
        score = float(group)
        score = f'{_score_to_rating(score)}'
    except Exception as ex:
        # log error reason
        score = "n/a"

    return score
