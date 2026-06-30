from collections.abc import Mapping
from pathlib import Path
from typing import Final

import importlib_resources as resources

from exasol.toolbox.util.workflows.exceptions import (
    InvalidWorkflowNameError,
    NotMaintainedWorkflowError,
)

WORKFLOW_TEMPLATES_DIRECTORY = "exasol.toolbox.templates.github.workflows"
NOT_MAINTAINED_WORKFLOW_NAMES: Final[list[str]] = ["slow-checks"]
DOCUMENTATION_ONLY_WORKFLOW_NAMES: Final[list[str]] = ["pr-merge"]


def get_workflow_templates() -> Mapping[str, Path]:
    """
    Returns a mapping for workflow templates, where the keys are filenames without the
    '.yml' extension and the values are the filepaths.
    """
    package_resources = resources.files(WORKFLOW_TEMPLATES_DIRECTORY)
    return {
        workflow_path.name.removesuffix(".yml"): Path(str(workflow_path))
        for workflow_path in package_resources.iterdir()
        if workflow_path.is_file() and workflow_path.name.endswith(".yml")
    }


def validate_workflow_name(workflow_name: str) -> str:
    """
    Validate that the given workflow exists and is allowed in the current context.
    """
    if workflow_name not in WORKFLOW_TEMPLATE_OPTIONS:
        raise InvalidWorkflowNameError(workflow_name, WORKFLOW_TEMPLATE_OPTIONS.keys())
    if workflow_name in NOT_MAINTAINED_WORKFLOW_NAMES:
        raise NotMaintainedWorkflowError(workflow_name)
    return workflow_name


WORKFLOW_TEMPLATE_OPTIONS = get_workflow_templates()
