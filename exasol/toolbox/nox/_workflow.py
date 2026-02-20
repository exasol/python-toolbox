from __future__ import annotations

import argparse

import nox
from nox import Session

from exasol.toolbox.util.workflows.workflow import (
    WORKFLOW_CHOICES,
    update_workflow,
)
from noxconfig import PROJECT_CONFIG


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nox -s workflow:generate",
        usage="nox -s workflow:generate -- [-h]  <workflow_choice>",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "workflow_choice",
        choices=WORKFLOW_CHOICES,
        help="Select one workflow or 'all' to all workflows.",
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

    update_workflow(workflow_choice=args.workflow_choice, config=PROJECT_CONFIG)
