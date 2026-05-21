import difflib
from pathlib import Path
from typing import (
    Any,
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
)
from exasol.toolbox.util.workflows.process_template import WorkflowRenderer
from exasol.toolbox.util.workflows.templates import validate_workflow_name
from exasol.toolbox.util.workflows.workflow_orchestrator import (
    WorkflowChoice,
    WorkflowOrchestrator,
)


class Workflow(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    template_path: Path
    output_path: Path
    content: str

    @classmethod
    def load_from_template(
        cls,
        template_path: Path,
        output_directory: Path,
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
                return cls(
                    template_path=template_path,
                    output_path=output_directory / template_path.name,
                    content=workflow_renderer.render(),
                )
            except (YamlError, YamlKeyError) as ex:
                raise ex
            except Exception as ex:
                # Wrap all other "non-special" exceptions
                raise ValueError(f"Error rendering file: {template_path}") from ex

    def compare_to_file(self) -> str:
        existing_content = ""
        if self.output_path.is_file():
            existing_content = self.output_path.read_text().strip()

        generated_content = self.content.strip()

        diff = difflib.unified_diff(
            existing_content.splitlines(),
            generated_content.splitlines(),
            fromfile=f"existing: {self.output_path.name}",
            tofile="generated",
            lineterm="",
        )
        return "\n".join(diff)

    def write_to_file(self) -> None:
        if self.compare_to_file() == "":
            logger.debug("Skip up-to-date workflow file %s", self.output_path.name)
            return
        logger.info("Write workflow file %s", self.output_path.name)
        self.output_path.write_text(self.content + "\n")


def update_workflow(workflow_choice: WorkflowChoice, config: BaseConfig) -> None:
    """
    Updates a selected workflow or all workflows.
    """

    orchestrator = WorkflowOrchestrator(
        workflow_choice=workflow_choice,
        config=config,
    )
    workflow_dict = orchestrator.templates
    logger.info(f"Selected workflow(s) to update: {list(workflow_dict.keys())}")

    workflow_patcher = orchestrator.workflow_patcher
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
                output_directory=config.github_workflow_directory,
                github_template_dict=config.github_template_dict,
                patch_yaml=patch_yaml,
            )
            workflow.write_to_file()
        except YamlKeyError as ex:
            raise InvalidWorkflowPatcherEntryError(
                file_path=config.github_workflow_patcher_yaml, entry=ex.entry  # type: ignore
            ) from ex
