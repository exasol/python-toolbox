from __future__ import annotations

from collections.abc import (
    Iterator,
    Mapping,
)
from functools import cached_property
from pathlib import Path
from typing import (
    Annotated,
    Final,
)

from pydantic import BaseModel

from exasol.toolbox.config import BaseConfig
from exasol.toolbox.util.workflows import logger
from exasol.toolbox.util.workflows.exceptions import (
    InvalidWorkflowPatcherEntryError,
    NotMaintainedWorkflowError,
    YamlKeyError,
)
from exasol.toolbox.util.workflows.patch_workflow import (
    WorkflowCommentedMap,
    WorkflowPatcher,
)
from exasol.toolbox.util.workflows.templates import (
    WORKFLOW_TEMPLATE_OPTIONS,
    validate_workflow_name,
)
from exasol.toolbox.util.workflows.workflow import Workflow

ALL: Final[str] = "all"
WorkflowChoice = Annotated[
    str, f"Should be a value from {[ALL, *WORKFLOW_TEMPLATE_OPTIONS.keys()]}"
]
WORKFLOW_CHOICES: Final[list[str]] = [ALL, *WORKFLOW_TEMPLATE_OPTIONS.keys()]


class WorkflowOrchestrator(BaseModel):
    """Orchestrate workflow rendering, comparison, and writing."""

    workflow_choice: WorkflowChoice
    config: BaseConfig

    @cached_property
    def templates(self) -> Mapping[str, Path]:
        """
        A mapping of workflow templates names to paths. This can be a single
        item or all workflow templates.
        """
        if self.workflow_choice == ALL:
            return WORKFLOW_TEMPLATE_OPTIONS
        return {self.workflow_choice: WORKFLOW_TEMPLATE_OPTIONS[self.workflow_choice]}

    @cached_property
    def workflow_patcher(self) -> WorkflowPatcher | None:
        if not self.config.github_workflow_patcher_yaml:
            return None
        return WorkflowPatcher(
            github_template_dict=self.config.github_template_dict,
            file_path=self.config.github_workflow_patcher_yaml,
        )

    def _extract_workflow_patch(
        self, workflow_name: str
    ) -> WorkflowCommentedMap | None:
        """
        Return the patch data for a workflow, or ``None`` if no patcher is configured.
        """
        if self.workflow_patcher is None:
            return None
        return self.workflow_patcher.extract_by_workflow(workflow_name=workflow_name)

    def _is_new_project(self) -> bool:
        """
        A project is considered new if no YML files are present in the GitHub directory.
        """
        return not any(self.config.github_workflow_directory.glob("*.yml"))

    def _iter_workflows(self) -> Iterator[Workflow]:
        logger.info(f"Selected workflow(s) to update: {list(self.templates.keys())}")
        is_new_project = self._is_new_project()
        for workflow_name, template_path in self.templates.items():
            patch_yaml = self._extract_workflow_patch(workflow_name=workflow_name)

            if self._skip_workflow(workflow_name, is_new_project):
                continue

            yield self._load_workflow(
                template_path=template_path, patch_yaml=patch_yaml
            )

    def _load_workflow(
        self, template_path: Path, patch_yaml: WorkflowCommentedMap | None
    ):
        from exasol.toolbox.util.workflows.workflow import Workflow

        try:
            return Workflow.load_from_template(
                template_path=template_path,
                output_directory=self.config.github_workflow_directory,
                github_template_dict=self.config.github_template_dict,
                patch_yaml=patch_yaml,
            )
        except YamlKeyError as ex:
            raise InvalidWorkflowPatcherEntryError(
                file_path=self.config.github_workflow_patcher_yaml, entry=ex.entry
            ) from ex

    def _skip_workflow(self, workflow_name: str, is_new_project: bool) -> bool:
        """
        Return ``True`` if the workflow should be skipped because it is not maintained
        by the PTB, otherwise return ``False``.
        """
        try:
            validate_workflow_name(workflow_name)
        except NotMaintainedWorkflowError:
            if not is_new_project:
                logger.debug(
                    "Skipping not-maintained workflow in older project: %s",
                    workflow_name,
                )
                return True
        return False

    def write_workflows(self) -> None:
        """
        Render the selected workflows and write them to disk.
        """
        for workflow in self._iter_workflows():
            workflow.write_to_file()
