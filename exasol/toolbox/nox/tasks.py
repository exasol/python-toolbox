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

import nox
from nox import Session

from exasol.toolbox.metrics import (
    Format,
    create_report,
    format_report,
)
from exasol.toolbox.nox._documentation import (
    build_docs,
    clean_docs,
    open_docs,
)
from exasol.toolbox.nox._format import (
    _code_format,
    _pyupgrade,
    fix,
)
from exasol.toolbox.nox._lint import (
    _pylint,
    _type_check,
    lint,
    type_check,
)
from exasol.toolbox.nox._release import prepare_release
from exasol.toolbox.nox._shared import (
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
from noxconfig import PROJECT_CONFIG


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
