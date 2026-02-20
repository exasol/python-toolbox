from __future__ import annotations

import argparse

import nox
from nox import Session

from exasol.toolbox.util.workflows.workflow import (
    ALL,
    WORKFLOW_NAMES,
    update_selected_workflow,
)
from noxconfig import PROJECT_CONFIG


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nox -s workflow:update",
        usage="nox -s workflow:update -- [-h] --name",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--name",
        default=ALL,
        choices=WORKFLOW_NAMES,
        help="Select one template by name or 'all' to update everything.",
        required=True,
    )
    return parser


@nox.session(name="workflow:generate", python=False)
def generate_workflow(session: Session) -> None:
    """
    Generate or update the specified GitHub workflow or all of them.
    """
    parser = _create_parser()
    args = parser.parse_args(session.posargs)

    PROJECT_CONFIG.github_workflow_directory.mkdir(parents=True, exist_ok=True)

    update_selected_workflow(workflow_name=args.name, config=PROJECT_CONFIG)
