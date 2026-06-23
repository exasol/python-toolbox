from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.workflows.custom_workflow import CustomWorkflow


class CustomWorkflowEntry(TypedDict):
    exists: bool
    secrets: tuple[str, ...]


class CustomWorkflowExtractor(BaseModel):
    model_config = ConfigDict(frozen=True)

    github_workflow_directory: Path
    sonar_token_name: str
    custom_workflows: tuple[str, ...] = (
        "cd-extension",
        "fast-tests-extension",
        "merge-gate-extension",
        "slow-checks",
    )

    def _build_custom_workflow_entry(
        self,
        workflow: str,
    ) -> CustomWorkflowEntry:
        file_path = self.github_workflow_directory / f"{workflow}.yml"

        secrets: tuple[str, ...] = ()
        if file_path.is_file():
            custom_workflow = CustomWorkflow.load_from_file(file_path=file_path)
            secrets = custom_workflow.extract_secrets()

        return {
            "exists": file_path.exists(),
            "secrets": secrets,
        }

    def _build_merge_gate_entry(
        self, custom_workflows_dict: dict[str, CustomWorkflowEntry]
    ) -> CustomWorkflowEntry:
        return {
            "exists": True,
            "secrets": custom_workflows_dict["merge-gate-extension"]["secrets"]
            + custom_workflows_dict["slow-checks"]["secrets"]
            # from the `report.yml`
            + (self.sonar_token_name,),
        }

    def build_custom_workflow_dict(
        self,
    ) -> dict[str, CustomWorkflowEntry]:
        """
        Build the template metadata used to specify whether a custom workflow is
        present and which secrets its caller must pass through.

        The secret names are extracted from the reusable workflow itself via
        :meth:`CustomWorkflow.extract_secrets`.
        """

        custom_workflows_dict = {}
        for workflow in self.custom_workflows:
            custom_workflows_dict[workflow] = self._build_custom_workflow_entry(
                workflow=workflow,
            )

        custom_workflows_dict["merge-gate"] = self._build_merge_gate_entry(
            custom_workflows_dict
        )
        return custom_workflows_dict
