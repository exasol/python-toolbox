from collections.abc import Mapping
from pathlib import Path

import importlib_resources as resources

WORKFLOW_TEMPLATES_DIRECTORY = "exasol.toolbox.templates.github.workflows"


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


WORKFLOW_TEMPLATE_OPTIONS = get_workflow_templates()
