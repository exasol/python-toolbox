from collections.abc import Mapping
from pathlib import Path
from typing import (
    Annotated,
    Any,
    Final,
)

from pydantic import (
    BaseModel,
    ConfigDict,
)
from structlog.contextvars import (
    bound_contextvars,
)

from exasol.toolbox.util.workflows import logger
from exasol.toolbox.util.workflows.exceptions import YamlError
from exasol.toolbox.util.workflows.patch_workflow import WorkflowCommentedMap
from exasol.toolbox.util.workflows.process_template import WorkflowRenderer
from exasol.toolbox.util.workflows.templates import WORKFLOW_TEMPLATE_OPTIONS

ALL: Final[str] = "all"
WORKFLOW_NAMES: Final[list[str]] = [ALL, *WORKFLOW_TEMPLATE_OPTIONS.keys()]

WorkflowName = Annotated[str, f"Should be a value from {WORKFLOW_NAMES}"]


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str

    @classmethod
    def load_from_template(
        cls,
        file_path: Path,
        github_template_dict: dict[str, Any],
        patch_yaml: WorkflowCommentedMap | None = None,
    ):
        with bound_contextvars(template_file_name=file_path.name):
            logger.info(f"Load workflow template: {file_path.name}")

            if not file_path.exists():
                raise FileNotFoundError(file_path)

            try:
                workflow_renderer = WorkflowRenderer(
                    github_template_dict=github_template_dict,
                    file_path=file_path,
                    patch_yaml=patch_yaml,
                )
                workflow = workflow_renderer.render()
                return cls(content=workflow)
            except YamlError as ex:
                raise ex
            except Exception as ex:
                # Wrap all other "non-special" exceptions
                raise ValueError(f"Error rendering file: {file_path}") from ex


def _select_workflows(workflow_name: WorkflowName) -> Mapping[str, Path]:
    if workflow_name == ALL:
        return WORKFLOW_TEMPLATE_OPTIONS
    return {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}
