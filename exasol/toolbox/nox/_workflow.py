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
        "--name",  # Changed to singular
        default=ALL,
        choices=["all"] + WORKFLOW_NAMES,
        help="Select one template by name or 'all' to update everything.",
        required=True,
    )
    return parser


@nox.session(name="workflow:update", python=False)
def update_workflow(session: Session) -> None:
    """
    Update (or install if it's not yet existing) one or all generated GitHub workflow(s)
    """
    parser = _create_parser()
    args = parser.parse_args(session.posargs)

    # Ensure that the GitHub workflow directory exists
    PROJECT_CONFIG.github_workflow_directory.mkdir(parents=True, exist_ok=True)

    update_selected_workflow(workflow_name=args.name, config=PROJECT_CONFIG)
