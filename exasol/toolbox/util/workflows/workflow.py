import difflib
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
    NotMaintainedWorkflowError,
    YamlError,
    YamlKeyError,
)
from exasol.toolbox.util.workflows.patch_workflow import (
    WorkflowCommentedMap,
    WorkflowPatcher,
)
from exasol.toolbox.util.workflows.process_template import WorkflowRenderer
from exasol.toolbox.util.workflows.templates import (
    WORKFLOW_TEMPLATE_OPTIONS,
    validate_workflow_name,
)

ALL: Final[str] = "all"
WORKFLOW_CHOICES: Final[list[str]] = [ALL, *WORKFLOW_TEMPLATE_OPTIONS.keys()]

WorkflowChoice = Annotated[str, f"Should be a value from {WORKFLOW_CHOICES}"]


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    content: str

    @classmethod
    def load_from_template(
        cls,
        template_path: Path,
        github_template_dict: dict[str, Any],
        patch_yaml: WorkflowCommentedMap | None = None,
    ):
        with bound_contextvars(template_file_name=template_path.name):
            logger.debug("Load workflow template: %s", template_path.name)

            if not template_path.exists():
                raise FileNotFoundError(template_path)

            try:
                workflow_renderer = WorkflowRenderer(
                    github_template_dict=github_template_dict,
                    file_path=template_path,
                    patch_yaml=patch_yaml,
                )
                workflow = workflow_renderer.render()
                return cls(content=workflow)
            except (YamlError, YamlKeyError) as ex:
                raise ex
            except Exception as ex:
                # Wrap all other "non-special" exceptions
                raise ValueError(f"Error rendering file: {template_path}") from ex

    def compare_to_file(self, file_path: Path) -> str:
        existing_content = file_path.read_text().strip() if file_path.exists() else ""
        generated_content = self.content.strip()

        diff = difflib.unified_diff(
            existing_content.splitlines(),
            generated_content.splitlines(),
            fromfile=f"existing: {file_path.name}",
            tofile="generated",
            lineterm="",
        )
        return "\n".join(diff)

    def write_to_file(self, file_path: Path) -> None:
        if self.compare_to_file(file_path=file_path) == "":
            logger.debug("Skip up-to-date workflow file %s", file_path.name)
            return
        logger.info("Write workflow file %s", file_path.name)
        file_path.write_text(self.content + "\n")


def _select_workflow_template(workflow_name: WorkflowChoice) -> Mapping[str, Path]:
    """
    Returns a mapping of workflow names to paths. Can be a single item or all workflow
    templates.
    """
    if workflow_name == ALL:
        return WORKFLOW_TEMPLATE_OPTIONS
    return {workflow_name: WORKFLOW_TEMPLATE_OPTIONS[workflow_name]}


def update_workflow(workflow_choice: WorkflowChoice, config: BaseConfig) -> None:
    """
    Updates a selected workflow or all workflows.
    """
    workflow_dict = _select_workflow_template(workflow_choice)
    logger.info(f"Selected workflow(s) to update: {list(workflow_dict.keys())}")

    workflow_patcher = None
    if config.github_workflow_patcher_yaml:
        workflow_patcher = WorkflowPatcher(
            github_template_dict=config.github_template_dict,
            file_path=config.github_workflow_patcher_yaml,
        )

    is_new_project = not any(config.github_workflow_directory.glob("*.yml"))
    for workflow_name in workflow_dict:
        patch_yaml = None
        if workflow_patcher:
            patch_yaml = workflow_patcher.extract_by_workflow(
                workflow_name=workflow_name
            )

        try:
            validate_workflow_name(workflow_name)
        except NotMaintainedWorkflowError:
            if not is_new_project:
                logger.debug(
                    "Skipping not-maintained workflow in older project: %s",
                    workflow_name,
                )
                continue

        try:
            workflow = Workflow.load_from_template(
                template_path=workflow_dict[workflow_name],
                github_template_dict=config.github_template_dict,
                patch_yaml=patch_yaml,
            )
            file_path = config.github_workflow_directory / f"{workflow_name}.yml"
            workflow.write_to_file(file_path=file_path)
        except YamlKeyError as ex:
            raise InvalidWorkflowPatcherEntryError(
                file_path=config.github_workflow_patcher_yaml, entry=ex.entry  # type: ignore
            ) from ex
