from collections.abc import Mapping
from importlib.abc import Traversable

import importlib_resources as resources

WORKFLOW_TEMPLATES_DIRECTORY = "exasol.toolbox.templates.github.workflows"


def get_workflow_templates() -> Mapping[str, Traversable]:
    """
    Returns a mapping where keys are filenames without the '.yml' extension.
    """
    package_resources = resources.files(WORKFLOW_TEMPLATES_DIRECTORY)
    return {
        workflow_path.name.removesuffix(".yml"): workflow_path
        for workflow_path in package_resources.iterdir()
        if workflow_path.is_file() and workflow_path.name.endswith(".yml")
    }


WORKFLOW_TEMPLATE_OPTIONS = get_workflow_templates()
