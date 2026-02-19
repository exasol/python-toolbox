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

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.util.workflows import logger
from exasol.toolbox.util.workflows.exceptions import (
    InvalidWorkflowPatcherEntryError,
    YamlError,
    YamlKeyError,
)
from exasol.toolbox.util.workflows.patch_workflow import (
    WorkflowCommentedMap,
    WorkflowPatcher,
)
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
            except (YamlError, YamlKeyError) as ex:
                raise ex
            except Exception as ex:
                # Wrap all other "non-special" exceptions
                raise ValueError(f"Error rendering file: {file_path}") from ex

    def write_to_file(self, file_path: Path) -> None:
        logger.info(f"Write out workflow: {file_path.name}", file_path=file_path)
        file_path.write_text(self.content + "\n")


def _select_workflow_template(workflow_name: WorkflowName) -> Mapping[str, Path]:
    """
    Returns a mapping of a workflow template or of all workflow templates.
    """
    if workflow_name == ALL:
        return WORKFLOW_TEMPLATE_OPTIONS
    return {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}


def update_selected_workflow(workflow_name: WorkflowName, config: BaseConfig) -> None:
    """
    Updates a selected workflow or all workflows.
    """
    workflow_dict = _select_workflow_template(workflow_name)
    logger.info(f"Selected workflow(s) to update: {list(workflow_dict.keys())}")

    workflow_patcher = None
    if config.github_workflow_patcher_yaml:
        workflow_patcher = WorkflowPatcher(
            github_template_dict=config.github_template_dict,
            file_path=config.github_workflow_patcher_yaml,
        )

    for workflow_name in workflow_dict:
        patch_yaml = None
        if workflow_patcher:
            patch_yaml = workflow_patcher.extract_by_workflow(
                workflow_name=workflow_name
            )

        try:
            workflow = Workflow.load_from_template(
                file_path=workflow_dict[workflow_name],
                github_template_dict=config.github_template_dict,
                patch_yaml=patch_yaml,
            )
            file_path = config.github_workflow_directory / f"{workflow_name}.yml"
            workflow.write_to_file(file_path=file_path)
        except YamlKeyError as ex:
            raise InvalidWorkflowPatcherEntryError(
                file_path=config.github_workflow_patcher_yaml, entry=ex.entry  # type: ignore
            ) from ex
