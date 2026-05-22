from __future__ import annotations

import argparse

import nox
from nox import Session

from exasol.toolbox.util.workflows.workflow_orchestrator import (
    WORKFLOW_CHOICES,
    WorkflowOrchestrator,
)
from noxconfig import PROJECT_CONFIG


def _create_parser(session_name: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=f"nox -s {session_name}",
        usage=f"nox -s {session_name} -- [-h]  <workflow_choice>",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "workflow_choice",
        choices=WORKFLOW_CHOICES,
        help="Select one workflow or 'all' to all workflows.",
    )
    return parser


@nox.session(name="workflow:check", python=False)
def check_workflow(session: Session) -> None:
    """
    Check the specified GitHub workflow or all of them to see if any differ from
    the generated values. If any differ, an error is raised.
    """
    parser = _create_parser("workflow:check")
    args = parser.parse_args(session.posargs)

    PROJECT_CONFIG.github_workflow_directory.mkdir(parents=True, exist_ok=True)

    outdated_workflows = WorkflowOrchestrator(
        workflow_choice=args.workflow_choice,
        config=PROJECT_CONFIG,
    ).find_differing_workflows()

    if outdated_workflows:
        count = len(outdated_workflows)
        count_label = "workflow is" if count == 1 else "workflows are"
        workflow_list = "\n".join(f"- {workflow}" for workflow in outdated_workflows)
        session.error(f"\n{count} {count_label} out of date:\n" f"{workflow_list}")


@nox.session(name="workflow:generate", python=False)
def generate_workflow(session: Session) -> None:
    """
    Generate or update the specified GitHub workflow or all of them.
    """
    parser = _create_parser("workflow:generate")
    args = parser.parse_args(session.posargs)

    PROJECT_CONFIG.github_workflow_directory.mkdir(parents=True, exist_ok=True)

    WorkflowOrchestrator(
        workflow_choice=args.workflow_choice,
        config=PROJECT_CONFIG,
    ).generate_workflows()
