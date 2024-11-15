from __future__ import annotations

import argparse

import nox
from nox import Session

from exasol.toolbox.metrics import (
    Format,
    create_report,
    format_report,
)
from noxconfig import PROJECT_CONFIG


@nox.session(name="project:report", python=False)
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
            - :code:`nox -s test:coverage`
            - :code:`nox -s lint:code`
            - :code:`nox -s lint:security`
    """
    formats = tuple(fmt.name.lower() for fmt in Format)
    usage = "nox -s project:report -- [options]"
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
        PROJECT_CONFIG.root / ".security.json",
    )
    if not all(file.exists() for file in required_files):
        session.error(
            "Please make sure you run the `test:coverage`, `lint:security` and the `lint:code` target first"
        )
    sha1 = str(
        session.run("git", "rev-parse", "HEAD", external=True, silent=True)
    ).strip()
    args: argparse.Namespace = parser.parse_args(args=session.posargs)
    project_report = create_report(commit=sha1)
    fmt = Format.from_string(args.format)

    print(format_report(project_report, fmt))
